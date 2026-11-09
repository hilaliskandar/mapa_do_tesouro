# FED02 — FPM, ITR e Fundeb: conciliação por hipóteses decendiais e piloto RREO

**Data de referência:** 09/11/2026. **Resultado:** hipóteses aritméticas testadas; ligação causal/contábil **não homologada**; sem alteração da base SQLite, migrations, indicadores e publicação.

## 1. Fonte preservada e parâmetros

Dataset STN Transferências Constitucionais para Municípios; competência **2026/09**, 13.889 registros para os 645 municípios paulistas, três valores decendiais. Snapshot R2 `financas-municipais-sp-canonico/sp_645/federal/stn/2026_09/candidates/STN_SP645_ITEMS_2026_09_FROM_097638ce.csv`, SHA256 `3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb`. Chaves IBGE já auditadas 645/645 contra o SQLite materializado. Operações realizadas apenas em cópia lida do R2, com aritmética decimal exata e sem transformar resultados em receita orçamentária.

Documentação primária da STN para transferências constitucionais e legais: https://www.gov.br/tesouronacional/pt-br/estados-e-municipios/transferencias-a-estados-e-municipios/transferencias-constitucionais-e-legais. A STN identifica retenções de **20%** das transferências que integram a base Fundeb e diferencia os repasses ao fundo da distribuição posterior (FNDE). A documentação de demonstrativos fiscais sobre deduções, receita bruta e Fundeb está disponível em https://conteudo.tesouro.gov.br/manuais/index.php?Itemid=675&catid=619&id=1221:03-03-05-01-tabela-3-demonstrativo-da-receita-corrente-liquida&option=com_content&view=article . Não confundir a norma geral de dedução com definição já comprovada dos campos particulares do CSV STN.

## 2. Hipóteses e provas

Teste H1, `FUNDEB/DEDU = (FPM/FPM)/4` se FPM no arquivo fosse exatamente 80% do bruto e DEDU só contivesse retenção FPM; 645 municípios × 3 decêndios = **1.935 comparações**. [Workflow 42673047882](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42673047882), **success**, [código](../pipeline/qa/audit_stn_fpm_fundeb_residuals.py). **64/1.935** resíduos foram de no máximo R$0,05 em módulo. Por decêndio: **31, 18, 15**. Medianas dos resíduos `DEDU - FPM/4`: **R$555,10**, **R$1.194,94**, **R$2.779,99**, respectivamente. A igualdade simples é rejeitada para a maior parte das observações.

Teste H2, `FUNDEB/DEDU = (FPM/FPM + ITR/ITR)/4`, **somente onde ambas as linhas FPM e ITR constam no arquivo STN**. [Workflow 42673434287](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42673434287), **success**, [código](../pipeline/qa/audit_stn_dedu_fpm_itr_hypotheses.py). Existem **632 municípios com linha ITR**, perfazendo **1.896 comparações município–decêndio**. **1.895/1.896** resíduos ficaram dentro de **R$0,05**; valor mediano **−R$0,02**, mínimo **−R$0,0525**, máximo **R$0,00**. Em **1.871/1.896** casos a inclusão do ITR reduziu o erro absoluto da fórmula FPM isolado; **24** empataram e **1** aumentou ligeiramente o erro. A razão `(DEDU - (FPM + ITR)/4)` foi calculada em reais com `Decimal`, sem aproximação por ponto flutuante.

**Interpretação restrita:** os resultados são fortemente consistentes com retenção de **20% sobre FPM e ITR brutos**, quando os valores de FPM e ITR do CSV representarem os respectivos saldos de **80% após a retenção**. A equivalência `20% da base bruta = 25% de 80% da base bruta` é matemática; **a STN ainda precisa confirmar que os campos do CSV de fato possuem essa definição**. Nenhum valor municipal bruto/líquido foi reconstruído ou promovido à base. O campo positivo `FUNDEB/DEDU` **não** é uma nova entrada positiva de receita municipal. Em **13 municípios** não existe linha `ITR/ITR` no recorte; ausência de linha não é zero contábil nem prova que a relação se aplique.

