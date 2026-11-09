# RMSJRP — G06-F3 | Auditoria de vínculos entre propostas, parcerias e empenhos federais
**Data da pesquisa:** 09/11/2026. **Estado:** descoberta do esquema e dois pilotos de vinculação concluídos; **execução financeira por pagamento federal, ingresso municipal e liquidação não comprovada**. Não representa avaliação de efeito da LC 200/2023.

## 1. Ponto de partida
O G06-F2 documentou **9.338 propostas** nos dois módulos Transferegov, distribuídas em 508 da Gestão de Parcerias e 8.830 da API Discricionárias e Legais, em 231 páginas e 74/74 consultas com QA aprovado. Essas quantidades não são número de convênios distintos e não comprovam pagamento.

A presente diligência investiga se as **chaves oficiais** da API permitem progredir do objeto `proposta` ao objeto `parceria` e ao `empenho-parceria`, sem juntar documentos por valor ou semelhança textual.

## 2. Esquemas de dados oficiais examinados
Fonte: https://api-publica.transferegov.gestao.gov.br/ . Em [GitHub Actions 42636780122](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42636780122), resultado `success`, foram recuperados os OpenAPI de:
- **Gestão de Parcerias**, 18 rotas, SHA OpenAPI `b91d29099b6d17e36e88cb13067373ba763b8ec704aaa6e5a97a6b37901119a2`;
- **Discricionárias e Legais**, 13 rotas, SHA `269f37a85ae00c45823b596e2acd179c251a5d1b3e3730391fab233b59054106`;
- **Transferências Especiais**, 24 rotas, SHA `211f0d32a7f1c03a6da1d3bd05b7569670f2f29edb89d7938f3476f42b249595`;
- **Fundo a Fundo**, 21 rotas, SHA `a1205c6af06b0b155d2f83a4efa08ff01938f7ab115c6ed72e11c272f911af5a`.

Foram selecionadas **30 rotas de interesse**, das quais **13 candidatas financeiras**, pela descrição e parâmetros. **Uma rota existente não significa que sua execução financeira esteja populada ou completa**.

A rota `/parcerias/parceria` aceita `id_proposta`, devolve `id_parceria` e campos de situação, assinatura (`dh_assinatura`), publicação e URL do documento; `/parcerias/empenho-parceria` aceita `id_parceria`, devolve identificador, situação e valor de **empenho**, quando houver. **A rota `/parcerias/ordem-pagamento` não disponibiliza filtro direto por `id_parceria`**. Sem identificador comprovado de junção, não foram somadas ordens de pagamento a essas parcerias.

## 3. Primeiro piloto com cinco propostas identificadas
Fonte: `editorial/rmsjrp/pilotar_celebracao_empenho_g06f3.py`; [run 42637134609](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42637134609), `success`, QA `pass`.

| Município | Proposta | Parceria na API | Empenho na API |
|---|---:|---:|---|
| São José do Rio Preto | 75094 | 74879 | Há registro |
| Olímpia | 13999 | 13973 | Não localizado neste filtro |
| Olímpia | 14002 | 13976 | Não localizado neste filtro |
| Mirassol | 76321 | 76106 | Há registro |
| José Bonifácio | 92185 | 91870 | Não localizado neste filtro |

**Resultado:** 5/5 propostas com identificação municipal e chave válida, 5/5 com registro de parceria correlato, dois registros de empenho associados por `id_parceria`. **Nenhum dos cinco retornou data de assinatura no campo `dh_assinatura`**; assim, não se afirma que tenham sido juridicamente celebrados. A ausência de empenho retornado não prova inexistência de empenho em outros sistemas, tempos ou situações. A documentação não valida transferência paga.

Três produtos armazenados no R2 privado `rmsjrp/g06/2026_11_09/instrumentos_api_f3/` com readback SHA-256:
- `G06F3_CADEIA_PILOTO.csv` SHA `934d895049a1061ad566e79911e127f8893704da6621a2450d0a2fff9260201f`;
- `G06F3_EMPENHOS_PILOTO.csv` SHA `75e2ab3a6b51983e049a46e187b5e65deec3aeeda23a5c310230908e0a66cd49`;
- `QA_G06F3_PILOTO.json` preservado e conferido.

## 4. Segundo piloto controlado: um registro de Parcerias por município
Foi utilizada **somente** a parte Parcerias do `G06F2_PROPOSTAS_CANONICAS.csv` (508 linhas, com SHA `c6234fc4f72575bc639c99388f0db43afac7a93cc09dc663b34828293af890a7`); para cada um dos 37 municípios selecionou-se uma proposta, priorizando `Aprovada` e, entre aprovadas, o ano mais antigo e ID numérico menor.

