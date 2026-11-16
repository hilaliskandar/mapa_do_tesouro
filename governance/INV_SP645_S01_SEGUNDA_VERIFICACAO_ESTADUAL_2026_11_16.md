# S01 — segunda verificação das fontes estaduais e descoberta de novas modalidades

Data: 16/11/2026. Branch: `investimentos-territoriais-sp645-20261111`. Escopo: **descoberta e caracterização**, sem microdados financeiros adquiridos.

## 1. Evidência direta via Crawl2AI

| Página oficial | Evidência recuperada | Restrição |
|---|---|---|
| https://www.transparencia.sp.gov.br/Convenios | HTML sanitizado tem botão identificado `id="btnExportarCsv"`; tabela de consulta com filtros; página declara atualização 15/11/2026 11:03 | URL/POST efetivo do botão não identificado no HTML sanitizado; CSV ainda não baixado |
| https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx | HTML contém `<form name="form1" id="form1">` e campos `__VIEWSTATE`, `__VIEWSTATEGENERATOR`, `__EVENTVALIDATION` típicos de ASP.NET Web Forms | Não interpretar o valor dinâmico desses campos como token estável; nenhum POST de consulta foi executado; não foi identificado endpoint bulk |
| https://www.transparencia.sp.gov.br/EmendasParlamentares/Concedidas | Portal exibe emendas concedidas, categorias de finalidade e transferências especiais estaduais, filtros por beneficiário/localização, valor previsto e repassado, exportação CSV e dicionário | CSV/IDs ainda não recuperados; valor previsto não é o mesmo que repassado |
| https://www.transparencia.sp.gov.br/EmendasParlamentares/Realizadas | O próprio título visível é **Transferências Especiais Federais**; também há opção CSV e plano de ação | Fonte de perspectiva do **órgão estadual** sobre repasses federais; não classificar como emenda estadual e prevenir duplicidade com Transferegov |
| https://www.transparencia.sp.gov.br/Home/MapSite | Mapa de páginas oficiais inclui Convênios e Transferências realizadas, despesas, ordens bancárias, emendas, consulta livre e temporal de execução | Links são candidatos a validação, não APIs ou downloads comprovados |

A camada de extração do Crawl2AI fornece HTML **pré-processado/sanitizado**, que não inclui scripts da página. Logo, não permite inferir com segurança o método AJAX ou os parâmetros HTTP do evento `btnExportarCsv`. Tentativa anterior com `execute_js` falhou no conector; não foi reportado sucesso de simulação de clique nem de arquivo capturado.

## 2. Decisões metodológicas

1. **Criar fonte autônoma SP_EMENDAS_CONC**, com indicador `valor_repassado` separado de `valor_previsto`, evitando soma com convênios que materializem a mesma emenda.
2. **Criar fonte SP_EMENDAS_REAL como referência cruzada federal**, pois o portal a apresenta sob a rubrica 'Transferências Especiais Federais'; conciliar com Transferegov em vez de somar montantes.
3. **Manter SP_CONV e SP_SEFAZ como fontes P0 de maior urgência**. O próximo passo é obter o CSV ou o histórico de requisições do botão, depois inspecionar a interface ASP.NET e sua possibilidade de consulta reprodutível.
4. Criar controles separados de **fonte identificada**, **mecanismo de download confirmado**, **download executado**, **arquivo com hash validado**, **dados normalizados**, **conciliação aprovada**, **indicador publicado**. Não pular etapas.
5. Preservar o histórico FED01–FED21 em filas de exceção; não deslocar a prioridade para os 19 projetos.

## 3. Procedimentos técnicos propostos

### SP_CONV

Obter o documento HTML não sanitizado (ou sessão gráfica com acesso à aba Rede) e localizar os listeners de `#btnExportarCsv`. Registrar método HTTP, URL do download, parâmetros, sessão, exigência de cabeçalhos, cobertura sem filtros e limite de linhas. Fazer uma **única amostra controlada**, documentar cabeçalho, linhas, encoding e período; só então preparar coleta histórica por ano ou arquivo estadual integral. Utilizar o dicionário oficial https://www.transparencia.sp.gov.br/Dicionarios/Dicion%C3%A1rio%20de%20dados_conv%C3%AAnios.xlsx para tipar dados após aquisição.

### SP_SEFAZ

Inspecionar o formulário em sessão reutilizável, capturar nomes de campos, eventos postback, opções de período e convenente e persistir parâmetros dinâmicos por solicitação. Executar consulta piloto por um município/competência com controle de estornos; procurar antes alternativa de dados abertos/CSV estável na própria Sefaz. Não automatizar contorno de autenticação, captcha ou bloqueios.

### SP_EMENDAS_CONC e SP_EMENDAS_REAL

Validar rotas de exportação, granularidade por emenda, órgão, beneficiário e valor repassado. Não imputar percentuais normativos de capital/custeio como realização financeira; distinguir regra de aplicação e pagamento observado. Registrar potencial duplicidade entre emenda, convênio e transferência da mesma operação.

## 4. Saída deste ciclo e próximo gate

Atualizados os controles `fontes.csv`, `endpoints.csv` e `pendencias.csv` no diretório [investimentos_sp645](controls/investimentos_sp645/). **Nenhum registro foi incluído em `execucoes.csv`, `snapshots.csv`, `cobertura.csv` ou `conciliacoes.csv`**, pois esta rodada de descoberta não produziu microdados ou pacotes financeiros completos com manifesto verificável.

Próximo gate: identificação comprovada do mecanismo de exportação e primeiro CSV estadual armazenado, com SHA-256, contagem de linhas, schema, município/ano e arquivo de origem. Se não houver extração confiável, registrar impedimento explícito e priorizar fonte alternativa de dados abertos, sem produzir resultados fictícios.

`public_release_authorized=false`; SQLite/Pages públicos inalterados.
