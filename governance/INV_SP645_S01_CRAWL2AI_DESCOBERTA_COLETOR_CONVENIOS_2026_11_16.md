# S01 — descoberta da coleta oficial de convênios SP por Crawl2AI

**Data:** 16/11/2026. **Situação:** identificação de fonte e implementação inicial do coletor, **sem transferência concluída de ZIP nesta sessão**.

## 1. Ferramenta e evidência

O conector **Crawl2AI/Crawl4AI** foi chamado diretamente em `https://www.transparencia.sp.gov.br/Convenios` por `crawl` sem configurações especiais. Diferentemente da extração `html` sanitizada, a resposta `crawl` forneceu HTML completo com JavaScript inline e link real para dados abertos.

Identificações diretas no código oficial:

- ZIP de dados abertos no atributo `href="/Dados Abertos/Convenios/convenio.zip"`, URL resolvida: `https://www.transparencia.sp.gov.br/Dados%20Abertos/Convenios/convenio.zip`.
- `exportarCsv()` chama `baixarArquivo('/Convenios/ExportarCsv', ...)`.
- `baixarArquivo` usa **POST**, cabeçalho `Content-Type: application/json` e corpo `JSON.stringify(montarFiltro(1))`.
- `montarFiltro(page)` define `orgaoCelebrante`, `unidadeCelebrante`, `tipoInstrumentoJuridico`, `nomeBeneficiario`, `cnpjBeneficiario`, `anoCelebracao`, `page`, `pageSize` e `totalItens`; filtros sem preenchimento retornam `null`.
- Busca de resultados `POST /Convenios/Buscar`; resposta manipulada em `res.items`, `res.page`, `res.totalPages`, `res.totalItems`, `res.pageSize` e `res.ultimaAtualizacao`.
- Chamada GET do `/Convenios/ExportarCsv` pelo Crawl2AI retornou **HTTP 405** e cabeçalho `Allow: POST`, compatível com a definição da página.
- Tentativa de navegação `crawl` ao ZIP encontrou `Page.goto: Download is starting`: **evidência de início de download**, mas o conector **não entregou arquivo** ou bytes ao agente. Tentativa adicional em ambiente de download retornou falha; não foi verificado arquivo, tamanho, CRC ou hash. Não converter esse resultado em aquisição concluída.
- Módulo `execute_js` do conector falhou mesmo em script simples; tentativas com opções de `crawl` para JS/download também geraram erro do conector. O `crawl` padrão foi bem-sucedido para obter o contrato.

## 2. Produto técnico registrado

Criado [`pipeline/coleta/collect_sp_convenios_oficial.py`](../pipeline/coleta/collect_sp_convenios_oficial.py): coletor **somente-leitura**, com opção explícita `--download`, download ZIP do endpoint oficial, restrição de host, arquivo com timestamp UTC, limite de tamanho, SHA-256, teste CRC, inventário dos membros ZIP e manifesto JSON. **Código versionado, ainda não executado em ambiente com acesso e ZIP baixado**. O QA estrutural não equivale a conciliação de valores, cobertura histórica ou homologação financeira. Recomenda-se executar no runner remoto de coleta já validado nas aquisições Transferegov, sem depender do navegador Browserless cujo plano atingiu limite nesta sessão.

## 3. Próximo gate executável

1. Executar `python pipeline/coleta/collect_sp_convenios_oficial.py --download --outdir <diretorio_privado>` em executor remoto com conectividade e espaço adequados; **não gravar microdados pessoais no repositório**.
2. Conferir resposta HTTP, tamanho, hash, CRC, membros e dicionário oficial de convênios.
3. Analisar schema, período coberto, chaves, CNPJ, beneficiários e tipos de instrumento; confrontar totais das consultas do portal.
4. Somente após QA, persistir o snapshot bruto no R2 privado e registrar `execucoes.csv`/`snapshots.csv` e a cobertura SP645.
5. Se arquivo completo tiver período inferior ao necessário, usar `POST /Convenios/Buscar` ou `POST /Convenios/ExportarCsv` com filtros por ano e checkpoint, após teste de limites.

**Importante:** a obtenção de um ZIP geral em lote é preferível a 645 consultas repetidas por município, desde que comprovada abrangência. `public_release_authorized=false`.
