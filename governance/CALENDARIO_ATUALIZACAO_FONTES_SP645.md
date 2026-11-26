# Calendário permanente de atualização — Mapa do Tesouro

Data: 26/11/2026. Estado: proposta registrada, agendamentos ainda não habilitados. Escopo SP645 com prioridade RMRP e capital em fonte TCM-SP separada. Catálogo legível por máquina: `data/catalogs/source_refresh_calendar.json`.

## Operação

- Seg: DCA, RREO, RGF e extrato de entregas. Ter: TCESP. Qua: Transferegov. Qui: ObrasGov e SIAFEM. Sex: MSC e recuperação de lacunas. Sáb: QA e reconciliação. Dom: build candidato e promoção somente após autorização. Sondagens leves diárias onde indicado.
- DCA: semanal fevereiro–julho, mensal agosto–janeiro, retificações históricas trimestrais. Prazo ordinário municipal 30/04 do ano seguinte (LRF art. 51).
- RREO: referência bimestral; RGF: quadrimestral ou semestral conforme ente e demonstrativo; monitorar calendário oficial e retificações, consultas seletivas em D+2/7/14/30 após prazo. MSC: semanal, janela de três meses e encerramento separado.
- TCESP: sondagem semanal, atualização mensal no primeiro dia de terça-feira após dia 20; ano anterior trimestral. RCL e cadastros PPA mensais. Nunca presumir disponibilidade mensal uniforme.
- Transferegov: sondagem diária leve e ingestão semanal; ObrasGov e SIAFEM semanal; reconciliação periódica. Validar migração de APIs antes de habilitar. Comunicado 23/2026 e página de APIs revisada em 19/11/2026 indicam novos ambientes e cronograma de implantação de módulos até outubro de 2027.
- Estatísticas auxiliares e dimensões territoriais: conforme catálogo; datas exatas de divulgação dependem da fonte.
- Estados: due, probing, unchanged, collecting, validated, quarantined, failed, persisted, published; ausência não equivale a zero. Preservar última versão válida e registrar idade da referência e da coleta separadamente.
- Chave idempotente: fonte, município, exercício, período, produto, versão de origem; hashes, manifests, checkpoints por lote, backoff e exclusão mútua por fonte. Quando metadados não confiáveis, sondagem não prova ausência de atualização; baixar na janela de refresh.
- Agendador: GitHub Actions em branch padrão, catálogo em versão aprovada; runner e credenciais já existentes; não agendar coletores hardcoded para 2026 sem generalização e testes. Não publicar automaticamente sem gate QA e política de autorização.
- Indicadores públicos: referência disponível, última consulta bem-sucedida, cobertura, fonte, lacunas e próxima janela; internamente registrar erro, retries e versão.

## Evidência empírica

Siconfi 2026: 539 municípios, 3220 demonstrativos observados, 106 sem dados; run 45804816212 e piloto RMRP. Prazo oficial 5º RREO e MSC outubro: 30/11/2026, não inferir atraso antes do prazo.

TCESP refresh RMRP run 45858905499, artifact 15136808553: 68/68 atualizados e com avanço temporal, nenhuma quarentena. Despesas: 23 outubro, 11 setembro; receitas: 22 outubro, 11 setembro, 1 agosto. Cobertura R2 `tcesp/rmrp/2026/refresh/run_45858905499/coverage_b7e61233879fdaab9cd04a6c8655400f23b2b1c212b3a356837614029a92e90e.json`. Snapshots anteriores preservados.

Fontes oficiais: https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp101.htm ; https://siconfi.tesouro.gov.br/ ; https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br ; https://www.gov.br/transferegov/pt-br/comunicados/comunicados-gerais/2026/comunicado-no-23-2026-do-portal-do-transferegov.br .

Próximo: implementar orquestrador com dry-run, controle de execução persistente e adaptação dos coletores para múltiplos exercícios. Não há cron recorrente habilitado nesta alteração.
