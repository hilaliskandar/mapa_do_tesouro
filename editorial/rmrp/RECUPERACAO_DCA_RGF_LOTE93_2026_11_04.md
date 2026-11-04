# Lote 93 — Recuperação de DCA capital 2024 e saneamento do filtro RGF 2025 da RMRP

**Data da diligência:** 04/11/2026. **Estado:** série DCA atualizada com 2 observações recuperadas; 8 RGF oficiais do Executivo recuperados com filtro correto; homologação **parcial** (ver divergências intra-RGF). Mantêm-se intactos o DOCX/PDF do Volume II e as 39 matrizes SWOT. Este dossiê complementa, sem apagar, os Lotes 91 e 92.

## I. Saneamento de duas das sete lacunas de receita de capital (DCA I-C)

**Fonte primária:** API da Secretaria do Tesouro Nacional `https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/dca`. Consultas diretas, filtros `an_exercicio`, `id_ente`, `no_anexo=DCA-Anexo I-C`, seleção da coluna **Receitas Brutas Realizadas** e conta sintética `RO2.0.0.0.00.0.0`.

| Município | IBGE | Ano | Valor observado na API, R$ correntes | Consulta oficial |
|---|---|---:|---:|---|
| Cajuru | 3509403 | 2024 | **1.737.955,48** | https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/dca?an_exercicio=2024&id_ente=3509403&no_anexo=DCA-Anexo%20I-C |
| Morro Agudo | 3531902 | 2024 | **5.955.739,80** | https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/dca?an_exercicio=2024&id_ente=3531902&no_anexo=DCA-Anexo%20I-C |

**Resultado: R$ 7.693.695,28 adicionais** em dados efetivamente localizados. A cobertura de 2024 passa de 32/34 a **34/34**; receita de capital bruta metropolitana de 2024 passa de soma parcial **R$ 356.106.269,27** a total observado **R$ 363.799.964,55**, sem imputações.

A série 2015–2025 passa de 367/374 a **369/374 observações (98,66%)**. Apenas cinco lacunas persistem:
1. Cássia dos Coqueiros (2015);
2. Cajuru (2017);
3. Santa Cruz da Esperança (2017);
4. Santa Rita do Passa Quatro (2021);
5. Santa Cruz da Esperança (2022).

Todos os cinco municípios-anos apresentaram **itens de DCA Anexo I-C na API**, mas não foi encontrada a conta sintética de capital nas respectivas respostas. Logo, **não classificar como declaração ausente nem imputar zero**. A informação disponível limita-se à ausência da *conta* exigida para esta série. Consulta complementar ao **RREO Anexo 01 do 6º bimestre de 2015** para Cássia encontrou `ReceitasDeCapital` com valor **R$ 257.239,70**, estágio “Até o Bimestre (c)” — **não se substituiu a DCA** por dado de outro demonstrativo devido à diferença de declaração, estágio e critério. Fonte RREO: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rreo?an_exercicio=2015&nr_periodo=6&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2001&id_ente=3510906 .

A receita de capital permanece **bruta, nominal, não deflacionada**; não se confunde com receitas de transferências de capital, caixa disponível ou despesa liquidada em investimento. Os valores corrigidos devem ser incorporados aos indicadores editoriais apenas após cotejo de qualidade da série histórica e harmonização monetária.

## II. Correção da parametrização e prova de entregas RGF

**Achado de método:** As consultas do Lote 92 para oito municípios utilizaram `in_periodicidade=Q`, `nr_periodo=3`, `co_tipo_demonstrativo=RGF`. A ausência de respostas nessa combinação **não indicava ausência de declaração**. A inspeção dos **extratos oficiais de entrega** pelo endpoint `extrato_entregas?an_referencia=2025&id_ente=<IBGE>` recuperou registros de 2025 para todos os oito municípios. Em todos, o Executivo declarou **“Relatório de Gestão Fiscal Simplificado”**, periodicidade **S**, período **2** (2º semestre), tipo **S**. **Barrinha e Pitangueiras** possuem status de última declaração **RE (retificado)**; os demais constam com **HO (homologado)**.

