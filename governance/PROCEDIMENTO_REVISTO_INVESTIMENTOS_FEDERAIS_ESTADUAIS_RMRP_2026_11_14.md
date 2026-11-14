# Procedimento operacional revisado — aquisição e conciliação de investimentos públicos

**Versão:** 2026-11-14 / v1.0  
**Abrangência:** 34 municípios da RMRP, extensível a SP645.  
**Estado:** revisão de procedimento **antes da retomada da execução**. Este documento não constitui autorização para publicação, reprocessamento generalizado ou promoção de dados.  
**Base:** auditoria `governance/AUDITORIA_DOCUMENTAL_APIS_TRANSFEREGOV_OBRASGOV_SIAFEM_2026_11_14.md`; relatório `governance/RELATORIO_INV_RMRP_FED02_PAD_CONVENIOS_DESEMBOLSOS_2026_11_14.md`; relatórios FED03; logs de execução. Preservar integralmente os resultados e referências dos runs anteriores.

## 1. Objeto e indicadores não intercambiáveis

A finalidade é medir **investimento federal e estadual destinado e/ou realizado no território municipal**, e não transferências correntes gerais. O sistema deve oferecer fatos independentes para:
1. investimento **previsto/aprovado** em plano ou programa;
2. valor **pactuado** por instrumento;
3. **empenho** da origem;
4. **desembolso/ordem bancária federal** para o instrumento;
5. **recebimento** efetivamente comprovado por beneficiário, quando evidenciado;
6. **documento de liquidação** e sua situação;
7. **movimentação/pagamento do convenente** com tipo, data, sinal, retenções e possível estorno;
8. **item financiado classificado como GND4** por ligação documental, sem rateios presumidos;
9. **execução física da obra** e localização, segundo Obrasgov/outra fonte;
10. **despesa orçamentária municipal** conforme DCA/FINBRA/TCESP, que não equivale a 4, 7 ou 9.

**Não somar etapas da mesma cadeia**. Sem chave oficial entre pagamento e item de capital, a classe é `pagamento_sem_natureza_de_investimento_comprovada`. Ausência de registro é `nao_observado`, jamais zero pressuposto.

## 2. Inventário oficial e arquivo correto

Catálogo canônico em 14/11/2026: https://api-publica.transferegov.gestao.gov.br/downloads . Buscar nomes por descoberta do catálogo, não por suposição. A documentação antiga ainda aponta `repositorio.dados.gov.br`; não preferir links antigos sem verificar disponibilidade.

| Arquivo ZIP oficial | Uso e relação esperada | Estado da validação |
|---|---|---|
| `siconv_proposta` | `ID_PROPOSTA` e município proponente `COD_MUNIC_IBGE` | 6.410 propostas RMRP em snapshot anterior |
| `siconv_convenio` | `ID_PROPOSTA` ↔ `NR_CONVENIO` | 1.793 registros RMRP em snapshot anterior |
| `siconv_plano_aplicacao_detalhado` | `ID_PROPOSTA`, `ID_ITEM_PAD`, GND e situação | 28.456 itens RMRP; 7.917 GND4 aprovados em snapshot anterior |
| `siconv_desembolso` | `NR_CONVENIO`, `ID_DESEMBOLSO` | 2.537 eventos RMRP em snapshot anterior |
| `siconv_pagamento` | `NR_CONVENIO`, `NR_MOV_FIN`, `ID_DL`, `TP_MOV_FINANCEIRA` | 7.575.512 linhas nacionais, 28.503 vinculadas à RMRP; sem classificação monetária |
| **`siconv_obtv_convenente`** | **`NR_MOV_FIN`**, modalidade `TP_AQUISICAO` e valor `VL_PAGO_OBTV_CONV` | **3.113.841 linhas nacionais**, esquema validado run 43618166707 |
| `siconv_dl` | **`ID_DL`**, **`ID_PROPOSTA`**, status e valor da DL | **7.710.768 linhas nacionais**, esquema validado run 43618166707 |
| `siconv_empenho_desembolso` | **`ID_EMPENHO`**, **`ID_DESEMBOLSO`**, valor grupo | **393.062 linhas nacionais**, esquema validado run 43618166707 |
| `siconv_itens_dl` | Potencial ponte entre DL e item de plano | **PENDENTE: ler colunas reais**; não assumir `ID_ITEM_PAD` |
| `siconv_pagamento_tributo` | Retenções/tributos; verificar layout | Pendente |
| `siconv_ingresso_contrapartida` | Ingresso da contrapartida do convenente | Pendente |
| `siconv_coordenadas_obra`, `siconv_dados_obrasgov_geral` | Evidência de localização de obra e vínculo CIPI | Pendente |
| `siconv_contrato_cipi`, arquivos de medições | Possível ligação obra/contrato/medição | Pendente |

