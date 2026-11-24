# INV-RMRP — QA SIAFEM no SQLite real 2025 reconstruído a partir do R2

**Data:** 12/11/2026. **Branch:** `investimentos-territoriais-sp645-20261111`, PR #233 (draft).

## 1. Localização correta da fonte canônica

Foi verificada a existência do bucket privado `financas-municipais-sp-canonico` via API Cloudflare. O inventário de objetos (119 itens na listagem sem prefixo) **não identificou objeto SQLite** com extensão `.db`, `.sqlite` ou `.sqlite3`. O bucket `finbra-publicacao` também não apresentou SQLite identificável (205 objetos). Portanto, não se deve descrever esse teste como download de SQLite previamente armazenado no R2.

A origem efetivamente usada pela arquitetura do projeto está em:
- Objeto R2 `sp_645/site_inputs/FINBRA_SP645_BASE_MULTIFONTES_2025_GATE_C.xlsx`.
- Metadata R2: **335.517 bytes**, `last_modified=2026-10-09T00:26:22.089Z`.
- Hash esperado SHA-256 **`ffd626cfde3fa1c79d7a552d5b3a8ad2e3509dce5efcc9c62c39eb76c3796566`**, verificado pelo utilitário existente `deployment/download_r2_source.py`.
- Materializador oficial `pipeline.ingest.import_multifuentes`, mapeamento `data/mappings/base_multifuentes_sp645_2025.yml` e migrações versionadas.

Esse método reproduz o processo já empregado na regressão FED04 de 10/11/2026. Trata-se de reconstrução do SQLite a partir de **dados reais do exercício de 2025**, não de validação da base histórica 2013–2025 no mesmo arquivo.

## 2. Implementação e execução

Artefatos adicionados:
- `pipeline/qa/qa_siafem_rmrp_sqlite_real_2025.py` — confronta bancos SQLite origem e staging, com hashes de conteúdo fiscal e visão pública.
- `.github/workflows/inv-rmrp-siafem-real-2025-qa.yml` — consulta somente leitura do R2, reconstrução local, importação em cópia descartável e auditoria.

Execução [GitHub Actions **43234916467**](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43234916467) em 12/11/2026: **concluída com `success`**. O job `qa-real`, ID `131239588279`, confirmou sucesso em todas as etapas relevantes: leitura R2 e SHA-256; reconstrução SQLite; importação SIAFEM em cópia; auditoria de regressão fiscal; arquivamento somente do QA.

Artefato temporário: [`inv-rmrp-siafem-real2025-qa-43234916467`](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43234916467/artifacts/13950404743), ID `13950404743`; digest ZIP `sha256:486c28b5094894f0bf988a1709b20a2f52a830edb18933dd220992a27f7be6bd`. O ZIP contém apenas o relatório de QA, **não** a planilha de origem nem o banco SQLite.

## 3. Resultados dos testes

Os logs registraram estado de sucesso `qa_pass_real_2025_reconstructed_source_only`.

- **29.670 observações fiscais** existentes na reconstrução de 2025 mantidas sem alteração de conteúdo.
- `municipio`, `universo`, `universo_municipio`, `variavel`, `crosswalk_variavel`, `observacao`, `cobertura`, `build` e `build_source`: conteúdo original preservado por hash estável de todas as linhas.
- `fonte`: registros fiscais originais preservados, com apenas uma nova fonte de referência SIAFEM.
- `v_observacao_publicavel`: linhas e valores anteriores e posteriores à importação idênticos.
- `PRAGMA integrity_check` aprovado nos dois bancos; `PRAGMA foreign_key_check` sem violações.
- **34 atores prefeituras**, **752 instrumentos estaduais**, **889 linhas convênio-ano**, **1.017 pagamentos contabilizados pela fonte** e **30.552.102.920 centavos** (R$ 305.521.029,20) de valor liberado/estornado.
- **Zero lançamentos bancários individuais inventados** e zero projetos homologados automaticamente.
- Resultado do importador: origem `canonico_2025_reconstruido.sqlite` preservada; destino `siafem_isolado_qa.sqlite` criado apenas no runner descartável.

## 4. Restrições e próximo gate

**O QA sobre dados reais de 2025 está concluído, mas o QA sobre a materialização histórica de 2013–2025 permanece aberto.** Não há base para afirmar regressão de todas as séries históricas, pois o importador local foi executado contra a fotografia 2025.

O estágio SIAFEM `inv_siafem_convenio_ano` representa **transferências estaduais agregadas por instrumento e ano**, não pagamentos individuais, despesa de capital executada por município ou investimento físico concluído. Não é aditivo com orçamento previsto, transferências federais de mesmo financiamento ou despesa municipal posteriormente realizada.

Próximas operações: (a) confirmar qual pipeline reconstrói a base histórica em SQLite e ensaiar sobre esse snapshot quando disponível; (b) derivar prévia isolada para consulta por município, sub-região, ano e convênio apenas a partir da série anual exata, sem promoção à API pública de produção; (c) QA de não dupla contagem e de estado `em_revisao`; (d) manter FED04/PR #232 intocados.

**Governança:** nenhum R2, SQLite ou D1 produtivo foi escrito; PR #233 sem merge ou implantação produtiva.
