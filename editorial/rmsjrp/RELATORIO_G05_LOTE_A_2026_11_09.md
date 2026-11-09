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


## 9. Complemento G05-B — programas e ações TCESP (execução concluída, análise substantiva pendente)
A leitura direta dos agregados estaduais **por programa e por ação**, para 2023, 2024 e 2025, foi concluída no [GitHub Actions run 42562212589](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42562212589), status `success`, artifact `13649449797`. O processamento `editorial/rmsjrp/build_programas_acoes_g05b.py` filtra os 37 códigos IBGE, estágio **valor liquidado** e grupo 44, preserva o identificador do órgão, do programa e da ação, e concilia 111 pares município-ano com os totais auditados na Fase I. **4.884 registros de movimento** entre chaves programáticas e de ação foram produzidos para três intervalos (2023–2024, 2024–2025, 2023–2025), dos quais 480 compõem o extrato ranqueado por magnitude, com QA.

**Maiores quedas nominais por chave órgão/programa em 2024–2025**, em reais correntes e **não** corrigidos pelo IPCA:

| Município | Órgão e programa | Redução nominal |
|---|---|---:|
| São José do Rio Preto | Prefeitura, programa 9 — Planejamento e Infraestrutura Urbana | R$ 171,98 milhões |
| Olímpia | Prefeitura, programa 45 — Concessão Água e Esgoto | R$ 46,67 milhões |
| São José do Rio Preto | SEMAE, programa 31 — Investimentos | R$ 13,09 milhões |
| Monte Aprazível | Prefeitura, programa 14 — Infraestrutura de Serviços Urbanos | R$ 9,56 milhões |
| São José do Rio Preto | Prefeitura, programa 8 — Gestão do SUS | R$ 7,15 milhões |

Os títulos são os **rótulos contábeis presentes no TCESP**, não interpretações de execução física, responsabilidade da União ou eventos conclusivos sobre obras. As cifras deste quadro são diferenças por chave contábil específica; podem divergir das quedas **reais totais municipais** e não se devem somar a elas. A ocorrência de uma chave em um ano e sua ausência em outro não comprova encerramento de projeto: requer verificação de recodificações, mudanças de órgão e eventuais deslocamentos de classificações.

Os três arquivos G05-B foram persistidos e tiveram leitura de retorno SHA-256 no R2 privado em `rmsjrp/g05/2026_11_09/programas_acoes/`:
- `G05B_TRANSICOES_PROGRAMA_ACAO_2023_2025.csv`: SHA `02bbf839bf849fc374ee3dcb64aad8dc9695c6972cfaec2cff89ee741ccd5d31`;
- `G05B_MAIORES_MOVIMENTOS.csv`: SHA `d9b99861b86b211ee533e388617ec615fcec35087b9b0b8eeb624cf541860742`;
- `QA_G05B.json`: SHA `f792619b7c8595bc62fa2d31803dc76f9a432de0c75fd999fb6bc5920fe5f2d6`.

**Situação de continuidade:** G05-A e G05-B aritmética e contabilidade aprovados. Prossegue pendente **G05-C** cartografia com camada IBGE EPSG:4674 auditada; e **G05-D** revisão interpretativa dos principais programas/ações contra documentos primários (contratos, orçamento, projetos e cronograma), com especial atenção aos três municípios de maior contribuição negativa. Não declarar G05 inteiramente homologado até os mapas e a revisão de interpretações.


## 10. Complemento G05-C — cartografia oficial IBGE 2022, com QA aprovado
A etapa cartográfica foi executada no [GitHub Actions run 42562450625](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42562450625), resultado `success`, artifact `13650151673`, usando exclusivamente a **Malha Municipal Digital de São Paulo de 2022** do IBGE, fonte [FTP IBGE SP_Municipios_2022.zip](https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2022/UFs/SP/SP_Municipios_2022.zip). Essa camada oficial supera a limitação do GeoJSON simplificado do painel estadual.

A versão original foi preservada, SHA-256 `341664fdb610df9b92a8f01546e1a83474135cf686c4dcf6c2e0ea91552b0013`. O script `editorial/rmsjrp/gerar_mapas_g05c.py` inspecionou o CRS declarado na própria PRJ (`EPSG:4674`, SIRGAS 2000), as 645 feições estaduais, as **37 geometrias selecionadas por código IBGE**, a existência de códigos únicos e a validade geométrica de todas as 37. O mapa usa os vértices completos do arquivo de origem, **sem simplificação**. Houve verificação visual das duas pranchas; auditoria topológica completa de todas as fronteiras do estado não foi realizada, e não se afirmou tal nível de QA.

Foram produzidos:
1. `MAPA_G05_VAR_INVEST_2024_2025.png`: variação real percentual do investimento liquidado, 2024–2025, por município; variações positivas e negativas visualizadas no território.
2. `MAPA_G05_INVESTIMENTO_PC_2025.png`: investimento liquidado real per capita em 2025, preços de setembro/2026; a população 2025 da DCA repete numericamente a de 2024, cautela obrigatória.
3. `RMSJRP_37_IBGE2022_EPSG4674.geojson`: recorte com 37 feições e valores fiscal-geográficos para recomposição das pranchas.
4. `QA_G05C_CARTOGRAFIA.json`: proveniência, integridade e hashes.

Objetos preservados no R2 privado em `rmsjrp/g05/2026_11_09/cartografia/`, com leitura de retorno e validação SHA-256:
- ZIP IBGE original: `341664fdb610df9b92a8f01546e1a83474135cf686c4dcf6c2e0ea91552b0013`;
- GeoJSON regional: `d171e094f045461687900463925297bdb843a1db07e32a3cfa78940a063cc3a2`;
- mapa de variação: `661bc3e2c23ba0e32f2de792e0e2105c0c316fe086a09571d1c6e03de913868c`;
- mapa per capita: `e0f557ceb5a55aeeb33a906e658b8838794377b2c937aaf3ec4a954126760b53`;
- QA: `1f0142a3a014bc9b946f4af9926e6bc4cbd428c04d1835d6ce31a7a29822b927`.

**Estado após G05-C:** G05-A (decomposição territorial), G05-B (programas/ações) e G05-C (dois mapas) possuem QA técnico e persistência aprovados. **Ainda pendente G05-D**: leitura substantiva de programas/ações e possíveis recodificações, com confronto a documentos orçamentários, contratos e cronogramas para as conclusões individualizadas; também verificar coerência editorial dos mapas com textos quando forem inseridos. Não homologar inferências causais apenas pela qualidade das tabelas e mapas.
