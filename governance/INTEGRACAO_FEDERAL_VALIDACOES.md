# Diário de validação — Integração federal e Novo PAC

Documento incremental complementar ao [plano](INTEGRACAO_FEDERAL_PAC_PLANO.md) e ao [README principal](../README.md).

## Registro 2026-11-03 — Abertura de projeto

**Escopo realizado**
- Repositório `hilaliskandar/mapa_do_tesouro` e branch-base `main` identificados via GitHub.
- README canônico, `governance/PROJECT_STATE.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`, `PENDING_TASKS.md` e `QA_CHECKLIST.md` examinados.
- Arquitetura compatível com extensão: ingestão → normalização → SQLite → JSON static-first → Pages, snapshots privados R2, hashes, proveniência, QA e baseline `TIC_TIM_30`.
- Código de adaptadores, integração com D1/SQLite, pipelines e frontend **não foram modificados**.
- Dados das APIs públicas foram **testados em investigação anterior de outro projeto**, não homologados neste repositório. Leituras reais anteriores: Obrasgov (`/projeto-investimento`, `/empenho`, `/execucao-fisica`), Transferegov parcerias (`/programa`, `/proposta`, `/parceria`, `/empenho-parceria`) e transferências especiais (`/data-atualizacao`).
- Fontes Nova PAC/MCMV com recursos XLSX/ZIP/CSV localizadas previamente, mas arquivos binários **não inspecionados**.

**Gate G0:** documentação criada; revisão por PR ainda não realizada. **G1:** inspeção inicial, sem inventário completo de schema/código. **G2–G7:** não executados.

**Verificações e ressalvas**
- Sem teste local de código, pois o PR inicial contém exclusivamente documentação.
- Não se confirmou ainda nenhuma equivalência financeira entre empenho federal e receita municipal, nem cobertura Novo PAC por identificador.
- Não inferir implantação ou execução de automações pela abertura do PR.

**Próximo incremento:** inspecionar `pipeline/acquire/`, `data/schema/`, `pipeline/build/` e testes; desenhar adaptadores públicos com fixtures e confirmar em execução isolada. Documentar resultados aqui e no README em cada novo commit.

## Template obrigatório para novas rodadas

```text
Data/hora:
Gate:
Branch/commit:
Fonte / endpoint / versão OpenAPI:
Parâmetros e universo:
Artefatos (nome, SHA-256, MIME, data-base):
Cobertura, nulos e cardinalidade:
Testes e evidências (run/URL/log):
Diferenças contábeis e relações reprovadas:
Resultado: APROVADO | REPROVADO | PENDENTE | BLOQUEADO
Decisão, responsável e próximo passo:
Atualização realizada no README: SIM/NÃO
```
