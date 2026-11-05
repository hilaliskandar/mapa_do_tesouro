# Lote 102 — Cronologia oficial de RGF e recuperação do repositório fiscal de Barrinha

**Data de execução:** 05/11/2026. **Escopo:** Pontal, Barrinha e Orlândia, RGF de 2025 e 2026, Executivo. **Conclusão:** metadados oficiais das entregas recuperados e novo repositório municipal de Barrinha efetivamente navegado; **ainda não há reconciliação dos indicadores nem arquivo PDF de encerramento de 2025 comprovadamente lido**. Volume II do Lote 98 (66 páginas) preservado.

## 1. Extratos de entrega: observações oficiais, não inferências

Fonte primária: STN/Siconfi, endpoint `https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/extrato_entregas`, filtros exatos `an_referencia=2025|2026&id_ente=IBGE`. Busca direta via Crawl2AI; foram recuperados todos os registros de RGF de cada município e separados os registros da **Prefeitura Municipal** daqueles da **Câmara de Vereadores**. Datas UTC devolvidas no campo `data_status`; abaixo datas civis sem inferir uma linha histórica de todas as versões:

| Município | IBGE | Documento Executivo | Periodicidade | Período | Status | Data e hora oficial UTC |
|---|---|---|---|---|---|---|
| Pontal | 3540200 | RGF 2025 | Q | 2 | HO | 2026-04-03T10:07:55Z |
| Pontal | 3540200 | RGF 2025 | Q | 3 | HO | 2026-04-03T10:21:33Z |
| Pontal | 3540200 | RGF 2026 | Q | 1 | HO | 2026-07-11T14:33:08Z |
| Barrinha | 3505609 | RGF Simplificado 2025 | S | 2 | **RE** | 2026-03-17T14:49:38Z |
| Barrinha | 3505609 | RGF Simplificado 2026 | S | 1 | HO | 2026-07-28T10:39:45Z |
| Orlândia | 3534302 | RGF Simplificado 2025 | S | 2 | HO | 2026-01-30T11:28:46Z |
| Orlândia | 3534302 | RGF Simplificado 2026 | S | 1 | HO | 2026-07-31T13:23:11Z |

- `HO` e `RE` são valores de **status no extrato**, não prova da qualidade ou consistência contábil. `RE` em Barrinha requer exame de protocolo e da versão retificada; **o endpoint usado não expôs versões anteriores nem a data da versão inicial**.
- Os extratos mostram Executivo e Legislativo como instituições distintas. Nunca usar dados de RGF da Câmara para solucionar contas do Executivo.
- **Pontal:** o RGF de fechamento 2025 em API foi associado a 03/04/2026, **depois** da publicação municipal do Diário Oficial de 18/03/2026 (edição 1906). Isso **não prova** que o documento posterior seja retificação do anterior.
- **Orlândia:** o RGF publicado no Diário Oficial em 29/01/2026 (edição 2238) antecede **por um dia** o registro Siconfi de 30/01/2026. A ordem cronológica também **não prova identidade nem correção de versões**.
- **Barrinha:** status `RE` no 2º semestre/2025, datado de 17/03/2026. A ausência de PDF municipal correspondente na coleta desta etapa impede ligar o registro ao conteúdo de declaração anteriormente enviada.

URLs oficiais:
- Pontal 2025: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/extrato_entregas?an_referencia=2025&id_ente=3540200
- Pontal 2026: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/extrato_entregas?an_referencia=2026&id_ente=3540200
- Barrinha 2025: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/extrato_entregas?an_referencia=2025&id_ente=3505609
- Barrinha 2026: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/extrato_entregas?an_referencia=2026&id_ente=3505609
- Orlândia 2025: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/extrato_entregas?an_referencia=2025&id_ente=3534302
- Orlândia 2026: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/extrato_entregas?an_referencia=2026&id_ente=3534302

## 2. Repositório oficial de Barrinha recuperado: avanço relevante

