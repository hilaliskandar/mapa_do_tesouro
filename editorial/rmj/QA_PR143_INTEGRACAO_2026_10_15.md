# Revisão de integração do PR #143 — 2026-10-15

Estado: **RETER EM RASCUNHO**. Não executar merge ou publicação de produção.

## Evidências verificadas
- PR #143 contém 15 arquivos alterados, incluindo boletim HTML, rotinas TCESP, testes de navegador, workflow de preview e protocolo dos 12 universos.
- Core CI e Pages Preview no commit `4530e9741bc390ad3c2293e3282a130c88202a2c`: concluídos com sucesso (runs 38083298053 e 38083298057). Isto não prova aprovação do workflow independente de extração `rmj-editorial-preview.yml`.
- `editorial/rmj/conciliacao_tcesp_dca_2023_2024.csv` declara 14 resultados `CONCILIADO`, mas `editorial/rmj/RETOMADA_2026-10-10.md` afirma que a execução anteriormente consultada foi cancelada antes de comprovar as 14 consultas. Há inconsistência de rastreabilidade, ainda que não se conclua erro dos valores.
- `editorial/rmj/qa_tcesp_2023_2024.py` verifica somente integridade de extração e escreve `PENDENTE_DCA`: não confere a DCA canônica.
- A extração TCESP no workflow é `continue-on-error`, e os testes e deploy prosseguem mesmo com ausência de evidência TCESP; isto é aceitável para complemento opcional, desde que nenhum conteúdo dependente dessa evidência seja anunciado como certificado.
- O protocolo editorial prioriza FINBRA/DCA e limita TCESP detalhado a estudos específicos. Não há justificativa para transformar a coleta dos 23 municípios externos à RMJ em requisito de merge.
- Protocolo propõe 12 universos, enquanto API editorial v0.4.0 tem 11; TIC_TIM_30 exige contrato editorial próprio se publicado como 12º.

## Gates antes do merge
1. **G0:** identificar o artifact, job, arquivo, SHA-256 e fonte oficial para cada uma das 14 conciliações TCESP × DCA 2023/24; não confiar apenas na tabela de resultados.
2. **G1:** rodar verificação em centavos, por município/ano e estágio, dos totais de investimento; erros e divergências impedem promoção desses dados. Uma execução sem erros de download não equivale à conciliação.
3. **G2:** manter o resumo FINBRA como independente da extração TCESP; marcar conteúdo complementar como `pendente` quando G0/G1 falharem.
4. **G3:** conferir dados, links, gráfico/tabela, acessibilidade e status HTML com prévia remota e evidência de navegador dos dois tamanhos de tela.
5. **G4:** resolver diferença 11 vs 12 universos, sem alterar cadastro fiscal de produção por conveniência editorial.
6. **G5:** confirmar deflator e ano-base antes de exibir valores reais; na falta, identificar a série como nominal.
7. **G6:** reexecutar CI e preview após integração dos PRs #166 e #167 em `main`. Não publicar automaticamente.
8. **G7:** obter aprovação editorial expressa para versão final.

## Extração adicional
Não realizar coleta maciça ou inferência de dados sem necessidade documentada. Prioridade: recuperar artifacts existentes do GitHub Actions, que preservam as fontes usadas, e confrontar os extratos com a DCA já homologada. Nova consulta à fonte TCESP somente para pares com artifact ausente, corrompido ou divergente; guardar SHA, URL, ano, município, estágio e momento da coleta.

## Situação em 2026-10-15
PR mantido em rascunho, pendências acima abertas. A incorporação dos PRs #166 e #167 não altera por si a prova de conciliação editorial.

## Evidência adicional recuperada e examinada

O artifact GitHub Actions `11680818755`, gerado no run `38083298057`, foi recuperado e auditado. O ZIP tem SHA-256 `3c7d59fdc6fe570d93af0f26ae4bbf0176dc24858f13fd8da5305f8bc0fd48c7`. Contém 14 JSONs municipais de 2023–2024, logs, manifesto e `qa_summary.json` com 14 extrações bem-sucedidas e zero erros. O controle original declara `pendentes_conciliacao_dca=14`.

A auditoria independente dos JSONs confirmou 14/14 equivalências exatas, em centavos, com **a coluna TCESP** de `editorial/rmj/conciliacao_tcesp_dca_2023_2024.csv`, além do fechamento dos totais de programa e ação do grupo 44 liquidado e presença de hashes ZIP nos 14 extratos. **Não foi feita leitura independente do arquivo canônico DCA para validar a coluna DCA da tabela.** Logo, a expressão `CONCILIADO` da tabela ainda requer comprovação dessa segunda fonte. Este achado substitui a suspeita inicial de ausência dos extratos, mas não aprova a conciliação interfontes.

Não é necessária nova extração TCESP para esses 14 casos: os dados primários da extração já estão preservados no artifact. Nova coleta só se justifica após demonstrar lacuna/retificação ou discrepância em fonte primária.

## Gate G1 aprovado — conciliacao independente 2023–2024

