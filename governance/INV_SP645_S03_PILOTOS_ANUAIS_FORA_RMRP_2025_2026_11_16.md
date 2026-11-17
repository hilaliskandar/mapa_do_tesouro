# S03 — primeiros lotes sistemáticos SIAFEM 2025 fora da RMRP

**Execução:** 16/11/2026. **Recorte:** transferências voluntárias do Estado de SP, prefeituras, natureza Investimento, exercício da liberação 2025. **Fonte oficial:** https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx, com contrato HTML/Crawl2AI já documentado. **Publicação:** proibida até QA financeiro; `public_release_authorized=false`.

## 1. Metodologia operacional

A partir do cadastro **645/645 IBGE7→SIAFEM** [crosswalk](controls/investimentos_sp645/crosswalk_ibge_siafem_2026_11_16.csv), a rotina [`collect_sp_siafem_annual_batch.py`](../pipeline/coleta/collect_sp_siafem_annual_batch.py) ordena os **611 municípios externos à RMRP**, seleciona fatia determinística por `offset` e `limit`, abre sessão ASP.NET, obtém estados dinâmicos, envia formulário POST com `Beneficiado=Prefeituras`, `Tipo=Investimento`, `LiberacaoInicio=01/01/2025` e `LiberacaoFim=31/12/2025`. O extrator converte valores com `Decimal` em **centavos inteiros**, preserva estornos negativos, ignora linha totalizadora para somar e confere totais oficiais de valor liberado/estornado e quantidade de pagamentos antes de registrar a consulta como validada.

Os registros brutos, inclusive identificadores de convênio e CNPJ do convenente, ficam **exclusivamente no R2 privado**; apenas indicadores de cobertura/QA, sem documentos individuais, ficam nos logs/controles públicos. A fonte anual registra **linhas convênio-ano**, não eventos de pagamento individual; o dado não deve ser somado à base regional de 12/11 nem a despesas municipais.

## 2. Execuções e leitura de retorno

| Execução | Offset | Municípios consultados | Resultado | Convênios-ano | Pagamentos | Valor líquido | Armazenamento |
|---|---:|---:|---|---:|---:|---:|---|
| [43921580825](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43921580825) | 0 | 5 | 5/5 com totalizador conciliado | 14 | 15 | R$ 6.835.173,32 | R2 privado validado |
| [43921923273](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43921923273) | 0, repetido | 5 | **Retrabalho de amostra**, sem novos municípios; corrigido | 14 | 15 | **não somar** | R2 privado separado e identificado como duplicata lógica |
| [43922061944](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43922061944) | 5 | 5 | 4/5 com totalizador; uma consulta sem informação suficiente para afirmar zero | 11 | 12 | R$ 2.260.768,14 | R2 privado validado |

**Resultado consolidado de consultas únicas satisfatórias:** **9 municípios adicionais** fora da RMRP, **25 registros convênio-ano**, **27 pagamentos contabilizados**, **R$ 9.095.941,46** em liberação líquida/estorno 2025, distribuídos entre **dois lotes distintos**. Uma décima consulta foi efetuada, mas permanece **sem resultado homologável como zero**. Não somar a execução duplicada de offset 0.

### Municípios em consulta única satisfatória

| Município | IBGE7 | Convênio-ano | Pagamentos | Valor líquido |
|---|---|---:|---:|---:|
| Adamantina | 3500105 | 4 | 5 | R$ 2.533.955,64 |
| Adolfo | 3500204 | 1 | 1 | R$ 285.540,81 |
| Aguaí | 3500303 | 3 | 3 | R$ 2.291.180,25 |
| Águas da Prata | 3500402 | 2 | 2 | R$ 490.000,00 |
| Águas de Lindóia | 3500501 | 4 | 4 | R$ 1.234.496,62 |
| Águas de Santa Bárbara | 3500550 | 1 | 1 | R$ 99.785,22 |
| Águas de São Pedro | 3500600 | 4 | 4 | R$ 936.891,77 |
| Agudos | 3500709 | 4 | 4 | R$ 853.524,39 |
| Alfredo Marcondes | 3500808 | 2 | 3 | R$ 370.566,76 |

**Pendente: Alambari (IBGE7 3500758).** A consulta de 2025 não apresentou linha financeira nem totalizador confirmando ausência. O estado é **consulta não conclusiva**, não `sucesso_sem_registro` e não zero. Verificar mensagem explícita do portal antes de qualquer classificação de ausência.

**Importante:** os valores deste quadro foram calculados do retorno oficial e reconciliados no nível do totalizador, mas continuam em fase de **QA de cobertura e integração**, não homologação para publicação.

## 3. Objetos preservados em R2

Bucket `financas-municipais-sp-canonico`:

- Lote offset 0: `sp_645/estadual/siafem/batches/2025/piloto_extra_rmrp_05/d5297a510939d83e8f2972b5c31e19e89dd8944ab8335c4d57b15f273374f4f8/`, arquivos `raw.json` e `qa.json`.
- Lote offset 5: `sp_645/estadual/siafem/batches/2025/piloto_extra_rmrp_offset_5_len5/794cfb0e0ad35cbe06912af5f36cd1725761439279593c57fba5d3576739cbdd/`, arquivos `raw.json` e `qa.json`.
- Reexecução indevida de offset 0: `sp_645/estadual/siafem/batches/2025/piloto_extra_rmrp_offset_0_len5/bb2edbfd233098336e78ce4f7c1e23ad7924f499a0abd85653183929eb80ae87/`; **não computar como nova cobertura**.

Todos os uploads e readbacks de hashes foram concluídos. Os novos estados foram registrados em `governance/controls/investimentos_sp645/{execucoes,snapshots,cobertura,pendencias}.csv`.

## 4. Decisões e sequência

1. Corrigir a falha de offset do workflow foi necessário para impedir repetição do primeiro lote; `BATCH_OFFSET` e `BATCH_YEAR` são agora aplicados ao comando, e o manifesto registra códigos IBGE7 consultados.
2. A série anual exata **RMRP34 de 12/11** permanece a fonte de referência para os 34 municípios, com 238 consultas e valor já reconciliado. Não reconsultar 2020–2025 sem razão; atualizar 2026 incrementalmente.
3. Para municípios **fora da RMRP**, estão registrados **9/611 com resposta estruturada para 2025**, **1/611 pendente de ausência/erro**, **601/611 ainda não consultados nesse recorte**. O cadastro territorial 645/645, por si, não representa cobertura financeira 645/645.
4. Prosseguir em lotes delimitados, com checkpoint e controle de revisitas, e separar consultas `sucesso_com_registros`, `sucesso_sem_registro` e `erro/indeterminado`. Não considerar resultados positivos em outros anos como cobertura de 2025.
5. A ampliação aos 645 municípios e aos exercícios anteriores depende de plano escalável de cotas, reintentos, logs, reconciliação e política de retificação. Não há promoção à base canônica de produção nem publicação no site neste ciclo.

**Resultado verificável:** dois lotes distintos + uma reexecução duplicada identificada, snapshots privados confirmados, documentação e controle de cobertura atualizados.
