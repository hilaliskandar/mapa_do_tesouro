# Diagnóstico RGF × API E2 — 16/10/2026

## Fonte e teste
O candidato estadual RGF 2023–2024 aprovado no Gate E foi recuperado do artifact `gate-e-rgf-history-2023-2024-corrected`, execução `37776058337`, com SHA-256 CSV `7faef8188fd56bff6bb8031dfe3a8eeec11fe56e67f986bdc0007a4ee7646eeb`. A comparação com a API E2 é conduzida por `qa_rgf_gate_e_api.py` no workflow `audit-rgf-gate-e-e2.yml`.

## Falha de homologação detectada
A primeira execução `38897261022` terminou **failure**, com relatório de diagnóstico ID `12044128852`. Em 1.371 pares numéricos elegíveis, houve 1.371 diferenças aparentes de escala: percentuais legais do RGF são armazenados no E2 como razões (ex.: 0,4099) e no candidato de referência em pontos percentuais (40,99%). Também foram identificados 1.371 registros com informação no candidato e ausência de observação correspondente na série da API E2. Esses grupos não devem ser somados como se representassem uma quantidade de casos únicos. São dimensões diferentes do mesmo exame.

As regras de exibição dos boletins e fichas foram corrigidas no ramo: indicadores legais RGF/RCL usam fator 100 somente na apresentação; razões derivadas cujas fórmulas já incorporam 100 não recebem multiplicação. O comparador passou a converter a unidade antes de testar diferenças. **A ausência histórica continua sendo condição de reprovação**, não é imputada nem suprimida da QA.

## Consequência
Não declarar homologação externa RGF. Exigir a resolução das ausências históricas município–ano–campo, verificando se correspondem a lacuna na exportação da API, escopo de indicadores ou material de origem. CAPAG permanece condicionado à comparação com a planilha oficial da posição de setembro/2026, preservando `n/d` como categoria oficial. RREO permanece pendente de arquivo-fonte do anexo e período correspondentes.

A checagem DCA independente já aprovada permanece válida apenas para os 68 cotejos efetuados; não valida, por consequência, RGF, RREO ou CAPAG. O PR #198 segue bloqueado para publicação.

## Reexecução tipificada após correção de escala

Execução [38898420526](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38898420526), commit `63f4396cf3c8a05a31a82497870774c6d77a9352`. Relatório diagnóstico artefato `12045301229` (`qa_rgf_api_e2.json`).

- 1.371 comparações entre dois valores numéricos: **zero divergências após normalizar a escala**.
- 1.371 conflitos de disponibilidade: todos identificados como `status_nao_aplicavel` na API editorial, apesar de haver número no candidato RGF validado.
- Distribuição das ocorrências de estado: despesa total com pessoal 465; dívida consolidada líquida 465; dívida consolidada 441.
- Não houve nenhum caso nas categorias `year_absent`, `null_value` e `variable_not_exported` entre os conflitos assinalados.
- Os totais contam ocorrências por universo × município × ano × variável; municípios sobrepostos são repetidos entre universos. Não interpretar como número de municípios únicos.

**Decisão:** manter `strict_pass=false` e o bloqueio de publicação. A existência dos valores na referência aprovada não autoriza sobrescrever automaticamente os registros `nao_aplicavel` da API. Deve-se investigar na camada de ingestão, harmonização e exportação o motivo e a proveniência dessa atribuição de status. Depois, refazer a integração a partir do banco canônico e executar novamente a paridade, respeitando os arquivos oficiais e o controle de versões.

## Causa estrutural identificada nos mapeamentos

A investigação dos arquivos fonte distinguiu duas rotas de ingestão:

- `data/mappings/sp645_typology_2021_2025.yml`: período estadual 2021–2025; os três indicadores de razões legais `dtp_pct_rcl`, `dc_pct_rcl` e `dcl_pct_rcl` estão mapeados desde **2023**, com `scale: 0.01`. O catálogo **não inclui** os três valores monetários RGF `rgf_despesa_total_pessoal`, `rgf02_divida_consolidada` e `rgf02_divida_consolidada_liquida`.
- `data/mappings/base_multifuentes_sp645_2025.yml`: janela somente **2025**, com as três contas monetárias RGF oficiais.
- `data/mappings/base_multifuentes_v0_4.yml`: mapeamento inicial TIC-TIM com janela 2015–2025; esta existência documental não comprova alimentação equivalente da base estadual E2.

Em `pipeline/ingest/import_multifuentes.py`, `nao_aplicavel` é atribuído quando o ano cai fora da janela declarada para a variável; a ausência de observação monetária em 2023–2024 na rota estadual pode, portanto, resultar da montagem do histórico canônico ou de preenchimento de estados posterior. **O ponto exato de materialização das linhas `nao_aplicavel` no banco publicado ainda requer inspeção do artefato canônico**, e não está demonstrado somente pelos mapeamentos.

### Providência técnica fundamentada

Criar uma etapa separada de integração do histórico monetário RGF Gate E, preservando chave município–ano–variável, fonte RGF Anexos 01/02, status observado/ausente e SHA do CSV aprovado. Não modificar observações `nao_aplicavel` indiscriminadamente: somente registros cujo valor e proveniência sejam confirmados em conjunto devem ser elegíveis para atualização. Reconstruir o SQLite e a API de publicação, recalcular coberturas, comparar com a referência aprovada e exigir novo QA de 10 universos/280 fichas antes da liberação.

**Status:** causa de omissão dos valores monetários históricos no recorte identificada; solução na base canônica ainda não aplicada. O gate editorial segue reprovado.
