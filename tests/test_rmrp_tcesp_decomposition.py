import csv
import json
import pytest
from editorial.rmrp.build_decomposicao_tcesp import build


def prepare(tmp_path):
    roster=tmp_path/"cities.csv";raw=tmp_path/"raw";raw.mkdir()
    with roster.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["codigo_ibge","municipio","slug"])
        w.writeheader();w.writerow({"codigo_ibge":"3543402","municipio":"Ribeirão Preto","slug":"ribeirao-preto"})
    for year,cents in [(2023,100),(2024,250),(2025,180)]:
        doc={"slug":"ribeirao-preto","year":year,"bad_values":0,
             "investimento_44_liquidado_centavos":cents,
             "programas_44_liquidado_completos":[["10","Programa",cents/100,cents]],
             "acoes_44_liquidado_completas":[["10","100","Ação",cents/100,cents]]}
        (raw/f"ribeirao-preto_{year}.json").write_text(json.dumps(doc))
    return roster,raw


def test_three_years_reconcile_program_action(tmp_path):
    roster,raw=prepare(tmp_path)
    output=tmp_path/"out.csv"
    result=build(roster,raw,output,expected=1)
    assert result["reconciliations"]==4
    assert result["source_documents"]==3
    with output.open(encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f,delimiter=";"))
    assert len(rows)==4
    assert sorted(int(r["variacao_centavos"]) for r in rows)==[-70,-70,150,150]


def test_missing_year_never_imputed(tmp_path):
    roster,raw=prepare(tmp_path)
    (raw/"ribeirao-preto_2024.json").unlink()
    with pytest.raises(FileNotFoundError):
        build(roster,raw,tmp_path/"out.csv",expected=1)
    assert not (tmp_path/"out.csv").exists()


def test_unbalanced_extract_rejected(tmp_path):
    roster,raw=prepare(tmp_path)
    p=raw/"ribeirao-preto_2025.json"
    data=json.loads(p.read_text());data["investimento_44_liquidado_centavos"]=999
    p.write_text(json.dumps(data))
    with pytest.raises(ValueError,match="aggregate mismatch"):
        build(roster,raw,tmp_path/"out.csv",expected=1)
