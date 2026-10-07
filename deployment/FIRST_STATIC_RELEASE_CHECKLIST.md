# Checklist da primeira publicação estática

## Build

- [ ] base canônica validada pelo hash esperado;
- [ ] pipeline completo sem erro;
- [ ] 30 municípios e 13 exercícios no universo inicial;
- [ ] 75 objetos documentados;
- [ ] 30 geometrias municipais;
- [ ] manifest sem divergência de hash;
- [ ] CI verde no commit publicado.

## Interface

- [ ] panorama abre sem erro;
- [ ] seleção de município funciona;
- [ ] seleção de ano funciona;
- [ ] séries históricas carregam;
- [ ] comparação anual carrega;
- [ ] mapa responde à troca de variável;
- [ ] análises temáticas carregam;
- [ ] fontes e cobertura carregam;
- [ ] crosswalk carrega;
- [ ] dicionário e metodologia carregam;
- [ ] “Como ler” abre para indicadores críticos.

## Indicadores sentinela

- Receita tributária / receita corrente;
- Investimentos / receita corrente;
- DTP / RCL;
- DC / RCL;
- DCL / RCL;
- Caixa após RPNP / RCL;
- CAPAG.

## Segurança

- [ ] `_headers` presente;
- [ ] nenhuma credencial na pasta publicada;
- [ ] nenhum `wrangler.toml` real versionado;
- [ ] nenhum endpoint administrativo no frontend;
- [ ] nenhuma dependência de `workers.dev`;
- [ ] domínio/rota de produção definidos apenas no ambiente privado.

## Cloudflare Pages

- [ ] projeto criado no workspace correto;
- [ ] primeira publicação feita como preview;
- [ ] preview inspecionado manualmente;
- [ ] produção promovida somente após aprovação;
- [ ] custom domain adicionado somente após validação;
- [ ] versão/data/hash do build registrados no changelog operacional privado.
