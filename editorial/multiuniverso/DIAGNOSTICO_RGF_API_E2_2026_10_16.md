# Diagnóstico RGF × API E2 — 16/10/2026

## Fonte e teste
O candidato estadual RGF 2023–2024 aprovado no Gate E foi recuperado do artifact `gate-e-rgf-history-2023-2024-corrected`, execução `37776058337`, com SHA-256 CSV `7faef8188fd56bff6bb8031dfe3a8eeec11fe56e67f986bdc0007a4ee7646eeb`. A comparação com a API E2 é conduzida por `qa_rgf_gate_e_api.py` no workflow `audit-rgf-gate-e-e2.yml`.

## Falha de homologação detectada
A primeira execução `38897261022` terminou **failure**, com relatório de diagnóstico ID `12044128852`. Em 1.371 pares numéricos elegíveis, houve 1.371 diferenças aparentes de escala: percentuais legais do RGF são armazenados no E2 como razões (ex.: 0,4099) e no candidato de referência em pontos percentuais (40,99%). Também foram identificados 1.371 registros com informação no candidato e ausência de observação correspondente na série da API E2. Esses grupos não devem ser somados como se representassem uma quantidade de casos únicos. São dimensões diferentes do mesmo exame.

As regras de exibição dos boletins e fichas foram corrigidas no ramo: indicadores legais RGF/RCL usam fator 100 somente na apresentação; razões derivadas cujas fórmulas já incorporam 100 não recebem multiplicação. O comparador passou a converter a unidade antes de testar diferenças. **A ausência histórica continua sendo condição de reprovação**, não é imputada nem suprimida da QA.

## Consequência
Não declarar homologação externa RGF. Exigir a resolução das ausências históricas município–ano–campo, verificando se correspondem a lacuna na exportação da API, escopo de indicadores ou material de origem. CAPAG permanece condicionado à comparação com a planilha oficial da posição de setembro/2026, preservando `n/d` como categoria oficial. RREO permanece pendente de arquivo-fonte do anexo e período correspondentes.

A checagem DCA independente já aprovada permanece válida apenas para os 68 cotejos efetuados; não valida, por consequência, RGF, RREO ou CAPAG. O PR #198 segue bloqueado para publicação.
