# FED04 — QA de publicação e carregamento de novas variáveis fiscais

**Data:** 10/11/2026. **Situação:** regressão local aprovada; integração e homologação pendentes. **Sem alteração de produção.**

## Problema identificado

O arquivo da branch principal `pipeline/build/load_catalog.py` não inclui os campos `publicavel` e `ativo` ao inserir/atualizar variáveis, embora ambos existam em `data/schema/001_initial.sql` com valor padrão 1. O simples carregamento de um novo catálogo com `publicavel: 0` e `ativo: 0` poderia criar variáveis publicáveis; isso impede carregar as quatro candidatas FED04 sem correção.

## Alteração isolada e revisão

- Branch: [`fed04-catalog-safety-20261110`](https://github.com/hilaliskandar/mapa_do_tesouro/tree/fed04-catalog-safety-20261110).
- [PR #232, **rascunho**](https://github.com/hilaliskandar/mapa_do_tesouro/pull/232), **não integrado**.
- Carregador proposto: se `publicavel` ou `ativo` constar explicitamente no YAML, aplicar flags 0/1; se forem omitidas, preservar estado anterior no `ON CONFLICT`, e usar os defaults históricos na primeira inserção; rejeitar valores inválidos (incluindo string `"false"`).
- Testes [`tests/test_fed04_catalog_flags.py`](https://github.com/hilaliskandar/mapa_do_tesouro/blob/fed04-catalog-safety-20261110/tests/test_fed04_catalog_flags.py). Workflow [`fed04-catalog-safety-qa.yml`](https://github.com/hilaliskandar/mapa_do_tesouro/blob/fed04-catalog-safety-20261110/.github/workflows/fed04-catalog-safety-qa.yml), que deverá executar esses testes e `tests/test_schema.py`.

## Teste local executado

Em um ambiente Python 3 com `pytest` e `PyYAML`, foram reproduzidas a lógica Python e as definições relevantes do esquema SQL inicial da branch. A execução não usou banco do usuário, segredos, API externa ou produção. Comando de verificação:

```bash
python -m pytest -q tests/test_fed04_catalog_flags.py
```

**Resultado:** `7 passed`. Os testes cobrem:
1. Inserção com `publicavel=0` e `ativo=0`, além de não exibição de uma observação existente em `v_observacao_publicavel`;
2. Defaults 1/1 retrocompatíveis quando opções são omitidas em inserção nova;
3. Preservação de flags privadas após atualização apenas documental;
4. Mudança explícita de um campo sem modificar o outro;
5. Rejeição de flag em formato string;
6. Idempotência de duas cargas idênticas;
7. Carga das **quatro variáveis do arquivo real de propostas** com `publicavel=0` e `ativo=0`.

**Limitação essencial:** os testes locais operaram sobre cópia de código e DDL relevante, não sobre clone conectado do repositório nem sobre SQLite canônico materializado. O teste do sétimo cenário usou arquivo local com os quatro IDs e estados da proposta; a execução diretamente no runner GitHub continua necessária. **O status combinado do commit `f919b3c09cad53de1584c96025087261020b5837` retornou lista vazia de `statuses`; isso não comprova teste CI aprovado ou reprovado.**

## Gate de publicação

O carregador existente em `main` **não foi alterado** e o PR foi deixado como rascunho. Verificar no GitHub Actions a execução do workflow e sua compatibilidade com as demais rotinas; executar teste em SQLite de build isolado a partir da base canônica e comparar a visibilidade das variáveis antes/depois. Só depois decidir sobre merge. As quatro variáveis FED04 continuam em `governance/proposals`, excluídas da carga automática.

**Observação de esquema:** a visão `v_observacao_publicavel` seleciona por `publicavel=1`; o campo `ativo` não é filtro de proteção nessa visão. Portanto a garantia de não publicação exige `publicavel=0` — `ativo=0` isoladamente **não basta**. A decisão de alterar a semântica da visão deve ser tratada separadamente e submetida a regressão específica.

**Próximos passos:** validar CI do PR #232; conferir `tests/test_schema.py`; QA isolado sobre build representativo; revisão contábil do crosswalk FED04; promoção somente conforme gates de homologação. Nenhuma migração nem deploy ocorreu.
