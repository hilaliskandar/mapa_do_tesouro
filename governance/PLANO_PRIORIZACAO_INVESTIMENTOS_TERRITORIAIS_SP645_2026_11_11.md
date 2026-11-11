# Prioridade de desenvolvimento — Investimentos públicos territorializados nos municípios paulistas

**Decisão registrada em:** 11/11/2026  
**Projeto:** Mapa do Tesouro — `hilaliskandar/mapa_do_tesouro`  
**Abrangência:** 645 municípios do Estado de São Paulo; visões derivadas por regiões metropolitanas, aglomerações urbanas e outras divisões territoriais já homologadas.  
**Situação:** prioridade aprovada como orientação de trabalho; fontes e acervo inventariados; **a ingestão estadual de novos instrumentos e pagamentos ainda não foi executada nesta documentação**. Não alterar DCA/FED04, banco SQLite canônico, R2, D1 ou publicação.  
**Branch isolada:** `investimentos-territoriais-sp645-20261111`, criada a partir de `main` para evitar misturar a nova iniciativa com o PR #232, que segue *draft*.

## 1. Produto e conceito

Pergunta de produto: **quanto está sendo investido em cada município, por quem, em que intervenção, em que fase, com qual financiamento, onde e com qual evidência de execução?** O objeto central é uma **carteira territorial de projetos/intervenções e seus eventos**, integrada às séries agregadas já existentes, não uma tabela de repasses confundidos com investimentos realizados.

Separar quatro dimensões que devem ser apresentadas lado a lado, não somadas:

1. **Investimento executado diretamente no território por ente federal, estadual ou municipal:** desembolsos, liquidações de despesas de capital, obras e equipamentos conforme a fonte efetivamente documente; estágio físico diferenciado.
2. **Transferências intergovernamentais vinculadas a investimento:** recursos federal→estado, federal→município, estadual→município e fundo a fundo; transferência paga não comprova obra concluída nem deve ser somada à despesa final financiada com o mesmo recurso.
3. **Carteira e compromissos futuros:** projetos anunciados, selecionados, propostos, instrumentos celebrados, contratos, valores previstos e empenhos; **não computar como executado**.
4. **Financiamentos e agentes não orçamentários:** estatais não dependentes, concessões, PPPs, operações de crédito e aporte privado no Novo PAC; exibir em trilhas distintas, sem chamar todo investimento listado no PAC de investimento público orçamentário.

**Princípio de territorialidade:** município de execução da intervenção ≠ município sede do fornecedor ≠ município beneficiário formal do instrumento ≠ município recebedor do crédito ≠ domicílio do favorecido da emenda. Criar papéis territoriais explícitos, podendo haver vários municípios por projeto, com regra de rateio verificável ou valor territorial `nao_alocado`. O recorte municipal e os filtros regionais usam o cadastro IBGE canônico, sem criar várias bases paralelas.

## 2. Estado real do projeto reutilizável

- [Plano de integração federal SP645 existente](PLANO_INTEGRACAO_DADOS_FEDERAIS_SP645_2026_11_09.md): modelo SQLite canônico e R2 existente `financas-municipais-sp-canonico`, sem bancos paralelos; gates FED00–FED08; propostas de atualização incremental.
- [Matriz de fontes federais SP645](MATRIZ_FONTES_FEDERAIS_SP645.csv): 14 conjuntos com status distintos, inclusive Transferegov, STN, CGU e Obrasgov.
- [RMSJRP, G06-F3](../editorial/rmsjrp/RELATORIO_G06F3_VINCULOS_2026_11_09.md): 37 municípios, registros de propostas e parceria, sete registros de empenho na amostra; **não** pagamentos. Coletor/registros a reaproveitar. R2 regional em `rmsjrp/g06/2026_11_09/`; não substituir ou duplicar.
- [Pré-inventário de carteira da RMRP](../editorial/rmrp/PRE_INVENTARIO_CARTEIRA_LOTE37.md): investimento municipal liquidado e transferências de capital de 2025 para 34 municípios; **não** descreve projetos individualizados.
- Dados TCESP estaduais 2023–2025 e DCA 2013–2025 já existentes na base do projeto; integrar por chaves e manter somatórios consistentes.
- Auditoria FED04 do Fundeb encontra-se em branch/PR independente: **pausada para priorização**, não cancelada e não homologada; preservação de todos os documentos e gates.

