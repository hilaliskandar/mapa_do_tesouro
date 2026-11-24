# F00 — auditoria de existência e persistência do acervo federal RMRP34

**Data:** 17/11/2026. **Escopo:** Transferegov e Obrasgov **somente financeiro**, sem dossiês físicos, contratos individuais, geometrias ou geocodificação. **Estado:** auditoria de inventário documental e metadados Drive, não recálculo de valores nem nova homologação. `public_release_authorized=false`.

## Descoberta principal

**O conjunto de sete ZIPs nacionais que alimentam FED03C/FED04B já havia sido adquirido e preservado integralmente** em 15/11/2026, incluindo `siconv_itens_dl.zip` de **548.549.412 bytes**, cujo upload e readback SHA-256 foram confirmados em adendo final da [auditoria FED03C](INV_RMRP_FED03C_PAGAMENTOS_REAIS_QA_2026_11_15.md). Relatos intermediários de que o quarto ZIP aguardava upload, reproduzidos em planos de 14–15/11, são **históricos superados** e não devem gerar nova coleta. Os nomes, tamanhos e estado privado dos sete ZIPs e de dois pacotes SQLite/QA regionais foram **reconfirmados nesta sessão em consultas ao metadado Google Drive**; conferência SHA dos bytes nesta sessão **não foi reexecutada** (valores dos hashes são os já demonstrados por download integral e readback nos relatórios de 15–16/11).

Inventário verificável, com `drive_file_id`, tamanho, SHA histórico, recorte reportado e proveniência, guardado em [`F00_RMRP_FEDERAL_PACOTES_VERIFICADOS_2026_11_17.csv`](controls/investimentos_sp645/F00_RMRP_FEDERAL_PACOTES_VERIFICADOS_2026_11_17.csv).

## Componentes financeiros reais já existentes

| Fonte | Evidência | Estado do encerramento |
|---|---|---|
| Transferegov, pagamentos | **28.503** movimentos distintos, em **1.286** convênios; transações 2009–2026, **R$ 627.287.678,10** na soma *nominal bruta* | Microdados reais em SQLite privado. Esse valor **não é** pagamento líquido nem gasto final de investimento |
| Transferegov, documentos | **28.256** DL; **39.498** itens DL; **395** filhos do módulo específico OBTV | Recorte conservado, QA de FK e cardinalidade concluído, mas natureza de capital do pagamento e estornos ainda não homologados |
| Transferegov, desembolsos | **2.537** eventos; **2.535** com grupos de empenho exatamente reconciliados; uma diferença de R$ 88.000,00 e um evento sem ponte | Conciliação parcial suficiente para **valor de desembolso reconciliado**, não para classificar como gasto de investimento efetivo |
| Transferegov, classificação de empenho | Nos grupos reconciliados: natureza `44` = R$ 450.501.858,85; `33` = R$ 263.567.534,82; `34` = R$ 250.000,00 | **Categoria de desembolso vinculada ao empenho**, não categoria de pagamento final GND4; não somar ao desembolso pai |
| Obrasgov | **218** projetos candidatos vinculados ao proponente da RMRP; 150 registros de contrato CIPI, 257 empenhos CIPI ligados a 193 projetos em análise posterior | Fonte de vínculo e identificação; contratos/execução/empenhos na *nova API Obrasgov* retornaram total global zero em 16/11; nenhum valor de execução pode ser imputado como zero. Nenhum montante adicional aditivo homologado |
| Dimensão territorial RMRP | **34/34** municípios distribuídos por quatro sub-regiões; recorte de projetos por proponente não equivale a localização territorial da intervenção | Dimensões municipais disponíveis para tabela anual privada, com advertência semântica |

O recorte financeiro real de pagamentos já passou por `NR_MOV_FIN` único, zero filhos OBTV órfãos, zero itens DL órfãos e `integrity_check=ok` em [FED03C](INV_RMRP_FED03C_PAGAMENTOS_REAIS_QA_2026_11_15.md). Na [FED03D](INV_RMRP_FED03D_FED04C_AUDITORIA_REAL_2026_11_15.md), 22.318 pagamentos foram rotulados `COM OBTV` e 6.185 `PAGAMENTO A FAVORECIDO`; somente 395 linhas no módulo específico OBTV foram associadas. Há 33 pagamentos de valor zero e 34 pagamentos com DL não `Ativo` (28 `Inativo`, seis `Em Elaboração`), sem que sejam presumidos inválidos.

