# Matriz de migração do mapa_do_tesouro

Classificações:
- **PROMOVER**: conceito ou componente deve entrar no núcleo canônico do novo projeto.
- **ADAPTAR**: conteúdo relevante, mas precisa ser reescrito para a nova arquitetura ou reconciliado com a base atual.
- **LEGACY**: preservar integralmente para rastreabilidade e consulta histórica, sem usar como base de produção.
- **DESCARTAR**: não transportar para o novo núcleo; manter apenas no histórico Git do projeto original.

| Origem | Classificação | Destino proposto | Justificativa |
|---|---|---|---|
| README.md — finalidade, perguntas analíticas e princípios | PROMOVER | README.md + governance/METHODOLOGY.md | Define auditabilidade, granularidade, ausência ≠ zero e limites interpretativos |
| README.md — referências MCASP, MDF, PCASP, MSC, CAPAG, IFGF, IBGE etc. | ADAPTAR | governance/SOURCES.md | Conteúdo relevante, mas versões e links devem ser verificados/atualizados |
| README.md — execução Streamlit | LEGACY | reference/legacy/mapa_do_tesouro/ | Arquitetura substituída por static-first/Cloudflare |
| CHANGELOG.md | PROMOVER COMO HISTÓRICO | reference/legacy/mapa_do_tesouro/CHANGELOG.md | Registra decisões metodológicas e correções importantes |
| docs/arquitetura_analitica.md | ADAPTAR | governance/ARCHITECTURE.md + METHODOLOGY.md | Boa modelagem conceitual, porém arquitetura técnica muda |
| docs/mapa_semantico.md | PROMOVER | governance/METHODOLOGY.md + pipeline/harmonization/ | Base conceitual diretamente relevante ao crosswalk temporal |
| docs/nota_versao_*.md | LEGACY | reference/legacy/mapa_do_tesouro/docs/ | História técnica útil, não documentação operacional atual |
| configuracoes/indicadores.yml | ADAPTAR | governance/indicators.yml ou catálogo no SQLite | Fórmulas devem ser reconciliadas com os indicadores já consolidados no painel atual |
| configuracoes/configuracao_padrao.yml | ADAPTAR | config/ | Parâmetros úteis, mas caminhos e etapas precisam ser redesenhados |
| nucleo/gerenciador_execucao.py | ADAPTAR | pipeline/run_manifest.py | Ideia de manifesto e rastreabilidade deve permanecer |
| nucleo/gerenciador_cartografico.py | ADAPTAR | pipeline/geo/ | Reaproveitar validações; frontend usará GeoJSON/Leaflet |
| processamentos/normalizar_finbra.py | PROMOVER COM TESTE | pipeline/ingest/normalize_finbra.py | Normalização longa e preservação de proveniência são centrais |
| processamentos/construir_hierarquia_contabil.py | PROMOVER COM TESTE | pipeline/accounting/hierarchy.py | Proteção contra dupla contagem e relações pai-filho são essenciais |
| processamentos/construir_mapa_semantico.py | PROMOVER COM TESTE | pipeline/harmonization/semantic_map.py | Estrutura diretamente alinhada ao crosswalk temporal |
| processamentos/aperfeicoar_mapa_semantico.py | ADAPTAR | pipeline/harmonization/ | Regras devem ser consolidadas para evitar duplicação de lógica |
| processamentos/agregar_conceitos_semanticos.py | PROMOVER COM TESTE | pipeline/aggregations/ | Agregações auditáveis são requisito canônico |
| processamentos/calcular_indicadores.py | ADAPTAR | pipeline/indicators/ | Deve ser reconciliado com DCA/RREO/RGF/CAPAG já consolidados |
| demais processamentos de validação/qualificação | ADAPTAR | pipeline/validation/ | Aproveitar regras, simplificando artefatos intermediários |
| relatorios/*.py | LEGACY | reference/legacy/mapa_do_tesouro/ | Relatórios HTML/PDF deixam de ser núcleo do pipeline |
| aplicacao.py | LEGACY | reference/legacy/mapa_do_tesouro/ | Interface Streamlit não será base da nova aplicação |
| testes/teste_normalizacao.py | PROMOVER | tests/data/ | Testes de invariantes devem permanecer |
| testes/teste_reconciliacao_normalizacao.py | PROMOVER | tests/data/ | Fundamental para paridade |
| testes/teste_qualificacao_codigos.py | PROMOVER | tests/accounting/ | Protege interpretação de códigos |
| testes/teste_hierarquia_contabil.py | PROMOVER | tests/accounting/ | Protege contra regressão hierárquica |
| testes/teste_selecao_agregacao_hierarquica.py | PROMOVER | tests/accounting/ | Protege regra de seleção pai/filhos |
| testes/teste_mapa_semantico.py | PROMOVER | tests/harmonization/ | Essencial para comparabilidade temporal |
| testes/teste_agregacoes_semanticas.py | PROMOVER | tests/aggregations/ | Essencial para agregados canônicos |
| testes/teste_indicadores*.py | ADAPTAR | tests/indicators/ | Reconciliar fórmulas com catálogo atual |
| testes/teste_gerenciador_cartografico.py | ADAPTAR | tests/geo/ | Preservar validações úteis |
| testes/teste_gerenciador_execucao.py | ADAPTAR | tests/governance/ | Migrar para manifesto de build |
| testes/teste_versao_manifesto.py | PROMOVER | tests/governance/ | Versionamento explícito é requisito |
| referencias/catalogos/ | PROMOVER COMO REFERÊNCIA | reference/catalogs/ | Catálogos podem apoiar classificação e QA |
| pyproject.toml | ADAPTAR | pyproject.toml | Remover dependências exclusivas de Streamlit/relatórios e acrescentar stack do novo pipeline |

## Regras de promoção

Um módulo legado só poderá ser promovido para o novo núcleo quando:

1. houver teste automatizado;
2. a saída for reconciliada com a base consolidada do projeto FINBRA/TIC-TIM;
3. não alterar silenciosamente valores originais;
4. preservar proveniência e status de ausência;
5. registrar versão da regra;
6. não introduzir dependência desnecessária do frontend;
7. passar por comparação de regressão com os resultados canônicos atuais.

## Decisões já tomadas

- O banco nascerá com escopo estadual.
- `TIC_TIM_30` será um universo cadastrado.
- SQLite será o artefato canônico de dados.
- Cloudflare D1 será réplica operacional opcional.
- Consultas previsíveis serão pré-computadas em JSON e servidas por CDN.
- O painel HTML final será congelado como referência funcional, não como base de desenvolvimento.
- A interface Streamlit do legado não será portada como frontend principal.
