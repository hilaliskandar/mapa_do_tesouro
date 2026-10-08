# QA — Gate C RREO RCL SP645 — 2025

Run: `37728745160`.

## Resultado

- municípios no universo: 645;
- municípios solicitados: 645;
- requisições concluídas: 645;
- falhas: 0;
- linhas normalizadas: 645;
- RCL observada: 531;
- RCL ausente: 114;
- cobertura observada: 82,33%;
- issues de normalização: 0;
- população RREO observada: 531/645.

Hashes:

- CSV normalizado: `d66d92bd8b75e319d0c6bb432961e791f2c5ad10d25f197b3a10db512ed75ba3`;
- árvore bruta: `4ebb8250a762fc62467dc3119288482f85d8e02b19d3a6aa8139b8dee53868a9`;
- artifact GitHub: `sha256:00d6297440f09e57e61de811410227c48a5d1d98387e5b9d55c3db6fa6fc50d8`.

## Interpretação

A execução estadual foi tecnicamente íntegra. As 114 ausências resultam de payloads sem a linha canônica de RCL no contrato do RREO Anexo 03, período 6. Elas permanecem ausentes e não são convertidas em zero.

A cobertura de 82,33% é cobertura da variável, não cobertura de requisição: a API respondeu às 645 consultas.

## Decisão

RREO 2025 aprovado como snapshot estadual privado, com cobertura variável explicitada.

Antes de qualquer promoção analítica, as 114 ausências devem ser tratadas por fila seletiva de validação/recuperação, sem alterar o valor observado dos 531 municípios.


## Diagnóstico cruzado sem imputação

As 114 ausências do RREO foram comparadas ao snapshot oficial CAPAG, aba `CAPAG Ano Base 2025`.

Resultado:

- 114/114 possuem RCL preenchida no snapshot CAPAG/RGF;
- portanto, as 114 lacunas são específicas do contrato RREO Anexo 03 na consulta executada;
- não representam ausência geral de RCL do município.

Essa comparação é apenas diagnóstica. O valor da outra fonte não é usado para preencher `rreo_rcl_total_12m`, porque RREO e RGF/CAPAG permanecem objetos de fonte distintos.
