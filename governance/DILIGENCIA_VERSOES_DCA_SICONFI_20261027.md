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
