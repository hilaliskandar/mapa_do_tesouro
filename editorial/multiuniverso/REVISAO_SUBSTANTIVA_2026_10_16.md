# Revisão substantiva das sínteses editoriais — 16/10/2026

## Escopo e método
Revisão do código gerador dos dez boletins e das regras de comunicação dos indicadores, confrontadas com o contrato publicado em `governance/PUBLICATION_API.md` e com as salvaguardas editoriais da RMJ. Esta auditoria **não** é uma nova verificação de valores do Siconfi ou de cada JSON individual.

## Achados
1. **Seleção arbitrária — corrigida no gerador.** Anteriormente a síntese tomava as três primeiras variáveis por tema na ordem do payload. A nova regra usa ordem alfabética do rótulo, explicitamente identificada como amostra ilustrativa, sem atribuir primazia econômica.
2. **Unidades heterogêneas — contenção.** As narrativas passam a exigir unidades quantitativas reconhecidas; a tabela integral mantém indicadores de outras unidades. É necessária auditoria posterior do catálogo de unidades e dos casos categóricos, sem conversionismo automático.
3. **Cobertura incompleta — controle preservado.** As sínteses exigem `observed = expected = member_count`, quartis ordenados e pelo menos quatro municípios. Os quadros preservam coberturas menores.
4. **Interpretação limitada.** Medianas e quartis permitem caracterizar heterogeneidade, mas não explicam fatores determinantes, não quantificam evolução real e não demonstram entrega física de investimentos.
5. **Comparabilidade com RMJ — parcial.** O boletim de Jundiaí possui decomposição independente TCESP por programas/ações e narrativas municipais; os dez boletins E2 expõem a API DCA/RGF/RREO/CAPAG, não equivalem àquele módulo especializado.
6. **Hierarquia temática — sujeita a dicionário.** Agrupamento no E2 depende de palavras-chave e não constitui classificação contábil oficial. A futura edição aprovada deve adotar metadados/catálogo explícitos para toda variável, antes de ampliar conclusões.
7. **Histórico.** A série de medianas deve ser interpretada como a mediana dos municípios disponíveis em cada ano; mudanças na composição da amostra impedem afirmar trajetória homogênea.

## Aceite pendente
- Auditoria da tabela `variavel_id → unidade → tema → fonte → interpretação` com base no catálogo canônico.
- Revisão de uma amostra estratificada de indicadores: receita, despesa, funções territoriais, demonstrativos legais e CAPAG em universos de tamanhos distintos.
- QA remoto HTTP de uma prévia própria, inclusive metadados das fichas; Playwright local já executado.
- Decisão sobre aprofundamento das narrativas e a replicação (ou não) do módulo TCESP por programa/ação.
- Nenhum merge/implantação para produção até deliberação dos gates.

O PR #198 permanece versão candidata, sem alterar o boletim RMJ nem o painel estadual.
