# INV-RMRP — Quinta prévia estadual SIAFEM com série anual exata

**Data:** 12/11/2026. **Ambiente:** PR nº 233 isolada; não publicado na produção.

## Entregas executadas

A validação real da integração SIAFEM em SQLite reconstruído foi aprovada no workflow [43234916467](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43234916467), com 29.670 observações fiscais originais preservadas e 752 instrumentos / 889 convênios-ano em staging. Detalhes no relatório `RELATORIO_INV_RMRP_SQLITE_REAL_2025_QA_2026_11_12.md`.

Foi criada a quinta interface experimental:
**https://pr-233.finbra-tic-tim-referencia.pages.dev/siafem-investimentos-rmrp-preview.html**

Implementação:
- `app/static/siafem-investimentos-rmrp-preview.html` com filtros por sub-região da RMRP, município IBGE, ano e número de convênio, totais de valor liberado/estornado com centavos, pagamentos e convênios.
- `app/static/data/api/v3/investimentos/rmrp/siafem-sp-investimentos-anual-preview.json`: 34 municípios, 238 linhas município-ano, 889 linhas convênio-ano, 752 convênios distintos, 1.017 pagamentos contabilizados e **R$ 305.521.029,20** em valores liberados/estornados por exercício de 2020 a 12/11/2026. Sem CNPJ na interface da prévia, sem vínculos especulativos com obras.
- `deployment/materialize_investimentos_preview.py` e `deployment/qa_investimentos_preview.py` atualizados para exigir o status `preview_transferencias_estaduais_em_revisao_nao_execucao_municipal`, conferir códigos municipais, números e somas, e impedir promoção silenciosa a despesa executada.

## QA e implantação efetivamente confirmados

No [GitHub Actions **43235935045**](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43235935045), job `build-deploy-qa` concluído com **success**:

- Build do candidato a partir do snapshot público existente — aprovado.
- Materialização do overlay RMRP apenas na PR nº 233 — aprovada.
- QA local `qa_investimentos_preview.py` — aprovado.
- Deploy isolado Cloudflare Pages no alias `pr-233` — aprovado.
- QA remoto de Pages e da quinta prévia RMRP — aprovado.

**Falha independente:** o job `rmj-browser-qa` do mesmo workflow terminou com `failure` no passo `Install Chromium for QA`. Não houve execução da interação de browser da RMJ nessa rodada. Como o workflow é a soma dos jobs, seu status geral segue `failure`, embora o job de implantação e QA da prévia RMRP tenha passado. Essa falha deve ser tratada em atividade de infraestrutura distinta, não atribuída à qualidade dos dados SIAFEM.

## Segurança metodológica

A prévia mostra **transferências estaduais a prefeituras classificadas como investimento no SIAFEM**, inclusive estornos com sinal, com atualização declarada da fonte até 12/11/2026. Não exibe gastos efetivamente executados pelos municípios, fase física de obra ou financiamento federal; tampouco soma transferências a despesas municipais. O **valor previsto de contrato** não é uma medida repetida por ano. Um convênio plurianual aparece com seu valor de liberação correspondente a cada ano.

O código de visualização não modifica nenhuma base; o snapshot JSON é derivado das tabelas de governança exatas e testadas no GitHub. A produção continua intocada.

## Próximos gates

1. Testar a mesma extensão sobre materialização fiscal histórica 2013–2025, quando localizada/reproduzida em cópia de QA, além da reconstrução já homologada de 2025.
2. Verificar a qualidade do navegador RMJ e resolver a instalação Chromium sem mascarar testes.
3. Relacionar transferências estaduais aos objetos e locais de investimento apenas quando existirem chaves/documentos oficiais; a sede municipal beneficiária não identifica o local físico da obra.
4. Revisar experiência visual, paginação e performance da quinta prévia antes de aprovação de publicação, mantendo PR #233 draft e proteção contra dupla contagem.