**Correção P0 concluída e validada:** `siconv_obtv.zip` NÃO é o nome do arquivo disponibilizado; o nome correto é `siconv_obtv_convenente.zip`. O 404 anterior era erro de descoberta. Não descrever OBTV como indisponível.

## 3. Ordem das ligações e testes de cardinalidade

1. Proposta → convênio: `ID_PROPOSTA` e `NR_CONVENIO`; controlar N:1 e N:M, rejeitar conflitos de identidade; normalizar chaves somente com regra documentada.
2. Convênio → desembolso: `NR_CONVENIO` → `ID_DESEMBOLSO`; estudar duplicidade, cancelamento e data do evento.
3. Convênio → pagamento: `NR_CONVENIO` com identificador de movimento `NR_MOV_FIN`; contabilizar **linhas de movimentação**, não 'pagamentos líquidos'.
4. Pagamento → OBTV do convenente: `NR_MOV_FIN` é **candidato a chave** em ambos os esquemas. Testar unicidade, cardinalidade, colisões entre convênios e tipo de aquisição antes de qualquer junção produtiva. Não duplicar valor pago, nem somar `VL_PAGO_OBTV_CONV` a `VL_PAGO` automaticamente.
5. Pagamento → DL: `ID_DL` corresponde a campo presente no CSV de DL. Testar chave e contexto de convênio/proposta, pois `ID_DL` isolado pode estar associado a versões. Não equiparar valor de DL com valor líquido ao fornecedor.
6. DL → seus itens: ler `siconv_itens_dl`, verificar colunas e relacionamento efetivo com `ID_ITEM_PAD`/plano antes de implementar. **Somente ligação explícita aprovada e validada** sustenta despesa de capital comprovada, e a documentação deve registrar se é execução programática, liquidação ou pagamento.
7. Empenho → desembolso: `ID_EMPENHO` + `ID_DESEMBOLSO`, conforme layout confirmado de `siconv_empenho_desembolso`; analisar o sentido de `VALOR_GRUPO` e relação N:M; não somar com desembolso novamente.

Em cada junção produzir: contagem fonte, chaves únicas, duplicatas, campos vazios, linhas correspondentes, não correspondentes, conflito, cardinalidade 1:1/1:N/N:M, fan-out, histórico de versões e exemplos documentados **sem dados pessoais**. Restringir join por contexto de origem sempre que houver possibilidade de colisão.

## 4. Aquisição segura, snapshots e repetibilidade

- Antes de coletar: consultar catálogo atual (URL, nome exato, data exibida, tamanho declarado); capturar também dicionário/versão quando disponíveis.
- Fazer uma única captura nacional por versão da fonte, com limites de rede e espaço; usar download temporário, retry/backoff **somente** para erros transitórios 429/5xx e jitter; jamais transformar 404 em zero de dados.
- Ao final: conferir cabeçalho, codificação, delimitador, esquema esperado, membros ZIP, CRC/descompressão, quantidade de linhas, SHA-256 do ZIP e arquivos de saída, data/hora da consulta e competência referenciada. Substituição de caracteres inválidos durante decodificação é **erro de qualidade registrado**, não reparo silencioso.
- Materializar em staging versionado imutável. Persistir em **R2 privado apenas mediante procedimento autorizado com credenciais/escopo adequados**, com chave de versão contendo fonte, extração e checksum; fazer readback de bytes/hash e inventário. Se não houver confirmação, estado `artifact_only_sem_snapshot_duravel`.
- Nenhuma atualização de SQLite canônico, D1 público, Pages, dados agregados ou publicação antes da homologação. Trabalhar em runner/SQLite de desenvolvimento separados.
- Evitar republicar valores ou microdados de `NOME_FORNECEDOR`, `IDENTIF_FORNECEDOR`, `DESC_DL` e dados bancários nos logs, CSV públicos, GitHub ou HTML. O fato de uma fonte ser pública não elimina a necessidade de minimização.
- Os resultados de períodos anteriores permanecem como snapshots separados; diferenças de linhas entre coletas não representam necessariamente falha, podem ser atualizações/retificações. QA de `6.410`, `1.793`, `7.917` etc. é **baseline de comparação**, não asserção permanente de igualdade.

## 5. Tipos de movimentação e cálculo monetário

Antes de qualquer soma de `VL_PAGO`:
- Inventariar o domínio real de `TP_MOV_FINANCEIRA` (códigos/descrições e ocorrência) e confrontar com o dicionário e tutorial oficial.
- Identificar sinal, unidade, formato decimal, estorno, devolução, cancelamento, transferências internas, tributos, retenções e pagamentos múltiplos por `NR_MOV_FIN`/`ID_DL`.
- Preservar valores nominais exatos em **inteiros de centavos**, não `float`, guardando moeda e período. Não inferir valor bruto = valor líquido; não atribuir pagamento a GND4 por coeficiente financeiro estimado.
- Conferir `DATA_PAG` e `DATA_EMISSAO_DL` e eventual data do desembolso, mantendo exercício fiscal distinto por etapa e tipo de evento.
- Construir indicadores por estágio e universo comparável. Somente pagamentos de investimento com classificação econômica e vínculo financeiro comprovados poderão alimentar métricas de aplicação financeira de capital.

