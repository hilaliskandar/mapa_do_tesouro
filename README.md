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

**Causa do recorte 2025 identificada no código-fonte:** `data/mappings/base_multifuentes_sp645_2025.yml` define para `dca_investimentos_liquidada` `availability_start: 2025` e `availability_end: 2025`. Isso explica a classificação `nao_aplicavel` na API SP645 para 2023 e 2024 **como recorte declarado no mapeamento do artefato**, sem provar inexistência de dados históricos na DCA original. **Não ampliar artificialmente o intervalo de disponibilidade** antes de incorporar e auditar a série DCA histórica de 2023/2024 com proveniência documentada. Priorizar ingestão histórica auditável e só depois revisão do crosswalk, reconstrução da API e reexecução da matriz.

## Segunda conciliação estadual com DCA histórica completa — 26/10/2026
- Recuperada do Drive a fonte canônica `DCA_SP_645_2013_2025_CANONICO.csv` (ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, modificada em 08/10/2026), SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`, já documentado na auditoria externa RMJ. O arquivo contém 645 linhas por ano de 2023, 2024 e 2025.
- Cruzamento local da DCA histórica com os valores TCESP em centavos da matriz original do run `40333583682` (não foi alterado o banco, o mapeamento temporal ou a produção): **2023: 618 concordantes, 26 divergentes, 1 sem cobertura TCESP; 2024: 625 concordantes, 19 divergentes, 1 sem cobertura TCESP; 2025: 633 concordantes, 10 divergentes, 1 sem cobertura TCESP e 1 sem observação DCA. Total: 1.876 concordâncias, 55 divergências e 4 não confrontáveis, sobre 1.935 linhas; 1.931 efetivamente confrontáveis.**
- **Controle cruzado:** Guatapará 2023 (IBGE 3518859) apresenta diferença TCESP − DCA de **R$ 10.176,00**, exatamente o valor documentado na auditoria regional anterior, corroborando o uso da série histórica.
- Maiores diferenças por módulo observadas: 3548807/2023 = −R$ 14.524.638,13; 3554102/2024 = +R$ 5.158.659,54; 3545209/2023 = −R$ 4.607.410,17; 3522158/2024 = −R$ 3.882.278,14; 3533254/2024 = −R$ 3.772.112,47. **Não atribuir causas, erros ou correções às fontes sem auditar documentos originais e revisão temporal.**
- Arquivos da execução local nesta conversa: `conciliacao_tcesp_dca_sp645_historica_2023_2025.csv` e `resumo_auditoria_historica.json`, preservando código IBGE, exercício, fontes em centavos e diferença. São evidências analíticas derivadas, não substituem o CSV DCA original nem os artefatos de origem TCESP.
- **Etapa seguinte:** conferir individualmente as 55 divergências, começando pelas diferenças monetárias maiores, cruzar retificações dos relatórios DCA/TCESP e integrar a série DCA histórica ao pipeline estadual apenas após revisão explícita de cobertura e proveniência. A API v2 que restringe `dca_investimentos_liquidada` a 2025 permanece intencionalmente inalterada, assim como a publicação pública.

## Priorização de divergências TCESP × DCA — 26/10/2026
- Conciliação histórica efetiva de 2023–2025: 1.935 combinações município–ano, 1.876 concordantes, 55 divergentes e quatro não confrontáveis. Fonte DCA canônica do Drive id `1BtXY_FxydMREEbMACJtaoW2n24ohVH33` e SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`. Fonte TCESP: matriz auditada `40333583682`. Não confundir com a API v2 recortada a 2025.
- **Materialidade:** soma dos valores absolutos das 55 diferenças **R$ 41.859.666,49**; saldo assinado TCESP menos DCA **−R$ 13.120.489,55**; dez maiores diferenças representam **90,2198%** da soma absoluta. Por exercício: 2023, 26 casos, soma absoluta R$ 21.685.604,42, saldo −R$ 17.957.596,40; 2024, 19 casos, soma absoluta R$ 18.806.796,77, saldo +R$ 3.498.015,55; 2025, dez casos, soma absoluta R$ 1.367.265,30, saldo +R$ 1.339.091,30. Há 51 municípios distintos com ao menos uma divergência.
- **Fila de exame:** P1 = dez maiores diferenças absolutas (90,22% da materialidade); P2 = posições 11–25; P3 = posições 26–55. Primeiros casos por código IBGE/ano/TCESP−DCA: 3548807/2023 −R$ 14.524.638,13; 3554102/2024 +R$ 5.158.659,54; 3545209/2023 −R$ 4.607.410,17; 3522158/2024 −R$ 3.882.278,14; 3533254/2024 −R$ 3.772.112,47. Confrontar documentos originais, estágio liquidado, grupo 44, atualização/retificação e escopo, sem corrigir valores por hipótese.
- Arquivos de trabalho verificados nesta sessão: `rmrp_auditoria/conciliacao_reprocessada/priorizacao_divergencias_tcesp_dca.csv` e `priorizacao_divergencias_resumo.json`; não presumir persistência desses arquivos no repositório ou R2. Produção inalterada.

## Conferência dirigida dos dez maiores desvios — 26/10/2026
- **Conferência independente da fonte DCA:** o arquivo `DCA_SP_645_2013_2025_CANONICO.csv`, Drive id `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5` foi reaberto e confrontado por código IBGE/ano com o ranking e a matriz histórica. Nos **dez maiores desvios**, o valor `dca_investimentos_liquidada` coincide exatamente com a matriz, após conversão decimal para centavos; todas as dez diferenças aritméticas TCESP−DCA foram verificadas. `qa_issue_count=0` no CSV desses dez registros (isso não atesta correção contábil). Resultado do script de conferência: `rmrp_auditoria/conciliacao_reprocessada/dossie_top10_conferencia_dca.json` em sessão local; não afirmar persistência no repositório/R2.
- Cinco maiores situações conferidas (IBGE/exercício, TCESP−DCA): 3548807/2023 −R$ 14.524.638,13; 3554102/2024 +R$ 5.158.659,54; 3545209/2023 −R$ 4.607.410,17; 3522158/2024 −R$ 3.882.278,14; 3533254/2024 −R$ 3.772.112,47.
- **Limite da diligência:** a conferência é documental sobre a extração canônica DCA e a matriz TCESP previamente auditada. Ainda **não** examina diretamente os anexos contábeis de origem, trilhas de retificação ou detalhamento original TCESP para esses dez casos; causas permanecem indeterminadas. Próxima etapa: recuperar e comparar documentos originais de cada município/ano, classificando estágio de despesa, órgão, grupo 44, data de atualização e eventuais retificações, preservando valores divergentes.

## Reextração seletiva independente dos dez maiores desvios — 26/10/2026
- **Iniciada a execução real de nova coleta dos ZIPs oficiais TCESP**, separada dos artefatos históricos, para os dez pares município–exercício de maior diferença monetária. Script novo: `governance/reextrair_tcesp_divergencias_seletiva.py`, commit `ef2fda0f`; workflow `.github/workflows/tcesp-selective-top10-reextract.yml`, commit `16ab1cf7`; execução [40341031425](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40341031425).
- Reextração **somente leitura**, uma tarefa por ano (2023: 3548807, 3545209, 3502804; 2024: 3554102, 3522158, 3533254, 3548906, 3534708, 3520301; 2025: 3517901). O processo baixa integralmente o ZIP oficial de cada ano, verifica CRC, percorre todas as linhas, retém apenas os registros selecionados, calcula com `Decimal` os valores em centavos do grupo 44 por estágio e documenta hash SHA-256, tamanho, contagem de linhas e presença mensal. Não usa a função de agregação do script anterior.
- Cada tarefa recupera o artefato de auditoria antigo do mesmo ano (`40263996213` em 2023/2024; `40262193781` em 2025) para comparar hash da fonte antiga e atual e total liquidado por município, gravando `seletiva_qa.json` e `comparacao_anterior_nova.json`. **Não inferir resultado antes da conclusão de todos os jobs**; diferença no total da nova coleta reprova o gate e exige diagnóstico de origem/pipeline/retificação. O ZIP bruto recente não é enviado nos artefatos; a fonte permanece referenciada por URL e hash.
- O workflow estava `in_progress` no último exame. Não houve alteração da DCA canônica, TCESP preservado, API ou produção.

**Controle independente complementar aprovado em 26/10/2026:** workflow `.github/workflows/tcesp-top10-aggregation-parity.yml`, [run 40341927996](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40341927996), `success`, artefato `tcesp-top10-aggregation-three-level-qa`. Nos dez casos prioritários, somatórios dos agregados históricos por município/mês/estágio, programa e ação foram exatamente iguais em todos os grupos, e seus totais `valor liquidado` corresponderam à matriz TCESP anterior. Isto comprova consistência **interna da agregação preservada**, não a fidelidade ao conteúdo bruto do ZIP nem a concordância com DCA. A reextração independente dos três ZIPs oficiais no [run 40341031425](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40341031425) continuava em etapa de download/processamento em 2023, 2024 e 2025 no último exame; resultados pendentes, sem alegar resolução das divergências. Nenhum dado canônico ou produção foi modificado.

## Auditoria da reextração TCESP — 26/10/2026, revisão de acesso à fonte
- Na execução [40341031425](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40341031425), o job de **2024 falhou na leitura do arquivo baixado** (`zipfile.BadZipFile: File is not a zip file`) antes de qualquer conferência contábil. Essa falha **não** comprova erro dos valores anteriores nem mudança de fonte; é necessário verificar conteúdo HTTP, resposta e integridade do download. Os jobs 2023 e 2025 ainda estavam sem resultado terminal na última consulta desta atualização.
- Adicionado controle fail-closed em `governance/reextrair_tcesp_divergencias_seletiva.py` (commit `cdfad43a`) que verifica assinatura ZIP antes da leitura e salva `source_access_diagnostic.json` com ano, URL, bytes, hash e assinatura hexadecimal inicial, quando o download não é ZIP. Não registrar conteúdo incorreto como execução homologada. A alteração será aplicada em **execução subsequente**, não ao job antigo já iniciado.
- **Próxima diligência:** identificar se o endereço TCESP agora retorna página HTML, bloqueio temporário ou redirecionamento; buscar fonte oficial alternativa/arquivo bruto persistido, se disponível, com hash e versão; executar a auditoria seletiva somente após validação de arquivo ZIP. Preservar dados anteriores e não atribuir causa às divergências com a DCA sem fonte íntegra. Produção intacta.

**Atualização da mesma execução:** o job 2025 também finalizou com `failure`, pela mesma exceção `zipfile.BadZipFile` ao abrir o conteúdo obtido no endereço oficial. Ambos os jobs 2024 e 2025 falharam **antes** de comparar valores TCESP antigos e novos. O job 2023 continuava `in_progress` no exame. O controle novo de diagnóstico ainda não havia sido aplicado a estes jobs. Não confundir a falha de obtenção/formato com divergência contábil.

## Diagnóstico definitivo da acessibilidade dos ZIPs oficiais TCESP — 26/10/2026
- A execução seletiva [40341031425](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40341031425) terminou com **`failure` nos três exercícios**, todos com `zipfile.BadZipFile` antes da leitura contábil. Não houve comparação válida nova/extratos antigos; não atribuir erro aos investimentos TCESP.
- Criada auditoria HTTP apenas de cabeçalhos e primeiros 256 bytes `.github/workflows/tcesp-zip-access-diagnostic.yml`, commit `6a37611c`. [Run 40344430852](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40344430852), sucesso nos três anos: `HEAD` HTTP 200 `application/zip` e `GET Range: bytes=0-255` HTTP **206**, com prefixo ZIP `504b0304` nos três casos e `Content-Range` consistente com o tamanho total da fonte.
- Tamanhos informados pelo servidor: **2023 2.103.701.773 bytes; 2024 2.070.545.389 bytes; 2025 2.104.704.991 bytes**. O teste de assinatura é preliminar e **não** comprova integridade integral do ZIP. Como as três falhas ocorreram após download de ~2GB, a hipótese prioritária é arquivo truncado, intermediário ou transferência incompleta; ainda não comprovada por comparação de tamanho/hash de cada falha.
- Inventário de R2 por API Cloudflare, em leitura, confirmou em `tcesp/estadual/despesas/2024/run_40263996213/` a existência de `qa.json`, `r2_manifest.json`, CSVs agregados por mês/estágio, programa e ação; **não** encontrou o ZIP bruto nessa pasta. Persistência dos agregados não equivale a preservação da fonte ZIP original.
- **Próxima etapa:** implementar e testar um download retomável por `Range`, verificando `Content-Range`, tamanho integral, assinatura e integridade CRC do ZIP antes do parser; idealmente persistir uma cópia bruta com hash para permitir nova extração sem download recorrente de 2GB. Manter a mesma seleção dos dez pares prioritários e preservar os resultados históricos, sem alterar produção.

**Correção técnica preparada após o diagnóstico HTTP:** `governance/download_tcesp_zip_range.py` (commit `3d99db1d`) implementa download retomável via HTTP 206 e intervalos `Content-Range` estritamente validados, com controle de comprimento total, SHA-256, integridade CRC e membro CSV. A reextração `governance/reextrair_tcesp_divergencias_seletiva.py` foi adaptada no commit `5467a822` para aceitar `--source-file` previamente verificado, evitando nova transferência integral por repetição. **Essas mudanças ainda não têm execução integral aprovada**; os arquivos de ~2GB precisam ser obtidos e auditados em uma execução controlada, preferencialmente uma vez por ano, antes de comparar os dez casos. Os dados originais e a produção não foram modificados.

## Teste controlado de download por faixas e reextração oficial — 26/10/2026
- O primeiro teste de fumaça do downloader identificou um **erro de sintaxe introduzido no parâmetro `--source-file`** do extrator seletivo. Corrigido em `e276fb4b`. A repetição encontrou erro na expressão de teste da assinatura ZIP (`b'PK\\x03\\x04'` em vez de bytes efetivos), corrigido em `21e9db39` com `bytes.fromhex('504b0304')`. Esses erros eram **do código de teste/preparação**, não dos dados fiscais.
- **Teste HTTP controlado `40345463611` aprovado (`success`)**: código das duas rotinas compilou e duas faixas contíguas de 128 bytes da fonte oficial TCESP 2024 foram obtidas como HTTP 206, com `Content-Range` correto, tamanho total consistente e assinatura ZIP. A verificação de 256 bytes não valida um ZIP completo.
- O extrator passou a ler o ZIP validado diretamente, sem duplicar ~2GB no disco, commit `ea7a7843`. Nova execução piloto **somente para 2025, município IBGE 3517901**, workflow `.github/workflows/tcesp-2025-range-reextract.yml`, run [40345679633](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40345679633), iniciada para: baixar o ZIP integral por faixas HTTP 206 com retomada e CRC, recalcular independentemente os investimentos liquidados, comparar hash atual e histórico e diferença dos totais em centavos. O teste publica apenas relatórios QA, não o ZIP de ~2GB e não altera dados canônicos ou produção.
- **Condição ainda pendente:** a execução integral não estava concluída na data deste registro; não declarar resolvida a divergência 3517901/2025 sem resultado do workflow. Se aprovada, ampliar o mesmo procedimento a 2023 e 2024, priorizando os nove casos restantes, com preservação de hashes e evidências.

## Continuidade da reextração seletiva TCESP — 26/10/2026
- O teste integral de 2025 [run 40345679633](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40345679633) **continuava em execução na etapa de download por faixas e CRC** no último exame deste registro. Não há resultado conclusivo da reprodução do valor liquidado do município `3517901` nem de hash do ZIP integral; não declarar o caso resolvido.
- Preparada a extensão auditável para **2023 (3 casos) e 2024 (6 casos)** em `.github/workflows/tcesp-2023-2024-range-reextract.yml`, commit `39c4b394`, sob acionamento manual, com `max-parallel: 1` para evitar concorrência de grandes transferências. O workflow verifica download oficial completo, SHA-256, CRC, reextração independente, comparação município a município com agregados históricos de `40263996213` e diferença em centavos. Artefatos contêm relatórios QA, não o ZIP bruto de cerca de 2 GB.
- **Protocolo de continuidade:** verificar o desfecho de `40345679633`; se 2025 concluir com validação, acionar controladamente a execução de 2023–2024. Caso falhe, diagnosticar HTTP/transferência/ZIP e ajustar antes de replicar. Nenhuma alteração na DCA canônica, nos valores TCESP anteriores, na API ou na produção.

## Acompanhamento de transferência TCESP e controles de retomada — 26/10/2026
- O piloto integral [40345679633](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40345679633) continuava `in_progress`, na etapa de transferência oficial de 2025, na última consulta; **nenhuma reextração comparativa conclusiva disponível ainda**. Não presumir sucesso nem falha contábil.
- Aprimorado `governance/download_tcesp_zip_range.py` no commit `357580d5`: registro do percentual/progresso por faixa e uso de `If-Range` baseado no ETag obtido na consulta HEAD para evitar combinação silenciosa de versões do ZIP numa retomada; a retomada de arquivo parcial é recusada se não houver ETag. **A execução já iniciada usa código do checkout anterior; as melhorias valem para novas execuções.**
- O teste controlado de sintaxe e acesso a duas faixas HTTP 206 foi repetido no [run 40350558166](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40350558166), finalizado com `success`. Esse teste valida as rotinas e as duas faixas iniciais, não a integridade do ZIP de ~2 GB.
- Extensão 2023/24 permanece preparada, ainda sem execução. A decisão seguinte depende do encerramento e dos artefatos do run 40345679633, preservando produção e versões históricas.

