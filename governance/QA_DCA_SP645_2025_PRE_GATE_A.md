# QA preliminar — DCA SP 645 — 2025

Data da análise: 2026-10-07.

## Escopo

Este registro documenta a execução estadual anterior ao Gate A formal:

- workflow: `Run SP 645 DCA 2025`;
- run ID: `37684287610`;
- resultado: `success`;
- municípios: 645;
- anexos: I-C, I-D e I-E;
- respostas brutas: 1.935;
- falhas: 0;
- linhas normalizadas: 645;
- variáveis normalizadas: 26;
- issues de normalização: 0;
- SHA-256 do CSV normalizado: `619367dd8b2c5b3db6f7a6c902b41e2f2685616cf8560e2e852e7583f386eec7`;
- SHA-256 da árvore bruta: `0968069763f557afef9fe33bd9b141ea99c3e3c792faff856ab2627fa181375f`.

Este documento é preliminar porque o workflow canônico `SICONFI SP 645 Full DCA Gate A` ainda estava em execução quando a análise foi registrada.

## Cobertura por variável

| Variável | Observado | Ausente | Cobertura |
|---|---:|---:|---:|
| dca_receita_corrente_bruta | 644 | 1 | 99,84% |
| dca_receita_tributaria_bruta | 644 | 1 | 99,84% |
| dca_iptu_principal | 643 | 2 | 99,69% |
| dca_itbi_principal | 641 | 4 | 99,38% |
| dca_iss_principal | 643 | 2 | 99,69% |
| dca_fpm_cota_mensal | 643 | 2 | 99,69% |
| dca_icms_cota_parte | 644 | 1 | 99,84% |
| dca_ipva_cota_parte | 643 | 2 | 99,69% |
| dca_operacoes_credito | 152 | 493 | 23,57% |
| dca_alienacao_bens | 269 | 376 | 41,71% |
| dca_transferencias_capital | 622 | 23 | 96,43% |
| dca_despesa_total_liquidada | 644 | 1 | 99,84% |
| dca_despesa_corrente_liquidada | 644 | 1 | 99,84% |
| dca_pessoal_encargos_liquidada | 644 | 1 | 99,84% |
| dca_juros_encargos_liquidada | 309 | 336 | 47,91% |
| dca_investimentos_liquidada | 644 | 1 | 99,84% |
| dca_inversoes_financeiras_liquidada | 54 | 591 | 8,37% |
| dca_amortizacao_divida_liquidada | 553 | 92 | 85,74% |
| dca_func_saude_liquidada | 644 | 1 | 99,84% |
| dca_func_educacao_liquidada | 644 | 1 | 99,84% |
| dca_func_urbanismo_liquidada | 639 | 6 | 99,07% |
| dca_func_habitacao_liquidada | 146 | 499 | 22,64% |
| dca_func_saneamento_liquidada | 330 | 315 | 51,16% |
| dca_func_gestao_ambiental_liquidada | 527 | 118 | 81,71% |
| dca_func_transporte_liquidada | 458 | 187 | 71,01% |
| populacao_dca | 644 | 1 | 99,84% |

## Ausências centrais

O código IBGE `3551207` concentra a única ausência simultânea em receita corrente, receita tributária, despesa total, despesa corrente, pessoal, investimentos, Saúde, Educação, ICMS e população.

Nos três artefatos brutos desse município em 2025, os arquivos existem e a aquisição foi concluída sem erro, mas o Siconfi retornou `items=[]` em I-C, I-D e I-E. Portanto, a ausência é da resposta da fonte naquele recorte e não decorre de falha do normalizador.

Outras ausências tributárias são pontuais:

- `3544004`: ausência em IPTU, ITBI, ISS, FPM e IPVA;
- `3512605`: ausência em ITBI;
- `3543501`: ausência em ITBI.

Nesses casos, os anexos brutos contêm registros; o que não aparece é a conta exata definida pelo mapping canônico para a variável correspondente. A regra permanece: não substituir automaticamente por outra rubrica e não promover ausência a zero.

## Interpretação

A cobertura é praticamente completa para as variáveis estruturais centrais. Coberturas baixas em operações de crédito, alienação de bens, inversões financeiras, Habitação, juros e outras rubricas esparsas não devem ser interpretadas automaticamente como problema de coleta. Para cada variável, a distinção entre inexistência de movimento, omissão declaratória e ausência de rubrica exige análise da fonte.

## Relação com o Gate A

O Gate A formal deve confirmar ou refutar:

1. 645 municípios solicitados;
2. 1.935 respostas brutas;
3. nenhuma falha não resolvida;
4. 645 linhas normalizadas;
5. hashes registrados;
6. cobertura variável a variável;
7. preservação das ausências descritas acima.

Se os resultados coincidirem, este documento pode ser promovido de QA preliminar para registro definitivo de 2025.
