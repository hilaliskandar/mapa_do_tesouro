# Finanças Municipais SP — proposta de migração

Esta branch prepara a transição do projeto `mapa_do_tesouro` para uma nova plataforma de dados e análise fiscal municipal, com arquitetura estadual, auditável, versionável e preparada para publicação na Cloudflare.

## Princípios

1. O código e a metodologia versionados no Git são a fonte canônica da lógica de processamento.
2. A base operacional deve ser construída por pipeline reprodutível; não deve ser editada manualmente.
3. Ausência de dado não equivale a zero.
4. Conta oficial, agregação analítica, indicador derivado e classificação oficial são objetos distintos.
5. Toda variável deve ter definição, unidade, fonte, período, regra de harmonização e cautelas.
6. Mudanças classificatórias ao longo do tempo devem ser explicitadas em crosswalk.
7. Os universos municipais são filtros da base estadual; `TIC_TIM_30` é um universo inicial, não a estrutura do banco.
8. Funcionalidades aprovadas não podem desaparecer silenciosamente: cada versão deve passar por testes de regressão funcional.
9. O SQLite canônico local é o artefato auditável dos dados; D1 poderá ser uma réplica operacional para consulta web.
10. O frontend será static-first: consultas previsíveis devem ser pré-computadas e servidas por CDN; Worker/D1 ficam para consultas dinâmicas.

## Escopo inicial

A primeira versão operacional continuará cobrindo os 30 municípios TIC-TIM e a série 2013–2025 já consolidada. O esquema deverá, porém, nascer preparado para os 645 municípios paulistas.

## Arquitetura-alvo

```text
fontes oficiais
    ↓
pipeline Python
    ↓
validação + harmonização + indicadores + QA
    ↓
SQLite canônico
    ├── snapshots e hashes
    ├── JSON estático para consultas frequentes
    └── publicação operacional
          ├── Cloudflare Static Assets/CDN
          ├── Worker/API
          ├── D1
          └── R2
```

## Legado

O projeto `mapa_do_tesouro` passa a ser tratado como ancestral metodológico e técnico. Seu conteúdo não será descartado. A classificação de cada módulo está documentada em `migration/MIGRATION_MATRIX.md`.

O painel HTML consolidado do projeto FINBRA/TIC-TIM será preservado como referência funcional congelada em `reference/legacy/painel_html_final/`.

## Estrutura prevista do novo projeto

```text
financas-municipais-sp/
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── wrangler.toml
├── governance/
├── pipeline/
├── data/
├── app/
├── tests/
├── docs/
└── reference/legacy/
```

## Estado desta branch

Esta branch não converte ainda a arquitetura antiga. Ela registra as decisões de migração, a classificação do legado e a estrutura-alvo. Nenhum módulo legado deve ser promovido automaticamente para produção sem teste de paridade com a base fiscal já consolidada.
