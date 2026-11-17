# F03/F04 — compilação monetária de fontes já preservadas, sem reconciliação

**Data:** 17/11/2026. **Alteração de escopo por solicitação:** suspender temporariamente conciliações, estornos, classificação líquida e GND4 efetivamente pago; priorizar a recuperação dos **dados ainda não compilados** de Transferegov e Obrasgov para os 34 municípios da RMRP. Manter `public_release_authorized=false` e não alterar banco fiscal produtivo.

## Aquisição e disponibilidade

O banco real privado `RMRP_FED08B_EMPENHO_DESEMBOLSO_PRIVADO.sqlite`, recuperado do Drive e com QA de integridade na etapa anterior, já contém a tabela `contrato_cipi_fed04b` e a tabela `empenho_cipi_fed08b`. Foi executada uma **nova compilação** dessas tabelas, sem nova chamada aos endpoints oficiais.

**Limitação de novas consultas nesta rodada:** execução local não resolveu DNS externo das APIs oficiais de Transferegov e Obrasgov; a alternativa Browserless retornou **limite de unidades (HTTP 401)**. Assim, nenhuma extração inédita remota foi concluída. Não transformar essa limitação técnica em inexistência de registros da fonte.

## Campos e quantidades recuperados dos registros já preservados

| Conjunto | Linhas | Projetos distintos | Montante candidato | Estágio financeiro |
|---|---:|---:|---:|---|
| `contrato_cipi_fed04b` | 150 linhas de origem; **134 registros distintos** pela chave (projeto, ID contrato, número contrato, valor) | 131 | **R$ 201.335.149,95** | Valor global do contrato; não necessariamente pago |
| `empenho_cipi_fed08b` | 257 | 193 | **R$ 147.402.874,08** | Empenho; não pagamento |
| `obra_proponente` | 218 | 218 | Valor adicional não identificado no cadastro | Projeto pelo proponente, sem confirmação do local de execução |

Havia **16 linhas repetidas** de contratos pela chave descrita, sem chaves com montantes conflitantes. Todos os 150 valores literais de contrato foram interpretados em centavos; o valor agregado decorre **somente das 134 chaves distintas**. A contagem de 257 empenhos foi mantida tal como registrada na origem, sem hipótese de equivalência a pagamentos. **Montantes não aditivos entre si nem aos desembolsos ou gastos municipais.**

## Gestão de Parcerias — classificação recuperada

A tabela `parcerias_categoria_proposta` preserva **743 propostas**, sendo **94** de investimento proposto, **588** de custeio, **59** mistas e **2** indefinidas. Esta tabela **não contém montantes monetários**; não foram fabricados valores para essas propostas. Transferências Especiais, Parcerias financeiras e o universo monetário estadual do Obrasgov ainda exigem captura específica por API/snapshot, quando houver conectividade.

## Arquivos locais da execução

O pacote `RMRP_F03_F04_PRECOMPILADO_PRIVADO_2026-11-17.zip` foi criado com 5 CSVs e `qa.json`, incluindo:
- `obrasgov_cipi_contratos_brutos_rmrp.csv` — 150 linhas, identificadores, valor literal, centavos e marcação da primeira ocorrência lógica;
- `obrasgov_cipi_empenhos_rmrp.csv` — 257 registros com ID de projeto, município proponente, natureza, valor em centavos e data;
- `obrasgov_projetos_valores_candidatos_rmrp.csv` — 218 projetos e contagens/valores em estágios separados;
- `obrasgov_valores_por_municipio_proponente_rmrp.csv` — agregados por IBGE7, sem confundir contratos com empenhos;
- `transferegov_parcerias_cobertura_municipal_rmrp.csv` — número de propostas por classe;
- `qa.json` — contagens e observações de qualidade.

**SHA-256 do ZIP local:** `7cb9d4c1c438f07a4d37c3805993fa65a312c12f9a6fb3741e6cb4a4ff81fd97`. O pacote foi criado na sessão de trabalho e ainda **não foi persistido no Drive/R2**; arquivos brutos originais permanecem preservados no Drive privado, como anteriormente documentado.

## Próximas aquisições que realmente faltam

1. **Transferências Especiais — Transferegov:** recuperar beneficiários RMRP, planos de ação, valores, empenhos/ordens bancárias, origem e competência. Identificadores e estágios separados.
2. **Gestão de Parcerias:** complementar as 743 propostas com valores financeiros, quando endpoint de parceria/empenho/ordem disponibilizar identificador de vínculo.
3. **Obrasgov:** obter os campos monetários do módulo `projeto-investimento` para o universo SP e o recorte RMRP, com paginação/IDs, marcando a ausência de valores nulos. Os módulos `empenho`, `contrato` e `execucao-fisica` da nova API estavam globalmente vazios na verificação de 16/11; não interpretar como execução zero.
4. Usar runner GitHub Actions autorizado para aquisição incremental assim que houver workflow parametrizado, sem redownload de arquivos nacionais já preservados e com checkpoint, hash, readback e matriz `fonte+modalidade+municipio+ano`.

**Prioridade formal agora: ampliar aquisição e compilar valores identificáveis; não executar reconciliadores F01/F02 nem aprofundamento físico das obras até nova orientação.**