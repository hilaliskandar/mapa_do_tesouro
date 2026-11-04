# Lote 95 — Painel equilibrado de receitas de capital, diligência das cinco lacunas e preparação editorial

**Data:** 04/11/2026. **Situação:** painel longitudinal de 30 municípios construído, verificado e persistido no Google Drive. **Não** há homologação final do Volume II nem revisão dos seus 63 fólios.

## 1. Objetivo e lastro documental

Base de entrada: `RMRP_RECEITAS_CAPITAL_REAL_IPCA_LOTE94.xlsx` produzida no Lote 94, que continha 374 chaves município-ano, 369 registros observados, cinco lacunas, deflação IPCA por **média anual dos números-índice mensais** para reais a preços médios de 2025. A base original foi **preservada sem edição**.

Foram realizadas em 04/11/2026 cinco novas consultas **diretas à API da STN/Siconfi via Crawl2AI** para cada município-ano pendente, sendo examinados tanto DCA Anexo I-C quanto RREO Anexo 01, sexto bimestre. Todas as cinco DCA retornaram registros, mas não a rubrica sintética `RO2.0.0.0.00.0.0` da coluna `Receitas Brutas Realizadas`. Quatro dos RREO consultados não apresentaram receita de capital no retorno; **Cássia dos Coqueiros (2015)** apresentou R$257.239,70 em `ReceitasDeCapital`, coluna `Até o Bimestre (c)`. **Não foi promovido à DCA**, pois pertence a demonstrativo e estágio distintos.

### Consultas originais por município-ano

| Exercício | Município | Código IBGE | DCA I-C | RREO A01 B6 | Decisão |
|---:|---|---|---|---|---|
| 2015 | Cássia dos Coqueiros | 3510906 | 74 itens, sem RO2 | R$257.239,70 de receita de capital | manter DCA NA; registrar valor RREO apenas como controle alternativo |
| 2017 | Cajuru | 3509403 | 77 itens, sem RO2 | sem linha de receita de capital no retorno | manter NA |
| 2017 | Santa Cruz da Esperança | 3546256 | 89 itens, sem RO2 | sem linha de receita de capital no retorno | manter NA |
| 2021 | Santa Rita do Passa Quatro | 3547502 | 118 itens, sem RO2 | sem linha de receita de capital no retorno | manter NA |
| 2022 | Santa Cruz da Esperança | 3546256 | 88 itens, sem RO2 | sem linha de receita de capital no retorno | manter NA |

URLs parametrizadas, por exemplo:
- `https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/dca?an_exercicio=2015&id_ente=3510906&no_anexo=DCA-Anexo%20I-C`
- `https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rreo?an_exercicio=2015&nr_periodo=6&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2001&id_ente=3510906`

Os dez links exatos, município-ano, constam na aba `DILIGENCIA_5_LACUNAS` da planilha. **Ausência de conta não é evidência de zero**.

## 2. Painel longitudinal equilibrado

**Critério:** somente municípios com 11 valores numéricos observados para receita de capital bruta DCA, um para cada exercício de 2015 a 2025. Os códigos dos quatro municípios excluídos exclusivamente da análise longitudinal fixa são:
- Cajuru 3509403;
- Cássia dos Coqueiros 3510906;
- Santa Cruz da Esperança 3546256;
- Santa Rita do Passa Quatro 3547502.

**Resultado:** 30 municípios × 11 anos = **330 registros completos**, sem imputação, preservados os 34 municípios e 374 linhas na base principal. Séries corrigidas por IPCA médio anual em preços médios de 2025. **Amostra fixa não é total metropolitano** e não substitui análise dos 34 municípios em 2024 e 2025.

| Ano | Painel 30, R$ reais médios de 2025 | Soma observada no universo de até 34, R$ reais médios de 2025 |
|---:|---:|---:|
| 2015 | 238.413.532,37 | 246.454.159,78 |
| 2016 | 240.644.188,65 | 247.866.222,57 |
| 2017 | 176.891.227,94 | 182.942.166,08 |
| 2018 | 194.884.539,31 | 203.889.462,17 |
| 2019 | 248.651.579,19 | 259.149.198,80 |
| 2020 | 409.198.822,73 | 422.590.802,28 |
| 2021 | 263.198.982,04 | 266.110.518,65 |
| 2022 | 331.237.133,12 | 338.776.177,34 |
| 2023 | 305.763.958,44 | 319.469.457,20 |
| 2024 | 370.724.349,28 | 382.050.909,44 |
| 2025 | 320.747.898,01 | 327.942.785,14 |