## Matriz de impedimentos por campo

| Indicador pretendido | Estado | Próxima verificação |
|---|---|---|
| Quantidade de propostas, convênios e desembolsos vinculados a proponentes da RMRP | Candidato auditado | Conferir competências e retificações antes da integração |
| Desembolso por convênio/ano de transferência federal | Parcial com fonte/ID real | Manter dois registros excepcionais isolados e sem ajuste presumido |
| Valor de pagamento nominal bruto a favorecidos | **R$ 627.287.678,10**, resultado histórico exploratório | Recortar por município e ano, auditando semântica do evento e exclusões |
| Valor líquido pago a favorecidos | **Não homologado** | Identificar devoluções, estornos, retenções, pagamentos de tributos e documentos em cada cadeia |
| Valor pago de investimento GND4 | **`null` nos 34 municípios** | Associar `ID_DL` a itens PAD/natureza por chave oficial, sem rateio por hipótese |
| Valor financeiro Obrasgov adicional ao Transferegov | **Não homologado** | Inventariar campo de valor de cadastro/projeto, ID CIPI e sobreposição; não tratar fonte como parcela financeira adicional |
| Total de investimentos públicos efetivamente executados na RMRP | **Indisponível como soma consolidada** | Separar despesas municipais executadas de repasses federais/estaduais e execução direta, sem dupla contagem |

## Próximas ações executáveis, na ordem

1. **F01 (principal):** abrir o SQLite privado `RMRP_FED08B_EMPENHO_DESEMBOLSO_PRIVADO_2026-11-16.zip` e usar `desembolso_fluxo` como tabela-pai de valores em centavos. Produzir relatório **por IBGE7, ano do evento e modalidade** para os 2.535 desembolsos reconciliados, isolando os dois eventos excepcionais. Confrontar as colunas existentes, sem inferir recorte territorial pelo local de obra.
2. **F02:** usar a cópia privada `RMRP_FED03C_FED04B_REAL_STAGING_2026-11-15.zip` para perfil dos 28.503 movimentos, os 33 zerados e os 34 vinculados a DL não ativo. A tabela de pagamentos, e não cada item DL/OBTV, é o fato-pai; calcular valor líquido **somente** quando estornos/devoluções estiverem documentalmente disponíveis.
3. **F03:** classificar lacunas reais de Parcerias/Especiais/Tesouro/CGU, separando ausência de arquivo de falta de conciliação, sem redownload dos ZIPs já conferidos.
4. **F04:** extrair apenas valores de projeto na base de 218 candidatos e seus vínculos com Transferegov, incluindo status de disponibilidade, mas não somá-los aos repasses sem desduplicação por ID e estágio.
5. **F05:** cruzar FINBRA/TCESP municipal e SIAFEM estadual já prontos com os fatos financeiros federais por **34 municípios × exercícios observados**, produzindo `financiamento` e `execução` como painéis distintos em prévia privada.

## Gates de controle

- Proibição de somar repasses da União/Estado à despesa municipal que pode ter sido financiada com o mesmo recurso; fato de financiamento é separado de despesa liquidada/realizada.
- Valor de investimento GND4 **efetivamente pago** permanece `null` até prova de chave documental; não usar `44` de empenho como substituto.
- Não exigir localização física, contratos individuais ou medição de obra para fechar a tabela **financeira**.
- Não atribuir `0` à indisponibilidade de módulos da API Obrasgov.
- Preservar versões, datas de extração, prova SHA histórica e estado de acesso privado; sem escrita na base fiscal produtiva ou publicação no site.

**Conclusão F00:** não há pendência conhecida de aquisição dos **sete ZIPs nacionais** já auditados em 15/11; o bloqueio principal é **semântico e contábil**, nos estágios de pagamento/estorno e na identificação da natureza e não sobreposição. A cobertura integral de modalidades federais fora desse conjunto ainda não foi demonstrada.
