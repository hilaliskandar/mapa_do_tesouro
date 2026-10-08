from __future__ import annotations

from dataclasses import dataclass


ANNEX_01 = "RGF-Anexo 01"
ANNEX_05 = "RGF-Anexo 05"
NON_LINKED_TOTAL = "TOTAL DOS RECURSOS NÃO VINCULADOS (I)"


@dataclass(frozen=True)
class FieldSpec:
    cod_conta: str
    coluna: str
    conta: str | None = None


ANNEX01_FIELDS = {
    "rgf_despesa_total_pessoal": FieldSpec(
        cod_conta="DespesaComPessoalTotal",
        conta="DESPESA TOTAL COM PESSOAL - DTP (VI) = (IIIa + IIIb)",
        coluna="Valor",
    ),
    "rgf_rcl_denominador_legal": FieldSpec(
        cod_conta="ReceitaCorrenteLiquidaAjustada",
        conta="= RECEITA CORRENTE LÍQUIDA AJUSTADA PARA CÁLCULO DOS LIMITES DA DESPESA COM PESSOAL (V)",
        coluna="Valor",
    ),
    "rgf_dtp_percentual_rcl": FieldSpec(
        cod_conta="DespesaComPessoalTotal",
        conta="DESPESA TOTAL COM PESSOAL - DTP (VI) = (IIIa + IIIb)",
        coluna="% sobre a RCL Ajustada",
    ),
}

ANNEX05_FIELDS = {
    "rgf_caixa_bruta_nao_vinculada": FieldSpec(
        cod_conta="DisponibilidadeDeCaixaBruta",
        coluna="DISPONIBILIDADE DE CAIXA BRUTA (a)",
    ),
    "rgf_rp_liquidados_anteriores_nao_vinculados": FieldSpec(
        cod_conta="RestosAPagarLiquidadosENaoPagosDeExerciciosAnteriores",
        coluna="De Exercícios Anteriores (b)",
    ),
    "rgf_rp_liquidados_exercicio_nao_vinculados": FieldSpec(
        cod_conta="RestosAPagarLiquidadosENaoPagosDoExercicio",
        coluna="Do Exercício (c)",
    ),
    "rgf_rp_nao_liquidados_anteriores_nao_vinculados": FieldSpec(
        cod_conta="RestosAPagarEmpenhadosENaoLiquidadosDeExerciciosAnteriores",
        coluna="Restos a Pagar Empenhados e Não Liquidados de Exercícios Anteriores (d)",
    ),
    "rgf_demais_obrigacoes_nao_vinculadas": FieldSpec(
        cod_conta="DemaisObrigacoesFinanceiras",
        coluna="Demais Obrigações Financeiras (e)",
    ),
    "rgf_caixa_liquida_antes_rpnp": FieldSpec(
        cod_conta="DisponibilidadeDeCaixaLiquida",
        coluna="DISPONIBILIDADE DE CAIXA LÍQUIDA (ANTES DA INSCRIÇÃO EM RESTOS A PAGAR NÃO PROCESSADOS DO EXERCÍCIO) (g)=(a-(b+c+d+e)-f)",
    ),
    "rgf_rp_nao_liquidados_exercicio_nao_vinculados": FieldSpec(
        cod_conta="RestosAPagarEmpenhadosENaoLiquidadosDoExercicio",
        coluna="RESTOS A PAGAR EMPENHADOS E NÃO LIQUIDADOS DO EXERCÍCIO (h)",
    ),
    "rgf_caixa_liquida_apos_rpnp": FieldSpec(
        cod_conta="DisponibilidadeDeCaixaLiquidaAposRP",
        coluna="DISPONIBILIDADE DE CAIXA LÍQUIDA (APÓS A INSCRIÇÃO EM RESTOS A PAGAR NÃO PROCESSADOS DO EXERCÍCIO) (i) = (g - h)",
    ),
}


def _find_unique(items: list[dict], spec: FieldSpec, *, conta: str | None = None) -> tuple[float | None, list[dict]]:
    matches = []
    for item in items:
        if item.get("cod_conta") != spec.cod_conta:
            continue
        if item.get("coluna") != spec.coluna:
            continue
        expected_conta = conta if conta is not None else spec.conta
        if expected_conta is not None and item.get("conta") != expected_conta:
            continue
        matches.append(item)

    if not matches:
        return None, []
    if len(matches) != 1:
        return None, [{"type": "ambiguous_match", "field": spec.cod_conta, "count": len(matches)}]

    value = matches[0].get("valor")
    return (float(value) if value is not None else None), []


def normalize_annex01(payload: dict) -> dict:
    items = payload.get("items", [])
    row = {
        "cod_ibge": str(payload.get("entity_id") or ""),
        "ano": int(payload["year"]),
    }
    issues: list[dict] = []

    for field, spec in ANNEX01_FIELDS.items():
        value, found_issues = _find_unique(items, spec)
        row[field] = value
        issues.extend({**issue, "variable": field} for issue in found_issues)

    row["qa_issue_count"] = len(issues)
    row["issues"] = issues
    return row


def normalize_annex05(payload: dict) -> dict:
    items = payload.get("items", [])
    row = {
        "cod_ibge": str(payload.get("entity_id") or ""),
        "ano": int(payload["year"]),
    }
    issues: list[dict] = []

    for field, spec in ANNEX05_FIELDS.items():
        value, found_issues = _find_unique(items, spec, conta=NON_LINKED_TOTAL)
        row[field] = value
        issues.extend({**issue, "variable": field} for issue in found_issues)

    row["qa_issue_count"] = len(issues)
    row["issues"] = issues
    return row
