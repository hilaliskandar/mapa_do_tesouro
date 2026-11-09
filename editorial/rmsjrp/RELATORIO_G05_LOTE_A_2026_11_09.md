# RMSJRP — G05 | Diagnóstico metropolitano e sub-regional, lote A
**Data:** 09/11/2026. **Estado:** cálculo territorial e comparação município–região executados, verificados e preservados; cartografia analítica, decomposição por programa/ação e interpretação municipal individual ainda pendentes. **Não homologar G05 integral antes dessas etapas.**

## 1. Fontes, processamento e proveniência
- Código reexecutável: `editorial/rmsjrp/build_diagnostico_g05.py`.
- Fonte municipal G04: `rmsjrp/g04/2026_11_09/SERIES_MUNICIPAIS_2013_2025.csv`; SHA-256 `1f0413304c54edbe57fe129a506d088da2cd296d767f901992c02f803fbd62e5`.
- Fonte territorial G04: `rmsjrp/g04/2026_11_09/SERIES_TERRITORIAIS_2013_2025.csv`; SHA-256 `70438537957f6b31bdf80e2e6705a5153735757a42d6cc8129067006087f6268`.
- Conferência TCESP G03, 111 pares município-ano, liquidação grupo 44: `rmsjrp/fase1/2026_11_09/tcesp/MATRIZ_TCESP_RMSJRP_2023_2025.csv`; SHA `5aa597f2a4f18caebdc8b652113f4745953919abe6c6c201ab9c29fc0f509a53`.
- Execução externa de QA: [GitHub Actions 42561961530](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42561961530), `success`, artifact `13649986299`. A gravação e a leitura de retorno SHA-256 foram confirmadas para os seis produtos no R2 privado `rmsjrp/g05/2026_11_09/`.
- Dados observados: FINBRA/DCA e TCESP 2023–2025. Correção: IPCA por média anual do Lote 17 RMRP, preços de setembro/2026. Sem imputação de ausências. Dados derivados não são evidência causal.

## 2. Trajetória metropolitana, preços constantes de setembro de 2026

| Indicador | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| Receita corrente real, R$ milhões | 6.849,79 | 7.326,16 | 7.645,26 |
| Investimento liquidado real, R$ milhões | 513,23 | 532,17 | 219,31 |
| Investimento real per capita, R$ | 532,25 | 551,37 | 227,23 |
| Investimento/receita corrente nominal, % | 7,49 | 7,26 | 2,87 |
| População de referência DCA | 964.260 | 965.175 | 965.175 |

De 2023 a 2025, a receita corrente real cresceu **11,61%**, ao passo que o investimento real diminuiu **57,27%**. Em 2024–2025, o investimento real caiu **58,79%**, em R$ **312,86 milhões**, apesar do crescimento de **4,36%** da receita corrente real entre os mesmos exercícios. O denominador populacional de 2025 repete 2024 na base DCA e **não constitui estimativa demográfica anual independente**.

## 3. Quatro sub-regiões, variação real 2024–2025

| Sub-região | Redução real dos investimentos, R$ milhões | Variação do investimento real | Variação da receita corrente real |
|---|---:|---:|---:|
| São José do Rio Preto — 14 municípios | −267,97 | −64,79% | +3,97% |
| José Bonifácio — 11 | −16,86 | −29,13% | +3,38% |
| Tanabi — 6 | −22,38 | −61,50% | +5,24% |
| Nova Granada — 6 | −5,64 | −23,23% | +9,31% |
| **RMSJRP — 37** | **−312,86** | **−58,79%** | **+4,36%** |

A sub-região do polo responde por aproximadamente **85,65% da redução regional líquida**. Todas as quatro sub-regiões reduziram o investimento real, mas em intensidade desigual. Não inferir que isso decorra de uma mesma causa fiscal.

## 4. Decomposição por município, 2024–2025
A soma das reduções municipais **brutas** foi R$ **327,58 milhões**, parcialmente compensada por R$ **14,72 milhões** de aumentos em outros municípios, resultando no saldo negativo de R$ **312,86 milhões**.

- Municípios com **redução real**: **29/37**; com aumento: **8/37**.
- São José do Rio Preto: **−R$ 220,83 milhões**; **−74,98%** em relação a 2024. Contribuição assinada de **70,59%** para o saldo regional negativo.
- Olímpia: **−R$ 47,05 milhões**; **−70,38%**; contribuição assinada de **15,04%**.
- Monte Aprazível: **−R$ 13,84 milhões**; **−87,06%**.
- Municípios com aumentos reais em 2024–2025: Irapuã, José Bonifácio, Orindiúva, Palestina, Paulo de Faria, Severínia, Uchoa e Urupês. Aumento observado não equivale à melhoria estrutural da capacidade de investimento.

