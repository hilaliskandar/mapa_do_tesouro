
> **Nota de retificação (12/11/2026):** a seção 7, após leitura dos documentos assinados do processo 135/2024, substitui conclusões anteriores sobre suposta divergência entre contrato assinado 117/2024 e aditivo. Ambos apontam 952816/2023; cadastro e resumos apontam 952819/2023.

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
- O **Diário Oficial de Serrana nº 1.858, de 15/05/2025**, divulga o **aditivo** do Contrato Administrativo nº **117/2024**, Concorrência Pública nº **014/2024**, Processo nº **135/2024**, com a empresa **DGB Engenharia e Construções Ltda.**, mencionando repasse federal **952816/2023/MCidades/CAIXA** para obra de objeto semelhante. **Entretanto, a publicação original do Contrato nº 117/2024 (Diário nº 1.701, de 05/09/2024) menciona 952819/2023.** O aditivo de 05/05/2025 elevou o contrato a **R$ 1.157.107,62**. Fonte oficial: https://www.serrana.sp.gov.br/media/uploads/diario_oficial/diario_oficial_1858.pdf.
- O planejamento municipal também registra **outros instrumentos estaduais de recapeamento** — nº 100540/2024 e nº 73755/2024 — em documento de dezembro de 2024: https://www.serrana.sp.gov.br/media/uploads/diario_oficial/diario_oficial_1774-1.pdf. A existência de frentes estaduais de recapeamento **não demonstra** que financiem a mesma obra do repasse federal.
- **Resultado corrigido:** a identidade entre o projeto Obrasgov e o Contrato 117/2024 **não está homologada**: a publicação original do contrato indica 952819/2023, enquanto o aditivo indica 952816/2023 e o empenho do projeto é associado a 952816/2023. O convênio estadual SIAFEM **51010120251346122** tem objeto genérico de recapeamento de diversas ruas; não foi encontrada referência a ele no contrato federal ou prova de identidade de ruas. **Nenhum vínculo estadual homologado.**

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
| Serrana | 30461.35-22 | 952816/2023 no projeto federal; 952819/2023 na publicação original do contrato municipal | Concorrência 014/2024; Contrato 117/2024 com referência contraditória no aditivo de 2025 | NÃO comprovado |
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

**Serrana — revisão cronológica obrigatória.** A Concorrência 008/2024, Processo 078/2024, traz o repasse **952819/2023** e foi declarada **deserta** em junho de 2024. Posteriormente, a Concorrência 014/2024, Processo 135/2024, também citou **952819/2023** no aviso e na publicação original do Contrato 117/2024, enquanto seu **aditivo de maio de 2025 cita 952816/2023**. Portanto, há uma **contradição documental dentro do mesmo processo contratual**, e não é possível afirmar que o contrato 117/2024 tenha sido originalmente vinculado a 952816/2023. Os dois números correspondem a instrumentos federais distintos existentes. O empenho federal **2023NE002700** do projeto Obrasgov está associado no extrato federal a **952816/2023**, porém **não existe prova suficiente de que corresponda ao Contrato 117/2024**, que originalmente traz 952819/2023. Nenhuma associação Obrasgov–contrato municipal deve ser homologada antes de obter contrato assinado, retificação e anexos do Processo 135/2024. Fonte cronológica: Diários municipais nº 1.624 (17/05/2024), nº 1.661 (12/07/2024), nº 1.666 (19/07/2024), nº 1.701 (05/09/2024) e nº 1.858 (15/05/2025). Evidência detalhada em `governance/INV_RMRP_SERRANA_117_2024_CONFLITO_REPASSES_952819_952816_2026_11_12.json`. Fontes: `https://www.serrana.sp.gov.br/media/uploads/licitacao/concorrencia_008_2024/4_-_anexo_ii.pdf` e `https://www.serrana.sp.gov.br/media/uploads/diario_oficial/diario_oficial_1858.pdf`.

**Controle:** novos achados demonstram um vínculo **federal** em Sertãozinho e uma distinção de dois instrumentos **federais** em Serrana. Nenhuma transferência estadual SIAFEM foi atribuída a obra específica. A base estadual de R$ 305.521.029,20 permanece intacta e não é somada aos orçamentos federais ou municipais.

## 6. Retificação expressa da conclusão anterior sobre Serrana

A verificação dos Diários Oficiais nº **1.666** e **1.701** demonstrou que o aviso da Concorrência nº **014/2024** e o Contrato nº **117/2024** publicado originalmente mencionam **952819/2023**, ao passo que o aditivo de 2025 menciona **952816/2023**. Assim, **qualquer afirmação anterior de que o Contrato 117/2024 estava documentalmente confirmado como execução do repasse 952816/2023 deve ser considerada superada**. Este estudo só homologa o vínculo federal do **Projeto Básico da Concorrência 004/2025 de Sertãozinho** ao repasse 953043/2023; para Serrana, o vínculo entre contrato municipal e projeto Obrasgov permanece em revisão. Não há qualquer vínculo SIAFEM estadual homologado.


