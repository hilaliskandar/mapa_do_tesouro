# Lote 64 — Recuperação operacional do acervo cartográfico do Volume I para o Volume II

Data: 02/11/2026. **Estado:** fontes cartográficas preexistentes localizadas e conferidas por metadados/consulta textual; reutilização editorial organizada. Não declara recuperação do arquivo vetorial, exportação de PNG individuais ou inspeção visual completa.

## Acervo efetivamente localizado

1. **Matriz original de 16 indicadores:** `RMRP_VOLUME_PUBLICO_MAPAS_E_ANALISES_16_INDICADORES_2026_10_19.pdf`, Google Drive ID `10vbnQ_eBNsSmpWekFrrgJyeyTeNlm3YN`, PDF 4.666.919 bytes, 19/10/2026, link https://drive.google.com/file/d/10vbnQ_eBNsSmpWekFrrgJyeyTeNlm3YN/view . Inventário existente `editorial/rmrp/INVENTARIO_16_MAPAS_2026_10_28.md` identifica 16 mapas em quatro mosaicos das páginas 2, 3, 6 e 7.
2. **Volume I cartográfico de trabalho:** `RMRP — Trabalho cartográfico 16 indicadores — 28-10-2026`, Google Docs ID `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`, modificado 31/10/2026; texto legível conferido (aproximadamente 110 mil caracteres), link https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit .
3. Inventário GitHub documenta estágio final anterior: **16 imagens/51 tabelas no Google Doc**, exportação de prova de 74 páginas; é registro histórico de QA, não contagem estrutural atual revalidada por API Docs nesta execução.
4. **Arquivo vetorial original:** não localizado nem inspecionado nesta diligência. A existência e reutilização de mapas cartográficos preexistentes foi comprovada; isso **não verifica individualmente CRS, geometrias ou topologia** da fonte vetorial.

## Matriz de reaproveitamento — selecionar apenas indicadores pertinentes

| Mapa Volume I | Tema | Inserção no Volume II | Tratamento |
|---|---|---|---|
| 1 | Receita corrente por habitante | Parte I, seção 2, trajetórias e desigualdades | Reutilizar com ano/escala explícitos, sem interpretar como gráfico de variação histórica |
| 2 | IPTU, ISS e ITBI / receita corrente | Parte I, seção 3, composição | Reutilizar com nota: composição tributária observada, não exposição líquida IBS |
| 3 | FPM, ICMS e IPVA / receita corrente | Parte I, seção 3, transferências | Reutilizar para contrastar origem dos ingressos, preservando denominação da rubrica |
| 5 | IPTU por habitante | Parte I, seção 4, diferenças municipais | Complementar, não central ao mecanismo IBS |
| 6 | ISS por habitante | Parte II, antes das matrizes municipais | Reutilizar com nota obrigatória: verificar se indica ISS principal ou total, e ano |
| 7 | ITBI por habitante | Parte I, estrutura tributária | Opcional, não confundir com IBS |
| 8 | FPM por habitante | Parte I, sub-regiões e autonomia | Reutilizar com ressalva sobre transferência constitucional |
| 9 | Despesa corrente por habitante | Parte I, seção 5, custeio | Opcional |
| 10 e 11 | Pessoal e encargos por habitante / receita | Parte I, pressão do custeio | Usar apenas como DCA, não índice legal DTP/RCL |
| 14 | Investimento liquidado por habitante | Parte I, seção 5, investimento | Reutilizar; distinguir investimento por habitante nominal e real conforme legenda |
| 15 | Evolução real dos investimentos entre triênios | Parte I, seção 5, dinâmica de capital | **QA obrigatório:** classe intermediária cruza zero (−10,6% a +16,7%); não atribuir sentido positivo/negativo só por cor |
| 16 | Oscilação de investimentos 2021–2025 | Parte I, trajetória e volatilidade | Uso seletivo, nota sobre intervalo e metodologia |

Os mapas 4, 12 e 13 (saúde e educação) têm pertinência secundária ao Volume II tributário e devem ser preservados como evidência contextual do Volume I, evitando ampliar texto sem função argumentativa.

## Política editorial de integração

- Inserir material cartográfico em sequência argumentativa correspondente, não em atlas autônomo.
- Reutilizar as figuras existentes em lugar de recriar geometria; priorizar imagem individual com legenda legível quando houver versão verificada.
- O manuscrito Markdown pode referenciar as fontes do Drive imediatamente, mas isso **não equivale a ter embutido arquivos raster em seu repositório**; eventual publicação em PDF requer incorporar os bytes de imagem e confirmar resolução e direitos de uso.
- Não transformar PDF em vetor cartográfico, nem dizer que QA espacial foi realizado por inspeção dos mapas estáticos.
- Para eventual mapa *novo* de ISS+ICMS, recuperar a mesma geometria de origem e conferir 34 chaves IBGE, CRS preferencial EPSG:4674, integridade topológica, dados em reais/preços adequados e classificação frio→quente.

## Resultado e pendências

**Resolvido:** não é necessária nova solicitação de mapas ou geometrias ao usuário; os 16 mapas originais e a edição de trabalho são localizáveis no Drive; inventário de reaproveitamento por capítulo preparado.

**Pendente:** identificar acesso ao vetorial original; recuperar/exportar recortes gráficos originais como arquivos independentes; QA visual das legendas e incorporar os raster efetivamente no relatório final. Até lá, usar referências ao acervo validado, não representar o mapa M1 como novo produto concluído.
