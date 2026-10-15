# Auditoria de completude e coerencia editorial — RMJ
Data: 15/10/2026
Escopo: arquivo `editorial/rmj/index.html` integrado a main antes desta revisao; leitura das 23 secoes publicas, dados estaticos e textos exibidos. Auditoria documental/editorial, nao substitui revisao independente das 35 observacoes municipio-ano nem dos documentos originais do TCESP.

## Inventario de cobertura ja existente

- Receitas e despesas: contas selecionadas de IPTU, ISS, ITBI, cotas-partes de ICMS/IPVA, FPM mensal, despesa total, corrente, pessoal, investimento, juros e amortizacao; valores anuais, cobertura e participacao, 2021-2025.
- Comparacao regional: sete municipios, valores, razoes sobre receita corrente bruta ou despesa total liquidada; denominadores somados antes das divisoes.
- Evolucao: valores nominais, variacoes reais pelo IPCA medio anual do IBGE e diferencas em pontos percentuais entre 2021 e 2025.
- Interpretacao: sintese municipal dinamica das variacoes reais e da participacao, com ressalvas contra inferencia causal.
- Funcoes: urbanismo, habitacao, saneamento, transporte, gestao ambiental, saude e educacao quando observadas.
- Investimentos: conciliacao contábil DCA/TCESP em 2025 para todos os sete municipios, R$ 265.425.559,07, diferenca zero; principais programas de cada municipio; detalhamento de Jundiai por programa e duas acoes destacadas.
- Controles complementares: comparacoes historicas, concentracao, picos, series reais, cruzamentos e indicadores legais com interpretacao metodologica separada.

## Inconsistencias identificadas

1. **Confirmada e corrigida neste PR (alta):** a secao `investigacao` afirmava que a atribuicao por programa e acao nao fora verificada, contradizendo `conciliacao-rmj` e `programas-investimento`, que documentam programas dos sete municipios em 2025 e acoes de Jundiai. A nova redacao reconhece explicitamente os dados ja publicados e limita apenas a explicacao interanual, contratos e obras.
2. **Redundancia controlada (media):** `contas`, `receitas`, `reais`, `sintese` e `investigacao` retomam definicoes fiscais semelhantes. Por ora mantidas porque fazem papeis distintos (consulta, serie, deflacao, narrativa, limites); consolidar apenas se leitura editorial indicar fadiga ou incoerencia efetiva.
3. **Cobertura assimetrica (media):** a conciliacao TCESP de 2025 cobre sete municipios, mas o detalhamento de acoes destacado no texto concentra-se em Jundiai. Nao apresentar acoes de Jundiai como retrato regional nem extrapolar causalidade.
4. **Pendencia empirica real (alta):** comparar detalhamentos por programa e acao entre exercicios, rastrear mudancas de classificacao e contratos relevantes, e diferenciar liquidação de pagamento e entrega fisica.
5. **Pendencia metodologica (media):** auditar de modo independente denominadores, recortes e ausencia de dados das novas participacoes e narrativas a partir do CSV fonte antes de ampliacao para outras regioes.

## Critério para novas ampliacoes

Nao iniciar outra familia de indicadores sem verificar se ja existe no HTML, em datasets consolidados ou no inventario. Separar, por item, `ja publicado`, `calculado mas nao publicado`, `fonte incompleta` e `investigacao causal dependente`. Preservar publicacao do painel estadual em projeto distinto e bloquear merge editorial em caso de teste de navegador reprovado.
