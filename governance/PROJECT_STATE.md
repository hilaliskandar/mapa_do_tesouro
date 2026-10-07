# Estado do projeto

Data de referência: 2026-10-07.

## Estado operacional

A `main` é a fonte de verdade.

O baseline público TIC-TIM 30 permanece publicado e protegido por CI, QA de paridade e contratos metodológicos.

A expansão estadual está no estado `gate_b_history_characterized`.

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
- 2022: 644;
- 2023: 645;
- 2024: 630;
- 2025 local: 632;
- 2025 Gate A: 645.

O normalizador aceita CSV e XLSX locais, registra hashes, cobertura e códigos faltantes.

### Crosswalk temporal concluído para receitas centrais

Foram comprovados diretamente nos arquivos locais quatro regimes:

- 2013: códigos antigos + `Receitas Realizadas`;
- 2014–2017: códigos antigos + `Receitas Brutas Realizadas`;
- 2018–2021: códigos intermediários + `Receitas Brutas Realizadas`;
- 2022+: códigos atuais + `Receitas Brutas Realizadas`.

As variantes estão explicitadas no mapping canônico. As despesas centrais permanecem no mesmo contrato observado.

## Próximo gate operacional

O próximo trabalho é completar a série com **delta incremental**, não repetir aquisições estaduais integrais:

1. priorizar exercícios com poucas lacunas: 2022, 2018, 2019, 2015, 2016 e 2013;
2. tratar 2024 e o snapshot local de 2025 com deltas maiores;
3. avaliar 2014 separadamente por ser o snapshot local mais incompleto;
4. preservar snapshot original e delta como artefatos distintos;
5. promover anos aprovados ao R2 privado;
6. consolidar snapshot multianual estadual;
7. somente então iniciar integração estadual de RREO, RGF e CAPAG.

## Regras para retomada

1. ler este arquivo;
2. verificar `main`, PRs e CI;
3. consultar o Drive antes de qualquer coleta externa;
4. consultar apenas os códigos/anexos faltantes quando houver snapshot local;
5. preservar ausência como ausência;
6. respeitar o crosswalk por exercício;
7. manter TIC-TIM 30 como baseline de regressão até promoção formal do baseline estadual.