Arquivo DCA canônico obtido diretamente do Google Drive: ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, nome `DCA_SP_645_2013_2025_CANONICO.csv`, SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5` (hash aprovado do Gate B). Para cada um dos sete códigos IBGE e anos 2023 e 2024, o campo `dca_investimentos_liquidada` foi lido diretamente desse CSV e convertido em centavos via `Decimal`, sem arredondamento de ponto flutuante. Os montantes foram comparados com `investimento_44_liquidado_centavos` dos 14 JSONs do artifact TCESP `11680818755` (SHA-256 ZIP `3c7d59fdc6fe570d93af0f26ae4bbf0176dc24858f13fd8da5305f8bc0fd48c7`). **Resultado: 14/14 conciliações exatas; diferença de 0 centavo em todos os casos.** Esse teste valida a paridade de totais de investimento liquidado desses pares; não homologa automaticamente programas/ações individualmente nem exercícios de outros municípios. G0/G1 dos 14 pares ficam aprovados; G2–G7 permanecem conforme exigências anteriores.

## Revisão adicional de HTML e CI — 2026-10-15

Após atualização do ramo para `6cdbeace25f2b856ea9eb0755b94302a5609120f`, Core CI `38677928774` e Pages Preview `38677928724` foram concluídos com sucesso. Nesta última execução, os jobs `build-deploy-qa`, `rmj-tcesp-historical-evidence` e os três jobs complementares de 23 municípios também reportaram sucesso. Esses resultados não substituem o workflow separado `RMJ Editorial Preview` e seu `qa_browser.cjs`; não foi obtida prova independente da execução recente desse teste de navegador. A URL pública do preview RMJ não pôde ser aberta pelo navegador de consulta deste ambiente: disponibilidade remota não homologada nesta revisão.

Inspeção direta do `editorial/rmj/index.html`: título e aviso **PILOTO EDITORIAL — EM REVISÃO**, capítulos de receitas, despesas, território e reconciliação; o HTML declara expressamente que os montantes permanecem **nominais**, à espera de série anual de IPCA aprovada. A existência de referência textual a TCESP não substitui hyperlinks explícitos para os documentos de fonte; revisar fontes clicáveis no produto final. O cabeçalho limita a edição a 'Exercícios 2024 e 2025' enquanto existe análise de tendências 2021–2025; editar o escopo de maneira inequívoca na revisão editorial.

**Decisão:** manter PR #143 como rascunho; gates pendentes: QA visual remoto comprovado, rastreabilidade dos links e recorte temporal de abertura, compatibilidade editorial 11/12 universos, autorização de publicação. G0/G1 para os 14 extratos TCESP de 2023–2024 permanecem aprovados.

## Disponibilidade da prévia — verificação adicional

A URL `https://rmj-piloto.finbra-tic-tim-referencia.pages.dev/` foi recuperada com sucesso por Crawl2AI em 2026-10-15. O conteúdo retornado confirma o título, navegação e aviso de piloto editorial, mas **ainda exibe o cabeçalho anterior** ('Exercícios 2024 e 2025'). Isso demonstra que o novo commit de correção do cabeçalho ainda não foi verificado na prévia remota. A consulta de conteúdo não equivale ao teste automatizado Playwright de interação, responsividade e console; o gate visual permanece pendente.

## Atualizacao operacional de 15/10/2026 — preview e QA preventivo

O endpoint `https://rmj-piloto.finbra-tic-tim-referencia.pages.dev/` foi novamente recuperado via Crawl2AI, agora com o cabeçalho **'Referência principal: 2024 e 2025; séries históricas selecionadas: 2021–2025'**, confirmando a atualização da prévia pública. Foram identificadas referências externas ao arquivo DCA do Drive, ao contexto editorial da API, ao IBGE/SIDRA, à documentação e ao repositório. Esta verificação é de conteúdo HTTP e links publicados, não um teste real de navegador/JS.

O arquivo `editorial/rmj/check_html.py` foi reforçado no commit `549c5bca214c0414102be7263bc372c3dbe14d2a`, adicionando controles de presença de links de fontes, delimitação temporal e advertência de montantes nominais. Novos workflows Core CI e Pages Preview foram acionados (runs `38680328880` e `38680328881`, ainda em fila na observação inicial), sem inferir sucesso antes de resultado. O workflow especifico RMJ Editorial Preview e a comprovacao de responsividade/console continuam gates pendentes.

Decisao: reter o PR em rascunho, com G0/G1 aprovados (14/14 conciliacoes TCESP x DCA) e gate de HTML/QA em revisao. Nenhum merge nem alteracao deliberada da producao estadual nesta etapa.

## Diretriz editorial adicional — separacao publico/interno

Decisao do usuario em 2026-10-15: o boletim destina-se ao publico externo geral, nao devendo exibir termos internos de controle de versao, QA, pipelines, manifestos, dificuldades de extracao, inventarios de arquivo ou situacao de PR. Esses registros permanecem exclusivamente neste caderno de governanca e nos artefatos de auditoria. Preservam-se no boletim explicacoes de conceitos, fontes oficiais acessiveis, periodos, cobertura, numeros comparaveis, formulas legiveis e limitacoes substantivas indispensaveis a interpretacao.

Aplicacao inicial: HTML limpo de selo 'piloto editorial em revisao', versao interna, rodape de governanca e secao de inventario operacional; substituidos por explicacao ao leitor das despesas, investimentos e das fontes. Validador estrutural e testes foram alinhados para nao exigirem metadados internos no HTML. Commits no ramo: `290f458f`, `107c2ea0`, `ee1b2b61`, `80512ce6`, `96cfcbcf`. Publicacao de producao nao autorizada; PR permanece em rascunho ate novos testes e revisao.
