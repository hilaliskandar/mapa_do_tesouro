# INV-RMRP — Série anual exata SIAFEM de transferências estaduais de investimento, 2020–2026

**Versão da apuração:** 12/11/2026. **Fonte primária:** [Secretaria da Fazenda e Planejamento de São Paulo — Transferências Voluntárias / SIAFEM](https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx), com atualização declarada até 12/11/2026.

## Resumo executivo

A série anual de transferências estaduais de investimento para as prefeituras dos **34 municípios da Região Metropolitana de Ribeirão Preto** foi recuperada diretamente na fonte oficial **com precisão de centavos**, por meio de **238 consultas** (34 municípios × sete anos, 2020–2026).

**Resultado consolidado: R$ 305.521.029,20 de valores liberados/estornados e 1.017 pagamentos** no período. As 238 consultas foram completadas sem erro, e os valores por ano/município/convênio reconciliaram sem diferenças com a extração integral anterior dos 752 convênios e com os respectivos totais municipais oficiais.

O resultado **substitui, para qualquer uso analítico, os montantes anuais aproximados** obtidos inicialmente das páginas individuais de convênio. Os conjuntos de dados provisórios permanecem no repositório como histórico metodológico, mas não devem alimentar indicadores monetários publicados.

## Série anual exata e auditada

| Ano da liberação | Pagamentos | Valor liberado/estornado |
|---|---:|---:|
| 2020 | 205 | R$ 33.016.042,80 |
| 2021 | 113 | R$ 25.602.636,07 |
| 2022 | 234 | R$ 72.485.541,18 |
| 2023 | 174 | R$ 62.146.772,20 |
| 2024 | 150 | R$ 57.352.622,11 |
| 2025 | 90 | R$ 35.932.976,66 |
| 2026 (até 12/11) | 51 | R$ 18.984.438,18 |
| **Total** | **1.017** | **R$ 305.521.029,20** |

**Atenção:** 2026 é ano incompleto na data de coleta. As transferências constituem fluxos financeiros direcionados a investimento segundo a classificação SIAFEM, **não despesas de investimento comprovadamente executadas pelas prefeituras nem obras concluídas**.

## Método e parâmetros

1. Abrir formulário oficial PesquisaComposta.aspx e, para cada um dos 34 municípios da lista RMRP (IBGE7), selecionar `Municipio` pelo identificador local do SIAFEM; exceção nominal `Brodowski`, exibido no sistema como `BRODOSQUI`.
2. Selecionar radio `Beneficiado = Prefeituras` e `Tipo = Investimento`, mantendo região administrativa em branco, pois esta não é igual à RMRP.
3. Para cada ano de 2020 a 2025, preencher `LiberacaoInicio = 01/01/AAAA` e `LiberacaoFim = 31/12/AAAA`. Para 2026, `LiberacaoFim = 12/11/2026`.
4. Enviar formulário ASP.NET com estado de sessão pelo método POST; ler exclusivamente a grade `grdTransferencia`, totalizador `Valor Liberado/Estornado`, contagem `Quantidade de Pagamentos` e linhas com identificação oficial do convênio. Preservar os valores monetários em **centavos inteiros**, sem conversões por ponto flutuante na base final.
5. Para cada município/ano, validar: soma das linhas por convênio = total do sistema; soma da quantidade de pagamentos das linhas = totalizador do sistema; reconstituir total municipal 2020+ e comparar à primeira extração. Nenhuma divergência nas **238 combinações**; total regional **R$ 305.521.029,20**, diferença **zero centavo**; pagamento total **1.017**.
6. **Não somar a coluna Valor Convênio entre anos.** O mesmo instrumento pode aparecer em várias linhas anuais; o valor contratado não é um fluxo anual. O arquivo de 889 linhas contém apenas o valor liberado no ano correspondente como medida somável.

## Recuperação dos cinco convênios com HTTP 500

A página individual de detalhes `Convenio.aspx` falhou por HTTP 500 para cinco convênios, impedindo antes a identificação do ano. A nova consulta anual em `PesquisaComposta.aspx` retornou os lançamentos com **centavos**, inclusive desses cinco instrumentos:

