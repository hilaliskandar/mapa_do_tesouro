# Baseline de migração — Base multifuentes v0.4

## Artefato de origem

- arquivo: `FINBRA_TIC_TIM_30M_BASE_MULTIFONTES_2013_2025_v0_4.xlsx`
- SHA-256 observado em 2026-10-06: `f51d8615f3742b1d414f1edff67805cac1a10cbc18764b454aab518de9c9e3f1`
- aba de primeira ingestão: `Base multifuentes`
- registros município-ano: **390**
- municípios: **30**
- exercícios: **2013–2025**
- pares município-ano distintos: **390**

## Coberturas sentinela

Estas contagens descrevem variáveis específicas e não devem ser generalizadas para toda a camada-fonte.

| Variável | Observado | Ausente | Não aplicável |
|---|---:|---:|---:|
| Receita corrente bruta | 389 | 1 | 0 |
| IPTU | 388 | 2 | 0 |
| ITBI | 387 | 3 | 0 |
| ISS | 387 | 3 | 0 |
| RCL oficial | 328 | 2 | 60 |
| DTP | 315 | 15 | 60 |
| DTP/RCL | 315 | 15 | 60 |
| DC | 320 | 10 | 60 |
| DCL | 320 | 10 | 60 |
| DC/RCL | 319 | 11 | 60 |
| DCL/RCL | 320 | 10 | 60 |
| CAPAG nota | 30 | 0 | 360 |

## Regra de aceite da primeira ingestão

A primeira carga SQLite somente poderá ser promovida quando:

1. houver exatamente 30 municípios, 13 exercícios e 390 pares município-ano;
2. todas as observações mapeadas forem comparadas célula a célula com a aba de origem;
3. o validador de paridade retornar zero divergências;
4. as contagens de cobertura sentinela coincidirem com este baseline;
5. o hash do arquivo-fonte estiver registrado no manifesto do build.

## Observação metodológica

Cobertura é propriedade da variável, não apenas da planilha ou demonstrativo. A existência de um RGF/RREO para determinado município-ano não garante que todos os campos necessários estejam observados.
