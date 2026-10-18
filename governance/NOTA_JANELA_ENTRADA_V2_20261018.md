# Janela historica no construtor privado

A verificacao do codigo localizou em pipeline/build/sp645_private_input.py uma exigencia explicita dos anos 2021 a 2025 nas linhas 62-64. O modulo tambem grava metadados dessa janela nas linhas 118-148. Portanto, a restricao antecede a exportacao da API v2. Para ampliar a exposicao, integrar dados DCA 2013-2025 ja existentes e testar harmonizacao, disponibilidade, manifesto, paridade e regressao. Mudar apenas a constante dos anos nao seria suficiente.
