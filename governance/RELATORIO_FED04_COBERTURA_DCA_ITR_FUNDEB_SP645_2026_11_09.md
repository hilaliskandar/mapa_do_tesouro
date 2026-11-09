# FED04 — Cobertura analítica de ITR e Fundeb na DCA paulista de 2025

**Data:** 09/11/2026. **Status:** auditoria de presença de contas e origem da informação, sem integração fiscal nem promoção ao SQLite canônico.

## 1. Questão respondida

As receitas de ITR e do Fundeb **já constam nos registros originais de receitas do FINBRA/SICONFI (DCA)**, apesar de **não integrarem, como variáveis autônomas, as 46 variáveis do SQLite reconstruído em 2025**. Para o ITR, a DCA contém conta de receita bruta e a coluna específica `Deduções - FUNDEB`. O Fundeb contém, entre outras, conta de transferências recebidas e conta distinta da complementação federal. O valor adicional da STN é sobretudo **granularidade mensal/decendial, origem dos fluxos e desagregação de componentes**, inclusive VAAT/VAAR no snapshot 09/2026; não cabe tratar o mesmo valor como segunda receita municipal.

## 2. Duas fontes locais originais em Google Drive

A política de fontes já estava no catálogo [`finbra_dca_sp_drive_2013_2025.yml`](../data/catalogs/finbra_dca_sp_drive_2013_2025.yml): **arquivo anual primário** e **suplemento preenchendo somente lacunas**, sem substituir registros presentes, pois revisões ou diferenças de origem podem existir.

