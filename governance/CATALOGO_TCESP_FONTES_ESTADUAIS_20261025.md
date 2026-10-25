# Catálogo inicial de fontes TCESP — expansão estadual e exercício de 2026

Data de verificação: 25/10/2026. Fontes primárias: https://transparencia.tce.sp.gov.br/conjunto-de-dados e https://transparencia.tce.sp.gov.br/apis. Páginas efetivamente extraídas pelo Crawl2AI. Estado: catalogação e planejamento; não houve importação dos conjuntos nesta etapa.

## Descoberta substantiva
O catálogo oficial disponibiliza **downloads estaduais anuais consolidados** de despesas e receitas, além dos extratos municipais do portal. Priorizar esses arquivos consolidados como opção para cobertura dos 645 municípios, depois de confirmar identidade e layout das unidades municipais; preservar consulta municipal para 2026 parcial, preenchimento de lacunas e auditoria.

| Família | Referência temporal e atualização declaradas | Evidência no catálogo (25/10/2026) | Ação |
|---|---|---|---|
| Despesas consolidadas | 2008–2025, semanal | ZIP 2023: 1,96 GB, atualizado 03/02/2026; 2024: 1,93 GB, 13/10/2026; 2025: 1,96 GB, 21/10/2026 | Avaliar custos de ingestão dos três grandes ZIPs (não baixar automaticamente) |
| Receitas consolidadas | 2008–2025, semanal | ZIP 2023: 31,93 MB; 2024: 32,90 MB; 2025: 33,82 MB, atualização 21/10/2026 para 2025 | Primeiro piloto estadual, amostragem e QA |
| RCL mensal | Desde janeiro de 2015, semanal | CSV atualizado em 23/10/2026, 838,08 KB | Alta prioridade: snapshot + identidade de município/mês |
| Dívida ativa | Desde 2014, anual | CSV 2019–2024 e 2014–2018 | Importar somente após conferir layout e chaves |
| Resultado das análises Audesp (LRF, ensino, saúde) | Desde 2016, mensal | CSV atualizado em 01/10/2026, 468,90 KB | Piloto de valores e percentuais |
| Planejamento municipal | Quadriênios | Cadastro programas e ações 2018–2021, 2022–2025 e **2026–2029**, atualizado 30/07/2026 | Importar dimensões de programa/ação, com validade temporal |
| Relatório de atividades | Anual, desde 2015 | Conjuntos de programas até 2024 visíveis | Associar indicadores/metas, sem inferir resultados físicos dos valores financeiros |
| Ajustes, licitações e outras informações de contratação | Arquivos específicos, periodicidades heterogêneas | Recursos visíveis no catálogo | Catalogar como famílias próprias, distintas de execução fiscal |

## URLs oficiais confirmadas na página
- Despesas estaduais 2025: https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2025.zip
- Despesas estaduais 2024: https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2024.zip
- Despesas estaduais 2023: https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/despesas-2023.zip
- Receitas estaduais 2025: https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/receitas-2025.zip
- Receitas estaduais 2024: https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/receitas-2024.zip
- Receitas estaduais 2023: https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/receitas-2023.zip

## Consulta municipal e restrição importante
A página oficial de APIs documenta GET JSON/XML:
- /api/{formato}/despesas/{municipio}/{exercicio}/{mes}
- /api/{formato}/receitas/{municipio}/{exercicio}/{mes}
- /api/{formato}/municipios

**A própria documentação das APIs declara exercícios 2014–2019**, logo não é prova de suporte a 2023–2026. Verificar por consulta controlada antes de elegê-la canal de coleta recente. Para 2026, o código do projeto já utiliza downloads municipais do tipo https://transparencia.tce.sp.gov.br/sites/default/files/csv/despesas-{slug}-{ano}.zip; cobertura temporal depende dos meses presentes no arquivo.

