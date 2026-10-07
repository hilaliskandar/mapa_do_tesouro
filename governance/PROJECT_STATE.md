# Estado do projeto

Data de referência: 2026-10-07.

## Estado operacional

A `main` é a fonte de verdade.

O baseline público TIC-TIM 30 está publicado e protegido por CI, QA de paridade e contratos metodológicos. A infraestrutura de deploy automático está ativa.

A expansão estadual já ultrapassou a prova conceitual: o pipeline processa 645 municípios em piloto privado e a aquisição direta DCA do Siconfi possui smoke test e crosscheck contra o baseline publicado.

## Baseline público

- universo: `TIC_TIM_30`;
- período: 2013–2025;
- release funcional: v0.1.1;
- produção: `https://finbra-tic-tim-referencia.pages.dev`;
- preview: `https://preview.finbra-tic-tim-referencia.pages.dev`;
- metodologia territorial: `strict_complete`.

Esse baseline não deve ser substituído por cargas estaduais incompletas.

## SP_645

### Estado atual

`pilot_scale`.

O snapshot estadual de receitas 2020–2023 é prova de escala e infraestrutura. Ele contém apenas variáveis semanticamente compatíveis e não constitui baseline estadual.

### Próximo gate

Construir uma primeira carga DCA estadual auditável diretamente do Siconfi, preservando arquivos brutos, manifestos, hashes, normalização e cobertura.

Critério de aceite mínimo:

1. 645 códigos municipais reconhecidos;
2. nenhum município descartado silenciosamente;
3. falhas de aquisição explicitadas;
4. três anexos DCA tratados conforme contrato;
5. cobertura variável a variável;
6. paridade com sentinelas TIC-TIM 30;
7. ausência preservada;
8. artefatos brutos e normalizados com SHA-256;
9. tempo de execução e volume registrados;
10. nenhuma publicação automática no baseline atual.

## Sequência recomendada

### Gate A — DCA estadual

Executar aquisição estadual controlada para um exercício recente, validar cobertura e performance e armazenar o resultado como artifact/snapshot de QA.

### Gate B — série DCA

Expandir progressivamente para a janela necessária, sem misturar estágios ou códigos incompatíveis.

### Gate C — população

Integrar denominadores anuais compatíveis antes de promover indicadores per capita.

### Gate D — RREO/RGF

Integrar RCL, pessoal, dívida e liquidez pelos demonstrativos próprios.

### Gate E — CAPAG

Integrar classificação e componentes oficiais, com data de posição identificada.

### Gate F — baseline estadual

Somente então gerar indicadores derivados, tipologias, pares, static-first e candidate estadual.

## Regras para retomada

Em nova conversa ou sessão:

1. ler este arquivo;
2. verificar `main`, PRs abertos e CI;
3. ler `INVENTORY.md`;
4. ler o documento específico do gate em andamento;
5. nunca reabrir ramo superado sem justificar no changelog;
6. registrar toda decisão metodológica antes de alterar dados publicados.