| Fonte | Arquivo | SHA-256 efetivamente conferido | Cobertura observada |
|---|---|---|---|
| Anexo I-C estadual 2025 — primário | [CSV bruto de receitas 2025](https://drive.google.com/file/d/185x_7zgX9aGOy0Z6Drh-iA9vBY83JU1F/view) | `502b0edb79d2fc7c330854877b5f6f2bfbd97fffca8189fb58f53a8b830a3827` | 85.903 registros, **632 municípios** |
| Suplemento de receitas 2022–2025 | [XLSX consolidado](https://drive.google.com/file/d/1FX1QFhv3_lUhfqxEW0z5KJ0EWGPoMZGQ/view) | `60c8f9cd356a4294b694263654f385b1b6e6aed20581ce8b5ddb1cd01a36105c` | Aba `2025-finbra`: 87.077 linhas, **642 municípios** |

A união das identidades municipais nos dois arquivos locais contém **642 códigos únicos**. O suplemento possui todos os 632 do primário e mais 10 códigos; portanto, **o arquivo local anual nunca foi substituído pelo suplemento em registros coincidentes**. Na auditoria de quatro contas e três colunas, foram identificadas **128 diferenças de valor em células coincidentes** entre as duas fontes. Essas diferenças exigem registro e comparação de versões, **não substituição automática**. Amostras das primeiras 100 divergências ficaram no QA local; a matriz de valores candidatos preserva sempre o valor da fonte anual quando presente.

A matriz candidata resultante possui **7.704 linhas** (642 municípios × 4 contas × 3 colunas), com distinção de `observado_baseline`, `preenchimento_candidato_suplemento`, `zero_explicito` e `linha_ausente`; SHA-256 do CSV `359989e9a3287ce37b4150662133ce4a4ca79d4985b8558032543febe01ab183`. O arquivo de auditoria foi disponibilizado como artefato local da conversa. **A matriz candidata foi preservada na mesma pasta de fontes do Google Drive**, sem sobrescrever a origem, em [QA_FED04_ITR_FUNDEB_DCA_SP_2025_642_MUNICIPIOS.csv](https://drive.google.com/file/d/19qUwskjGxBrakPakHuXl9WR5J6Z1a8Rv/view), tamanho **2.097.322 bytes**, SHA-256 **`359989e9a3287ce37b4150662133ce4a4ca79d4985b8558032543febe01ab183`**. O arquivo foi **recuperado novamente do Drive e teve SHA idêntico ao original local (readback aprovado)**. A matriz não foi importada no SQLite nem no R2; foi classificada como artefato derivado de QA.

## 3. Cobertura de contas específicas na união local — DCA bruta 2025

| Conta/coluna — `Receitas Brutas Realizadas` | Fonte anual | Somente suplemento (candidato) | Total identificado nos 642 códigos |
|---|---:|---:|---:|
| ITR — `RO1.7.1.1.52.0.0` | 621 | 10 | **631** |
| Fundeb recebido — `RO1.7.5.1.00.0.0` | 611 | 10 | **621** |
| Fundeb: complementação da União — `RO1.7.1.5.00.0.0` | 446 | 5 | **451** |
| FPM mensal — `RO1.7.1.1.51.1.0` | 631 | 10 | **641** |

Na coluna `Deduções - FUNDEB`, a conta do **ITR aparece para 600 municípios na origem anual e nove adicionais no suplemento**, totalizando **609** no universo local de 642. A conta de FPM mensal tem 610 + 9 = 619 casos com dedução específica. Linhas ausentes **não representam automaticamente zero**; colunas analíticas só devem ser comparadas e agregadas conforme a natureza e o estágio de receita.

## 4. Lacunas territoriais e consulta complementar oficial

A comparação com o crosswalk territorial **STN–IBGE SP645** já validado, artefato de auditoria [GitHub Actions 42658172768](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42658172768), revelou os **três municípios que não aparecem em nenhum dos dois arquivos locais de receitas 2025**:

- **Braúna**, IBGE `3507704`;
- **Sarutaiá**, IBGE `3551207`;
- **Tanabi**, IBGE `3553401`.

Foi realizada consulta pontual, em 09/11/2026, ao [endpoint oficial DCA](https://apidatalake.tesouro.gov.br/docs/siconfi/) com `an_exercicio=2025` e `no_anexo=DCA-Anexo I-C`. **Braúna** retornou 103 linhas; **Tanabi**, 129 linhas; ambas apresentam as quatro contas de receita bruta selecionadas. Para **Sarutaiá**, a API retornou zero linhas. A consulta prévia ao `extrato_entregas` também não encontrou DCA 2025 para Sarutaiá; isso não constitui afirmação de descumprimento sem verificar prazos, revisões e alternativas documentais.

Com os dois documentos adicionais consultados diretamente na API, a **disponibilidade comprovada de registros do anexo alcança 644 dos 645 municípios**, mas os dados desses dois municípios **não foram ainda incorporados à matriz local de 642**. Se observadas exclusivamente as contas com receita bruta presentes nessas duas consultas, os máximos documentais passam a ITR **633**, Fundeb recebido **623**, complementação federal **453** e FPM mensal **643** — sempre com a ressalva de que **Rio das Pedras não possui as contas selecionadas nos registros consultados**.

**Rio das Pedras (3544004)**: ao contrário de Sarutaiá, a API retornou 206 linhas do Anexo I-C de 2025 e há DCA homologada no extrato de entregas, mas nenhuma das quatro contas analíticas selecionadas. O problema é **ausência de detalhamento contábil nas rubricas específicas**, não falta de DCA. A presença de contas agregadas com valores e deduções incomuns requer auditoria separada. Não preencher as contas por dedução de agregados ou STN.

## 5. Encaminhamento para modelo canônico

1. **Aproveitar primeiro as contas DCA**: instituir variáveis específicas (com `fonte_preferencial_id=SICONFI_DCA`) somente após validar o esquema de contas e colunas, inclusive sua evolução anual de 2013–2025.
2. Para Fundeb, manter ao menos **três conceitos distintos**: receita distribuída do fundo, complementação da União e deduções para formação. O campo da STN `FUNDEB/DEDU` **não é outra transferência positiva a somar**.
3. Para ITR, manter **receita bruta e dedução identificadas**, sem presumir líquido igual ao valor da STN antes da conciliação. Registrar presença anual e município como estados de observação.
4. **Não recapturar desnecessariamente os 645 municípios pela API**: o primário e suplemento estão no Drive e a API deve atender prioritariamente às lacunas, retificações e controle independente.
5. Resolver Braúna/Tanabi como **delta de fonte externa documentado**; Sarutaiá permanece ausência de anexo. Investigar Rio das Pedras como anomalia de classificação/declaração.
6. Não somar Fundeb recebido, componentes de formação e complementação federal sem controle de sobreposição. Ementário, MCASP e estágio contábil têm precedência para interpretação fiscal.
7. **Não aplicar migrations nem atualizar valores públicos** até superar o QA e definir categorias que acrescentam informação, evitando dupla contagem.

**Evidência independente adicional:** [piloto de oito municípios no GitHub](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42700053330), com 96 combinações conta–coluna, CSV e JSON preservados no R2 privado, readback SHA do CSV aprovado.

**Conclusão:** a STN oferece **mais detalhe dos fluxos**, particularmente nos componentes do Fundeb, mas **ITR, recebimento do Fundeb e complementação federal já constam na contabilidade municipal original**. A primeira ampliação útil do sistema é a normalização dessas contas DCA, e não a criação de receitas duplicadas baseadas na STN.


## 6. Verificação final de persistência em Drive

A matriz de controle de **7.704 linhas** foi carregada na pasta Google Drive das fontes e verificada por leitura de retorno. [Abrir matriz de QA](https://drive.google.com/file/d/19qUwskjGxBrakPakHuXl9WR5J6Z1a8Rv/view). A comparação dos SHA-256 confirmou **`359989e9a3287ce37b4150662133ce4a4ca79d4985b8558032543febe01ab183`** tanto na origem local quanto no download após persistência. As fontes de dados originais não foram modificadas. As **128 divergências** entre fonte anual e suplemento permanecem apenas identificadas para revisão; a matriz preserva prioridade da fonte anual.

## 7. Fechamento da matriz de identidade SP645 com deltas API

Em 09/11/2026 concluiu-se uma **matriz estadual de presença de contas, com 645 códigos IBGE e 7.740 linhas** (645 municípios × quatro contas analíticas × três colunas de receita/dedução), com três fontes de origem **explicitamente distintas**: (i) CSV anual I-C de 2025, primário; (ii) XLSX `Receitas 2022–2025`, usado somente quando o primário não contém a célula; (iii) **delta pontual da API SICONFI** para Braúna e Tanabi. Sarutaiá está representado por 12 linhas `anexo_sem_registros`, **sem imputação de zero**. Os valores de origem nos municípios do delta API não foram utilizados para substituir valores dos arquivos locais. O controle de 645 códigos foi verificado quanto à unicidade da chave `codigo_ibge × conceito × coluna`.

| Conceito, `Receitas Brutas Realizadas`, exercício 2025 | Municípios com linha observada | Sem linha/sem anexo |
|---|---:|---:|
| FPM — cota mensal regular, `RO1.7.1.1.51.1.0` | **643** | 2 |
| ITR, `RO1.7.1.1.52.0.0` | **633** | 12 |
| Fundeb recebido, `RO1.7.5.1.00.0.0` | **623** | 22 |
| Fundeb — complementação federal, `RO1.7.1.5.00.0.0` | **453** | 192 |

**Persistência confirmada:** [`QA_FED04_DCA_ITR_FUNDEB_2025_SP645_COMPLETO.csv`](https://drive.google.com/file/d/1Tik1vEa5tSIIHp0GLPEjgJi_M6HUdP_d/view), pasta de fontes do projeto no Google Drive; **2.106.605 bytes**, SHA-256 **`9e34296a0aa9abdcd8fa5c8af9432bcb52d1cd8e550c4ae377c3efcf5947afe7`**, **download de retorno e comparação SHA aprovados**. O arquivo de 642 municípios preservado anteriormente continua como versão intermediária, não como a matriz estadual concluída.

**Questão substantiva resolvida:** o ITR já tem conta fiscal específica na DCA de 2025 e aparece em 633 municípios, apesar de não ter sido transformado em variável individualizada na plataforma. O Fundeb recebido e a complementação federal também têm contas distintas na DCA, e sua decomposição em eventos, origens e complementações VAAT/VAAR pela STN é informação complementar, **não receita municipal adicional automaticamente somável**.

**Pendências:** 128 discrepâncias entre fontes locais em células coincidentes não resolvidas; Rio das Pedras possui DCA mas não as quatro contas analíticas; Sarutaiá permanece sem anexo; validar contas e ementários 2013–2024 antes de promover variáveis ao SQLite. **Nenhuma migration, escrita em `observacao` ou publicação de indicador ocorreu.**
