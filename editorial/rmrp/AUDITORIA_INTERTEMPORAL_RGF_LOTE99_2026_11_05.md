# Lote 99 — Auditoria intertemporal dos RGF de Pontal, Barrinha e Orlândia (2025–2026)

**Data:** 05/11/2026. **Estado:** novas consultas oficiais STN/Siconfi efetivamente executadas e controles tabulares produzidos. **Não** houve retificação identificada que permitisse homologar as inconsistências de 2025. O Volume II do Lote 98 continua preservado em pré-homologação.

## 1. Método de verificação

Consultas diretas ao endpoint público `https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf` por meio de Crawl2AI, com filtros explícitos de `an_exercicio`, `id_ente`, `in_periodicidade`, `nr_periodo`, `co_tipo_demonstrativo`, `no_anexo` e `co_poder=E`. Em Pontal foi utilizado **RGF quadrimestral** (Q); em Barrinha e Orlândia, **RGF Simplificado semestral** (S). Foram examinados Anexos 02 e 06 de cada ciclo quando disponíveis; também preservada a consulta ao RREO Anexo 03, sexto bimestre de 2025, para Pontal.

Não se deve comparar percentuais de DCL sem identificar qual RCL ajustada (para pessoal ou endividamento) foi utilizada como denominador; tampouco tratar divergência entre anexos como prova de irregularidade.

## 2. Pontal: anomalia circunscrita temporalmente, sem retificação comprovada

| Indicador | RGF Q2/2025 | RGF Q3/2025 | RGF Q1/2026 |
|---|---:|---:|---:|
| Receita Corrente Líquida (R$) | 203.662.085,89 | **13.494.039,69** | 212.620.509,32 |
| DTP (R$) | 100.083.934,05 | 108.682.695,50 | 109.163.591,30 |
| DTP/RCL ajustada (%) | 49,14 | **805,41** | 51,35 |
| DCL (R$) | 63.005.269,88 | 179.919.782,20 | 187.765.094,56 |
| DCL/RCL ajustada (%) | 30,94 | **1.333,33** | 88,33 |

No RREO 2025, Anexo 03, 6º bimestre, a RCL dos últimos doze meses foi **R$ 209.571.785,24**. Diferença para o RGF Q3/2025: **R$ 196.077.745,55**; razão aproximada **15,531 vezes**.

A reaparência de RCL em patamar próximo a R$ 200 milhões no RGF Q1/2026 reforça **hipótese de inconsistência no denominador do RGF Q3/2025**, mas não comprova erro material de declaração, a sua causa, nem corresponde a retificação oficial. **A variação da DCL entre períodos também exige investigação específica**, não sendo lícito usar exclusivamente a RCL para “corrigir” seus percentuais.

RGF Q1/2026: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2026&in_periodicidade=Q&nr_periodo=1&co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2006&id_ente=3540200&co_poder=E

RGF Q3/2025: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2025&in_periodicidade=Q&nr_periodo=3&co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2006&id_ente=3540200&co_poder=E

RREO B6/2025: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rreo?an_exercicio=2025&nr_periodo=6&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2003&id_ente=3540200

## 3. Barrinha: inconsistência de 2025 e nova discrepância do valor de DCL em 2026

**2025, S2:** RGF Anexo 02: **DCL R$42.986.801,45**, RCL ajustada para endividamento **R$161.507.819,10**, razão **26,62%**. O Anexo 06 apresenta a **mesma DCL R$42.986.801,45** e a mesma RCL ajustada, mas traz **31,40%** como percentual da DCL. O percentual implicaria denominador de aproximadamente **R$136,90 milhões**, não observado nesses campos. A diferença **não se resolve pela distinção entre RCL para pessoal e para endividamento**, porque os campos ajustados do Anexo 06 são iguais nesse exercício.

**2026, S1:** RGF Anexo 02 declara **dívida consolidada R$19.798.063,50**, deduções **R$19.085.509,85**, **DCL positiva R$712.553,65** e RCL ajustada para endividamento **R$174.203.904,82**, relação **0,41%**. O Anexo 06, entretanto, mostra na linha monetária de DCL **-R$19.085.508,85**, mas apresenta a razão **0,41%**: o percentual coincide com o cálculo do Anexo 02, enquanto o valor monetário simplificado não coincide com a DCL detalhada. A semelhança entre o valor absoluto do campo simplificado e o das deduções do Anexo 02 é notável, mas **não deve ser rotulada como erro de mapeamento específico sem documentação do responsável**.

Portanto, a anomalia é **reiterada em períodos distintos e envolve campos diferentes**: percentual em 2025 e valor nominal em 2026. Não homologar automaticamente o percentual simplificado, nem o valor monetário do Anexo 06.

