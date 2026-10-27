# Diligência Siconfi — semântica dos status e investigação de versões da DCA
Data: 27/10/2026. Escopo: dez maiores divergências de investimentos liquidados entre TCESP e DCA.

## Fontes oficiais consultadas
- Manual Siconfi — histórico das declarações: https://manualsiconfi.tesouro.gov.br/area-publica/consultas/consultar-historicos/consultar-historico-das-declaracoes
- Manual Siconfi — consulta de pacote: https://manualsiconfi.tesouro.gov.br/consultas/consultar-pacote-de-declaracoes
- Tesouro — como retificar declaração: https://siconfi.tesouro.gov.br/siconfi/pages/public/conteudo/conteudo.jsf?id=20103
- Manual de procedimentos das declarações e MSC (2020): https://siconfi.tesouro.gov.br/siconfi/pages/public/arquivo/conteudo/Manual_de_Procedimentos_Declaracoes_e_MSC_20_02_2020.pdf

## Interpretação documental
As categorias oficiais são **Homologado** e **Retificado**, com modalidade dentro/fora do prazo. O procedimento de retificação exige alteração/reabertura e nova homologação; a situação retificada é reconhecida como entrega válida. Os literais `HO` e `RE` encontrados em `status_relatorio` são compatíveis com essas denominações. A correspondência literal código→situação ainda deve ser conferida em dicionário oficial específico do endpoint; não se pressupõe que a data de `data_status` comprove qual valor foi alterado.

O histórico público do Siconfi permite consultas por ente, poder, instituição, exercício, declaração e escopo; oferece situação e data de homologação e exportação CSV/PDF. O pacote de declarações permite filtragem por período de homologação/retificação. A mera existência desses recursos não comprova acesso programático a todas as versões anteriores nem a seus valores.

## Evidência já recuperada do projeto
Dez extratos DCA `/extrato_entregas` foram consultados. Quatro situações `RE`: São Caetano do Sul/2023, Taubaté/2024, Ourinhos/2024 e Iguape/2024. Seis `HO`: Salto/2023, Itaóca/2024, Novais/2024, São Carlos/2024, Araçatuba/2023 e Guaraci/2025. Em Taubaté, Ourinhos e Iguape, os valores atuais de DCA coincidem exatamente com os TCESP previamente reextraídos; em São Caetano do Sul, `RE` convive com divergência persistente. Portanto, `RE` não explica, por si só, a conciliação.

## Procedimento necessário para prova causal
1. Obter da consulta pública de histórico de cada ente as entradas de DCA e datas/estados, incluindo registros anteriores, identificadores e arquivo exportado.
2. Solicitar via consulta de declarações ou pacote, quando disponível, os arquivos referentes aos estados históricos. Verificar se são versões distintas e registrar hash, data, escopo institucional, situação e conteúdo.
3. Localizar em cada arquivo o Anexo I-D, coluna Despesas Liquidadas, conta DO4.4.00.00.00.00, e confrontar por centavos com snapshot canônico histórico e API atual.
4. Caso o histórico público não disponibilize a versão anterior, manter a hipótese de retificação não demonstrada e documentar o bloqueio de acesso; não atribuir a mudança de valor à retificação apenas pela data de status.
5. Repetir inicialmente Taubaté, Ourinhos e Iguape, e usar São Caetano do Sul como controle negativo (status RE mas divergência persistente). Depois investigar os seis HO e os 45 casos restantes.

## Proteções
Não substituir o CSV canônico DCA, os objetos TCESP no R2, a API nem a produção. Registrar snapshots distintos e diferenças em centavos. Esta diligência documental não produziu novas versões numéricas dos demonstrativos nem solucionou causalmente as divergências.


