# Fechamento G1 — Auditoria quantitativa da receita de capital e do deflator IPCA da RMRP

**Corte:** 05/11/2026. **Gate:** G1 do plano de fechamento, execução da **primeira frente quantitativa (DCA/IPCA/painel 30 e cotejo editorial dirigido)**. **Situação:** esta frente foi validada após recuperação do cache de fórmulas em **cópia separada**; o G1 integral permanece aberto para os demais indicadores do Volume II.

## 1. Arquivos efetivamente utilizados

- `/mnt/data/RMRP_LOTE94_DEFLATOR_QA/RMRP_RECEITAS_CAPITAL_REAL_IPCA_LOTE94.xlsx` — original do Lote 94 com 12 abas e **1.278 fórmulas**. **Preservado byte a byte**.
- `/mnt/data/RMRP_LOTE95_PAINEL_E_LACUNAS/RMRP_RECEITAS_CAPITAL_PAINEL_EQUILIBRADO_LOTE95.xlsx` — painel e séries independentes de apoio do Lote 95.
- `/mnt/data/RMRP_LOTE98_RENDER/RMRP_VOLUME_II_QA_HOMOLOGACAO_LOTE98.pdf` — Volume II, **66 páginas**, sem alteração nesta etapa.
- Cópia de validação corrigida: `/mnt/data/RMRP_FECHAMENTO_G1/RMRP_LOTE94_COPIA_CACHE_COMPLETO_G1.xlsx`.
- Programa reproduzível: `/mnt/data/RMRP_FECHAMENTO_G1/auditar_g1.py` e `/mnt/data/RMRP_FECHAMENTO_G1/reparar_cache_lote94.py`.

## 2. Auditoria integral das fórmulas (dado novo do G1)

Foram inventariadas **1.278 células de fórmula** no XLSX original. O método recalculou independentemente, em Python, os grupos efetivamente usados:
- médias dos 12 números-índice mensais do IPCA e fatores anuais 2025/ano;
- referências entre planilhas, multiplicações das receitas nominais por fator;
- somas, contagens `COUNTIFS`, `SUMIF`, médias `AVERAGE` e condições `IF`;
- controles de DCL/RCL do RGF;
- cálculos de diferença e razão do controle de Pontal.

**Achado:** **49 fórmulas não tinham valor armazenado em cache no XLSX original**, sendo **46 da aba `COBERTURA_ANUAL`** e **3 da aba `PONTAL_QA_RGF_RREO`**. Essa é deficiência de interoperabilidade com leitores que usam valores em cache, **não é prova de fórmula incorreta**. As outras **1.229 fórmulas apresentaram valores cached coincidentes** com o recálculo independente.

Uma **cópia** do XLSX foi criada, editando apenas o valor armazenado `<v>` correspondente às 49 células sem cache; fórmulas e conteúdos originais, estilos e nomes de abas foram comparados célula a célula com o original, sem mudanças. Validação após a operação:
- **1.278/1.278 fórmulas com cache presente**;
- **1.278/1.278 comparações aritméticas aprovadas**;
- nenhum erro de fórmula detectado pelo recálculo;
- arquivo ZIP/XLSX válido e reaberto pelo OpenPyXL;
- **original do Lote 94 preservado**.

**Limitação:** o recálculo feito por código reproduz os padrões de fórmula inventariados; não constitui prova da execução por todas as versões do Excel. A cópia de cache completo não representa alteração do modelo ou dos valores de entrada.

## 3. Reconciliação da cobertura DCA e do Lote 95

- **374 chaves município–exercício únicas**, 34 códigos IBGE e 11 exercícios (2015–2025), **34 registros por ano**.
- **369 valores observados de receita de capital bruta DCA**, cinco contas sintéticas não encontradas (NA, não zero): Cássia dos Coqueiros 2015; Cajuru 2017; Santa Cruz da Esperança 2017 e 2022; Santa Rita do Passa Quatro 2021.
- Índices IPCA: **132 meses** (12 por exercício) e deflação pela **média anual**, com base em reais a **preços médios de 2025**.
- **374/374 chaves** da série do Lote 94 coincidem em ordem com as do Lote 95.
- **Zero divergências de valores deflacionados** entre resultados cacheados do Lote 94 e valores do Lote 95 para 369 registros observados; as cinco células NA permanecem ausentes.
- **30 municípios com 11 observações completas**, isto é, **330 registros**, no painel longitudinal equilibrado. Quatro municípios com ao menos uma lacuna não integram o painel, mas continuam nos cortes anuais quando observados.
- Para **cada ano de 2015–2025**, somas recalculadas para painel 30 e conjunto de registros disponíveis de até 34 municípios coincidiram com a planilha do Lote 95, tolerância R$0,01.

