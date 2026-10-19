# Coleta TCESP RMRP por quatro sub-regiões

Fonte da composição: Prefeitura de Ribeirão Preto, plano de desenvolvimento urbano integrado, https://www.ribeiraopreto.sp.gov.br/portal/noticia/plano-de-desenvolvimento-urbano-integrado-da-rmrp-e-apresentado-em-reuniao.

O roster versionado `editorial/rmrp/municipios_subregioes_tcesp.csv` contém 34 municípios e códigos IBGE do catálogo territorial já usado pela plataforma.

| Lote | Municípios | Extratos 2023–2025 |
|---|---:|---:|
| Sub-região 1 | 15 | 45 |
| Sub-região 2 | 6 | 18 |
| Sub-região 3 | 6 | 18 |
| Sub-região 4 | 7 | 21 |
| Total | 34 | 102 |

Workflow `.github/workflows/rmrp-tcesp-subregioes.yml`: 4 jobs de matriz usando o mesmo runner WSL2 dedicado; GitHub executa os jobs em fila, pois só há um runner com a etiqueta. Dentro de cada job, até três downloads concorrem simultaneamente, com timeout e três tentativas por documento.

Cada extrato usa o extrator TCESP existente na RMJ, verifica slug, ano, `bad_values=0`, hash da fonte e igualdade em centavos dos totais 44 Valor Liquidado por programa e ação. Guarda JSON e metadados de auditoria por município e ano. A revisão humana e a conciliação externa DCA serão realizadas **após a coleta**; não confundir a verificação interna com paridade FINBRA.

O workflow possui gatilho de push apenas para alteração do próprio YAML na main (permitindo uma execução inicial na integração) e acionamento manual posterior. Não comita documentos, não altera API e não publica o caderno. Em caso de falha, preserva todos os JSONs validados e relatório de pendências como artefato de Actions, com retenção de 30 dias.

O reaproveitamento ocorre para extratos já presentes no diretório de trabalho do job, mas o workspace padrão do GitHub Actions pode ser limpo entre execuções. Para evitar nova coleta em outras execuções, recuperar os artifacts concluídos para armazenamento persistente e adaptar a entrada de futuras execuções a esse acervo antes da repetição. Os 102 extratos ainda não estão incorporados nem reconciliados na DCA.