A pesquisa anterior limitava-se ao portal WordPress (https://portal.barrinha.sp.gov.br/portaltransparencia/) com iframe que não fornecia os documentos em modo textual. Nesta diligência, **o Crawl2AI efetivamente acessou pela URL HTTP e porta 50000 o serviço oficial separado**:
- Início do serviço: http://www.barrinha.sp.gov.br:50000
- Publicações obrigatórias: http://www.barrinha.sp.gov.br:50000/publicacoes-obrigatorias
- Filtro “Rel. de Gestão Fiscal”: http://www.barrinha.sp.gov.br:50000/publicacoes-obrigatorias?categoria=rel-de-gestao-fiscal
- Seção de responsabilidade fiscal: http://www.barrinha.sp.gov.br:50000/responsabilidade-fiscal
- Página concreta de LRF 2025: http://www.barrinha.sp.gov.br:50000/responsabilidade-fiscal/LRF-2025
- Página “Relatório Gestão Fiscal”, arquivo histórico: http://www.barrinha.sp.gov.br:50000/publicacoes-obrigatorias/RELATORIO-GESTAO-FISCAL
- Página “Relatórios de Gestal Fiscal”, grafia conforme o portal, arquivo histórico: http://www.barrinha.sp.gov.br:50000/publicacoes-obrigatorias/RELATORIOS-DE-GESTAL-FISCAL

A página `LRF-2025` foi **integralmente recuperada em Markdown**, com vários hiperlinks de PDF publicados pela prefeitura, inclusive:
- **“ANEXO RGF”**, arquivo rotulado `ANEXO X RGF 2 QUADR 2025.pdf`: http://www.barrinha.sp.gov.br:50000/responsabilidade-fiscal/LRF-2025/ANEXO%20X%20RGF%202%20QUADR%202025.pdf
- **“ANEXO III”**, receita corrente líquida `ANEXO 3 RCL.pdf`: http://www.barrinha.sp.gov.br:50000/responsabilidade-fiscal/LRF-2025/ANEXO%203%20RCL.pdf
- **“METAS FISCAIS 3o QUADR 2025”**, arquivo de 2025: http://www.barrinha.sp.gov.br:50000/responsabilidade-fiscal/LRF-2025/3%C2%BA%20quadr.%202025.pdf

**Qualidade e limitação dos índices municipais:** o rótulo do relatório de 2025 na página aponta **“2 QUADR 2025”**. Essa identidade não corresponde automaticamente ao **RGF Simplificado S2/2025**, objeto da auditoria do Siconfi. No outro arquivo fiscal, item visível **“RGF 4 BIM 2025”** aponta para documento com nome de arquivo **2024** (`ANEXO X RGF 2 QUADR 2024.pdf`), demonstrando que os títulos e caminhos no portal têm inconsistências de catalogação. Não realizar equivalência documental a partir apenas do título do link.

A **tentativa real de leitura do PDF** “ANEXO X RGF 2 QUADR 2025.pdf” pelo Crawl2AI falhou com erro de ferramenta `INVALID_ARGUMENT / Error executing tool md`; tentativa Python Requests no contêiner falhou por DNS, sem download binário. **Nenhum número desse PDF foi extraído nem seu conteúdo verificado visualmente**, e não há prova de que seja a publicação do encerramento de 2025. A página `LRF-2026` não estava publicada no caminho tentado e retornou erro de aplicação; essa resposta não autoriza afirmar que inexista publicação de 2026 em outro canal.

## 3. Matriz de versões após a descoberta

| Caso | Evidência primaria municipal | Evidência STN | Principal impasse |
|---|---|---|---|
| Pontal 2025 | Diário Oficial 18/03/2026, RGF Executivo Anexo 01, valores divergentes de RCL e DTP | RGF Q3/2025 HO em 03/04/2026; RREO B6 RCL coincide com publicação municipal | recuperar histórico de transmissão e manifestação; não corrigir 805,41% por imputação |
| Orlândia 2025 | Jornal Oficial 29/01/2026, RGF Executivo com DCL e DTP divergentes da API | RGF Simplificado S2/2025 HO em 30/01/2026 | examinar versão publicada, metadados e diferenças de regime/Audesp versus Siconfi |
| Barrinha 2025 | Portal oficial em :50000 lista arquivo de **2º quadrimestre**, sem comprovação de PDF S2 | RGF Simplificado S2/2025 com status **RE** em 17/03/2026 | recuperar PDF de encerramento e protocolo de retificação |
| Barrinha/Orlândia 2026 S1 | Repositório municipal ainda sem demonstrativo recuperado | RGF Simplificado S1/2026 HO, divergências numéricas entre anexos documentadas no Lote 99 | conciliação entre RGF A02/A06 e relatório publicado |

## 4. Implicações para o Volume II e decisões

- **Não modificar** o Volume II Lote 98 (66 páginas) enquanto subsistirem diferenças entre os dados municipais e os do Siconfi.
- Manter **Pontal e Barrinha em quarentena**, com Orlândia em pendência documental relevante (P0 na matriz do Lote 101).
- Separar claramente: **conteúdo de documento publicado**, **status de entrega**, **tipo/periodicidade** e **valor numérico**. Uma declaração `HO` não constitui homologação pela equipe do relatório.
- Prioridade próxima: explorar o arquivo de PDF do portal `:50000` com ferramenta que devolva binário e realizar inspeção visual; localizar especificamente o RGF Executivo **S2/2025**, e **não** inferir do link “2 QUADR 2025”; localizar Diário Oficial da mesma data e versões anteriores do Siconfi.
- Para Pontal e Orlândia, obter versão protocolizada/Audesp, assinatura e eventuais retificações, confrontando campos de numerador e denominador.

**Fontes coletadas e verificadas diretamente:** sete extratos STN, páginas do portal `:50000` e da seção `LRF-2025` em Crawl2AI; publicação municipal Pontal/Orlândia já documentada nos Lotes 100–101. **Limitação principal:** PDF de Barrinha não lido nesta rodada. O projeto continua em **pré-homologação**, sem juízo sobre infração.
