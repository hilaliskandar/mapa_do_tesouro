# Lote 101 — Confronto dos RGF publicados em Diário Oficial e dados do Siconfi

**Data:** 05/11/2026. **Objeto:** diligência documental de homologação dos indicadores RGF 2025 de Orlândia, Pontal e Barrinha, no âmbito do Volume II da Região Metropolitana de Ribeirão Preto. **Resultado:** publicação primária do Executivo de Orlândia localizada e cotejada; de Pontal, publicação já localizada no Lote 100 foi reexaminada, inclusive estrutura de anexos; em Barrinha, ainda não se obteve publicação original do Executivo que permita resolver as diferenças. **Volume II Lote 98 (66 páginas) não modificado.**

## 1. Orlândia — fonte municipal primária nova

**Jornal Oficial de Orlândia, edição extraordinária nº 2238, de 29/01/2026, página 5**, “Relatório de Gestão Fiscal — Poder Executivo”, período janeiro/dezembro de 2025. Endereço: https://www.dosp.com.br/exibe_do.php?i=NzY5NTky . Texto primário localizado e lido na versão indexada do Diário Oficial: https://www.dosp.com.br/impressao.php?i=NzY5NTky . A leitura com Crawl2AI da URL de exibição encontrou erro de extração; a inspeção via busca web apresentou o texto completo da tabela municipal. Screenshot web do recurso não foi possível por problema de tipagem/captura. **Não declarar validação visual do PDF original**.

| Indicador | Diário Oficial municipal 29/01/2026 | Siconfi RGF simplificado S2/2025 | Observação |
|---|---:|---:|---|
| RCL ajustada para cálculo de endividamento | R$ 263.501.501,04 | R$ 263.501.501,04 | Coincidente |
| RCL utilizada para pessoal no quadro municipal | R$ 261.870.013,04 | R$ 261.870.013,04 | Coincidente |
| Dívida consolidada líquida | **−R$ 19.720.109,67** | **−R$ 17.264.485,35** no Anexo 02 | Divergência material de R$ 2.455.624,32 |
| DCL / RCL ajustada para endividamento | **−7,48%** | **−6,55%** no Anexo 02 | Coerência aritmética interna da publicação municipal |
| Despesa total com pessoal | **R$ 139.863.791,37** | **R$ 139.797.400,92** no Anexo 06 | Divergência de R$ 66.390,45 |
| DTP / RCL de pessoal | **53,40%** | **53,38%** no Anexo 06 | Índices próximos, mas não idênticos |

Os valores oficiais do Siconfi foram consultados e preservados nos Lotes 93 e 99, com os filtros `an_exercicio=2025&in_periodicidade=S&nr_periodo=2&co_tipo_demonstrativo=RGF%20Simplificado&no_anexo=RGF-Anexo%2002` ou `RGF-Anexo%2006&id_ente=3534302&co_poder=E`. No Diário Oficial, o quadro usa expressamente “Metodologia da LRF e Leiaute do Sistema Audesp do Tribunal de Contas do Estado de São Paulo”. Não se pode assumir equivalência do processo de captura e da data da informação entre Audesp e Siconfi.

**Conclusão documental:** a diferença anteriormente identificada no Lote 99 entre `−6,55%` (A02) e `−6,59%` (A06) do Siconfi pode ser parcialmente explicada por denominadores internos distintos, mas o **documento municipal publicado contém outro numerador de dívida líquida**, de modo que a divergência entre versões **não se resolve apenas pela escolha do denominador**. A publicação municipal também difere no numerador da despesa com pessoal. Não selecionar um valor como definitivo sem verificar protocolo, data de transmissão, versão e eventuais retificações.

**Observação normativa:** o percentual municipal de DTP de 53,40% supera o limite prudencial geral de 51,3% do Executivo e permanece abaixo do máximo de 54%. Isso não substitui parecer sobre cumprimento da LRF: exigiria confirmar composição, cálculos, versões e eventual medida corretiva aplicável. O índice Siconfi de 53,38% também supera 51,3%, sem resolver a divergência entre fontes.

## 2. Pontal — revisão da edição de 18/03/2026

