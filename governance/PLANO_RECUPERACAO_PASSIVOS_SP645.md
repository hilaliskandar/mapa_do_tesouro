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
