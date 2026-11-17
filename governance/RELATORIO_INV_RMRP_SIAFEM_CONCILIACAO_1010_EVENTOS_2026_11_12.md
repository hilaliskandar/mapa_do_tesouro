# INV-RMRP — Auditoria dos eventos individualizados SIAFEM: 752 convênios, 1.010 lançamentos de investimento

**Data:** 12/11/2026. **Escopo:** 34 municípios da RMRP; transferências voluntárias estaduais a prefeituras, tipo Investimento, liberação desde 01/01/2020. **Fonte:** https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx (atualização declarada de 12/11/2026).

## 1. Universo validado — fonte agregada

A consulta principal identificou **752 convênios** e **R$ 305.521.029,20 de valor liberado/estornado**, com **R$ 362.933.954,59 de valor dos convênios**. Os 34 totais municipais reproduziram exatamente as somas das respectivas linhas. Registros persistidos em governanca dos lotes SIAFEM 01 e 02 e seus manifestos; ver também RELATORIO_INV_RMRP_SIAFEM_752_CONVENIOS_305M_2026_11_12.md.

Os valores de convênio contratado, recurso transferido, despesa municipal executada e produto físico não são aditivos.

## 2. Consulta das páginas individuais

Foram consultadas as páginas oficiais Convenio.aspx?Convenio=IDENTIFICADOR dos **752 convênios**, em nove lotes de aquisição, cada um preservado em governance/inv_rmrp_siafem_eventos/parte_01...parte_09_2026_11_12.json.

- **747 convênios** com detalhes integralmente acessíveis; **5 páginas HTTP 500**.
- Os detalhes acessíveis contêm **1.119 linhas financeiras**. Delas, **103** são anteriores a 2020 e **6** são de natureza CUSTEIO (embora o convênio também tenha investimentos).
- Restam **1.010 eventos datados de 2020 a 2026**, natureza INVESTIMENTO, cuja contagem por instrumento coincide **exatamente** com o indicador Quantidade de Pagamentos da consulta resumida, para os 747 convênios acessíveis. **Zero divergências de quantidade** após aplicação dos filtros temporais e de natureza aos eventos.
- Os seis eventos de custeio indevidamente misturados, que totalizam R$ 200.512 na forma de apresentação sem centavos, foram excluídos. Os casos ocorreram em Monte Alto, Santa Rita do Passa Quatro, Santa Rosa de Viterbo, Serrana e Taiúva; um convênio de Santa Rosa possui dois eventos de investimento e um de custeio.

### Conciliação monetária

Os resumos com **747 convênios** acessíveis informam **R$ 304.401.529,92** em liberações/estornos com centavos. As linhas do detalhamento exibem **valores sem centavos para todos os 1.119 eventos**; a soma dos 1.010 eventos de investimento exibidos é de **R$ 304.401.527,00**, diferença de **R$ -2,92**. A discrepância é compatível com arredondamentos na apresentação e foi inferior à tolerância de meio real por evento para cada instrumento. A base de referência EXATA deve continuar sendo o resumo monetário, e a série anual derivada dos detalhes deve manter estado **PROVISÓRIO / SEM CENTAVOS**.

Nenhum valor anual em reais pode ser apresentado como exato a partir do detalhe; a quantidade de eventos por ano é verificável e o montante anual só pode ser estimado até obter a resolução integral da coluna numérica.

### Contagem por ano da liberação

| Ano | Lançamentos de investimento acessíveis |
|---|---:|
| 2020 | 201 |
| 2021 | 111 |
| 2022 | 233 |
| 2023 | 174 |
| 2024 | 150 |
| 2025 | 90 |
| 2026 | 51 |
| **Total recuperado** | **1.010** |

Esses totais **não representam 100% dos eventos dos 752 convênios**, porque cinco instrumentos permanecem sem detalhamento.

## 3. As cinco exceções

| Município | Convênio (literal da fonte) | Quantidade prevista | Valor líquido exato do resumo |
|---|---|---:|---:|
| Altinópolis | 5128032684769\\19 | 1 | R$ 198.346,48 |
| Batatais | 5128032447861\\19 | 2 | R$ 385.000,00 |
| Cássia dos Coqueiros | 51010936677718 A | 1 | R$ 55.002,67 |
| Guariba | 5128031465476\\19 | 2 | R$ 345.150,13 |
| Monte Alto | 512803165957\\18C | 1 | R$ 136.000,00 |
| **Total** | **5 instrumentos** | **7** | **R$ 1.119.499,28** |

As URLs individuais devolvem **HTTP 500**. Testaram-se as formas literais, substituição de barra invertida por barra normal, codificação explícita da barra e normalizações da separação antes do sufixo; nenhuma dessas alternativas retornou detalhes. O erro é de acesso ao detalhamento da aplicação, **não comprovação de inexistência de pagamentos**. Os cinco instrumentos mantêm seus valores com centavos nos totais municipais e regional exatos.

## 4. Novos artefatos de auditoria

- `governance/INV_RMRP_SIAFEM_1010_EVENTOS_DATADOS_INVESTIMENTO_2026_11_12.csv`: 1.010 eventos individualizados, com código IBGE, número de convênio, data, item de despesa, classificação e valor *como exibido*, sem atribuir precisão de centavos inexistente.
- `governance/INV_RMRP_SIAFEM_752_QA_DETALHE_FINANCEIRO_2026_11_12.json`: universo, universo acessível, discrepância monetária, contagens, exceções e situação QA.
- `governance/INV_RMRP_SIAFEM_MUNICIPIO_ANO_AGREGADO_PROVISORIO_2026_11_12.json`: agrupamento por município e ano com contagens de eventos e montantes **visuais aproximados, não homologados**; 211 combinações município–ano com eventos. **Não publicar valores anuais como receitas exatas nem substituir séries TCESP**.
- `governance/inv_rmrp_siafem_eventos/parte_01...parte_09_2026_11_12.json`: evidência fonte de todos os 752 convênios e resultados da consulta individual.

## 5. Encaminhamentos

1. Investigar os cinco HTTP 500 por uma rota oficial alternativa, documento SIAFEM ou solicitação ao órgão; preservar integralmente o nome literal do instrumento.
2. Procurar endpoint ou relatório que exporte eventos financeiros com centavos e datas, incluindo cancelamentos/estornos, e reconcilie por instrumento, ano, CNPJ e item de despesa.
3. Não imputar a repartição anual dos R$ 1.119.499,28 nem arredondar a diferença total como se fosse exatidão por ano.
4. Incluir os registros em **cópia real** do SQLite canônico, jamais na produção, com modelo distinto para instrumento, evento financeiro e despesa municipal executada.
5. Executar QA cruzado nas dimensões município, sub-região, ano, natureza e instrumento, antes de publicar visualização financeira nova.

**Controle:** PR nº 233 continua isolada, sem merge, sem alterações de base SQLite, R2 ou D1 produtiva, mantendo a PR nº 232 e FED04 independentes.
