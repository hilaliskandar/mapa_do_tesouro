# Paridade externa RREO e CAPAG — 16/10/2026

## Fontes independentes e versão auditada
- **RREO 2025**: coleta Gate C [run 37728745160](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/37728745160), artefato `gate-c-rreo-rcl-sp645-2025` ID `11529781219`, CSV `normalized/rreo_rcl_2025.csv` SHA-256 `d66d92bd8b75e319d0c6bb432961e791f2c5ad10d25f197b3a10db512ed75ba3`. Anexo 03, período 6, coluna TOTAL (ÚLTIMOS 12 MESES), 2025.
- **CAPAG oficial**: arquivo `capag-municipios-posicao-2026-set.xlsx` no Drive, ID `1BlT2WxtBIGVeP1b4-GM3Auv0OdU6p7C9`, SHA-256 `1b1379a5a531920223f1d448be155b70f51eb50180d8c819f1b7da3575a8eb11`; posição 01/09/2026 e ano-base 2025.
- **Base candidata**: `sp645_private.sqlite` do build privado aprovado [run 38905063653](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38905063653), artefato ID `12048275648`.

## Resultados executados
RREO: confrontados os 645 códigos IBGE em `rreo_rcl_total_12m` do CSV Gate C versus `rreo_rcl_oficial` do SQLite; 531 valores observados coincidentes em centavos (tolerância 0,01), 114 ausências coincidentes, **zero divergências**.

CAPAG: comparados os 645 códigos IBGE na planilha oficial versus `capag` do SQLite; **645 classificações coincidentes, zero divergências**. Distribuição: A+ 27, A 108, B+ 17, B 68, C 371, D 1, n.d. 53.

**Cautela sobre a planilha CAPAG:** a aba `Prévia da CAPAG` possui **duas tabelas distintas**, ambas com coluna `CAPAG`. Na primeira, colunas 1–4, há distribuição diferente, incluindo categoria `n.e.`, com 103 diferenças contra o SQLite; essa não é a coluna de classificação oficial definida pelo catálogo do projeto. A segunda tabela, **código IBGE na coluna 25 e classificação CAPAG na coluna 28**, corresponde à distribuição oficial previamente documentada e tem paridade integral. Confundir as duas representa risco real de regressão ou divulgação de nota incorreta. A auditoria deixa ambas explícitas, sem apagar a constatação inicial.

A implementação reproduzível está em `editorial/multiuniverso/qa_externa_capag_rreo.py` com controle SHA dos dois arquivos, extração por código IBGE, comparação de status e tratamento de `n.d.` como categoria oficial. Separadamente, `pipeline/qa/audit_capag_official_distribution.py` impõe controle agregado na construção privada, mas **não substitui** a paridade individual.

## Decisão
Os recortes auditados de RREO (RCL 2025) e CAPAG (classificação oficial setembro/2026, ano-base 2025) estão aprovados para a **base privada candidata**. Não significa homologação dos outros anexos RREO, outros anos, ou dos três indicadores constitutivos CAPAG. O PR #198 permanece isolado, sem merge nem deploy; exigem-se ainda revisão editorial final e garantia de URLs canônicas de fonte para publicação.
