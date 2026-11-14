# Retomada da investigação de investimentos federais — Transferegov, Obrasgov e conciliação

**Data:** 14/11/2026. **Branch:** `investimentos-territoriais-sp645-20261111`. **Escopo:** SP645 como universo de aquisição, RMRP34 como piloto de reconciliação. **Status:** coleta de layouts complementares efetivamente executada e confirmada; inspeção do arquivo nacional de itens DL independente em andamento. Nenhuma escrita em SQLite/D1 produtivo, R2, Pages ou publicação.

## Evidências reaproveitadas e pontos de partida

- RUN [43618166707](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43618166707) validou nacionalmente os esquemas `siconv_pagamento` (7.575.512), `siconv_obtv_convenente` (3.113.841), `siconv_dl` (7.710.768) e `siconv_empenho_desembolso` (393.062). Os números são **linhas nacionais**, não investimentos pagos.
- Para RMRP34 proponente, os trabalhos anteriores localizaram 6.410 propostas, 1.793 convênios, 28.456 itens PAD (7.917 GND4 aprovados) e 28.503 movimentos de pagamento relacionados a 1.286 convênios. A identidade do município de execução segue distinção independente da sede do proponente.
- Os **645 municípios IBGE7** e seus recortes 16 RA, 43 RG, 9 RM e 1 AU já estão preparados na dimensão `governance/DIM_SP645_IBGE_RA_RG_RM_AU_CONSOLIDADA_2026_11_14.csv`, com QA de fonte oficial. Essas classificações são alternativas, não aditivas.

## Novos arquivos oficiais realmente inspecionados

Catálogo oficial confirmado em https://api-publica.transferegov.gestao.gov.br/downloads (arquivos listados em 14/11/2026).

A rotina de auditoria `pipeline/acquire/inv_sp645_transferegov_new_source_layout.py` usa download temporário atômico, retry limitado para 429/5xx e problemas transitórios, SHA-256, um único membro CSV, conferência completa de CRC, cabeçalhos e amostra estrita (1000 linhas), sem imprimir microdados de convenentes ou fornecedores. O ZIP é removido do runner após a inspeção; o artefato de Actions **contém apenas metadados**. Não equivale a staging nacional persistido em R2.

**Workflow concluído com SUCCESS:** [43629864912](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43629864912).

| Arquivo | Cabeçalho oficial real verificado | Implicação |
|---|---|---|
| `siconv_pagamento_tributo` | `NR_CONVENIO`, `DATA_TRIBUTO`, `VL_PAG_TRIBUTOS` | É registro de tributos por convênio; **não** apresenta `NR_MOV_FIN` nem `ID_DL`. Não vincular ingenuamente a movimento individual |
| `siconv_ingresso_contrapartida` | `NR_CONVENIO`, `DT_INGRESSO_CONTRAPARTIDA`, `VL_INGRESSO_CONTRAPARTIDA` | Evento de ingresso de contrapartida. Não somar como pagamento de despesa GND4 |
| `siconv_coordenadas_obra` | `ID_PROPOSTA`, `NOME_PROJETO_CADASTRO_OBRA`, `LATITUDE_CADASTRO_OBRA`, `LONGITUDE_CADASTRO_OBRA` | Candidato a georreferência de obra no contexto de proposta, requer validação de coordenadas, cardinalidade e localização administrativa; não assumir que cada coordenada equivale a um projeto distinto |
| `siconv_contrato_cipi` | `ID_CONTRATO`, `NR_CONTRATO`, `ID_PROJETO_INVESTIMENTO` e outros 18 campos, incluindo situação, valor global e datas | Ponte documental potencial entre contrato e projeto Obrasgov; **valor global do contrato não equivale a pagamento federal** |
| `siconv_dados_obrasgov_geral` | `id_projeto_investimento`, `nr_instrumento`, `programa_governo`, `link_transparencia` | Ponte adicional entre número de instrumento e projeto Obrasgov, sujeita a cardinalidade e revisão de qualidade |

**Dados de estágio distintos**: tributos, ingressos de contrapartida, parcelas de transferências, documentos de liquidação, despesas do convenente e pagamentos do Tesouro não são automaticamente aditivos. Manter valores por evento e não produzir soma de investimentos enquanto estiverem sem prova de natureza econômica.

