# RMRP — auditoria substantiva de natureza da despesa TCESP (19/10/2026)

## Escopo e evidência
Fonte: GitHub Actions [run 39208371015](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/39208371015), artefato 12166413578, SHA-256 ZIP `c41370e35b0c88eead1ff5695b5c03673c5d04a7441a781c07c7b753a31aa57e`. ZIP contém SUMMARY.json e arquivos individuais de Ribeirão Preto 2024/2025, Sertãozinho 2025 e Guatapará 2023. Scripts e testes aprovados no commit e7dfaf8f0c361b32baec21dd3f572312919858d1. Fonte primária indicada nos JSONs: arquivos CSV de despesas do TCESP. Este documento é auditoria **de triagem**, não atestado de regularidade jurídico-contábil.

## Resultados agregados dos registros candidatos

| Município | Ano | Programa e ação | Elementos identificados | Liquidação (R$) | Leitura |
| --- | --- | --- | --- | ---: | --- |
| Ribeirão Preto | 2024 | 0/30003 — Operações especiais / Pagamento de precatórios judiciais | 44909100 — Sentenças Judiciais | 16.532.808,21 | **Investigação dirigida:** identificar objeto original da obrigação judicial e vínculo com despesa de capital |
| Ribeirão Preto | 2024 | 20218/20140 — Cuida Bem Ribeirão / Operação de manutenção de cemitério | 44905199 — Outras Obras e Instalações | 1.207.168,18 | **Falso positivo semântico para dívida:** palavra “operação”; despesa registrada como obras/instalações, sujeito à verificação usual de finalidade |
| Ribeirão Preto | 2025 | 0/30003 — Operações especiais / Pagamento de precatórios judiciais | 44909100 — Sentenças Judiciais | 14.487.299,55 | **Investigação dirigida:** verificar origem judicial e natureza do dispêndio |
| Sertãozinho | 2025 | 0/1 — Amortização da dívida de longo prazo, pagamento de mapa precatório / Amortização da dívida contratada, precatórios, encargos e obrigações tributárias | 44909100 — Sentenças Judiciais | 11.766.474,22 | **Investigação prioritária:** denominação combina obrigações distintas; elemento 44909100 isoladamente não comprova classificação incorreta |
| Sertãozinho | 2025 | 57/2402 — Saneamento básico / Manter e operacionalizar | 44905239; 44905199; 44905204; 44905212; 44905299; 44905191 | 3.596.913,26 | **Falso positivo semântico para dívida:** obras, instalações e equipamentos; classificação funcional e material exige análise própria |

**Conciliação aritmética dos candidatos:** três ações do elemento 44909100 somam R$ 42.786.581,98. As duas ações selecionadas apenas por termos de operação/manutenção somam R$ 4.804.081,44. Total das cinco ações R$ 47.590.663,42. Os valores se referem a três combinações município-ano e não devem ser somados como um único total anual regional.

**Guatapará 2023:** investimento liquidado grupo 44 R$ 2.118.940,79, nenhuma correspondência de palavras-chave. Não interpretar esse zero de correspondências como inexistência de precatórios ou passivos; diferença histórica de R$ 10.176,00 ainda exige confronto específico.

## Critérios de decisão
1. O elemento 44909100 identifica sentença judicial na natureza orçamentária utilizada, mas não distingue, sozinho, se a obrigação originária decorre de investimento, custeio ou outra modalidade. Não presumir reclassificação automática.
2. A palavra “amortização” na descrição programática não prova que os R$ 11,77 milhões associados ao elemento 44909100 constituam amortização de principal da dívida; exige documento analítico de origem.
3. Termos “operação” e “operacionalizar” produziram falsos positivos de triagem. Manter seus registros como candidatos para verificação de finalidade material, sem classificá-los como serviço da dívida.
4. Não equiparar liquidação contábil à execução física de obras nem inferir irregularidade pela presença do elemento 44909100.
5. Preservar CSV original, ZIP/hash, exercício, estágio, elemento e códigos de programa/ação antes de qualquer eventual revisão substantiva.

## Próximas diligências
- Examinar origem e objeto dos precatórios e sentenças das três ações 44909100 (processos/descrição do empenho quando disponíveis) e atribuir estado `confirmado_capital`, `confirmado_nao_capital` ou `indeterminado`, com evidência.
- Verificar obras/equipamentos das duas ações de manutenção/operacionalização, evitando classificá-las como dívida.
- Resolver a divergência de Guatapará 2023 por diferença de universo, elemento, estágio e extração, sem substituir valores auditados.
- Cruzar essas cinco ações com a matriz dos 2.955 registros, evitando duplicidade e preservando versões do relatório regional; publicar alterações apenas após QA específico.


## Deliberação de escopo — classificação simplificada

Por orientação expressa do projeto, encerra-se a diligência para determinar a obrigação originária de cada precatório. Nas análises gerenciais, basta destacar os registros identificados como precatórios por denominação da ação, mantendo separadas eventuais sentenças judiciais sem essa indicação. Os valores oficiais de investimentos não são alterados. Pode-se apresentar, como medida **analítica** e somente quando a cobertura for suficiente, 'investimentos liquidados excluídos os precatórios identificados'. Não investigar processos individuais ou empenhos para essa finalidade. Não converter o total de todo elemento 44909100 automaticamente em precatórios quando a descrição da ação for insuficiente. As ações selecionadas apenas por 'operação'/'operacionalizar' não são precatórios e não demandam investigação judicial. A pendência de Guatapará sobre divergência de totais permanece separada desta triagem.