De 2024 a 2025 o painel fixo recuou aproximadamente **13,48%** em valores reais. Para a comparação de 34 municípios, ambos anos de cobertura integral, a queda da série Lote 94 permaneceu aproximadamente **14,16%**. O painel fixo evita efeito de composição, mas exclui quatro municípios. **Não confundir receita de capital bruta com despesa de investimento liquidada.**

## 3. Arquivos gerados e efetivamente persistidos

- **XLSX** com quatro abas (`SERIE_REAL_374`, `PAINEL_EQUILIBRADO_30`, `DILIGENCIA_5_LACUNAS`, `NOTA_INCORPORACAO_VOL_II`): `RMRP_RECEITAS_CAPITAL_PAINEL_EQUILIBRADO_LOTE95.xlsx`, upload **Google Drive confirmado**, ID **1jssZ2QQjXfAoB1nr-ovRUDLq7E4XLJOz**, URL https://docs.google.com/spreadsheets/d/1jssZ2QQjXfAoB1nr-ovRUDLq7E4XLJOz/edit .
- **CSV BR** de resumo anual do painel fixo (11 linhas): `RMRP_PAINEL_30_2015_2025_LOTE95.csv`, upload **Google Drive confirmado**, ID **1jpS_1bK1aRnxuNuJh6gk8eb3DiQizV9O**, URL https://drive.google.com/file/d/1jpS_1bK1aRnxuNuJh6gk8eb3DiQizV9O/view .
- Script reproduzível local: `/mnt/data/RMRP_LOTE95_PAINEL_E_LACUNAS/gerar_lote95.py`.
- QA JSON local: `/mnt/data/RMRP_LOTE95_PAINEL_E_LACUNAS/QA_LOTE95.json`.

**Controles executados:** 34 identificadores, 374 chaves na base principal, 369 registros com receita real, cinco ausências, painel de exatamente 30 municípios em todos os onze anos, 330 linhas completas, 11 agregados anuais. Após uma tentativa inicial de regravar a planilha com fórmulas do lote anterior, o artefato definitivo foi gerado **como livro autônomo de valores auditados**, para não perder caches de fórmulas originais do Lote 94. O XLSX do Lote 94 foi mantido intacto. Portanto, o novo livro traz **valores congelados e URLs de proveniência**, enquanto as **fórmulas de deflação permanecem na planilha original do Lote 94**. O arquivo final de Lote 95 foi aberto em modo leitura após a gravação e as contagens conferidas.

## 4. Indicadores fiscais e decisões editoriais

Continuam válidos e **não saneados** os bloqueios anteriores:
- Pontal: RCL no RGF Q3/2025 **R$13.494.039,69**, contra RCL no RREO B6/2025 **R$209.571.785,24**; percentuais fiscais originais em quarentena.
- Barrinha: DCL/RCL informado no RGF A06 **31,40%**, no A02 **26,62%**.
- Orlândia: DCL/RCL no A06 **-6,59%**, no A02 **-6,55%**.
- Termo FNDE Guariba **959097/2024**: conciliação de desembolsos e pagamentos em CSV oficial ainda pendente, embora contrato 043/2025 e ordem de início estejam documentados.
- QA gráfico de 63 páginas e revisão jurídica e das matrizes SWOT do Volume II não concluídos.

**Deliberação editorial recomendada:** para gráficos de trajetória 2015–2025, preferir série equilibrada de 30 municípios, acompanhada de nota de cobertura. Para cortes 2024–2025, é válido usar os totais dos 34 municípios porque ambos têm cobertura integral. Não substituir a série de investimentos liquidada por receita de capital, nem inserir valores ausentes como zero. A presente nota não produz homologação externa.

## 5. Próximo gate

Completar QA cruzado RGF/RREO para demais municípios e verificar eventual retificação de Pontal/Barrinha/Orlândia; retomar PDF/obra Guariba e conciliação Transferegov; examinar espaço editorial e figuras das 63 páginas do Volume II; finalizar revisão normativa. O corpus fiscal atualizado **está pronto para proposta de incorporação analítica condicionada**, não para edição final sem revisão.