| Município | Convênio | Ano | Pagamentos | Valor exato |
|---|---|---:|---:|---:|
| Altinópolis | 5128032684769\\19 | 2020 | 1 | R$ 198.346,48 |
| Batatais | 5128032447861\\19 | 2021 | 1 | R$ 334.000,00 |
| Batatais | 5128032447861\\19 | 2022 | 1 | R$ 51.000,00 |
| Cássia dos Coqueiros | 51010936677718 A | 2020 | 1 | R$ 55.002,67 |
| Guariba | 5128031465476\\19 | 2020 | 1 | R$ 104.650,06 |
| Guariba | 5128031465476\\19 | 2021 | 1 | R$ 240.500,07 |
| Monte Alto | 512803165957\\18C | 2020 | 1 | R$ 136.000,00 |

**Total das sete liberações dos cinco convênios: R$ 1.119.499,28.** O detalhamento linha a linha da página original ainda apresenta erro HTTP 500, mas já não impede a apuração anual exata por instrumento.

## Matriz de persistência e QA

**Capturas originais:** `governance/inv_rmrp_siafem_anuais_exatos/lote_01_2026_11_12.json` a `lote_05_2026_11_12.json` (238 consultas, 34 municípios e sete anos).

**Tabelas canônicas para a branch de desenvolvimento, sem promoção automática à produção:**

- `governance/INV_RMRP_SIAFEM_34_MUNICIPIOS_2020_2026_ANUAL_EXATO_2026_11_12.csv`: 238 combinações município × ano (com zeros explícitos, se retornados pela fonte).
- `governance/INV_RMRP_SIAFEM_889_CONVENIO_ANO_EXATO_2026_11_12.csv`: 889 relações convênio × ano, com valores monetários exatos e quantidades de pagamentos.
- `governance/INV_RMRP_SIAFEM_2020_2026_RESUMO_ANUAL_EXATO_2026_11_12.csv`: sete totais regionais anuais.
- `governance/INV_RMRP_SIAFEM_2020_2026_ANUAL_EXATO_QA_2026_11_12.json`: parâmetros de consulta, totais originais, reconciliação, exceções e rastreabilidade.

**Controles:** 238 combinações município-ano, 889 linhas convênio-ano, 752 convênios únicos no intervalo completo; 1.017 pagamentos (não confundir com número de linhas convênio-ano). A soma dos montantes anuais reproduziu exatamente a soma do filtro geral por município. O fluxo de valor/centavos foi separado da tabela de eventos com data, para evitar multiplicar o valor do instrumento nas consultas por evento.

## Históricos superados e restrições de inferência

A base de **1.010 lançamentos individuais** permanece útil para análise de datas e itens de despesa, mas a representação financeira sem centavos e a indisponibilidade de cinco detalhes a tornam inferior à nova série exata para qualquer agregação monetária. Em 12/11/2026, a coluna repetida de valor total do convênio foi retirada do CSV de 1.010 eventos para eliminar risco de dupla contagem.

Os arquivos `INV_RMRP_SIAFEM_MUNICIPIO_ANO_AGREGADO_PROVISORIO_2026_11_12.json` e `INV_RMRP_SIAFEM_ANO_EXATO_PARCIAL_2026_11_12.csv` foram **superados para uso monetário** pelas séries anuais exatas acima; preservados para documentação do processo de QA.

O recorte mede liberação/estorno **estadual** sob o tipo de despesa investimento. Não somar com o valor previsto do convênio, com o repasse federal que possa financiar a mesma política, com a despesa liquidada municipal ou com o custo de obras; fazer tratamento de fonte e consolidação intergovernamental antes de interpretar investimentos totais no território.

**Próximo gate:** incluir no SQLite real em cópia isolada, preservando contrato, ano, município, sinais, natureza e QA; validar contas da interface experimental; não alterar a produção. **PR #233 em draft**, sem merge ou modificação da base canônica, FED04/PR #232 preservados.
