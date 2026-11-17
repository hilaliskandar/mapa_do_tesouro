# F01/F02 — primeira matriz financeira real de desembolsos e pagamentos da RMRP34

**Apuração:** 17/11/2026. **Fontes:** ZIPs de staging privados oficiais FED08B (16/11) e FED03C/FED04B (15/11), recuperados do Drive com hash integral validado e SQLite íntegros. **Escopo:** 34 municípios da RMRP pelo **papel de proponente**. **Não é total de investimento federal executado, nem etapa de homologação pública**. `public_release_authorized=false`.

## Execução comprovada sobre dados reais

Foram recuperados do Google Drive os dois pacotes de staging já existentes:
- `RMRP_FED08B_EMPENHO_DESEMBOLSO_PRIVADO_2026-11-16.zip` ([origem](https://drive.google.com/file/d/1IhdpGNx6f5aGu5qtpv1XshKNck8Dr39I/view)); SHA-256 `bfa04d63b9670f79f812fd53b236506ff45efb444d75afa1b456cfcf47d5693d`; contém SQLite de 15.892.480 bytes.
- `RMRP_FED03C_FED04B_REAL_STAGING_2026-11-15.zip` ([origem](https://drive.google.com/file/d/1ZXhCXe-nDMadChIoV2QzoYHczBTigJsJ/view)); SHA-256 `8184c1e06d4e4258d9c1bdd01daa407e7c7387f3251b80fb0a9cba7db60f36ea`; contém SQLite de 15.134.720 bytes.

Em ambos: ZIP CRC íntegro, `PRAGMA integrity_check=ok`, `foreign_key_check` sem ocorrências. O processamento utilizou tabelas-pai `desembolso_fluxo` e `pagamento_fed03c`, sem somar colunas das tabelas-filhas de empenhos, DL, itens DL e OBTV.

## Resultados monetários validados aritmeticamente e seus limites

| Medida da fonte | Registros | Centavos | BRL | Natureza / interpretação |
|---|---:|---:|---:|---|
| Desembolso ao convenente com conciliação exata com grupos de empenho | **2.535** | 71.431.939.367 | **R$ 714.319.393,67** | Desembolso reconciliado, não gasto final municipal |
| Desembolso com divergência de ponte | **1** | 47.500.000 | R$ 475.000,00 | Desembolso pai existe, diferença de R$ 88.000,00 com a soma dos grupos |
| Desembolso sem ponte de empenho | **1** | 19.472.080 | R$ 194.720,80 | Desembolso pai existe, sem vínculo na tabela analisada |
| **Todos os desembolsos pai** | **2.537** | **71.498.911.447** | **R$ 714.989.114,47** | Total observado de desembolsos documentados, incluindo os dois casos não reconciliados |
| Movimentações nominais de pagamentos a favorecidos | **28.503** | **62.728.767.810** | **R$ 627.287.678,10** | **Bruto nominal**, sem prova de líquido por estorno ou capital efetivamente pago |

**Não somar os R$ 714,99 milhões aos R$ 627,29 milhões:** são etapas parcialmente sobrepostas da mesma cadeia e exercem funções diferentes. O total bruto dos desembolsos é conhecido por suas linhas-pai, mas somente o subconjunto de R$ 714,319 milhões tem conciliação de grupos de empenho comprovada.

As duas exceções pertencem ao proponente **Ribeirão Preto (IBGE7 3543402)**, nos exercícios **2012** (R$ 194.720,80 sem ponte) e **2013** (R$ 475.000,00, diferença de R$ 88.000,00). Não foi inventada solução documental nem redistribuído valor.

### QA independente de pagamentos

- `NR_MOV_FIN`: **28.503** movimentos distintos, sem duplicação.
- Modalidades em `tp_mov`: **22.318** `PAGAMENTO A FAVORECIDO COM OBTV` (**R$ 513.795.203,10**) e **6.185** `PAGAMENTO A FAVORECIDO` (**R$ 113.492.475,00**).
- **33** pagamentos de valor nominal zero; nenhum sinal negativo nos valores selecionados. **A ausência de negativos nesta tabela não comprova ausência de devoluções/estornos em outras fontes.**
- Situação de DL associada aos movimentos: **28.469** `Ativo`, **28** `Inativo`, **6** `Em Elaboração`; o valor nominal dos 34 movimentos com DL não ativo soma **R$ 272.120,91**, mas a situação do documento **não prova** irregularidade nem autoriza exclusão automática.
- Datas de pagamento válidas de **2009–2026**; desembolsos da série de **2008–2026**.

## Produtos privados gerados

Arquivo [**RMRP_F01_F02_AGREGADOS_PRIVADOS_2026-11-17.zip**](https://drive.google.com/file/d/1fM3fw-jnWEAE5EpUoJk7JTMJAkmzA4YL/view), armazenado na mesma pasta Drive privada de staging da RMRP:
- `rmrp_f01_f02_municipio_ano_privado.csv`: **505 combinações município-ano observadas** ao combinar ambos os estágios, com totalizadores em **centavos inteiros**, contagens, status de conciliação e campos líquidos/GND4/Obrasgov **vazios (não zeros)**.
- `rmrp_f01_f02_resumo_anual_privado.csv`: série regional anual dos dois estágios, sem soma entre eles.
- `rmrp_f01_f02_qa_publicavel_sem_identificadores.json`: QA agregada, checks, exceções sem número de desembolso, hashes das fontes e limitações.

**Verificação independente do pacote:** 10.976 bytes; SHA-256 `5bf3385d7e170cd4e7b7911e933eb97c3be08db4aa677d0c8d1a4502aa3e4913`; ZIP CRC íntegro. Upload Drive confirmado com `shared=false` e pasta `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`. **Readback do Drive executado na mesma sessão, hash byte a byte idêntico**.

Os agregados cobrem proponentes dos 34 municípios. Linhas com ausência de evento em um ano não foram transformadas em zero e não se inferiu localização física de execução.

## Primeiro comparativo temporal ilustrativo de ESTÁGIOS, não investimento total

| Ano | Desembolsos ao convenente reconciliados | Pagamentos nominais brutos a favorecidos |
|---:|---:|---:|
| 2023 | R$ 37.755.199,86 | R$ 34.246.177,06 |
| 2024 | R$ 120.055.217,32 | R$ 59.457.571,28 |
| 2025 | R$ 85.961.124,04 | R$ 104.112.691,17 |
| 2026 parcial | R$ 121.801.512,03 | R$ 106.662.279,68 |

A defasagem temporal entre recebimento ao convenente e pagamentos a favorecidos impede interpretar a diferença anual como gasto próprio ou recursos não aplicados.

## Pendências restantes F01–F02 e transição

1. **F01:** exceções com identificadores preservados somente no pacote privado FED08B: buscar ponte oficial que explique o desembolso sem empenho e a diferença de R$ 88.000,00; manter ambos como `nao_reconciliado` até evidência.
2. **F02:** verificar movimentos de devolução/estorno em fontes oficiais, status de pagamentos, retenções e possíveis sobreposições de OBTV/DL. Não remover 34 movimentos com DL não ativo apenas pelo status. 
3. **F02 natureza de despesa:** inspecionar a ponte documental real `ID_DL` → itens → plano de aplicação/GND, sem presumir GND4 pago a partir do código `44` do empenho.
4. **F03–F04:** completar modalidades federais Parcerias/Especiais e avaliar valores Obrasgov sem somá-los a desembolsos/pagamentos já representados.
5. **F05:** confrontar fatos federais por ano/município com SIAFEM estadual e despesas municipais FINBRA/TCESP como **colunas distintas**; não gerar investimento total público executado enquanto houver fontes de execução direta e natureza de gasto sem cobertura.

**Resultado do gate:** F01/F02 **concluídos somente quanto a matriz real de estágios e conciliação do subconjunto existente**. Permanecem parciais quanto a valor líquido, capital final pago e duas exceções. Nenhum deploy público ou modificação do banco fiscal canônico.
