# INV-RMRP — Confronto de contratos municipais e instrumentos federais para quatro projetos Obrasgov

**Data da verificação:** 12/11/2026. **Projeto:** mapa_do_tesouro, PR nº 233 (draft). **Unidade de análise:** quatro projetos Obrasgov vinculados, por similaridade de objeto, a dez convênios SIAFEM municipais candidatos. **Nenhum vínculo financeiro estadual foi homologado.**

## 1. Método e qualidade das fontes

Os quatro projetos foram selecionados na matriz `INV_RMRP_SIAFEM_OBRASGOV_17_PARES_CANDIDATOS_NAO_HOMOLOGADOS_2026_11_12.csv`, que resulta do confronto entre os objetos oficiais SIAFEM e a amostra Obrasgov. Antes da busca externa foram confirmados os quatro IDs, as dez combinações convênio-projeto e os órgãos concedentes.

Fontes primárias utilizadas: API federal Obrasgov (`/projeto-investimento`, `/contrato`, `/empenho`, consultas filtradas por ID), portais de licitações municipais, diários oficiais municipais e extratos federais de contratos de repasse. Consultou-se inicialmente o Crawl2AI, que nesta rodada devolveu **erro interno** para os quatro primeiros URLs testados; a extração de páginas prosseguiu por navegador Browserless quando possível e por descoberta de fontes oficiais, preservando essa limitação de leitura. As duas páginas de Guariba consultadas por navegador apresentaram **HTTP 403 Cloudflare**; seus textos foram identificados em indexação pública e, por isso, devem continuar qualificados como pendentes de recaptura documental direta. A página de Sertãozinho foi aberta com HTTP 200. O Diário Oficial municipal de Serrana foi identificado e seu conteúdo específico recuperado em pesquisa; não houve substituição de fonte oficial por afirmações extraídas de títulos gerais.

## 2. Achados por projeto

### Guariba — Obrasgov 30964.35-52

- O projeto federal tem objeto de infraestrutura urbana, recapeamento asfáltico, sinalização viária e rampas de acessibilidade, com executor **Município de Guariba**, repassador **Ministério das Cidades**, e empenho federal **2023NE002773** na API Obrasgov.
- O portal municipal registra a **Concorrência nº 013/2024**, com objeto correspondente e indicação expressa do **Contrato de Repasse federal nº 953042/2023**, operação CAIXA **1091451-14/2023**. Fonte: https://www.guariba.sp.gov.br/portal-da-transparencia/licitacao/editais/concorrencia-publica/013-2024-concorrencia-publica-aberto.
- A página municipal do convênio nº 953042/2023 identifica o concedente Ministério das Cidades e objeto correspondente: https://www.guariba.sp.gov.br/portal-da-transparencia/convenios/convenio-9530432-2.
- **Resultado:** forte correspondência entre o projeto Obrasgov e instrumento federal; a recaptura integral do documento de Guariba permanece pendente em razão do HTTP 403. O convênio estadual **2901182739674/19** não está referenciado nos documentos obtidos; **nenhum vínculo SIAFEM homologado**.

### Santa Rita do Passa Quatro — Obrasgov 30692.35-17

- O projeto federal apresenta recapeamento asfáltico em diversos trechos, com executor Prefeitura Municipal e empenho federal **2023NE002685**.
- Foram identificadas diversas contratações municipais de recapeamento, que não podem ser fundidas: Pregão Presencial nº 006/2024 (Processo nº 0181/2024), Pregão Presencial nº 018/2024 (Processo nº **0405/2024**) para o **Jardim Lagoinha**, e Concorrência Eletrônica nº 006/2025 (Processo nº **00167/2025**).
- O Diário Oficial municipal registra **Contrato nº 109/2024**, com a empresa **DGB Engenharia e Construções Ltda.**, valor **R$ 315.000,00**, para recapeamento de trechos no **Jardim Lagoinha**. Fonte: https://www.dosp.com.br/impressao.php?i=NTE0ODcy e procedimento anterior: https://www.dosp.com.br/impressao.php?i=NTA0ODg5. Também foram encontrados contratos nº 106/2024 e 164/2025 de objetos de recapeamento, sem prova de identidade com o projeto.
- **Resultado:** não foi localizado número de instrumento federal que vincule um desses certames ao projeto `30692.35-17`. Os convênios estaduais candidatos nº **2901182269745/19**, **2901183131278/19**, **2901183354726/19** e **2901183414566/19** permanecem **sem vínculo demonstrado**. É necessário confirmar os trechos e as referências financeiras nos anexos dos certames.

### Serrana — Obrasgov 30461.35-22