RGF S1/2026 Anexo 02: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2026&in_periodicidade=S&nr_periodo=1&co_tipo_demonstrativo=RGF%20Simplificado&no_anexo=RGF-Anexo%2002&id_ente=3505609&co_poder=E

RGF S1/2026 Anexo 06: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2026&in_periodicidade=S&nr_periodo=1&co_tipo_demonstrativo=RGF%20Simplificado&no_anexo=RGF-Anexo%2006&id_ente=3505609&co_poder=E

## 4. Orlândia: distinção de denominador em 2025, divergência adicional de numerador em 2026

**2025, S2:** os Anexos 02 e 06 coincidem na DCL **-R$17.264.485,35**, mas informam, respectivamente, **-6,55%** e **-6,59%**. O primeiro percentual corresponde ao cálculo com a **RCL ajustada para endividamento R$263.501.501,04**. O segundo é numericamente compatível com a **RCL ajustada para pessoal R$261.870.013,04**. **Hipótese documental forte:** seleção de denominador diferente entre anexos, sem necessidade de alterar o numerador. Não concluir conformidade do procedimento até verificar a disciplina do modelo fiscal.

**2026, S1:** RGF Anexo 02: dívida consolidada **R$5.752.579,17**, deduções **R$24.518.380,71**, DCL **-R$18.765.801,54**, RCL ajustada para endividamento **R$271.214.292,75**, razão **-6,92%**. Anexo 06 apresenta DCL **-R$24.285.593,30** e razão **-7,49%**, ambos diferentes do Anexo 02; RCL ajustada para endividamento no Anexo 06 **R$271.214.292,75**, RCL ajustada para pessoal **R$269.874.260,75**. As diferenças **não são explicadas integralmente apenas pela escolha do denominador**, pois o numerador declarado diverge. Sem imputação de irregularidade ou valor substitutivo.

RGF S1/2026 Anexo 02: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2026&in_periodicidade=S&nr_periodo=1&co_tipo_demonstrativo=RGF%20Simplificado&no_anexo=RGF-Anexo%2002&id_ente=3534302&co_poder=E

RGF S1/2026 Anexo 06: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2026&in_periodicidade=S&nr_periodo=1&co_tipo_demonstrativo=RGF%20Simplificado&no_anexo=RGF-Anexo%2006&id_ente=3534302&co_poder=E

## 5. Controle tabular e validação

Arquivos efetivamente produzidos na conversa:
- `/mnt/data/RMRP_LOTE99_AUDITORIA/CONTROLE_EXCECOES_RGF_LOTE99.xlsx`: 7 registros com valores originais, 15 URLs oficiais e notas de classificação.
- `/mnt/data/RMRP_LOTE99_AUDITORIA/EXCECOES_RGF_2025_2026_LOTE99.csv`: CSV BR (separador `;`, decimal `,`).
- `/mnt/data/RMRP_LOTE99_AUDITORIA/QA_LOTE99.json`: testes de contagem e reprodução de razões.
- `/mnt/data/RMRP_LOTE99_AUDITORIA/criar_controle.py`: gerador reproduzível.

O XLSX foi aberto após sua geração e verificado quanto ao número de linhas/abas. Os dados provêm de consultas oficiais às APIs e os percentuais derivados foram recalculados independentemente; os campos declarados foram preservados. A planilha usa valores estáticos auditados, sem fórmulas ocultas. **Não há confirmação de upload dos binários ao Drive**; este dossiê GitHub constitui o registro permanente até eventual arquivamento dos artefatos.

## 6. Matriz de pendências de homologação — atualização da decisão

- **Pontal P0:** quarentena mantida, agora com forte controle intertemporal RGF Q2/2025, Q3/2025 e Q1/2026 + RREO B6/2025. Requer declaração retificadora, balanço/relatório municipal publicado e/ou manifestação formal sobre RCL e composição da dívida.
- **Barrinha P0:** não homologar DCL/RCL do A06 para 2025 nem sua DCL nominal S1/2026. Requer documento retificado ou conciliação de contas A02/A06; persistência entre anos reforça a prioridade.
- **Orlândia P1:** 2025 com hipótese de denominador divergente; 2026 com divergência adicional de DCL. Exigir cotejo de versões e metodologia antes de escolha de índice para nota fiscal.
- **Guariba FNDE P0:** não houve nesta rodada download dos arquivos oficiais de desembolsos; permanece pendente conforme Lotes 90, 97 e 98.
- **IBS P0:** não alterada a matriz de restrições de 2019–2026 e coeficientes 2027 (LC 227/2026).
- **Volume II:** não foi editado. Preservada cópia de 66 páginas do Lote 98 até conclusão fiscal e jurídica substantiva.

As divergências identificadas representam **limitações da informação disponível**, não prova automática de descumprimento fiscal ou falha imputável ao gestor municipal.
