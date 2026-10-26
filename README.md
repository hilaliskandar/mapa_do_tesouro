# Finanças Municipais SP

**Guia canônico da RMJ:** [documentação operacional, metodologia, evidências e publicação](editorial/rmj/README.md). O boletim da RMJ é publicado separadamente em https://financas-rmj.pages.dev/; não se confunde com o portal estadual.

Plataforma auditável para ingestão, harmonização, análise e visualização territorial de finanças municipais, com base principal no FINBRA/Siconfi e integração progressiva de DCA, RREO, RGF, CAPAG, população e demais fontes oficiais.

O repositório nasceu do projeto `mapa_do_tesouro`, cuja metodologia e rotinas históricas permanecem como ancestral do núcleo atual. A arquitetura vigente, porém, separa dados, regras analíticas, documentação, build estático e publicação.

## Estado canônico

A produção pública vigente é a release `v0.4.0`, com:

- universo estadual `SP_645` como padrão;
- 13 universos analíticos sobrepostos no painel;
- API editorial estática v1;
- 11 universos editoriais para boletins fiscais;
- 287 contextos município × universo;
- RMSP editorial com 38 municípios, excluindo a capital;
- Cidades Médias com 33 municípios, inclusive as sobreposições com RM/AU;
- frontend e API publicados no Cloudflare Pages;
- QA automatizado local e remoto.

O baseline `TIC_TIM_30` permanece preservado como referência histórica de regressão e rollback.

## Arquitetura atual

```text
fontes oficiais / snapshots aprovados
            ↓
        ingestão
            ↓
 normalização + harmonização
            ↓
       proveniência
            ↓
     SQLite canônico
            ↓
 agregações / indicadores
            ↓
 estatísticas / tipologias / pares
            ↓
       QA e hashes
            ↓
      JSON static-first
            ↓
      frontend estático
            ↓
 Cloudflare Pages / CDN
```

Consultas dinâmicas e D1 permanecem opcionais. A API editorial v1 é formada por JSONs estáticos publicados no mesmo build e não introduz servidor de API em runtime.

## Universos

### TIC_TIM_30

É o baseline de regressão e o universo atualmente publicado. Qualquer expansão deve preservar sua paridade ou explicar formalmente as divergências.

### SP_645

É o universo estadual em preparação. A prova de escala já valida 645 municípios, mas a primeira release estadual exige cobertura multifuentes compatível com o contrato conceitual do baseline.

## Princípios obrigatórios

- ausência nunca é zero;
- dados oficiais, agregações analíticas, indicadores derivados, indicadores legais e classificações oficiais são objetos distintos;
- indicadores legais usam seus demonstrativos próprios;
- mudanças de código, estágio ou fonte devem permanecer visíveis no crosswalk;
- conta-pai e conta-filha não podem ser somadas sem regra de hierarquia;
- valores, status e proveniência são versionados;
- ranking e pares são instrumentos comparativos, não avaliação normativa;
- uma funcionalidade aprovada não pode desaparecer silenciosamente de uma versão futura;
- artefatos publicados devem ser relacionáveis ao build por SHA-256.

## Regra territorial

`despesa_territorial` usa a regra canônica `strict_complete`:

```text
Urbanismo
+ Habitação
+ Saneamento
+ Gestão Ambiental
+ Transporte
```

O agregado só é observado quando os cinco componentes estão observados. Caso contrário, permanece `NA`. A regra histórica parcial é preservada apenas para regressão.

## Fontes fiscais

- Siconfi/FINBRA — DCA;
- RREO — inclusive RCL quando aplicável;
- RGF Anexo 01 — Despesa Total com Pessoal;
- RGF Anexo 02 — dívida;
- RGF Anexo 05 — disponibilidade de caixa e restos a pagar;
- Tesouro Transparente — CAPAG;
- IBGE — população e demais denominadores quando incorporados.

A documentação detalhada está em `governance/SOURCES.md`.

## Aquisição direta Siconfi

O repositório já possui aquisição direta para DCA e clientes para demonstrativos legais. A expansão estadual deve usar essa rota preferencialmente a planilhas intermediárias quando houver equivalência semântica validada.

O smoke estadual DCA valida:

- lista de 645 municípios;
- anexos I-C, I-D e I-E;
- armazenamento de artefatos brutos;
- normalização;
- hashes;
- manifestos;
- retries para falhas transitórias.

Também existe crosscheck direto entre Siconfi e o baseline publicado para municípios sentinela.

## Snapshot privado estadual

O piloto estadual atual está em objeto privado versionado no R2. O GitHub conserva apenas contrato, manifesto, hashes, código e testes.

Escopo validado:

- 645 municípios;
- 2020–2023;
- 2.580 município-ano;
- receita corrente;
- receita tributária;
- IPTU;
- ITBI;
- ISS;
- 12.900 observações;
- 12.900 registros de proveniência.

Despesas, população fixa de 2024, RREO, RGF e CAPAG são deliberadamente excluídos desse piloto por incompatibilidade ou ausência de contrato estadual aprovado.

## Documentação canônica

Para retomar o projeto em nova conversa ou ambiente, consultar nesta ordem:

1. `governance/PROJECT_STATE.md` — estado operacional e próximo gate;
2. `governance/INVENTORY.md` — inventário do que existe e do que é legado;
3. `governance/ARCHITECTURE.md` — arquitetura vigente;
4. `governance/METHODOLOGY.md` — princípios metodológicos;
5. `governance/DATA_MODEL.md` — modelo de dados e proveniência;
6. `governance/EXPANSAO_SP_645.md` — expansão estadual;
7. `governance/QA_CHECKLIST.md` — gates de promoção;
8. `CHANGELOG.md` — histórico de versões.

## Estrutura principal

```text
governance/          documentação, decisões e QA
pipeline/
  acquire/           aquisição das fontes
  ingest/            ingestão para o núcleo
  normalize/         normalização
  accounting/        regras contábeis
  harmonization/     harmonização temporal
  aggregations/      agregações
  indicators/        indicadores
  build/             SQLite, JSON e site
data/
  schema/            migrations
  catalogs/          catálogos e contratos
  mappings/          mappings de fontes
  snapshots/         manifestos versionados
app/                 frontend estático
deployment/          publicação e acesso a snapshots privados
tests/               regressão, metodologia, dados e frontend
reference/           material legado e de referência
```

## Publicação

Produção:

`https://finbra-tic-tim-referencia.pages.dev`

Preview estável:

`https://preview.finbra-tic-tim-referencia.pages.dev`

O deployment é separado do rebuild dos dados. Alterações de interface podem ser promovidas sem reconstruir a base; atualizações de dados exigem pipeline, QA, hash e nova versão de dados.

## Próximo gate

A infraestrutura estadual, multiuniverso e a API editorial v1 estão em produção. O próximo ciclo é editorial: validar os templates de publicação com um caderno-piloto, congelar regras de narrativa e preparar a primeira Edição de Referência dos 11 universos.

A fila administrativa está limpa em 2026-10-09: zero issues abertas e zero pull requests abertos. As pendências operacionais estão consolidadas em `governance/PENDING_TASKS.md`.

## Legado

As rotinas antigas de Streamlit, hierarquia, mapa semântico, normalização e agregações continuam úteis como referência metodológica e de regressão, mas não definem sozinhas a arquitetura de produção atual.

## ATENÇÃO — retomada da frente editorial RM/AU (18/10/2026)