- O projeto federal, executado pelo **Município de Serrana**, tem por objeto **recapeamento asfáltico e substituição de rede de esgoto** e apresenta repassador Ministério das Cidades, empenho federal **2023NE002700**, na API Obrasgov.
- O **Diário Oficial de Serrana nº 1.858, de 15/05/2025**, divulga o **Contrato Administrativo nº 117/2024**, Concorrência Pública nº **014/2024**, Processo nº **135/2024**, com a empresa **DGB Engenharia e Construções Ltda.**, associado ao **Contrato de Repasse federal nº 952816/2023/MCidades/CAIXA**, para obra de objeto coincidente. O aditivo de 05/05/2025 elevou o contrato a **R$ 1.157.107,62**. Fonte oficial: https://www.serrana.sp.gov.br/media/uploads/diario_oficial/diario_oficial_1858.pdf.
- O planejamento municipal também registra **outros instrumentos estaduais de recapeamento** — nº 100540/2024 e nº 73755/2024 — em documento de dezembro de 2024: https://www.serrana.sp.gov.br/media/uploads/diario_oficial/diario_oficial_1774-1.pdf. A existência de frentes estaduais de recapeamento **não demonstra** que financiem a mesma obra do repasse federal.
- **Resultado:** forte correspondência documental entre obra Obrasgov e contrato/repasse federal. O convênio estadual SIAFEM **51010120251346122** tem objeto genérico de recapeamento de diversas ruas; não foi encontrada referência a ele no contrato federal ou prova de identidade de ruas. **Nenhum vínculo estadual homologado.**

### Sertãozinho — Obrasgov 31536.35-60

- O Obrasgov identifica executor Município de Sertãozinho, repassador Ministério das Cidades e pavimentação por recapeamento de vias urbanas; a API não retornou empenho ou contrato para esse projeto específico nesta consulta.
- Extrato federal publicado no DOU de dezembro de 2023 identifica o **Contrato de Repasse nº 953043/2023**, celebrado pelo Município de Sertãozinho com o Ministério das Cidades/CAIXA, para pavimentação e recapeamento de vias urbanas, com **R$ 578.003,00** previstos como recursos federais no instrumento inicial. Repositório de cópia do DOU: https://ecrie.com.br/sistema/conteudos/arquivo/a_39_0_1_15092025102339.pdf. O DOU nº 65 de 04/04/2024 registra aditamento do mesmo contrato: https://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?captchafield=firstAccess&data=04%2F04%2F2024&jornal=530&pagina=71.
- A prefeitura publicou **Concorrência Eletrônica nº 004/2025, Processo nº 119/2025**, para recapeamento e sinalização horizontal de vias no perímetro urbano: https://www.sertaozinho.sp.gov.br/portal/editais/0/1/2845/. A **página resumida** não informa o repasse, mas o **Projeto Básico no arquivo ZIP oficial da própria licitação identifica expressamente o Contrato de Repasse nº 953043/2023/MCidades, programa 2219, ação 00T1**. Portanto, está **comprovada a vinculação federal do certame a esse instrumento**, sem qualquer comprovação de participação dos quatro convênios SIAFEM estaduais candidatos.
- Notícia municipal de 2026 informa execução de recapeamento com recursos estaduais e federais em vários bairros, mas não identifica o conjunto de instrumentos nem autoriza associar cada obra aos convênios SIAFEM candidatos: https://www.sertaozinho.sp.gov.br/portal/noticias/0/3/12686/prefeitura-executa-obras-de-recapeamento-asfaltico-em-diversos-bairros-da-cidade.
- **Resultado revisado:** o Projeto Básico municipal contém referência **documental e inequívoca** ao repasse federal nº 953043/2023, confirmando o elo instrumento–Concorrência nº 004/2025, além da correspondência do objeto com o projeto Obrasgov. O mesmo arquivo apresenta o número truncado **95043/2023** em passagem introdutória, discrepância de digitação registrada e resolvida pela referência completa em outra seção e pelo DOU. Convênios estaduais SIAFEM **290118662729/18**, **290118688542/18**, **51010120231760627** e **51010120240542814** permanecem **sem vínculo demonstrado**.

## 3. Matriz de decisão

| Município | Projeto | Instrumento federal documentado | Certame/contrato municipal | Vínculo estadual SIAFEM |
|---|---|---|---|---|
| Guariba | 30964.35-52 | 953042/2023 (prefeitura; conteúdo indexado, acesso direto 403) | Concorrência 013/2024 | NÃO comprovado |
| Santa Rita do Passa Quatro | 30692.35-17 | Não identificado | Pregões 006 e 018/2024, Concorrência 006/2025; Contrato 109/2024 para Jardim Lagoinha | NÃO comprovado |
| Serrana | 30461.35-22 | 952816/2023 | Concorrência 014/2024; Contrato 117/2024 | NÃO comprovado |
| Sertãozinho | 31536.35-60 | 953043/2023 (Projeto Básico municipal e extrato DOU) | Concorrência 004/2025 vinculada expressamente ao repasse federal; contrato de execução e medições pendentes | NÃO comprovado |

**Controle de qualidade:** os dez pares anteriores de similaridade foram mantidos como candidatos e **zero** foi promovido à tabela de instrumentos/projetos relacionados. Valor previsto Obrasgov, empenho federal, transferência estadual SIAFEM e despesa municipal liquidada são grandezas diferentes, que não devem ser somadas ou utilizadas como substitutos umas das outras.

