# INV-RMRP — Auditoria da cobertura histórica DCA e SIAFEM sem dupla contagem

**Data:** 12/11/2026. **Escopo:** 34 municípios da RMRP; 13 exercícios DCA (2013–2025), sete exercícios SIAFEM (2020–2026). **Status:** QA territorial/temporal aprovado; NÃO significa conciliação contábil entre fontes.

## 1. Arquivos oficiais e checksums

**DCA SP645:** CSV histórico de 2013–2025, bucket R2 privado `financas-municipais-sp-canonico`, objeto `sp_645/dca/2013_2025/normalized.csv`; 2.096.525 bytes, SHA-256 canônico `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`. A leitura autenticada confirmou **8.385 linhas = 645 municípios × 13 anos**, com 29 colunas; não é um arquivo SQLite. A importação na rotina QA foi somente leitura, com validação de SHA.

**SIAFEM/SP:** `governance/INV_RMRP_SIAFEM_34_MUNICIPIOS_2020_2026_ANUAL_EXATO_2026_11_12.csv`, 34 municípios × 7 anos, 238 combinações (algumas com valor zero explícito); **R$ 305.521.029,20 liberados/estornados** e **1.017 pagamentos contabilizados** pelo sistema. 2026 limitado a 12/11.

**Cadastro:** `governance/INV_RMRP_34_MUNICIPIOS_PILOTO_IBGE_VERIFICADO_2026_11_11.csv`, IBGE7 e quatro sub-regiões.

## 2. QA executado e resultado

Código: `pipeline/qa/qa_inv_rmrp_dca_historica_siafem.py`; workflow `.github/workflows/inv-rmrp-dca-historica-siafem-qa.yml`.

- [GitHub Actions **43237431751**](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43237431751) — **success**; artefato QA [13952218730](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43237431751/artifacts/13952218730), com manifesto de cobertura sem cópia do CSV privado.
- DCA: **442 combinações município × exercício** da RMRP encontradas, cobrindo 34 municípios × 13 anos, sem falha de chave.
- Interseção DCA × SIAFEM: **204/204 combinações município × ano de 2020 a 2025**, zero lacuna territorial ou temporal.
- SIAFEM 2026: 34 combinações adicionais, **sem dado DCA correspondente**, porque a fonte DCA termina em 2025.
- **12 células DCA ausentes** considerando dois campos em 442 linhas históricas: 2 em investimento liquidado (2013 e 2014) e 10 em transferências de capital (2013, 2014, 2015, 2017, 2021, 2022, 2025). Nenhuma ausência deve ser tratada como zero.
- Na **interseção 2020–2025**, os **204 valores de investimento municipal liquidado** estão preenchidos; existem **3 valores ausentes de transferências de capital**.

## 3. Ausências DCA identificadas (não preencher automaticamente)

| Município | Ano | Campo ausente |
|---|---:|---|
| Luís Antônio | 2013 | Investimentos liquidados |
| Luís Antônio | 2013 | Transferências de capital |
| Cássia dos Coqueiros | 2014 | Transferências de capital |
| Santa Cruz da Esperança | 2014 | Transferências de capital |
| Serra Azul | 2014 | Investimentos liquidados |
| Serra Azul | 2014 | Transferências de capital |
| Cássia dos Coqueiros | 2015 | Transferências de capital |
| Cajuru | 2017 | Transferências de capital |
| Santa Cruz da Esperança | 2017 | Transferências de capital |
| Santa Rita do Passa Quatro | 2021 | Transferências de capital |
| Santa Cruz da Esperança | 2022 | Transferências de capital |
| Santa Cruz da Esperança | 2025 | Transferências de capital |

Os três valores ausentes **na série comparável 2020–2025** correspondem a Santa Rita do Passa Quatro/2021 e Santa Cruz da Esperança/2022 e 2025, todos no campo DCA transferências de capital. Os valores do SIAFEM nesses anos continuam disponíveis, mas não podem preencher, por equiparação indevida, o campo DCA.

## 4. Matriz versionada de convivência não aditiva

Criado `governance/INV_RMRP_SIAFEM_DCA_PAINEL_PARALELO_2020_2026_NAO_ADITIVO_2026_11_12.csv`, com **238 linhas município × ano** e campos distintos para:

1. `dca_investimentos_liquidados_centavos` + status (despesa liquidada de investimento pela administração municipal);
2. `dca_transferencias_capital_centavos` + status (rubrica declarada na DCA que não identifica automaticamente a origem SIAFEM);
3. `siafem_estadual_investimento_liberado_estornado_centavos` + quantidade documental de pagamentos (transferência estadual para investimento).

Para os anos **2020–2025** (204 linhas), os status registram 204 investimentos DCA observados; 201 transferências de capital DCA observadas e três ausências. Para **2026** (34 linhas), os dois valores DCA ficam vazios com marcador `DCA_ANO_NAO_DISPONIVEL`, enquanto SIAFEM conserva os valores exatos. São proibidas soma e subtração interpretadas como investimento territorial total ou taxa de execução sem estudo documental de correspondência.

A matriz é auditada por `pipeline/qa/qa_inv_rmrp_dca_siafem_parallel.py`, que compara cada célula à fonte R2 com validação de tipo decimal e à série oficial SIAFEM, exigindo as mesmas 238 chaves, ausências e regra explícita de não aditividade. O workflow de QA histórico foi ampliado; [execução **43238298245**](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43238298245) concluiu com **success**, com validação da matriz; o Core CI [43238298267](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43238298267) também concluiu com sucesso.

## 5. Restrições inferenciais e próximos gates

- O inventário DCA 2013–2025 **não foi importado como observações históricas no SQLite** nesta etapa. A verificação cobre CSV histórico, chaves, cobertura e comparação paralela. A prova de não regressão do SQLite fiscal real permanece homologada **somente para a reconstrução de 2025** (workflow 43234916467).
- DCA “investimentos liquidados” descreve um estágio da despesa local; SIAFEM “liberado/estornado” descreve fluxo estadual. Mesmo quando ambos são referentes ao mesmo município e ano, não se presume vínculo causal ou igualdade contábil.
- DCA “transferências de capital” pode reunir fontes estaduais, federais e outras; não usar o valor SIAFEM para substituir DCA e não somá-los.
- Manter a quinta prévia da PR #233 como experimento, sem promoção do painel paralelo à produção, até validação editorial e metodológica específica.
- Próximo desenvolvimento: definir estratégia de materialização histórica canônica em SQLite e QA de regressão integral, incluindo ausência versus zero, além de estudo documental de vinculação a convênios, projetos e obras.

**Governança:** nenhuma escrita no R2, D1 ou SQLite produtivos. PR #233 continua draft; PR #232/FED04 inalterada.