## 3. Catálogo de fontes e ordem de execução

A matriz executável de fontes encontra-se em `governance/MATRIZ_FONTES_INVESTIMENTOS_TERRITORIAIS_SP645_2026_11_11.csv`. Prioridades:

**P0 — primeiras bases a obter e homologar, em paralelo por natureza:**
- **Transferegov novo portal** https://api-publica.transferegov.gestao.gov.br/ : **Transferências Especiais**, **Gestão de Parcerias** e **Discricionárias/Legais**. As duas primeiras APIs e o CSV nacional de Discricionárias/Legais devem sustentar tanto estoque quanto eventos; não depender do módulo financeiro novo ainda em desenvolvimento.
- **Obrasgov novo portal** https://api-publica.obrasgov.gestao.gov.br/ : identificador de obra, projeto, localização, responsável, valores e estágios físicos/financeiros, com QA de atualização pelo órgão gestor.
- **Portal da Transparência do Estado de SP** https://www.transparencia.sp.gov.br/Convenios : instrumentos estaduais, concedentes, beneficiário/CNPJ, objeto e valor; exportação e dicionário de dados.
- **Sefaz-SP Transferências Voluntárias** https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx : liberações efetivas registradas no SIAFEM/SP desde agosto de 2007, incluindo cancelamentos/estornos negativos, filtros por município e tipo **Investimento/Custeio**.
- **TCESP e DCA/SICONFI** : investimentos municipais empenhados/liquidados/pagos e transferências de capital; preservar estágio e classificação.
- **CGU Portal da Transparência** https://portaldatransparencia.gov.br/download-de-dados/ : transferências, pagamentos, documentos de despesa, convênios e emendas; fonte de eventos financeiros quando faltar no Transferegov.

**P1 — cobertura setorial e controle:**
- **Novo PAC** https://www.gov.br/casacivil/pt-br/novopac/transparencia : carteira de intervenções e fontes de financiamento; distinguir parcela pública, estatal, financiada e privada, evitando somar global contratado a pagamento.
- **Fundo Nacional de Saúde** https://portalfns.saude.gov.br/consultas/ : detalhamento de pagamentos, repasses fundo a fundo, propostas e convênios; contabilizar apenas linhas com categoria de investimento comprovada, sem equiparar custeio SUS a obra.
- **FNDE** https://www.gov.br/fnde/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-1/ : obras de creches/escolas, Novo PAC e repasses educacionais; SIGEF pode exigir CAPTCHA, devendo haver alternativa documentada sem automação enganosa.
- **Tesouro Transparente/STN** https://www.tesourotransparente.gov.br/temas/estados-e-municipios/transferencias-a-estados-e-municipios : transferências constitucionais/legais e emendas; essencial para conciliar ingresso fiscal, não necessariamente despesa de investimento.
- **Sefaz-SP SIGEO/SIAFEM** https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/FlexConsDespesa.aspx : execução orçamentária estadual (empenhado, liquidado e pago) e programa/ação. Associar a municípios **somente quando houver campo territorial ou documentação explícita**, pois muitas ações estaduais atendem redes ou regiões.
- **Portal de Dados Abertos SP** https://dadosabertos.des.sp.gov.br/ : busca sistemática por projetos e dados setoriais adicionais.

**P2 — extensão e fontes locais:** PAC setorial, DAEE, DER/SP, CDHU, SABESP, infraestrutura e empresas públicas; concessões/PPPs e investimento privado em trilha isolada; órgãos setoriais municipais e transparência local. Não confundir limites institucionais nem distribuir gasto centralizado entre municípios sem evidência.

## 4. Estratégia de aquisição (arquivos completos antes de chamadas 645×N)

**E0 — Prova de acesso:** recuperar contratos OpenAPI/Swagger e modelo de dados, lista de arquivos, metadados (URL, versão, data, tamanho, periodicidade, licença, esquema, autenticação e paginação). Verificar as interfaces **em novembro de 2026**, não assumir que rotas legadas funcionam após migração em agosto de 2026.

