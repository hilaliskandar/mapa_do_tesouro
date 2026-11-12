# INV-RMRP — Staging histórico contextual DCA 2013–2025 + SIAFEM 2020–2026

**Data:** 12/11/2026. **Estado:** aprovado em cópias descartáveis com fonte real R2; **não** é publicação e **não** promove DCA histórica ao catálogo fiscal público.

## Fontes e procedimento

A partir do R2 `financas-municipais-sp-canonico`, foram baixados os dois artefatos oficiais versionados, ambos com SHA-256 validado:

1. `sp_645/site_inputs/FINBRA_SP645_BASE_MULTIFONTES_2025_GATE_C.xlsx`, SHA-256 `ffd626cfde3fa1c79d7a552d5b3a8ad2e3509dce5efcc9c62c39eb76c3796566`: fonte para a reconstrução fiscal canônica de 2025 (645 municípios, 29.670 observações).
2. `sp_645/dca/2013_2025/normalized.csv`, SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`: DCA histórica, 8.385 linhas; 442 linhas referentes aos 34 municípios da RMRP entre 2013 e 2025.

O workflow [**43239171930**](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43239171930) — `INV RMRP - QA DCA historica em SQLite isolado` — encerrou **success**. Etapas:

- Reconstruir SQLite real **somente de 2025** pelo importador e mapeamento oficiais existentes.
- Criar cópia distinta com `import_inv_rmrp_siafem_dev.py`, contendo 752 instrumentos e 889 registros convênio–ano (R$ 305.521.029,20; 1.017 pagamentos contabilizados documentalmente).
- Criar terceira cópia, jamais reutilizando o caminho de origem, pelo novo `pipeline/build/import_inv_rmrp_dca_historica_contexto_dev.py`.
- Acrescentar tabela **`inv_rmrp_dca_contexto_ano`** exclusiva da cópia de QA, com 442 registros município×ano, duas medidas DCA em **centavos inteiros** e estados `OBSERVADO`, `ZERO_EXPLICITO`, `AUSENTE_NAO_ZERO`. Chave primária `codigo_ibge,ano`; FK para município da reconstrução fiscal.
- Aplicar `PRAGMA integrity_check` e `foreign_key_check`; repetir QA de regressão `qa_siafem_rmrp_sqlite_real_2025.py` entre o banco fiscal inicial e a cópia final.

## Evidências de execução

Os logs da execução 43239171930 registraram:

- `QA_PASS_STAGING_HISTORICO_SEPARADO`;
- **442 registros históricos DCA**, 34 municípios e 13 exercícios;
- **2 ausências** de valor de investimentos liquidados e **10 ausências** em transferências de capital DCA, preservadas como `AUSENTE_NAO_ZERO`;
- **889 registros convênio–ano SIAFEM** e R$ 305.521.029,20 (30.552.102.920 centavos) preservados na terceira cópia;
- `qa_pass_real_2025_reconstructed_source_only`, com **29.670 observações fiscais de 2025** inalteradas e visão pública fiscal não modificada;
- nenhuma violação de integridade SQLite/relacionamentos, nenhum lançamento de pagamento individual sintético, nenhuma promoção de obras/projetos.

Workflow versionado em `.github/workflows/inv-rmrp-dca-historica-sqlite-qa.yml`; código do staging em `pipeline/build/import_inv_rmrp_dca_historica_contexto_dev.py`; evidência de relatório QA no artefato do workflow (somente JSON, sem XLSX/CSV privados ou bancos SQLite).

## Significado e restrições

**O resultado comprova coexistência segura da DCA histórica RMRP em tabela contextual e do SIAFEM em tabela de transferências por convênio/ano, em um SQLite descartável que preserva integralmente o conteúdo fiscal de 2025.** A DCA histórica **não** foi materializada como 13 anos de observações do catálogo fiscal público `observacao`; também não foi validada contra eventual implementação do SQLite canônico histórico da plataforma. Essa integração histórica integral permanece um gate próprio.

Não somar transferências de capital DCA, desembolsos estaduais SIAFEM, investimentos municipais liquidados DCA e valores previstos de convênio para construir um suposto investimento total. A correspondência por município e ano demonstra cobertura, não identifica origem, destinação ou obra física; a análise de sobreposição requer documentos individualizados.

Dados de 2026 continuam SIAFEM sem DCA 2026 no snapshot 2013–2025. Ausências históricas não são convertidas em zero.

**Governança:** nenhuma escrita no R2, D1, SQLite produtivo ou página principal; PR #233 em draft, PR #232/FED04 preservada.

## Encaminhamentos

1. Testar integração do acervo DCA 2013–2025 ao **modelo oficial de observações históricas**, somente após análise de crosswalk e fonte por exercício; não confundir staging contextual com catálogo homologado.
2. Ampliar o tratamento de sobreposição de financiamentos estaduais, federais e despesas municipais, exigindo vínculos documentais e política de não dupla contagem.
3. Reavaliar futuramente se a interface experimental de transferências estaduais precisa de consulta contextual paralela DCA, com medidas separadas e legendas inequívocas, sem transformar a matriz em indicador aditivo.