## Reextração independente TCESP 2025 aprovada e ampliação 2023–2024 — 26/10/2026
- **Run 40345679633 terminou `success`**: ZIP oficial completo de despesas 2025, **2.104.704.991 bytes**, verificação CRC `pass`, SHA-256 `ca4e0936c9d61d511aa0b778182a5ab3724503e0149ea84a8e0da17aae4b2d93`. O hash coincide exatamente com o reportado na extração histórica auditada (2025). Arquivo CSV interno `despesas-2025.csv`.
- Na reextração independente do município IBGE **3517901, 2025**, `valor liquidado` do grupo 44 antigo **482.777.814 centavos**, novo **482.777.814 centavos**: diferença **zero**. A divergência com o valor DCA **422.548.920 centavos** (diferença TCESP menos DCA R$ 602.288,94) permanece sem causa documental comprovada. Não se justifica alterar qualquer valor por hipótese.
- Após o êxito de 2025, liberada a execução controlada de **2023 e 2024** pelo workflow `.github/workflows/tcesp-2023-2024-range-reextract.yml`, commit `fd3cf59d`; execução [40357587853](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40357587853) iniciou `queued`, com `max-parallel: 1`, para os **nove outros casos**. Os hashes e novos totais precisam ser verificados nos artefatos finais antes de qualquer conclusão. Bases canônicas, preview e produção permanecem inalteradas.

## Dossiê consolidado da reextração independente dos dez maiores desvios — 26/10/2026
- Novo relatório permanente: [REEXTRACAO_TCESP_CASOS_PRIORITARIOS_20261026.md](governance/REEXTRACAO_TCESP_CASOS_PRIORITARIOS_20261026.md), commit `d90859d2`, com procedimento, origem, hash e CRC do ZIP integral de 2025, reprodução exata em centavos de `3517901/2025`, diferença TCESP−DCA que permanece e critérios explícitos para interpretar os nove outros casos.
- O run [40357587853](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40357587853) de 2023–24 permanece dependente da conclusão de download integral de ~2GB por exercício; não declarar igualdade, divergência nova ou erro de pipeline antes do relatório de cada job. Quando os jobs terminarem, verificar `comparison.json`, `seletiva_qa.json`, hash da fonte e `all_totals_equal` por código IBGE. Produção e bases canônicas preservadas.

## Resultado seletivo de 2023 — 26/10/2026
- Run [40357587853](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40357587853): **job 2023 `success`**, ZIP oficial 2.103.701.773 bytes, CRC íntegro e SHA-256 antigo/novo idêntico `78de6ad8c031240a81c789d5e1379d12efd0a44536c62dbfbaba2c6e45f893d0`. Reextração independente do estágio `valor liquidado` do grupo 44 replicou exatamente os três totais: 3502804 R$ 32.513.168,01; 3545209 R$ 39.898.893,44; 3548807 R$ 147.173.188,49. **Diferença zero em todos**. Agora **4/10 casos prioritários reextraídos** com totais idênticos, incluído o caso 2025. A tarefa 2024 ainda estava em transferência na última verificação; seis pares sem comparação conclusiva. Dossiê atualizado em [governance/REEXTRACAO_TCESP_CASOS_PRIORITARIOS_20261026.md](governance/REEXTRACAO_TCESP_CASOS_PRIORITARIOS_20261026.md). Não confundir reprodutibilidade TCESP com solução de divergências TCESP–DCA; produção inalterada.

## Reextração integral dos dez casos prioritários — atualização posterior de 26/10/2026
- A tarefa de **2023** do run [40357587853](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40357587853) permanece `success`, com 3/3 totais reproduzidos e mesmo hash da fonte oficial. A tarefa de **2024** já encerrou o download completo e entrou na etapa `Reconstruct priority investment totals independently`, ainda `in_progress` na última consulta. Portanto, **não foi homologada comparação final dos seis casos de 2024** nesta atualização. A análise causal TCESP–DCA permanece condicionada ao resultado e aos demonstrativos originais; não alterar fontes/produção por hipótese.

## Fechamento da reextração independente dos dez maiores desvios — 26/10/2026
- [Run 40357587853](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40357587853) terminou **`success` em 2023 e 2024**; em conjunto com o [run 40345679633](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40345679633) (2025), **10/10 casos prioritários** reproduziram exatamente os investimentos liquidados TCESP em centavos, sem diferença entre extrações. Os três ZIPs oficiais passaram nos testes de integridade CRC e tiveram hashes antigos/novos idênticos.
- SHA-256 do ZIP 2024: `b019086c76ff69dd3f03e2ace3c83005064caa74024723e00a34c7cbb36e90f6`; tamanho 2.070.545.389 bytes. Os seis casos 2024, código IBGE/centavos antigo=novo: 3520301/1.554.845.411; 3522158/390.391.912; 3533254/130.523.240; 3534708/9.026.750.766; 3548906/13.874.083.267; 3554102/4.543.193.366. Os três casos 2023 e um de 2025 já haviam sido aprovados.
- Dossiê de auditoria consolidado: [governance/REEXTRACAO_TCESP_CASOS_PRIORITARIOS_20261026.md](governance/REEXTRACAO_TCESP_CASOS_PRIORITARIOS_20261026.md), commit `62ee6218`. **Não classificar as 55 diferenças TCESP–DCA como erro de pipeline apenas por discrepância entre fontes.** O teste excluiu erro de extração não reproduzível nos dez casos, mas não valida comparabilidade contábil integral. Seguir para exame das fontes originais e de eventuais retificações, sem alterar valores canônicos nem produção.

## Início da reconciliação documental TCESP–DCA — 26/10/2026
- Criado [governance/TRIAGEM_DOCUMENTAL_TCESP_DCA_TOP10_20261026.md](governance/TRIAGEM_DOCUMENTAL_TCESP_DCA_TOP10_20261026.md), commit `34ef8212`, com a matriz dos dez maiores desvios e a verificação dos **critérios exatos implementados no código**: DCA `DCA-Anexo I-D`/coluna `Despesas Liquidadas`/conta `DO4.4.00.00.00.00`; TCESP seleção de `ds_elemento` com prefixo `44`, `tp_despesa = valor liquidado`, somatório mensal `vl_despesa` em centavos.
- Embora a reextração independente dos dez casos TCESP esteja **10/10 reproduzida**, isso não testa se os critérios de seleção de grupo 44 e a conta DCA DO4.4 têm a mesma abrangência contábil. Próxima etapa é confrontar dicionários oficiais, escopo do ente, tratamentos de estorno, órgãos/unidades, versões/retificações dos demonstrativos e diferença residual por município/ano, sem propor correção enquanto não houver prova documental. As hipóteses estão classificadas como **pendentes**, não como causas identificadas. Produção inalterada.

## Conciliação documental TCESP–DCA: acesso aos originais Siconfi — 26/10/2026
- Criada a [diligência Siconfi DCA API](governance/DILIGENCIA_SICONFI_DCA_API_20261026.md), commit `4c0fa978`, reunindo fontes oficiais para a próxima checagem dos dez desvios de maior materialidade. O contrato de API do Tesouro expõe `/dca` e `/extrato_entregas` na base `https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/`, com respostas JSON, 5.000 itens/página por padrão e **limite declarado de uma requisição por segundo**. O histórico público Siconfi distingue declarações homologadas e não homologadas; a documentação DCA define o Anexo I-D como despesa por natureza.
- **Limite da constatação:** nesta diligência foram verificadas as páginas oficiais e a disponibilidade documental dos serviços, **não** os registros individuais ou eventuais retificações dos dez pares, nem uma prova de equivalência entre `DO4.4.00.00.00.00` (DCA) e prefixo `44` (TCESP). O endpoint de especificação OpenAPI não pôde ser extraído pelo crawler; antes da consulta automatizada, confirmar parâmetros oficiais e paginação. Começar por 3548807/2023, 3554102/2024 e 3545209/2023, preservando resposta bruta/hash e sem extrapolar causalidade. Produção e bases mantidas.

## Verificação direta Siconfi DCA para os dez maiores desvios — 26/10/2026
- Foram consultados os **10/10 pares** por API Siconfi `/dca` (Anexo I-D, Padrão, Despesas Liquidadas, `DO4.4.00.00.00.00`), todos com `hasMore=false`, e confrontados aos valores DCA históricos e TCESP já reextraídos. **Três casos de 2024 agora mostram concordância DCA atual–TCESP:** Taubaté (3554102) R$ 45.431.933,66, Ourinhos (3534708) R$ 90.267.507,66, Iguape (3520301) R$ 15.548.454,11. Os valores canônicos históricos eram inferiores, respectivamente, em R$ 5.158.659,54, R$ 721.663,28 e R$ 495.010,68. Nos outros **sete casos** a DCA atual coincide com o snapshot e o desvio TCESP persiste.
- Os extratos de entrega já foram lidos para São Caetano do Sul/2023 (`RE`, 2024-07-10), Taubaté/2024 (`RE`, 2025-08-14) e Salto/2023 (`HO`, 2024-04-30); as siglas são mantidas como metadados brutos, **sem interpretação causal ou comprovação de retificação**. Os outros sete extratos ainda precisam ser examinados.
- Relatório: [governance/CONFRONTO_DCA_API_EXTRATOS_TOP3_20261026.md](governance/CONFRONTO_DCA_API_EXTRATOS_TOP3_20261026.md), commit `5849e90f`. Preservar ambos os estados da DCA (snapshot histórico e consulta atual), sem sobrescrever a fonte canônica ou alterar produção antes de auditoria de versões, proveniência e repercussão nos demais 55 registros.

## Extratos oficiais Siconfi DCA dos dez maiores desvios — 26/10/2026
- **10/10 extratos de entrega DCA consultados** por API Siconfi `/extrato_entregas` com `id_ente` e `an_referencia`, e valor DCA atual conferido nos dez casos em `/dca`. A matriz completa de códigos de situação, datas UTC, observações do valor atual e limitações de histórico está em [governance/CONFRONTO_DCA_API_EXTRATOS_TOP3_20261026.md](governance/CONFRONTO_DCA_API_EXTRATOS_TOP3_20261026.md), atualização commit `ed605b44`.
- Nos casos de **Taubaté/2024, Ourinhos/2024 e Iguape/2024**, a DCA atual coincide em centavos com o TCESP auditado, enquanto o snapshot DCA histórico difere; o extrato de cada um traz código literal `RE` com datas de status 2025-08-14, 2025-10-20 e 2026-05-14, respectivamente. **Não concluir que estas datas demonstram a mudança exata do valor** sem acesso a versões anteriores da declaração. São Caetano do Sul/2023 também aparece com `RE`, mas segue divergente; portanto `RE` não é critério suficiente para conciliação.
- Próxima diligência: estabelecer a interpretação formal dos códigos e verificar histórico de valores/retificações. Preservar snapshot canônico DCA e dados TCESP como evidências; a atualização automática da plataforma está suspensa até critérios de versionamento e homologação.

## Auditoria dos extratos de entrega DCA dos dez casos — 27/10/2026
- Concluídas consultas diretas a `/extrato_entregas` dos **10/10** pares de maior diferença TCESP–DCA; todos os sete extratos novos retornaram `hasMore=false`. Código bruto de situação da DCA por município: **RE** em São Caetano do Sul/2023, Taubaté/2024, Ourinhos/2024 e Iguape/2024; **HO** em Salto/2023, Itaóca/2024, Novais/2024, São Carlos/2024, Araçatuba/2023 e Guaraci/2025. Datas e forma de envio em [governance/CONFRONTO_DCA_API_EXTRATOS_TOP3_20261026.md](governance/CONFRONTO_DCA_API_EXTRATOS_TOP3_20261026.md), commit `b56691c6`.
- **Três casos (Taubaté, Ourinhos, Iguape)** passaram a apresentar DCA atual igual ao TCESP e todos registram `RE`, mas **São Caetano do Sul também registra `RE` e mantém a divergência**. Não afirmar equivalência entre o código de situação e uma retificação que explica o valor sem consultar o histórico de versões e a definição oficial dos códigos. Permanecem separados snapshot DCA, DCA API atual e TCESP íntegro. Nenhuma alteração na base canônica nem produção.


## Diligência de versões e status Siconfi — 27/10/2026
- Registrado o exame documental de situações homologada e retificada, a utilidade da consulta de histórico e dos pacotes de declarações e seus limites de prova em [governance/DILIGENCIA_VERSOES_DCA_SICONFI_20261027.md](governance/DILIGENCIA_VERSOES_DCA_SICONFI_20261027.md), commit `1ddda314`.
- No grupo dos dez maiores desvios, os literais de situação do extrato são quatro `RE` e seis `HO`. Taubaté, Ourinhos e Iguape/2024 têm DCA atual coincidente com TCESP, mas o status `RE` por si só não demonstra qual retificação alterou os valores; São Caetano do Sul/2023 é controle negativo com `RE` e diferença persistente.
- Próximo controle: recuperar histórico de versões e, se acessível, os conteúdos antigos das declarações; confrontar conta DO4.4.00.00.00.00 com snapshots anterior e atual, por centavos, registrando hashes. Sem mudança nas bases canônicas, R2, API ou produção.


### Confirmação de acesso ao histórico público Siconfi — 27/10/2026
- O manual e a interface pública do histórico DCA foram consultados diretamente: formulários por ente, exercício, Poder, instituição e escopo; resultado com data de homologação e situação e exportação CSV/PDF. O pacote de declarações é descrito como ZIP com filtros por data de homologação/retificação, **não como prova de acesso a todas as versões de cada valor**.
- A automação da sessão JSF não retornou resultados municipais nesta rodada; nenhuma versão histórica antiga foi obtida. Registrado o controle e o procedimento de navegação em [governance/DILIGENCIA_VERSOES_DCA_SICONFI_20261027.md](governance/DILIGENCIA_VERSOES_DCA_SICONFI_20261027.md), commit `1af90bcb`.
- Próxima ação: consulta interativa e exportação de históricos de Taubaté/2024, Ourinhos/2024, Iguape/2024 e São Caetano do Sul/2023, seguida de teste de acesso aos valores da versão anterior. Até lá, manter separadas as séries DCA snapshot, DCA API atual e TCESP. Sem alterações em base ou produção.


### Investigação da consulta de versões históricas DCA — 27/10/2026
- Conferidas oficialmente três vias distintas: Histórico de Declarações (estado/data de homologação); Consulta Pública de Declarações (estado atual e PDF/XLS); e Linha do Tempo em **Gerir Declaração** (histórico de operações na área restrita). A documentação consultada não comprovou que a API pública ou os pacotes ZIP forneçam todas as versões substituídas do Anexo I-D. Não supor que retificação explique individualmente mudança de valor sem recuperar o demonstrativo anterior.
- Registradas as fontes, as limitações e a distinção entre **conciliação numérica atual** (3 de 10 pares agora concordantes) e **explicação causal documentada** (pendente) no [dossiê de versões DCA](governance/DILIGENCIA_VERSOES_DCA_SICONFI_20261027.md), commit `5601035c`.
- Próximos passos: testar a consulta pública PDF/XLS e exportação de histórico para os quatro casos de controle; se a versão antiga não puder ser obtida, solicitar formalmente metadados e versões à STN. Manter DCA snapshot, DCA atual e TCESP separados; sem alterações na produção.


### Histórico Siconfi: inspeção JSF e restrição de navegador — 28/10/2026
- Recuperado via Crawl2AI o HTML do formulário público `formHistorico` da consulta de histórico da DCA; identificados filtros Municipal/Executivo/Balanço Anual (DCA)/2023–2024 e escopos homologadas/não homologadas, além do campo JSF `javax.faces.ViewState`. Não houve retorno de dados municipais filtrados.
- Tentativa de executar navegador Browserless/Puppeteer bloqueada por **HTTP 401, cota de unidades do plano gratuito esgotada**; isso não constitui resultado negativo do Siconfi. Documentação oficial da API aberta examinada não revelou método explícito de recuperar conteúdo de todas as versões substituídas.
- Adendo técnico e encaminhamentos registrados em [governance/DILIGENCIA_VERSOES_DCA_SICONFI_20261027.md](governance/DILIGENCIA_VERSOES_DCA_SICONFI_20261027.md), commit `c906482b`. Próximo teste preferencial: Playwright no GitHub Actions em execução manual isolada, reaproveitando infraestrutura já existente no repositório, para testar interação do formulário e exportação dos quatro históricos prioritários, sem autenticação. Não modificar DCA, TCESP, API ou produção.


### Piloto de inspeção da interface pública Siconfi — 28/10/2026
- Criados `governance/qa_siconfi_history_form.py` (commit `9068842a`) e `.github/workflows/siconfi-history-form-qa.yml` (commit `f0e0832b`) para inspeção isolada da página pública com Playwright/Chromium no GitHub Actions. O teste verifica presença do formulário e controles, registra status HTTP e título e salva captura da tela e relatório JSON, sem autenticação ou acesso a registros privados.
- O workflow é acionável manualmente e por push dos dois arquivos. **A execução e o resultado do Actions ainda precisam ser conferidos**; não declarar a consulta municipal ou histórico exportado como concluído. Este primeiro gate não preenche municípios nem obtém versões históricas: sua função é homologar o ambiente de navegador e os controles JSF antes de ampliar o piloto para Taubaté/2024.
- Próximos passos: verificar run e artefato `siconfi-history-form-qa`; se o gate passar, implementar seleção assistida de município/exercício e exportação CSV/PDF do histórico, preservando versões de origem e hashes. Nada foi alterado em DCA, TCESP, API ou produção.