A **contribuição assinada ao saldo regional** pode exceder 100% quando quedas e altas se compensam. A **participação na queda bruta** tem outro denominador; as duas métricas são mantidas separadas no arquivo `G05_CONTRIBUICOES_MUNICIPAIS.csv`.

Em 2023–2024, **23/37** municípios já tinham queda real de investimento; em 2023–2025, **30/37** registraram redução real. Assim, o sinal da maioria municipal diferiu do crescimento de investimento observado no agregado entre 2023 e 2024 — evidência de forte efeito composicional naquele intervalo.

## 5. Polo e demais municípios
| Exercício | Participação do polo no investimento regional real | Participação do polo na receita corrente real |
|---|---:|---:|
| 2023 | 51,88% | 45,91% |
| 2024 | 55,34% | 46,31% |
| 2025 | 33,59% | 46,88% |

O peso do polo no investimento caiu **21,75 pontos percentuais** entre 2024 e 2025, enquanto sua participação na receita corrente permaneceu próxima de 46–47%. É necessário examinar o calendário e os programas de investimento do município antes de estabelecer explicações.

## 6. Produtos, hashes e persistência
Todos os arquivos abaixo foram escritos no R2 privado sob `rmsjrp/g05/2026_11_09/`, recuperados e conferidos por hash no run `42561961530`.

| Produto | Linhas | SHA-256 |
|---|---:|---|
| `G05_TERRITORIOS_2023_2025.csv` | 15 | `d8c83b181e5949dbae13f68262d762079a476a27e373f97d5672689071558c26` |
| `G05_VARIACOES_TERRITORIAIS.csv` | 15 | `3982738c51faa41454bb0f8c3fb8b51927f36a58985e28a9b6dda4596160d9a0` |
| `G05_CONTRIBUICOES_MUNICIPAIS.csv` | 111 | `670ca3079eabb9a8d6218d104b8762ee8e8de7239ba6d1f0bc9273e80f87136c` |
| `G05_POLO_DEMAIS.csv` | 6 | `7cc1bcf373dfd9019946d9ee1db620f04c22e9e0ba615cb46dee355be7dadd7c` |
| `G05_DIRECAO_INVESTIMENTOS.csv` | 3 | `98a3d90965b0aeff0a458ebd0b002828d4d090e45761797942492e97dd30bc04` |
| `QA_G05.json` | 1 | `2c8b1d3bba318a51dfca09d4c124a18d49efecca7fc558e3da3c7a871c8b6b4a` |

O QA reproduziu os 111 valores nominais municipais TCESP × DCA, verificou 37 códigos, 15 território-anos, 111 decomposições municipais e agregações e preservou as fontes originais intocadas.

## 7. Cartografia: limite verificado e decisão
A fonte `data/catalogs/sp645_web_cartography.yml` documenta GeoJSON com 645 municípios, 645 polígonos, sem geometria nula, apto a visualização web. O próprio inventário registra **ausência de CRS explícito no payload** e **não aprova uso métrico ou analítico**. Não foi possível recuperar uma malha IBGE 2022, EPSG:4674, com proveniência comprovada nesta execução. **Portanto nenhum mapa coroplético foi declarado homologado**. Para os próximos trabalhos recuperar camada analítica já usada nos mapas RMRP ou outra malha IBGE oficial identificada, executar auditoria espacial de códigos, geometrias, CRS e topologia, e gerar mapas nos capítulos pertinentes sem simplificação geométrica.

## 8. Limites e próxima etapa precisa
- Este é o **lote A do G05**, com diagnóstico fiscal quantitativo e decomposição por município. **Pendente G05-B:** programas/ações TCESP para os municípios que concentram quedas e altas, detalhamento do papel dos investimentos de São José do Rio Preto, Olímpia e Monte Aprazível, revisão da diferença entre fluxo anual e cronograma de obras.
- **Pendente G05-C:** mapas e figuras com malha auditada, QA de legendas e inserção junto às análises.
- O cruzamento RREO/RGF está parcialmente disponível; não substituí-lo por DCA e não considerar ausência como zero.
- Não atribuir causalidade à LC 200/2023 nem antecipar conclusões de cenários G06.
- Próxima ação: recuperar acervos TCESP de programas e ações preservados no R2, filtrar municípios-chave, produzir tabela das maiores variações e examinar recodificações; em paralelo localizar e validar camada EPSG:4674 antes dos mapas. Registrar cada subgate no README principal e no HANDOFF, mantendo o estado `G05=in_progress` até terminar esses procedimentos.
