# Lote 96 — Incorporação editorial condicionada da série fiscal e QA visual do Volume II

**Data:** 04/11/2026. **Estado:** nova cópia editorial produzida e renderizada; **não homologada para circulação externa**.

## 1. Insumos efetivamente examinados

- Documento-fonte local do Lote 87: `RMRP_VOLUME_II_MAPA15_CORRIGIDO_LOTE87.docx`, com 312 parágrafos e 45 tabelas; PDF renderizado do mesmo lote: **63 páginas**.
- Insumos fiscais persistidos no Drive no Lote 95: `RMRP_RECEITAS_CAPITAL_PAINEL_EQUILIBRADO_LOTE95.xlsx` ID `1jssZ2QQjXfAoB1nr-ovRUDLq7E4XLJOz` e CSV de 30 municípios ID `1jpS_1bK1aRnxuNuJh6gk8eb3DiQizV9O`.
- Dossiês de QA: `RECUPERACAO_DCA_RGF_LOTE93_2026_11_04.md`, `DEFLATOR_RECEITA_CAPITAL_QA_LOTE94_2026_11_04.md` e `PAINEL_EQUILIBRADO_RECEITA_CAPITAL_LOTE95_2026_11_04.md`. **Não houve reextração genérica nem alteração de valores nesses lotes**.

## 2. Correções objetivas da edição de trabalho

Foi gerado por edição mínima do DOCX original `RMRP_VOLUME_II_INTEGRACAO_FISCAL_LOTE96.docx` e renderizado em `RMRP_VOLUME_II_INTEGRACAO_FISCAL_LOTE96.pdf`.

- **Página 6, após os mapas FPM/ICMS/IPVA:** removidas uma nota interna inadequada ("a referência não significa que imagens tenham sido embutidas nesta edição Markdown", pedido de conferência antes da diagramação) e duas URLs excessivamente extensas no corpo. Substituição por leitura interpretativa de composição fiscal e crédito de fonte: FINBRA/Siconfi, IBGE, cartografia do Volume I.
- **Páginas 14–15 da nova edição:** inserida subseção **"Receitas de capital e comparabilidade da série histórica"**, sem apresentar receitas de capital como investimento liquidado. Dados DCA I-C 2015–2025: **369/374 combinações observadas**; cinco contas sintéticas ausentes, não transformadas em zero. Valores em reais médios de 2025 por deflação com índice IPCA médio anual (SIDRA 1737).
- Na subseção foram explicitados **dois universos**: painel equilibrado de **30 municípios** 2024 R$370,72 mi, 2025 R$320,75 mi, retração real aproximada de **13,48%**; e universo completo de **34 municípios** 2024 R$382,05 mi, 2025 R$327,94 mi, retração real aproximada de **14,16%**. A trajetória longa usa apenas painel fixo; cortes 2024/25 possuem cobertura 34/34.
- **Página 15, limites de informação:** corrigida a afirmação antiga de cobertura RGF 26/34 para **34/34 declarações do Executivo em 2025 localizadas**, mediante filtro de modalidades quadrimestral e simplificada semestral. Evidenciados os casos **Pontal, Barrinha e Orlândia** sob QA; cobertura não equivale a certificação de cumprimento da LRF.
- **Página 15 e início da Parte II:** removida a nota metadocumental ("o mapa precisa de QA ... antes de eventual reprodução") acerca do mapa de ISS por habitante; a nota agora informa a natureza do dado observado e seu limite de interpretação face ao IBS. Em outro trecho da abertura da Parte II, retirado o comando "Verificar a rubrica específica..." e preservada a necessidade substantiva de conferir os componentes legais do IBS.
- **Conclusões, 'Limites de homologação':** atualizadas para refletir o exame documental das declarações RGF 34/34, sem declarar validação fiscal completa.
- **Referências:** inseridas referências metodológicas à API pública Siconfi/STN e ao IPCA mensal IBGE/SIDRA (1737, variável 2266) no início da seção bibliográfica, preservadas as entradas anteriores.
- Título descritivo e rodapé atualizaram o número da edição para **Lote 96**, data 04/11/2026. **Mapas, figuras e matrizes SWOT não foram alterados ou redimensionados**.

