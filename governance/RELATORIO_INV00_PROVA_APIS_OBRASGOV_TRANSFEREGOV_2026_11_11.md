# INV00 — Provas de acesso das APIs Transferegov e Obrasgov (11/11/2026)

**Escopo:** sondagem pública read-only das APIs e de uma página de projetos em SP; não constitui extração estadual nem homologação de pagamentos. **Método:** Browserless com acesso HTTPS à origem oficial de cada API, `fetch()` de OpenAPI v3.1.0, teste de endpoint com limite cinco registros, comparação da resposta e registro de parâmetros.

## APIs efetivamente consultadas

| Origem | Endpoint | HTTP | OpenAPI | Rotas | Evidência |
|---|---|---:|---|---:|---|
| Transferegov — Parcerias | https://api-publica.transferegov.gestao.gov.br/parcerias/openapi.json | 200 | 3.1.0 | 18 | contrato retornado |
| Transferegov — Especiais | https://api-publica.transferegov.gestao.gov.br/especiais/openapi.json | 200 | 3.1.0 | 24 | contrato retornado |
| Transferegov — Discricionárias/Legais | https://api-publica.transferegov.gestao.gov.br/discricionarias/openapi.json | 200 | 3.1.0 | 13 | contrato retornado |
| Obrasgov — Projetos | https://api-publica.obrasgov.gestao.gov.br/obras/openapi.json | 200 | 3.1.0 | 8 | contrato retornado em sessão dedicada à mesma origem |

**Total:** quatro contratos públicos e **63 rotas documentadas**, mas **não necessariamente 63 rotas operacionais de dados**, e sem prova de completude ou disponibilidade de pagamentos. O download cross-origin de Obrasgov na página Transferegov falhou, mas o teste na origem própria Obrasgov respondeu HTTP 200, caracterizando restrição de origem/navegador e não indisponibilidade geral da API.

### Obrasgov — primeiro retorno de dados (UF=SP)

GET `https://api-publica.obrasgov.gestao.gov.br/obras/projeto-investimento?uf_principal=SP&pagina=1&tamanho_da_pagina=5` → **HTTP 200**. Resposta JSON com `data`, `total_pages`, `total_items`, `page_number`, `page_size`.

- `total_items=20942`; `total_pages=4189`, `page_number=1`, `page_size=5`; **cinco registros retornados**. São contagens **declaradas pela API para o filtro `uf_principal=SP` em 11/11/2026**, não enumeração completa, nem contagem validada de empreendimentos distintos em execução, concluídos ou com pagamento.
- IDs nos cinco primeiros registros: `90697.35-39`, `13148.35-25`, `102443.35-00`, `130316.35-00`, `35007.35-90`.
- Os cinco registros amostrais continham ao menos uma geometria `pins` e uma entrada em `investimentos_previstos`. **Não extrapolar 5/5 à população**.
- O contrato expõe rotas: `/data-atualizacao`, `/projeto-investimento`, `/empenho`, `/execucao-fisica`, `/contrato`, `/geometria`, `/historico-situacao-cancelada-paralisada`, `/estudo-viabilidade`.
- `/projeto-investimento` suporta `uf_principal`, `situacao`, `pagina` e `tamanho_da_pagina` de 1 a 200, dentre outros parâmetros; é adequada a **paginação estadual**. Antes de adquirir todas as páginas, conferir limite/consistência e paginação estável por snapshot.

**Exemplos de classificação e geolocalização:**
- `90697.35-39`: qualificação viária e pavimentação em **Campina do Monte Alegre**, situação **Cadastrada**, investimento previsto **R$1.442.600,02**, fonte **Federal**, PIN `POINT (-48.47714 -23.59272)`; organização repassadora Ministério das Cidades; natureza Obra. **Não comprova obra em execução ou pagamento**.
- `13148.35-25`: pista de skate em **Santos**, situação **Concluída**, investimento previsto **R$3.304.263,70**, fonte **Federal**, PIN `POINT (-45.35308 -23.97125)`; natureza Obra. **Situação cadastral não equivale automaticamente a obra finalizada e recebida ou pagamento integral**.

### Transferegov — proposta existente G06-F3, verificação de natureza de despesa

GET `https://api-publica.transferegov.gestao.gov.br/parcerias/proposta?id_proposta=75094&pagina=1&tamanho_da_pagina=5` → HTTP 200, registro com `id_proposta=75094`, município recebedor **São José do Rio Preto (3549805)**, fundo municipal de saúde recebedor, `vl_total_planejamento_gastos=2000000`, objeto de incremento do atendimento especializado MAC e **categoria de despesa `Custeio` / subcategoria `Serviços`**.

**Achado anti-falso-investimento:** a mera presença no módulo de Parcerias, a existência de fundo público recebedor, ou o valor de planejamento NÃO autorizam classificar o item como investimento de capital. A categorização precisa ser capturada da proposta/instrumento e confrontada com execução.

## Pendências técnicas e operação recomendada

1. Capturar **todos os projetos SP Obrasgov**, com controle de paginação, chave estável, timestamps, `total_items`, snapshots/hashes, campos nulos, agrupamentos espaciais e duplicação por obra/projeto. Evitar publicar `20942` como número de investimentos financiados sem auditoria.
2. Avaliar as rotas `empenho`, `execucao-fisica`, `geometria` e `contrato`, preservando `id_projeto_investimento` nas relações e distinguindo o estágio.
3. Obter CSVs nacionais Discricionárias/Legais; dados completos e financeiros do Transferegov Especiais; testar CGU para desembolsos. Não fazer junção de pagamento por similaridade de valor.
4. Para gestão de Parcerias, capturar `categorias_despesa_proposta` como evidência de custeio versus capital e **não inferir liquidação ou pagamento da simples aprovação**.
5. Antes de promover, obter fonte de repasse estadual SIAFEM e projetos próprios do Estado não associados a transferências.
6. Esta sondagem **não alterou bases**, não gerou R2, SQLite, Cloudflare, deployment ou publicação.

**Status:** `INV00` parcialmente verificado para OpenAPI, `INV01` ainda não iniciado (sem snapshots completos de dados).