## Regras de implementação
1. Não confundir fontes/datasets com dimensões de extração. Investimentos liquidados, movimentações e IPTU/ISS/ITBI são recortes derivados, não catálogo exaustivo do TCESP.
2. Separar versão de publicação da fonte, ano, mês, município, domínio, layout, tipo de movimentação e SHA-256; distinguir acervo temporário de R2 com readback.
3. Priorizar piloto de **receitas estaduais 2023–2025** e RCL, pela menor transferência, antes dos ZIPs de despesas de aproximadamente 2 GB por ano. Confirmar esquema, universo e eventual presença de entidades além das 645 prefeituras.
4. Comparar qualidade/conciliação com arquivos municipais TCESP já salvos (RMRP, RMJ, São Carlos), registrando divergências; não sobrescrever DCA/FINBRA.
5. 2026: não há ZIP anual estadual de despesas/receitas 2026 identificado na listagem consultada. Consultar extratos municipais, verificar quais meses estão presentes e nunca completar meses ausentes com zeros.
6. Planejar coleta seletiva missing-only após inventariar fontes em nível de dataset e objeto R2. Não iniciar grande download estadual antes do piloto.
7. Atualizar a matriz SP645 com hierarquia família do dataset > produto derivado > município > exercício > mês/versão, mantendo a matriz v2 como testemunho de cobertura dos três manifestos já preservados.

## Próxima execução
Inspecionar o layout de uma amostra oficial de receitas consolidadas, confirmar chaves municipais e reconciliação com município conhecido; testar o catálogo RCL; só então formalizar jobs segmentados de importação e QA, sem alteração da API pública.

## Piloto efetivamente executado — receitas estaduais 2025
- Workflow somente leitura: `.github/workflows/tcesp-receitas-2025-schema-probe.yml`; script `governance/probe_tcesp_receitas_2025.py`.
- Run [40236994657](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40236994657), conclusão `success`; artifact `tcesp-receitas-2025-schema-probe`, ID `12615171971`. O relatório JSON foi recuperado e lido.
- Fonte: `https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/receitas-2025.zip`.
- ZIP de **35.462.775 bytes**; SHA-256 `16df083d2088127108957a028f6c824265813c74542f528108526b44a392b84b`.
- Um arquivo interno: `receitas-2025.csv` de **523.628.376 bytes** descompactados. Primeira amostra decodificada em Latin-1, separador `;`, **18 colunas**: `id_rec_arrec_detalhe, ano_exercicio, ds_municipio, ds_orgao, mes_referencia, mes_ref_extenso, ds_poder, ds_fonte_recurso, ds_cd_aplicacao_fixo, ds_cd_aplicacao_variavel, ds_categoria, ds_subcategoria, ds_fonte, ds_d1, ds_dd2, ds_d3, ds_tipo, vl_arrecadacao`.
- **Limite da prova:** inspeção de cabeçalho e cinco amostras, sem percorrer todos os registros. Número de municípios, meses existentes, totais e conciliação TCESP/DCA **não verificados** ainda. Dados não persistidos no R2 nem ingeridos no SQLite.
- Próxima etapa: pipeline de streaming sobre o ZIP para enumerar municípios/meses, contar linhas, validar chaves, parse monetário em centavos e gerar totais por município/mês/classificação, sem guardar dados identificadores individuais; comparar amostras selecionadas com extratos locais já preservados antes de autorizar promoção R2.

## Auditoria integral de receitas estaduais 2025 — execução concluída
- Run [40237096710](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40237096710), conclusão **success**; artifact `tcesp-receitas-2025-full-qa` ID `12615267305`, ZIP e relatório `qa.json` efetivamente recuperados.
- Script reproduzível `governance/auditar_tcesp_receitas_estaduais_2025.py`; workflow `.github/workflows/tcesp-receitas-2025-full-qa.yml`. Arquivo fonte com SHA-256 `16df083d2088127108957a028f6c824265813c74542f528108526b44a392b84b` (mesmo ZIP da prova de esquema).
- CSV completo: **896.299 linhas**, **644 valores distintos de ds_municipio**, todos os registros com `ano_exercicio=2025`, sem município vazio, mês inválido ou valor monetário inválido. **Todos os 644 têm meses 1–12 representados** (não prova valor positivo em cada mês).
- Foram emitidos `linhas_por_municipio`, `totais_por_municipio_centavos`, distribuição de cobertura mensal e diagnóstico de preenchimento. A conferência dos valores usa Decimal em centavos e conserva ajustes negativos.
- **Ponto de identidade territorial:** são 644 municípios identificados frente ao universo SP645 da plataforma. O CSV usa nome do município, não código IBGE. Antes de converter em cobertura 644/645, reconciliar nomes oficiais e a jurisdição sobre a capital paulista; não presumir que o ausente corresponde a um determinado município sem confrontação.
- **Limites:** ainda não foram cruzados valores com DCA ou arquivos municipais; o resultado não equivale a persistência R2 ou ingestão SQLite. Nenhum dado bruto de 2025 foi incorporado à plataforma pública.
- Próxima etapa: conciliar 644 nomes com roster IBGE SP645 (acentos, homônimos, nomes históricos); registrar explicitamente eventual jurisdição TCM-SP e executar cruzamentos agregados seletivos com RMRP/RMJ/São Carlos. Depois estender procedimento a 2023–2024 e atualizar 2026 por extração municipal parcial.

