# Gate cadastral RMRP — candidata estadual SP645

**Data:** 23/11/2026. **Frente:** publicação controlada da dimensão territorial, sem promoção financeira.

## Correção de rota

O pipeline genérico `.github/workflows/pages-preview.yml` materializa um snapshot de referência de 30 municípios e é usado para a PR 233; **não** constitui o pipeline estadual autorizado para reconstituir a produção de 645 municípios. A implantação correta da release estadual v0.4.0 usa `.github/workflows/pages-sp645-production.yml` com fonte canônica R2, rebuild SP645 e QA estadual. A candidata estadual é `.github/workflows/pages-sp645-candidate.yml`.

## Implementação concluída no código

- Criado `deployment/materialize_rmrp_territorial_sp645.py`, que verifica o catálogo contra o CSV oficial do projeto e exige 34 códigos IBGE7 únicos, quatro sub-regiões com composição 15/6/6/7 e somente três campos municipais estritamente cadastrais.
- No modo `--site`, exige build SP645 preexistente com `index.html` e `data/metadata.json`, e copia **somente** `territorio-rmrp-validado.html` e `data/api/v3/investimentos/rmrp/territorio-validado.json`. Não copia as outras páginas e APIs experimentais de investimentos.
- No modo `--url`, consulta via HTTPS os mesmos recursos publicados e repete a validação, incluindo Content-Type de JSON.
- O workflow de candidata `pages-sp645-candidate.yml` foi atualizado com o overlay limitado após o build SP645 e validação HTTP remota isolada, preservando `qa_sp645_pages.py`, `qa_api_v2.py` e `qa_remote_sp645_v2_json.py` já existentes.

## Execução de QA solicitada

[GitHub Actions run 45285817646](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45285817646), branch `investimentos-territoriais-sp645-20261111`, workflow `pages-sp645-candidate.yml`, entrada `alias=sp645-rmrp-cadastro`.

No momento do primeiro registro, o workflow havia passado pelos testes gerais, download com hashes dos insumos privados e preparação da entrada estadual; o build SP645 seguia em processamento. **Não registrar como aprovada até conclusão do job.** A candidata destina-se ao subdomínio isolado `https://sp645-rmrp-cadastro.finbra-tic-tim-referencia.pages.dev/`; verificar Cloudflare e job antes de declarar a URL disponível.

## Gates para produção

1. Todos os passos da candidata devem concluir com sucesso, inclusive QA estadual local/remoto e API v2.
2. Conferir que nenhum campo monetário novo nem localização física candidata foi incorporado.
3. Examinar o comportamento em navegador desktop/mobile e a navegação e persistência da interface estadual existente.
4. Preparar uma release **formal e isolada**, compatível com o workflow de produção SP645; não confundir aprovação de candidata com autorização automática de deploy.
5. Implantar somente depois dos gates e registrar URL, SHA e QA de produção. A release v0.4.0 permanece como rollback.

**Estado:** alteração de código e disparo da candidata confirmados. `public_release_authorized=false` permanece para investimentos financeiros não homologados.