**E1 — Aquisição completa por fonte:** baixar CSV nacionais disponíveis do Transferegov Discricionárias/Legais e CGU, captura de Transferegov Especiais/Parcerias via API paginada quando não existir dump mais confiável, e Obrasgov por API; recuperar liberações Sefaz-SP e cadastro de convênios estaduais usando download oficial. **Não substituir lote nacional por 645 consultas repetidas sem necessidade.**

**E2 — Staging reversível:** gravar originais imutáveis, manifestos SHA-256, contagem, datas de extração, paginação, URL canônica, filtros, formato e versão em R2 **sob prefixo próprio** (sugerido `investimentos/sp645/{fonte}/{data}/`, sujeito a validação dos bindings existentes); CSV/Parquet normalizado com dicionário, sem tocar `observacao` canônica. Snapshot com readback e controle de retificação.

**E3 — Normalização por entidades e eventos:** cadastros `projeto`, `instrumento`, `transferencia`, `evento_financeiro`, `execucao_fisica`, `execucao_orcamentaria`, `ator`, `projeto_municipio` e `evidencia`. Cada evento monetário identifica data, estágio, unidade, fonte, beneficiário, financiador e chave primária. Compatibilidade com `data/schema`, `observacao_proveniencia` e `artefato_fonte`; migrations só **propostas**, nunca aplicadas à produção antes de homologação.

**E4 — Vinculações explicitamente comprovadas:** cadeia `emenda → proposta → instrumento/parceria → empenho → ordem/pagamento → obra/projeto → execução local`, com IDs e fontes. Entre sistemas, relação `comprovada`, `candidata`, `nao_identificada`; não fazer merge automático por valor ou nome similar. Composição multientidade e rateio territorial somente se houver base legal/contábil específica.

**E5 — Piloto antes da carga estadual:** utilizar **RMSJRP 37 municípios** e **RMRP 34** com testes de porte/população e projeto com financiamento misto. Sentinelas: São José do Rio Preto/proposta 398 e sete empenhos G06-F3, casos de Guariba e obras já identificadas no acervo RMRP. Validar datas, documentos, localização e duas fontes independentes quando possível. Primeiro produto demonstrável: carteira de projetos com valores previstos e pagamentos explicitamente documentados, sem preencher lacunas.

**E6 — Expansão estadual 645:** comparação de contagens e somatórios por fonte, situação, órgão, município, exercício e instrumento; cobertura territorial e fonte incompleta explícita. Atualizações incrementais + janela retroativa para mudanças e estornos.

## 5. Modelo de dados mínimo para viabilizar dashboard

**Dimensões (sem repetir o cadastro canônico):**
- `projeto_id` (chave da plataforma) e `fonte_projeto_id` com namespace;
- nome/objeto, setor, subárea, tipo de intervenção (obra, equipamento, serviço, financiamento), situação, órgãos executores e financiadores;
- instrumento jurídico (número e origem), fonte orçamentária, emenda quando houver;
- localização: código IBGE de execução, abrangência, coordenadas, grau de precisão, múltiplos municípios, método de atribuição e evidência;
- `evento_id`, fonte, data de competência, data de pagamento, estágio financeiro, sinal estorno, valor, moeda, recebedor e código de documento;
- execução física: marco, porcentagem, data da referência, agência responsável;
- URL/documento, atualização, hash, cobertura, confiança do vínculo e estado de QA.

**Classificações obrigatórias:** `federal_direto`, `estadual_direto`, `municipal_direto`, `transferencia_federal_municipal`, `transferencia_federal_estadual`, `transferencia_estadual_municipal`, `fundo_a_fundo`, `estatal_nao_dependente`, `credito`, `privado`; e `previsto`, `selecionado`, `celebrado`, `empenhado`, `liquidado`, `pago`, `transferido`, `medicao_fisica`. Uma mesma obra pode ter fontes múltiplas e eventos múltiplos, sem somar `valor_global` e parcelas.

## 6. Painel e indicadores possíveis

**Visão municipal:** carteira de projetos ativos/entregues/paralisados, filtros por eixo, executor, governo financiador, instrumento e fonte; mapa de localização com precisão marcada; linha do tempo de contrato/repasse/obra; total contratado e desembolsado **em colunas separadas**; investimento municipal liquidado e transferência ingressada em trilhas próprias.

