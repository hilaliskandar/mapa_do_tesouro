# Estado do projeto

Data de referência: 2026-10-07.

## Estado operacional

A `main` é a fonte de verdade.

O baseline público TIC-TIM 30 está publicado e protegido por CI, QA de paridade e contratos metodológicos. A infraestrutura de deploy automático está ativa.

A expansão estadual já ultrapassou a prova conceitual: o pipeline processa 645 municípios em piloto privado, a aquisição direta DCA do Siconfi possui smoke test e crosscheck contra o baseline publicado, e existe acervo histórico local no Google Drive com os anexos FINBRA/DCA estaduais organizados por exercício.

## Hierarquia de fontes operacionais

Para reconstrução histórica e processamento em lote, deve-se preferir o acervo local do Google Drive antes de realizar coleta externa em massa.

Pasta canônica de trabalho FINBRA/SP:
`https://drive.google.com/drive/folders/1K_Raj0pKEyktVY5BVa_raOZ4cQdJ8HQ4`

A pasta contém diretórios anuais de 2013 a 2025, a base `FINBRA_DCA_CANONICA_FINAL_2013_2025_2026-09-26`, caderno metodológico e diversos artefatos de QA e tratamento.

Regra operacional:

1. Google Drive local = fonte preferencial para reconstrução histórica, cargas em lote e reprocessamento;
2. Siconfi externo = validação por amostra, atualização incremental, confirmação de versão e investigação de lacunas/divergências;
3. coleta externa integral só deve ocorrer quando não houver arquivo local equivalente, quando a versão local estiver desatualizada ou quando houver necessidade explícita de auditoria independente.

Essa regra reduz carga desnecessária sobre os serviços externos e melhora a reprodutibilidade.

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

### Gate A

O Gate A formal usa aquisição direta do Siconfi para um exercício completo como teste de auditoria independente e de robustez da rotina de coleta.

Para expansão temporal, não se deve repetir por padrão esse padrão de 1.935 requisições por ano se o acervo local contiver os três anexos equivalentes.

### Gate B — série DCA

A série deve ser construída prioritariamente a partir do acervo local do Drive.

Já verificado:

- 2023: anexos estaduais I-C, I-D e I-E disponíveis em XLSX;
- 2024: anexos estaduais I-C, I-D e I-E disponíveis em XLSX;
- 2025: anexos estaduais I-C, I-D e I-E disponíveis em CSV;
- diretórios anuais também existem para 2013–2022.

O Siconfi deve ser usado no Gate B para sentinelas, divergências, lacunas e atualização incremental.

## Sequência recomendada

### Gate A — DCA estadual

Concluir a execução estadual controlada de 2025, validar cobertura e performance e armazenar o resultado como artifact/snapshot de QA.

### Gate B — série DCA

Ingerir e harmonizar a série histórica a partir dos arquivos locais do Drive, começando por 2023–2025 e depois retrocedendo progressivamente até 2013. Em cada exercício, registrar hash, estrutura, cobertura e paridade por sentinelas com o Siconfi.

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
4. consultar primeiro o acervo local do Drive antes de planejar coleta externa em massa;
5. ler o documento específico do gate em andamento;
6. nunca reabrir ramo superado sem justificar no changelog;
7. registrar toda decisão metodológica antes de alterar dados publicados.
