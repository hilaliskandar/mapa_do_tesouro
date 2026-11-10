# FED04 — Investigação da divergência FNDE × DCA por exercício de referência e de recebimento

**Data:** 10/11/2026. **Escopo:** 645 municípios de São Paulo, complementação federal ao Fundeb, com referências de 2024 e DCA 2025. **Status:** conciliação de identidade municipal e aprofundamento documental; sem equivalência monetária ou de caixa homologada. Não houve escrita no banco fiscal publicado.

## 1. Problema original

A matriz estadual [`FED04_MATRIZ_MUNICIPAL_FNDE_DCA_FUNDEB_2025_SP645_2026_11_10.csv`](FED04_MATRIZ_MUNICIPAL_FNDE_DCA_FUNDEB_2025_SP645_2026_11_10.csv) foi efetivamente construída com **645 códigos IBGE7**, unindo a matriz DCA 2025 [preservada no Google Drive](https://drive.google.com/file/d/1Tik1vEa5tSIIHp0GLPEjgJi_M6HUdP_d/view) às listas FNDE VAAT/VAAR da sexta publicação do Fundeb 2025 (Portaria MEC/MF nº 5/2026). Classificação: **156 em ambas**, **297 apenas DCA**, **16 apenas FNDE**, **176 sem positivo nas fontes selecionadas**. Os 297 respondem por **R$ 265.487.655,96** em receitas brutas DCA da conta `RO1.7.1.5.00.0.0`. A conta só foi considerada quando na coluna `Receitas Brutas Realizadas` e com valor positivo; linhas ausentes não foram imputadas como zero.

O recorte dos 297 está materializado integralmente em [`FED04_297_CASOS_DCA_SEM_FNDE_2025_COM_RECLASSIFICACAO_2024_2026_11_10.csv`](FED04_297_CASOS_DCA_SEM_FNDE_2025_COM_RECLASSIFICACAO_2024_2026_11_10.csv): IBGE7, município, valor DCA 2025, presença/ausência de beneficiário FNDE nos exercícios de referência 2024 e 2025, prioridade de auditoria e fonte.

## 2. Nova fonte oficial primária para a conciliação intertemporal

[FNDE: Fundeb 2024 — Portaria MEC/MF nº 3, de 28/04/2025, ajuste de contas do exercício 2024](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2024-1). Dois arquivos Excel obtidos e inspecionados na [execução GitHub Actions 42844304196](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42844304196), com as colunas `UF`, `Ente Federado`, `Código IBGE`, valor devido, valor distribuído e ajuste:

- [VAAR — ajuste 2024](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2025-1/AjustedaComplementaoVAAR.xlsx/@@download/file), SHA-256 `9032b5d115409210c160890f7b56b1d56952caa19c1b4db9636a194d38105593`: **149 municípios paulistas com valor devido ou distribuído positivo**. A linha da **rede estadual `UF=SP, código IBGE=35`** também existe, mas foi **corretamente excluída** do universo de 645 municípios.
- [VAAT — ajuste 2024](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2025-1/AjustedaComplementaoVAAT.xlsx/@@download/file), SHA-256 `01546c827401504d2865abd688c7b7ad0c4`: **11 municípios paulistas com valores positivos**.
- A união de municípios beneficiários das duas modalidades **em 2024**, conforme esses arquivos, é de **158 códigos municipais únicos**, sem interpretação da rede estadual como município.
- **Cuidado:** o FNDE publicou em **2025 ajustes referentes a 2024**. O valor do ajuste pode ser positivo ou negativo e não se equipara à receita total realizada em 2025. O FNDE também informa cronogramas com **13 parcelas de janeiro de 2025 a janeiro de 2026 para o exercício 2025**, confirmando que exercício de referência e ano civil dos fluxos não são necessariamente idênticos: [comunicado oficial de 2025](https://www.gov.br/fnde/pt-br/assuntos/noticias/fundeb-ultrapassara-r-325-bilhoes-em-2025).

## 3. Resultado do cruzamento 2024 ↔ 2025

Cruzaram-se os **297 municípios apenas DCA em 2025** com os beneficiários municipais nos ajustes FNDE referentes ao exercício **2024**, usando somente IBGE7 como chave e preservando os valores da DCA **sem substituição**.

| Estrato dentro dos 297 | Municípios | Valor bruto declarado na DCA 2025 |
|---|---:|---:|
| **Com benefício VAAT e/ou VAAR 2024 no FNDE** | **106** | **R$ 200.133.696,95** |
| **Sem correspondência encontrada no FNDE 2024 nem 2025 para VAAT/VAAR** | **191** | **R$ 65.353.959,01** |
| **Total inicial** | **297** | **R$ 265.487.655,96** |

A reclassificação **identificou antecedente documental em 106 casos** e cobriu **75,38% do valor DCA antes sem relação documental com 2025**. A coocorrência de benefício em 2024 e receita em 2025 é **consistente com a possibilidade de fluxos entre exercícios**, mas **não demonstra que a receita DCA de 2025 corresponde a uma parcela de 2024**. O cruzamento entre os 297 e as listas específicas 2024 encontrou **103 com VAAR e 4 com VAAT**, com sobreposição de um município entre essas modalidades (união 106).

Para investigação subsequente, a ordem de trabalho é: (P1) os **191 municípios ainda sem correspondência** nos dois exercícios, (P2) confirmação do fluxo financeiro dos **106 com antecedente 2024**, (P3) 16 registros FNDE 2025 com linha DCA ausente, sem supor receita zero.

## 4. Casos-sentinela e sinais de diferença de período ou rubrica

| Município | DCA 2024 | DCA 2025 | FNDE VAAR 2024: ajuste publicado em 2025 | Observação |
|---|---:|---:|---:|---|
| **São Paulo (3550308)** | R$ 150.278.714,33 | **R$ 117.028.677,98** | R$ 3.407.596,68 | Presença no VAAR 2024, ausência dos beneficiários VAAT/VAAR 2025 na publicação final estudada |
| **Guarulhos (3518800)** | R$ 24.044.021,29 | **R$ 14.329.462,45** | R$ 393.878,83 | Mesmo perfil de antecedente VAAR 2024 |
| **Araçatuba (3502804)** | R$ 3.606.329,40 | **R$ 1.540.109,59** | R$ 62.413,13 | VAAR 2024 verificado |
| **Adamantina (3500105)** | R$ 284.312,16 | **R$ 196.800,92** | R$ 4.534,67 | VAAR 2024 verificado |
| **Americana (3501608)** | Rubrica não localizada na consulta | **R$ 205.810,89** | Não identificada | Mantém-se sem correspondência 2024/2025 nesses anexos, exige apuração |

DCA 2024/2025 extraída pontualmente da API oficial [SICONFI Anexo I-C](https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio=2025&no_anexo=DCA-Anexo%20I-C&id_ente=3550308), com retorno `hasMore=false`. Valores de ajuste devidos/distribuídos extraídos diretamente do XLSX oficial. **A discrepância entre valor total da receita DCA e ajuste anual isolado mostra por que este último não pode ser usado como substituto.**

**São Paulo: confronto adicional com demonstrativo municipal independente.** O [RREO — Anexo 8, 6º bimestre de 2025, divulgado pela Prefeitura](https://prefeitura.sp.gov.br/documents/d/fazenda/demonstrativo_mde_6bim_2025_anexo_8_rreo_v2) registra receita realizada de complementação VAAR de **R$ 84.813.833,88**, sem valores realizados nas modalidades VAAT e VAAF. A rubrica da DCA 2025 registra **R$ 117.028.677,98**. O diferencial simples é **R$ 32.214.844,10**, que **precisa de reconciliação de classificação e competência**, sem ser rotulado como lançamento irregular. Esses valores não são necessariamente contas e estágios idênticos; nunca impor igualdade automaticamente. São Paulo e Guarulhos juntos representam **49,48% do valor** dos 297 casos sem correspondência nos anexos FNDE 2025.

## 5. Tratamento dos 16 casos inversos

A matriz SP645 registra **16 municípios com registro positivo FNDE 2025, mas sem linha de receita bruta na conta específica DCA**, não «receita zero». São 15 casos presentes no VAAR e um no VAAT (Barra do Chapéu). Todos mantêm `estado_dca=linha_ausente` na matriz; a possível razão deve ser avaliada por outro demonstrativo municipal, estágio contábil, data de recebimento e eventual declaração retificadora. Esses 16 casos ficam classificados para verificação dirigida, **sem imputação**.

## 6. Recomendação de operacionalização

1. Para cada município, preservar a **série de receita DCA por exercício civil** separada da **série FNDE por exercício de referência e modalidade (VAAF/VAAT/VAAR)**.
2. Persistir futuros eventos de pagamento com ao menos `codigo_ibge`, `ano_referencia_fundeb`, `competencia_pagamento`, `modalidade`, `valor`, `fonte`, `versao_publicacao` e `tipo_evento` (cota, ajuste, retenção etc.).
3. Construir um de-para estritamente auditado entre somatórios de pagamentos **realizados no ano de 2025**, inclusive parcelas relativas a 2024, e o lançamento da DCA 2025; separar receita bruta, líquida e deduções.
4. Não usar apenas o ajuste anual do FNDE como prova da origem do valor DCA, nem comparar modalidades previstas com receita contábil realizada sem verificar caixa e reconhecimento.
5. Priorizar a investigação dos **191 sem correspondência** e os **16 inversos**, mantendo os **106 com antecedente 2024** sob estado `antecedente_documental_2024_confirmado_fluxo_2025_a_conciliar`.
6. **Nenhuma alteração nos dados canônicos, R2, SQLite, APIs ou painel público**; [PR #232](https://github.com/hilaliskandar/mapa_do_tesouro/pull/232) permanece rascunho. O gate FED04 segue `in_progress`.

## 7. Reprodutibilidade

- Código de verificação FNDE 2024: [`pipeline/qa/probe_fnde_2024_adjustments.py`](https://github.com/hilaliskandar/mapa_do_tesouro/blob/fed04-catalog-safety-20261110/pipeline/qa/probe_fnde_2024_adjustments.py), com [workflow](https://github.com/hilaliskandar/mapa_do_tesouro/blob/fed04-catalog-safety-20261110/.github/workflows/fed04-fnde-2024-ajustes-qa.yml).
- [Execução aprovada 42844304196](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42844304196), com validação de **297 = 106 + 191** e **R$ 265.487.655,96 = R$ 200.133.696,95 + R$ 65.353.959,01**.
- [Tabela individual de 297 casos reclassificados](FED04_297_CASOS_DCA_SEM_FNDE_2025_COM_RECLASSIFICACAO_2024_2026_11_10.csv), com 297 chaves únicas persistidas e conferidas; [matriz completa SP645](FED04_MATRIZ_MUNICIPAL_FNDE_DCA_FUNDEB_2025_SP645_2026_11_10.csv).