Filtro reproduzível da extração:
```
https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2025&in_periodicidade=S&nr_periodo=2&co_tipo_demonstrativo=RGF%20Simplificado&no_anexo=RGF-Anexo%2006&id_ente=CODIGO_IBGE&co_poder=E
```

**Extração completa dos oito RGF Anexo 06**, todos com 22 ou 23 registros retornados para o filtro específico:

| Município | IBGE | Status da entrega | RCL, R$ | DTP/RCL ajustada, % (Anexo 06) | DCL/RCL ajustada, % (Anexo 06) |
|---|---|---|---:|---:|---:|
| Barrinha | 3505609 | RE | 163.137.716,10 | 50,38 | **31,40** |
| Guariba | 3518602 | HO | 201.175.390,31 | 47,39 | -12,42 |
| Nuporanga | 3533601 | HO | 68.317.277,84 | 43,83 | 3,22 |
| Orlândia | 3534302 | HO | 263.831.501,04 | 53,38 | **-6,59** |
| Pitangueiras | 3539509 | RE | 207.274.329,72 | 48,82 | 15,23 |
| Sales Oliveira | 3544905 | HO | 80.049.794,62 | 41,16 | -1,10 |
| Taiúva | 3553203 | HO | 43.328.146,44 | 42,39 | -15,25 |
| Taquaral | 3553658 | HO | 29.796.666,44 | 46,29 | -34,75 |

**Status de entrega não significa homologação analítica da qualidade dos indicadores**; o uso jurídico dos valores depende da consistência dos conceitos e do exame dos anexos detalhados.

## III. Controle de consistência entre Anexos 02 e 06

Além do Anexo 06, foram **efetivamente consultados os oito RGF Anexos 02** (Dívida Consolidada Líquida), com os mesmos filtros (apenas `no_anexo=RGF-Anexo%2002`). Resultados:

| Município | DCL/RCL no Anexo 06 (%) | DCL/RCL no Anexo 02 (%) | Resultado |
|---|---:|---:|---|
| Barrinha | **31,40** | **26,62** | **Divergência material de 4,78 p.p.** |
| Guariba | -12,42 | -12,42 | Coincide |
| Nuporanga | 3,22 | 3,22 | Coincide |
| Orlândia | **-6,59** | **-6,55** | Divergência de 0,04 p.p. |
| Pitangueiras | 15,23 | 15,23 | Coincide |
| Sales Oliveira | -1,10 | -1,10 | Coincide |
| Taiúva | -15,25 | -15,25 | Coincide |
| Taquaral | -34,75 | -34,75 | Coincide |

Em **Barrinha**, o Anexo 02 declara DCL de **R$ 42.986.801,45** e RCL ajustada para endividamento de **R$ 161.507.819,10**. A razão aritmética corresponde a **26,62%**, enquanto o Anexo 06 declara **31,40%**. Trata-se de inconsistência **interna aos dados oficiais de RGF simplificado**, a esclarecer antes do uso legal dos percentuais de dívida.

Em **Orlândia**, a dívida líquida de **-R$ 17.264.485,35**, frente à RCL ajustada para endividamento de **R$ 263.501.501,04**, produz **-6,55%**, valor apresentado no Anexo 02; o Anexo 06 apresenta -6,59%, diferença pequena, mas além de arredondamento usual a duas casas. **Não promover nenhum dos dois a “valor corrigido” sem confirmação de retificação**.

Os DTP/RCL dos oito municípios são percentuais reportados nos Anexos 06; a presente rodada realizou conferência cruzada específica da dívida, não reauditoria integral de RGF Anexo 01, RREO e limites legais. Por isso, a cobertura documental passou de 26/34 para **34/34 municípios**, mas **não equivale à homologação jurídico-fiscal dos 34**.