## Arquivo prioritário ainda em inspeção

`siconv_itens_dl.zip`, 523,1 MB declarados no catálogo, é a fonte candidata à ponte documental DL→itens do plano. Executado isoladamente no workflow [43629868488](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43629868488), com CRC integral e apenas cabeçalho/amostra como saída. **Não afirmar os nomes de colunas até esse job terminar e o manifesto confirmar.**

## Etapas seguintes

1. Conferir o esquema real e a integridade de `siconv_itens_dl` na execução acima. Verificar se existe `ID_DL` e identificador efetivo do item PAD; se não houver, analisar alternativa documental, nunca deduzir ligação por proximidade.
2. Fazer inventário de tipos `TP_MOV_FINANCEIRA` e sinais/situações com contagem por domínio, sem imprimir microdados. Reconciliar `siconv_pagamento` × OBTV e DL, com testes de cardinalidade/fan-out.
3. Testar ligações `ID_PROPOSTA`→coordenadas, `ID_CONTRATO`→CIPI e `NR_CONVENIO`/número de instrumento→projeto Obrasgov, registrando duplicatas, inconsistências e municípios que não são proponentes.
4. Reaproveitar fontes externas: API Obrasgov para localização física, CGU convênios/ordens bancárias para controles, SIAFEM-SP para liberações estaduais, e Transferegov Especiais/Parcerias como modalidades distintas.
5. Capturar e manter **uma versão nacional única por fonte** em staging privado imutável, checksum, CRC e readback; derivar SP645 e RMRP34 desse mesmo conjunto.
6. Agregar apenas valores financeiros de mesmo estágio e natureza homologada e preservar dados indeterminados como ausência, não zero.

## Critérios de governança

- No fluxo SP645, municípios são atribuídos por código IBGE de proponente/beneficiário/local da obra **com papel registrado**; RA/RG/RM/AU decorrem exclusivamente desse código.
- Não presumir geolocalização física de investimento a partir de sede do fornecedor.
- Não produzir total de investimento executado usando GND4 aprovado do PAD como substituto de pagamento.
- Os workflows são isolados, conservam apenas relatórios sem nomes, CNPJ ou linhas de pagamento, e não promovem a base canônica.


## Fechamento da inspeção do `siconv_itens_dl`

**Run [43629868488](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43629868488): SUCCESS**, com CRC do ZIP nacional verificado e inspeção estrita de cabeçalho/amostra; manifesto de metadados arquivado. Cabeçalho real:

`ID_ITEM_DL;NOME_ITEM_DL;QTD_ITEM_DL;UNIDADE_ITEM_DL;VALOR_TOTAL_ITEM_DL;DESCRICAO_ITEM_DL;ID_DL`.

**Conclusão documental P0:** a chave `ID_DL` existe no item e na tabela de DL; **`ID_ITEM_PAD` não consta do CSV `siconv_itens_dl`**. A cadeia `pagamento → DL → item da DL` tem chave candidata, mas a cadeia `item da DL → item PAD GND4` **NÃO tem chave direta documentada neste esquema**. A presença do nome/descrição não autoriza equiparar os itens por correspondência textual ou valor idêntico. Os valores `VALOR_TOTAL_ITEM_DL` não são ainda comprovadamente pagamentos líquidos; retenções/tributos e status da DL precisam ser auditados.

A análise dos arquivos pequenos também demonstra que `siconv_pagamento_tributo` e `siconv_ingresso_contrapartida` têm `NR_CONVENIO`, **não têm `NR_MOV_FIN` ou `ID_DL`**, impossibilitando atribuição direta a movimento individual pela chave disponível. `siconv_coordenadas_obra` oferece `ID_PROPOSTA`; `siconv_contrato_cipi` oferece `ID_CONTRATO` e `ID_PROJETO_INVESTIMENTO`, e `siconv_dados_obrasgov_geral` usa `id_projeto_investimento` e `nr_instrumento`, aptos a testes de cardinalidade posteriores.