**Esta é uma amostra intencional para testar a infraestrutura, NÃO uma amostra aleatória ou estimador estatístico da taxa de celebração de convênios.** Rotina `editorial/rmsjrp/amostrar_37_parcerias_g06f3.py`; [run 42637564508](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42637564508), resultado `success`, QA `pass`.

| Controle | Resultado |
|---|---:|
| Municípios com proposta selecionada e consulta completada | **37/37** |
| Registros de parceria associados ao ID da proposta | **37** |
| Registros com preenchimento de metadado de assinatura | **1** |
| Registros com metadado de publicação | **0** |
| Registros de empenho associados ao ID de parceria | **7** |
| Consultas de parceria com falha de acesso | **0** |

O registro com metadado de assinatura foi associado ao código municipal **3549805, São José do Rio Preto**, proposta **398**. **Uma data no campo de assinatura da API não substitui a leitura do termo contratual assinado**. Os sete registros de empenho são contabilizados como **registros de compromisso orçamentário**, não como comprovantes de pagamento, ordem bancária, receita municipal creditada ou despesa local liquidada.

A primeira execução da amostra, [42637462645](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42637462645), falhou por incompatibilidade nominal da chave do manifesto G06-F2 (`file` em vez de `name`). O erro foi identificado, corrigido no código e **a execução seguinte [42637564508](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42637564508) terminou com sucesso**. Não apagar o registro da falha, importante para reprodutibilidade.

Persistência no R2 privado `rmsjrp/g06/2026_11_09/instrumentos_api_f3_amostra37/`, quatro objetos com readback SHA:
- `G06F3_AMOSTRA_37_CADEIAS.csv` SHA `422a9e20ed87262125db165c89d28fea3f0bc189e75c3388c64d90407befe2a5`;
- `G06F3_EMPENHOS_37.csv` SHA `c5fcd2ef754f42cc0cba1b04ef11ffe62181143f4c6a2e1134d8e7ebc57dc72e`;
- `QA_G06F3_AMOSTRA37.json`, manifesto e limitação;
- `G06F2_PROPOSTAS_CANONICAS.csv`, **cópia de verificação** da base de origem F2, não uma versão nova dos registros.

O conjunto contém horários de recuperação e referências de cada consulta. **O coeficiente 1/37 não deve ser divulgado como taxa de celebração da região**, pois a seleção não é probabilística, o campo pode estar incompleto e os instrumentos podem exigir comprovação em outros portais.

## 5. Diagnóstico metodológico

O estudo passou de `proposta_localizada` para `parceria_registro_identificado` em casos selecionados, e para `registro_empenho_localizado` em nove retornos de dois pilotos **não independentes** (2 no primeiro e 7 no segundo), portanto **não somar esses nove como empenhos exclusivos**, pois há sobreposição de municípios e consultas. Em nenhum caso se obteve documento de assinatura e comprovante de pagamento em cadeia integral. Não afirmar que a ausência de metadado exclui celebração formal em documentos externos.

A base financeira de transferências especiais ou fundo a fundo exigirá suas próprias chaves, filtros e critérios jurídicos; não igualar `Parcerias` a todo o regime de discricionárias e legais. A LC 200/2023 limita diretamente determinadas despesas da União, mas nenhum registro desta diligência documenta contingenciamento ou descontinuidade específica causada pelo teto.

## 6. Próximas operações G06-F4
1. Para **São José do Rio Preto/proposta 398** obter termo assinado e publicação mediante a URL documental ou processo público; verificar `dh_assinatura` e o objeto, sem inferir celebração de outros 36 casos.
2. Para os **sete empenhos associados** capturar `nr_empenho`, `aa_empenho`, valor e situação na fonte SIAFI; procurar vínculo inequívoco com ordem bancária/pagamento federal por número de documento ou identificação do favorecido, com coincidência de período e unidade gestora.
3. Vincular crédito na receita municipal e eventual liquidação de investimento em DCA/TCESP **por documento**, não por similaridade textual ou montante.
4. Repetir consultas em amostra maior/estratificada somente com controle de paginação, alterações de status e instrumentos jurídicos efetivos. Auditoria transversal das 508 propostas exige classificação e contagem de celebração ancorada em documento, não taxa inferida do campo na amostra.
5. Manter `G06=in_progress`; não imputar transferência ou efeito LC 200 a registros sem prova. A revisão jurídico-normativa G06-J continua prevalecendo sobre interpretações de impacto.

**Situação final:** ligação proposta–registro de parceria e alguns empenhos demonstrada tecnicamente; **instrumento celebrado, pagamento federal, receita municipal e liquidação por obra ainda não comprovados**. G06-F3 avança na rastreabilidade, sem homologação de causalidade.