## Verificação direta das interfaces públicas em 27/10/2026
Foram lidas diretamente por Crawl2AI as páginas oficiais do [Histórico das Declarações](https://manualsiconfi.tesouro.gov.br/area-publica/consultas/consultar-historicos/consultar-historico-das-declaracoes), da [Consulta de Pacote de Declarações](https://manualsiconfi.tesouro.gov.br/consultas/consultar-pacote-de-declaracoes) e a [interface pública real do histórico](https://siconfi.tesouro.gov.br/siconfi/pages/public/consulta_historico_declaracoes/historico_declaracoes_list.jsf).

A consulta pública exige Esfera, UF (municipal), Ente, Poder, Instituição e Escopo; permite filtros de exercício e tipo de declaração, com resultado em exercício, declaração, data de homologação e situação, além de exportação CSV/PDF. O pacote é documentado como ZIP de declarações homologadas/retificadas filtrável por período de homologação/retificação, mas sua descrição não afirma disponibilizar versões históricas sucessivas da *mesma* declaração.

A página pública de histórico respondeu e apresentou controles e tabela vazia **antes da seleção dos parâmetros**; isto não constitui resultado negativo para nenhum município. A tentativa de extração programática dos elementos interativos da página falhou na ferramenta JS do crawler, portanto não há consulta municipal concluída nem arquivo histórico antigo recuperado nesta rodada.

A documentação oficial das situações homologada e retificada consta também do [Manual de Procedimentos das Declarações e MSC de maio de 2020](https://siconfi.tesouro.gov.br/siconfi/pages/public/arquivo/conteudo/Manual_de_Procedimentos_Declaracoes_e_MSC_29_05_2020.pdf). A documentação geral não é um dicionário de codificação literal da API: manter `RE` e `HO` como valores de origem até confrontar a especificação desse campo.

**Próxima diligência prioritária:** executar o formulário interativo com ambiente de navegador capaz de preservar a sessão JSF, selecionar Prefeitura/Executivo/DCA e os exercícios de Taubaté, Ourinhos, Iguape e São Caetano do Sul; exportar os históricos quando disponíveis. Separadamente, procurar identificadores de versões e verificar se alguma edição anterior pode ser aberta; se não, registrar ausência de acesso à versão, sem inferência causal. A API atual e os dez extratos já consultados não precisam de nova consulta apenas para repetir seus valores.


## Investigação adicional de vias públicas e restritas — 27/10/2026
- O manual da [Consulta de Declarações](https://manualsiconfi.tesouro.gov.br/area-publica/consultas/consultar-declaracoes/consultar-declaracao) informa filtros por município, poder, órgão e exercício e disponibilidade dos documentos PDF ou XLS; o retorno descrito apresenta **estado atual** da declaração, sem especificar acesso a versões substituídas.
- A orientação oficial [Como retificar uma declaração](https://siconfi.tesouro.gov.br/siconfi/pages/public/conteudo/conteudo.jsf?id=20103) descreve cancelamento de assinaturas, edição ou substituição de dados e nova assinatura/homologação. Essa regra confirma a possibilidade de mudança do conteúdo declarado, mas não identifica quais rubricas foram alteradas nos casos concretos.
- O [Manual de Procedimentos de Declarações e MSC](https://www.siconfi.tesouro.gov.br/siconfi/pages/public/arquivo/conteudo/Manual_de_Procedimentos_Declaracoes_e_MSC_20_02_2020.pdf) descreve a **Linha do Tempo** em *Gerir Declaração*, com data, situação e ações, após autenticação na área restrita. Não se demonstrou acesso externo a uma cópia da versão anterior.
- A [API pública](https://apidatalake.tesouro.gov.br/docs/siconfi/) documenta `/dca` e `/extrato_entregas`, mas não foi identificado nessa documentação endpoint explícito para consultar todas as versões do mesmo quadro DCA. Isso não prova inexistência de outro recurso; registra apenas limite da documentação consultada.

**Decisão técnica:** não tentar reproduzir sessão privada nem inferir que o pacote ZIP contém snapshots históricos. Manter a reconciliação dos dez pares em duas camadas: paridade numérica atual (3 resolvidos, 7 persistentes) e causalidade/versão (pendente). Priorizar eventual obtenção pública de PDF/XLS e histórico exportado, ou diligência documental formal à STN para dados de versões, com datas/hashes e campo DO4.4.00.00.00.00. Nenhum valor canônico ou implantação foi modificado.
