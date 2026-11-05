# Lote 103 — Reconciliação interexercícios RGF de Pontal e localização do acervo oficial de Barrinha

**Data:** 05/11/2026. **Objeto:** aprofundar a auditoria dos dados fiscais 2025–2026, buscando comprovar os saldos de exercício anterior e localizar demonstrações originais do Executivo. **Estado:** nova divergência material de Pontal identificada no próprio RGF do exercício subsequente; acervo de documentos de Barrinha confirmado no portal municipal, mas PDF 2025 não foi lido. Volume II da RMRP, Lote 98 (66 p.), **não modificado**.

## 1. Pontal — reconciliação de abertura de 2026 com fechamento de 2025

Fontes primárias consultadas via API oficial Siconfi/STN para município **3540200**, Poder Executivo:
- RGF **Anexo 02**, exercício 2025, periodicidade Q, período 3: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2025&in_periodicidade=Q&nr_periodo=3&co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2002&id_ente=3540200&co_poder=E
- RGF **Anexo 02**, exercício 2026, periodicidade Q, período 1: https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2026&in_periodicidade=Q&nr_periodo=1&co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2002&id_ente=3540200&co_poder=E

| Conta | RGF A02 Q3/2025: `Até o 3º Quadrimestre` | RGF A02 Q1/2026: `Saldo do exercício anterior` | Diferença / avaliação |
|---|---:|---:|---|
| Dívida consolidada | R$ 173.246.915,32 | **R$ 173.246.915,32** | Coincide ao centavo |
| Deduções da dívida consolidada | **−R$ 6.672.866,88** | **−R$ 34.811.026,99** | Diferença de −R$ 28.138.160,11 |
| Dívida consolidada líquida | **R$ 179.919.782,20** | **R$ 208.057.942,31** | Diferença de +R$ 28.138.160,11 |
| Receita Corrente Líquida | **R$ 13.494.039,69** | **R$ 209.571.785,24** | Diferença de +R$ 196.077.745,55 |
| RCL ajustada para limite de endividamento | **R$ 13.494.039,69** | **R$ 209.271.785,24** | Diferença de +R$ 195.777.745,55 |
| DCL / RCL ajustada, % | **1.333,33%** | **99,42%** | Não comparáveis sem conciliação de versões |

**Achado:** mesmo no corpus transmitido ao Siconfi, a abertura de 2026 registra **RCL do encerramento de 2025** coincidente ao centavo com o RREO B6/2025 e com a publicação municipal de 18/03/2026. Mais importante, **a dívida consolidada bruta é idêntica** nas colunas de fechamento 2025 e saldo anterior 2026, mas as deduções e, por conseguinte, a DCL **não são**. O desacordo contábil não se limita ao denominador RCL. A diferença na DCL decorre aritmeticamente de diferença no campo de deduções, sem ser possível estabelecer com esses registros a natureza do ajuste ou eventual retificação.

**Critério de controle:** os campos de saldo anterior e fechamento de exercício devem ser **objeto de conciliação contábil**; identidade perfeita não pode ser exigida se houve reapresentação ou retificação documentada. Como tal documento não foi encontrado, não se deve eleger como corretos os saldos de 2026 e substituir os de 2025 automaticamente. Classificar **Pontal P0 — discrepância intra-Siconfi interexercícios, além de divergência Siconfi/DO**. Evitar inferência de descumprimento da LRF.

## 2. Barrinha — documento de 2025 localizado no índice oficial, ainda sem leitura de PDF

Foi recuperado via Crawl2AI o portal **real de prestação de contas** na porta 50000, não apenas o WordPress de entrada:
- https://portal.barrinha.sp.gov.br/portaltransparencia/ (página institucional);
- http://www.barrinha.sp.gov.br:50000 (aplicação própria de transparência);
- http://www.barrinha.sp.gov.br:50000/responsabilidade-fiscal/LRF-2025 (página com PDFs fiscais);
- http://www.barrinha.sp.gov.br:50000/publicacoes-obrigatorias?categoria=rel-de-gestao-fiscal (índice temático);
- http://www.barrinha.sp.gov.br:50000/publicacoes-obrigatorias/RELATORIOS-DE-GESTAL-FISCAL (índice antigo, grafia original).