## 3. Verificação de integridade e resultado da paginação

Foi utilizada a sequência **DOCX → render_docx.py → PNG de cada página + PDF → inspeção visual → novo render**. A primeira renderização revelou que notas de fonte herdavam **negrito excessivo** do DOCX do Lote 87. Na segunda passagem, a formatação dessas notas foi normalizada e o arquivo foi novamente renderizado. Versão final:

| Teste | Resultado |
|---|---|
| Extensão | **64 páginas**, contra 63 no Lote 87; crescimento decorre da nova subseção de análise |
| Integridade textual | **64/64 páginas com palavras** |
| Posicionamento | **Nenhuma caixa de palavra fora da área da página**, segundo extração geométrica de texto |
| Quadros e mapas existentes | Mantidos sem alteração no documento-fonte, com observação nas pranchas renderizadas |
| Metalinguagem pesquisada | Nenhuma ocorrência restante dos trechos de controle "Markdown", "Lote 87", "precisa de QA" e cobertura RGF 26/34 no PDF final |
| Inspeção | Realizada por pranchas de contato de 64 páginas e inspeção ampliada das páginas 6, 14, 15 e final |
| Conclusão | **QA gráfico e textual básico da versão incrementada aprovado; homologação jurídica, quantitativa integral e documental ainda pendente** |

Trilha local de reprodutibilidade:
- `/mnt/data/RMRP_LOTE96_QA/revisar_volume_ii_lote96.py` — script de alteração editorial.
- `/mnt/data/RMRP_LOTE96_QA/QA_LOTE96.json` — verificação geométrica de 64 páginas.
- `/mnt/data/RMRP_LOTE96_QA/render/` — 64 PNGs e PDF da versão produzida.
- `/mnt/data/RMRP_VOLUME_II_INTEGRACAO_FISCAL_LOTE96.docx` — nova cópia DOCX.
- `/mnt/data/RMRP_LOTE96_QA/render/RMRP_VOLUME_II_INTEGRACAO_FISCAL_LOTE96.pdf` — PDF correspondente.

**Persistência:** esta nota será preservada no repositório, enquanto os arquivos binários são anexos criados na conversa. Não declarar upload para Drive até resposta positiva de ferramenta que aceite os arquivos novos do contêiner. Nenhum arquivo do Lote 87 foi sobrescrito.

## 4. Pontos ainda condicionantes da homologação externa

1. RGF/RREO: **Pontal** apresenta no 3º quadrimestre de 2025 RCL RGF R$13.494.039,69, contra RCL RREO B6 R$209.571.785,24; ainda sob quarentena. **Barrinha** DCL/RCL A02 26,62% versus A06 31,40%; **Orlândia** A02 -6,55% versus A06 -6,59%. Conferir retificações, anexos legais e eventuais manifestações das administrações.
2. DCA I-C: permaneceram **cinco combinações sem a conta sintética**, mesmo com declaração encontrada; Cássia 2015 possui valor de RREO alternativo, não incorporado. Necessário definir eventual ausência efetiva da receita com documentos de retificação.
3. Transferegov/Guariba: o contrato FNDE 043/2025 e a ordem de início foram lidos em ciclos anteriores, mas **desembolsos e pagamentos** do Termo 959097/2024 ainda não foram conciliados a partir de CSV oficial.
4. Direito: exame exaustivo da EC 132/2023, LC 214/2025 e LC 227/2026 quanto ao regime da receita média de referência e da transição do IBS; sem projeção de ganhos/perdas municipais.
5. Cenários 2027–2030: preservar as **408 combinações município–ano–cenário sem valores arbitrariamente imputados** e os 60 recortes agregados; não incorporar parâmetros não homologados.
6. Revisão externa final: verificar links, citações, texto legal atual e coerência dos demais indicadores, além da inspeção de legenda/fonte do mapa 15 na versão de produção.

**Status:** nova versão integrada de trabalho disponível, não substitui versão homologada inexistente. Ao contrário dos Lotes 88–95, este lote efetivamente **alterou em cópia separada o Volume II**, com renderização concluída e controle básico de integridade.
