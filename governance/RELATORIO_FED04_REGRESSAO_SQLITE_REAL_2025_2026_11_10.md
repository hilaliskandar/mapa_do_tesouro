# FED04 — Regressão em SQLite reconstruído do acervo canônico de 2025

**Data:** 10/11/2026. **Conclusão:** `qa_pass_disposable_real_2025_source_only`. Não constitui homologação de valores de ITR/Fundeb nem revisão de toda a base histórica.

## Execução autenticada

- [GitHub Actions 42829442185](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42829442185), workflow `FED04 - real source SQLite candidate visibility QA`, **success**.
- [Artefato QA 13770516803](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42829442185/artifacts/13770516803): `QA_FED04_REAL_DB_VISIBILITY.json`; ZIP com digest GitHub `sha256:7d39f2b53210ab380f93e3b17877f68c4a0366f1f54a01a61bff9b7022659664`.
- Head do PR [#232](https://github.com/hilaliskandar/mapa_do_tesouro/pull/232): `0848835da3881e0ad8ddce0494a6a234fb148571`. Checkout do runner: commit de merge provisório `c699195bd8cb3f378384f0067331c4fedfbffe7e`. **Não houve merge em main**.
- [Workflow de QA](https://github.com/hilaliskandar/mapa_do_tesouro/blob/fed04-catalog-safety-20261110/.github/workflows/fed04-real-sqlite-visibility-qa.yml) e [auditoria Python](https://github.com/hilaliskandar/mapa_do_tesouro/blob/fed04-catalog-safety-20261110/pipeline/qa/audit_fed04_real_db_visibility.py) na branch isolada.

## Fonte real e delimitação

O runner leu **somente** o objeto do bucket R2 existente `financas-municipais-sp-canonico`:

`sp_645/site_inputs/FINBRA_SP645_BASE_MULTIFONTES_2025_GATE_C.xlsx`

SHA-256 verificado antes da importação: `ffd626cfde3fa1c79d7a552d5b3a8ad2e3509dce5efcc9c62c39eb76c3796566`.

Em seguida, o workflow reconstruiu o banco **local e descartável** `build/fed04-real-qa/isolated_2025.sqlite` com o mapeamento canônico `data/mappings/base_multifuentes_sp645_2025.yml`, sem acessar qualquer SQLite operacional. A prova cobre a reconstrução real da **fotografia 2025**, não todo o banco histórico estadual 2013–2025.

## Resultados quantitativos do QA

| Controle | Evidência do log |
|---|---|
| Municípios SP | **645** |
| Observações iniciais | **29.670** |
| Variáveis pré-existentes no catálogo SQLite reconstruído | **75** |
| Variáveis FED04 carregadas exclusivamente como metadados | **4** |
| Flags das quatro variáveis FED04 | `publicavel=0`, `ativo=0` |
| Observações sintéticas inseridas apenas na base descartável | **4** |
| Mudança nas observações antigas depois do carregamento | **Nenhuma**, por SHA-256 |
| Mudança nas variáveis antigas | **Nenhuma**, por SHA-256 |
| Mudança na visão pública após carga e quatro valores sintéticos | **Nenhuma**, por SHA-256 |
| Integridade SQLite e chaves estrangeiras | **ok** |
| Escrita em R2 ou publicação de banco | **Não** |

Hashes diretamente do JSON de QA, antes/depois da carga:

- `observacao` original: `25a83917a79e8effe10f48c19d548fe63d085c86fba67c7d9ec28e8c8cf51b92`;
- `v_observacao_publicavel` original e após inserções: `0a610e3775d8804b3edd49f7e7e1ee512abe2a5c1e08a2e52d59cd8859b9e1ea`;
- `variavel` antiga (sem as quatro candidatas): `30dbdfcd980c432f9d20f63ea01b89b227e5db9f4becc174fd889ff5fcbb4c9c`.

A auditagem do SQL registrou todas as quatro variáveis candidatas com `publicavel=0` e `ativo=0`; as quatro inserções de valores numericamente arbitrários foram rotuladas como `FED04_SYNTHETIC_QA_ONLY` e feitas **apenas na base descartável**. O artefato do Actions inclui somente o resumo JSON, **não** o arquivo XLSX de origem, o SQLite nem os valores fiscais municipais.

## Regressão transversal do mesmo head

- [Core CI 42829442056](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42829442056): **196 testes aprovados**.
- [SP 645 Scale Test 42829441928](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42829441928): **success**.
- [Pages Preview 42829441922](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42829441922): **em execução na consulta imediatamente anterior à emissão deste relatório**; consultar estado mais recente antes de promover.
- [Pages Preview anterior 42817420434](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42817420434): **success**, inclusive instalação do Chromium e interações em desktop/mobile após fixar Ubuntu 24.04.

## Decisão e próximas diligências

A proteção de publicação do **carregador de catálogos** foi comprovada sobre dados reais de 2025 e a prova de regressão avançou de fixtures sintéticas para um build representativo. Esse resultado **não autoriza** inferir que as quatro contas DCA têm valores fiscais homologados, aplicáveis a cada ano de 2013–2025.

Manter [PR #232](https://github.com/hilaliskandar/mapa_do_tesouro/pull/232) em rascunho até revisão de cobertura, de seus efeitos sobre catálogos públicos e validação semântica/crosswalk de ITR e Fundeb. Próximo gate técnico independente: compatibilidade com o materializador histórico (não somente XLSX 2025). Próximo gate metodológico: ementário oficial por exercício, natureza de complementação do Fundeb, FPM de 2013–2017 e exceções municipais Rio das Pedras/Sarutaiá. **Nenhuma migração canônica, alteração de série histórica ou deploy de produção foi efetuada.**