## Jurisdição e conciliação territorial — verificação de 25/10/2026
- O `qa.json` do artifact `12615267305` foi reaberto diretamente: entre os **644 nomes** encontrados na receita TCESP 2025, **não há município `São Paulo`**; nomes contendo `Paulo` incluem `Paulo de Faria`, mas não a capital.
- Confirmado por fontes primárias do próprio TCESP: o Tribunal fiscaliza os **644 municípios paulistas exceto a Capital**. Referências oficiais: https://www.tce.sp.gov.br/paineis-tcesp (Observatório Fiscal, 644 exceto Capital); https://www.tce.sp.gov.br/6524-86-municipios-paulistas-apresentam-desequilibrio-contas-aponta-tcesp (22/07/2025). A capital é jurisdicionada ao Tribunal de Contas do Município de São Paulo, conforme https://portal.tcm.sp.gov.br/Pagina/53040.
- **Decisão de modelagem:** SP645 permanece universo estadual canônico; TCESP fornece 644 municípios sob sua jurisdição; São Paulo (código IBGE **3550308**) deve compor a plataforma por fonte própria identificada (TCM-SP e/ou finanças municipais com proveniência), sem criar linha zero ou classificar como falha de extração do TCESP.
- Primeiro teste de cruzamento com a DCA (run `40237361965`) falhou com diagnóstico controlado: CSV DCA possui apenas `cod_ibge` e indicadores, sem coluna nominal. O segundo teste (run `40237439710`) verificou DCA no R2 por hash, mas a consulta à API oficial de localidades do IBGE excedeu o tempo limite da rede GitHub Actions. **Correspondência nominal das outras 644 cidades não deve ser marcada como homologada até ocorrer comparação determinística com cadastro oficial.**
- Scripts/workflows reexecutáveis: `governance/conciliar_tcesp_receitas_2025_sp645.py`; `.github/workflows/tcesp-receitas-2025-sp645-roster-ibge.yml`. Não houve alteração dos dados-fonte, R2, SQLite ou plataforma pública.