A página `LRF-2025` efetivamente enumera arquivo **`ANEXO X RGF 2 QUADR 2025.pdf`**:
http://www.barrinha.sp.gov.br:50000/responsabilidade-fiscal/LRF-2025/ANEXO%20X%20RGF%202%20QUADR%202025.pdf

**Limitações verificadas nesta rodada:** leitura do PDF em Crawl2AI Markdown falhou com erro de ferramenta; captura de screenshot da URL PDF pelo Crawl2AI também falhou; tentativa Python Requests no contêiner falhou por resolução DNS. A ferramenta web de consulta tampouco conseguiu abrir o endereço na porta 50000. Portanto, **não foi recuperado texto nem imagem do PDF nem se verificou o seu conteúdo**. Seu nome **2 QUADR** não é suficiente para equipará-lo ao RGF Simplificado **2º semestre** transmitido ao Siconfi, nem para classificar a publicação como retificadora.

Foi encontrado no índice histórico um item intitulado **“RGF 4 BIM 2025”** vinculado a **arquivo 2024**: erro de catalogação; demanda verificação do próprio documento, nunca atribuição automática por rótulo. A rota `/responsabilidade-fiscal/LRF-2026` apresentou erro de aplicação e **não demonstra inexistência** de documentos de 2026.

Busca adicional externa por RGF do Executivo de Barrinha 2025/2026 resultou principalmente em agregadores que reproduzem os dados Siconfi, mas **nenhum PDF oficial de encerramento foi materialmente lido**. A cifra DCL/RCL **26,62%** está no Anexo 02 do Siconfi, enquanto o Anexo 06 contém **31,40%**; essa divergência segue aberta. Não inferir que o agregador independente possa dirimir divergência intradeclaração.

## 3. Pontal e Orlândia: cronologia ainda não conclusiva

Mantidas as datas oficiais de entrega do Siconfi do Lote 102: Pontal Q3/2025 `HO 2026-04-03T10:21:33Z`, Orlândia S2/2025 `HO 2026-01-30T11:28:46Z`, Barrinha S2/2025 `RE 2026-03-17T14:49:38Z`. **Os status não fornecem o histórico de versões anteriores**.

Conforme os Lotes 100–101, fontes municipais publicadas diferem do Siconfi em numeradores e/ou denominadores; nenhum novo documento protocolizado foi obtido nesta rodada. O quadro de Pontal tem agora **prova adicional de inconsistência entre o encerramento e a coluna de saldo anterior** no próprio Anexo 02 do Siconfi, fortalecendo a prioridade da auditoria.

## 4. Gates e decisão editorial

- **Pontal P0:** requer cópias oficiais do RGF de encerramento 2025 e abertura 2026, seus protocolos de transmissão, eventuais notas de reapresentação e demonstração das deduções da dívida consolidada; **não homologar RCL, DCL e percentuais de encerramento 2025.**
- **Barrinha P0:** recuperar em meio binário e inspecionar o PDF do Executivo, identificar ano e período internos, confrontar o RGF simplificado S2/2025 e buscar histórico da declaração retificada `RE`; sem documento lido, **não homologar índice A06 de DCL**.
- **Orlândia P0:** continuar a conciliação entre DO de 29/01/2026 e Siconfi de 30/01/2026, incluindo despesas de pessoal e dívida, preferencialmente em registros de Audesp/TCE-SP.
- **Guariba FNDE:** ainda depende de dados financeiros federais e municipais de empenho, liquidação e pagamento; nenhuma novidade neste lote.
- **IBS 2027–2030:** manter cenários condicionais e sem projeção monetária não homologada.
- **Volume II:** conservar Lote 98, 66 páginas, sem substituir tabelas/indicadores até saneamento fiscal e jurídico.

**Resultado:** Lote 103 integra nova conciliação de saldos interexercícios e documenta falhas verificadas de leitura dos PDFs municipais. A conclusão é de **inconsistência dos registros disponíveis, sem imputação de ilicitude ou erro por agente determinado**.
