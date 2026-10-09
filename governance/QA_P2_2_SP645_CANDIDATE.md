# QA P2.2 — candidata SP645

Data de referência: 2026-10-09.

Manifesto: `data/catalogs/sp645_candidate_2026_10_09.yml`.

## Integridade

- [x] esquema válido;
- [x] chaves municipais válidas;
- [x] anos esperados presentes;
- [x] duplicidades críticas ausentes;
- [x] ausência não convertida em zero;
- [x] cobertura registrada.

Evidências: Core CI, Gate F, 645 municípios, 271 linhas de cobertura, zero ausências implícitas criadas pelo refresh.

## Metodologia

- [x] variáveis com definição e unidade;
- [x] indicadores com fórmula e componentes;
- [x] indicadores legais usam demonstrativos próprios;
- [x] crosswalk temporal documentado;
- [x] alterações metodológicas versionadas.

## Paridade

- [x] resultados reconciliados com TIC_TIM_30;
- [x] divergências explicadas;
- [x] SHA-256 registrado.

Paridade: 30/30 municípios; cinco diferenças CAPAG classificadas como revisão oficial; zero regressões.

## Funcional

- [x] F101–F118 auditados;
- [x] mapa funcional;
- [x] séries funcionais;
- [x] exportação funcional;
- [x] fontes e metodologia acessíveis.

F116 foi saneado pela issue #110 e PR #111. Core CI e Pages Preview ficaram verdes.

## Segurança e implantação

- [x] política de segredos documentada;
- [x] configuração de produção fora do repositório;
- [x] ambiente local reproduzível sem Cloudflare;
- [x] `deployment/wrangler.example.toml` presente;
- [x] rollback documentado em `deployment/ROLLBACK.md`.

## Decisão P2.2

O checklist técnico-documental está atendido. Esta aprovação não publica a candidata estadual.

A próxima etapa é P2.3: decisão explícita de promoção ou manutenção como candidata privada.