O bloco anterior sobre v0.4.0 documenta a infraestrutura inicial e **não** resume os desenvolvimentos editoriais posteriores. Antes de iniciar novo cálculo, coleta, API, gerador ou boletim, ler obrigatoriamente [Continuidade operacional RM/AU](governance/CONTINUIDADE_OPERACIONAL_RM_AU_2026_10_18.md), [estado](governance/PROJECT_STATE.md), [inventário](governance/INVENTORY.md) e [pendências](governance/PENDING_TASKS.md). O portal estadual e o boletim independente [RMJ](https://financas-rmj.pages.dev/) são publicações distintas. Não presumir que PRs, catálogos ou candidatos estejam implantados sem teste do pacote público.


## TCESP — continuidade da integração fiscal (25/10/2026)

**Estado comprovado:** os dados TCESP já extraídos da RMRP e de São Carlos estão preservados no bucket privado R2 `financas-municipais-sp-canonico`, sem alteração da API ou do painel público. As operações de upload, manifesto e recuperação com verificação SHA-256 foram concluídas nos workflows abaixo. Os arquivos do GitHub Actions são temporários (retenção 30 dias); usar prioritariamente o R2 para novas análises.

| Acervo | Conteúdo | Chave de armazenamento no R2 | Workflow de persistência |
|---|---|---|---|
| RMRP histórico | 102 extratos de investimentos liquidados, 34 municípios × 2023–2025 | `tcesp/rmrp/2023_2025/run_39203495737/` | [run 40230628954](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40230628954) |
| RMRP 2026 | 68 extratos (34 receitas e 34 despesas), exercício parcial | `tcesp/rmrp/2026/run_40229219185/` | [run 40230188884](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40230188884) |
| São Carlos | 16 arquivos de extração/auditoria, 2023–2026, quatro tipos de documento | `tcesp/sao-carlos/2023_2026/acervo_20261025/` | [run 40231520362](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40231520362) |

**Cautelas:** os 186 arquivos não são observações homogêneas. RMRP 2023–2025 representa apenas investimentos liquidados, e RMRP 2026 abrange receitas e movimentações de despesas; São Carlos contém documentos de detalhamento e auditoria. Em 2026, as despesas da RMRP apresentam janeiro–agosto e as receitas, janeiro–agosto em 33 municípios e janeiro–maio em Jardinópolis. A ausência de registros não é zero. Persistência em R2 não equivale a ingestão SQLite ou publicação.

**Qualidade e divergências:** na RMRP 2023–2025, 101/102 pares município–ano conciliaram exatamente investimentos TCESP/DCA; Guatapará 2023 difere R$ 10.176,00. São Carlos 2024 apresenta divergência de aproximadamente R$ 3,16 milhões entre TCESP e DCA em investimentos liquidados. Não corrigir esses valores sem exame das fontes.

**Inventário estadual:** [run 40231222578](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40231222578) construiu a matriz de cobertura 645 municípios × 2023–2026 × receitas/despesas, a partir dos manifestos R2 e do catálogo DCA, sem consultar o TCESP. A matriz precisa ser atualizada para reconhecer São Carlos como persistido. A categoria `cobertura_a_verificar` significa ausência de comprovação no acervo inventariado, não ausência na fonte original.

**Outros acervos:** workflows legados `.github/workflows/rmj-tcesp-2025-backfill.yml` e `.github/workflows/tictim-tcesp-complemento-23.yml` existem, mas sua preservação atual e completude não foram comprovadas. Verificar os runs e artefatos antes de recolher ou marcar como persistidos.

**Próximos passos:** (1) inventariar RMJ/TIC-TIM e acervos remanescentes, (2) atualizar a matriz de cobertura com São Carlos, (3) definir fila `missing-only` por código IBGE/ano/domínio, com atualização temporal controlada para 2026, (4) integrar camada TCESP complementar em SQLite/API sob QA e testes de regressão, sem sobrescrever DCA/FINBRA. Documentação detalhada: [plano de integração](governance/PLANO_INCREMENTAL_TCESP_SP645_20261025.md), [inventário fiscal São Carlos](editorial/sao_carlos/README_fiscal.md) e [guia do runner](editorial/rmrp/README_RUNNER_WSL2_TCESP.md).

## Continuidade operacional — TCESP 2023–2025, SP645 e API v2

**Atualização: 26/10/2026.** Esta seção é o ponto de retomada da integração complementar dos investimentos municipais TCESP, em conjunto com [homologação detalhada](governance/HOMOLOGACAO_TCESP_R2_SQLITE_API_V2_20261026.md). Manter este README atualizado após novas verificações, correções ou publicações, indicando o último run homologado e as pendências ainda abertas.

**Dados e persistência.** Auditoria integral de despesas estaduais TCESP para os 644 municípios sob jurisdição do Tribunal, exercícios 2023, 2024 e 2025; São Paulo capital não deve ser tratada como dado zero. QA dos anos 2023/24: run `40263996213`; 2025: `40262193781`. Agregados por município/mês/estágio, programa e ação persistidos no R2 privado, prefixos `tcesp/estadual/despesas/{ano}/run_{run}/`. A preservação dos CSVs não inclui o ZIP bruto de todas as despesas.

**Camada complementar.** Schema `data/schema/006_tcesp_investimentos.sql`, importador `pipeline/build/import_tcesp_investimentos.py`, exportação `pipeline/build/export_tcesp_investimentos_api_v2.py`, interface `app/static/tcesp-investimentos.html` e `app/static/tcesp-investimentos.js`. Integração opt-in `deployment/stage_tcesp_api_v2.py` e validação de 1.932 arquivos municipais/ano. Run de regressão sobre cópia do acervo fiscal real `40322855496` **success**, navegador Chromium com sete cenários e nenhum erro JavaScript não tratado. **Não houve deploy público dessa camada.**

**API v2 estadual pré-existente.** O artefato privado `sp645-private-site-40317752109`, do run `40317752109`, foi auditado no run `40326152205`: `deployment/qa_api_v2.py` aprovado, 645 municípios, 174.795 observações, 75 variáveis. **Esse resultado NÃO significa que esteja implantado externamente.** Workflow responsável pela prévia estadual: `.github/workflows/pages-sp645-candidate.yml`, com alias padrão `sp645-candidate`; o workflow de prévia fiscal anterior é `.github/workflows/pages-preview.yml`.

**Diagnóstico externo atualizado.** A sondagem somente leitura `40327538489` examinou `preview.finbra-tic-tim-referencia.pages.dev` e `sp645-candidate.finbra-tic-tim-referencia.pages.dev`. Nos dois endereços, `/data/manifest.json` respondeu HTTP 200 com JSON; `/data/api/v2/manifest.json` e `/data/api/v2/catalog/municipalities.json` responderam HTTP 200 com **`text/html`**, não JSON. Portanto **nenhum desses aliases teve API v2 remota homologada**. Hipóteses a testar: ausência do artefato v2 no deploy apontado pelo alias ou fallback de roteamento HTML; não assumir qual delas é correta sem inspeção de deployment e rotas.

**Próximo procedimento, em ordem.** (1) Verificar no Cloudflare Pages quais deployments e commits atendem a `preview` e `sp645-candidate` e suas regras de roteamento; (2) preparar nova implantação **somente de prévia isolada** a partir do artefato SP645 homologado, com URL diferenciada e rollback, se cabível; (3) antes de aprovar, exigir HTTP 200, `Content-Type` JSON, análise JSON válida, contrato `645` municípios e QA da API v2; (4) em seguida repetir regressão integrada TCESP sobre a prévia estadual; (5) elaborar e auditar conciliação contábil TCESP × DCA por exercício e município, sem pressupor igualdade conceitual; (6) produção somente em fluxo explícito, após evidências e aprovação.

**Regra de segurança:** não alterar a base canônica DCA/FINBRA, não converter ausência de registro em zero e não confundir QA local, persistência em R2 ou resposta HTTP 200 em HTML com publicação homologada.

**Verificação adicional da Cloudflare Pages em 26/10/2026.** A API de gerenciamento da Cloudflare confirmou a existência do projeto `finbra-tic-tim-referencia` e retornou deployments recentes da categoria `preview`, principalmente branches `pr-*`, com estado `success`. Esta leitura do histórico recente **não demonstrou implantação SP645** no alias `sp645-candidate`; não confundir sucesso de deploys `pr-*` com publicação da API estadual. O workflow de publicação estadual isolada existe e foi identificado, mas seu acionamento/deploy efetivo permanece a comprovar. Prosseguir conferindo o histórico filtrado por branch/alias e só então decidir eventual nova publicação de prévia isolada.

## Inventário conclusivo de deployments Cloudflare Pages — 26/10/2026
- Consulta **somente leitura** ao endpoint de administração Cloudflare Pages do projeto `finbra-tic-tim-referencia`, varrendo as 25 páginas de 20 deployments (492 registros no total). A conta confirmou o alias isolado `sp645-candidate` em **09/10/2026 10:20:44 UTC**, deployment `cfbac01c-d9f6-4a43-a672-c203b85bff37`, branch `sp645-candidate`, commit `9c381a86b41bce6eb3fad07aa8d0cf7a0ab56a4a`, status `success`.
- Também houve deployments anteriores `sp645-candidate` em 09/10/2026 09:02 UTC (`ac88c1ec-f43c-4f41-93c7-c3c8b052a7b8`) e 08:58 UTC (`7b6519de-ccde-4625-bd88-e174e3c28b79`). Nenhum deployment dessa branch posterior a 09/10 foi encontrado no histórico retornado.
- Alias `preview`: último deployment localizado em **07/10/2026 16:17 UTC**, ID `d3c41b36-a042-44c4-a6e6-3acf34f5c412`; implantação `main` mais recente localizada em **09/10/2026 10:26 UTC**, ID `bfa41be5-1eb3-4fcb-827a-fbe9ca3e6ce4`. Os demais deploys recentes na conta são principalmente branches `pr-*`.
- O artefato SP645 privado homologado (`run 40317752109`, 26/10/2026; QA `40326152205`) **é posterior ao último deploy conhecido do alias estadual**. Assim, a ausência de JSON da API v2 em `sp645-candidate` é consistente com uma implantação antiga; a inspeção de deployments não demonstra por si só se existia fallback HTML naquela versão.
- **Próximo passo autorizado tecnicamente, ainda não executado:** preparar e homologar um novo deployment de **prévia isolada**, com nome de branch específico e verificações externas de JSON e regressão, sem alterar `main`, `preview` ou `sp645-candidate` até a aprovação da versão substituta. Não foi feito deploy nesta diligência.

**Bloqueio automático na futura prévia SP645.** O módulo `deployment/qa_remote_sp645_v2_json.py` (commit `453d9abe`) testa a entrega externa de `/data/api/v2/manifest.json` e dos catálogos de municípios e variáveis, recusando resposta HTML mesmo com HTTP 200; exige MIME JSON, análise JSON válida e invariantes de 645 municípios e 75 variáveis. O workflow `.github/workflows/pages-sp645-candidate.yml` agora o executa **após** uma eventual implantação isolada (commit `849509bf`) e arquiva o relatório. Isto reforça a validação de implantações futuras; **não dispara, por si, nenhuma publicação**.

## Homologação externa de prévia SP645 — 26/10/2026
- **Concluída:** workflow `.github/workflows/sp645-isolated-v2-validation.yml`, [run 40329504327](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40329504327), resultado `success`.
- A execução recuperou o artefato estadual auditado `sp645-private-site-40317752109` da execução `40317752109`, verificou localmente os contratos de páginas e API v2 e publicou **somente a prévia isolada** `sp645-v2-qa-20261026` no projeto Cloudflare Pages existente.
- Endereço de homologação externa: `https://sp645-v2-qa-20261026.finbra-tic-tim-referencia.pages.dev`. O workflow aprovou `deployment/qa_remote_sp645_v2_json.py` para três endpoints JSON (`manifest.json`, catálogo de municípios e variáveis), exigindo `Content-Type` JSON, análise válida e invariantes 645 municípios/75 variáveis; `deployment/qa_sp645_pages.py` externo também aprovado. A validação não equivale a implantação de produção.
- **O bloqueio da API v2 remota foi resolvido nesta nova prévia**, sem reescrever os aliases antigos `preview` ou `sp645-candidate` e sem alterar `main`. Os antigos aliases permanecem registrados como não homologados para API v2.
- **Ainda pendentes:** incorporar a camada complementar de investimentos TCESP 2023–2025 na prévia estadual validada; repetir QA dos 1.932 detalhes e interface no endereço externo; conciliar formalmente TCESP × DCA/FINBRA; decidir promoção por fluxo de produção explícito somente após homologação completa.

## Prévia integrada SP645 + TCESP — 26/10/2026
- Workflow `.github/workflows/sp645-tcesp-integrated-preview.yml`, execução [40330429300](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40330429300), construiu camada TCESP a partir dos artefatos auditados 2023–2025, integrou-a ao artefato estadual SP645 previamente validado e executou **deploy somente no alias isolado** `sp645-tcesp-qa-20261026`, sem alterar `main`, `preview`, `sp645-candidate` ou o alias da prévia fiscal v2.
- URL: `https://sp645-tcesp-qa-20261026.finbra-tic-tim-referencia.pages.dev`; deployment Cloudflare ID `47141558-ef64-4bb0-97f8-9350e147f952`, estado `success` em 26/10/2026. A execução integrada teve **conclusão global `failure`** porque a primeira consulta aos novos endpoints TCESP retornou HTTP 403 logo após o deploy; as verificações anteriores, inclusive a API fiscal v2 remota, passaram.
- Uma diligência posterior, [40330751722](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40330751722), `success`, sondou o alias de branch e a URL imutável do deployment. Nos dois endereços, retornaram HTTP 200 com MIME JSON válido por assinatura inicial: `/data/api/v2/manifest.json`, `/data/api/v2/tcesp/manifest.json`, `/data/api/v2/tcesp/2025/municipios.json` e detalhe `/data/api/v2/tcesp/2025/municipios/3525904.json`. HTML e JS de consulta de investimentos também retornaram 200 com tipos adequados. Evidência: artefato `integrated-tcesp-remote-probe`, ID `12653093577`.
- **Interpretar corretamente:** implantação da prévia realizada e acessibilidade dos endpoints confirmada posteriormente; a execução integral de deploy **não** ficou aprovada, e o teste posterior foi uma sondagem HTTP/MIME, não a auditoria funcional integral em navegador externo. É necessário repetir as verificações de contrato JSON (conteúdo, totais, exercícios), testes de navegação e estabilidade sem novo deploy antes de considerar esta prévia plenamente homologada.
- Próximas frentes: comparar investimentos TCESP × DCA com fonte e estágio harmonizados; corrigir o tratamento de possível indisponibilidade transitória imediatamente após publicação; homologar interface e API complementares no endereço externo. **Produção segue inalterada.**

**Validação funcional externa complementar, atualização 26/10/2026.** Workflow `validate-existing-tcesp-preview.yml`, run `40330923128`, encontrou HTTP 403 ao tentar analisar o conteúdo TCESP após a validação fiscal v2 externa. Trata-se de falha da consulta externa, **não** de evidência de erro dos dados importados. A sondagem independente `40330751722` havia confirmado HTTP 200/JSON nos mesmos endpoints, em alias e URL imutável. É necessário avaliar intermitência/bloqueio por origem, impor nova tentativa limitada e testar tanto a URL de branch quanto a imutável; não homologar prematuramente a experiência remota. O novo workflow não realizou deploy.

**Nova rodada de verificação externa sem redeploy:** workflow `.github/workflows/validate-existing-tcesp-preview.yml` foi ajustado para usar a URL imutável do deployment `47141558.finbra-tic-tim-referencia.pages.dev` e retentativas limitadas nos HTTP 403/429/502/503. Na execução `40331065453` passaram as verificações externas da API fiscal SP645 e dos arquivos de conteúdo TCESP de **2023, 2024 e 2025**; o ensaio de navegador Chromium estava em andamento no último exame. Só registrar aprovação integral após resultado terminal `success`. Nenhuma alteração adicional em implantação/produção.

## Conciliação auditada RMRP TCESP × DCA — registro de continuidade 26/10/2026
- Documento metodológico e de resultados: [`governance/CONCILIACAO_INVESTIMENTOS_TCESP_DCA_RMRP_2023_2025.md`](governance/CONCILIACAO_INVESTIMENTOS_TCESP_DCA_RMRP_2023_2025.md), consolidado a partir da auditoria pré-existente [`editorial/rmrp/QA_TCESP_102_EXTRATOS_DCA_20261019.md`](editorial/rmrp/QA_TCESP_102_EXTRATOS_DCA_20261019.md), run `39203495737`.
- **Escopo exclusivamente RMRP:** 34 municípios × 2023–2025 = 102 confrontos. Investimentos liquidados TCESP grupo 44 versus `dca_investimentos_liquidada`: **101 pares exatos; uma exceção, Guatapará (3518859), 2023, R$ 10.176,00 TCESP acima da DCA**. Totais TCESP RMRP: 2023 R$ 484.958.575,24; 2024 R$ 500.824.152,06; 2025 R$ 302.301.895,18. Não atribuir causa à divergência sem documentos de origem.
- **Limite explícito:** a conciliação de 102 pares não permite atestar paridade para os 644 municípios TCESP ou 1.932 pares estaduais. Comparação estadual futura deve distinguir `concordante`, `divergente` e `nao_confrontavel`, preservando estágio, fonte e versão.
- Na execução de verificação externa `40331065453`, a validação fiscal SP645 e o conteúdo TCESP anual passaram; a etapa Chromium ainda não apresentava resultado terminal no exame realizado nesta atualização. Não declarar navegador externo aprovado antes da conclusão do run. Nenhum deploy adicional foi realizado nesta etapa.

## Matriz estadual de conciliação TCESP × DCA — 26/10/2026
- O teste de navegador externo da prévia integrada, run **40331065453**, alcançou conclusão **`success`**; as verificações da API fiscal e de TCESP para 2023–2025, incluindo Chromium, estão aprovadas nesse run. A implantação permanece somente no alias isolado, sem produção.
- Nova rotina reprodutível `pipeline/qa/conciliar_tcesp_dca_sp645.py`, workflow `.github/workflows/tcesp-dca-sp645-parity.yml`. **Run 40333583682** `success`: 645 municípios × 3 exercícios = 1.935 linhas; **633 concordantes, 10 divergentes e 1.292 não confrontáveis**, sempre em centavos inteiros e mantendo observações ausentes sem inventar zeros. Saídas: `conciliacao_tcesp_dca_sp645.csv` e `conciliacao_tcesp_dca_sp645.summary.json` no artefato do workflow.
- Dez divergências calculadas estão em **2025**, código IBGE e diferença TCESP menos DCA (R$): 3517901 +602.288,94; 3514908 +364.390,04; 3519501 +150.000,00; 3554300 +90.569,00; 3544004 +80.717,56; 3535309 +55.627,84; 3541208 −9.750,00; 3525805 +9.584,92; 3549904 −2.587,00; 3552304 −1.750,00. Esses desvios **não foram explicados por documentos de origem** e não autorizam substituir valores.
- **Limitação crítica:** a versão da API v2 DCA usada nesta execução não forneceu observações confrontáveis para 1.292 linhas; a matriz não prova concordância estadual integral. Não apagar a conciliação RMRP anterior (101/102 pares exatos, divergência Guatapará/2023 R$ 10.176,00, baseada em fonte externa com cobertura diferente). Examinar disponibilidade da DCA por ano e motivo e reexecutar com a série histórica completa.
- Documentação de resultados e ressalvas: [conciliação estadual preliminar](governance/CONCILIACAO_INVESTIMENTOS_TCESP_DCA_SP645_2023_2025.md). **Produção continua inalterada**.

## Auditoria estratificada da matriz estadual TCESP × DCA — 26/10/2026
- Recuperado o arquivo original `conciliacao_tcesp_dca_sp645.csv` do artefato `statewide-tcesp-dca-reconciliation` (ID `12656900180`), execução `40333583682`; auditado independentemente pelo script `auditar_matriz_sp645.py`, verificando 1.935 chaves únicas, presença de 645 municípios por exercício, classificação e igualdade aritmética em centavos.
- **Distribuição comprovada:** 2023: 645 não confrontáveis; 2024: 645 não confrontáveis; 2025: 633 concordantes, 10 divergentes e 2 não confrontáveis. No total, 1.292 não confrontáveis: **1.288 `status_nao_aplicavel`** (644 em 2023 e 644 em 2024), **3 `sem_cobertura_tcesp`** (capital paulista 3550308, uma ocorrência por ano) e **1 `status_ausente`** (3551207, exercício 2025).
- **Significado:** a API DCA estadual utilizada marcou investimentos liquidados de 2023 e 2024 como `nao_aplicavel`, impossibilitando **todos** os confrontos desses exercícios, ainda que haja auditoria regional independente com DCA histórica. O resultado de 633/643 = **98,44%** de concordâncias se aplica **somente aos pares confrontáveis de 2025**. Não inferir igualdade estadual em 2023–2024 nem ausência de informação na fonte DCA original a partir da situação desta versão do artefato.
- As dez diferenças de 2025 permanecem sem atribuição causal; a auditoria RMRP 2023–2025 com 101/102 pares iguais e exceção Guatapará/2023 permanece válida nos seus próprios limites de fontes e versões.
- **Próxima intervenção:** investigar por que a API SP645 catalogou a variável DCA de investimentos liquidados de 2023 e 2024 como `nao_aplicavel`; confrontar o mapeamento da variável, o esquema/crosswalk e o histórico completo da DCA. Reprocessar matriz com extração canônica auditada, sem sobrescrever dados TCESP, DCA ou promover a prévia à produção.