## 6. Cobertura por fonte e territorialização

- Escopo inicial por **município proponente** em `COD_MUNIC_IBGE` RMRP34; cobertura de execução no território é uma dimensão **separada**, não inferida do proponente.
- Usar `SIGLA`/`MUNICIPIO` dos itens apenas como indicação nominal, com revalidação no cadastro IBGE e controle dos casos externos; não converter correspondência por nome em geocódigo homologado.
- O recorte anterior encontrou 7.891 itens GND4 aprovados com nome municipal da RMRP, 20 em outras localidades paulistas, seis em outras UFs, sete casos de proponente diferente do destino RMRP. Preservar a lista de exceções e não reclassificar automaticamente como erro.
- Obrasgov/CIPI e medições: tratar projeto, financiamento, execução territorial e despesa como fatos distintos, reconciliando por chave oficial sempre que possível. Projeto com municípios múltiplos precisa de fração comprovada ou marcação `plurimunicipal_sem_rateio`.
- Transferências Especiais, Gestão de Parcerias, Fundo a Fundo, TED, emendas e execução direta estadual: entradas independentes; controlar interseção de instrumento e programa para eliminar duplicidade documental.
- SIAFEM-SP: `Tipo=Investimento`, fonte classifica liberações estaduais, e não execução municipal; considerar valores negativos como cancelamento/estorno, universo de convênios com liberação desde agosto/2007; conferir atualização e reconciliação com os 238 município-ano já auditados.
- CGU/Portal da Transparência: usar arquivos de convênios e ordens bancárias para **conferência**, não como valor novo automaticamente aditivo.

## 7. Gates necessários para reiniciar a execução

| Gate | Critério de aceite | Estado no momento desta revisão |
|---|---|---|
| R0: contrato de fontes | Catálogo, URLs, nomes e esquemas reais verificados | **Parcial:** OBTV e 4 esquemas validados; `siconv_itens_dl` pendente |
| R1: integridade da ingestão | Hash, layout, linhas, CRC, versão e persistência durável com readback | **Não concluído** para persistência R2 |
| R2: vínculos administrativos | Controles de chave e fan-out nas cadeias proposta/convênio/DL/OBTV | **Parcial:** proposta/convênio/desembolso e pagamentos por convênio |
| R3: semântica financeira | Tipos, estornos, retenções, valores e datas auditados | **Não concluído** |
| R4: natureza de investimento | Item GND4 aprovado, DL/item e pagamento classificados por vínculo documental | **Não concluído** |
| R5: territorialização | município executor comprovado ou categoria de localização indeterminada | **Parcial** |
| R6: reconciliação externa | Consistência CGU, Obrasgov, SIAFEM sem dupla contagem | **Parcial** |
| R7: série analítica | exercícios comparáveis, metodologia de deflator e indicadores por estágio | **Pendente** |
| R8: promoção | aprovações e QA de produção, rollback, backups, idempotência | **Bloqueado até gates anteriores** |

## 8. Retomada após a revisão — sequência aprovada metodologicamente

**Primeira execução futura:** inspeção somente de `siconv_itens_dl` e definição técnica de chave entre `siconv_dl` e PAD; complementar domínio/estado dos campos de pagamento e OBTV **sem gerar totais de investimento**. **Segunda:** matriz de cardinalidade real e teste de não duplicação por `ID_DL`, `NR_MOV_FIN`, `NR_CONVENIO`; registrar conflitos. **Terceira:** classificar valores com precisão de centavos e estado de movimentação, por exercício e município **proponente**; manter localização de aplicação em coluna própria. **Quarta:** persistir um snapshot durável em R2 com readback e conciliar com fontes CGU/Obrasgov/SIAFEM; somente então expor indicadores na prévia isolada.

## 9. Referências oficiais verificadas na auditoria

- https://api-publica.transferegov.gestao.gov.br/
- https://api-publica.transferegov.gestao.gov.br/downloads
- https://www.gov.br/transferegov/pt-br/ferramentas-gestao/paineis-gerenciais/arquivos/modelo-dados-csvs-discricionarias-e-legais.zip/@@display-file/file
- https://www.gov.br/transferegov/pt-br/manuais/transferegov/discricionarias
- https://api-publica.obrasgov.gestao.gov.br/
- https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx
- https://portaldatransparencia.gov.br/download-de-dados/convenios

**Não comprovado nesta revisão:** consulta íntegra de `siconv_itens_dl`, significado efetivo de todos os códigos `TP_MOV_FINANCEIRA`, montantes líquidos de investimento pagos e persistência R2 com readback. Não informar esses elementos como concluídos.
