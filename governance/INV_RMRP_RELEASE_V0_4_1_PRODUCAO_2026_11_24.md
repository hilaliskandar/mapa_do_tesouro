# Publicação de produção SP645 v0.4.1 — catálogo territorial RMRP

**Data:** 24/11/2026. **Resultado:** release publicada e QA de produção aprovado.

## Endereços oficiais

- Plataforma pública: **https://finbra-tic-tim-referencia.pages.dev/**
- Página nova: **https://finbra-tic-tim-referencia.pages.dev/territorio-rmrp-validado.html**
- Dados cadastrais JSON: **https://finbra-tic-tim-referencia.pages.dev/data/api/v3/investimentos/rmrp/territorio-validado.json**

## Cadeia de proveniência

1. [PR nº 234](https://github.com/hilaliskandar/mapa_do_tesouro/pull/234) partiu de `main` e incorporou exclusivamente os componentes cadastrais RMRP, com alterações de pipeline opt-in e testes; squash-merge na `main`, SHA **`4c44ed21effd3c884e2cbd308fdef84ca1ef2344`**.
2. [QA final da candidata estadual 45295117443](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45295117443): **success**, incluindo `RMRP_BROWSER_QA_PASS` em Chromium desktop 1280×800 e celular 375×812, 34 municípios, filtro de Batatais com sete municípios, busca nominal, integração com a página inicial, API v2, QA estadual SP645 local/remoto.
3. [GitHub Release v0.4.1](https://github.com/hilaliskandar/mapa_do_tesouro/releases/tag/v0.4.1) criada com `release_universe: SP_645`, apontando para o commit aprovado.
4. Workflow [SP645 Pages Production 45395727209](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/45395727209) disparado na `main` com `release_tag=v0.4.1` e `include_rmrp_territory=true`: **concluído com sucesso**. Passaram a leitura da release, testes gerais, verificação dos insumos canônicos privados com hash, build da base estadual SP645, overlay somente cadastral, QA local, upload do artefato de produção, deploy e verificações remotas `qa_sp645_pages.py` e `materialize_rmrp_territorial_sp645.py --url`.
5. Cloudflare Pages, projeto `finbra-tic-tim-referencia`, implantação **production**, URL de deploy imutável **https://4e8542e2.finbra-tic-tim-referencia.pages.dev**, commit **`4c44ed21effd3c884e2cbd308fdef84ca1ef2344`**, estágio **success**, criada em 24/11/2026 às 12:41:41 UTC.

## Limites de conteúdo e interpretação

O novo catálogo registra **34 municípios**, 4 sub-regiões com cardinalidades **15, 6, 6, 7**. O JSON contém apenas `codigo_ibge`, `municipio` e `sub_regiao` para cada município. A consulta é cadastral: **não comprova execução de obra, não localiza fisicamente investimentos e não contém valores pagos**.

O build da produção preservou a arquitetura e testes do universo SP645 (645 municípios), API v1/v2, indicadores e cartografia. As camadas de SIAFEM, Transferegov e Obrasgov sob QA permanecem fora do cálculo público de investimentos executados.

A release anterior **v0.4.0** continua referência para rollback. O workflow `pages-sp645-production.yml` exige release formal e o parâmetro opt-in `include_rmrp_territory`, default `false`. Não confundir o sucesso de cadastro com homologação dos registros financeiros: **`public_release_authorized=false` permanece aplicável às séries monetárias ainda em revisão**.

## Continuidades

- A revisão cadastral da RMRP está encerrada **para os componentes publicados na v0.4.1**.
- Para futuras atualizações, adicionar somente bases com QA rastreável, identificando fonte, tipo de evento financeiro, competência, localização e status de homologação.
- A coleta SIAFEM/SP fora da RMRP em 2025 retoma do **checkpoint 525/611**, com 445 consultas reconciliadas, 80 inconclusivas e 86 ainda não consultadas. Próxima janela `offset=525, limit=5, year=2025`, verificando idempotência.
