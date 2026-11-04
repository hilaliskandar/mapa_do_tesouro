# Lote 91 — Recuperação da receita de capital bruta DCA I-C 2020–2025; acesso a bases federais

**Data:** 04/11/2026. **Volume:** II, RMRP, controle fiscal de pré-homologação. **Estado:** extração municipal concluída e persistida no Google Drive; comparabilidade e lacunas ainda sujeitas à homologação analítica.

## 1. Execução efetiva

Os seis arquivos oficiais arquivados no Drive de Anexo I-C FINBRA/DCA 2020–2025 foram recuperados, sendo cinco XLSX e um CSV, e examinados por script de extração reproduzível (local `gerar_capital_rmrp_lote91.py`). A filtragem adotou **código IBGE de cada um dos 34 municípios**, coluna exata **Receitas Brutas Realizadas** e identificador sintético **`siconfi-cor_RO2.0.0.0.00.0.0`**. Foram preservadas a identidade de cada arquivo, linha da fonte, status e unidade monetária em reais nominais. **Não foram somadas contas filhas**; duplicações por chave município–ano foram testadas.

O método foi conferido diretamente contra o cabeçalho das fontes (colunas `Instituição, Cod.IBGE, UF, População, Coluna, Conta, Identificador da Conta, Valor`). Foram lidas todas as linhas de dados do escopo e identificados 204 registros município–ano potenciais.

## 2. Resultado

| Ano | Observações | Ausentes | Duplicados | Soma observada, R$ correntes |
|---|---:|---:|---:|---:|
| 2020 | 34/34 | 0 | 0 | 311.469.228,18 |
| 2021 | 33/34 | 1 | 0 | 212.418.462,03 |
| 2022 | 33/34 | 1 | 0 | 295.518.170,79 |
| 2023 | 34/34 | 0 | 0 | 291.477.896,93 |
| 2024 | 32/34 | 2 | 0 | 356.106.269,27 |
| 2025 | 34/34 | 0 | 0 | 327.942.785,14 |
| **Total** | **200/204** | **4** | **0** | **não somar exercícios para inferência de saldo ou receita anual** |

**Ausências:**
- 2021: **Santa Rita do Passa Quatro**, código 3547502;
- 2022: **Santa Cruz da Esperança**, 3546256;
- 2024: **Cajuru**, 3509403; e **Morro Agudo**, 3531902.

Uma pesquisa complementar em toda a planilha dos respectivos exercícios **não localizou outras linhas correspondentes ao mesmo município e rubrica sintética `RO2.0.0.0`**. Ausência não significa valor zero e nenhum valor foi imputado. Para os exercícios incompletos, os totais metropolitanos são **somas parciais**.

**Controle 2025:** o total de **R$327.942.785,14** reproduz exatamente o resultado nominal agregado do **Lote 39**, em quatro sub-regiões; foi executada nova extração da fonte CSV 2025, sem simplesmente copiar o total anterior.

## 3. Proveniência por exercício

- 2020 XLSX: https://drive.google.com/file/d/1l5E_in3CFmz_PDUcgK8kEABbtRCMpYnu/view
- 2021 XLSX: https://drive.google.com/file/d/1m8SwRQooXJRd6RHHzr7UVnnbUSqYMW8R/view
- 2022 XLSX: https://drive.google.com/file/d/1q8ZjZ1W7L8cOY1bqOLHxBDFYGrgPb63s/view
- 2023 XLSX: https://drive.google.com/file/d/1SeGGScw5Vd9PrZzLBDcPg9KDXDAjjjRI/view
- 2024 XLSX: https://drive.google.com/file/d/1ZJyPzXbwB7jvnrOmQXjv5tS1Fpuq5enu/view
- 2025 CSV: https://drive.google.com/file/d/185x_7zgX9aGOy0Z6Drh-iA9vBY83JU1F/view