**Visão estadual:** total por região, distribuição por habitante apenas com população e cobertura homogênea, concentração territorial, projetos em atraso ou sem execução, participação relativa por setor e por nível de governo, cobertura documental por fonte.

**Indicadores com gate de QA:** `valor_carteira_projetos`, `pagamentos_federais_com_destino_municipal`, `liberacoes_estaduais_municipios`, `investimento_municipal_liquidado`, `obras_em_execucao`, `obras_paralisadas` e `projetos_com_ligacao_financeira_comprovada`. **Não publicar um único "total de investimento público no município" enquanto houver risco de dupla contagem das transferências com os gastos executados e cobertura desconhecida de obras diretas estaduais/federais.** Exibir blocos complementares e eventual agregado apenas para eventos de execução final deduplicados.

## 7. Gates e critérios mensuráveis

| Gate | Entrega | Homologação |
|---|---|---|
| INV00 | Matriz de fontes e contratos com estado real | URLs e documentação oficiais, versão, paginação e acesso registrados; nenhuma API hipotética declarada operacional |
| INV01 | Snapshots completos P0 em staging | hash e readback, ano, formato, quantidade, erros e cobertura |
| INV02 | Dicionário/crosswalk, esquema proposto | chaves estáveis, assinaturas jurídicas e estágios separados, sem colisão SQLite |
| INV03 | Piloto RMSJRP/RMRP de vínculo projeto–instrumento | identificadores comprovados; duplicatas e eventos sem vínculo explicitados |
| INV04 | Pagamentos federais + liberações estaduais | datas e estornos, beneficiário e município pagador/recebedor auditados |
| INV05 | Obrasgov e investimentos diretos no território | geocodificação/abrangência e execução física versus financeira |
| INV06 | SP645 completo e QA de fontes | cobertura município×fonte×ano; zero somente quando fonte explicita |
| INV07 | Prévia isolada do dashboard | desempenho, indicadores auditados, mapas, feedback e regressão |
| INV08 | Decisão de publicação | aprovação explícita, documentação de limites, rollback |

**Definição de conclusão da primeira entrega operacional:** ao menos um arquivo/endpoint oficial por fonte P0 com snapshot verificável e schema; um conjunto de projetos individualizados ligado a municípios por ID; distinção paga/contratada/destinação e prova de não duplicação na amostra. **Não afirmar ingestão/integração/pagamento efetivo enquanto os gates não forem executados.**

## 8. Operação imediata

1. Inventariar os arquivos CSV nacionais de Discricionárias/Legais e CGU e a API de Transferências Especiais; **iniciar por dados de pagamento, se disponíveis**, além dos instrumentos.
2. Examinar a API Obrasgov e capturar amostra georreferenciada com identificadores de projeto.
3. Recuperar arquivo estadual de convênios e liberações SIAFEM/SP, confirmando se o valor corresponde a investimento ou custeio.
4. Construir uma matriz integrada do piloto RMSJRP/RMRP com projeto, instrumento, beneficiário, município da obra, ente executor, status financeiro e evidência.
5. Submeter QA e somente então expandir os coletores aos 645 municípios e criar elementos no painel.

**Critério de prioridade prática:** primeiro **valores efetivamente pagos/liberados e projetos de investimentos individualizados**, depois maior cobertura temporal/histórica e integrações setoriais; dados de propostas não podem dominar a interface em detrimento de gastos comprovados.

## 9. Fontes verificadas na decisão

- Transferegov nova plataforma: https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br e https://api-publica.transferegov.gestao.gov.br/
- Obrasgov nova API e descrição: https://www.gov.br/obrasgov/pt-br/ferramentas-de-gestao-e-transparencia/api-de-dados-abertos-obrasgov-br_novo
- Portal paulista: https://www.transparencia.sp.gov.br/Convenios e https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx
- Sefaz SP, execução por empenho, liquidação e pagamento: https://www.fazenda.sp.gov.br/SigeoLei131/Paginas/FlexConsDespesa.aspx
- Portal da Transparência federal, API: https://api.portaldatransparencia.gov.br/ e downloads https://portaldatransparencia.gov.br/download-de-dados/
- FNS: https://portalfns.saude.gov.br/consultas/ ; FNDE: https://www.gov.br/fnde/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-1/
- Novo PAC: https://www.gov.br/casacivil/pt-br/novopac/transparencia
