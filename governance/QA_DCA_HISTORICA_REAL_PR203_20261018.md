# Conferencia independente do CSV DCA canonico 2013-2025

Data: 18/10/2026. Fonte: arquivo Drive DCA_SP_645_2013_2025_CANONICO.csv. SHA-256 verificado: `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`.

A leitura integral do arquivo identificou 8385 pares municipio-ano unicos, 645 municipios e 13 exercicios de 2013 a 2025. O CSV possui 26 variaveis normalizadas e 218010 posicoes de valor, sendo 177221 preenchidas com numero decimal finito e 40789 celulas vazias. Nao foram encontrados codigos IBGE invalidos, pares duplicados, divergencias de esquema, anos inesperados ou registros com qa_issue_count diferente de zero.

O exportador isolado foi integrado pelo PR 203 no commit `8163e0efc34b9d0ce85790988b02aab03b07b6f0`, apos Core CI, SP645 Scale Test e Pages Preview aprovados. A auditoria numerica mencionada aqui foi uma **validacao independente do CSV original**; **nao equivale a executar literalmente o exportador** `pipeline/build/export_dca_historical_v2.py` sobre o CSV real. Essa execucao e a comparacao byte a byte de uma amostra de JSONs seguem pendentes. Nenhum endpoint publico ou dado contábil foi modificado.

Proximo gate: executar exportador real em ambiente isolado, verificar manifesto, 645 JSONs municipais, contagem e estado de cada observacao, reconciliação por ano e variável e hashes dos produtos; depois decidir, em PR separado, como ligar o contrato historico ao indice v2 sem afetar a tipologia 2021-2025.
