# Integração candidata dos recortes territoriais EL2026 ao universo de investimentos SP645

**Data:** 14/11/2026. **Destino:** `hilaliskandar/mapa_do_tesouro`, branch de desenvolvimento `investimentos-territoriais-sp645-20261111`. Sem alterações em SQLite, R2 ou site.

## Fontes originais efetivamente inspecionadas

EL2026 `hilaliskandar/el2026`, branch main:
- `dados_referencia/dim_municipio_tse_ibge_sp_2026.csv` — blob Git `e2b0e3b306372c30e25071e0fcc696de244f2ee1`, 645 pares TSE–IBGE7 únicos.
- `dados_referencia/regionalizacao_seade/conciliacao_v10/municipios_ra_rg_v10.csv` — blob `7122138f319b41a19b7029b4a85f366cf14f6d65`, 645 linhas com código TSE, RA/RG Seade, status de conciliação com pontos.
- `dados_referencia/regionalizacao_seade/conciliacao_v10/relatorio_qa.json` — `DIAGNOSTICO_NAO_HOMOLOGADO`; 16 RA, 43 RG, nenhum município sem região, método de votação por pontos de estabelecimentos.
- `dados_referencia/dim_rm_au_sp_2025_municipios.csv` — blob `920cc94aa348d988322b86a34322f2f1e40942bf`; 255 vínculos município–RM/AU distintos em referência 2025. Uma linha por município, removidas duplicações de São Paulo em sub-regiões.
- `docs/COMPOSICAO_RM_AU_2025.md` — documentação de 9 RMs e uma AU e 390 municípios externos às RM/AU; versão 2025, não verificação normativa atual.
- `dados_referencia/regionalizacao_seade/README.md` — fontes RA/RG geográficas Seade, 2021, arquivo de 16 e 43 polígonos CRS EPSG:4674 com SHA-256 e ressalvas de vigência.

## Conciliação efetiva

Foi feita associação exata `municipio_tse` → `CD_MUNICIPIO_TSE` → `CD_MUNICIPIO_IBGE`; no RM/AU a associação é diretamente por `COD_IBGE`. **Não** foi feita correspondência fuzzy por nome, e códigos de RM/AU (ex. `00301`, `04901`) permanecem texto para preservar zeros à esquerda.

| QA determinística por atributos | Resultado |
|---|---:|
| Municípios IBGE únicos | 645 |
| Linhas RA/RG correspondidas por TSE | 645 |
| RA distintas | 16 |
| RG distintas | 43 |
| RG associadas a mais de uma RA | **0** |
| Unidades RM/AU | **9 RM + 1 AU** |
| Municípios em RM/AU | 255 |
| Municípios fora de RM/AU | 390 |
| Códigos RM/AU sem correspondência IBGE | **0** |
| Municípios compartilhados entre RM/AU | **0** |
| Membros da RMRP na fonte RM/AU | **34** |
| Diferença simétrica contra roster RMRP34 já validado no projeto fiscal | **0** |

**Observação de integridade:** a hierarquia `SP -> RA -> RG -> município` é uma árvore de pertencimentos na versão inspecionada. As RM/AU constituem **outra dimensão de agrupamento**, que pode cortar RA e RG. Por exemplo, na junção por município a RM de Ribeirão Preto abrange **5 RA e 6 RG**; a RM de São José do Rio Preto abrange **2 RA e 4 RG**, e a AU de Franca abrange **2 RA e 3 RG**. Não forçar encaixe de RM/AU dentro de RA ou RG, nem somar totais de RA com totais de RM (sobreposição do universo).

## Materialização experimental

- CSV de 645 linhas: `governance/INV_SP645_CROSSWALK_RA_RG_RM_AU_EL2026_CANDIDATO_2026_11_14.csv`
- Script de QA: `pipeline/qa/audit_inv_sp645_el2026_territories.py`
- Workflow: `.github/workflows/inv-sp645-qa-territorios-el2026.yml`
- Execução iniciada [43621768319](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43621768319), **concluída com SUCCESS**: controles de código, pertencimento RG→RA, unicidade RM/AU, 645 municípios e RMRP34 aprovados; ainda não homologa vigência normativa ou geometria.