### Comparações 2024–2025 confirmadas

| Universo | 2024, R$ médios 2025 | 2025, R$ médios 2025 | Taxa real calculada |
|---|---:|---:|---:|
| Painel fixo 30 municípios | 370.724.349,28 | 320.747.898,01 | **−13,4807577018%** |
| Universo completo 34 municípios | 382.050.909,44 | 327.942.785,14 | **−14,1625429926%** |

Conceito: **receita de capital bruta realizada** da DCA I-C, **não investimento liquidado**, não transferência federal comprovada e não disponibilidade de caixa. Comparar com outras séries do Volume II somente após harmonizar suas datas-base de preços.

## 4. Proveniência editorial inicial conferida contra o PDF do Lote 98

A extração textual do PDF confirmou:
- **Página 2:** distinção explícita entre setembro/2026 (séries gerais) e preços médios de 2025 (nova série de capital).
- **Página 15:** informação **369/374**, cinco contas ausentes não convertidas em zero, IPCA médio anual.
- **Página 16:** comparação 30 municípios R$370,72 mi → R$320,75 mi (−13,48%); comparação 34 municípios R$382,05 mi → R$327,94 mi (−14,16%); RGF Executivo 2025 recuperado 34/34, com ressalvas para Pontal/Barrinha/Orlândia.
- **Página 60:** quadro sobre cenários ainda usa a expressão **“RGF/RREO com cobertura parcial”** de modo pouco específico, embora a página 16 já registre RGF Executivo 2025 34/34. **Pendência editorial EDI-02:** harmonizar essa redação, distinguindo cobertura de RGF 2025, outros recortes RREO e consistência dos indicadores. Não substituir indevidamente “parcial” para todas as bases RREO sem nova verificação.

A matriz de proveniência inicial mapeia **nove indicadores/grupos** com fonte, universo, período, cálculo, unidade, página e estado de QA. A **expansão para os demais indicadores do relatório ainda é tarefa G1 aberta**.

## 5. Artefatos novos da auditoria

- `/mnt/data/RMRP_FECHAMENTO_G1/QA_G1_ORIGINAL_SEM_CACHE.json`: estado do XLSX original e as 49 faltas de cache.
- `/mnt/data/RMRP_FECHAMENTO_G1/QA_G1_METODOS_E_RESULTADOS.json`: recálculo sobre a cópia corrigida, **zero divergências em 1.278 fórmulas**.
- `/mnt/data/RMRP_FECHAMENTO_G1/AUDITORIA_FORMULAS_G1.csv`: registro célula a célula das 1.278 fórmulas com cache corrigido e comparação numérica.
- `/mnt/data/RMRP_FECHAMENTO_G1/SERIE_ANUAL_VALIDADA_G1.csv`: receita nominal e real por ano, painel 30 e soma de observações disponíveis.
- `/mnt/data/RMRP_FECHAMENTO_G1/MATRIZ_PROVENIENCIA_G1.csv`: nove entradas iniciais.
- `/mnt/data/RMRP_FECHAMENTO_G1/RMRP_LOTE94_COPIA_CACHE_COMPLETO_G1.xlsx`: **cópia com caches completados**, sem editar o original.

O registro dos novos arquivos em Drive, se realizado, deve usar referências reais de bytes criadas no turno e posterior confirmação de metadados; não inferir conteúdo remoto somente do nome.

## 6. Critério de aceite e próximos passos

**Aprovada a frente G1-1 (receita de capital, IPCA e painel longitudinal)**. **Não declarar G1 integral fechado**: continuam a auditoria da proveniência dos demais indicadores fiscais, investimentos, despesas, transferências, cartografia, cenários e os casos em quarentena, antes de revisão integral de conclusões. O Volume II do Lote 98 não foi editado.

**Próxima frente G1-2:** ampliar a matriz indicador–fonte–fórmula–universo–página para as tabelas e sínteses restantes, identificar referências desatualizadas e submeter as divergências substantivas já conhecidas ao G2; não reabrir a série de capital validada sem fonte nova.
