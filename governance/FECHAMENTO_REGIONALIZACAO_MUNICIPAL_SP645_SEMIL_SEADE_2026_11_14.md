# Regionalização dos 645 municípios — fonte direta SEMIL/Seade e integração fiscal

**Data da extração:** 14/11/2026. **Status:** fonte estadual municipal lida integralmente, identidades e associações verificadas; QA de workflow em execução quando este documento foi elaborado. Não houve alteração do banco SQLite/D1, R2 produtivo, site ou dados de investimentos.

## Decisão de fonte e distinção conceitual

**A regionalização fiscal é por código IBGE7 do MUNICÍPIO.** Não deriva de zonas eleitorais, locais de votação ou seção. A localização de obras, quando conhecida, é atributo distinto do município proponente.

A extração prioritária ocorreu diretamente pela camada municipal **Limite_Muncipal_IGC_Seade** no serviço cartográfico da Secretaria de Meio Ambiente, Infraestrutura e Logística do Estado de São Paulo — SEMIL:

- Serviço: https://mapas.semil.sp.gov.br/server/rest/services/Hosted/Limite_Muncipal_IGC_Seade/FeatureServer/0
- Consulta utilizada: https://mapas.semil.sp.gov.br/server/rest/services/Hosted/Limite_Muncipal_IGC_Seade/FeatureServer/0/query?where=1%3D1&outFields=cod_ibge%2Cmunicipio%2Cgid_ra%2Cgid_rg%2Cra%2Crg&returnGeometry=false&resultRecordCount=1000&f=pjson
- Conferência independente `returnCountOnly=true`: **645 registros**.
- Metadados da camada: `maxRecordCount=2000`, paginação suportada, campos `fid`, `cod_ibge`, `municipio`, `gid_ra`, `gid_rg`, `ra`, `rg`.
- Resposta dos 645 atributos: `exceededTransferLimit=false`; não se restringiu a página parcial, nem a um filtro de regiões.
- A data da consulta **não** equivale a data jurídica de vigência regional. Registrar a referência temporal da fonte, e revisar atos vigentes para estudos históricos.

O acervo original Seade com **16 polígonos RA, 43 polígonos RG, CRS EPSG:4674** foi previamente auditado a partir dos ZIPs fornecidos. A tabela `DIM_HIERARQUIA_SEADE_RG_RA_GEOMETRIA_2026_11_14.csv` estabelece vínculo entre todas as 43 RG e sua RA única por interseção espacial.

## Resultado do confronto integral

| Verificação | Valor |
|---|---:|
| Registros municipais do serviço público estadual | 645 |
| Códigos IBGE únicos e válidos, UF SP (prefixo 35) | 645 |
| Regiões Administrativas distintas | 16 |
| Regiões de Governo distintas | 43 |
| Vinculações RG→RA divergentes da hierarquia derivada dos ZIPs originais | **0** |
| Códigos ausentes no cadastro candidato SP645 | **0** |
| Municípios da RMRP preservados | 34/34 |
| Divergências de códigos RA/RG frente à tabela experimental anterior | **0** |
| Regiões Metropolitanas e Aglomerações Urbanas (referência 2025) | 9 RM + 1 AU |
| Municípios em RM/AU (referência 2025) | 255 |
| Municípios fora de RM/AU | 390 |

A coincidência com a matriz preliminar de EL2026 representa **concordância entre duas rotas de verificação**, não autenticação da origem eleitoral como fonte fiscal. A tabela nova usa os seis atributos recebidos diretamente do serviço estadual; a composição RM/AU é importada separadamente da dimensão municipal `dim_rm_au_sp_2025_municipios.csv` de EL2026.

## Produtos versionados