Os QA foram preservados em `sp_645/federal/stn/2026_09/candidates/QA_FPM_FUNDEB_DECENDIOS_2026_09_42673047882.json` (hash `33d504f947541a68ea7f065591c275b69bc2e7f7299428a30f32665b2095cb73`) e `sp_645/federal/stn/2026_09/candidates/QA_STN_DEDU_FPM_ITR_2026_09_42673434287.json` (hash `1bf4b1603875724591d263fd0b166953b62518a222f30ecac025059a551dd42f`). **Etapa é teste de hipóteses, não homologação de receitas.** A execução revisada [42673731964](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42673731964) não produziu jobs e terminou `failure`; logo, sua tentativa de identificar a exceção de R$0,0525 ainda **não foi verificada**. Manter a versão anterior aprovada como prova.

## 3. Pilotagem SICONFI RREO de 2026

A API oficial pública **SICONFI** está documentada em https://apidatalake.tesouro.gov.br/docs/siconfi/ , com limite de **1 requisição por segundo**, em JSON. Uma comparação de setembro de 2026 STN (mensal, caixa) exige demonstrativo municipal que inclua setembro e outubro, não o acumulado até agosto; a **DCA anual 2026 não deve ser presumida disponível durante o próprio ano**.

O script [`probe_siconfi_rreo_fpm_fundeb_2026.py`](../pipeline/acquire/probe_siconfi_rreo_fpm_fundeb_2026.py), [run 42673859324](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42673859324), **success**, consultou **3 municípios sentinelas** com códigos IBGE reais (Ribeirão Preto **3543402**, São José do Rio Preto **3549805**, Olímpia **3533908**), **Anexos 01 e 03**, **4º e 5º bimestres de 2026**: 12 consultas, respeitado o limite de frequência.

| Município | RREO Anexo 01 – 4º bim. | RREO Anexo 03 – 4º bim. | 5º bim. de 2026 |
|---|---:|---:|---|
| Ribeirão Preto | 492 registros | 437 registros | Sem registros nos dois anexos |
| São José do Rio Preto | 529 | 432 | Sem registros nos dois anexos |
| Olímpia | 491 | 422 | Sem registros nos dois anexos |

**Seis respostas com registros e seis respostas vazias, zero erros de conexão.** Resposta vazia **não equivale a receita zero**, nem prova inadimplência de entrega sem consulta ao `extrato_entregas`. O **4º bimestre encerra em agosto** e não deve ser comparado diretamente com as transferências STN **de setembro**. O 5º bimestre cobre setembro–outubro, cuja entrega deverá ser consultada posteriormente. No Anexo 03 já se observou a linha `DeducaoDeReceitaParaFormacaoDoFUNDEB`, mas não se inferiu seu valor ou estágio a partir do nome do campo. O relatório de QA do piloto está disponível como artefato [run 42673859324](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42673859324) e não contém reprodução de todos os valores fiscais. A seleção dos registros deve verificar coluna `cod_conta`, `conta`, `coluna`, exercício, bimestre, demonstrativo, versão/retificação e código IBGE.

## 4. Encaminhamento técnico

1. Verificar **documentação do extrato STN** e demonstrativo BB de distribuição com retenções separadas para FPM e ITR, preferindo documento público com composição decendial e códigos.
2. Recuperar e conferir a exceção de **R$0,0525** e os **13 municípios sem linha ITR**; tolerância de arredondamento não deve ser alargada silenciosamente. Não inferir zero onde o item está ausente.
3. Consultar `extrato_entregas` antes do RREO 5º bimestre 2026. Quando houver arquivo municipal disponível, comparar **períodos harmonizados** e valores do mesmo estágio, evitando totalizar fluxo STN e despesa/receita DCA como se fossem da mesma origem.
4. Manter `FED02=in_progress`; não aplicar a [migration candidata](proposals/PROPOSTA_STN_EVENTOS_DECENDIAIS_SP645.sql) e não escrever `observacao` anual até aprovação contábil e revisão dos 27 pares.

**Estado:** evidência forte da composição FPM–ITR para `FUNDEB/DEDU`, sem transformação em regra operacional de soma nem declaração de causalidade de política fiscal.
