# Gate cadastral RMRP — integração à prévia da plataforma

**Data de execução:** 23/11/2026. **Escopo:** exclusivamente cadastro territorial, sem valores financeiros ou pontos físicos de obras.

## Artefatos incorporados

- `app/static/data/api/v3/investimentos/rmrp/territorio-validado.json`: 34 municípios, códigos IBGE7 únicos, quatro sub-regiões legais com cardinalidades 15/6/6/7; campos municipais restritos a código, nome e sub-região.
- `app/static/territorio-rmrp-validado.html`: consulta navegável por nome/código e sub-região, com advertência explícita sobre não vinculação a execução financeira/física.
- `deployment/materialize_investimentos_preview.py`: overlay exclusivo da prévia PR 233 inclui os dois arquivos e recusa divergências de QA territorial.
- `deployment/qa_investimentos_preview.py`: testes locais e HTTP remoto conferem unicidade, campos permitidos, totalizações e compatibilidade IBGE7 com cadastros pré-existentes.

**Fonte do cadastro:** `governance/INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv`, com dimensão das sub-regiões ratificada no gate FED06B a partir da LC paulista 1.290/2016, art. 4º. Foram excluídos deliberadamente os valores preliminares do CSV de origem.

## Execução e comprovações

- Workflow GitHub Actions: [Pages Preview run 45283751255](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45283751255).
- Job **`build-deploy-qa` concluído com sucesso**, abrangendo materialização, QA local da aplicação, QA específico de investimentos e QA HTTP remoto.
- Implantação Cloudflare Pages PR 233: ID `d4e037d0` (prefixo URL), commit `2e3b83bb25a6e2347fc923456fc6ae742207b27c`, estágio `deploy=success`.
- Página no alias de prévia: **https://pr-233.finbra-tic-tim-referencia.pages.dev/territorio-rmrp-validado.html**.
- JSON no alias de prévia: **https://pr-233.finbra-tic-tim-referencia.pages.dev/data/api/v3/investimentos/rmrp/territorio-validado.json**.
- O job independente `rmj-browser-qa` foi **cancelado** durante a etapa de instalação do Chromium, com as etapas de navegação não executadas. Portanto, **não houve homologação visual/browser completa**. O QA local e remoto específico da camada de investimentos permaneceu aprovado no job `build-deploy-qa`.

## Gate público

O novo conteúdo está **integrado e verificado na prévia**, não no endereço principal de produção. A implantação de produção permanece na release `v0.4.0` (09/10/2026). A prévia PR 233 ainda é uma branch de desenvolvimento; a publicação pública demanda um candidato de release isolado, regressão de indicadores v1/TCESP/DCA e aprovação no fluxo `pages-production.yml`.

O código cadastral está pronto para composição da release; os dados financeiros SIAFEM/Transferegov/Obrasgov não foram promovidos nem considerados investimentos executados. `public_release_authorized=false` permanece para os indicadores que dependem de homologação.
