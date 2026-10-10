#!/usr/bin/env python3
"""Consolida extratos TCESP para QA. Nao considera extracao conciliacao com DCA."""
import csv
import json
import pathlib
import sys

CITIES = ("cabreuva", "campo-limpo-paulista", "itupeva", "jarinu", "jundiai", "louveira", "varzea-paulista")
YEARS = (2023, 2024)

def main(folder):
    folder = pathlib.Path(folder)
    records, errors = [], []
    for year in YEARS:
        for city in CITIES:
            path = folder / f"{city}_{year}.json"
            record = dict(municipio_slug=city, ano=year, situacao_extracao="ERRO",
                          fonte_tcesp=f"https://transparencia.tce.sp.gov.br/sites/default/files/csv/despesas-{city}-{year}.zip",
                          linhas_tcesp="", investimento_liquidado_tcesp_rs="",
                          investimento_liquidado_dca_rs="", diferenca_rs="",
                          situacao_conciliacao="PENDENTE_DCA", arquivo_extrato=path.name)
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                assert data["slug"] == city and data["year"] == year, "municipio/ano divergente"
                assert not data.get("bad_values"), "valores invalidos no TCESP"
                totals = data.get("totals_44_by_type", {})
                matches = [v for k, v in totals.items() if str(k).strip().casefold() == "valor liquidado"]
                assert len(matches) == 1, "total liquidado do grupo 44 ausente ou duplicado"
                assert isinstance(matches[0], (int,float)), "valor nao numerico"
                record.update(situacao_extracao="OK", linhas_tcesp=data["rows"],
                              investimento_liquidado_tcesp_rs=f"{matches[0]:.2f}")
            except (OSError, ValueError, KeyError, AssertionError, TypeError) as exc:
                errors.append(f"{city} {year}: {exc}")
            records.append(record)
    with (folder / "controle_conciliacao.csv").open("w", newline="", encoding="utf-8-sig") as fp:
        writer = csv.DictWriter(fp, fieldnames=records[0].keys(), delimiter=";")
        writer.writeheader()
        writer.writerows(records)
    summary = dict(esperados=len(records), extraidos_com_sucesso=len(records)-len(errors),
                   pendentes_conciliacao_dca=len(records), erros=errors,
                   observacao="Extracao TCESP nao e conciliacao DCA; requer comparacao com a base canonica.")
    (folder/"qa_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return int(bool(errors))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv)>1 else "build/rmj-tcesp-2023-2024"))
