# FED06B — territorialização das quatro sub-regiões legais da RMRP

**Execução:** 15/11/2026. **Status:** correspondência município–sub-região validada e materializada na prévia **privada** da API v3. Não equivale a localização de obra ou homologação financeira.

## Fundamento normativo e fontes

- Lei Complementar estadual nº 1.290, de 6 de julho de 2016, **artigo 4º**, promulgada no DOE de 7/7/2016: [Alesp](https://www.al.sp.gov.br/norma/178709) e [DOE original](https://www.imprensaoficial.com.br/Certificacao/GatewayCertificaPDF.aspx?notarizacaoID=36ec97f7-da47-4cb8-9587-5f4496f80f1d).
- [Panorama Regional do PDUI da RMRP, 2021](https://rmrp.pdui.sp.gov.br/wp-content/uploads/P5_PANORAMA-REGIONAL-RMRP_14122021.pdf): enumera os mesmos agrupamentos de 15, 6, 6 e 7 municípios.
- Alesp registra a lei nº 1.290/2016 como sem revogação expressa e sem alterações cadastradas na página consultada em 15/11/2026. Textos de **projetos de lei de 2022** que propuseram retirada de municípios não foram aplicados à dimensão vigente sem comprovação de aprovação.

A lista de 34 municípios com código IBGE7 está versionada em [`governance/DIM_RMRP34_IBGE_SUBREGIOES_LC1290_2016_2026_11_15.csv`](DIM_RMRP34_IBGE_SUBREGIOES_LC1290_2016_2026_11_15.csv). Preservar `codigo_ibge` como texto.

## Processamento realizado

Origem: `RMRP_FED06_PREVIEW_API_V3_PRIVADA_2026-11-15.zip`, SHA-256 `f9823c325c5e56df1707d37205b1071ad1c06b320163e364ba9e55d074d50957`.

1. Verificação exata e bijetiva dos nomes legais contra os 34 códigos IBGE dos arquivos de índice municipal; sem atribuição por semelhança aproximada. Normalização técnica apenas de maiúsculas e acentos.
2. Materialização de `subregioes.json` e `subregioes/01.json` a `subregioes/04.json`.
3. Inclusão de `subregiao_rmrp_codigo`, `subregiao_rmrp_nome` e URL de origem normativa no índice e nos 34 arquivos municipais. Atualização do `manifest.json` e `pendencias.json`.
4. Conservação dos 218 arquivos de projeto, 19 arquivos anuais e dos valores originais, mantendo `public_release_authorized=false`.
5. Inclusão do script reprodutível no próprio ZIP privado.

### QA

| Indicador | Resultado |
|---|---:|
| Sub-região 01 | 15 municípios |
| Sub-região 02 | 6 municípios |
| Sub-região 03 | 6 municípios |
| Sub-região 04 | 7 municípios |
| Municípios sem grupo / atribuídos a mais de um grupo | **0 / 0** |
| Arquivos JSON no pacote atualizado | **280** |
| Propostas discricionárias preservadas | 6.410 |
| Convênios preservados | 1.793 |
| Desembolsos preservados | 2.537 |
| Emendas, vínculos, preservados | 1.240 |
| Propostas Parcerias preservadas | 743 |
| Projetos Obrasgov por proponente preservados | 218 |
| Integridade dos totais sub-regionais × índices municipais | **aprovada** |
| Corrupção de ZIP | **nenhuma** |

O conjunto soma exatamente 34 municípios e seus quantitativos reproduzem o SQLite de origem por `municipio_proponente`. O pacote de saída contém 280 JSON, um script e outros arquivos auxiliares. As quatro sub-regiões são **recortes administrativos oficiais**, não prova de execução territorial de projetos.

## Persistência privada e rastreabilidade

Pacote: [RMRP_FED06B_SUBREGIOES_PRIVADA_2026-11-15.zip](https://drive.google.com/file/d/1gjLGe4IfK5WipARJ7SBo9WcsGWtrFoQ5/view), ID Drive `1gjLGe4IfK5WipARJ7SBo9WcsGWtrFoQ5`, na pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`. Readback após upload confirmou tamanho **617.065 bytes**, acesso não compartilhado, SHA-256 `efebff7aaff130aae57587c5aa5fd138e94706be8a4e76a5946c6807636778da` e `testzip()=None`.

Pacote FED06 anterior preservado no mesmo Drive, ID `15T2iptAUK3TsQ-_EMQumaNK3jTugE8Zk`, 603.812 bytes, SHA-256 `f9823c325c5e56df1707d37205b1071ad1c06b320163e364ba9e55d074d50957`. Nenhuma alteração ao banco canônico ou Pages.

## Gates que continuam bloqueando a publicação

- **FED03C:** ainda falta capturar e conciliar os arquivos nacionais de `siconv_pagamento`, `siconv_obtv_convenente`, `siconv_dl` e `siconv_itens_dl`, mais CGU quando disponível. **Não** denominar desembolso ao convenente de investimento pago. Pagamentos ↔ OBTV seguem relação 1:N.
- **FED04B:** coordenadas de propostas `siconv_coordenadas_obra` e correspondências projeto–instrumento ainda dependem de fonte e validação geométrica.
- **FED06 final:** falta hospedagem privada e homologação funcional; a prévia de arquivos não é um deploy. O manifesto continua com `public_release_authorized=false`.

A dimensão sub-regional não deve voltar a constar como pendência. Prioridade imediata: recuperar insumos nacionais pelo ambiente de aquisição autorizado, sem refazer as 80 páginas de propostas e 218 consultas Obrasgov concluídas.
