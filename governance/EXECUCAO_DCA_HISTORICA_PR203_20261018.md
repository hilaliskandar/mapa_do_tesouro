# Execução real do exportador histórico — 18/10/2026

O exportador `pipeline/build/export_dca_historical_v2.py`, integrado pelo PR #203, foi recuperado pelo conector GitHub e executado em ambiente isolado com o CSV canônico `DCA_SP_645_2013_2025_CANONICO.csv`. A conexão git clone pelo terminal não estava acessível; foi usada uma cópia fiel do código exibido pelo conector.

## Conferências realizadas

- Fonte SHA-256: `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`; corresponde ao Gate B.
- Exportação: 645 JSONs municipais, um manifesto, 8.385 pares município-ano, 26 variáveis, exercícios 2013–2025.
- Valores: 177.221 observados e 40.789 ausentes, preservando textos decimais e a distinção entre ausência e zero.
- Auditoria independente sobre o CSV e os JSONs: 218.010 células comparadas; zero divergências.
- Total de JSONs exportados: 646. SHA-256 do manifesto produzido: `905ecb016866abca3887b66cf1ea5681333147aeac1dcb920ee1491a7b61af30`.
- Relatório integral com hash de cada JSON e pacote ZIP foram gerados como anexos nesta conversa.

## Limites

Esta execução não modifica o portal público nem integra automaticamente o histórico aos endpoints estaduais existentes da API v2. O manifesto mantém `publication_qa=not_evaluated`. A concordância comprova fidelidade ao CSV canônico, não acurácia independente de cada declaração fiscal nem equivalência temporal sem o crosswalk.

## Próximo portão

Definir um contrato de descoberta histórico separado, com versão, rotas, catálogo, proveniência e esquema consistente; testar publicação como prévia independente; confrontar possíveis conflitos com a API v2 2021–2025 sem substituir os valores já homologados; somente depois propor implantação e integração editorial para LiteLLM.
