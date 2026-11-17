# INV-RMRP — Importação SIAFEM/SP em cópia SQLite e QA offline

**Data:** 12/11/2026. **Branch:** investimentos-territoriais-sp645-20261111. **PR:** #233 (draft).

## Resultado implementado

- Importador de desenvolvimento: `pipeline/build/import_inv_rmrp_siafem_dev.py`.
- Teste offline com banco **sintético**: `pipeline/build/test_inv_rmrp_siafem_dev.py`.
- Workflow: `.github/workflows/inv-rmrp-siafem-staging-qa.yml`.
- **GitHub Actions:** [execução 43219431660](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43219431660), conclusão **success**. QA dos dados anuais exatos [43219431478](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43219431478), também **success**.

## Contrato de ingestão em cópia

A fonte SQLite precisa existir, e o destino precisa ser um caminho **novo e diferente**. O importador abre a origem em `mode=ro`, utiliza `sqlite3.backup` e somente modifica a cópia. Em falha, faz rollback e descarta a cópia de saída. Protege contra sobrescrever arquivos existentes.

A extensão SQL existente `governance/proposals/INV_RMRP_SCHEMA_EXTENSAO_SQLITE_2026_11_11.sql` continua sendo aplicada apenas à cópia de desenvolvimento, mantendo as tabelas históricas fiscais intocadas.

- `inv_ator`: 34 prefeituras identificadas por IBGE7 e CNPJ oficial do SIAFEM.
- `inv_instrumento`: 752 instrumentos com chaves `siafem_sp:IBGE:NUMERO`, valor de convênio separado da execução anual e `qa_status=em_revisao`.
- `inv_siafem_convenio_ano` (nova tabela específica de staging): 889 linhas com `instrumento_id`, município, ano, quantidade de pagamentos, valor exato de liberação/estorno em centavos, origem auditável, `qa_status=em_revisao`. Não repete o valor total do convênio em cada ano.
- `inv_evento_financeiro`: **zero linhas novas** para SIAFEM; os registros anuais **não** equivalem a pagamentos bancários individualizados. Não foram criados projetos/obras homologados nem links entre SIAFEM e Obrasgov baseados em coincidências.
- `fonte` e `artefato_fonte`: metadados de fonte, URL, versionamento, SHA256 do arquivo e advertência de unidade analítica.

## QA sintético reproduzido

O teste constrói origem SQLite mínima com 34 municípios, tabela `fonte` e `artefato_fonte`; importa os dados reais extraídos do SIAFEM na **cópia sintética**; depois confere:

1. Origem permanece sem tabelas da extensão.
2. Destino tem 752 instrumentos e 889 registros convênio-ano.
3. Soma financeira = **30.552.102.920 centavos** (R$ 305.521.029,20).
4. Soma de quantidades = **1.017 pagamentos informados pela fonte**.
5. `PRAGMA integrity_check=ok`, `foreign_key_check` vazio.
6. Nenhum lançamento financeiro individual ou projeto homologado criado indevidamente.
7. Nova importação no mesmo arquivo de saída é rejeitada.

**Limite fundamental:** a aprovação do teste sintético não prova compatibilidade com o arquivo SQLite canônico armazenado no R2. A importação na cópia **real** permanece pendente e exigirá acesso ao snapshot efetivo, hash, segurança de leitura e QA de regressão. Não houve escrita na produção.

## Uso futuro

Com uma cópia real do SQLite canônico disponível, a execução prevista é:

```bash
python pipeline/build/import_inv_rmrp_siafem_dev.py \
  --source-db /caminho/copia_canonica_origem.sqlite \
  --output-db /caminho/inv_rmrp_siafem_qa_novo.sqlite \
  --repo-root .
```

Não executar contra arquivo produtivo como destino e não apontar para uma saída existente.

**Gates:** validar a cópia real, cruzar com a despesa municipal sem somar transferência e execução, depois criar consultas somente sobre staging. A PR #233 permanece isolada, e a PR #232/FED04, preservada.
