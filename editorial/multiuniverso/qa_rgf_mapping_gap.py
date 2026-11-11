#!/usr/bin/env python3
"""Detecta lacuna estrutural de contas monetarias RGF no recorte historico estadual."""
import json,pathlib,yaml
root=pathlib.Path(__file__).resolve().parents[2]
with (root/"data/mappings/sp645_typology_2021_2025.yml").open(encoding="utf-8") as f: hist=yaml.safe_load(f)
with (root/"data/mappings/base_multifuentes_sp645_2025.yml").open(encoding="utf-8") as f: recent=yaml.safe_load(f)
monetary=("rgf_despesa_total_pessoal","rgf02_divida_consolidada","rgf02_divida_consolidada_liquida")
ratios=("dtp_pct_rcl","dc_pct_rcl","dcl_pct_rcl")
missing=[v for v in monetary if v not in hist["variables"]]
ratio_mapped=[v for v in ratios if hist["variables"].get(v,{}).get("availability_start")==2023]
current=[v for v in monetary if recent["variables"].get(v,{}).get("availability_start")==2025]
report={"historical_money_unmapped":missing,"historical_ratios_since_2023":ratio_mapped,"money_in_2025_mapping":current,"gate":"blocked" if missing else "mapping_coverage_restored","note":"Mapeamento não prova status do banco nem integra registros automaticamente."}
out=root/"build/rgf-e2/qa_rgf_mapping_gap.json"
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(report,ensure_ascii=False))
assert len(ratio_mapped)==3 and len(current)==3
# Diagnostico explicito; nao publicar nem declarar cobertura enquanto lacuna existir.
if missing:raise SystemExit("BLOQUEADO: RGF monetario de 2023-2024 nao incluído na rota historica estadual")
