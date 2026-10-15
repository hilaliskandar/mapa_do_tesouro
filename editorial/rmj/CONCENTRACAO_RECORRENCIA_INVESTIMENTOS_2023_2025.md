# Concentração e recorrência contábil dos investimentos da RMJ — 2023–2025

Data: 15/10/2026. Base: séries completas da Despesa Detalhada TCESP, **grupo 44, estágio Valor Liquidado**, conciliadas com DCA para os 21 pares município–exercício.

## Construção

Lidos 429 registros de programas e 937 de ações dos CSVs íntegros dos três exercícios. Para cada município–ano e nível de classificação, foram calculados:

- Participação do maior programa/ação = maior valor liquidado / total liquidado no município e ano.
- Participações dos três e dos cinco maiores = soma ordenada dos valores liquidados / total.
- Índice Herfindahl-Hirschman (HHI) = soma dos quadrados das participações em fração unitária. É métrica descritiva de concentração contábil, não medida de eficiência.
- Presença da mesma chave contábil em um, dois ou três exercícios: programa = (município, código de programa); ação = (município, código de programa, código de ação). Não se exige identidade de nome para o agrupamento; as descrições de cada ano são preservadas em colunas separadas.
- Nenhuma ausência é automaticamente interpretada como extinção de política e nenhum reaparecimento como entrega física; programas recodificados podem artificialmente reduzir a recorrência medida por chave.

Arquivos gerados nesta etapa, entregues na conversa: `rmj_concentracao_2023_2025.csv` (42 linhas, 7 municípios × 3 anos × 2 níveis); `rmj_maiores_classificacoes_2023_2025.csv` (210 linhas, cinco maiores de cada combinação); `rmj_recorrencia_contabil_2023_2025.csv` (694 chaves únicas no trienio, programa e ação).

## Participação dos três maiores programas no investimento do exercício

| Município | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| Cabreúva | 64,27% | 49,71% | 60,98% |
| Campo Limpo Paulista | 87,84% | 91,49% | 91,90% |
| Itupeva | 89,39% | 92,56% | 79,99% |
| Jarinu | 92,05% | 97,40% | 86,42% |
| Jundiaí | 70,22% | 78,08% | 77,15% |
| Louveira | 70,09% | 76,47% | 70,72% |
| Várzea Paulista | 77,70% | 97,97% | 99,03% |

## Participação do maior programa

| Município | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| Cabreúva | 26,01% | 18,25% | 25,49% |
| Campo Limpo Paulista | 68,58% | 79,09% | 80,48% |
| Itupeva | 58,20% | 71,00% | 31,37% |
| Jarinu | 69,17% | 90,17% | 70,22% |
| Jundiaí | 43,69% | 52,19% | 50,72% |
| Louveira | 31,00% | 33,17% | 32,16% |
| Várzea Paulista | 60,86% | 55,55% | 85,06% |

## Recorrência contábil de códigos de programa

Parcela do valor acumulado de 2023 a 2025 alocada a **códigos de programa com investimentos liquidados nos três anos**:

| Município | Parcela dos valores no trienio |
|---|---:|
| Cabreúva | 98,3% |
| Campo Limpo Paulista | 99,4% |
| Itupeva | 97,9% |
| Jarinu | 97,9% |
| Jundiaí | 100,0% |
| Louveira | 91,9% |
| Várzea Paulista | 15,7% |

**Ressalva essencial:** a baixa recorrência de Várzea Paulista decorre, em parte, da recodificação já evidenciada (ação 1009 presente nos três anos sob programas 40 e 70). Portanto, esta medida **não** significa descontinuidade da ação hospitalar nem que só 15,7% das políticas foram mantidas. É uma medida de estabilidade das chaves, útil para detectar necessidade de leitura crítica.

## Recomendações para o painel

- Inserir a análise de concentração na seção já existente de programas, apresentando top 1/top 3, destaque dos maiores movimentos e explicações.
- Mostrar presença da classificação em vários anos como informação descritiva, não “investimento recorrente” no sentido de despesa permanente nem “investimento excepcional” no sentido jurídico.
- Identificar a concentração como **exposição à execução de poucos programas**, sem afirmar causalidade sobre receitas, obras e contratos.
- Não reabrir rastreamento exaustivo de LOA/PPA. Priorizar comparação contábil já comprovada e exemplos municipais que agreguem valor editorial.
- Próximo gate: conferir alinhamento com seções existentes de `editorial/rmj/index.html` e só então publicar, após testes e revisão de narrativa.

Fonte dos microdados: https://transparencia.tce.sp.gov.br/ (arquivos municipais Despesa Detalhada por ano); registros de hash/origem estão nos CSVs e JSONs originais de auditoria do projeto.