**Situação de contagens:** esta coleta foi schema+amostra de 1.000 registros por arquivo + CRC integral. A contagem total de linhas nacionais desses novos arquivos **não foi calculada**, e não deve ser inferida de seu tamanho.


## Auditoria de cardinalidade nacional Obrasgov/CIPI — executada

[Workflow 43630077789](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43630077789), `SUCCESS`; relatório agregador de chaves no artefato `inv-sp645-obrasgov-cipi-cardinality` ID `14127537342`. Código `pipeline/qa/audit_inv_sp645_obrasgov_cipi_join.py`. Foram baixados e verificados com CRC três arquivos nacionais, contados os vínculos sem imprimir identificadores ou nomes. Valores **não** foram somados.

| Controle da fonte | Resultado |
|---|---:|
| `siconv_dados_obrasgov_geral`, linhas / projetos únicos | 48.086 / 48.086 |
| Projetos repetidos na tabela geral | 0 |
| Números de instrumento distintos na tabela geral | 48.086 |
| `siconv_contrato_cipi`, linhas | 39.099 |
| Projetos distintos nessa tabela de contratos | 27.458 |
| Contratos com ID de projeto ausente | 0 |
| Linhas de contratos com ID de projeto encontrado na tabela geral | **39.099** |
| Projetos com múltiplos registros de contratos | **3.715** |
| Cardinalidade resultante de join pela chave de projeto, em linhas | 39.099 (sem fan-out adicional, pois tabela geral tem projeto único) |
| `siconv_coordenadas_obra`, linhas | 132.102 |
| Propostas distintas com coordenadas | 61.819 |
| Propostas com duas ou mais linhas de coordenadas | **10.343** |
| Linhas sem `ID_PROPOSTA` | 0 |

**Cuidado:** a tabela geral nacional `siconv_dados_obrasgov_geral` é apenas o conjunto correspondente disponível no Transferegov. Não afirmar que cobre todos os projetos do portal Obrasgov ou todas as obras federais. Contrato CIPI→projeto é uma relação N:1; projeto→coordenadas não foi unido no presente teste porque a tabela de coordenadas se relaciona pela `ID_PROPOSTA`, não pela chave CIPI. Um convênio ou proposta pode ter várias localizações.

**Próxima operação:** vincular os IDs documentais dos instrumentos e das propostas a proponentes paulistas por IBGE7, segregar valores de contrato de pagamentos, conferir geolocalizações e coordenadas externas. Este QA demonstra viabilidade de junção, não o volume de investimento executado.


## Domínio nacional de movimentações financeiras — execução completa

[Run 43630172358](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43630172358) concluído com `SUCCESS`. Arquivo nacional `siconv_pagamento.zip` adquirido sob código `pipeline/acquire/inv_sp645_payment_type_domain.py` em runner temporário, ZIP CRC verificado, leitor integral de linhas e metadados de contagem sem beneficiários, sem valores individuais e sem totais monetários.

- **7.575.512 linhas nacionais examinadas**, conciliando o total anteriormente observado no FED03.
- `TP_MOV_FINANCEIRA`: **`PAGAMENTO A FAVORECIDO COM OBTV` 5.734.760** e **`PAGAMENTO A FAVORECIDO` 1.840.752**, sem outros códigos/denominações na extração.
- `VL_PAGO` — mera classificação léxica do sinal/zero: **7.549.033 não negativos diferentes de zero; 26.451 zeros textuais; 28 negativos textuais**. **Não é valor de pagamento líquido**, nem classifica estorno: exige verificação documental e situação financeira. O algoritmo de sinais não substitui conversão de moeda com Decimal e precisão de centavos.
- Nenhum vazio nas colunas `NR_MOV_FIN`, `NR_CONVENIO`, `TP_MOV_FINANCEIRA`, `VL_PAGO`, `DATA_PAG` e `ID_DL` neste arquivo nacional, segundo o inventário de valores textuais vazios.
- **Limite:** este resultado não verifica unicidade global de `NR_MOV_FIN`, cardinalidade com OBTV, ocorrência de cancelamentos fora da série de pagamento, nem execução de capital. Não produzir soma de dinheiro sem classificação e prova documental.
