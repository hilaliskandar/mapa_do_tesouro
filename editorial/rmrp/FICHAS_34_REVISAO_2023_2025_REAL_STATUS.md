# RMRP — fichas municipais com série 2023–2025 e atualização real

Atualização: 19/10/2026. **Status: produto analítico candidato; não publicado.**

A revisão do caderno municipal incluiu o exercício intermediário de 2024 e a comparação monetária de 2023 a 2025 em preços de setembro de 2026, com os fatores da série IBGE/SIDRA 1737 já utilizados em `ANALISE_REAL_IPCA_SUBREGIOES_2013_2025.md`.

Produtos integrais gerados no pacote desta conversa:
- `FICHAS_FISCAIS_34_MUNICIPIOS_REVISAO_2023_2025.md` (34 fichas em quatro sub-regiões, com valores nominais e reais, participação tributária, intensidade de investimento e comparação com o agregado sub-regional).
- `INDICADORES_FICHAS_34_MUNICIPIOS_2023_2025_REAL.csv` (34 linhas, três exercícios e indicadores derivados).
- `QA_FICHAS_REVISADAS_2023_2025.json` (75 verificações aprovadas).
- `revisar_fichas_34_2024_real.py` (rotina reproduzível).

Fonte dos dados: `DCA_SP_645_2013_2025_CANONICO.csv` (Google Drive ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`) e roster `editorial/rmrp/municipios_subregioes_tcesp.csv`. Foram aprovadas 75 verificações independentes de somas por sub-região e pelo total RMRP (cinco contas × três anos × cinco recortes), com 34/34 observações das contas testadas em cada ano. O cadastro permanece 15+6+6+7.

## Alertas de leitura

Alguns municípios apresentaram variações negativas reais de investimento acima de 80% entre 2023 e 2025, entre eles Santa Cruz da Esperança, Sales Oliveira e Jardinópolis. O resultado não equivale, por si, à suspensão de investimentos físicos ou à avaliação de desempenho. A inclusão de 2024 permite identificar picos ou vales intermediários, evitando atribuir uma trajetória monotônica a todos os municípios.

Diferenças entre investimento/receita municipal e taxa da sub-região foram calculadas contra razões de somas, nunca como média simples das razões locais. A CAPAG é apenas categoria municipal do snapshot. A divergência TCESP-DCA Guatapará de 2023 (R$ 10.176,00) segue preservada. A triagem de precatórios permanece simplificada, sem pesquisa individual de processos.

## Próximas providências

1. Incorporar integralmente as fichas e a matriz auditável à versão editorial do repositório, evitando perda dos arquivos entre sessões.
2. Fazer revisão autoral seletiva dos 34 perfis, verificando as maiores diferenças intermunicipais, a influência dos maiores municípios e anos atípicos.
3. Integrar o panorama metropolitano, quatro sub-regiões e fichas em caderno único, com sumário, notas de fonte e indicadores de cobertura por exercício.
4. Executar os controles de publicação e homologação antes de alterar o caderno público ou a API fiscal.

**Este registro resume o produto, mas não substitui os arquivos integrais.**