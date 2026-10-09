# Finanças Municipais SP v0.3.1

release_universe: SP_645

Patch operacional da release multiuniverso `v0.3.0`.

## Alteração

O QA remoto passa a tolerar a janela de propagação do Cloudflare Pages quando uma URL retorna HTTP 200 antes de o conteúdo JSON correto estar disponível no endpoint principal.

A validação repete a leitura e a decodificação JSON antes de declarar falha.

## Escopo

Não há alteração nos dados, nos 13 universos, nas regras analíticas, nas tipologias, nos marcadores, nos pares ou na interface do painel.

Permanecem:

- SP_645 como universo padrão;
- TIC_TIM_30;
- CIDADES_MEDIAS;
- 9 regiões metropolitanas;
- AU_FRANCA;
- recálculo das estatísticas relativas por universo.

## Evidência

A produção `v0.3.0` foi efetivamente publicada, e a verificação direta posterior confirmou `/data/universes.json`, `CIDADES_MEDIAS` e o seletor de recorte. O falso negativo ocorreu apenas na leitura imediata do endpoint principal após o deploy.

A `v0.3.1` corrige esse comportamento do QA antes de uma nova promoção controlada.