O cadastro dos 34 municípios e quatro sub-regiões foi conferido com `editorial/rmrp/municipios_subregioes_tcesp.csv`.

## 4. Artefatos gerados e efetivamente preservados no Drive

Todos enviados à pasta de arquivos-fontes `1ywdJpIzgXWC9otX9Rq0HBQqYTjzUnRSK`, com respostas `success: true` do conector:

- **XLSX municipal e síntese territorial:** https://docs.google.com/spreadsheets/d/1_pykfuwvsFF-2Cle4sHLrmqsxvU7JyUJ/edit — ID `1_pykfuwvsFF-2Cle4sHLrmqsxvU7JyUJ`;
- **CSV BR com 204 registros, ausentes identificados e URL por linha:** https://drive.google.com/file/d/18YAoDX6WbtKvG8oqBcVpT-qGCrZcHsb9/view — ID `18YAoDX6WbtKvG8oqBcVpT-qGCrZcHsb9`;
- **LEIA_ME metodológico:** https://drive.google.com/file/d/1gyOMJHuMtXpNlQk9rPBcg1D6l4meGdmO/view — ID `1gyOMJHuMtXpNlQk9rPBcg1D6l4meGdmO`.

Artefato local de QA `QA_RECEITA_CAPITAL_IC_LOTE91.json` foi produzido; a existência de arquivo no ambiente local **não equivale a arquivamento remoto**. O script gerador local também deve ser arquivado em repositório quando houver mecanismo seguro para transferir seu conteúdo, sem recriar como se já persistido.

## 5. Alcance e limites de homologação

Este lote recupera valores **brutos** e **nominais** de receitas de capital realizadas, **não** transferências de capital líquidas, receitas disponíveis em caixa, recursos efetivamente aplicados em investimentos, nem repasses individualizados de convênios. Os três exercícios com lacunas não podem ser usados como totais integrais de 34 municípios; comparar com 2025 requer cobertura equivalente e deflacionamento uniforme por IPCA médio anual para fluxos fiscais, conforme convenção do Volume II. Verificar mudanças de ementário/classificação entre 2020 e 2025.

As ausências permanecem em aberto, para conferência em declarações alternativas e retificações DCA sem imputação de zero.

## 6. Tentativa de acesso às bases federais do Transferegov

A URL pública do repositório federal de 65 arquivos ZIP/CSV, identificada no Lote 90, permanece conhecida. Foi testada uma via alternativa por Browserless, mas a integração respondeu **HTTP 401 por limite da cota gratuita**, sem execução do código de consulta. A falha de DNS do ambiente local na tentativa anterior de baixar ZIP persiste. **Não houve download nem filtragem de `siconv_convenio.zip` e `siconv_desembolso.zip` neste lote**, e não se deve declarar saneada a divergência dos identificadores 959097/953042 da escola de Guariba.

## 7. Próximos gates

1. Buscar declaração alternativa DCA ou retificações dos quatro municípios–anos ausentes; verificar se são faltas de envio ou de conta e documentar a situação por fonte.
2. Integrar 2015–2019 do Lote 38 (167/170) e 2020–2025 do presente lote em uma série de 11 anos, com matriz de completude e notas de mudança classificatória.
3. Implementar, quando houver acesso binário válido, a extração filtrada dos ZIPs federais e a conciliação do Termo FNDE 959097/2024.
4. Conferir RGF/RREO para oito municípios ainda ausentes e os indicadores anômalos de Pontal, sem misturar razão DCA com métrica legal.
5. Somente incorporar a nova série às análises do Volume II após deflator consistente, verificação da cobertura e da situação do título contábil.
6. Completar QA visual integral das 63 páginas e revisão jurídica; preservar a atual versão de trabalho até a homologação.

**Resultado:** execução do componente DCA 2020–2025 e persistência verificada de dados quantitativos no Drive, não apenas plano de extração. Volume II permanece em pré-homologação.
