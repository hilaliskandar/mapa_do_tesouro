# Auditoria editorial 02 — RM de Jundiaí

Consulta: 2026-10-12. Fonte: API pública v1, build multifuentes-v0.4-cef702e5edbd.
Estado: evidência de QA editorial, sem alteração de produção.

## Endpoints auditados

- https://finbra-tic-tim-referencia.pages.dev/data/api/v1/publication/contract.json
- https://finbra-tic-tim-referencia.pages.dev/data/api/v1/publication/universes/RM_JUNDIAI/context.json
- https://finbra-tic-tim-referencia.pages.dev/data/api/v1/publication/universes/RM_JUNDIAI/municipalities/{codigo_ibge}.json

Os sete endpoints municipais retornaram JSON com municipio, variaveis, latest, group_latest, relative_latest e series. Identificadores verificados: 3508405, 3509601, 3524006, 3525201, 3525904, 3527306 e 3556503.

## Comparação municipal 2025

Na tabela, percentuais são apresentados como 100 × valor decimal observado na API (conversão de exibição), SEM modificar dado armazenado ou recalcular indicador fiscal.

| Município | Receita tributária/RC (%) | Investimento/RC (%) | Investimento per capita (R$) | CAPAG |
|---|---:|---:|---:|---|
| Cabreúva | 17,15 | 4,31 | 414,72 | A |
| Campo Limpo Paulista | 22,79 | 2,42 | 122,26 | C |
| Itupeva | 32,63 | 2,87 | 274,42 | C |
| Jarinu | 26,20 | 3,14 | 282,76 | A |
| Jundiaí | 33,49 | 3,24 | 298,69 | A+ |
| Louveira | 17,48 | 2,32 | 304,47 | C |
| Várzea Paulista | 20,21 | 9,68 | 411,39 | B |

## Não conformidade QA-ED-01 — escala de percentuais

Exemplo Jundiaí, receita_tributaria_pct_receita_corrente:
- latest.value = 0.3348879480405985;
- metadata.unidade = percentual;
- metadata.formula = '100 * dca_receita_tributaria_bruta / dca_receita_corrente_bruta'.
O valor armazenado equivale à razão, não ao percentual multiplicado por 100. Outro exemplo: investimento_pct_receita_corrente = 0.03240326221362716, com fórmula catalogada 100 * investimentos/receita.

Decisão proposta: distinguir data_scale=ratio_0_1 de display_unit=percent e display_multiplier=100; corrigir metadados de fórmula OU alterar contrato de valores após auditoria exaustiva. Não alterar valores de API sem migração versionada. Checar outros indicadores legais, percentuais, diferenças da mediana e séries.

## Não conformidade QA-ED-02 — status de QA

Contrato e sete contextos municipais: build.qa_status='candidate'; build.app_version='0.4.0'; documentação de release registra publicação e QA remoto aprovado. O status do *snapshot de dados* não pode ser confundido com o estado de aprovação do *deploy*. Definir dois campos separados ou atualizar status apenas mediante evidência de gate.

## Não conformidade QA-ED-03 — documentação de indicadores

Nas variáveis examinadas, metadata.como_ler e metadata.cautelas são null. Exigir conteúdo editorial versionado para indicadores selecionados e explicitar a fonte primária além da origem pipeline:ratio. latest.referencia_origem registra pipeline:ratio (2025); em séries históricas aparece SP645 Site Input!..., indicando diferenças na linhagem que requerem documentação.

## Cobertura e limites

O agregado territorial strict_complete para 2025 está observado apenas em Louveira (1/7). Os demais seis municípios apresentam status ausente, nunca zero. Não compor total regional com esse subtotal.

## QA requerido para promoção editorial

1. Testes automáticos de escala entre valor, fórmula, unidade e renderização em TODAS as variáveis.
2. Metadados de build com estados distintos para snapshot, artefato e deploy.
3. Dicionário editorial completo em variáveis da Edição de Referência.
4. Comparação contra contextos individuais e estatísticas de grupo.
5. Verificação do snapshot CAPAG e ano-base antes da narrativa.
6. Preservar baseline e serviço público sem alteração até gate aprovado.

## Interpretação preliminar

Jundiaí lidera o grupo em participação tributária (33,49%). Várzea Paulista apresenta maior participação de investimentos sobre receita corrente (9,68%). Essas ordenações não constituem juízo de desempenho. CAPAG apresenta A+:1, A:2, B:1 e C:3 no contexto consultado. Apresentar ano-base versus posição da apuração.

