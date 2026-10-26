# Diligência documental — acesso aos originais da DCA via API Siconfi

Data: 26/10/2026. Fase: preparação da verificação documental dos dez maiores desvios TCESP–DCA.

## Constatações em fontes oficiais
- A documentação [Siconfi API do Tesouro](https://apidatalake.tesouro.gov.br/docs/siconfi/) declara base `https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/`, formato JSON e **limite de uma requisição por segundo**, com 5.000 itens por página por padrão.
- No catálogo de serviços do [Conecta gov.br](https://www.gov.br/conecta/catalogo/apis/siconfi-extratos-das-declaracoes-contabeis), a integração está identificada como **API externa** e cobre DCA, RREO, RGF, MSC e **extrato de entregas**.
- O contrato público expõe as operações **`/dca`**, com conteúdo dos quadros anuais, e **`/extrato_entregas`**, para relatórios homologados e retificados. É necessária inspeção da especificação OpenAPI para estabelecer os parâmetros exatos antes de qualquer consulta automatizada.
- O Siconfi possui [consulta de histórico de declarações](https://siconfi.tesouro.gov.br/siconfi/pages/public/consulta_historico_declaracoes/historico_declaracoes_list.jsf), que distingue declarações homologadas e não homologadas; a consulta requer filtros de ente, exercício, poder e instituição.
- A orientação oficial [para DCA 2023](https://siconfi.tesouro.gov.br/siconfi/pages/public/arquivo/conteudo/2024_Regras_Gerais_e_Instrucoes_de_preenchimento_DCA_2023.pdf) identifica o **Anexo I-D** como demonstração das despesas por natureza e prevê regra de compatibilização do total liquidado do Anexo I-D com parcelas do Anexo I-E. Isso não resolve automaticamente o confronto com o grupo 44 TCESP.

## Hipóteses e limites
A confirmação de que o Siconfi mantém histórico de declarações e extratos de homologação permite planejar a verificação de **versão/retificação** dos dez pares prioritários. Entretanto, **não se obtiveram ainda registros DCA individuais por município nem versões de declaração** nesta diligência. Tampouco há comprovação de que o endpoint de DCA forneça, sozinho, todas as versões históricas; o extrato e o histórico público precisam ser examinados separadamente.

## Próxima operação reprodutível
1. Recuperar a especificação OpenAPI do Siconfi e verificar os parâmetros oficiais de `/dca` e `/extrato_entregas`, preservando a versão do contrato.
2. Escolher inicialmente os pares 3548807/2023, 3554102/2024 e 3545209/2023, já reproduzidos nos ZIPs TCESP.
3. Para cada par, solicitar a linha exata DCA `Anexo I-D` / `Despesas Liquidadas` / `DO4.4.00.00.00.00`, com URL e data da consulta, total de linhas, situação, referência e resposta bruta ou hash. Implementar paginação e frequência <= 1 requisição/segundo.
4. Consultar os respectivos extratos de entrega e histórico para datas de homologação, retificação e eventuais versões; documentar indisponibilidades explicitamente.
5. Comparar com a extração canônica de 2013–2025 e os valores TCESP independentes; explicar apenas diferenças documentalmente demonstradas, sem imputar causa à fonte.

Nenhuma base canônica, API ou publicação foi alterada. Este documento não afirma que qualquer divergência tenha sido explicada.
