# G30 — Gate de incorporação editorial — 2026-11-06

## Resultado verificado
O caderno de trabalho G30 contém 34 textos municipais individualizados e cinco conjuntos territoriais (matriz metropolitana e quatro sub-regionais), totalizando 39 entradas. Foi gerada matriz CSV local com colunas: escala, território, sub-região, tema dominante, indicadores numéricos citados, fonte de confronto, texto proposto, ressalva específica, status e controle pendente.

Conferência estrutural: 15 municípios em Ribeirão Preto, seis em Jaboticabal, seis em Mococa e sete em Batatais. Os 34 nomes são distintos. A matriz e o relatório de gate foram salvos como artefatos locais da sessão em `/mnt/data/RMRP_G30_MATRIZ_INCORPORACAO_39_TERRITORIOS_2026_11_06.csv` e `/mnt/data/RMRP_G30_RELATORIO_GATE_INCORPORACAO_2026_11_06.md`. **Esses caminhos são locais à sessão e não constituem persistência binária permanente no GitHub.**

## Bloqueio de integração
Busca de arquivos no Drive por `name contains 'G29'`, `name contains 'G28'` e `name contains 'LOTE98'` não encontrou o binário G29. O fechamento G29 do repositório informa que o DOCX e PDF (69 páginas, 45 tabelas, 16 imagens) estavam no ambiente de trabalho original, não no GitHub. A pesquisa no ambiente atual localizou os cadernos G30, mas não o DOCX G29.

**Consequência:** a matriz apresenta 39 propostas pendentes e zero alterações diretamente integradas à G29. Não reconstruir a edição definitiva sobre arquivos anteriores ao G29.

## Critérios de incorporação
1. Comparar cada texto ao quadro municipal/sub-regional na G29, respeitando variações nominais/reais, intervalos e índices de IPCA.
2. Preservar notas fiscais de Pontal, Barrinha e Orlândia; de projetos em Guariba; divergência TCESP/DCA de Guatapará; método cartográfico aplicável a Santa Rosa de Viterbo.
3. Resguardar os 45 quadros/tabelas e as 16 mídias, com conferência por hash e renderização.
4. Adotar substituições seletivas e documentadas, preservando argumentos da G29 que tenham evidência mais específica.
5. Distinguir força/fraqueza (condições internas verificadas) de oportunidade/ameaça (fatores externos, não presumidos como fatos).

## Próximo passo
Recuperar o DOCX exato G29, produzir uma cópia de trabalho G30 integral, registrar diff, executar QA de tabelas, figuras, remissões, paginação e ressalvas. O estado editorial continua **G30 caderno analítico preparado, integração pendente**.
