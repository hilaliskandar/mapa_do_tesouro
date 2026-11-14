# Implantação dos universos administrativos como seleções do painel SP645

**Data:** 14/11/2026. **Branch isolada:** `investimentos-territoriais-sp645-20261111`. **Status:** catálogo e seletor integrados, QA de SQLite e site estático com dados sintéticos aprovado. Validação integral em build privado com dados fiscais reais iniciada no run [43629259658](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43629259658), resultado pendente na criação deste documento. Não houve merge em `main`, alteração de R2, implantação em Pages ou publicação.

## Modelo de seleção

O registro canônico é `municipio.codigo_ibge` com sete dígitos. Foram integradas:
- **16 RA**: `RA_SEADE_01` ... `RA_SEADE_16`, tipologia `regiao_administrativa`; uma RA por município; 645 vínculos.
- **43 RG**: `RG_SEADE_01` ... `RG_SEADE_43`, tipologia `regiao_governo`; uma RG por município; 645 vínculos.
- **9 RM e uma AU**, existentes na versão 2025: 255 vínculos, sem duplicidade dentro desta tipologia; 390 municípios ficam fora.
- **SP_645**, **TIC_TIM_30** e **CIDADES_MEDIAS**, mantidos sem modificação.

**Total catalogado:** 72 universos, sendo 1 estadual + 59 administrativos + 10 metropolitanos/AU + 2 analíticos/de projeto. Essas são **seleções alternativas**: a soma de uma RA com RM/AU pode duplicar municípios e não é uma categoria fiscal adicional.

## Fontes municipais

Camada SEMIL / Seade `Limite_Muncipal_IGC_Seade`, `cod_ibge`, `municipio`, `gid_ra`, `gid_rg`, `ra`, `rg`, consulta estadual sem filtro com 645 registros, `exceededTransferLimit=false`; conferência `returnCountOnly=true` = 645.

- `governance/DIM_SP645_IBGE_RA_RG_SEMIL_SEADE_2026_11_14.csv` (fonte municipal direta)
- `governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv` (concatenação territorial, sem dados eleitorais)
- `governance/DIM_HIERARQUIA_SEADE_RG_RA_GEOMETRIA_2026_11_14.csv` (43 RG associadas a uma RA por geometria)
- `data/catalogs/territorial_universes_sp_2025.yml` (RMs e AU já presentes)
- `data/catalogs/administrative_universes_sp_2026.yml` (novo catálogo com 59 universos e 1.290 vínculos)

O catálogo RA/RG tem referência de **consulta 2026-11-14**; não comprova vigência histórica para cada exercício fiscal. Evitar declarar limites atuais por mera data de consulta.

## Implementação

1. `pipeline/build/build_sp645_private_site.py`: importa o catálogo administrativo adicional pelo importador normalizado `import_universe_catalog`, com controles de chave IBGE e idempotência. Não altera o catálogo legado.
2. `app/static/app.js`: seletor territorial organizado em categorias Estado, projetos, análises, RM, AU, RA e RG, mediante `optgroup` sem injetar nomes em HTML.
3. `deployment/qa_sp645_pages.py`: verifica a presença e a dimensão de cada uma das 16 RA e 43 RG no catálogo efetivamente construído, preservando os 13 universos existentes e os contratos editoriais.
4. `tests/test_administrative_universes_sp645.py`: valida 59 universos, 1.290 relações, 645 códigos únicos, 16+43 coberturas, composição RM/AU, pertencimento RG→RA, carga SQLite repetida sem duplicação, preservação do estado.
5. `tests/test_sp645_ra_rg_static_selection.py`: cria SQLite temporário com observação **sintética rotulada como teste**, importa os catálogos reais e gera um site estático SP + RA + RG, verificando arquivos `metadata.json`, `municipalities.json`, `annual/2025.json` e `municipalities/{ibge}.json`. Não mistura dados sintéticos às fontes públicas.
6. Workflow `.github/workflows/inv-sp645-universe-integration.yml`, run [43629189485](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43629189485) **SUCCESS** (testes, QA e sintaxe JS).
7. Workflow `.github/workflows/inv-sp645-ra-rg-private-preview.yml`: reproduz o build privado com os arquivos fiscais canônicos R2 em branch isolada, exige 72 universos e QA local de todos os mapas e dados; **não publica** em produção. Run [43629259658](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43629259658).

## Critérios de promoção

- Prova da construção integral do site privado com dados fiscais reais e 72 universos.
- Integração ao seletor deve estar acompanhada de arquivos por região, não só etiquetas.
- Comparação dos resultados SP645 e RMRP já existentes antes/depois; nenhuma alteração de valores monetários municipais.
- Controle de número de arquivos e tamanho/tempo de build (59 novos recortes implicam maior custo de cálculos regionais; não ultrapassar limites do CI).
- Validação temporal da composição regional para estudos históricos. A interface deve informar referência atual da classificação e não projetar essa associação para o passado sem regra documental.
- Implantação somente após QA, prévia e autorização operacional; base R2 e publicação permanecem intactas.

## Resultado funcional esperado

O usuário escolhe, por exemplo, `Regiões Administrativas — Seade → RA de Ribeirão Preto`, ou `Regiões de Governo — Seade → RG de Ribeirão Preto`, ou `Regiões Metropolitanas → Região Metropolitana de Ribeirão Preto`. Os três recortes são independentes, com municípios e estatísticas próprias, mas usam a mesma base fiscal IBGE7. Variações de indicadores entre universos refletem mudança de grupo de comparação, não mudança de observações municipais.