## Homologação territorial do arquivo estadual de receitas TCESP 2025 — 25/10/2026
- Execução conclusiva [40238111626](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40238111626); artefato `tcesp-receitas-2025-sp645-roster-ibge` ID `12615802785`; `resultado.json` recuperado e reexaminado.
- DCA canônica lida do R2, validada por SHA-256; cadastro auxiliar público de código e nome IBGE usado para completar a coluna nominal ausente no arquivo DCA. Controle determinístico entre código municipal canônico e cadastro: **645 códigos distintos**.
- Fonte oficial atual do IBGE confirmou a denominação **Florínea, código 3516101** (https://www.ibge.gov.br/cidades-e-estados/sp/florinea.html e https://www.ibge.gov.br/explica/codigos-dos-municipios.php). O espelho auxiliar consultado conservava a grafia antiga `Florínia`. Correção explícita por código no script, sem aplicar correspondência aproximada indiscriminada.
- Resultados finais: **644 nomes TCESP**, **644 correspondências inequívocas com códigos IBGE**, **zero nomes não correspondentes**, **zero ambiguidades**, **um município fora da jurisdição TCESP**, `3550308 São Paulo`. A cobertura territorial do consolidado 2025 está **homologada para a jurisdição TCESP 644/644**, respeitando a distinção do universo estadual 645.
- Código: `governance/conciliar_tcesp_receitas_2025_sp645.py`; workflow `.github/workflows/tcesp-receitas-2025-sp645-roster-ibge.yml`. O estado homologado refere-se ao pareamento de nomes e códigos e à cobertura mensal identificada; **não implica conciliação contábil, aprovação de importação ou persistência em R2**.
- Próxima fase: amostragem de totais por município contra os extratos TCESP previamente preservados, inspeção de linhas de receitas por tipo/classificação, e eventual processamento de exercícios 2023/2024. O município São Paulo deve ser tratado em cadeia própria TCM-SP e fontes oficiais municipais.

## Denominação municipal Florínea e auditoria histórica de receitas
- Reconfirmação direta em 25/10/2026 nas fontes oficiais do IBGE: **Florínea**, código **3516101**. Referências: https://www.ibge.gov.br/cidades-e-estados/sp/florinea.html e https://www.ibge.gov.br/explica/codigos-dos-municipios.php.
- Documentos cartográficos históricos do mesmo IBGE registram **Florínia** para 3516101, inclusive mapa de 2007 (https://geoftp.ibge.gov.br/cartas_e_mapas/mapas_para_fins_de_levantamentos_estatisticos/contagem_da_populacao_e_censo_agropecuario_2007/mapas_municipais_estatisticos/sp/florinia.pdf). A grafia atual **Florínea** consta nos mapas do IBGE de 2022. Armazenar `Florínia` como variante histórica de nome, sem criar nova unidade geográfica e sem alterar montantes.
- Rotina QA estadual de receitas 2023 e 2024 criada: `governance/auditar_tcesp_receitas_estaduais_historico.py`; workflow `.github/workflows/tcesp-receitas-2023-2024-qa.yml`; execução [40238668013](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40238668013). Apenas diagnóstico, sem persistência nem publicação. A avaliação de seu resultado deve depender do status final e da leitura dos dois artifacts anuais.

## Resultado homologado do QA de receitas estaduais 2023–2024
A execução [40238668013](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40238668013) terminou com sucesso em ambos os jobs. Artifacts recuperados, abertos e `qa.json` lidos independentemente: 2023 ID **12615935979**, 2024 ID **12616355060**.

| Exercício | Linhas de receita | Municípios identificados | Municípios com registros em 12 meses | Problemas básicos | SHA-256 do ZIP oficial |
|---|---:|---:|---:|---|---|
| 2023 | 852.367 | 644 | 644 | Nenhum | `8a3e5b3db4aa8b47ffad2906f1cd2eb83bd6094dc83d855bc768bbf6ca475236` |
| 2024 | 872.652 | 644 | 643 | Nenhum valor, ano ou mês inválido | `583307edd4b3cbecac1eaf7b920891eb78678facf665bd9f154301a2a75d01cd` |
| 2025 | 896.299 | 644 | 644 | Nenhum | `16df083d2088127108957a028f6c824265813c74542f528108526b44a392b84b` |

**Ressalva de 2024:** Bernardino de Campos tem registros para os meses 1–5 e 7–12, **sem linha para junho** no arquivo estadual. Não imputar zero; investigar extrato municipal de 2024 e eventual alteração da versão publicada. Todos os 644 municípios continuam representados no arquivo anual. A capital São Paulo não está presente nos três conjuntos, coerente com a jurisdição do TCESP.

As contagens de linhas são observações do dataset; não equivalem a quantidade de municípios nem a cobertura por rubrica. QA até aqui compreende decodificação, períodos, presença de municípios e aritmética decimal; **não houve conciliação externa por rubrica DCA nem ingestão R2/SQLite**.

Próxima validação: comparar os arquivos anuais oficiais às extrações municipais existentes, identificar o caso Bernardino de Campos 2024, auditar detalhamento por natureza da receita, reconciliar valores compatíveis e decidir integração sob versionamento.

## Confronto direto de fontes — Bernardino de Campos 2024
- Run [40239257634](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40239257634); artifact `tcesp-bernardino-receitas-2024` ID `12615834668`. Relatório `auditoria.json` extraído do artefato e analisado; teste reprodutível em `governance/verificar_bernardino_receitas_2024.py`.
- O arquivo **estadual** `receitas-2024.zip` (SHA-256 `583307edd4b3cbecac1eaf7b920891eb78678facf665bd9f154301a2a75d01cd`) e o arquivo **municipal** `receitas-bernardino-de-campos-2024.zip` (SHA-256 `f722f327dffe0539fb07ec0c1acbd53dc03ed8a78fb6daf19d81370d3d5254cf`) apresentam **1.424 registros** de Bernardino de Campos cada, colunas idênticas, quantidades de registros por mês idênticas e somas mensais iguais em centavos.
- **Nenhuma das duas fontes possui linha com mes_referencia=6.** Há **247** linhas no mês 7, enquanto os outros meses têm entre 107 e 127. Não inferir que a arrecadação de junho foi transferida para julho sem rastreio de competência e documentos de origem. `divergencias_mensais=[]`; `invalid_values=0` nas duas origens.
- Consequência metodológica: a lacuna foi reproduzida na fonte municipal e **não deriva da agregação estadual**. Classificar junho de Bernardino de Campos 2024 como `sem_registro_na_fonte`; não preencher valor zero. A auditoria municipal/estadual demonstrou paridade de totais para este município, não universalidade da igualdade em outros municípios.