## IV. Pontal — status de entrega e quarentena preservados

O extrato de 2025 de Pontal comprova três entregas de RGF padrão quadrimestral do Executivo, com a última do 3º quadrimestre **homologada em 03/04/2026**; a entrega do 2º quadrimestre também foi homologada em 03/04/2026. Isso ajuda a delimitar a procedência declaratória, mas **não resolve** o conflito entre RCL do RGF Q3 (**R$ 13.494.039,69**) e RREO B6 (**R$ 209.571.785,24**), constatado no Lote 92, com diferença de **R$ 196.077.745,55**. Não há neste lote ato de retificação posterior ou justificativa contábil capaz de homologar os índices 805,41%, 1.283,88%, 1.333,33%. **Pontal permanece em quarentena para comparações legais**.

## V. Artefatos gerados, cálculos e persistência

A planilha original do Lote 92 foi utilizada **sem regressão** como origem de uma edição nova, não substituída in-place. O Lote 93 atualizou somente as duas linhas de 2024, ajustou os controles de cobertura e lacunas, manteve as 374 chaves e os percentuais/anomalias de Pontal, e acrescentou a aba `RGF_8_RECUPERADOS` com as URLs das fontes e confronto entre anexos, além da aba `DCA_5_SEM_CONTA`.

- **XLSX auditado** (upload Google Drive confirmado): https://docs.google.com/spreadsheets/d/1OUjD12f46k7EZQ44FCyNLb-GhesCbUk7/edit , ID `1OUjD12f46k7EZQ44FCyNLb-GhesCbUk7`.
- **CSV 374 registros atualizado** (upload confirmado): https://drive.google.com/file/d/1jWcg13QoBFIsydkAaIDcPTF-twp6xNSq/view , ID `1jWcg13QoBFIsydkAaIDcPTF-twp6xNSq`.
- **QA JSON local**: `/mnt/data/RMRP_LOTE93_SICONFI_RGF_DCA/QA_LOTE93.json`; não declarar hospedagem remota até validação.
- **Gerador local**: `/mnt/data/atualizar_lote93.py`; a trilha de execução está documentada aqui.

A planilha preserva fórmulas de cobertura. Como `openpyxl` não recalcula fórmulas automaticamente, foi gravado o cache numérico de resultados validados após reconstruir os dados; conferência `data_only`: **2024 C11=34, D11=0, E11=R$ 363.799.964,55**, totais C13=369, D13=5. Foram conferidos os oito registros e URLs dos demonstrativos. Fórmulas de Pontal tiveram valores de cache recompostos. Ao abrir em Excel, o mecanismo nativo pode recalcular as fórmulas; permanecem preservadas.

## VI. Gates restantes para homologação

1. Conferir os cinco municípios-anos cujo Anexo I-C existe, mas não inclui a conta sintética de receitas de capital; em especial, validar inconsistência entre RREO e DCA de Cássia 2015, sem simplesmente transportar RREO à série.
2. Auditar RGF Anexos 01, 02 e 06 dos demais municípios, confrontar RREO e verificar duas inconsistências (Barrinha e Orlândia) antes de interpretações legais; manter Pontal isolado.
3. Deflacionar valores da série de receitas de capital em todos os anos com a **convenção IPCA média mensal anual** aplicada aos fluxos do Volume II, distinguindo a convenção IPCA dezembro para o mapa 15.
4. Concluir conciliação FNDE 959097/2024 de Guariba com CSVs oficiais, ainda pendente por falha anterior de download binário.
5. Finalizar inspeção visual individual das 63 páginas e revisão jurídica, mantendo a versão atual do Volume II em **pré-homologação**.

**Conclusão:** sete lacunas DCA reduziram-se a cinco e a cobertura documental dos oito RGF foi saneada. A extração anterior falhava por **filtros incompatíveis com a modalidade simplificada semestral**, não por ausência de declarações. Persistem divergências legais/contábeis que exigem cautela.
