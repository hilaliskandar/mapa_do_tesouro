# Proposta futura — integração de fontes federais à plataforma fiscal municipal

Estado: **proposta para estudo em fase posterior**, sem iniciar ingestão, alterar indicadores existentes ou criar vínculos contábeis automáticos.

## Objetivo
Examinar a viabilidade de incorporar à plataforma dados estruturados federais sobre **obras, projetos de investimento em infraestrutura, transferências intergovernamentais, convênios, execução físico-financeira e financiamentos**, complementando o atual acervo municipal fiscal. A nova camada deve preservar origem, data de referência, competência territorial e estágio de execução e não confundir projeto, compromisso, transferência efetiva e despesa municipal liquidada.

## Fontes iniciais e evidências oficiais verificadas em 26/10/2026
1. **Obrasgov.br** — portal de dados abertos descreve API para projetos de investimento em infraestrutura, incluindo geolocalização e acompanhamento de obras. Documentação e entrada: https://www.gov.br/obrasgov/pt-br/ferramentas-de-gestao-e-transparencia/api-de-dados-abertos-obrasgov-br_novo ; serviço https://api-publica.obrasgov.gestao.gov.br.
2. **Transferegov.br** — em julho de 2026 foi anunciado novo ambiente de APIs e arquivos CSV: https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br ; https://api-publica.transferegov.gestao.gov.br. API de dados abertos inicialmente para **Gestão de Parcerias** e **Transferências Especiais**; arquivos do módulo **Discricionárias e Legais**. O calendário oficial anunciado para APIs deste último módulo vai de atos preparatórios (até outubro/2026) a módulo de obras (até outubro/2027), portanto a existência e cobertura reais precisam ser revalidadas no momento de executar.
3. **Conecta gov.br** — catálogo https://www.gov.br/conecta/catalogo/ e https://www.gov.br/conecta/catalogo/catalogo_api. O catálogo inclui interfaces de gestão orçamentária, financeira, controle, cadastros e infraestrutura. **Catálogo não significa API pública sem credenciamento**: identificar para cada serviço público-alvo credenciais, condições de uso e autorização institucional.
4. **Caixa Econômica Federal** — investigar, sem pressupor API aberta, portais e bases estruturadas de repasses, mandatos da União, contratos, financiamento e operações urbanas/habitacionais. Identificar titularidade, escopo público, atualização, disponibilidade de arquivos oficiais e possibilidade de integração lícita.
5. **Demais fontes federais** — seleção orientada pelas lacunas analíticas identificadas no núcleo fiscal: Portal da Transparência/CGU, Tesouro Nacional/Siconfi, PNCP (quando pertinente a obras e contratação), dados.gov.br e fontes de execução orçamentária e transferências. Verificar interfaces e licenças, sem declarar endpoints não testados.

## Escopo de descoberta técnica
- Inventário de endpoints, documentação OpenAPI/Swagger, páginas de dados abertos e conjuntos de download; requisitos de autenticação, autorização, cotas e estabilidade.
- Campos de identificação de município (preferencialmente código IBGE), CNPJ do executor e do beneficiário, identificador de instrumento/obra, localização, tipo de objeto, fontes de financiamento, previsão, empenho, desembolso, liquidação, pagamento, avanço físico, vigência e situação.
- Identificação de **duplicações intersistemas** (mesmo projeto em Obrasgov/Transferegov/Caixa) e de efeitos de dupla contagem nas finanças municipais; construir chaves de cruzamento e proveniência antes de indicadores agregados.
- Cobertura por município e exercício, temporalidade, unidades monetárias, qualidade geográfica, status não informado versus zero, retificações e versões de API.
- Teste inicial apenas em conjunto reduzido e auditável de municípios, sem ingestão direta na base canônica; depois propor modelo de dados, QA, relatórios, visualização em mapas e publicação isolada.

## Condições para a futura implementação
1. Entregar matriz de fontes com **URL oficial**, tipo de acesso (aberto/credenciado/arquivo), cobertura, campos, atualização, licença, estabilidade e teste de amostra.
2. Desenhar entidade de projeto/obra/instrumento e relações com municípios, execução financeira, repasses e indicadores fiscais; deduplicar referências.
3. Aprovar regras de interpretação: transferências recebidas não equivalem automaticamente a investimento municipal; valor de convênio não equivale a desembolso; avanço físico não equivale a liquidação; financiamento não equivale a receita tributária.
4. Implantar pipeline incremental e reproduzível com snapshots, hashes, trilha de revisão e auditoria de completude; preservar publicação corrente até homologação.
5. Preparar visualizações territoriais e indicadores de investimentos e transferências federais somente com proveniência validada.

## Prioridade e continuidade
**Fila futura, após avançar na conciliação documental TCESP–DCA.** Primeiro estudo de viabilidade com Obrasgov e Transferegov, depois Caixa e restante do catálogo Conecta, sem tornar a entrada em produção dependente de APIs cujo acesso não esteja liberado.

Links de referência revisados: https://www.gov.br/transferegov/pt-br/comunicados/comunicados-gerais/2026/comunicado-no-23-2026-do-portal-do-transferegov.br e páginas oficiais citadas acima.
