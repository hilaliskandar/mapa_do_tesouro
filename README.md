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
