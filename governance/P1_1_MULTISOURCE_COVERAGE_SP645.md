# P1.1 — Cobertura multifuentes SP645

Data de referência: 2026-10-09.

## Objetivo

Consolidar a cobertura por variável, fonte, exercício e universo após o fechamento do Gate F, preservando os quatro estados canônicos:

- `observado`;
- `ausente`;
- `nao_aplicavel`;
- `em_revisao`.

A cobertura foi recalculada a partir da tabela final `observacao`, após os cálculos anuais, e não apenas a partir da ingestão inicial.

## Artefato de referência

Run estadual privado: `37886745605`.

Artifact: `11596229685`.

SHA-256: `8c7fbbbc6506bb7f820a0af934a4a1eee3a02b167eae6578e3fab1cef0af8927`.

Resultado estrutural:

- 645 municípios;
- 271 linhas de cobertura variável × ano;
- 271 linhas de cobertura variável × ano × fonte;
- zero linhas implícitas classificadas como ausência após o refresh;
- cobertura exportada em `coverage.json`;
- contribuição por fonte exportada em `coverage_sources.json`.

## Escopo temporal efetivo

### 2021–2022

O build estadual não contém DCA completo nesses exercícios. O histórico mínimo contém três indicadores DCA já harmonizados:

- receita tributária / receita corrente: 645/645;
- investimento / receita corrente: 645/645;
- despesa territorial / despesa total: 56/645 em 2021 e 66/645 em 2022.

As demais variáveis DCA aparecem como `nao_aplicavel` porque sua disponibilidade no mapping estadual começa em 2025.

### 2023–2024

Além dos três indicadores DCA anteriores, entram os indicadores históricos do RGF:

2023:
- DTP/RCL: 527/645;
- DCL/RCL: 527/645;
- DC/RCL: 471/645;
- despesa territorial / despesa total: 65/645.

2024:
- DTP/RCL: 530/645;
- DCL/RCL: 530/645;
- DC/RCL: 481/645;
- despesa territorial / despesa total: 72/645.

Portanto, 2021–2024 devem continuar descritos como **histórico mínimo para tipologias e comparação temporal**, e não como série estadual multifuentes completa.

## Cobertura 2025 por fonte

### SICONFI DCA

29 variáveis no mapping.

Células:
- observadas: 15.065;
- ausentes: 3.640;
- total esperado: 18.705.

A maior parte das contas centrais tem cobertura quase completa:

- receita corrente bruta: 644/645;
- receita tributária bruta: 644/645;
- despesa total liquidada: 644/645;
- investimentos liquidados: 644/645;
- pessoal e encargos: 644/645;
- ICMS cota-parte: 644/645;
- FPM: 643/645;
- IPTU: 643/645;
- ISS: 643/645;
- IPVA: 643/645;
- ITBI: 641/645;
- urbanismo: 639/645;
- transferências de capital: 622/645.

As lacunas materiais concentram-se em contas naturalmente mais esparsas ou potencialmente omitidas quando nulas:

- inversões financeiras liquidadas: 54/645;
- habitação liquidada: 146/645;
- operações de crédito: 152/645;
- alienação de bens: 269/645;
- juros e encargos liquidados: 309/645;
- saneamento liquidado: 330/645;
- transporte liquidado: 458/645;
- gestão ambiental liquidada: 527/645;
- amortização da dívida liquidada: 553/645.

Essas ausências **não devem ser convertidas em zero** sem verificação da semântica do demonstrativo. A issue #117 foi aberta para esse saneamento.

### SICONFI RGF Anexo 01

- despesa total com pessoal: 530/645;
- DTP/RCL: 530/645.

A lacuna principal é de cobertura municipal do demonstrativo, aproximadamente 115 municípios no snapshot usado.

### SICONFI RGF Anexo 02

12 variáveis no mapping.

Coberturas principais:

- dívida consolidada: 577/645;
- dívida consolidada líquida: 530/645;
- deduções da dívida consolidada: 530/645;
- disponibilidade de caixa: 530/645;
- restos a pagar processados: 510/645;
- dívida contratual: 454/645;
- parcelamento de dívidas: 373/645;
- demais haveres financeiros: 300/645;
- precatórios vencidos não pagos: 265/645;
- outras dívidas: 52/645.

