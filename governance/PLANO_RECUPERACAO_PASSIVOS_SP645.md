# Recuperação permanente de passivos SP645

26/11/2026. Determinação: completar coletas ainda não realizadas ou incompletas para todos os 645 municípios, em paralelo às atualizações periódicas. Não substituir ausência por zero nem considerar consulta vazia como comprovação de inexistência.

Fila independente de manutenção: chave fonte/IBGE/exercício/período/produto; estados não inventariado, não consultado, parcial, vazio inconclusivo, falha transitória, indisponível comprovado, não aplicável, validado, persistido, integrado. Reutilizar R2 e manifestos; não duplicar dados observados. Reconsultar conforme mudança de fonte, prazo oficial, retificação ou estratégia alternativa. Prioridade RMRP e depois SP645; preservar dimensão territorial oficial.

| Frente | Passivo inicial | Próximo gate |
|---|---|---|
| DCA | 40789 células ausentes em 218010; ausência não equivale a entrega ausente | Classificar por exercício/variável e extrato de entregas; recuperar somente faltantes efetivos |
| RREO/RGF 2026 | 106 cidades sem observações, 5 anexos vazios | Workflow sp645-siconfi-state-recovery-2026.yml: 98 cidades externas e 5 anexos; 8 RMRP já testadas com 192 vazios; verificar tipos simplificados separadamente |
| MSC | Sem coleta consolidada | Validar contrato API e piloto, depois priorizar 106 e expandir SP645 |
| TCESP 2026 | 609 municípios externos aos 35 com acervo | Mapear slugs oficiais; validar identidade e coletar pares receitas/despesas, preservar bruto e meses |
| TCM-SP | Capital fora do universo TCESP | Inventariar fontes e equivalências sem imputar |
| SIAFEM 2025 | 91 inconclusivos externos RMRP | Congelar fila e diagnosticar filtros/totalizadores; não interpretar vazio como zero |
| Transferegov | Cobertura e execução financeira não fechadas | Reutilizar snapshots, validar layouts novos e cobertura por município e modalidade |
| ObrasGov | Cobertura cadastral e financeira não fechada | Reutilizar IDs, territorializar, completar detalhamento e validar cardinalidade |
| Auxiliares | Cobertura a inventariar | Classificar fontes por aplicabilidade e período |

A fila de passivos deverá integrar o orquestrador sem usar o ledger simulado QA como produção. Regras de execução: checkpoints por lote, exclusão por fonte, limites API, prioridade a lacunas efetivas, evidência de consulta, reprogramação controlada e publicação somente após QA. Agendamento recorrente ainda não habilitado. Produção v0.6.0 preservada.

## Atualização de 27/11/2026

- TCE-SP 2026: 644 municípios jurisdicionados com ambos os domínios recuperados; piloto 10, expansão 200 e final 399, além dos 35 anteriores. Runs 45922343693, 45924519271, 45925931531; 798/798 extratos na expansão final, 20 lotes com readback R2. Ainda não integrados à plataforma; capital TCM-SP separada.
- Siconfi 2026: run 45925913226, 3.220 demonstrativos e 836.951 linhas normalizadas, cinco respostas vazias, 539 municípios, hash staging bd58cc084ea10d21203d3a0f2f02e39a233926844d41a06f79e313189b1eae0b. Recuperação convencional adicional 2.549 consultas vazias; mudar estratégia para simplificados e MSC.
- ObrasGov: inventário 4.224 projetos por proponente, 625 municípios; 218 anteriores + 100 piloto + 1.000 + 2.906 fichas previstas recuperadas, runs 45927622363, 45928187001, 45928847777; 30 lotes finais readback R2. Não equivale à execução financeira nem localização física.
- Transferegov: novo workflow sp645-transferegov-financial.yml para eventos-pai de desembolsos e pagamentos por proponente, com centavos, data, identificador e proveniência; sem dados pessoais de favorecidos. Nova leitura oficial necessária porque não está comprovada autorização do runner para ZIPs privados Drive. Preservar snapshots anteriores e não confundir estágios.
- Agendamento permanente e integração pública continuam pendentes; v0.6.0 preservada.
