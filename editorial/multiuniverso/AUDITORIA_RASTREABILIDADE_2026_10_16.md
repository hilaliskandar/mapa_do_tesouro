# Auditoria de proveniência por dependências — 16/10/2026

O catálogo editorial contém 50 variáveis por universo. Dessas, 15 não possuem `fonte_preferencial_id`, por serem indicadores derivados ou agregados analíticos, mas têm fórmulas explícitas.

A conferência das expressões calculou 10 indicadores cujas dependências imediatas estão integralmente no recorte de 50 variáveis e 5 cujas fórmulas referenciam variáveis ausentes do recorte. Casos: `despesa_territorial_pc` e `investimento_pc` usam `populacao_dca`; `despesas_capital_selecionadas` usa `dca_inversoes_financeiras_liquidada` e `dca_amortizacao_divida_liquidada`; `servico_divida_liquidado` usa `dca_juros_encargos_liquidada` e `dca_amortizacao_divida_liquidada`; `tributos_imobiliarios_pct_receita_tributaria` usa `tributos_imobiliarios`.

O gerador não atribui nova fonte oficial aos indicadores derivados: o arquivo `rastreabilidade.json` registra dependências, origens diretas explicitamente documentadas e referências não resolvidas. `qa_rastreabilidade.json` agrega os dez universos. Revisão de proveniência recursiva das variáveis fora do recorte é uma dependência pendente antes da conclusão metodológica.

Execução https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38890730435 aprovada no commit `50bfedc980f1d2f240b3d40d23ce16f620e2e973`, artefato `12041771580`, SHA-256 `e52795c9d4197a2e1b1a9fc79589b272f9bcdf9410fd7c289229fb371d154123`.

Não foram promovidas mudanças para produção; PR #198 permanece isolado.

## Ampliação ao catálogo central — 16/10/2026

As cinco dependências antes externas ao recorte de 50 variáveis receberam identificação documental em `editorial/multiuniverso/fontes_dependencias_externas.json`:
- `populacao_dca`: definida em `data/catalogs/variables_core.yml`, fonte SICONFI_DCA; é população informada na DCA, não a variável do IBGE.
- `tributos_imobiliarios`: agregado do mesmo catálogo, fórmula IPTU + ITBI; não tem fonte oficial única própria, mas parcelas SICONFI_DCA.
- `dca_juros_encargos_liquidada`: DCA Anexo I-D, Despesas Liquidadas, código DO3.2.00.00.00.00.
- `dca_inversoes_financeiras_liquidada`: DCA Anexo I-D, Despesas Liquidadas, código DO4.5.00.00.00.00.
- `dca_amortizacao_divida_liquidada`: DCA Anexo I-D, Despesas Liquidadas, código DO4.6.00.00.00.00.

As contas DCA também constam de `data/mappings/base_multifuentes_v0_4.yml` com `source_id=SICONFI_DCA`. A vinculação foi incorporada aos arquivos `rastreabilidade.json`, sem confundir fonte dos componentes com fonte preferencial própria do indicador derivado. Não foram acrescentados valores ou inventadas séries.

Geração e testes passaram no workflow https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38892646130, commit `8809775b2f6208b8b74678495bf7573bbe5de061`; artefato `12042073535`, SHA-256 `71a8115d1573928248b91f57fd782b4082f16c362a33ba5410c244ed197067ac`. Permanece necessário confrontar a origem das observações com os arquivos oficiais por exercício antes da homologação fiscal completa. Nenhum deploy de produção foi realizado.
