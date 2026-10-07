# Candidate de preview — 2026-10-07

## Commit de referência

- main: `ea37935182b01fd7f36c5f7d49ce430437802f48`

## Artefato local validado

- arquivo: `financas-municipais-sp-preview-ready.zip`
- tamanho aproximado: 2,2 MiB
- SHA-256: `3ca3ceb8aebd8df1b37db4edfd91c6b9792e3aa4bdeda1509428348eb0014a90`

## Conteúdo

O pacote contém o site estático pronto para preview, incluindo:

- HTML, CSS e JavaScript;
- 13 snapshots anuais;
- 30 arquivos municipais;
- catálogo documental;
- metodologia;
- cobertura;
- crosswalk;
- 30 geometrias municipais;
- `_headers` com políticas de segurança/cache.

## QA

- 30 municípios;
- 2013–2025;
- 75 objetos documentados;
- JavaScript sintaticamente válido;
- nenhuma ocorrência de `cache: "no-store"`;
- 30 geometrias no mapa;
- build real anteriormente validada com 870 pares dirigidos;
- publicação deve ocorrer inicialmente como preview.

## Deployment

O upload ao Cloudflare Pages exige sessão Wrangler/autenticação operacional local. Credenciais, account IDs, projeto real e domínio permanecem fora do repositório público.