### Acionamento do QA público Siconfi — 28/10/2026
- Solicitada execução do workflow **Siconfi public history form QA** por alteração do arquivo monitorado `governance/qa_siconfi_history_form.py`, commit `a41d46459824d07245c9b68b44ab606a1ee515ce`. O gatilho `push` está definido em `.github/workflows/siconfi-history-form-qa.yml`.
- **Execução não homologada**: o conector disponível para `fetch_commit_workflow_runs` lista apenas execuções originadas por pull request, não permitindo confirmar esse disparo `push`; a tentativa de verificar a página Actions diretamente falhou. O status combinado do commit retornou lista vazia, que **não comprova ausência nem sucesso** do job. Não foram recuperados logs nem artefatos.
- O ambiente local também não dispõe de resolução DNS para github.com, impossibilitando conferência independente por shell. Aguardar uma verificação efetiva da execução/artefato [Actions do workflow](https://github.com/hilaliskandar/mapa_do_tesouro/actions/workflows/siconfi-history-form-qa.yml) antes de afirmar teste aprovado ou avançar à recuperação dos históricos municipais. Bases fiscais, API e produção inalteradas.


### Gate de navegador Siconfi homologado — 28/10/2026
- A consulta ao GitHub Actions por workflow confirmou duas execuções `push` **success**: [run 40683579936](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40683579936), commit `a41d4645`, e [run 40682825752](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40682825752), commit `f0e0832b`.
- No run 40683579936, job `public-form` **completed/success**, inclusive passos Playwright/Chromium, execução de `governance/qa_siconfi_history_form.py` e upload do artefato. Evidência: [artefato siconfi-history-form-qa, ID 12813732628](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40683579936/artifacts/12813732628), ZIP com 2 arquivos (relatório JSON e captura de tela), SHA-256 do ZIP `faa5fc6dd620b0e585e4104fc8aff2da6aa808b0008a2130cb19039a49831649`, 71.758 bytes. Validade prevista do artefato até 11/11/2026.
- A lógica do script retorna exit code zero apenas com formulário `formHistorico` presente, após navegação HTTP e captura; assim o **gate técnico inicial de disponibilidade da interface pública foi aprovado**. Ainda NÃO houve consulta de município/exercício, exportação de histórico ou prova de versões antigas da DCA. O conteúdo interno de `report.json` ainda não foi inspecionado; não afirmar que todos os controles foram reconhecidos sem ler o arquivo.
- A próxima etapa é ampliar o piloto para seleção de Taubaté/2024 via JSF e download de histórico, mantendo execução manual e evidência rastreável, sem alterar base ou produção.


### Piloto de seleção JSF no histórico DCA — 28/10/2026
- Implementada segunda etapa em `governance/qa_siconfi_history_form.py`, commit `d0f43991`: para Taubaté/2024, inspeciona controles do formulário, tenta selecionar `Municipal` e `São Paulo` mediante eventos `change` no controle nativo PrimeFaces, captura `after_sphere.png` e exporta `report.json` com ações e opções do formulário. Para evitar falsas evidências, a versão **ainda não submete** uma consulta por município nem afirma recuperar versões anteriores; falta resolver autocomplete do ente/instituição e fluxo AJAX real.
- O GitHub Actions identificou o novo disparo automático por `push`: [run 40687588846](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40687588846), commit `d0f43991`; na primeira verificação sua conclusão ainda estava pendente. É necessário ler logs e relatório JSON para determinar se a seleção parcial foi realizada.
- Sem alteração das bases DCA/TCESP ou da produção. Uma aprovação da execução nesse piloto apenas valida o fluxo parcial; **não significa obter histórico Taubaté/2024**.


### Inspeção do artefato Siconfi e correção dos seletores — 28/10/2026
- Recuperado o ZIP do run [40687588846](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40687588846), artefato ID `12815921451`, SHA-256 `5b853361bab973a44e59d1ea10ffc3d73ee56b92a07f0bca4163c1dfc5ee27f8`; `report.json` registra HTTP 200, `formHistorico` presente, seleção `Municipal` e `municipal_results=false`, com status `partial_form_selection`.
- O próprio relatório mostrou que o campo de UF chama-se `formHistorico:estado_input` (e **não** `uf`). Demais códigos reais: São Paulo `35`; Executivo `E`; exercício `2024`; Balanço Anual (DCA) `QDCC`; escopo homologadas `HOMOLOGADO`. A etapa anterior não selecionou o Estado porque utilizava identificador incorreto.
- Corrigido o script no commit `1e4e12a1`, com seleção destes filtros e registro do estado de habilitação dos campos `ente` e `orgao`. Novo workflow por `push`: [run 40688139750](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40688139750), observado inicialmente `in_progress`; confirmar resultado e inspecionar novo `report.json` antes de avançar. Ainda **não** há consulta de dados municipais, exportação nem versão histórica anterior recuperada. Bases e produção intactas.


### Teste real do autocompletar Taubaté — 28/10/2026
- Workflow [run 40693009284](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40693009284), commit `0d22bbae`, concluído com `success`. Artefato [12818445756](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40693009284/artifacts/12818445756), ZIP com `report.json` e 3 capturas, examinado. Resultado: HTTP 200; seis seletores iniciais preenchidos; `ente_input_disabled=false`, `orgao_input_disabled=true`; texto `Taubaté` inserido, **zero sugestões detectadas no DOM**; `municipal_results=false`, status `partial_form_selection`.
- Para investigar se o comportamento decorre do preenchimento instantâneo sem eventos de teclado, o script foi ajustado (commit `a272affd`) para digitação sequencial real, espera de 4s, inspeção de `ente_panel` (incluindo visibilidade/HTML resumido) e conferência de `ente_hinput` (identificador interno). A nova execução ainda carece de conferência de resultado e artefato. Não considerar município selecionado sem `ente_hinput` validado nem iniciar consulta com identificador presumido.
- Dados contábeis, API e produção inalterados.


### Taubaté identificada no autocompletar Siconfi — 28/10/2026
- Execução [40695756309](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40695756309), commit `a272affd`, **success**. Artefato [12819352057](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40695756309/artifacts/12819352057), com `report.json` e capturas, examinado: após digitação sequencial, o painel `formHistorico:ente_panel` apareceu visível com uma opção `Taubaté`, `data-item-value=3554102`. O campo oculto `ente_hinput` ainda continha `Taubaté` no instante anterior ao clique, logo **não tratar autocompletar como seleção final**.
- Script atualizado no commit `49c566d1` para clicar somente na opção pública comprovada de código IBGE `3554102` e registrar `selected_ente_hidden`, estado de `orgao_input` e controles após seleção. Esse avanço do fluxo ainda exige conferência do novo job e artefato. Nenhuma submissão de consulta histórica, exportação ou acesso a versão anterior ocorreu até aqui.
- Sem modificações às bases canônicas, APIs e produção.


### Seleção efetiva do município Taubaté no histórico Siconfi — 28/10/2026
- Workflow [40699882574](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40699882574), commit `49c566d1`, concluído com **success**. Artefato [12821256789](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40699882574/artifacts/12821256789), ZIP de 296.503 bytes, recuperado e `report.json` inspecionado: `municipality_selected=true`, `selected_ente_hidden=3554102` e `orgao_after_selection_disabled=false`. Logo a opção Taubaté foi efetivamente selecionada, habilitando o campo institucional.
- Controles após a seleção: `formHistorico:orgao_input` (texto) e `formHistorico:orgao_hinput` (identificador oculto, ainda vazio). No commit `1cf49ecc`, o script passou a digitar `Prefeitura` e registrar as opções visíveis do autocompletar institucional em `orgao_candidates`, sem confirmar uma instituição por antecipação nem submeter histórico.
- **Pendente:** conferir o novo Actions/artifact, selecionar instituição com valor retornado e finalmente consultar/exportar o histórico de Taubaté/2024. Não existem valores históricos anteriores extraídos nesta etapa. Bases, APIs e produção preservadas.


### Taubaté/2024: identificação de Prefeitura no Siconfi — 28/10/2026
- Workflow [40700893704](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40700893704), commit `1cf49ecc`, `success`; artefato [12821807048](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40700893704/artifacts/12821807048), `report.json` examinado. Município previamente selecionado `3554102`; autocompletar de órgão retornou uma opção visível **Prefeitura Municipal de Taubaté - SP**, `data-item-value=7953`. Valor oculto antes do clique = texto `Prefeitura`, portanto a instituição ainda não estava formalmente selecionada.
- Script atualizado no commit `2988b630` para clicar apenas na opção institucional validada `7953`, registrar `orgao_hinput` após seleção, botões do formulário e captura de tela. O novo workflow necessita conferência de conclusão e artefato; consulta de histórico e exportação de versões antigas ainda não ocorreram.
- Isolamento mantido; bases DCA, TCESP, R2, API e produção intactas.


### Seleção da Prefeitura e tentativa controlada de consulta pública — 28/10/2026
- Workflow [40722435938](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40722435938) (commit `2988b630`) **success**; artefato [12832025393](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40722435938/artifacts/12832025393) recuperado e `report.json` examinado: `institution_selected=true`, `orgao_hidden_after_selection=7953`, `selected_ente_hidden=3554102`; botão `Consultar` presente no formulário.
- A captura `institution_selected.png` mostra os campos de seleção visual de esfera, UF, poder, exercício, declaração e escopo aparentemente em branco, embora os campos `<select>` internos tenham valores definidos nos passos anteriores. Logo a seleção PrimeFaces por disparo manual de `change` requer confirmação de sincronização visual/JSF; **não assumir que a consulta está corretamente parametrizada nem classificar a tabela inicial 'Nenhum registro encontrado' como resposta da pesquisa**, pois ainda não havia sido enviado comando Consultar.
- Novo commit `fd3c73a1` acrescentou um clique controlado no botão `Consultar`, sem autenticação, com coleta das mensagens de validação, texto e captura após o evento, para identificar se os parâmetros foram aceitos. Workflow [40727542975](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40727542975) detectado em progresso na última consulta; resultado e artefato pendentes.
- Nenhuma declaração histórica, arquivo antigo ou dado fiscal foi exportado. Bases canônicas e produção intactas.


### Bloqueio de verificação humana na consulta histórica DCA — 28/10/2026
- Workflow [40727542975](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40727542975), commit `fd3c73a1`, `success`, artefato [12833721234](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40727542975/artifacts/12833721234) recuperado e inspecionado. `report.json` confirma `query_clicked=true`, `selected_ente_hidden=3554102`, `orgao_hidden_after_selection=7953` e status nominal `query_attempted_results_unverified`.
- **Constatação decisiva na captura `after_query.png`:** a submissão exibiu desafio visual de verificação humana (captcha). Não houve conclusão válida da pesquisa, exportação ou demonstração de ausência de declarações. A tabela inicial com `Nenhum registro encontrado` **não** representa resultado negativo após consulta válida.
- A captura mostra seletores visuais de esfera/declaração aparentemente em branco, embora no DOM os `<select>` correspondentes tenham valores `M` e `QDCC`; corrigir sincronização PrimeFaces apenas para garantir qualidade do formulário, sem pretender ultrapassar o desafio de verificação humana.
- Código ajustado no commit `54629b13` para registrar o indicador `human_verification_detected` e distinguir tentativa de consulta de consulta efetivamente realizada. **Interromper tentativas automáticas de atravessar a validação humana.** Alternativas: consulta assistida em navegador por operador autorizado; acesso às entregas via API aberta `/extrato_entregas` já documentada; pedido documental à STN para versões pretéritas. Manter séries DCA snapshot, DCA API atual e TCESP separadas, sem alteração da produção.


## Decisão de encerramento da conciliação compulsória TCESP–DCA — 28/10/2026
**Decisão de direção do projeto:** encerrar a auditoria geral de diferenças TCESP–DCA como impedimento à continuidade. As duas fontes possuem identidades, regras declaratórias e granularidades próprias e devem ser mantidas como **séries oficiais distintas**, com indicação explícita da origem, definição e data de consulta. Não exigir igualdade numérica como condição de publicação nem substituir automaticamente valores de uma fonte pelos de outra.

- **TCESP:** fonte operacional das análises da execução orçamentária municipal paulista, incluindo investimentos liquidados por natureza, programa e ação, conforme arquivos oficiais estaduais e metodologia documentada.
- **Siconfi/STN, DCA:** fonte oficial das contas anuais declaradas ao Tesouro, preservando o Anexo I-D e as definições federais. Diferenciar snapshot histórico e API consultada posteriormente; ambos são evidências datadas, não substitutos intercambiáveis.
- **Diferenças:** indicar como divergência **entre medidas/fontes**, sem classificar automaticamente como erro, sem pressupor equivalência perfeita de cobertura ou atribuir causa específica não demonstrada. A identidade entre conceitos ainda não foi plenamente comprovada; a decisão de encerrar a rotina não equivale a demonstrar que cada diferença esteja explicada.
- **Reabertura seletiva:** apenas quando a discrepância modificar um indicador central, decisão editorial, ranking ou conclusão regional, ou houver evidência de erro de processamento, versão ou classificação. Preservar as diligências históricas como documentação, sem rotina adicional de recuperação de versões antigas da DCA.
- **Próxima prioridade:** voltar à integração, controles de qualidade e produção analítica do relatório RMRP, com mapas inseridos nas seções temáticas pertinentes, gráficos e tabelas rastreáveis, e avançar na plataforma estadual sem alterar produção automaticamente. Verificar o estado verificável dos artefatos e da implantação antes de publicar.

**Status da frente:** ENCERRADA PARA FINS DE FLUXO DE TRABALHO, COM RESSALVAS METODOLÓGICAS DOCUMENTADAS. Nenhum dado contábil, publicação ou endpoint alterado por esta decisão.


### Retomada do caderno fiscal RMRP — 28/10/2026
- Inventário editorial e roteiro de integração produzido em [`editorial/rmrp/RETOMADA_CONSOLIDACAO_2026_10_28.md`](editorial/rmrp/RETOMADA_CONSOLIDACAO_2026_10_28.md), commit `77427a97`. Localizados seis registros canônicos de consolidação DCA, evolução real IPCA, investimentos TCESP e estado do caderno integrado.
- Recuperação documental **parcial**: o arquivo integral de 34 fichas e o pacote de mapas/gráficos são mencionados, mas ainda não foram recuperados e conferidos nesta diligência. Não afirmar que o relatório integral foi recomposto. Planejada inserção de mapas nas seções temáticas (território, receitas, investimentos, gestão fiscal), sem atlas isolado.
- Fatos-base preservados: 34 municípios (15/6/6/7); DCA variação real 2023–2025 receita corrente +10,25%, despesa corrente +7,09%, investimento -42,97%; TCESP 2025 investimento liquidado R$ 302.301.895,18. Séries distintas. Sem alterações nas fontes, API ou publicação.


### Recuperação da edição nativa RMRP no Drive — 28/10/2026
- **Corrigido o inventário da retomada**: localizado e lido o README canônico de continuidade no Drive (`1e4G6zFFG6bxz_NKJj6yOwiJbkMb2i_MuQ4JLo3DrwlU`), que aponta a minuta editorial principal `1UXpfCAllRc84nj49yeRyT14H2Neij_S8elZzq79MxyY` e os relatórios integrados de 23/10. O caderno de 19/10 não é a última edição.
- Recuperada a referência de prova cartográfica nativa de 25/10 (`1FF5nX64MwOcX3oF5SKIl72w-4zG0MD74tzmtFsyMxAg`): 63 páginas, 51 tabelas, 34 fichas e quatro mapas ampliados junto aos capítulos, segundo QA anotado no README de continuidade. Prova não homologada e com 12 dos 16 mapas originais ainda não integrados nessa modalidade.
- O [inventário editorial de 28/10](editorial/rmrp/RETOMADA_CONSOLIDACAO_2026_10_28.md) foi corrigido com IDs/links dos originais e orientações para a continuidade. Pendente conferir conteúdo e formato da minuta editorial principal e planejar preservação dos 16 indicadores; nenhum documento canônico ou produção foi modificado.


### Base editorial de trabalho cartográfico da RMRP — 28/10/2026
- Conferência nativa por Google Docs: minuta editorial 23/10 (`1UXpf...`) **35 tabelas/2 imagens**, relatório consolidado 23/10 (`1-M-HK...`) **51 tabelas/4 imagens**, prova cartográfica 25/10 (`1FF5...`) **51 tabelas/4 imagens**. Portanto, não confundir a minuta menor com a versão consolidada integral.
- Criada cópia independente para continuidade [RMRP — Trabalho cartográfico 16 indicadores — 28-10-2026](https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit), cujo readback confirmou **51 tabelas, 4 imagens, 622 elementos de corpo**. Nenhuma edição nas fontes/principais e nenhuma publicação.
- [Inventário detalhado](editorial/rmrp/RETOMADA_CONSOLIDACAO_2026_10_28.md) atualizado com vínculo da cópia e plano para conservar os 16 indicadores cartográficos integrados aos capítulos, sem atlas separado.


### Preparação cartográfica dos 16 mapas RMRP — 28/10/2026
- Recuperado o PDF original de nove páginas [RMRP_VOLUME_PUBLICO_MAPAS_E_ANALISES_16_INDICADORES_2026_10_19](https://drive.google.com/file/d/10vbnQ_eBNsSmpWekFrrgJyeyTeNlm3YN/view). Extraídos os quatro mosaicos raster originais (páginas 2, 3, 6 e 7, 3000×2500 pixels) e gerados 16 recortes por quadrante, 1500×1250 pixels, **sem interpolação**, acompanhados de manifesto com hashes SHA-256, prova PDF de 16 páginas e pacote ZIP disponibilizados nesta conversa.
- [Inventário nominal dos 16 indicadores e distribuição editorial](editorial/rmrp/INVENTARIO_16_MAPAS_2026_10_28.md), commit `403cc539`. Quatro mapas individuais já estão na cópia nativa de trabalho; os outros 12 exigem QA de legenda, enquadramento e inserção por capítulo. **Nenhuma alteração no Google Doc principal ou na cópia de trabalho nesta etapa.**


### Regra cromática de leitura intuitiva da cartografia RMRP — 28/10/2026
- Diretriz aprovada: escala de magnitude **frio (baixo) → quente (alto)**; cores permitem leitura geral sem consulta obrigatória à legenda, que continua indispensável para valores/classes. Sem dado em cor neutra; variações com centro de zero visualmente distinguível; oscilação fria/baixa e quente/alta sem avaliação normativa.
- Parágrafo 'Como interpretar as cores' atualizado na [cópia de trabalho RMRP](https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit) e verificado: 51 tabelas, quatro imagens; nenhum mapa foi recolorido nem o consolidado principal alterado. [Protocolo e critérios de QA](editorial/rmrp/INVENTARIO_16_MAPAS_2026_10_28.md).


### Integração temática ITBI e FPM RMRP — 29/10/2026
- Avanço na [cópia de trabalho cartográfica](https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit): adicionados os mapas de **ITBI principal por habitante** e **FPM por habitante** com legenda completa e escala frio→quente, junto das análises temáticas. Conferência nativa: **51 tabelas, sete imagens**; PDF de prova com 65 páginas, posicionamento de ITBI p. 19, ISS p. 30 e FPM p. 31, cada figura junto de sua legenda textual. A página FPM foi renderizada e inspecionada. Restam nove mapas individuais a integrar, com QA de impressão e eventual correção dos anteriores.
- [Inventário de QA](editorial/rmrp/INVENTARIO_16_MAPAS_2026_10_28.md) atualizado (commit `ca693f4b`). Relatório consolidado original e publicação intactos.


### RMRP — estado consolidado da integração cartográfica e próximos controles — 29/10/2026
- **Documento editável de trabalho (não publicado):** https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit . O documento consolidado de origem permanece preservado, sem alteração. Os registros anteriores do README que mencionam 4, 7 ou 9 mapas descrevem estágios históricos, **não o estado atual**.
- **Estado confirmado após a última intervenção:** 16 de 16 mapas individuais inseridos em seções temáticas, 51 tabelas nativas preservadas e 34 fichas fiscais municipais; última prova exportada em PDF com **74 páginas**. Os mapas não constituem um atlas ao fim do volume. Os mapas de 2025 usam leitura sequencial fria (valor menor) a quente (valor maior); faixas numéricas originais foram recompostas sem recortar a quinta classe. As imagens cartográficas não tiveram seus polígonos recalculados ou efetivamente recoloridos pela base municipal.
- **Revisão editorial executada:** três ocorrências herdadas de “mosaico(s)” substituídas por remissões aos mapas individuais distribuídos nos capítulos. A descrição da participação do investimento na receita corrente foi corrigida: esse indicador consta de tabelas/análises, não de um mapa individual no conjunto de 16. Readback após revisão: zero referências textuais a “mosaico”, 16 imagens e 51 tabelas; exportação manteve 74 páginas. Controle no [inventário cartográfico](editorial/rmrp/INVENTARIO_16_MAPAS_2026_10_28.md), commit `a6cc68c6`.
- **Pendências de homologação:** realizar conferência gráfica sistemática **das 74 páginas**, incluindo legibilidade impressa das 16 legendas, encontro de figura com legenda, eventuais quebras de tabela e páginas pouco aproveitadas; corrigir apenas ocorrências comprovadas e reexportar para QA. Revisar padronização de estilos, numeração, títulos e consistência das 34 fichas antes de tornar público.
- **Pendência metodológica importante no mapa 15:** a classe de variação real de investimentos entre triênios **−10,6% a +16,7%** cruza zero; a cor dessa classe não distingue redução de crescimento. A ressalva consta da legenda textual. Para semântica cromática rigorosa, recuperar valores municipais e geometria vetorial (EPSG:4674), reclassificar com zero como quebra e validar 34 municípios; **não simular reclassificação por recoloração raster**. No mapa 16, tons mais quentes significam maior oscilação, não melhor desempenho.
- **Próxima ação operacional:** concluir auditoria de paginação e legibilidade, registrar resultados por página e intervenção no inventário, gerar nova prova PDF e somente então discutir homologação/publicação. Não considerar a existência de 16 imagens e 74 páginas prova suficiente de acabamento gráfico.

## Continuidade após QA trienal — 29/10/2026
- Leitura independente da fonte canônica DCA (Drive ID 1BtXY_FxydMREEbMACJtaoW2n24ohVH33), cruzada com os 34 códigos IBGE das fichas, confirmou 204 combinações município–ano em 2020–2025.
- Índices IPCA dez/2020–dez/2025 até set/2026 (SIDRA tabela 1737) reproduzem a comparação das médias anuais reais: 15 municípios com alta, 19 com queda; mediana municipal -4,03%. Investimento médio metropolitano +R$ 18,53 milhões/ano; receita corrente +R$ 1.813,45 milhões/ano; despesa corrente +R$ 2.043,85 milhões/ano. Saúde e Educação cresceram nos 34 municípios.
- Dossiê reprodutível: editorial/rmrp/QA_TRIENIOS_2026_10_29.md (commit 265dfe15). Não foram alterados dados, mapas ou versão homologada. Pendente QA da escala do mapa de variação entre triênios e controle gráfico das tabelas.


## RMRP — Revisão editorial da seção 12.2 — 30/10/2026
- **Cópia de trabalho:** Google Docs `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`. Frente de QA: `editorial/rmrp/QA_HIERARQUIA_E_FICHAS_2026_10_30.md`.
- A prova anterior evidenciou título da subseção 12.2 isolado na página 25 e primeira tabela na página 26. A inspeção da API Docs identificou dois parágrafos de legenda, dois separadores vazios e uma tabela nativa.
- **Correção desta rodada, confirmada pela API:** removida a propriedade `pageBreakBefore` do título 12.2 (agora `false`); preservado `keepWithNext=true` no título; removidos os espaçamentos acima/abaixo do primeiro parágrafo separador; ativado `keepWithNext=true` no segundo parágrafo da legenda, de modo a manter a cadeia até a tabela. Aplicado com controle de revisão.
- **Status de prova:** ajuste nativo persistido; a paginação final após essa rodada ainda requer nova exportação e inspeção gráfica independente. Não declarar resolvido nem homologado sem confirmar PDF. Não houve alteração de dados, mapas ou texto fiscal.
- Os números **73 páginas, 52 tabelas nativas e 16 mapas** são referência da última prova analisada, não certificação automática da versão agora editada. Permanecem pendentes a inspeção integral das tabelas e das legendas cartográficas e a homologação.

- **Verificação adicional após a edição (30/10, 12h):** exportação PDF novamente executada; arquivo disponibilizado com **4.063.202 bytes**, 73 páginas. Inspeção local com PyMuPDF constatou que a **página 25 ainda contém apenas o título 12.2 (54 caracteres extraídos)** e que a **página 26 começa pela legenda e tabela**. Logo, **não foi demonstrada correção gráfica**. A API nativa confirma as novas propriedades, mas a exportação apresenta a mesma composição; investigar atualização/cache do exportador ou a interação com a estrutura nativa. Não homologar.


## RMRP — correção homologada da quebra 12.2 — 31/10/2026
- **Defeito resolvido em prova PDF:** o título `12.2 O movimento entre 2023 e 2025 foi disseminado`, a legenda `Tabela 1 – Municípios segundo direção...` e a tabela nativa estão agora na **mesma página 25**.
- Intervenção: exclusão cirúrgica de um caractere separador de parágrafo imediatamente depois do título 12.2 (`deleteContentRange` no índice correspondente, com proteção por revisão); a tentativa anterior de remover integralmente dois parágrafos em lote falhou e não modificou o arquivo. A edição bem-sucedida preservou conteúdo fiscal e estrutura da tabela.
- **Nova prova realmente alterada:** PDF exportado com **4.062.467 bytes e 72 páginas** (a prova precedente tinha 4.063.202 bytes e 73 páginas). PyMuPDF localizou título e legenda da primeira tabela na página 25, com 1.843 caracteres extraídos nessa página: deixou de existir título isolado.
- **Status:** problema gráfico 12.2 encerrado com verificação textual de página e nova exportação. A homologação integral de 52 tabelas e 16 mapas, sobretudo legibilidade de legendas e quebras das fichas, continua pendente. Documento ainda não publicado. Cópia de trabalho Google Docs `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`.


## RMRP — lote de auditoria gráfica, 31/10/2026
- Prova PDF de 72 páginas auditada em lote com PyMuPDF: **16 imagens cartográficas** em páginas temáticas; fichas municipais com tabelas nativas e cabeçalhos repetidos nas continuações. Não confundir as páginas cartográficas pouco textuais com páginas vazias.
- Inspeção de páginas 43, 71 e 72 detectou duas quebras editoriais: orientações de leitura iniciadas na página 43, com continuação na 44; e última ficha municipal, Santo Antônio da Alegria, com somente duas linhas da tabela na penúltima página e restante na última.
- Na cópia Google Docs `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`, aplicadas em lote propriedades `pageBreakBefore=true` aos títulos `ORIENTAÇÕES PARA A LEITURA DAS FICHAS FISCAIS` e `Santo Antônio da Alegria — sub-região 4`, usando controle de revisão.
- **Prova reexportada e confirmada**: **73 páginas**, 16 imagens cartográficas. Orientações inteiras e início da sub-região 1 na página 44; ficha final, com tabela e comentário completos, começa na página 73. Imagens renderizadas das páginas 44 e 73 para inspeção de acabamento. A elevação de 72 para 73 páginas é deliberada para preservar blocos intactos sem reduzir a tipografia.
- Nenhum dado fiscal, comentário municipal, tabela ou mapa foi alterado deliberadamente; mudanças apenas de paginação. Não corresponde à homologação visual exaustiva das 52 tabelas e das 16 legendas impressas. Pendências: inspecionar visualmente todas as tabelas continuadas e os 16 mapas em tamanho de impressão, corrigir anomalias verificadas, registrar QA final antes de publicar.


## RMRP — auditoria gráfica ampliada de 31/10/2026 — 73 páginas
- Fonte examinada: prova PDF mais recente da cópia de trabalho Google Docs `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`. Inspeção programática integral com PyMuPDF e prancha de contato das 16 páginas cartográficas.
- **73 páginas**; **52 tabelas nativas** verificadas no Google Docs; **16 imagens cartográficas raster**, distribuídas nas páginas **5, 7, 10, 14, 16, 17, 19, 30, 31, 33, 34, 35, 36, 37, 38 e 40**. Uma imagem por página listada, sem ausência de figura entre as 16 catalogadas.
- Dimensões das figuras: 15 arquivos 1500 px de largura e mapa 15 (variação real dos investimentos entre triênios) em 2048 px; resolução efetiva em página de **240–332 dpi**. Não foi observada deformação evidente na prancha geral. Todavia o tamanho impresso das legendas, por serem parte das imagens raster, exige conferência ampliada caso a caso: DPI suficiente não comprova legibilidade de fontes pequenas.
- Varredura das fichas municipais, páginas 44–73: tabelas divididas aparecem com cabeçalho de continuação `Indicador | 2023 | 2024 | 2025`; nenhuma ausência de linha foi comprovada nessa análise textual. A divisão em páginas deve ser mantida quando a alternativa criaria espaços em branco excessivos. Não se detectou página final em branco: a ficha de Santo Antônio da Alegria ocupa a página 73.
- **Nenhuma alteração nativa efetuada nesta rodada**, pois não se comprovou defeito específico cuja correção fosse mais segura do que o arranjo existente. Resultado é auditoria ampliada, não homologação visual integral das 52 tabelas.
- Pendência para homologação: inspeção das legendas e dos limites das 16 figuras em escala física de impressão; inspeção focada das tabelas continuadas por página, inclusive alinhamento das linhas e repetição exata dos cabeçalhos. Preservar redação fiscal, 34 fichas e séries DCA. Publicação não autorizada.


## RMRP — lote de QA cartografico e tabelas continuadas (01/11/2026)
- Prova PDF: 73 paginas, 16 figuras em paginas 5, 7, 10, 14, 16, 17, 19, 30, 31, 33, 34, 35, 36, 37, 38 e 40. As imagens conservam 240–332 dpi de resolucao efetiva; foi gerada folha de contato e examinado em escala nativa o mapa da pagina 14, incluindo legenda de classes, intervalos e escala cromatica.
- A legenda do mapa da pagina 14 encontra-se completa (cinco classes e categoria sem dado), sem recorte. Como o mapa impresso ocupa 384,8 pt de largura para imagem de 1500 px, textos de legenda integrados ao raster podem apresentar corpo pequeno em A4; qualidade de resolucao nao equivale automaticamente a legibilidade em papel. Recomenda-se teste de impressao das legendas antes da homologacao de todas as figuras, sem alterar valores ou classificacoes.
- Varredura programatica em todas as paginas das fichas encontrou 29 paginas contendo tabelas municipais com cabecalho `Indicador | 2023 | 2024 | 2025`; em paginas com duas fichas, o cabecalho ocorre duas vezes. A procura por bordas inferiores de texto muito proximas ao limite fisico da pagina nao gerou ocorrencias (limiar de 32 pt). Nenhuma linha foi demonstrada perdida por essa verificacao. A pagina 72 nao contem cabecalho tabular, pois continua comentario municipal da pagina precedente; a ultima ficha com tabela integra a pagina 73.
- Arquivos auxiliares de QA gerados localmente: `rmrp_audit_data.json`, `rmrp_legendas_16.png` e `rmrp_map14_full.png` (nao presumir que estejam persistidos no GitHub/Drive).
- Nenhuma modificacao no Google Docs realizada neste lote: o trabalho foi de verificacao visual e programatica. Permanecem como pendencia a prova impressa das 16 legendas e a conferencia grafica integral de limites/alinhamentos de todas as 52 tabelas. Relatorio ainda nao homologado nem publicado.


## RMRP — homologação técnica consolidada para divulgação digital (01/11/2026)
- **Prova de referência congelada para QA:** `RMRP — Trabalho cartográfico 16 indicadores — 28-10-2026.pdf`, 73 páginas, 4.063.462 bytes, SHA-256 `d52d35bcc2ffc94bc8f55394b1b38862f305db71b15256692fbf92475263812b`. O nome histórico do arquivo não equivale à data da revisão; a versão editorial atual é a consolidada após as intervenções de 31/10.
- Auditoria abrangente em PDF via PyMuPDF: **34 títulos municipais únicos**, distribuição sub-regional **15/6/6/7**, cada ficha contendo exatamente uma ocorrência de cada uma das seis rubricas `Receita corrente nominal`, `Receita tributária nominal`, `Despesa corrente nominal`, `Despesa total nominal`, `Investimento nominal`, `Investimento real, set./2026` (**204 linhas de indicadores identificadas, sem falta ou duplicação**). Cabeçalhos repetidos nas fichas com tabelas continuadas foram reconhecidos e não constituem erro editorial.
- **16 imagens cartográficas presentes**. As auditorias anteriores verificaram DPI e presença das classes e legendas nos arquivos; não foi comprovada supressão, recorte ou deformação. Limitação residual: a prova física impressa em papel não foi realizada; eventual edição impressa requer esse controle próprio.
- **Decisão técnica:** versão **apta ao fechamento para divulgação digital em PDF**, não obstante inspeção impressa integral ainda pendente. As checagens programáticas e as inspeções visuais por amostra não equivalem a perícia visual individual de cada célula de todas as 52 tabelas. Para o escopo de divulgação digital, não existe defeito material conhecido e aberto que justifique reedição das 34 fichas ou reconstrução dos mapas. O status de publicação efetiva permanece **NÃO PUBLICADO**; preparar versão definitiva com nome/data atualizados, conferir hash e registrar destino/URL antes da divulgação.
- **Regra de congelamento:** não reabrir itens encerrados nem modificar dados, análises, gráficos ou paginação sem defeito material novo comprovado. Manter o Google Docs de trabalho `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI` e o original consolidado separados. Próximo passo é a emissão do artefato final identificado e a autorização de publicação; **nenhuma publicação externa foi executada neste fechamento**.

- **Artefato final de conferência emitido localmente:** `RMRP_Financas_Municipais_Relatorio_Analitico_2026-11-01_v1.pdf` (cópia binariamente idêntica à prova homologada, SHA-256 acima); a data de 01/11 identifica o congelamento do arquivo, **não altera a data que aparece na capa**. Não foi enviado ao Drive ou publicado no site.
- **Formato físico apurado com `pdfinfo`: US Letter (612 × 792 pt), não A4.** Isto não impede a divulgação digital, mas uma edição impressa em A4 exige prova própria de escalonamento e legibilidade das legendas.


## RMRP — disponibilização do PDF no Drive e limite de acesso (01/11/2026)
- PDF congelado em 01/11/2026 enviado ao Google Drive: `RMRP_Financas_Municipais_Relatorio_Analitico_2026-11-01_v1.pdf`, ID `1LSQYFzO9N-sxHfBJD4MYqSvIt4dygSFk`, URL `https://drive.google.com/file/d/1LSQYFzO9N-sxHfBJD4MYqSvIt4dygSFk/view?usp=drivesdk`. Upload concluído; metadados conferidos: MIME `application/pdf`, **4.063.462 bytes**, owner da conta conectada, `shared=false` e única permissão registrada `owner`.
- O conector disponível para compartilhamento oferece usuário específico ou domínio da organização; **não permite habilitar acesso público irrestrito** nesta interface. Logo, arquivo disponível no Drive da conta, **AINDA NÃO PUBLICADO PUBLICAMENTE**. Não circular o link como acesso anônimo validado.
- Para publicidade externa, configurar manualmente no Drive `Compartilhar > Acesso geral > Qualquer pessoa com o link > Leitor` (quando permitido pelo administrador), depois verificar abertura sem autenticação. Alternativamente escolher o destino público/editorial para deploy e validar HTTP/PDF/hash. Nenhuma alteração ao site público nem anúncio em redes foi feita.
- Conservar distinção entre homologação para divulgação digital e publicação efetivamente acessível; preservar o documento nativo e as 34 fichas, 52 tabelas e 16 mapas.


## Publicação editorial RMRP no Emdash — 01/11/2026
- Destino editorial confirmado no CMS do Radar Regulatório: coleção `posts`, categoria `estudos-e-analises` (Estudos e Análises, pt-BR). Não existe necessidade de criar nova seção apenas para este relatório.
- **Rascunho editorial efetivamente criado no Emdash e relido**: ID `01M6AN17PNGPDKP3YRHA77H3SG`, slug `financas-rmrp-receitas-investimentos-desigualdades-territoriais-2026`, status `draft`, título `Finanças municipais na Região Metropolitana de Ribeirão Preto: receitas, investimentos e desigualdades territoriais`. Conteúdo: síntese dos resultados, distinção entre comparações 2023/2025 e triênios, metodologia, 16 mapas e 34 fichas, ressalvas e metadados SEO. URL projetada pelo esquema `/posts/{slug}`, **não afirmar que já é pública**.
- PDF homologado 73p identificado no Drive pelo ID `1LSQYFzO9N-sxHfBJD4MYqSvIt4dygSFk`, porém metadados indicaram `shared=false`. A biblioteca do Emdash já contém PDFs (ex.: RMJ), mas a ferramenta MCP `media_upload` requer conteúdo binário como base64, não aceita diretamente referência `file_uri` exportada do Drive; a conexão disponível não fornece publicação de PDF por referência remota. **Não foi anexado PDF da RMRP ao Emdash.**
- **Estado: RASCUNHO, NÃO PUBLICADO.** Gate para publicação: carregar a cópia exata do PDF congelado no Emdash/R2, obter URL pública funcional e validar a resposta HTTP PDF; substituir na matéria o aviso de disponibilização pendente por link público; conferir persistência do vínculo e publicar o item. Não divulgar um link de Drive privado ao leitor. Nenhuma alteração no relatório-fonte nem no conteúdo fiscal.


## RMRP — campanha LinkedIn, agendamentos iniciais — 01/11/2026
- Canal Buffer LinkedIn `6a946366065799be46558e67`, fuso America/Sao_Paulo; verificados 82 posts previamente agendados (novembro/dezembro), preservados.
- Três chamadas metropolitanas criadas com 4 PNG cada, hospedados na biblioteca Emdash; destino comum: https://boletim.radarregulatorio.org/posts/financas-rmrp-receitas-investimentos-desigualdades-territoriais-2026.
- 02/11/2026 01h17: receitas versus investimentos; post Buffer `6ae76efad27d61fd66ff47fe`; status `scheduled`.
- 03/11/2026 07h23: diferenças entre sub-regiões; post Buffer `6ae76efca9b1b4ba58f2977e`; status `scheduled`.
- 04/11/2026 00h43: comparação entre triênios; post Buffer `6ae76efe7c4e555926661ac8`; status `scheduled`.
- **Pendência:** recuperar/validar as 38 minutas restantes (34 municípios e 4 sub-regiões), que não foram localizadas nos arquivos de trabalho acessíveis nesta sessão, antes de agendar. Não afirmar que 41 publicações estão agendadas. Sem publicação imediata; status indica agendamento, não postagem efetiva.


### Campanha LinkedIn RMRP — programação integral confirmada em 01/11/2026
- Canal Buffer LinkedIn `6a946366065799be46558e67`, organização `6a945ebadaf0def1db0ec1ab`, fuso America/Sao_Paulo.
- Arquivos-fonte recuperados de anexos: `Campanha_RMRP_41_chamadas (1).md`, `Campanha_RMRP_41_pautas_controle_EMDASH.xlsx`, `Campanha_RMRP_164_visuais (1).zip`.
- **41 de 41 pautas com status `scheduled` confirmado por nova leitura da fila Buffer**, IDs únicos, **4 imagens cadastradas em cada publicação**; 3 pautas metropolitanas agendadas inicialmente para 02–04/11, 34 municípios e 4 sub-regiões agendados depois para 05/11–12/12/2026.
- Horários distribuídos em janelas previamente definidas, no fuso de Brasília; verificação cruzada final encontrou **zero conflitos em intervalo inferior a 60 minutos** entre as 41 pautas RMRP e os demais agendamentos existentes na fila LinkedIn.
- Todas as pautas usam como destino único `https://boletim.radarregulatorio.org/posts/financas-rmrp-receitas-investimentos-desigualdades-territoriais-2026`.
- **Status `scheduled` não significa `sent`**. Verificar status e URLs reais no Buffer/LinkedIn após cada horário de publicação; planilha de controle Emdash original ainda contém estado anterior aos agendamentos, devendo ser sincronizada futuramente.


### QA de imagens Buffer/Emdash — 01/11/2026
- Canal LinkedIn: 41 pautas em status scheduled; consulta à fila retornou 164 objetos de mídia (4 por pauta), todos image/png; URLs de mídia do endpoint Emdash e sem arquivos locais como origem.
- Biblioteca Emdash: verificação paginada de 156 IDs de mídia distintos do manifesto, 156 encontrados, 156 status ready, sem tamanho zero.
- EXCEÇÃO: primeira pauta metropolitana Buffer `6ae76efad27d61fd66ff47fe`, 02/11 01h17 BRT: originalmente listada com 0 assets e erro `Please update the media URL to be publicly accessible before retrying the post.`; edição reassociou 4 PNGs e restaurou o horário customScheduled; Buffer conserva mensagem de erro, mesmo após readback. Não há evidência conclusiva de resolução. Tentativa de recriação rejeitada por duplicidade; post original preservado.
- Verificação pública HTTP ponta-a-ponta de todos os arquivos não foi concluída: internet do contêiner indisponível, browserless com cota esgotada e ferramentas de navegação não puderam provar status 200 de cada URL. Crawl2AI carregou representação de uma imagem, mas retornou indicador interno de proteção anti-bot; status ready no CMS e mídia cadastrada no Buffer não comprovam que o LinkedIn conseguirá buscar as imagens no instante de envio.
- Recomenda-se validar a primeira publicação em especial no horário previsto, observar status sent/error e a presença real do carrossel no LinkedIn.


### Falhas históricas Buffer LinkedIn — correção e repostagem, 01/11/2026
- Gmail: pesquisa de avisos Buffer identificou pelo menos 13 notificações de falhas no LinkedIn no período 23/10–01/11, em sua maioria com mensagem `Please update the media URL to be publicly accessible before retrying the post` (algumas outras relacionadas a problemas ou timeout no anexo). Também existem avisos antigos para Facebook, fora da fila LinkedIn ativa.
- Buffer: consulta filtrada por status `error` retornou zero, embora os e-mails comprovem erros históricos; originais não podem ser editados com segurança sem identificação de IDs de post, sobretudo os que já saíram da fila.
- **Três republicações da RMJ agendadas e relidas com status scheduled, zero erros, sem anexos quebrados e com linkAttachment nativo à página do estudo**:
  - 02/11 03h13 BRT — cenários fiscais 2027–2030, Buffer `6ae7752ecfdcf9feb714d317`;
  - 03/11 02h28 BRT — ISS/FPM/investimento por habitante, Buffer `6ae77530a9b1b4ba58f4de6c`;
  - 04/11 03h19 BRT — arrecadação versus investimento, Buffer `6ae77532142f545151f04ecc`.
- Nas republicações foram removidas frases que diziam haver imagens anexas e preservadas as análises e referências do e-mail de falha. As republicações não contêm imagens; usam prévia do artigo para evitar repetir falha de CDN.
- RMRP primeira pauta Buffer `6ae76efad27d61fd66ff47fe`: 4 imagens presentes, horário 02/11 01h17 confirmado, mas erro persistente `Please update the media URL ...`; permanece sob risco.
- Limitação: verificações HTTP externas de todas as imagens ainda não concluídas por falha de DNS no contêiner e quota Browserless; 156/156 itens do manifesto Emdash presentes e prontos não substituem teste de fetch por LinkedIn.


### Validação de URLs PNG com Crawl2AI local — 01/11/2026
- Leitura de manifesto `editorial/rmrp/campanha_41_pautas_midia_2026_11_01.json`: 164 referências (156 URLs únicas).
- Execução via MCP Crawl2AI local, `crawl`, `cache_mode=BYPASS`, 6 lotes de 26 URLs: **156/156 retornaram status_code HTTP 200 e Content-Type image/png; zero URLs falharam nesses critérios**.
- O campo `success:false` e a mensagem de proteção anti-bot `Structural: minimal_text, no_content_elements` surgem porque o crawler tenta extrair texto/HTML de imagens PNG; não são evidência de falha HTTP da imagem.
- Validação mede resposta HTTP observada pelo navegador do Crawl2AI, não prova download integral ou ingestão de mídia pelo servidor do LinkedIn. Buffer ainda registra erro residual de mídia no post `6ae76efad27d61fd66ff47fe`; manter acompanhamento e não afirmar resolvido sem confirmação de publicação efetiva.


## NOVO PROJETO — RMRP Volume II: arcabouço fiscal, reforma tributária e cenários 2027–2030 (01/11/2026)
**Plano operacional canônico:** [PLANO_VOLUME_2_ARCABOUCO_CENARIOS_2027_2030_2026_11_01.md](editorial/rmrp/PLANO_VOLUME_2_ARCABOUCO_CENARIOS_2027_2030_2026_11_01.md). **Status:** execução iniciada; não concluída. **Objetivo:** adaptar com rigor o relatório RMJ (77 páginas e 31 elementos gráficos) à RMRP (34 municípios e quatro sub-regiões), valorizando dados já disponíveis na plataforma de finanças municipais.

**Etapas/gates obrigatórios:** E1 leitura integral, fichamento crítico e QA do PDF/modelo RMJ; E2 inventário, acesso e auditoria da plataforma fiscal e reconciliação de cobertura; E3 fontes legais e bibliográficas oficiais; E4 diagnóstico municipal/sub-regional 2013–2025; E5 rastreamento PAC/transferências/investimentos federais; E6 três cenários condicionais 2027–2030; E7 39 SWOT com estratégias; E8 volume diagramado e homologação. **Não pular etapas nem classificar gate concluído sem evidências.**

**Partida verificada:** versão digital RMJ extraída via Crawl2AI, 120.998 caracteres com 9 capítulos, mas leitura analítica integral e QA dos 31 gráficos ainda pendentes; base DCA RMRP 2025 previamente consolidada: receita corrente R$ 11,836 bi, receita tributária R$ 3,011 bi, investimentos R$ 302,30 mi, razão investimento/receita corrente 2,55%; snapshot RGF/RREO incompleto (RCL/pessoal/caixa 26/34) e CAPAG com quatro n.d. Cuidado com escala dos percentuais não certificada. **Próximo passo:** E1 fichamento completo e E2 dicionário/cobertura da plataforma.

**Regras:** LC 200/2023 não implica teto municipal ou corte automático do FPM; separar efeitos da reforma do consumo; diferenciar gasto empenhado, liquidado e pago, receitas principais e agregadas, valores nominais/reais e ausência/zero. Sem percentuais prospectivos inventados. O estudo original RMRP permanece intacto; volume II é artefato separado. Registrar novos avanços tanto aqui quanto no plano canônico.


## RMRP Volume II — lote 09, 01/11/2026
- Avanço da comparação RREO de janeiro–agosto 2025/2026, com três municípios cujos valores individuais estão no Caderno 03: Ribeirão Preto (receita +3,84%; despesa liquidada +11,45%), Sertãozinho (+17,20%; +18,19%) e Barrinha (+17,60%; +14,84%). Rubricas exceto intraorçamentárias, valores nominais; razões entre fluxos não equivalem a saldo fiscal.
- [Caderno 03 atualizado](https://docs.google.com/document/d/18IVXIO-sMrs1KJhnpAO41smjNbkZyRBygpzvJSqdBXk/edit) e [plano canônico atualizado](editorial/rmrp/PLANO_VOLUME_2_ARCABOUCO_CENARIOS_2027_2030_2026_11_01.md). Lote 09 não encerra E2/E4: documento persistido traz somente três casos desagregados; tabela individualizada completa de 30 e QA de modalidades/retificações estão pendentes. Não presumir consulta nova à API ou dados completos de 2026.


## RMRP Volume II — lote 10: auditoria da base da plataforma (01/11/2026)
- Filtro da base estadual canônica `DCA_SP_645_2013_2025_CANONICO.csv` (Drive `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`) por 34 códigos IBGE RMRP: 442/442 pares 2013–2025; reconciliação 2025 aprovada para receitas correntes R$ 11.836.161.388,56, receita tributária R$ 3.010.951.678,78 e investimento liquidado R$ 302.301.895,18.
- Cobertura histórica: receitas correntes 440/442, investimentos 440/442, transferências de capital 432/442, função urbanismo 438/442, saneamento 341/442, transporte 300/442, habitação 84/442. Não converter campos vazios em zero.
- Resultados e detalhamento sub-regional registrados no [Caderno 03](https://docs.google.com/document/d/18IVXIO-sMrs1KJhnpAO41smjNbkZyRBygpzvJSqdBXk/edit) e no [plano canônico](editorial/rmrp/PLANO_VOLUME_2_ARCABOUCO_CENARIOS_2027_2030_2026_11_01.md).
- Interface pública da plataforma não pôde ser lida ao vivo nesta sessão; não confundir recorte da DCA (até 2025) com integração comprovada dos RREO/RGF parciais de 2026 ao frontend. E2/E4 permanecem em andamento; priorizar artefatos já persistidos e QA de versão sem nova consulta externa.


## RMRP Volume II — lote 11, integração multifuentes, 01/11/2026
- Arquivos existentes na plataforma: `FINBRA_SP645_BASE_MULTIFONTES_2025_GATE_C.xlsx` (Drive 12XfaN7ati-wGgw_a5puwechp7ipFdWRG) e `FINBRA_SP645_INDICADORES_2025_GATE_D.xlsx` (Drive 1wYnFB8Dg000qrBM1do8pe083FlqWzHDk). Filtro pelos 34 códigos RMRP: 34/34 linhas no exercício 2025 em ambas as bases.
- RCL, DTP/RCL, caixa pós-RPNP e dívida líquida: 26/34; dívida consolidada: 32/34. Quatro indicadores tributários/de investimento derivados examinados: 34/34. Oito municípios sem RCL/DTP na fotografia; sem imputações.
- Alerta Pontal: percentuais DTP/RCL 805,41 e DCL/RCL 1.333,33 na base integrada, valores NÃO HOMOLOGADOS até exame da escala/demonstrativo. CAPAG da base 2025 (4 n.d.) distinta da prévia set./2026 (1 n.d.): manter versionamento.
- Evidências e limites registrados no [Caderno 03](https://docs.google.com/document/d/18IVXIO-sMrs1KJhnpAO41smjNbkZyRBygpzvJSqdBXk/edit) e no [plano canônico](editorial/rmrp/PLANO_VOLUME_2_ARCABOUCO_CENARIOS_2027_2030_2026_11_01.md). Etapas E2/E4 ainda em andamento. Nenhuma consulta externa executada.


### RMRP Volume II — lote 12: matriz municipal 2025
Matriz de 34 municípios e 19 campos a partir de Gate C/Gate D, sem novas consultas externas: [arquivo versionado](editorial/rmrp/MATRIZ_EXPOSICAO_FISCAL_RMRP_2025_LOTE12.md). Oito lacunas RCL/DTP e anomalia de Pontal identificadas; CAPAG conservada por versão. Etapas E2/E4 ainda não encerradas; conferir [plano canônico](editorial/rmrp/PLANO_VOLUME_2_ARCABOUCO_CENARIOS_2027_2030_2026_11_01.md).


### RMRP Volume II — lote 13: assimetrias fiscais 2025
Distribuições e medianas dos 34 municípios e quatro SRs calculadas a partir da matriz Gate C/D: [análise do lote 13](editorial/rmrp/ANALISE_DESIGUALDADES_FISCAIS_2025_LOTE13.md). Medianas RMRP: tributação 14,20%, FPM 22,93%, investimento 2,33% da receita corrente, investimento per capita R$ 185,11. A SR3 tem maior mediana de FPM (27,77%), sem inferências causais. Nenhuma consulta externa; E2/E4 continuam abertos. [Plano](editorial/rmrp/PLANO_VOLUME_2_ARCABOUCO_CENARIOS_2027_2030_2026_11_01.md).


## Lote 14 — comparacao per capita e padrao monetario (01/11/2026)
- [Protocolo e resultados](editorial/rmrp/PROTOCOLO_PER_CAPITA_PRECOS_SET2026_LOTE14.md) persistidos no GitHub. A partir da DCA estadual existente, 34 municipios, populacao da linha de 2025 total 1.650.449, investimento per capita RMRP R$ 183,16, SR1 R$ 181,83, SR2 R$ 147,01, SR3 R$ 170,90, SR4 R$ 245,92 (valores nominais 2025).
- Metodo: razao dos totais por populacao, nao media de indicadores; valores nominais para conciliacao do mesmo exercicio, valores reais em precos de setembro/2026 para comparacoes 2013–2025. Para fluxos anuais, usar numero-indice de setembro/2026 dividido pela media dos 12 indices mensais do ano. O deflator e seus fatores anuais ainda necessitam recuperacao e QA do acervo. Portanto, nenhum valor real foi inventado neste lote. Para RREO jan-ago, deflacao propria do periodo, sem aplicar fator de ano fechado.
- E2/E4 continuam abertos; prioridade obter fatores IPCA ja existentes, auditar populacao e compor series reais comparaveis.


## Lote 15 — auditoria dos deflatores e base set./2026 (01/11/2026)
- Encontrada no Drive a planilha preexistente `RM_RIBEIRAO_PRETO_IPCA_SET2026.xlsx` (ID `16ssO4FZGm5wGlG9TxGSpN-3yCPsjAMBV`), criada em 19/10/2026: 2013–2025, IPCA setembro/2026 7.695,82, agregados reais e matriz de cobertura. **Status de origem: candidata analítica, não homologada.**
- Conflito de convenção: planilha RMRP deflaciona fluxos anuais por IPCA de dezembro do ano; convenção recente TIC-TIM determina média dos 12 índices mensais do ano. Ambas referências de setembro/2026 não asseguram mesmo valor real. Não declarar a série histórica homologada, preservar planilha original e recuperar médias mensais do acervo.
- Documentação detalhada: [auditoria de deflatores Lote 15](editorial/rmrp/AUDITORIA_DEFLATORES_SET2026_LOTE15.md). Valores nominais 2025 e per capita mantidos; preços reais da candidata permanecem apenas como evidência de trabalho anterior, não nova série aprovada. Sem consultas externas.


## Lote 16 — reconciliacao aritmetica do IPCA (01/11/2026)
- [Analise auditavel](editorial/rmrp/AUDITORIA_IPCA_RECONCILIACAO_2023_2025_LOTE16.md) persistida: receita corrente nominal 2023-2025 +20,505%, real sob indice dezembro +10,250%; investimento nominal -37,663%, real sob indice dezembro -42,968%. Reproduz a convencao da planilha RMRP de 19/10, **nao homologa a convencao dezembro** para fluxos anuais.
- Fatores IPCA dezembro: 2023 1,13620452; 2025 1,03951351, referencia set./2026 7695,82. Acervo de parametros e painel metodologico legado inspecionados, sem recuperacao neste lote de serie mensal integral para calculo das medias anuais. Nao imputar nem inventar fatores; preservar dados nominais, precos de setembro/2026 somente com metodo declarado, e unidades per capita. Nenhuma fonte externa acessada; E2/E4 abertos.


## Lote 17 — recuperacao da serie mensal IPCA e fatores reais (01/11/2026)
- Fonte localizada no acervo: `tabela1737.xlsx`, Google Drive ID `1ZzuDCnZC1X13f51XzsyJ34dH8dDLxp2Z` (SIDRA 1737 ate maio de 2026). Foram extraidos 12 meses por ano, 2013–2025, 156 observacoes, sem ausentes. O indice referencia setembro/2026 7.695,82 foi obtido da planilha RMRP existente, nao do arquivo mensal. Fatores e 13 medias documentados em [lote 17](editorial/rmrp/IPCA_MEDIA_ANUAL_SET2026_LOTE17.md).
- Metodo media anual para fluxos: fator 2023 1,1553290348; 2025 1,0541003834. Crescimento real RMRP 2023–2025 receitas correntes +9,9465%; investimentos liquidados -43,1250%. Anterior metodo dezembro: +10,2500% e -42,9680%, respectivamente. Nao misturar convencoes. Proxima prioridade aplicar fatores a 442 linhas DCA, verificar populacao por exercicio e cobertura. Sem fontes externas.


## Lote 19 — series reais com nomes completos das sub-regioes (01/11/2026)
- Entrega persistida: [series reais anuais 2013–2025](editorial/rmrp/SERIES_REAIS_SUBREGIOES_NOMEADAS_2013_2025_LOTE19.md), 65 registros, para Ribeirão Preto, Jaboticabal, Mococa, Batatais e toda a RMRP. Os nomes completos substituem siglas SR1–SR4 no texto e nos quadros, sem alterar o cadastro territorial.
- Fontes internas: DCA SP645 e tabela IPCA mensal 1737, indice referencial set./2026 7695,82 do acervo. Somente exibidos totais reais com cobertura completa; per capita exige tambem populacao observada para todos. Em 2013 a RMRP possui 33/34 em receitas e investimentos e nao recebeu totais indevidamente integrais. 2025 34/34: receita corrente real R$ 12.476.502.257,70, investimento real R$ 318.656.543,61, investimento real per capita R$ 193,07.
- A persistencia municipal integral de 442 linhas continua pendente (lote 18). O novo arquivo regional NAO deve ser apresentado como prova dessa persistencia. Sem pesquisa externa.


## Lote 20 — QA de Batatais e regra de nomenclatura (01/11/2026)
- [QA cruzado da Sub-região de Batatais](editorial/rmrp/QA_SERIE_BATATAIS_LOTE20.md): 91 observações municipais em 13 anos, sete municípios, 26 reconciliações anuais de receita corrente e investimento com série regional Lote 19. Desvios máximos ~R$ 0,01 por arredondamento; consistência interna aprovada para estas rubricas.
- Em todo novo texto/tabela/gráfico, usar nomes completos **Sub-região de Ribeirão Preto**, **Sub-região de Jaboticabal**, **Sub-região de Mococa** e **Sub-região de Batatais**, não SR1, SR2, SR3, SR4. Arquivos legados com códigos mantidos sem renomeação destrutiva.
- Persistência municipal individual de Ribeirão Preto, Jaboticabal e Mococa continua pendente. A conformidade de Batatais nao prova integridade das demais. Bases nominais preservadas; valores reais IPCA media anual a precos de setembro/2026; per capita para comparacao de portes.


## Lote 25 — séries municipais geradas localmente em 01/11/2026
- Concluída a execução real sobre arquivos arquivados: 156 índices IPCA mensais normalizados; 442 registros únicos, 440 populações disponíveis, sub-regiões de Ribeirão Preto (195), Jaboticabal (78), Mococa (78) e Batatais (91). `validar_rmrp_lote24.py` retornou PASSOU.
- CSVs locais e script foram arquivados como `pacote_series_rmrp_lote25.zip` na conversa atual, com README de fontes, QA e limitações. A conciliação metropolitana de 2025 verificou receita corrente de R$ 12.476.502.257,72 e investimentos de R$ 318.656.543,59 por soma de linhas arredondadas, diferença centesimal frente ao agregado publicado. São dados reais a preços de setembro/2026, com fator por média mensal e população DCA município-ano.
- **Importante:** os arquivos derivados foram persistidos no pacote da conversa, sem comprovação de upload desses quatro CSVs ao GitHub ou ao Drive. Para continuidade além da conversa, importar o ZIP no repositório/Drive, executar QA cruzado exaustivo versus 65 linhas do Lote 19 e revisar referência monetária antes de homologação editorial. Não apresentar a persistência externa como concluída.


## Lote 28 — trajetorias municipais 2015/2019/2023/2025 (01/11/2026)
- Entrega: [matriz de estabilidade de 34 municipios](editorial/rmrp/ESTABILIDADE_PERFIS_FISCAIS_2015_2025_LOTE28.md), commit `a364029225845f2838eb117035f8d1079e81fd9c`. Base DCA SP645 do acervo e cadastro territorial versionado; 136 observacoes completas nas quatro rubricas de receita corrente, receita tributaria, FPM e investimento liquidado.
- Cortes fixos: medianas municipais 2025, tributacao 14,2019% e FPM 22,9286%; 20 municipios mantiveram mesmo quadrante em todos os quatro anos; 11 mudaram entre 2015 e 2025. Participacao tributaria agregada RMRP 20,77% para 25,44%; FPM 11,64% para 12,84%; investimento/receita 3,73% para 2,55%.
- Metodo: razoes de receitas nominais do mesmo exercicio, totais ponderados por montante; para comparacoes de valores monetarios entre anos usar IPCA media mensal e R$ set/2026; quando houver comparacao de porte, per capita. Nomes das quatro sub-regioes sempre por extenso. Proxima tarefa: relacao entre despesa corrente, despesa de pessoal, composicao das receitas e investimento per capita, observando limites de inferencia. Nao inferir cumprimento LRF sem RCL e DTP homologadas.


## Lote 29 — despesas correntes, pessoal e investimento (01/11/2026)
- Entrega persistida: [analise Lote 29](editorial/rmrp/DESPESAS_CORRENTES_PESSOAL_INVESTIMENTOS_LOTE29.md), commit `affee25d68f3a05cbdaa2473f278c2a5e9c89619`. Compara quatro exercicios (2015, 2019, 2023 e 2025) e quatro sub-regioes nomeadas por extenso. Base DCA SP645 canonica, acesso interno arquivado, sem fontes externas novas.
- Agregado RMRP 2025: despesa corrente liquidada/receita corrente bruta 88,93%, pessoal e encargos liquidados/receita corrente 47,37%, investimentos liquidados/receita corrente 2,55%. Ribeirao Preto: 88,87%, 47,78%, 2,54%; Jaboticabal 91,21%, 48,98%, 2,08%; Mococa 85,48%, 44,00%, 2,63%; Batatais 89,27%, 45,50%, 3,08%.
- Atenção: razoes contabeis nao equivalem a DTP/RCL da LRF; Jaboticabal municipio com despesa corrente/receita corrente 102,10% exige investigação, não implica descumprimento legal. Para comparar fluxo monetario entre anos aplicar IPCA media anual a R$ setembro/2026 e por habitante. Proxima fase: investir por habitante versus compromissos correntes, trajetorias 2015–2025, casos ausentes e anomalias legais ja isoladas.


## Lote 30 — trajetorias municipais de despesa e investimento real (01/11/2026)
- [Analise persistida](editorial/rmrp/TRAJETORIAS_DESPESA_INVESTIMENTO_LOTE30.md), commit `c9d5ee95680b83c389fc25fd5faab9146686344c`. DCA canonica 2015/2019/2023/2025; fatores IPCA por media anual do Lote 17, referencia setembro de 2026; denominadores populacionais DCA por municipio-ano.
- Em 2023–2025, quatro municipios combinaram aumento da razao despesa corrente liquidada/receita corrente bruta e recuo do investimento real per capita: Batatais, Orlandia, Dumont, Brodowski. Contrastes: Cravinhos +9,47 p.p. na razao corrente e +71,93% no investimento pc; Jardinopolis -8,02 p.p. e -82,37%; Santa Cruz da Esperanca -9,07 p.p. e -86,72%; Santa Rosa de Viterbo -4,27 p.p. e +42,67%.
- Inferencia estritamente descritiva: ciclo de obras e transferencias de capital devem ser verificados antes de atribuir causalidade. Razao contabil de despesa corrente nao equivale a DTP/RCL legal; sem nova consulta externa. Nomes completos Sub-regiao de Ribeirao Preto, Sub-regiao de Jaboticabal, Sub-regiao de Mococa e Sub-regiao de Batatais em novos textos. Proximo gate: matriz completa de trajetorias e integracao na redacao do Volume II.


## Lote 31 — matriz comparativa 34 municipios (01/11/2026)
- Entrega persistida: [MATRIZ_TRAJETORIAS_MUNICIPAIS_LOTE31](editorial/rmrp/MATRIZ_TRAJETORIAS_MUNICIPAIS_LOTE31.md), commit `d84c696c7bbe248a95de071a627bcdb7d120e934`. Inclui receitas correntes reais pc 2015/2025, razao despesas correntes liquidadas/receitas 2025 e investimentos reais pc 2023/2025, para todos os 34 municipios. Base DCA SP645, cadastro territorial versionado e fatores IPCA media anual para R$ setembro/2026; nenhuma busca externa.
- 34/34 municipios tiveram crescimento de receita real por habitante de 2015 a 2025; 31/34 tiveram retracao de investimento real por habitante de 2023 a 2025. Janelas distintas, sem inferencia causal. Razao despesa corrente/receita corrente nao equivale a DTP/RCL legal. Nomes completos das quatro sub-regioes em todo novo quadro.
- Proximo: incorporar resultados na redacao interpretativa Volume II e elaborar arquitetura de cenarios condicionais 2027–2030; verificar cobertura RCL/DTP e anomalias ja isoladas, sem anualizar 2026 parcial.


### RMRP Lote 32 (01/11/2026)
Síntese interpretativa e cenários condicionais 2027–2030: [documento](editorial/rmrp/SINTESE_VOLUME_II_LOTE32.md), commit `f67542e`. Evidências: 34/34 municípios com crescimento da receita real per capita entre 2015–2025; 31/34 com queda do investimento real per capita entre 2023–2025. Sem causalidade estabelecida nem projeções arbitrárias. Pendentes: carteira de obras, receitas de capital, DTP/RCL e quantificação dos cenários. Preços setembro/2026, sub-regiões nomeadas por extenso. Plano operacional atualizado.


## Lote 33 — matriz auditavel dos cenarios 2027–2030 (01/11/2026)
- Documento persistido: [MATRIZ_PARAMETROS_CENARIOS_LOTE33](editorial/rmrp/MATRIZ_PARAMETROS_CENARIOS_LOTE33.md), commit `fff1e26367f443c162f2a900df71d9d6dba8e8a0`. Modelo com 34 municipios x 2027–2030 x tres cenarios; agregacao posterior nas quatro sub-regioes e na RMRP.
- Entradas: tributacao propria, FPM, ICMS/IPVA, despesas correntes, pessoal, investimentos, capital, caixa/divida, populacao, IPCA, reforma tributaria e instrumentos federais. Cada hipotese requer fonte, vigencia, cobertura e testes de soma; nao foram inseridos choques numericos arbitrarios. Ultimo ano anual consolidado 2025; dados 2026 parciais nao anualizados.
- Gates: E6 matriz de variaveis concluida, cenarios monetarios condicionados a parametros verificaveis; E4 pendencias RGF/RREO/RCL/DTP e Pontal; E5 carteira e fontes de capital pendentes. Proximo lote: dicionario de entradas e esquema tabular de cenarios com controles de cobertura e agregacao.


### Lote 34 — dicionario e controles dos cenarios (01/11/2026)
Especificacao versionada em [Lote 34](editorial/rmrp/DICIONARIO_E_CONTROLES_CENARIOS_LOTE34.md), commit 82039f52. Grade de 408 registros municipio-ano-cenario, 60 agregados sub-regionais e metropolitanos, campos com proveniencia, nulos e regras de soma. Ainda sem projeções numericas homologadas. Proximo lote: materializar grade, auditar 34 municipios e controles de ausencias.


### Lote 35 — grade de cenarios materializada (01/11/2026)
Documento: [GRADE_CENARIOS_LOTE35](editorial/rmrp/GRADE_CENARIOS_LOTE35.md), commit `df452bd`. Execucao real sobre fontes DCA/IPCA/cadastro arquivadas: 408 registros municipais, 60 agregados, 34/34 municipios em seis bases fiscais de 2025; QA de unicidade e conciliacao passou. Gerados arquivos locais CSV, XLSX, ZIP e script. Projecoes futuras permanecem nulas ate parametros auditados; nao anualizar 2026 parcial. Proximo gate: persistir arquivos derivados externamente e integrar RGF/RREO e carteira de investimentos.


### RMRP Lote 36 (01/11/2026)
Auditoria de RGF/RREO, caixa e capital: [relatorio](editorial/rmrp/COBERTURA_RGF_CAPITAL_LOTE36.md). RCL/DTP/caixa 26/34, oito ausentes, doze caixas negativos no snapshot, Pontal em quarentena. Transferencias de capital DCA 33/34, Santa Cruz da Esperanca ausente. Sem imputar zeros ou inferir ilegalidade. Plano de Volume II atualizado.


### Lote 37 — pre-inventario da carteira de investimentos (01/11/2026)
Persistido [PRE_INVENTARIO_CARTEIRA_LOTE37](editorial/rmrp/PRE_INVENTARIO_CARTEIRA_LOTE37.md), commit ca3417a9. DCA 2025: investimentos liquidados 34/34, transferencias de capital 33/34 (ausencia Santa Cruz da Esperanca). Matriz por municipio distingue fluxo de receita, despesa e carteira identificada; **nenhum projeto individual comprovado** na base contábil consultada. Notas Drive de auditoria de receita de capital total lidas; total nao corresponde a soma incompleta de transferencias, alienacoes e operacoes de credito. Proximo: recuperar DCA I-C/crosswalk e localizar instrumentos por identificadores oficiais. Sem fonte externa nova; sem projeção numerica.


### Lote 38 — receitas de capital brutas DCA I-C (01/11/2026)
Fonte nova recuperada no acervo Drive: `RMRP_RECEITA_CAPITAL_BRUTA_IC_2015_2019.xlsx` (ID `1ZddPo59osLV8L7J1pXJsgnmw2GJP_G5x`), conta RO2.0.0.0 e estágio Receitas Brutas Realizadas. Cobertura de 167/170 observacoes (2015–2019); ausencias Cássia dos Coqueiros 2015, Cajuru 2017, Santa Cruz da Esperança 2017. Metodologia e limite em [Lote 38](editorial/rmrp/RECEITA_CAPITAL_BRUTA_2015_2019_LOTE38.md), commit 1d8f577. Ainda sem homologação contábil e sem série 2020–2025 neste arquivo. Próximo: procurar I-C 2020–2025 e instrumentos individualizados. Não usar ausências como zero nem inferir financiamento de investimento.


### Lote 39 — receitas de capital DCA I-C (01/11/2026)
Recuperada no anexo I-C original 2025 a conta sintetica RO2.0.0.0, coluna Receitas Brutas Realizadas, para 34/34 municipios RMRP, total nominal R$ 327.942.785,14. Sub-regiao de Ribeirao Preto R$ 233.092.440,70; Sub-regiao de Jaboticabal R$ 32.712.302,23; Sub-regiao de Mococa R$ 36.523.843,09; Sub-regiao de Batatais R$ 25.614.199,12. Identificados no inventario Drive anexos I-C de 2020–2024, ainda nao extraidos no lote. Documento: [RECEITA_CAPITAL_IC_2025_LOTE39](editorial/rmrp/RECEITA_CAPITAL_IC_2025_LOTE39.md), commit 33bfb24. Valor bruto nao e receita liquida nem disponibilidade de caixa; proximo: extrair 2020–2024, auditar rubrica e reconciliar 2015–2025.


### RMRP Lote 40 — SWOT territoriais preliminares (02/11/2026)
- Entrega: [39 matrizes SWOT fiscais preliminares](editorial/rmrp/SWOT_PRELIMINARES_39_TERRITORIOS_LOTE40.md), com 34 municipios, quatro sub-regioes e RMRP, commit `27f8042437e80e5fe0aa82145f8b65d1e314d2c3`.
- Fontes: matrizes DCA e series reais ja arquivadas, sobretudo Lotes 26, 29, 31–33. Nenhuma extracao de FINBRA/Siconfi e nenhuma pesquisa externa. Dados reais referidos a setembro/2026; per capita segundo denominadores do mesmo ano.
- Resultado: E7 iniciado, 39 quadros preliminares sem homologacao. Forcas e fragilidades usam indicadores observados; oportunidades e ameacas sao condicionais, sem atribuir efeitos municipais automaticos a LC 200/2023. Preservados nulos, limites da cobertura RGF/RREO e anomalias de Pontal.
- Proximo gate: revisao critica individual dos 34 perfis com indicadores de tributacao/FPM e dimensoes qualitativas; evitar argumentos mecanicos; incorporar tabelas, mapas e graficos nas secoes proprias do Volume II. Nao bloquear o desenvolvimento pelo agregado de receitas de capital ainda nao identificado como variavel no catalogo editorial da plataforma; conferir sua presenca no SQLite antes de falar em lacuna da base.


### RMRP Lote 41 — auditoria de persistencia e robustez SWOT (02/11/2026)
- Auditoria registrada em [AUDITORIA_SWOT_OBJETIVIDADE_ROBUSTEZ_LOTE41](editorial/rmrp/AUDITORIA_SWOT_OBJETIVIDADE_ROBUSTEZ_LOTE41.md), commit `fd9677eb3d8af2aa1e7eae6e952859719966a18e`. Persistencia do texto Lote 40 confirmada: 39 matrizes, 34 municipios distintos, README e plano atualizados.
- Teste de repeticao: 34 oportunidades municipais em apenas quatro formulacoes (uma repetida 23 vezes); 34 ameacas em apenas tres (uma repetida 25 vezes). A diversidade numerica dos fatores internos nao demonstra argumentacao individual suficiente. Oportunidades confundem recomendacoes internas com fatores externos; ameacas confundem riscos internos com ameaças externas.
- Parecer: estrutura descritiva aproveitavel, E7 ainda nao homologado; nao publicar como SWOT final. Proximo lote: reelaborar 39 matrizes com composicao tributaria/FPM e indicadores complementares ja arquivados, singularidade municipal e distincao rigorosa entre evidencias, riscos externos e recomendacoes; se fator externo nao documentado, explicitar ausencia. Nenhuma nova extracao externa ou alteracao do arquivo original.


### RMRP Lote 42 — SWOT V2 (02/11/2026)
- Documento persistido: [SWOT_RMRP_V2_EVIDENCIAS_FISCAIS_LOTE42](editorial/rmrp/SWOT_RMRP_V2_EVIDENCIAS_FISCAIS_LOTE42.md), commit `df6f4aeeb5766115b4449cb2282b43c10430c891`; 39 matrizes, 34 municipios.
- Indicadores cruzados: tributacao/receita, FPM/receita, investimentos/receita, despesa corrente/receita e trajeto real per capita; dados preexistentes Lotes 12, 13 e 31. Nenhuma extracao nova.
- SWOT nao homologada: fatores externos sem instrumento comprovado assinalados como nao caracterizados; recomendacoes administrativas separadas. Proxima etapa: investigacao das evidencias externas ja arquivadas e singularidade dos casos.


### RMRP Lote 43 — qualificação das evidências externas SWOT (02/11/2026)
- Auditoria persistida: [QUALIFICACAO_EVIDENCIAS_EXTERNAS_SWOT_LOTE43](editorial/rmrp/QUALIFICACAO_EVIDENCIAS_EXTERNAS_SWOT_LOTE43.md), commit `8d471a80d5ef0e5bc97ee0e0d422f09be3094d43`.
- O pré-inventário financeiro Lote 37 apresenta investimento para 34/34 municípios e transferências de capital para 33/34, mas não atribui instrumentos ou projetos individualizados. A pesquisa nos arquivos de governança e nos documentos fiscais examinados não demonstrou carteira de convênios/obras com IDs municipais; não interpretar como inexistência na plataforma completa.
- Revisão dos quatro perfis sub-regionais e regra de evidências: oportunidades/ameaças externas sem documento individual permanecem não caracterizadas, nunca preenchidas com ações administrativas ou inferências causais; recomendações separadas. E7 ainda não homologado; E5 carteira pendente. Próximo: argumentos municipais próprios e integração às recomendações do Volume II. Sem nova extração fiscal.


### RMRP Lote 44 — recomendacoes fiscais territorializadas (02/11/2026)
- Documento de trabalho persistido: [RECOMENDACOES_TERRITORIALIZADAS_LOTE44](editorial/rmrp/RECOMENDACOES_TERRITORIALIZADAS_LOTE44.md), commit `83e5b9819ba468c05a4955fa1c0e3090fc34c73d`, com 34 casos municipais e sintese sub-regional.
- Utilizados exclusivamente Lotes 12, 13, 31, 42 e 43. Encaminhamentos diferenciados conforme tributacao/receita, FPM/receita, investimento/receita, despesa corrente/receita e variacao real per capita 2023-2025. Nao houve extracao ou pesquisa externa.
- Estado: recomendacoes analiticas preliminares e condicionais, nao propostas normativas homologadas. Projetos e instrumentos de financiamento nao foram imputados. Indicadores legais com ausencias e Pontal sob controle. Proximo: revisao de singularidade dos 34 textos, associacao de instrumentos efetivamente documentados e integracao editorial E8.


### RMRP Lote 45 - revisao municipal (02/11/2026)
Documento: [Revisao interpretativa de 34 municipios](editorial/rmrp/REVISAO_INTERPRETATIVA_34_MUNICIPIOS_LOTE45.md), commit 2579b29. Dados internos Lotes 12, 28 e 31, sem novas extracoes. Os 34 perfis combinam tributacao, FPM, gastos correntes e trajetorias reais de receitas e investimentos. Texto para revisao qualitativa, sem homologacao. Proximo: consolidacao sub-regional e montagem do Volume II.


### RMRP Lote 46 - consolidacao sub-regional e metropolitana (02/11/2026)
- Capitulo integrado: [Desigualdades fiscais e capacidade de investimento](editorial/rmrp/CAPITULO_DESIGUALDADES_FISCAIS_SUBREGIOES_LOTE46.md), commit `d98a7f71f944e4c82e85efdf6e3fbf451bfd7bb4`.
- Bases arquivadas: Lotes 28, 31, 32 e 45 e analise sub-regional de 2025. Quatro sub-regioes e RMRP, distinguindo totais ponderados, medianas e trajetorias municipais. Sem nova extracao fiscal.
- Resultado: redacao analitica candidata ao Volume II; mapa e graficos previstos nas secoes pertinentes, ainda nao produzidos neste lote. Alertas RGF/RREO e Pontal preservados. Proximo passo: Lote 47, integracao SWOT com argumentos territoriais, sem presumir eventos externos sem prova.


### RMRP Lote 47 - integracao editorial de 39 matrizes SWOT (02/11/2026)
- Documento: [Integracao SWOT 39 territorios](editorial/rmrp/INTEGRACAO_SWOT_39_TERRITORIOS_LOTE47.md), commit c13b8b21ae319934f85d92965114a125437e953a.
- Cruzamento concluido entre os Lotes 42 e 45: 34 municipios presentes, quatro sub-regioes e um conjunto metropolitano. Elementos fiscais internos preservados; recomendacoes destacadas; oportunidades e ameacas externas sem documento nao homologadas.
- Articulado com o capitulo Lote 46, sem novas extracoes. E7 segue pendente de homologacao qualitativa e demonstracao de eventos externos. Proximo: Lote 48, articulacao normativa do arcabouco federal e reforma tributaria, com revisao de fontes vigentes; em seguida cenarios Lote 49 e montagem editorial Lote 50.


### RMRP Lote 48 - arcabouco fiscal e reforma tributaria (02/11/2026)
- Capitulo normativo: [Arcabouco e reforma tributaria](editorial/rmrp/ARCABOUCO_FISCAL_REFORMA_TRIBUTARIA_LOTE48.md), commit `44998c2a1be5e6254a5476f66a13ffb8d58b708f`.
- Revisados os objetos juridicos da LC 200/2023, EC 132/2023, LC 214/2025 e LC 227/2026 em fontes oficiais. LC 200 incide diretamente sobre orcamentos da Uniao, sem teto automatico municipal; reforma tributaria requer transicao e parametros por ente antes de projetar impactos.
- Lote 48 documentado como capitulo candidato, ainda sem exegese exaustiva de todos os dispositivos e sem ganhos/perdas municipais quantificados. Nenhuma extracao fiscal. Proximo Lote 49: cenarios 2027-2030 com mecanismos documentados, parametros ausentes sem zeros artificiais.


### RMRP Lote 49 - cenarios condicionais 2027-2030 (02/11/2026)
- Capitulo: [Cenarios condicionais 2027-2030](editorial/rmrp/CENARIOS_CONDICIONAIS_2027_2030_LOTE49.md), commit e7e022314ae7636bc7d5f3feda75b8ecfabbc550.
- Integrados Lotes 33, 35, 46 e 48: tres cenarios nao probabilisticos, unidade municipal 34 x 4 anos x 3 cenarios (408 chaves), 60 chaves agregadas. Sem projecoes monetarias ou parametros arbitrarios.
- QA original da grade do Lote 35 documentado, mas persistencia externa dos CSV, XLSX e script permanece nao comprovada. Nenhuma nova extracao. Proximo: Lote 50 montar Volume II com capitulos, quadros, graficos e mapas nas secoes pertinentes; verificar arquivos antes de afirmar pacote final pronto.


### RMRP Lote 50 - manuscrito integral do Volume II (02/11/2026)
- [Manuscrito integrado Volume II](editorial/rmrp/VOLUME_II_RMRP_MANUSCRITO_INTEGRADO_LOTE50.md), commit `c85d24b5d05cff0984b63814bcd8c6ce0dc641bb`, com quatro partes: diagnostico e desigualdades (Lote 46), SWOT 39 recortes (47), arcabouco fiscal e reforma tributaria (48), cenarios condicionais 2027-2030 (49).
- Montagem editorial real de 100229 caracteres com resumo executivo, roteiro de figuras e mapas nos capitulos e lista de QA. Sem nova coleta fiscal. Os graficos, mapas e a paginacao final ainda NAO foram produzidos e conferidos; nao declarar documento publicado ou homologado.
- Proximo Lote 51: auditoria de coerencia, repeticao, citacoes normativas e qualidade grafo-cartografica, verificacao dos binarios do Lote 35 e montagem da versao revisada para exame externo.


### RMRP Lotes 51A-51B - reconstrucao SWOT sob a transicao tributaria (02/11/2026)
- [39 SWOT reconstruidas](editorial/rmrp/SWOT_TRANSICAO_TRIBUTARIA_ARCABOUCO_RMRP_LOTE51A.md), commit `3ab27862ab6645b95bd9f649ad5cb0213f95d11e`; 34 municipios, quatro sub-regioes e RMRP; fatores internos anteriores mantidos; oportunidades e ameacas reformuladas segundo transicao IBS/ISS, EC 132/2023, LC 214/2025, LC 227/2026 e canais indiretos LC 200/2023. Hipoteses condicionais, sem ganhos ou perdas monetarios inferidos.
- [Segunda montagem do Volume II](editorial/rmrp/VOLUME_II_RMRP_REVISAO_SWOT_LOTE51B.md), commit `e47c4db76474e8fd3b9477c88f593af1e3a55bba`, substitui a Parte II pelas SWOT revisadas. Manuscrito original Lote 50 e Lotes 40-47 preservados.
- Nova fase E7: revisao final de exposicao juridico-economica por municipio, decomposicao de ISS e verificacao das regras de transicao para 2027-2030; quadros ainda candidatos, nao homologados. Figuras e mapas pendentes. Nenhuma extracao fiscal nova.


### RMRP Lote 52 - auditoria da consistencia e utilidade das SWOT (02/11/2026)
- [Relatorio de auditoria](editorial/rmrp/AUDITORIA_SWOT_CONSISTENCIA_UTILIDADE_LOTE52.md), commit 118909a5babe56369c2e65f3d583fe79b6209d56. Conferidas 34 matrizes municipais, quatro sub-regionais e RMRP no Lote 51A; oportunidade 20 textos unicos, ameaca 10, estrategia 16; repeticao substantiva e inferencias ainda genericas.
- PARECER: SWOT E7 NAO HOMOLOGADAS. Indicador tributario total nao substitui ISS nem distribuicao do IBS; transicao normativa geral adequada em arts 127-128 ADCT, mas falta exegese distributiva e mecanismos por municipio. Oportunidades frequentemente sao estrategias internas e ameacas, incertezas analiticas; resposta municipal sem prioridade/responsavel/prazo/produto.
- Proximo: revisar 39 matrizes vinculando fato observado, regra legal, mecanismo, exposicao, grau de confianca e estrategia operacional municipal; preservar Lotes 51A/51B como historico ate substituicao homologada. Sem reextrair FINBRA/DCA.


### RMRP Lotes 53 e 54 - correcao das SWOT (02/11/2026)
- [SWOT corrigidas](editorial/rmrp/SWOT_CORRIGIDAS_EXPOSICAO_IBS_UTILIDADE_MUNICIPAL_LOTE53.md): 39 recortes, 34 fichas municipais; corrigida a inferencia de exposicao IBS pela receita tributaria total. ISS municipal nao conciliado no conjunto documental examinado; exposicao distributiva marcada INDETERMINADA, nunca zero. Participacoes ISS sub-regionais preservadas, sem imputacao municipal.
- [Manuscrito Volume II com SWOT corrigidas](editorial/rmrp/VOLUME_II_RMRP_SWOT_CORRIGIDAS_LOTE54.md), commit 16c9f88129a2798ccf7fb015d537d271d5090cec. Substituida a Parte II da montagem anterior, preservando a versao do Lote 51B.
- SWOT: condicionantes externos reformulados (IBS, distribuicao, programas federais), antigas forcas/fraquezas preservadas, estrategias com area responsavel sugerida, horizonte, produto e indicador. Nao se presumiu corte automatico do FPM ou causalidade da LC 200/2023. Sem nova extracao fiscal.
- **Status E7:** revisao substantiva executada; ainda sem homologacao externa. Pendem ISS municipal conciliado, parametros distributivos IBS, instrumentos de investimento e QA juridico/editorial. Proximo: recuperar ISS na plataforma ja existente e revisar exposicoes municipalmente, sem repetir extracao DCA.


### RMRP Lotes 55-56 — ISS municipal observado e SWOT IBS (02/11/2026)
- Novo documento [SWOT ISS municipal Lote 55](editorial/rmrp/SWOT_ISS_MUNICIPAL_OBSERVADO_LOTE55.md), commit b3122c7c77725e06812ff6a59da02b753a75688f: 34 municipios cruzados por IBGE com o arquivo existente `FINBRA_SP645_BASE_MULTIFONTES_2025_GATE_C.xlsx` no Drive (ID 12XfaN7ati-wGgw_a5puwechp7ipFdWRG). Medido ISS PRINCIPAL/receita corrente de 2025, sem confundir com ISS total, tributacao geral ou ganho/perda IBS. A exposicao liquida IBS segue INDETERMINADA.
- [Volume II atualizado Lote 56](editorial/rmrp/VOLUME_II_RMRP_ISS_SWOT_LOTE56.md), commit caae7a6fb5d14d38cb66b5e86b80e01f7a2e6d9c; Parte II substituida pela analise de ISS observado, versoes anteriores preservadas.
- Prioridades para homologacao: conciliar ISS total versus principal, historicidade ISS, mecanismos distributivos IBS, carteira de projetos e responsabilidades administrativas municipais. Nao houve nova extracao fiscal; a base consultada ja pertencia a plataforma.


### RMRP Lote 57 - ISS principal 2015-2025 (02/11/2026)
- [Serie municipal ISS principal](editorial/rmrp/SERIE_ISS_PRINCIPAL_2015_2025_LOTE57.md), commit 498e75c3c5657cabb12e89b336eb753c8566abb8. A base DCA 645 municipios 2013-2025 ja arquivada no Drive foi lida, sem reextracao. Recorte RMRP 34 x 11 = 374 chaves, 369 observacoes com indicador valido. Cinco lacunas: Brodowski, Pradopolis, Sales Oliveira e Serra Azul (2016); Santa Rita do Passa Quatro (2021).
- Taxas ISS principal/receita corrente por exercicio e evolucao 2015-2025 documentadas, sem confundir principal com ISS total, nem participacao historica com ganho/perda de IBS. ISS total e regras distributivas permanecem pendentes.
- Proximo: Lote 58 - leitura juridica das regras transitórias IBS e sua incidencia condicional, para orientar atualizacao das SWOT. Gate E7 ainda em QA; nenhuma projetacao de efeito liquido.


### RMRP continuidade Lotes 58-59-60A (02/11/2026)
- Lote 58: `editorial/rmrp/MATRIZ_LEGAL_TRANSICAO_DISTRIBUICAO_IBS_LOTE58.md` (mecanismo legal ISS + ICMS 2019-2026 e coeficientes CGIBS).
- Lote 59: `editorial/rmrp/ISS_ICMS_REFERENCIA_SWOT_LOTE59.md` (34 municipios, 238 registros 2019-2025; uma lacuna em Santa Rita do Passa Quatro 2021; nao equivale a receita media legal nem estima ganhos/perdas).
- Lote 60A: `editorial/rmrp/VOLUME_II_RMRP_COMPLEMENTO_IBS_LOTE60A.md` (manuscrito integrado com complemento das SWOT).
- Pendencias: ISS total/acessorios, ano 2026, correcao nominal e parametros IBS, carteira de obras, homologacao fiscal e figuras. Nao foram realizadas novas extracoes DCA.


### RMRP Lotes 61A e 61B - integracao das SWOT (02/11/2026)
- [39 recortes, com 34 fichas municipais consolidadas](editorial/rmrp/SWOT_CONSOLIDADAS_ISS_ICMS_LOTE61A.md), commit e53817fabf3d793be3223329a19f43c828bfc789. Fatores fiscais anteriores preservados e ISS principal e ICMS creditado em 2025 incorporados com ressalvas legais.
- [Manuscrito sem duplicacao da Parte II](editorial/rmrp/VOLUME_II_RMRP_SWOT_INTEGRADAS_LOTE61B.md), commit 859ef10c944899b3d334cd3eec199ea286403d55. Substitui lote 60A na leitura editorial; documentos anteriores preservados.
- QA: 34/34 municipios pareados. Efeito liquido do IBS indeterminado. ISS total/acessorios, 2026, coeficientes oficiais, financiamentos por instrumento, revisao editorial e graficos/mapas continuam pendentes. Nenhuma nova extracao DCA.


### RMRP Lote 62 - auditoria e recomposicao SWOT agregadas (02/11/2026)
- [Auditoria editorial e grafica](editorial/rmrp/AUDITORIA_EDITORIAL_GRAFICA_VOLUME_II_LOTE62.md), commit ead4fa4b1bf794430e0ebbafaaf928637eeca6d9: figuras F1-F6 e M1 nao incorporadas, roteiro ainda a produzir; persistem residuos editoriais e inconsistencias de versao.
- [Cinco SWOT agregadas formais](editorial/rmrp/SWOT_AGREGADAS_RECONSTRUIDAS_LOTE62A.md), commit 416c8e4fbf440800ba5971dc7f418e1d47423681: quatro sub-regioes mais RMRP; integram os 34 municipios do Lote 61A (39 matrizes).
- [Volume II revisto](editorial/rmrp/VOLUME_II_RMRP_SWOT_39_REVISADO_LOTE62B.md), commit a8a0dd71330a862c3abe0ed6c4bac6ed7df3ffdf: integracao das cinco matrizes e nota editorial corrigida. Documento em QA, nao homologado.
- Proximo: verificar figuras previamente existentes no Drive; produzir e conferir F1-F6 com dados ja arquivados, e mapa apenas com geometria oficial validada. Substituir metadados restantes e revisar coerencia normativa, efeito IBS indeterminado e binarios de cenarios.


### RMRP Lote 63 — figuras fiscais inseridas (02/11/2026)
- Três SVG produzidos a partir de indicadores municipais dos Lotes 12 e 31, sem nova extração DCA: `editorial/rmrp/figuras/F2_COMPOSICAO_FISCAL_2025_LOTE63.svg`, `editorial/rmrp/figuras/F3_DISPERSAO_TRIBUTACAO_FPM_2025_LOTE63.svg` (34 municípios), `editorial/rmrp/figuras/F4_INVESTIMENTO_REAL_2023_2025_LOTE63.svg` (oito municípios selecionados, valores reais set./2026).
- Manuscrito atualizado: `editorial/rmrp/VOLUME_II_RMRP_COM_FIGURAS_FISCAIS_LOTE63.md`; imagens vinculadas diretamente nas seções de composição e de investimentos da Parte I. Arquivos SVG e links conferidos por leitura do repositório; QA visual de renderização ainda pendente.
- Próximos: F1 série real sub-regional; F5 fluxo jurídico e F6 cenários; M1 apenas com geometria oficial validada. Nenhuma edição homologada.


### Lote 64 — reuso da cartografia preexistente (02/11/2026)
- Matriz original de 16 mapas do Volume I localizada no Drive (PDF ID 10vbnQ_eBNsSmpWekFrrgJyeyTeNlm3YN); caderno Google Docs de 16 indicadores (ID 19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI) conferido por metadados e leitura textual.
- Inventario com destinacao editorial: `editorial/rmrp/REUSO_CARTOGRAFICO_VOLUME_I_VOLUME_II_LOTE64.md` (commit 3cd813f97bbfa393361eb248447c3706ef199231).
- Manuscrito com referencias cartograficas nos capitulos relevantes: `editorial/rmrp/VOLUME_II_RMRP_REFERENCIAS_CARTOGRAFICAS_LOTE64B.md` (commit c0bc2d8ce6f5d88b4873d3d3e6a357e818052dc6).
- Nao exigir novamente arquivo geométrico do usuario: mapas ja existem. Pendente localizar arquivo vetorial original e QA dos recortes individuais/legendas; referencias externas no Markdown ainda nao sao raster embutido. Evitar mapa tematico ficticio. Mapa 15 do Volume I tem classe que cruza zero.


### Lote 65 (02/11/2026) — 16 imagens cartograficas efetivamente recuperadas
Fonte original PDF Drive ID 10vbnQ_eBNsSmpWekFrrgJyeyTeNlm3YN, quatro mosaicos 3000x2500 pixels em paginas 2/3/6/7. Extraidos os 16 paineis PNG em 1500x1180 pixels, com legendas de cinco classes preservadas e faixa superior de titulos de mosaico removida. Pacote ZIP local da conversa: `RMRP_16_MAPAS_VOLUME_I_RECUPERADOS_LOTE65.zip`, com manifesto e SHA-256. Documento de evidencia: `editorial/rmrp/EXTRACAO_CARTOGRAFICA_VOLUME_I_LOTE65.md` (commit 7cf795d857771be54b79122a4a173cc8d18b974f). Ainda falta transferir PNGs ao armazenamento permanente e testar a diagramacao de cada mapa no Volume II; o PDF original e Google Docs Volume I permanecem intactos. Mapa 15 exige ressalva sobre classe cruzando zero. Nao alegar recuperacao de geometria vetorial.


### Lote 66 — persistencia cartografica (02/11/2026)
Os 16 PNG do Volume I foram depositados em ZIP na Biblioteca `/RMRP/Volume_II/RMRP_16_MAPAS_VOLUME_I_RECUPERADOS_LOTE65.zip` (libfile_60d202d5c9748191ad891fc53d711ae6); oito imagens prioritarias tambem foram depositadas individualmente. Criada prova portatil HTML+8 PNG em ZIP `/RMRP/Volume_II/RMRP_VOLUME_II_PROVA_CARTOGRAFICA_LOTE66.zip` (libfile_61373a1bd2a8819190c6f3d941a93cbe). Evidencia: `editorial/rmrp/PROVA_INTEGRACAO_CARTOGRAFICA_LOTE66.md`, commit 1382cae4a9932cb6edff89d4b9245d4df01d3467. Upload ao Drive bloqueado, Biblioteca utilizada como alternativa efetiva. Integracao plena ao manuscrito paginado, QA de mapas e vetor ainda pendentes; nao tratar prova HTML como edicao final.


### Lote 67 — Caderno cartografico paginado (02/11/2026)
Criado PDF A4 de 9 paginas: `RMRP_VOLUME_II_CADERNO_CARTOGRAFICO_LOTE67.pdf`, oito mapas do Volume I em paginas proprias, titulo, fonte e notas metodologicas. SHA-256 e3c03b68ec4daa76b4972ffe71c2a343e17ff92a08f5306078f096fe96003f0a. Persistido na Biblioteca `/RMRP/Volume_II/RMRP_VOLUME_II_CADERNO_CARTOGRAFICO_LOTE67.pdf` (libfile_6ab5d5e76df0819188f5db26780556d4). PDFInfo confirma 9 paginas; QA visual executado sobre M15. Registro `editorial/rmrp/PROVA_PAGINADA_CARTOGRAFIA_LOTE67.md` (41927837b027e5a1923b06ffb03c2ae069c9b277). Ainda NAO e o Volume II integral nem layout homologado; faltam combinar manuscrito integral e figuras F1, F5, F6, revisar todas as paginas e dados normativos.


### Lote 68 — primeira edicao integrada texto e mapas (02/11/2026)
Manuscrito integral do Lote 64B com oito mapas recuperados do Volume I foi convertido em DOCX editavel e PDF de 54 paginas, com 45 tabelas. Binarios persistidos na Biblioteca em `/RMRP/Volume_II/RMRP_VOLUME_II_INTEGRADO_TEXTO_MAPAS_LOTE68.docx` e `.pdf`. Registro de evidencias: `editorial/rmrp/INTEGRACAO_VOLUME_II_TEXTOS_MAPAS_LOTE68.md` (commit 9f071c5dea9a2d31f5ef05588d36575c6613f69d). QA: render completo e inspecao da pagina 8; sem revisao visual de todas as paginas. F2, F3 e F4 estao no texto como referencias SVG, nao imagens embutidas; F1, F5 e F6 pendentes. Nao homologar.


### Lote 69 (02/11/2026) — Volume II com gráficos e mapas integrados
- Gerados DOCX e PDF, 56 páginas, 45 tabelas e 14 figuras (8 mapas + F1–F6), preservados na Biblioteca `/RMRP/Volume_II/RMRP_VOLUME_II_INTEGRADO_GRAFICOS_MAPAS_LOTE69.{docx,pdf}`.
- Relatório de evidência `editorial/rmrp/INTEGRACAO_GRAFICA_VOLUME_II_LOTE69.md`, commit `a1abf785a8d192b9b3f510798b5ce06c56e87319`.
- F1 é variação real 2015–2025 entre extremos, não série anual. F2–F4 refeitos sobre Lotes 12 e 31; F5–F6 são esquemas qualitativos.
- Renderizados 56 PNG, conferidos panoramicamente; falta QA página a página em 100%, edição final, atualização de referências e homologação jurídico-fiscal. Sem projeção arbitrária de IBS.


### Lote 70 — revisao editorial Volume II (02/11/2026)
Produzidos DOCX e PDF da edicao Lote 70 (57 paginas), a partir do Lote 69, mantendo 45 tabelas, 14 figuras e 39 SWOT. Atualizados metadados e referencias editoriais, adicionadas conclusoes/recomendacoes finais. QA de renderizacao e panorama das 57 paginas, sem homologacao plena. Registro `editorial/rmrp/REVISAO_EDITORIAL_VOLUME_II_LOTE70.md`, commit a41d685e307eb059ceb4e1da23786aafcd523b8d. Tentativa de upload a Biblioteca falhou; binarios entregues nesta conversa, nao alegar persistencia externa. Necessaria revisao de pagina integral e jurimetrica.


### Lote 71 — auditoria das 39 SWOT e revisão editorial (03/11/2026)
- Fonte revista: DOCX integral do Lote 70. Nova edição Lote 71: 55 páginas, 45 tabelas, 14 figuras e 39 SWOT preservadas. A fraqueza de Santa Rosa de Viterbo foi corrigida sem mudar crescimento real observado de 42,67%; mantida lacuna de Santa Rita do Passa Quatro em 2021. 34 notas de controle foram depuradas; metalinguagem de alguns trechos corrigida; sem novas projeções IBS.
- Registro e pendências: `editorial/rmrp/AUDITORIA_SWOT_E_REVISAO_EDITORIAL_LOTE71_2026_11_03.md`, commit `067716b4a726ad3ed48a43e806598cefb33da22b`.
- Artefatos criados nesta conversa: `/mnt/data/RMRP_VOLUME_II_REVISAO_SWOT_LOTE71.docx` e `.pdf`; **persistência na Biblioteca falhou por limite de armazenamento**. Não excluir documentos anteriores sem autorização. QA: render completo de 55 páginas, inspeção panorâmica e detecção automatizada de margens, mas não homologação visual integral ou jurídica. Revisão oficial/legal ainda pendente.


### Lote 72 — Drive Lote71 confirmado e auditoria substantiva (03/11/2026)
DOCX Lote71 gravado no Drive ID `17x7GJ-EBNJTDheYI4iZj73JThS-5bXaR` (2.104.507 bytes), PDF Lote71 ID `1pf2s8WS9mjHyYqhw_LRjO2CGF5aSAisT` (2.167.471 bytes); metadados verificados apos upload, preservando formatos originais. Auditoria direta das 34 SWOT no DOCX: forcas 34 variantes, fraquezas 34, oportunidades 1, ameacas 1, respostas 4, produtos 1; falta individualizacao substantiva das dimensoes externas. Checados textos oficiais LC227/2026 art.116 paragrafos 1, 7 e 8 e LC200/2023 art.1 paragrafo 1 inciso I; sem homologacao integral. Registro `editorial/rmrp/AUDITORIA_INDIVIDUALIZACAO_SWOT_REFERENCIAS_LOTE72_2026_11_03.md` (commit abaa9d455f1b0d35e81fc0a9bd4d1276290b75f2). Correcoes quantitativas e novos cenarios NAO executados. Pendencias juridicas e territoriais especificas mantidas.


### Lote 73 — individualizacao operacional das 34 SWOT (03/11/2026)
Matriz de prioridades municipais criada em `editorial/rmrp/MATRIZ_PRIORIDADES_34_SWOT_LOTE73_2026_11_03.md` (commit `3d9fb6748c751e45a36bf7b389f2b551a37ec0d5`), reconciliando Lotes 12 e 31. Filtros descritivos, nao legais: FPM >=35% (5 cidades); receita tributaria >=25% (3); queda real investimento pc >=60% (9); aumento real investimento pc (3); investimento/receita <1% (7); despesa corrente/receita >=95% (3); demais sem gatilho (14). Categorias sobrepoem-se. Pontal e Santa Rita do Passa Quatro possuem ressalvas especiais de QA. A matriz NAO afirma oportunidade/ameaca local externa provada, perdas IBS, nem causalidade do investimento. Ainda falta colher evidencia municipal de projetos, convenios, fontes e setores antes da revisao final das SWOT. Preservar Lote71 original no Drive.


### Lote 74 — fontes municipais externas das SWOT (03/11/2026)
Dossie piloto com coleta Crawl2AI em quatro municipios (Jardinopolis, Santa Rosa de Viterbo, Sao Simao, Taquaral). Verificadas fontes oficiais municipais sobre equipamentos Novo PAC Saude, dois convenios de obras urbanas (FID/Bairro Paulista), repasses hospitalares e reforma de cozinha piloto. Registro `editorial/rmrp/DOSSIE_FONTES_EXTERNAS_SWOT_LOTE74_2026_11_03.md`, commit `3b90bf1570a66fdad4f8346a82a41a51f0a634fa`. Nao afirmar causalidade sobre DCA nem execucao total sem plano, extrato e liquidacao. Cobertura 4/34, demais 30 pendentes. Lote71 no Drive segue canonico; dossie e sugestao de individualizacao, nao revisao homologada.


### 03/11/2026 — Lotes 75 e 76, evidencia externa das SWOT
- Lote 75: Sales Oliveira, Altinopolis, Jaboticabal e Serra Azul, com paginas oficiais lidas via Crawl2AI. Registro `editorial/rmrp/DOSSIE_FONTES_EXTERNAS_SWOT_LOTE75_2026_11_03.md`, commit `7b24445cb07865599252c779a15b4b79925a618c`.
- Lote 76: Sertaozinho (CAPS Novo PAC R$2,3 mi; praca estadual R$1,136 mi anunciados), Orlandia (40 moradias em licitacao e termo federal), Batatais (Decreto 4.818/2026 de contencao; extracao textual de DO) e Cassia dos Coqueiros (noticia de convenio FID de R$1 mi, ainda sem extrato oficial; screenshot PDF falhou). Registro `editorial/rmrp/DOSSIE_FONTES_EXTERNAS_SWOT_LOTE76_2026_11_03.md`, commit `293f8fde3b07adbf51378fd81b489a1cba2136d4`.
- Cobertura acumulada dos Lotes 74-76: 12/34 municipios com ao menos um indicio externo lido, mas graus de prova distintos; 22 sem dossie. Nao converter anuncio, noticia ou licitacao em execucao, pagamento ou causalidade fiscal. Lote71 permanece referencia no Drive; SWOT nao foram alteradas.


### 03/11/2026 — Lote 77 fontes externas das SWOT
Novo dossie `editorial/rmrp/DOSSIE_FONTES_EXTERNAS_SWOT_LOTE77_2026_11_03.md` (commit `da9ac54489e2cbdcbf3b3da640bf44498c77fad0`): Guariba (Novo PAC escola FNDE, valores de diferentes estagios a reconciliar), Nuporanga (escola e ESF inauguradas segundo prefeitura), Pontal (termos de colaboracao socioassistencial) e Serrana (lei autorizativa de convenio SEMIL/SP-Aguas/DER; assinatura nao provada). Cobertura cumulativa Lotes 74–77: 16/34 com evidencia lida, 18/34 pendentes; isso NAO significa SWOT homologada. Distinguir valores pactuados, repassados, contratados e pagos; sem causalidade fiscal, sem efeito IBS. Lote 71 continua no Drive como edicao de referencia.


### 03/11/2026 — Lote 78, fontes externas SWOT
Dossie `editorial/rmrp/DOSSIE_FONTES_EXTERNAS_SWOT_LOTE78_2026_11_03.md` (commit `ed3a1fc68390a4c4cdefff15ec59aeb6ac741f9f`). Verificadas com Crawl2AI fontes de Dumont (MCMV 20 moradias: R$1700 refere-se a assessoria, nao obra; praca homologada no indice, Fundo Municipal de HIS), Brodowski (Decreto 462/2026 programa habitacional e aporte previsto, ainda sem liquidacao) e Pradopolis (editais PNAB 2026). Cravinhos possui candidato de 40 moradias e contrato de R$5,8 mi em extratos indexados, sem leitura integral da fonte primaria, NAO promovido. Cobertura conservadora acumulada 19/34 com fonte externa municipal lida, 15 pendentes. Sem atribuicao causal ao investimento nem ganho IBS. Volume II Lote71 no Drive continua referencia.


### Lote 79 — primeira passagem completa dos 34 municipios (03/11/2026)
Novo dossie `editorial/rmrp/DOSSIE_FONTES_EXTERNAS_SWOT_LOTE79_2026_11_03.md` (commit `822f7d74d7f3764766955cdafc1656f92c624de7`). Investigados os 15 municipios pendentes com busca + extracao Crawl2AI. Saldo cumulativo Lotes 74–79: 34/34 com candidato documental, sendo 29/34 com ao menos uma fonte institucional/executora diretamente extraida, cinco com fontes oficiais reproduzidas ou indexadas e pendencia de inteiro teor originario (Barrinha, Guatapara, Luis Antonio, Santa Cruz da Esperanca, Cravinhos). Evidencias sobretudo de UBS, habitacao, saneamento, parcerias assistenciais, licitacoes, convênios e contratos. Ressalvas: acordo tecnico Ribeirao Preto/Sao Paulo nao tem repasse; Taiuva apresenta vigencia encerrada em 31/03/2026 e status potencialmente desatualizado; precos estimados de edital nao sao valores contratados/liquidados. Nao declarar SWOT homologadas. Lote 71 permanece base do Volume II no Drive.


### 03/11/2026 — Lotes 80–81, validacao e incorporacao das SWOT
Lote 80 `editorial/rmrp/VALIDACAO_PENDENCIAS_E_CONCILIACAO_LOTE80_2026_11_03.md`, commit `a952c7cc9207a2e9032a2b9fbc654de466dbb81a`: Cravinhos (estimado R$5.820.787,01; contrato R$5.800.787,01), Barrinha (predio odontologico estimado R$793.528,83; homologado R$714.175,95), Santa Cruz da Esperanca (R$13.803,52 corresponde ao aditivo do contrato 027/2026), Guatapara (estimativas sem contrato comprovado), Luis Antonio (adjudicacao do campo de grama sintetica sem execucao comprovada). Todos cinco ainda requerem inteiro teor originario para homologacao completa.
Lote 81 `editorial/rmrp/MATRIZ_INCORPORACAO_SWOT_34_MUNICIPIOS_LOTE81_2026_11_03.md`, commit `6cab8884133f3574332f61851d0c18e72548c96d`: matriz editorial das 34 SWOT, distinguindo fatores externos, acoes municipais internas, grau P1/P2/P3 e diligencias, sem resultados IBS inventados. Copia da matriz no Google Docs `1LrCMYReVdPvHqPdUHnWoFrVy88qBZKBvZwzthpqwtmA`; insercao de texto concluida. A versao Lote 71 no Drive permanece canônica, sem sobrescrita. Proxima etapa: cotejar rubricas fiscais e revisar pontualmente SWOT em nova edicao, apos verificar provas financeiras.
