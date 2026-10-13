# Auditoria factual da API v2 com dados canônicos — 13/10/2026

## Evidência primária
- GitHub Actions: SP645 Private Site Artifact, execução 38355047393, commit e81bf469658f683aabba84a1c7e677fa8f9f0720.
- Artefato arquivado: sp645-private-site-38355047393, ID 11792522202, SHA-256 do ZIP 6fd13fc6a169a6b9df2c4763ca60b8e529f8ec6cd43096fa8d509354cfd69af0.
- Fontes consultadas: data/api/v2/manifest.json, data/api/v2/qa/readiness.json, data/api/v2/catalog/variables.json e data/api/v2/catalog/universes.json, todos extraídos diretamente do artefato.
- Etapas comprovadas como sucesso: download com verificações SHA do R2; construção estadual; QA do build privado; Validate complete API v2 from canonical private build; upload do artefato.

## Inventário do resultado
- 645 fichas municipais estaduais, 13 universos regionais/temáticos/estadual.
- 75 variáveis catalogadas; 75 elegíveis tecnicamente para exportação.
- 174795 registros de observação exportados; exercícios 2021-2025.
- Estados de cobertura, para 75 variáveis vezes 645 municípios = 48375 combinações por exercício:

| Ano | observado | ausente | nao_aplicavel | em_revisao | sem_registro |
|---|---:|---:|---:|---:|---:|
| 2021 | 1346 | 589 | 29670 | 0 | 16770 |
| 2022 | 1356 | 579 | 29670 | 0 | 16770 |
| 2023 | 2880 | 990 | 27735 | 0 | 16770 |
| 2024 | 2903 | 967 | 27735 | 0 | 16770 |
| 2025 | 35286 | 13089 | 0 | 0 | 0 |

Nota: a tabela conta combinações município-variável, não municípios com alguma informação. O estado nao_aplicavel, tal como gravado no SQLite, não prova por si só uma indisponibilidade permanente, e sem_registro significa inexistência da linha correspondente. Os registros não observados não devem ser tratados como zero.

## Não conformidades de documentação
1. Todas as 75 variáveis têm ao menos um campo requerido incompleto segundo audit_api_readiness_v2.py; a recorrência principal é em como_ler/cautelas. Não concluir que faltam todos os metadados de cada variável.
2. As 17 variáveis cuja unidade é percentual não dispõem no relatório de comprovação explícita da escala de armazenamento e multiplicador de exibição. A análise de 2025 exige distinguir razões em 0-1 de percentuais já convertidos.
3. O manifesto declara publication_qa = not_evaluated: gate estrutural OK não equivale a certificação metodológica ou autorização de release.

## Decisão
**APROVADO:** montagem técnica com dados reais, integridade estrutural da API v2, unicidade territorial e fechamento das contagens de cobertura.
**PENDENTE:** explicação das lacunas de cobertura histórica, resolução dos campos editoriais exigidos, escala dos 17 indicadores e validação de comparabilidade anual/regional, bem como aprovação explícita de publicação.
**NÃO REALIZADO:** deploy da API v2 em ambiente público.

## Próximo trabalho
- Tabela priorizada dos 75 metadados incompletos, classificação por impacto e preenchimento com fontes verificadas.
- Tabela declarativa por variável de storage_scale, display_multiplier e regras de agregação; não inferir escala apenas por nome do indicador.
- Validação de numeradores/denominadores regionais, contagem e origem das observações históricas.
- Geração de artefato candidato com QA de publicação em estado próprio, seguido de prévia isolada e revisão editorial.