## 7. Retificação definitiva após leitura do contrato assinado e edital integral de Serrana

**12/11/2026 — esta seção substitui quaisquer conclusões precedentes que afirmem que o Contrato 117/2024 assinado teria originalmente citado 952819/2023.** O portal oficial da Prefeitura de Serrana disponibiliza o acervo específico da Concorrência 014/2024 em **https://www.serrana.sp.gov.br/licitacoes/1594**, com o contrato assinado, aditivo, edital, aviso, minuta, anexos, atas e homologação. Todos os PDFs primários foram obtidos efetivamente por navegação e a camada textual foi lida diretamente com PDF.js. O Crawl2AI apresentou erro interno para URLs pesquisados e o navegador de consulta textual público não abriu os PDFs; o navegador Browserless obteve os arquivos em HTTP 200.

**Cinco documentos integrais do próprio processo 135/2024 indicam inequivocamente 952816/2023, não 952819/2023:**

| Documento oficial | Página de referência | Repasse encontrado | SHA-256 do arquivo |
|---|---:|---|---|
| Aviso de licitação PDF | 1 | 952816/2023 | `eb3c91961851c518d0fbfbba295140adabceb615ec10f7693dae51209fc6bc9d` |
| Edital nº 042/2024, Concorrência 014/2024 | 1, 2 | 952816/2023 | `294040b5db56c694dee16f54238c8d56382d1150296edbda642cb24be16a34c9` |
| Anexo II, minuta contratual | 1, 2, 8 | 952816/2023 | `3eeb77ee3e1ef0c1fa4197523e7b30b86697d9f7be888bc7b5ab3b054c04ed3e` |
| Contrato nº 117/2024 **assinado**, DGB Engenharia | 1, 2, 10 | 952816/2023 | `fe09a75265b7338aa5301c349bb9e91be7bc746240e47143d616dc2364a84824` |
| Primeiro termo aditivo do Contrato 117/2024 | 1, 5 | 952816/2023 | `55418d284de30b3942d84e8e486e6de66aa28e2b9e850338aebb60abf24c5133` |

No Contrato nº 117/2024 assinado, a cláusula de custeio (página 10) informa **R$ 960.019,00 de recursos federais e R$ 2.069,57 de recursos próprios**, totalizando **R$ 962.088,57**, mesmo valor contratado. O aditivo aumentou o contrato em **R$ 195.019,05**, para **R$ 1.157.107,62**. A entidade contratada é DGB Engenharia e Construções Ltda. O PDF de 15 páginas tem assinatura digital identificável da contratada e demais assinaturas; não se presumiu validade criptográfica da assinatura sem certificação externa.

**Origem da divergência:** o **cadastro eletrônico da Concorrência 014/2024** (https://www.serrana.sp.gov.br/licitacoes/1594) e o resumo do Diário Oficial inicial apresentam **952819/2023**. A Concorrência anterior 008/2024 (https://www.serrana.sp.gov.br/licitacoes/1541) também apresenta 952819/2023 e havia sido declarada deserta. Não se demonstrou nos documentos integrais da Concorrência 014 que o repasse 952819 fosse a fonte do Contrato 117/2024. A fonte técnica e jurídica prioritária é o **documento assinado**, e não o cadastro resumido: assim, o erro analítico anterior foi retificado.

O **Anexo I técnico próprio do Processo 135/2024** (https://www.serrana.sp.gov.br/media/uploads/licitacao/concorr%C3%AAncia_014_2024/3_-_anexo_i.pdf) tem 34 páginas e 17.704.759 bytes, hash `39aa80b7f09f8971ae0d5806bc5e8e64d88c33f529b5f86d812d92525cf7b415`, **sem camada textual pesquisável**; ruas/trechos e outros aspectos técnicos ainda exigem leitura das plantas ou extração especializada. **Não foi utilizado o Anexo I da Concorrência 008 como substituto.**

**Situação corrigida:** o Contrato nº 117/2024 está documentalmente associado ao **repasse federal 952816/2023**. Esse número também foi identificado no registro federal relativo ao projeto Obrasgov 30461.35-22; a associação financeira federal agora é fortemente respaldada por identificador comum, mas a **identidade dos trechos da obra e a execução física/financeira final ainda exigem análise do Anexo I e das medições**. O financiamento estadual SIAFEM permanece **não comprovado** e nenhum valor foi somado ao total estadual.
