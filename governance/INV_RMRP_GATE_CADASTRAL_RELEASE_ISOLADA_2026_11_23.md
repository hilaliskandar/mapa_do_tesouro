# Candidata de release isolada — cadastro territorial RMRP

**Data:** 23/11/2026. **Estado:** branch isolada derivada de `main`, ainda não mesclada nem implantada em produção.

## Por que a branch foi isolada

A PR 233 de investimentos reúne trabalho exploratório, dados de pagamentos não homologados e prévias cadastrais. Publicar diretamente essa branch implicaria risco de incorporar indevidamente artefatos financeiros. A candidata `release-rmrp-cadastro-sp645-20261123` parte da `main` e limita a alteração aos seguintes componentes:

1. `app/static/territorio-rmrp-validado.html`: página de consulta aos 34 municípios da RMRP, com advertência explícita sobre a ausência de comprovação de execução financeira ou física.
2. `app/static/data/api/v3/investimentos/rmrp/territorio-validado.json`: cadastro com somente `codigo_ibge`, `municipio`, `sub_regiao`.
3. `governance/controls/rmrp_cadastro_ibge34_2026_11_23.csv`: crosswalk de 34 linhas sem campos monetários.
4. `deployment/materialize_rmrp_territorial_sp645.py`: overlay e QA estrito do cadastro, comparando JSON contra CSV, verificando totalizadores, campos e aviso HTML.
5. `.github/workflows/pages-sp645-candidate.yml`: opt-in manual `include_rmrp_territory`, por padrão `false`, com QA local e remoto após o build estadual.
6. `.github/workflows/pages-sp645-production.yml`: opt-in manual `include_rmrp_territory`, por padrão `false`, com QA do catálogo antes/depois do deploy da **release formal**.
7. `README.md`: endereço público fixado no alto.

O único dado novo destinado ao frontend é **cadastral**. A API v1, API v2, FINBRA/DCA, RREO, RGF, CAPAG, índices, valores e cartografia estadual permanecem gerados pelo mesmo pipeline SP645 de produção a partir dos inputs R2 com hashes controlados.

## Evidência de ensaio na branch de desenvolvimento

[Workflow 45285817646](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45285817646), branch `investimentos-territoriais-sp645-20261111`, alias `sp645-rmrp-cadastro`, concluiu **success**: testes gerais, download e readback dos insumos estaduais, build SP645, overlay territorial, QA estadual local, QA API v2 local, deploy privado da candidata, QA HTTP estadual, QA cadastral remoto e QA remoto de ausência de fallback HTML em JSON API v2.

Candidata técnica: https://sp645-rmrp-cadastro.finbra-tic-tim-referencia.pages.dev/territorio-rmrp-validado.html

**Importante:** o resultado da branch de desenvolvimento não dispensa o teste de candidata após o isolamento a partir da `main`. Não há release formal nova nem deploy em `main`/Cloudflare Pages produção.

## Gate pendente

- Executar `pages-sp645-candidate.yml` **na branch isolada**, com `include_rmrp_territory=true` e alias exclusivo; exigir QA remoto integral, sem perda de API v1/v2 e das 13 dimensões analíticas.
- Executar navegação desktop/mobile sobre o site estadual e a nova página, especialmente a lista de 34 municípios e os quatro filtros territoriais.
- Analisar a PR isolada, rever os arquivos alterados e aprovar incorporação à `main`.
- Somente após esses aceites, criar tag/release formal com `release_universe: SP_645` e acionar `pages-sp645-production.yml` com `include_rmrp_territory=true`, seguido de QA pós-publicação.
- Preservar o rollback v0.4.0; **não** liberar os valores de SIAFEM, Transferegov e Obrasgov como investimentos executados.

**Estado:** preparada para QA e revisão, `public_release_authorized=false` para novas medidas monetárias.


## Resultado do gate na branch isolada

- [GitHub Actions 45286673670](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45286673670): **job concluído com success**, em ref `release-rmrp-cadastro-sp645-20261123`, entrada `include_rmrp_territory=true`, alias `sp645-rmrp-release`.
- Passaram testes gerais, hashes e download de insumos estaduais privados, build do SP645, overlay cadastral, `qa_sp645_pages.py` local e remoto, `qa_api_v2.py` local, `qa_remote_sp645_v2_json.py` remoto e validação HTTPS do catálogo territorial, além do deploy isolado.
- [Cloudflare Pages, prévia isolada](https://sp645-rmrp-release.finbra-tic-tim-referencia.pages.dev/territorio-rmrp-validado.html): deploy `bec2619e`, ambiente `preview`, estágio `success`; SHA da candidata `7ed1976baeb9a3408c4f828702cac642f6d2465b`.
- O teste adicional de navegador externo **não foi executado**, porque a conexão Browserless retornou HTTP 401 por esgotamento da cota do plano. Não declarar aprovação visual/responsiva independente.
- [PR 234](https://github.com/hilaliskandar/mapa_do_tesouro/pull/234) aberta como **draft**; nenhum merge, tag/release formal ou deploy de produção foi realizado. A produção continua `v0.4.0`.

**Gate restante:** inspeção funcional de navegação/responsividade e revisão da PR isolada; após aceite, promoção por release SP645 formal e execução manual do workflow com `include_rmrp_territory=true`. Bloqueio monetário permanece.