O CSV carrega somente códigos e nomes regionais, sem dados eleitorais ou valores financeiros. Possui campo `ra_rg_status=RA_RG_SEADE_2021_PROXY_NAO_HOMOLOGADO` para impedir utilização silenciosa como regionalização juridicamente vigente. O script verifica grãos, chaves, cardinalidade, pertencimento único RG→RA, RM/AU sem duplicidade e identidade RMRP34, produzindo JSON auditável.

## Modelo recomendado para uso fiscal

Preservar `municipio(codigo_ibge)` canônico. Ao homologar as fontes:
- `dim_territorio(tipologia, codigo, nome, versao, fonte, status_vigencia)` com chaves compostas por tipologia + código + versão;
- `territorio_municipio(tipologia, codigo, versao, codigo_ibge, status_vinculo)`, grão município–território único;
- `hierarquia_territorial` somente para RG→RA (e ambos dentro de SP), **não** para RM/AU;
- `territorio_interseccao` opcional para cortes RA×RM/AU, derivado por códigos IBGE, sem rateios financeiros;
- `fora_rm_au` como categoria derivada dos 390 municípios, não como região administrativa fictícia.

As somas de indicadores **municipais comprovadamente territoriais** podem ser agregadas em cada tipologia separadamente. Valores de instrumento federal associados apenas ao município proponente devem ser apresentados como 'por município proponente', e não obra localizada. Empreendimentos plurimunicipais só podem ser atribuídos após prova do valor por município; sem prova, manter `nao_alocado`.

### Gates abertos

1. **P0:** RA/RG `DIAGNOSTICO_NAO_HOMOLOGADO` — confirmar pertencimento municipal em fonte Seade tabular/normativa e vigência; a conciliação atual por locais eleitorais não basta para afirmar hierarquia oficial.
2. **P0:** validar a referência RM/AU de 2025 contra atos vigentes em 2026 antes de rotular como composição oficial atual.
3. **P1:** testar dados municipais de investimentos em JOIN com a dimensão candidata e preservar totais por grupo; falha do join não deve zerar receitas.
4. **P1:** quando houver resultados de investimento por município executor, desdobrar RA/RG/RM/AU separadamente; proponente e local da obra não são atributos intercambiáveis.
5. **P2:** persistir versão homologada no R2, com readback e versões; não mesclar o resultado candidato ao SQLite/D1 de produção.

**Decisão:** recortes são estruturalmente reutilizáveis **já**, sob indicação de status e ano de referência; homologação normativa e operacional de agregados financeiros ainda pendentes.


## Esclarecimento corretivo — 14/11/2026

**A unidade territorial do painel EL2026 para Estado, RA, RG, RM/AU e município é o MUNICÍPIO por código IBGE7.** A agregação das 645 unidades municipais deve preceder qualquer decomposição eleitoral. **Zona eleitoral, local de votação e seção são componentes exclusivamente eleitorais** e não compõem o universo fiscal de investimentos.

A auditoria anterior cruzou um cadastro municipal **IBGE7** (via `dim_municipio_tse_ibge_sp_2026.csv`, necessário somente porque a versão de diagnóstico RA/RG estava indexada por município TSE) com `municipios_ra_rg_v10.csv`. O script desse último arquivo documenta que a **atribuição RA/RG específica dessa versão candidata** foi inferida por localização dos **locais de votação**, e portanto não é certificação do vínculo administrativo municipal. Isso não significa que a regionalização municipal da plataforma, o cadastro de 645 municípios ou o modelo fiscal sejam derivados de zonas eleitorais.

Para integração definitiva, **não usar `municipios_ra_rg_v10.csv` como fonte canônica de RA/RG municipal**. Reutilizar somente como candidato/conferência; reconstruir RA/RG por composição municipal oficial do Seade ou interseção homologada da malha IBGE com regiões Seade, com verificação de vigência, sem passagem por pontos, zonas ou seções eleitorais.

A dimensão RM/AU 2025 já utiliza diretamente `COD_IBGE` e o modelo resultante conserva unicamente `codigo_ibge` como chave de agregação. O campo `codigo_tse` no CSV candidato é atributo de rastreabilidade do cruzamento de origem e **deve ser removido da dimensão canônica financeira quando houver fonte RA/RG municipal homologada**.

**Errata conceitual:** a restrição de homologação RA/RG diz respeito ao **método de atribuição no arquivo candidato específico**, não à identidade IBGE dos 645 municípios nem à composição por zonas eleitorais. Essa distinção deve constar do README e do procedimento de expansão estadual.
