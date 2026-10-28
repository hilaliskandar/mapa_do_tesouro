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
