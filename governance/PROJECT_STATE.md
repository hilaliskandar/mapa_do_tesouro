# Estado do projeto

Data de referência: 2026-10-08.

## Estado operacional

A `main` é a fonte de verdade.

O baseline público TIC-TIM 30 permanece publicado e protegido por CI, QA de paridade e contratos metodológicos.

A expansão estadual está no estado `gate_b_dca_complete`: a série DCA SP645 2013–2025 foi consolidada, versionada e armazenada no Drive e no R2 privado.

## Hierarquia de fontes operacionais

O acervo FINBRA/DCA no Google Drive é a fonte operacional preferencial para reconstrução histórica e processamento em lote:

`https://drive.google.com/drive/folders/1K_Raj0pKEyktVY5BVa_raOZ4cQdJ8HQ4`

O Siconfi externo deve ser usado para:

- validação por amostra;
- complementação incremental de lacunas;
- atualização posterior ao snapshot local;
- auditoria independente.

Não se deve repetir coleta estadual completa quando existir snapshot local adequado.

## Baseline público

- universo: `TIC_TIM_30`;
- período: 2013–2025;
- release funcional: v0.1.1;
- produção: `https://finbra-tic-tim-referencia.pages.dev`;
- preview: `https://preview.finbra-tic-tim-referencia.pages.dev`;
- metodologia territorial: `strict_complete`.

## SP_645

### Gate A — aprovado

A aquisição estadual independente de 2025 foi concluída:

- 645 municípios solicitados;
- 1.935 respostas brutas;
- zero falhas;
- 645 linhas normalizadas;
- 26 variáveis;
- zero issues;
- SHA-256 normalizado `619367dd8b2c5b3db6f7a6c902b41e2f2685616cf8560e2e852e7583f386eec7`.

### Gate B — série histórica caracterizada

Os anexos locais I-C, I-D e I-E foram inspecionados para todos os exercícios de 2013 a 2025.

A cardinalidade mínima anual na interseção dos três anexos é:

- 2013: 638;
- 2014: 625;
- 2015: 643;
- 2016: 643;
- 2017: 645;
- 2018: 643;
- 2019: 642;
- 2020: 645;
- 2021: 645;
- 2022: 644 no snapshot anual; I-C complementado localmente para 645;
- 2023: 645;
- 2024: 630 no snapshot anual; I-C complementado localmente para 645;
- 2025 local: 632;
- 2025 Gate A: 645.

O normalizador aceita CSV e XLSX locais, registra hashes, cobertura e códigos faltantes.

A fonte suplementar local de receitas foi validada empiricamente:

- 2022/Guaraçaí: 9 células preenchidas, zero conflitos, SHA-256 composto `387b61416817db342f94c86759811000ef40a627320308651ccd6e34cec7d9d0`;
- 2024/15 municípios: receitas estruturais e população presentes em 15/15, SHA-256 do suplemento `6638fece3b2849c5c24295787f32f68ea499df2eee3e418386cdf3638f6391b2`.

A primeira complementação seletiva externa foi executada para 2018:

- Anhumas (`3502408`) e Monte Aprazível (`3531407`);
- 6 respostas consultadas: 2 municípios × 3 anexos;
- zero falhas de requisição;
- os seis payloads retornaram `items=[]`;
- SHA-256 do delta normalizado `5e9aba6ee6d627eceeddd1e7648be8bd4abfe5476a34a339dd39da2ad2dd9a79`;
- decisão: preservar as lacunas como ausência confirmada da fonte atual, sem novas tentativas automáticas.

A segunda complementação seletiva externa foi executada para 2015:

- Ferraz de Vasconcelos (`3515707`) e Tanabi (`3553401`);
- 6 pares município–anexo consultados;
- zero falhas de requisição;
- os seis payloads retornaram `items=[]`;
- SHA-256 do delta normalizado `b4e0e5df5329a7eb0883914711103f870f5973049aafc9fe114db4bf735f1178`;
- decisão: classificar 2015 como `source_confirmed_absence` e retirar da fila automática.


### Crosswalk temporal concluído para receitas centrais

Foram comprovados diretamente nos arquivos locais quatro regimes:

- 2013: códigos antigos + `Receitas Realizadas`;
- 2014–2017: códigos antigos + `Receitas Brutas Realizadas`;
- 2018–2021: códigos intermediários + `Receitas Brutas Realizadas`;
- 2022+: códigos atuais + `Receitas Brutas Realizadas`.

As variantes estão explicitadas no mapping canônico. As despesas centrais permanecem no mesmo contrato observado.

### Automação e resoluções recentes

A fila seletiva do Gate B opera automaticamente em lote. Ausências confirmadas são encerradas sem nova consulta; o lote para quando recupera dados que exigem composição fill-only.

Resultados já consolidados:

- 2013, 2015, 2016, 2018 e 2019: `source_confirmed_absence`;
- 2022: resolvido por suplemento local de receitas;
- 2024: `resolved_composite_fill_only`, 645 linhas, zero conflitos, SHA-256 `81804ece28290ddaec5360b1ff57059fbb3f53ceb15e466c940f4db467f68c63`;
- 2024 está armazenado no Drive e no R2 privado em `sp_645/dca/2024/normalized.csv`.

## Gate B DCA — concluído

A série estadual canônica contém:

- 645 municípios por exercício;
- 2013–2025;
- 8.385 município-ano;
- 26 variáveis;
- zero issues de normalização;
- SHA-256 multianual `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`;
- Drive file ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`;
- R2 `sp_645/dca/2013_2025/normalized.csv`;
- manifesto R2 `sp_645/dca/2013_2025/manifest.json`.

A fila seletiva DCA está vazia. As lacunas não recuperáveis em 2013, 2014, 2015, 2016, 2018 e 2019 foram confirmadas por consulta seletiva ao Siconfi e permanecem como ausência.

## Próximo gate operacional

O próximo bloco estadual deixa de ser DCA e passa à integração das demais fontes oficiais:

1. RREO;
2. RGF;
3. CAPAG;
4. denominadores complementares;
5. indicadores derivados e legais;
6. tipologias, pares e cartografia estadual;
7. paridade final antes de qualquer promoção do SP645 ao painel público.