Há dois tipos distintos de lacuna:

1. município sem demonstrativo válido no snapshot;
2. linha/componente ausente dentro de município que possui RGF02.

A segunda situação não pode ser interpretada automaticamente como zero. É necessário verificar o leiaute e a semântica da API/demonstrativo antes de qualquer preenchimento.

### SICONFI RGF Anexo 05

- caixa líquido após RPNP: 528/645.

### SICONFI RREO

- RCL oficial: 531/645.

### Tesouro CAPAG

4 variáveis no mapping.

- nota CAPAG: 645/645;
- conjunto das quatro variáveis: 2.554 células observadas em 2.580 esperadas.

A nota final possui cobertura completa; as 26 ausências restantes pertencem a componentes específicos do snapshot, preservadas como ausência.

### Derivados do pipeline

26 variáveis.

Células:
- observadas: 10.421;
- ausentes: 6.349.

A cobertura dos derivados é consequência direta da política estrita: o indicador só é observado quando os insumos necessários estão observados. A expansão de cobertura dos derivados só poderá ocorrer após saneamento semântico das fontes, nunca por imputação automática.

## Indicadores e agregações de menor cobertura em 2025

Cobertura inferior a 25%:

- diferença de capital selecionada: 13/645;
- despesas de capital selecionadas: 46/645;
- RGF02 outras dívidas: 52/645;
- inversões financeiras: 54/645;
- despesa territorial e seus derivados: 65/645;
- receitas de capital selecionadas: 78/645;
- habitação: 146/645;
- operações de crédito: 152/645.

Cobertura entre 25% e 50%:

- precatórios vencidos não pagos: 265/645;
- alienação de bens: 269/645;
- demais haveres financeiros: 300/645;
- serviço da dívida liquidado: 303/645;
- juros e encargos: 309/645.

Cobertura entre 50% e 80%:

- saneamento: 330/645;
- parcelamento de dívidas: 373/645;
- dívida contratual: 454/645;
- transporte: 458/645;
- DC/RCL: 476/645;
- restos a pagar processados: 510/645.

Cobertura entre 80% e 95%:

- gestão ambiental: 527/645;
- caixa líquido após RPNP: 528/645;
- DTP/RCL: 530/645;
- DCL/RCL: 530/645;
- RCL oficial: 531/645;
- amortização da dívida: 553/645;
- dívida consolidada: 577/645.

Cobertura igual ou superior a 95%:

- transferências de capital: 622/645;
- todos os principais agregados de receita corrente, tributação, investimento, despesa total, saúde, educação e transferências correntes: entre 639 e 645 municípios;
- CAPAG: 645/645.

## Interpretação

A base estadual de 2025 já é adequada para:

- comparação fiscal geral;
- receita corrente e tributária;
- investimento;
- principais transferências;
- CAPAG;
- pessoal e dívida com cobertura explicitamente documentada.

Ainda exige cautela para:

- composição funcional territorial;
- contas de capital esparsas;
- serviço da dívida por componentes;
- decomposição detalhada do RGF02.

A baixa cobertura dessas variáveis não deve ser confundida com inexistência econômica do fenômeno. Em especial, linhas omitidas em demonstrativos podem representar zero, ausência ou não preenchimento conforme a regra de cada fonte.

## Decisão de P1.1

P1.1 está concluída como etapa de inventário e consolidação de cobertura.

Foram corrigidas duas lacunas estruturais:

1. o estado `em_revisao` passou a integrar a cobertura canônica;
2. a cobertura passou a ser recalculada depois das transformações e ganhou visão separada por fonte.

A próxima etapa é P1.2, com recálculo **seletivo** somente depois de verificar a semântica das ausências nas fontes.

Prioridades P1.2:

1. issue #117 — semântica de linhas DCA esparsas;
2. qualificar a distinção entre ausência municipal e linha esparsa no RGF02;
3. recalcular derivados apenas onde houver regra documental defensável;
4. registrar delta de cobertura antes/depois;
5. preservar todo caso não demonstrado como ausência.
