# RMSJRP — G06-F | Descoberta e piloto auditado de instrumentos federais

**Data da execução:** 09/11/2026. **Natureza:** verificação técnica e cobertura de propostas do Transferegov, **não** auditoria integral dos convênios pagos, nem estimativa do efeito da LC 200/2023. **Estado:** descoberta 76 rotas aprovada, piloto 20 consultas aprovado e ampliação para 37 municípios aprovada quanto à conectividade e à confirmação territorial; ausência de paginação e dos estágios financeiros ainda impede considerar a cobertura exaustiva.

## 1. Fontes, migração e restrições temporais

A origem oficial é o [novo portal de APIs públicas Transferegov](https://api-publica.transferegov.gestao.gov.br/) e o [comunicado governamental de 10/07/2026, modificado em 13/07/2026](https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br).

O governo federal informou migração dos serviços em 2026. Em particular, o cronograma de API do módulo **Discricionárias e Legais** separa:
- atos preparatórios: julho–outubro/2026;
- instrumentos: novembro/2026–fevereiro/2027;
- execução financeira: março–junho/2027;
- obras: julho–outubro/2027.

Essas datas são **janelas de implantação informadas**, não prova de que todas as rotas estejam disponíveis hoje. A [comunicação de 17/07/2026, modificada em 02/10/2026](https://www.gov.br/obrasgov/pt-br/noticias/2026/comunicado-23-2026-mudancas-nos-acessos-as-apis-de-dados-abertos-do-transferegov-br-e-do-obrasgov-br) recomendou a migração e estabeleceu a descontinuação de endereços legados em 31/08/2026; não utilizar URLs antigas como fonte canônica sem testes.

**Crawl2AI:** foram tentadas as páginas do comunicado e do portal de API; o conector retornou erro interno. As fontes públicas HTML foram consultadas por acesso web alternativo e os schemas foram recuperados diretamente de um runner GitHub Actions. **Não atribuir a coleta ao Crawl2AI**.

## 2. Descoberta de rotas reais nos OpenAPI oficiais

O script [`discover_transferegov_g06f.py`](discover_transferegov_g06f.py), workflow `.github/workflows/rmsjrp-g06f-discovery.yml`, consultou os documentos OpenAPI dos quatro módulos, cada um com resposta válida e JSON estruturado:
- `/especiais/openapi.json`: **24 rotas**;
- `/parcerias/openapi.json`: **18 rotas**;
- `/discricionarias/openapi.json`: **13 rotas**;
- `/fundoafundo/openapi.json`: **21 rotas**.

**Total: 76 rotas**, não 76 consultas sobre os municípios nem 76 instrumentos. [Run 42629593944](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42629593944), `success`. Os filtros geográficos documentados incluem `cd_ibge_recebedor` em `/parcerias/proposta`, `cod_munic_ibge` em `/discricionarias/propostas` e `codigo_ibge_municipio_ente_recebedor_plano_acao` em `/fundoafundo/planos-acao`.

**Controle de identidade:** os OpenAPI descrevem os nomes de parâmetros; sua presença não prova existência de instrumentos num município, nem equivalência entre registros de módulos diferentes.

## 3. Piloto de cinco municípios, quatro módulos

Foram selecionados **São José do Rio Preto, Olímpia, Mirassol, José Bonifácio e Adolfo**, com códigos IBGE extraídos do cadastro geográfico já homologado. O script [`pilotar_transferegov_g06f.py`](pilotar_transferegov_g06f.py), workflow `.github/workflows/rmsjrp-g06f-pilot.yml`, enviou **20 consultas municipais** e observou:
- **15 HTTP 200**;
- **dez consultas com registros cuja localização foi confirmada por campo textual/código explícito**;
- **cinco HTTP 500**, todos no módulo `fundoafundo/planos-acao`. Isso **não indica inexistência de transferências fundo a fundo**;
- [Run 42630135250](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42630135250), `success` após redução dos exemplos persistidos a identificadores/metadados curtos.

Exemplos de **propostas**, não de pagamentos:
| Município | ID da proposta | Programa interno | Ano e data registrados | Situação cadastrada |
|---|---|---|---|---|
| São José do Rio Preto | 75094 | 167 | 2026; 13/05 | Aprovada |
| Olímpia | 13999 | 15 | 2025; 23/07 | Aprovada |
| Olímpia | 14002 | 15 | 2025; 23/07 | Aprovada |
| Mirassol | 76321 | 110 | 2026; 15/05 | Aprovada |
| José Bonifácio | 92185 | 122 | 2026; 06/11 | Aprovada |

Os IDs decorrem da resposta do módulo de Gestão de Parcerias `/parcerias/proposta?cd_ibge_recebedor=<codigo_ibge>`, com `cd_ibge_recebedor` e `nm_municipio_recebedor` explicitamente compatíveis. **Status `Aprovada` refere-se à proposta, não à comprovação de instrumento assinado, recurso pago pela União, recebido pela Prefeitura ou despesa municipal liquidada.** A fase de aprovação **não** configura um valor de transferência disponível para soma.

## 4. Cobertura dirigida aos 37 municípios em duas APIs

O script [`consultar_37_transferegov_g06f.py`](consultar_37_transferegov_g06f.py) consultou **37/37** códigos nos dois módulos com filtro geográfico explícito:
- Gestão de Parcerias, rota `/parcerias/proposta`: **37/37 consultas HTTP 200**, com confirmação territorial em **37/37**;
- Discricionárias e Legais, rota `/discricionarias/propostas`: **37/37 consultas HTTP 200**, com confirmação territorial em **37/37**.

**Total de 74 requisições bem-sucedidas e 74 confirmações geográficas**, [run 42630345679](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42630345679), `success`. Foram retidas **437 linhas de candidatos em amostras limitadas (máximo seis por município e por módulo)**. Essa contagem **não** deve ser apresentada como total de propostas, convênios, acordos, transferências ou instrumentos distintos: não foi verificada a paginação e possíveis correspondências entre módulos não foram deduplicadas como o mesmo instrumento. O inventário de cobertura mantém separadas as quantidades **da primeira resposta da API**, sem presumir completude.

O cruzamento geográfico utiliza o campo de código IBGE ou o nome explícito da localidade, e **não** associa repasses a municípios com base apenas em nomes dentro da descrição do programa. Os valores de propostas, quando disponíveis, não foram somados como valores transferidos.

## 5. Persistência, auditoria e limitações

A persistência compreende três conjuntos:
1. Descoberta: `ROTAS_OFICIAIS_G06F.csv` e `QA_G06F_API_DESCOBERTA.json`;
2. Piloto: `G06F_PILOTO_ENDPOINTS.csv` e `QA_G06F_PILOTO.json`;
3. Cobertura: `G06F_COBERTURA_37x2.csv`, `G06F_PROPOSTAS_CANDIDATAS_AMOSTRA.csv` e `QA_G06F_COBERTURA.json`.

Os três workflows passaram. Os dados são documentos derivados de **fontes oficiais**, mas ainda não formam uma série financeira conciliada. Os artefatos temporários do GitHub Actions (retenção configurada) devem ser salvaguardados em R2 privado, com SHA de retorno e pastas de origem identificadas. **A disponibilidade e o status da última operação de R2 devem ser verificados em [run 42630703933](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42630703933)** antes de afirmar que o backup definitivo foi homologado.

O levantamento não completou as cinco categorias de G06-E. A existência de propostas localizadas permite enriquecer o campo de **candidatos de instrumento**, mas **não** autoriza preencher os 185 pares município–modalidade atualmente NA com valores zero ou presumidamente pagos.

## 6. Próxima etapa G06-F2: transformar propostas em instrumentos e pagamentos comprovados

1. **Paginação e unicidade:** inspecionar os contratos OpenAPI das rotas consultadas, identificar parâmetros de paginação efetivamente declarados, percorrer todas as páginas com controle de limites; deduplicar `id_proposta`, instrumentação e alterações, preservando CNPJ público do ente apenas quando necessário para prova.
2. **Classificação de situação:** separar proposta em elaboração, enviada, aprovada, celebrada, executada, anulada etc., com categorias de origem e data de extração; instrumento assinado exige documento ou status específico.
3. **Rastreamento de execução financeira:** testar, onde disponíveis, rotas próprias de instrumento, empenho/pagamento, Transferegov CSV histórico, Portal da Transparência, Tesouro e FNDE/FNS. A data de proposta não é data de repasse; valor pactuado não é valor pago; pagamento federal não é liquidação municipal.
4. **Ligação municipal:** cruzar identificação de instrumento com crédito municipal, fonte e empenho/liquidação do projeto, respeitando exercícios e regimes de competência.
5. **Cobertura por categoria:** revisar a matriz G06-E com proveniência `instrumento_identificado` ou `pagamento_confirmado` apenas quando comprovado; manter NA onde não houver fonte, sem valores imputados.
6. **Atribuição à LC 200:** somente após identificar o mecanismo concreto de limitação federal e um contrafactual metodologicamente defensável. O presente levantamento tem status **`descoberta_e_propostas_verificadas_sem_execucao_financeira`**.

**Estado do gate:** G06-E `qa_pass` para a exposição DCA; G06-F1 `qa_pass` para schema e consultas municipais, **pendente** de completude de registros e execução financeira; G06 geral `in_progress`. Sem substituição das séries G04/G05 e sem publicação editorial.
