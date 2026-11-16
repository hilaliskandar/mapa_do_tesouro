# FED03D e FED04C — auditoria financeira preliminar e validação espacial IBGE

**Data de processamento:** 15/11/2026. **Universo:** 34 municípios da RMRP por proponente, não por local comprovado de execução. **Estado:** auditoria reprodutível sobre registros oficiais reais, sem homologação de investimento de capital nem publicação pública.

## Fontes recuperadas e verificadas

- SQLite privado combinado FED03C/FED04B, 28.503 pagamentos, 395 linhas do módulo específico OBTV, 28.256 DL, 39.498 itens DL e 441 coordenadas de propostas: [staging antecedente](https://drive.google.com/file/d/1ZXhCXe-nDMadChIoV2QzoYHczBTigJsJ/view). Hash ZIP validado antes de extrair: `8184c1e06d4e4258d9c1bdd01daa407e7c7387f3251b80fb0a9cba7db60f36ea`.
- Malha oficial **IBGE 2024, 645 municípios de São Paulo**, `SP_Municipios_2024.zip` recuperada em [geoftp.ibge.gov.br](https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2024/UFs/SP/SP_Municipios_2024.zip); projeção da fonte em `.prj` = **SIRGAS 2000 / EPSG:4674**; SHA-256 `92a54d06e6f5a9749368e522861b785eae8c797329c9fa09cbb1a0696319d8e3`; nenhum dos 645 polígonos resultou inválido na inspeção Shapely. [Cópia da malha no Drive privado](https://drive.google.com/file/d/1jEPA0q0_JJl5sex863j_rMUngusKZ6es/view).

## FED04C — resultado da interseção espacial

O teste anterior por caixa geográfica foi substituído por interseção efetiva `Point(longitude,latitude)` x 645 polígonos oficiais, preservando o ponto de origem sem transformações estimadas, pois fonte e geometria foram analisadas em coordenadas geográficas SIRGAS 2000. Cada ponto foi ligado à proposta original, e o IBGE do município interceptado foi **comparado** ao IBGE do proponente.

| Categoria de interseção | Coordenadas |
|---|---:|
| No próprio município proponente | **381** |
| Em outro município da RMRP | **49** |
| Em outro município paulista fora da RMRP | **5** |
| Fora dos polígonos de SP | **4** |
| `0,0` (coordenada claramente inválida) | **2** |
| **Total** | **441** |

São **430 pontos em municípios da RMRP**, pertencentes a **257 propostas distintas**. Dos **218 projetos Obrasgov** relacionados aos proponentes, **216** possuem ao menos uma coordenada de proposta associada que intersecta RMRP; **3 projetos** possuem alguma coordenada candidata em outro município paulista. Essas contagens de projetos **não são necessariamente disjuntas**, devido a 1:N entre projeto e coordenada.

**Advertência essencial:** localização de **coordenada cadastrada na proposta** não equivale à localização material da obra executada. As 381 coordenadas que coincidem com o município proponente são apenas *coerentes territorialmente*, não pontos de obra homologados. Os 49 registros em outro município da RMRP e os 5 em outro município paulista devem ser examinados documentalmente antes de decidir se representam execução intermunicipal, endereço de referência, erro de cadastro ou outro caso. Não alterar sinais de latitude, nem mover pontos automaticamente.

A cópia do SQLite recebeu `municipio_sp_ibge2024_fed04c` (645 registros) e `coordenada_intersecao_sp_fed04c` (441 registros), preservando IBGE7 como texto e o município proponente em campo separado. **QA:** `integrity_check=ok`; zero violações de chave estrangeira; 645 polígonos válidos.

[ZIP privado FED04C — SQLite espacial e QA](https://drive.google.com/file/d/1EcNwpKgfcqCtkoXxPJJ_5fqYk7mjV8CH/view), 5.542.635 bytes; SHA-256 `d897d6d3772295ded62d3dae824223cd7b0f7080ae430785126febcca0270be8`. Upload e readback de conteúdo SHA-256/CRC verificados.

## FED03D — primeira auditoria financeira dos movimentos, sem atribuição de GND

- **28.503 movimentos de pagamento**, **1.286 convênios** (instrumentos selecionados por município proponente RMRP).
- Soma aritmética dos **valores nominais brutos de movimentos de pagamento a favorecidos:** **62.728.767.810 centavos = R$ 627.287.678,10**. Valor de **evento**, não soma ao desembolso ao convenente, não valor líquido de estornos, nem indicador de capital efetivamente pago.
- Modalidades: **22.318** `PAGAMENTO A FAVORECIDO COM OBTV`, e **6.185** `PAGAMENTO A FAVORECIDO`. `siconv_obtv_convenente` contém apenas **395 linhas relacionadas** ao universo dos pagamentos, **248** com valor financeiro ausente nessa tabela; **não** é uma tabela-filho completa de todos os 22.318 movimentos designados `COM OBTV`.
- **33 movimentos de valor zero**, **0 com valor negativo** no recorte, **0 valores monetários nulos** no registro de pagamento; isso **não** exclui estornos/devoluções registrados em outras bases ou modalidades, nem permite cálculo líquido.
- Todos os 28.503 pagamentos possuem `ID_DL` relacionado ao recorte; os **28.503** vínculos pagamento→DL→convênio correspondem ao mesmo `ID_PROPOSTA`. Há **27.238 DL distintos referenciados** pelos pagamentos.
- Situações dos DL associados: **28.469 pagamentos** com DL `Ativo`; **28** com DL `Inativo`; **6** com DL `Em Elaboração`. Esses **34 casos** exigem verificação documental; não declarar automaticamente pagamento indevido ou inválido.
- Período encontrado pela data dos pagamentos: **2009–2026**, analisado pelo ano final da data `dd/mm/aaaa`, não por ordenação lexicográfica.
- Itens de DL podem ser detalhamentos de documentos, não pagamentos financeiros independentes. Não somar os valores das tabelas pai e filha. PAD com GND4 aprovado não constitui prova de GND4 efetivamente pago.

[ZIP privado com relatórios QA FED03D e FED04C](https://drive.google.com/file/d/1Sdtky5JNIvpILhfATr7n5KRkIRuN8-V-/view), SHA-256 `0680e4087a92722d2206ec1b68c8af3691bc0a382fb084f0d2dec100067dc817`, upload e readback SHA-256/CRC aprovados.

## Pendências e próximos testes

1. **FED03D — reconciliação líquida e natureza de despesa:** verificar devoluções, estornos, repasses, ordens bancárias e demais estágios oficiais; não inferir que ausência de negativos nos pagamentos exclui devoluções. Cruzar documento/itens de DL a natureza da despesa apenas mediante identificador oficial.
2. **FED04C — exame individual das divergências:** auditar 49 coordenadas em outro município da RMRP, 5 em SP fora da RMRP, 4 fora de SP e 2 registros `0,0`, incluindo municípios/fronteiras e confiabilidade da localização. Usar documentação de projeto/obra para classificação de `local_execucao_comprovado`; não confundir com localização candidata.
3. Produzir indicadores exploratórios **com rótulos inequívocos** em painel de desenvolvimento; manter valores de investimento executado em `null` enquanto não homologados.
4. **Publicação bloqueada:** `public_release_authorized=false`; nenhuma escrita na base fiscal canônica ou no site público.

Os três ZIPs novos da execução foram preservados na pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`, com metadados de acesso privado e hash integral conferido após download.