1. [DIM_SP645_IBGE_RA_RG_SEMIL_SEADE_2026_11_14.csv](DIM_SP645_IBGE_RA_RG_SEMIL_SEADE_2026_11_14.csv) — dimensão municipal diretamente recuperada do serviço SEMIL/Seade, 645 linhas, com IBGE7, nomes, códigos e denominações RA/RG.
2. [DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv](DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv) — dimensão candidata consolidada, 645 linhas e **zero dependência de TSE/zonas/locais**, usando RM/AU do recorte 2025 e campos de referência.
3. [audit_sp645_ibge_seade_semil_regionalizacao.py](../pipeline/qa/audit_sp645_ibge_seade_semil_regionalizacao.py) — teste determinístico de chaves, integridade, universo, relação RG→RA e igualdade da RMRP34.
4. [Workflow automatizado](../.github/workflows/inv-sp645-qa-municipal-semil.yml) — geração de artefato QA em ambiente isolado.

## Orientações para aplicação nos investimentos

- A tabela municipal usa a chave **`codigo_ibge`**, que deve se ligar ao cadastro `municipio`/universo `SP_645` do SQLite, após controle de cardinalidade 645→645 e `read-only` da fonte canônica.
- A dimensão RA/RG agora **dispensa totalmente o proxy eleitoral**. A anterior `INV_SP645_CROSSWALK_RA_RG_RM_AU_EL2026_CANDIDATO_2026_11_14.csv` está **SUPERADA PARA USO FISCAL**; preservada somente como histórico de auditoria.
- As tipologias `RA`, `RG` e `RM/AU` devem ser agregadas separadamente, sempre a partir do **grão de município único**. RM/AU e RA/RG se sobrepõem e não se somam.
- Nas séries fiscais, os agregados territoriais devem manter `papel_municipal` (proponente, beneficiário formal, executor, local da obra) e `estagio_financeiro` (plano, empenho, desembolso, pagamento, aplicação, despesa municipal) para evitar dupla contagem.
- Localidade ou evento cuja classificação territorial esteja ausente deve ser `nao_alocado` ou `nao_observado` conforme o caso, jamais zero.
- **Limite temporal:** este produto associa uma fotografia regional capturada em 14/11/2026 a RM/AU 2025; verificar a vigência institucional para comparações históricas e para a descrição jurídica de 2026. Não alterar bases produtivas sem controle de versão e homologação financeira.

## Histórico de resolução de bloqueios

As tentativas anteriores de baixar o CSV municipal do repositório Seade sofreram `timeout`; as tentativas de usar o repositório privado EL2026 em runner externo geraram 404. A fonte direta pública SEMIL resolveu o impasse de correspondência municipal sem depender desses servidores, fornecendo 645 registros completos. A captura de geometria municipal do IBGE deixa de ser necessária **para identificar os vínculos municipais RA/RG** nesta fotografia; continua útil como fonte independente para QA geométrico e eventual cartografia.


## Confirmação automatizada e quadros de consulta — fechamento complementar

O workflow [43628653845](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43628653845) concluiu **SUCCESS**, inclusive nas etapas de auditoria determinística e de upload do manifesto QA. Foram confirmados o grão de 645 IBGE7 únicos, 16 RA, 43 RG, RG→RA sem conflito, 10 RM/AU em composição 2025, 255 municípios em RM/AU, 390 externos e RMRP 34/34.

- [Resumo de 69 unidades territoriais](RESUMO_TERRITORIOS_SP645_RA_RG_RM_AU_2026_11_14.csv): 16 RA + 43 RG + 9 RM + 1 AU, com contagem de municípios e RA-pai das RG.
- [28 interseções não vazias RM/AU × RA × RG](INTERSECCOES_RM_AU_RA_RG_SP645_2026_11_14.csv): contagem por pertencimento municipal único para análises comparativas, sem duplicação.
- A consulta independente ao serviço público `returnCountOnly=true` retornou **645**, exatamente o número de atributos recuperados, sem sinal de transferência parcial. O `maxRecordCount` declarado no endpoint é **2000**.

**Situação:** a identidade e composição da fotografia consultada estão verificadas. Permanecem como gates específicos a conciliação temporal de atos de regionalização (especialmente para séries antigas) e a carga ao SQLite fiscal canônico com readback e promoção supervisionada. A presente edição não alterou valores de investimento nem bases publicadas.