## 4. Artefatos e próxima validação

A base de evidências foi persistida em `governance/INV_RMRP_OBRASGOV_4_PROJETOS_DOCUMENTOS_MUNICIPAIS_FEDERAIS_2026_11_12.csv` e o validador `pipeline/qa/qa_inv_rmrp_candidatos_siafem_obrasgov.py` foi ampliado para exigir os quatro projetos, identificadores federais, links de evidência e ausência de vínculos estaduais homologados.

**Próximo gate:** baixar integralmente os anexos das licitações e os projetos/memoriais de cada obra, em particular os trechos do Jardim Lagoinha em Santa Rita e os memoriais do recapeamento 004/2025 de Sertãozinho; identificar as ruas e fontes de recursos especificadas e procurar os números estaduais nos extratos municipais. Comprovação de cofinanciamento exige documento explícito de vinculação do instrumento à obra e respectivo escopo; coincidência de tema ou execução municipal não basta.

**Produção:** nenhuma alteração de R2/D1/SQLite produtivos; PR nº 233 permanece draft, com PR nº 232/FED04 preservada.


## 5. Verificação integral dos anexos da Concorrência 004/2025 e segregação de processos em Serrana — 12/11/2026

**Sertãozinho.** A página municipal `https://www.sertaozinho.sp.gov.br/portal/editais/0/1/2845/` possui link de download com redirecionamento HTML para o ZIP efetivo `https://www.sertaozinho.sp.gov.br/editais/004_-_recapeamento_asfaltico_15120805.zip`. O arquivo foi baixado no navegador autenticado como fonte pública, 2.888.706 bytes, SHA-256 **`b2889b5cf4a06c75fa8f1e1304d26d1127d15130553f139ea97b86212b30a173`**. Foram identificados 13 itens internos, entre os quais o Projeto Básico em DOCX, memoriais, planilha de custos em XLSX, plantas PDF e mapa municipal. O arquivo DOCX Projeto Básico tem SHA-256 **`4b4ab2b72fb36d841db01fd4744ee866b943ebf72368d73fb34c7077b3a70490`**, verificado pela leitura direta do XML `word/document.xml` dentro do ZIP/DOCX, sem OCR.

No Projeto Básico consta **Contrato de Repasse nº 953043/2023/MCidades, programa 2219, ação 00T1**. Uma seção introdutória escreve `95043/2023`, evidente divergência do mesmo documento; **não se deve criar segundo instrumento com base nesse erro**. Há orçamento máximo de **R$ 642.046,59**, composto por **R$ 578.003,00 de recursos federais** e **R$ 64.043,59 de recursos próprios**, soma documentalmente coincidente. O Projeto Básico identifica as vias **Rua Augusto Zanini; Rua Jordão Borguetti; Rua José Bonini; Travessa Luiz Guidugli; Rua Antônio Carotini; Rua Keitaro Hatajima**, cada qual com ponto de coordenadas geográficas referencial. Esses pontos **não** são traçados da obra.

A leitura integral do anexo **confirma a associação da Concorrência Eletrônica nº 004/2025 ao contrato de repasse federal 953043/2023**. Não comprova empenho, pagamento, medição, conclusão ou cofinanciamento estadual SIAFEM. Os quatro convênios estaduais candidatos permanecem em condição `SEM_VINCULO_ESTADUAL_COMPROVADO`. Evidência estruturada e hashes: `governance/INV_RMRP_SERTAOZINHO_004_2025_953043_PROJETO_BASICO_EVIDENCIA_2026_11_12.json`.

**Serrana.** Foi verificada uma distinção relevante entre contratos federais de objeto similar. O **anexo de minuta contratual da Concorrência 008/2024, Processo 078/2024** menciona expressamente o **repasse 952819/2023/MCidades/CAIXA**, enquanto o **Contrato Administrativo 117/2024, Concorrência 014/2024, Processo 135/2024**, conforme Diário Oficial nº 1.858 de 15/05/2025, menciona **952816/2023/MCidades/CAIXA**. São **dois processos e dois instrumentos federais distintos**, apesar da semelhança dos objetos de recapeamento e esgoto. Portanto, documentos disponíveis em `/licitacao/concorrencia_008_2024/` **não devem ser atribuídos automaticamente ao contrato 117/2024** ou ao projeto `30461.35-22`. Pendente localizar a documentação técnica própria da Concorrência 014/2024 para confirmação de trechos. Fontes: `https://www.serrana.sp.gov.br/media/uploads/licitacao/concorrencia_008_2024/4_-_anexo_ii.pdf` e `https://www.serrana.sp.gov.br/media/uploads/diario_oficial/diario_oficial_1858.pdf`.

**Controle:** novos achados demonstram um vínculo **federal** em Sertãozinho e uma distinção de dois instrumentos **federais** em Serrana. Nenhuma transferência estadual SIAFEM foi atribuída a obra específica. A base estadual de R$ 305.521.029,20 permanece intacta e não é somada aos orçamentos federais ou municipais.
