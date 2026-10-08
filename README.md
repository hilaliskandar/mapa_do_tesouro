# Finanças Municipais SP

Plataforma auditável para ingestão, harmonização, análise e visualização territorial de finanças municipais, com base principal no FINBRA/Siconfi e integração progressiva de DCA, RREO, RGF, CAPAG, população e demais fontes oficiais.

O repositório nasceu do projeto `mapa_do_tesouro`, cuja metodologia e rotinas históricas permanecem como ancestral do núcleo atual. A arquitetura vigente, porém, separa dados, regras analíticas, documentação, build estático e publicação.

## Estado canônico

O baseline público vigente é o universo `TIC_TIM_30`:

- 30 municípios;
- exercícios 2013–2025;
- SQLite canônico;
- 75 objetos técnicos/documentais;
- regra territorial `strict_complete`;
- proveniência por observação;
- frontend `static-first`;
- mapa, séries, comparação, análises temáticas, fontes, cobertura, crosswalk, dicionário e metodologia;
- publicação no Cloudflare Pages;
- preview e produção com QA automatizado.

O universo estadual `SP_645` está em expansão controlada. O Gate B DCA foi concluído para 2013–2025: 645 municípios por exercício, 8.385 município-ano, 26 variáveis e zero issues de normalização. No Gate C, RREO 2025 e CAPAG 2025 já possuem cobertura estadual validada; RGF Anexos 01/05 está em aquisição estadual e o Anexo 02 já possui infraestrutura manual preparada. O baseline público TIC-TIM 30 permanece protegido até a conclusão multifuentes.

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

Consultas dinâmicas e D1 permanecem opcionais; o uso básico do painel não depende de API em runtime.

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

O Gate B DCA estadual está concluído. No Gate C:

- RREO Anexo 03 / RCL 2025: aquisição estadual concluída, com 531/645 valores observados e 114 ausências preservadas;
- CAPAG 2025: snapshot oficial validado em 645/645 municípios;
- RGF Anexos 01/05: carga estadual 2025 em execução, com fallback shardado e QA automático;
- RGF Anexo 02: coletor estadual em formato longo preparado e mantido manual até o encerramento do 01/05.

Depois disso vêm denominadores complementares, recomposição dos indicadores, tipologias, pares e paridade estadual.

O baseline público TIC-TIM 30 permanece como referência de regressão até a aprovação de uma release estadual multifuentes.

## Legado

As rotinas antigas de Streamlit, hierarquia, mapa semântico, normalização e agregações continuam úteis como referência metodológica e de regressão, mas não definem sozinhas a arquitetura de produção atual.
