from __future__ import annotations

import argparse
import csv
import hashlib
import sqlite3
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import openpyxl
import yaml

from pipeline.build.init_db import initialize_database
from pipeline.build.load_catalog import load_catalog

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SCHEMA = ROOT / "data" / "schema" / "001_initial.sql"
DEFAULT_CATALOG = ROOT / "data" / "catalogs" / "variables_core.yml"
DEFAULT_MAPPING = ROOT / "data" / "mappings" / "base_multifuentes_v0_4.yml"
VERSION_FILE = ROOT / "VERSION"


def read_app_version() -> str | None:
    if not VERSION_FILE.exists():
        return None
    version = VERSION_FILE.read_text(encoding="utf-8").strip()
    return version or None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def normalize_ibge(value: object) -> str:
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    code = str(value).strip()
    if len(code) != 7 or not code.isdigit():
        raise ValueError(f"Codigo IBGE invalido: {value!r}")
    return code


def read_tabular_source(path: Path, source: dict) -> tuple[list[str], list[tuple], str, str]:
    source_format = str(source.get("format", "xlsx")).lower()

    if source_format == "xlsx":
        workbook = openpyxl.load_workbook(path, read_only=True, data_only=True)
        try:
            sheet_name = source_location
            worksheet = workbook[sheet_name]
            iterator = worksheet.iter_rows(values_only=True)
            headers = [str(value) if value is not None else "" for value in next(iterator)]
            rows = list(iterator)
        finally:
            workbook.close()
        return (
            headers,
            rows,
            sheet_name,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    if source_format == "csv":
        delimiter = str(source.get("delimiter", ","))
        encoding = str(source.get("encoding", "utf-8-sig"))
        with path.open("r", encoding=encoding, newline="") as handle:
            reader = csv.reader(handle, delimiter=delimiter)
            headers = next(reader)
            rows = [tuple(row) for row in reader]
        return headers, rows, source.get("sheet", "CSV"), "text/csv"

    raise ValueError(f"Formato de fonte nao suportado: {source_format!r}")


def import_multifuentes(
    workbook: Path,
    database: Path,
    *,
    schema: Path | None = None,
    catalog: Path = DEFAULT_CATALOG,
    mapping_path: Path = DEFAULT_MAPPING,
    overwrite: bool = False,
    build_timestamp: str | None = None,
    universe_id: str | None = None,
    universe_name: str | None = None,
    universe_description: str | None = None,
    universe_type: str | None = None,
) -> dict:
    mapping = load_yaml(mapping_path)
    source = mapping["source"]
    universe = mapping.get("universe", {})
    universe_id = universe_id or universe.get("id") or "TIC_TIM_30"
    universe_name = universe_name or universe.get("name") or universe_id
    universe_description = (
        universe_description
        or universe.get("description")
        or f"Universo analitico {universe_name}."
    )
    universe_type = universe_type or universe.get("type") or "analitico"

    if database.exists():
        if not overwrite:
            raise FileExistsError(
                f"{database} ja existe. Use --overwrite para reconstruir o artefato."
            )
        database.unlink()

    initialize_database(database, schema=schema)
    connection = sqlite3.connect(database)
    connection.execute("PRAGMA foreign_keys = ON")
    load_catalog(database, catalog)
    schema_version_row = connection.execute(
        "SELECT value FROM schema_metadata WHERE key='schema_version'"
    ).fetchone()
    schema_version = schema_version_row[0] if schema_version_row else "unknown"

    source_hash = sha256(workbook)
    expected_sha256 = source.get("expected_sha256")
    if expected_sha256 and source_hash != expected_sha256:
        raise ValueError(
            f"SHA-256 inesperado para a fonte: {source_hash} != {expected_sha256}"
        )

    headers, rows, source_location, source_mime_type = read_tabular_source(
        workbook, source
    )
    try:
        column_index = {name: index for index, name in enumerate(headers)}

        required_columns = set(mapping["keys"].values())
        required_columns.update(spec["column"] for spec in mapping["variables"].values())
        missing_columns = sorted(required_columns - set(column_index))
        if missing_columns:
            raise ValueError(f"Colunas ausentes na base: {missing_columns}")

        code_col = column_index[mapping["keys"]["codigo_ibge"]]
        name_col = column_index[mapping["keys"]["municipio"]]
        year_col = column_index[mapping["keys"]["ano"]]

        pairs = {
            (normalize_ibge(row[code_col]), int(row[year_col]))
            for row in rows
        }
        municipalities = {
            normalize_ibge(row[code_col]): str(row[name_col]).strip()
            for row in rows
        }
        years = sorted({int(row[year_col]) for row in rows})
        expected_years = list(
            range(
                int(source["expected_years"]["start"]),
                int(source["expected_years"]["end"]) + 1,
            )
        )

        if len(rows) != int(source["expected_rows"]):
            raise ValueError(
                f"Quantidade de linhas inesperada: {len(rows)} "
                f"!= {source['expected_rows']}"
            )
        if len(municipalities) != int(source["expected_municipalities"]):
            raise ValueError(
                f"Quantidade de municipios inesperada: {len(municipalities)} "
                f"!= {source['expected_municipalities']}"
            )
        if years != expected_years:
            raise ValueError(f"Anos inesperados: {years} != {expected_years}")
        if len(pairs) != len(rows):
            raise ValueError("Foram encontrados pares municipio-ano duplicados.")

        build_prefix = str(source.get("build_prefix", "multifuentes"))
        build_id = f"{build_prefix}-{source_hash[:12]}"
        artifact_id = f"{source['source_id']}:{source_hash[:16]}"
        timestamp = build_timestamp or datetime.now().astimezone().isoformat(timespec="seconds")

        connection.execute(
            """
            INSERT INTO universo(universo_id,nome,descricao,tipo)
            VALUES (?,?,?,?)
            """,
            (
                universe_id,
                universe_name,
                universe_description,
                universe_type,
            ),
        )

        for code, name in sorted(municipalities.items()):
            connection.execute(
                "INSERT INTO municipio(codigo_ibge,nome,uf) VALUES (?,?,?)",
                (code, name, "SP"),
            )
            connection.execute(
                """
                INSERT INTO universo_municipio(universo_id,codigo_ibge)
                VALUES (?,?)
                """,
                (universe_id, code),
            )

        connection.execute(
            """
            INSERT INTO build(
                build_id,build_timestamp,data_version,methodology_version,
                app_version,schema_version,data_sha256,qa_status,notes
            ) VALUES (?,?,?,?,?,?,?,?,?)
            """,
            (
                build_id,
                timestamp,
                source["data_version"],
                "0.1.0",
                read_app_version(),
                schema_version,
                source_hash,
                "candidate",
                "Carga tabular auditavel. data_sha256 corresponde ao artefato integrado de origem.",
            ),
        )
        connection.execute(
            """
            INSERT INTO build_source(
                build_id,fonte_id,source_version,retrieved_at,source_sha256
            ) VALUES (?,?,?,?,?)
            """,
            (
                build_id,
                source["source_id"],
                source["data_version"],
                timestamp,
                source_hash,
            ),
        )
        connection.execute(
            """
            INSERT INTO artefato_fonte(
                artefato_id,fonte_id,nome,source_version,
                retrieved_at,sha256,mime_type,observacao
            ) VALUES (?,?,?,?,?,?,?,?)
            """,
            (
                artifact_id,
                source["source_id"],
                workbook.name,
                source["data_version"],
                timestamp,
                source_hash,
                source_mime_type,
                "Artefato tabular integrado usado como fonte de carga.",
            ),
        )

        coverage = defaultdict(
            lambda: {"observado": 0, "ausente": 0, "nao_aplicavel": 0}
        )

        provenance_written = 0

        for row_number, row in enumerate(rows, start=2):
            code = normalize_ibge(row[code_col])
            year = int(row[year_col])

            for variable_id, spec in mapping["variables"].items():
                availability_start = int(spec["availability_start"])
                availability_end = int(spec["availability_end"])
                value_index = column_index[spec["column"]]
                raw_value = row[value_index] if value_index < len(row) else None

                if year < availability_start or year > availability_end:
                    status = "nao_aplicavel"
                    value_num = None
                    value_text = None
                elif raw_value is None or (
                    isinstance(raw_value, str) and not raw_value.strip()
                ):
                    status = "ausente"
                    value_num = None
                    value_text = None
                else:
                    status = "observado"
                    if spec["value_type"] == "numeric":
                        value_num = float(raw_value) * float(spec.get("scale", 1.0))
                        value_text = None
                    else:
                        value_num = None
                        value_text = str(raw_value)

                connection.execute(
                    """
                    INSERT INTO observacao(
                        codigo_ibge,ano,variavel_id,fonte_id,
                        valor_num,valor_texto,status,
                        referencia_origem,build_id
                    ) VALUES (?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        code,
                        year,
                        variable_id,
                        spec["source_id"],
                        value_num,
                        value_text,
                        status,
                        f"{source['sheet']}!{spec['column']}",
                        build_id,
                    ),
                )
                connection.execute(
                    """
                    INSERT INTO observacao_proveniencia(
                        codigo_ibge,ano,variavel_id,sequencia,tipo,
                        artefato_id,origem_aba,origem_campo,
                        origem_referencia,build_id
                    ) VALUES (?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        code,
                        year,
                        variable_id,
                        1,
                        "campo_fonte",
                        artifact_id,
                        source_location,
                        spec["column"],
                        f"{source['sheet']}!{spec['column']};row={row_number}",
                        build_id,
                    ),
                )
                provenance_written += 1
                coverage[(variable_id, year)][status] += 1

        expected_per_year = len(municipalities)
        for (variable_id, year), counts in sorted(coverage.items()):
            connection.execute(
                """
                INSERT INTO cobertura(
                    variavel_id,ano,universo_id,esperado,
                    observado,ausente,nao_aplicavel
                ) VALUES (?,?,?,?,?,?,?)
                """,
                (
                    variable_id,
                    year,
                    universe_id,
                    expected_per_year,
                    counts["observado"],
                    counts["ausente"],
                    counts["nao_aplicavel"],
                ),
            )

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    return {
        "build_id": build_id,
        "source_sha256": source_hash,
        "rows": len(rows),
        "municipalities": len(municipalities),
        "years": years,
        "variables": len(mapping["variables"]),
        "observations": len(rows) * len(mapping["variables"]),
        "provenance_rows": provenance_written,
        "source_artifact_id": artifact_id,
        "schema_version": schema_version,
        "universe_id": universe_id,
        "universe_name": universe_name,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Importa a base multifuentes TIC-TIM para o SQLite canonico."
    )
    parser.add_argument("workbook", type=Path)
    parser.add_argument(
        "--database",
        type=Path,
        default=ROOT / "data" / "financas_municipais_sp.sqlite",
    )
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    result = import_multifuentes(
        args.workbook,
        args.database,
        catalog=args.catalog,
        mapping_path=args.mapping,
        overwrite=args.overwrite,
    )
    for key, value in result.items():
        print(f"{key}={value}")


if __name__ == "__main__":
    main()