O Diário Oficial de Pontal, edição **1906**, de **18/03/2026**, https://dosp.com.br/exibe_do.php?i=NzkyNDYw , foi reexaminado. No Lote 100, a **página 22** apresentou RGF Anexo 01 do Executivo de 2025 com RCL R$ 209.571.785,24, RCL ajustada pessoal R$ 209.261.592,13, despesa total com pessoal R$ 101.819.534,91 e 48,66%. A **API Siconfi** do RGF do 3º quadrimestre traz RCL R$ 13.494.039,69, DTP R$ 108.682.695,50 e 805,41%. O RREO B6/2025 do Siconfi reproduz RCL R$ 209.571.785,24. Os dois numeradores e os dois denominadores permanecem inconciliados.

O exame do índice de páginas da edição 1906 localizou RGF **Anexo 03 (garantias)** na página 14. Foi localizada no mesmo exemplar a cifra R$ 83.638.210,59 de DCL em **RREO Anexo 06 (resultado nominal)**, página 35, mas **ela não é uma medida intercambiável automaticamente com RGF Anexo 02 (dívida consolidada líquida)**. A tentativa de screenshots das páginas 14, 22 e 35 pelo serviço de consulta retornou **cache miss**, tornando obrigatória inspeção visual posterior da edição antes de afirmar identidade contábil ou usar números daquela página para corrigir DCL do Siconfi.

O extrato de entrega do RGF Q3/2025 ao Siconfi, examinado nos lotes anteriores, aponta data 03/04/2026, posterior ao Diário Municipal de 18/03/2026. **Isso suscita hipótese de versões distintas, não comprova retificação.** É necessário o histórico protocolizado e a versão da dívida publicada pelo Executivo no RGF Anexo 02.

## 3. Barrinha — status de descoberta e fontes de menor força probatória

Nova rota institucional de transparência do Executivo localizada: https://portal.barrinha.sp.gov.br/portaltransparencia/ . A página recuperada está embutida em iframe; **não foi localizado nem lido um PDF do RGF do Executivo de S2/2025 ou S1/2026** capaz de solucionar discrepância entre anexos. A Câmara Municipal, https://www.barrinha.sp.leg.br/transparencia , **não é fonte substituta do RGF do Poder Executivo**.

O agregador independente https://prefeiturasemnumeros.com.br/municipios/barrinha-sp informa DCL/RCL 26,62% para 2025, reproduzindo o Anexo 02 do Siconfi, e 0,41% em S1/2026, mas **não constitui publicação primária independente** nem reconcilia a DCL monetária divergente do Anexo 06. A matriz de QA dos Lotes 93 e 99 permanece válida.

## 4. Matriz de evidências e próximos passos

| Município | Publicação municipal 2025 | Dados STN 2025 | Conciliação de versões | Estado |
|---|---|---|---|---|
| Pontal | RGF A01 do Executivo, DO 18/03/2026 | RGF Q3 e RREO B6 divergentes | **Não** | P0, quarentena |
| Orlândia | RGF do Executivo, DO 29/01/2026 | RGF Simplificado S2 A02/A06 divergentes da publicação | **Não** | P0, divergência de dívida e pessoal |
| Barrinha | Documento do Executivo **não localizado** | RGF Simplificado S2 A02/A06 diferem entre si | **Não** | P0, diligência pendente |

**Diligência sequencial:** (1) obter versões protocolizadas RGF Pontal, Orlândia e Barrinha e metadados de retificação; (2) tentar captura dos PDFs originais via repositório municipal/Diário e conferir visualmente quadros; (3) mapear no portal de Barrinha a rota interna do iframe até documentos oficiais; (4) verificar se Audesp/TCE-SP traz o mesmo RGF publicado em Orlândia; (5) **não substituir** valores na versão Lote 98 antes de conciliação.

## 5. Restrições

A descoberta das publicações foi feita com busca web por não haver descoberta nativa na conexão Crawl2AI; tentativas de leitura dos DO por Crawl2AI falharam, e o texto primário de Orlândia foi obtido do documento indexado pelo mecanismo de busca, não de uma renderização visual. Os documentos não foram baixados como PDF para arquivamento nesta rodada. Não se concluiu inexistência de outros documentos, irregularidades de declaração, violação legal ou homologação.

**O Volume II, edição Lote 98, de 66 páginas, foi preservado sem edição.**
