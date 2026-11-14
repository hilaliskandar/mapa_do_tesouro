# Retomada da regionalização municipal IBGE–Seade sem dados eleitorais

Data de referência: 14/11/2026. Resultado: protocolo e códigos preparados; **cruzamento dos 645 polígonos municipais ainda não executado com sucesso**. Nada promovido ao banco canônico.

## Entradas auditadas

Arquivos ZIP enviados pelo usuário em duas versões:
- `regiao_administrativa(1).zip`: SHA256 `951dc1c9b8e608c076d3838dadbe5824742a023be3803fbdcc51ed905340929c`, 16 geometrias Seade, `GID_RA` e `RA`, EPSG:4674, válidas, não vazias, ZIP sem erro CRC.
- `regiao_de_governo(1).zip`: SHA256 `6610569fff8fe7cbef5bffc1c658b4af63839be9a2152b930213b8cd6baa1a22`, 43 geometrias Seade, `GID_RG` e `RG`, EPSG:4674, válidas, não vazias, ZIP sem erro CRC.

Os hashes conferem exatamente com os ZIPs originais arquivados em `hilaliskandar/el2026/dados_referencia/regionalizacao_seade/fontes_originais/`. Os XLSX internos são dicionários de atributos de RA e RG, **não tabelas de pertencimento IBGE7 por município**.

Fonte territorial independente dos dados eleitorais, descoberta e verificada no catálogo do IBGE: `https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2025/UFs/SP/SP_Municipios_2025.zip`, ~15 MB, malha municipal SP 2025, publicado pelo IBGE; sistema SIRGAS 2000. A URL existe no catálogo; o download falhou neste container por indisponibilidade de resolução DNS, sem comprovar que a fonte esteja fora do ar. <https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html>

Fonte adicional tabular Seade, com códigos e agregações regionais: <https://repositorio.seade.gov.br/dataset/nomes-codigos-municipios-esp>, CSV `codigos_municipios_regioes.csv`. A tentativa direta em GitHub Actions falhou por **timeout** (run 43623267428); portanto seus campos e vínculos não foram homologados.

## Procedimentos implementados

A) `pipeline/qa/crosswalk_sp645_ibge_municipio_seade_regions.py` e workflow `.github/workflows/inv-sp645-ibge-seade-municipios.yml` no projeto `mapa_do_tesouro`. A tentativa [43625167920](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43625167920) falhou em HTTP 404 ao buscar o ZIP Seade por `raw.githubusercontent.com/hilaliskandar/el2026` de repositório privado — **falha de autenticação/distribuição de origem**, não teste geométrico.

B) Para reutilizar os ZIPs arquivados, foi criada **branch experimental isolada** `experiment/ibge2025-seade-ra-rg-sp645-20261114` no repositório `hilaliskandar/el2026`, com `scripts/auditar_municipios_ibge2025_seade_ra_rg.py` e `.github/workflows/qa-ibge2025-seade-ra-rg-municipal.yml`. Esta versão lê os ZIPs Seade diretamente do checkout, verifica SHA-256, baixa somente a malha IBGE e testa 645 códigos IBGE, uma única RA e RG por município e RG→RA. A tentativa [43625318339](https://github.com/hilaliskandar/el2026/actions/runs/43625318339) terminou `failure` **antes da alocação de runner**; a API retornou `runner_id:0`, `steps:[]`, `logs_url:null`, sem log técnico disponível. Não atribuir sem evidência esse evento a quota, credenciais ou código.

## Condições para continuidade

1. Reexecutar o workflow da branch experimental quando a infraestrutura Actions permitir, ou disponibilizar o ZIP oficial `SP_Municipios_2025.zip` no mesmo ambiente de análise dos dois ZIPs Seade.
2. Confirmar `CD_MUN` e `NM_MUN`, 645 geometrias municipais, CRS, validade, unicidade e cobertura do conjunto canônico.
3. Testar associação espacial de cada município IBGE às regiões Seade por geometria, registrar eventuais casos de fronteira, conferir cardinalidade e datas de referência 2021/2025.
4. Comparar com a tabela candidata anterior apenas como controle de regressão **sem usar pontos de votação como fonte**.
5. Gerar e revisar CSV municipal IBGE→RA→RG, conferir composição RM/AU com `COD_IBGE` 2025 e RMRP34, então persistir versão canônica com readback quando homologada.
6. Manter flag `candidato_espacial` até verificar vigência institucional de 2026. Nenhum valor monetário nem tabela de produção deve ser modificado por esta operação.

**Ponto conceitual:** o fato de um ZIP Seade conter regiões espacialmente representadas não o torna uma tabela de municípios. Para formar uma composição por município é necessária uma segunda origem com identificador IBGE municipal (malha municipal ou tabela tabular oficial), com junção auditável.
