# FED08 — auditoria cronológica financeira e validação HTTP da integração privada

**Data:** 16/11/2026. **Fonte:** snapshot Transferegov de 15/11/2026, SQLite FED04D/FED03E privado e build estático de prévia FED07. **Estado:** auditoria detalhada executada; aceite técnico local, sem homologação de GND4 pago nem de localização material de obra.

## 1. Auditoria cronológica de 28.503 pagamentos

Foi criado e executado o script reproduzível [`pipeline/qa/audit_rmrp_fed08.py`](../pipeline/qa/audit_rmrp_fed08.py). O script compara `DATA_PAG` da tabela `siconv_pagamento` com `DATA_DE_EMISSAO` de `siconv_dl` usando `datetime.strptime('%d/%m/%Y')`, mediante `ID_DL` e `NR_CONVENIO` já conciliados.

- **28.503/28.503 pagamentos** possuem as duas datas parseáveis.
- **808 pagamentos (2,84%)** apresentam data de pagamento **anterior** à data de emissão do DL ao qual estão vinculados. Desses, **807** têm DL atualmente `Ativo` e **um** DL atualmente `Inativo`.
- **592 ocorrências são de pagamentos datados de 2012** e **150 de 2013** (742/808, cerca de 91,8%). As demais distribuem-se por outros anos do período analisado.
- A divergência cronológica é **alerta para interpretação das datas e possíveis alterações históricas do cadastro**, não prova de pagamento irregular. O status atual do documento não equivale necessariamente ao status na data original do evento.
- As **oito** movimentações positivas ligadas a DL não `Ativo` totalizam **R$ 272.120,91** e abrangem datas de pagamento entre **2009 e 2016**. Um dos oito apresenta pagamento anterior à emissão do DL. A revisão das oito deve confrontar histórico documental, situação do instrumento, anulação e retificação, e não presumir irregularidade.

**Importante:** o total bruto anterior de R$ 627.287.678,10 continua sendo soma dos eventos de pagamento, **não** valor de investimento GND4 pago. A fonte atual `item_dl` conserva rótulos e valores de itens, mas não fornece no SQLite FED04D ponte documental homologada de cada item para elemento/GND de execução paga; o status de investimento permanece `nao_classificado`.

## 2. Divergências territoriais com projeto cadastrado

Dos **20 pares projeto–coordenada** divergentes do município proponente, são **19 projetos distintos**, classificados pelo estado atual do cadastro Obrasgov:

| Localização do ponto cadastral | Situação do projeto | Pares |
|---|---|---:|
| Outro município da RMRP | Cadastrada | 6 |
| Outro município da RMRP | Concluída | 4 |
| Outro município da RMRP | Em execução | 5 |
| Outro município de SP fora da RMRP | Concluída | 1 |
| Outro município de SP fora da RMRP | Em execução | 2 |
| Fora dos polígonos de SP | Concluída | 2 |
| **Total** | | **20** |

Não se confundem os 19 projetos com 19 obras executadas fisicamente naquele ponto. A associação identifica **coordenadas vinculadas à proposta** através de cadeia documental, não evidência conclusiva da implantação da obra. Antes de homologar um pin, exigir documentação de execução/endereço/medição/registro técnico que permita comparar município do ponto e município da obra, e conservar a incerteza quando não resolvida.

## 3. Artefato privado e QA

O pacote [`RMRP_FED08_AUDITORIA_DOCUMENTAL_PRIVADA_2026-11-16.zip`](https://drive.google.com/file/d/11Mqh7XLxH5fYAulx71hvUkWeTQorSYt5/view) contém três CSV privados (808 exceções cronológicas, oito pagamentos positivos de DL não ativo, 20 pares projeto–coordenada divergentes) e JSON agregado **sem identificadores individuais**. Tamanho 10.259 bytes, SHA-256 `aaaef0a7cdee4da5da20e2648d6e4f9c74f14226e84cdfba9f60584f559f558f`, upload para pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`, readback de conteúdo idêntico e CRC íntegro; `shared=false`.

Validações: conservação do universo de 28.503 pagamentos, 808 exceções cronológicas, oito movimentos positivos DL não ativo, 27.212.091 centavos nesses oito, 20 pares territoriais e 19 projetos distintos; `PRAGMA integrity_check=ok` e `foreign_key_check` sem violações.

## 4. Gate de integração técnica da plataforma

Foi executado o validador [`pipeline/qa/validate_rmrp_api_v3_fed07.py`](../pipeline/qa/validate_rmrp_api_v3_fed07.py) sobre a prévia privada integrada, com **1.603 verificações aprovadas**. O teste HTTP local [`deployment/qa_rmrp_fed07_local_http.py`](../deployment/qa_rmrp_fed07_local_http.py) levantou temporariamente um servidor restrito a `127.0.0.1` e verificou **288 requisições HTTP 200**, incluindo **285 JSON parseáveis**, sem falhas. Os seis endpoints preexistentes da RMRP no frontend foram comparados byte a byte entre o repositório e a árvore integrada e permaneceram **6/6 idênticos**. O pacote privado de referência da integração é [FED07_SITE_PREVIA_PRIVADA](https://drive.google.com/file/d/1whZO3RZABn9aIS3SrF5_8DqGdyBSwTZT/view).

O teste HTTP local **não é** teste visual de navegador nem publicação no Cloudflare Pages. A ausência de erros HTTP não substitui a verificação de cache/CDN, navegação, acessibilidade, responsividade ou regressão completa de séries TCESP.

## 5. Gate de homologação para o próximo avanço

- **Aprovado tecnicamente para incorporação em ambiente de desenvolvimento/restrito:** classificação de propostas e projetos por proponente, quatro sub-regiões, vínculos de instrumentos, contagens de pagamentos por instrumento e cobertura cadastral, sem qualquer indicador de capital executado.
- **Pendente de evidência substantiva:** natureza GND4 efetivamente paga, estornos/devoluções, temporalidade dos 808 alertas de DL, documentação individual dos 19 projetos com divergência de coordenada e comprovação dos pontos físicos.
- **Produção:** não houve deploy de nova release nem escrita em D1; `public_release_authorized=false` permanece obrigatório. As classes `em_revisao` e `candidato` não podem alimentar agregado rotulado como investimento executado.

**Próxima frente operacional:** identificar fontes oficiais capazes de demonstrar natureza da despesa efetivamente liquidada/paga; recuperar documentações dos 19 projetos prioritários em lotes menores e obter evidências individualizadas antes de mudar `qa_status` para `homologado`.
