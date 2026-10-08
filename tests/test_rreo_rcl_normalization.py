import gzip
import json

from pipeline.normalize.rreo_rcl import normalize_tree


def _write(path, items):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": "SICONFI",
        "endpoint": "rreo",
        "year": 2025,
        "entity_id": path.name.removesuffix(".json.gz"),
        "parameters": {"nr_periodo": 6},
        "status": "observado" if items else "ausente",
        "pages": 1,
        "requests": 1,
        "items": items,
    }
    with gzip.open(path, "wt", encoding="utf-8") as handle:
        json.dump(payload, handle)


def test_rreo_rcl_normalization_preserves_absence(tmp_path):
    root = tmp_path / "raw"
    annex = root / "rreo-anexo-03" / "2025"
    _write(
        annex / "3501608.json.gz",
        [
            {
                "cod_conta": "ReceitaCorrenteLiquida",
                "conta": "RECEITA CORRENTE LÍQUIDA (III) = (I - II)",
                "coluna": "TOTAL (ÚLTIMOS 12 MESES)",
                "valor": 123.5,
                "populacao": 1000,
            }
        ],
    )
    _write(annex / "3501707.json.gz", [])

    output = tmp_path / "rcl.csv"
    result = normalize_tree(root, output)

    rows = output.read_text(encoding="utf-8").splitlines()
    assert result["rows"] == 2
    assert result["observed_rcl_rows"] == 1
    assert result["issues"] == 0
    assert "123.5" in rows[1]
    assert rows[2].startswith("3501707,2025,,")
