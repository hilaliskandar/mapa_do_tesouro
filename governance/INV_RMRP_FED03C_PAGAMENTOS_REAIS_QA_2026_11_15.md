# FED03C — aquisição e recorte financeiro real de pagamentos, OBTV e liquidações

**Data:** 15/11/2026. **Fonte:** arquivos nacionais oficiais SICONV do Transferegov em `https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/`. A aquisição e o processamento foram realizados em runner remoto com conectividade, diferentemente do container local sem DNS. **São registros reais, não testes sintéticos.** Nenhum dado nacional bruto ou identificação de favorecidos foi publicado no GitHub.

## Fontes nacionais adquiridas e auditadas

| Arquivo | Linhas nacionais CSV | Tamanho ZIP (bytes) | SHA-256 ZIP | Drive privado |
|---|---:|---:|---|---|
| `siconv_pagamento.zip` | 7.575.512 | 374.662.483 | `bf5125e6aaf1105269947b1f905ff910113574dac6edb4335ebde3ec31cd8bc7` | [Arquivo oficial](https://drive.google.com/file/d/1mfk_Xd3J9-lQ5B5gelb9XhgH4mRD4TSK/view) |
| `siconv_obtv_convenente.zip` | 3.113.841 | 58.726.469 | `c44f9597b73bf0e01136411326a33857f7235e932182a3f70385d6710f5ad74b` | [Arquivo oficial](https://drive.google.com/file/d/1SoGpUlkcFBxc46bVjjg9SsGgAE4r6peA/view) |
| `siconv_dl.zip` | 7.710.768 | 216.458.339 | `637b6da28bbe87a50306eb431c3a23979e8fe52ed34d3ecc516615999041ea64` | [Arquivo oficial](https://drive.google.com/file/d/1mQFm981kWQknunL-DeldIKYCj5vRMQEH/view) |
| `siconv_itens_dl.zip` | 10.079.834 | 548.549.412 | `717a743a96b116ad8e92888c0426aa3b4b333b079af91aeff4d2a0e4aa7b3566` | Upload integral ainda não confirmado |

Os quatro downloads receberam resposta HTTP 200 e metadados `Last-Modified` em 15/11/2026. SHA-256 calculado por streaming e integridade ZIP verificada por `testzip()=None` para cada origem. **Os três primeiros ZIPs** estão no Drive privado na pasta `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`, com tamanhos e `shared=false` verificados por metadados. O quarto foi baixado e verificado em runner remoto; uma tentativa de upload excedeu o limite de tempo, de modo que **não consta como persistido**. Não confundir verificação do arquivo fonte com readback de integridade no Drive, ainda pendente para os três maiores.

## Recorte nacional executado

SQLite de desenvolvimento FED04B foi carregado do Drive e copiado como `RMRP_FED03C_FED04B_STAGING_2026-11-15.sqlite`, preservando 1.793 convênios, 6.410 propostas, 218 projetos e as tabelas territoriais anteriores.

| Conjunto | Linhas nacionais examinadas | Linhas selecionadas |
|---|---:|---:|
| Pagamentos `NR_CONVENIO` pertencentes ao recorte RMRP | 7.575.512 | **28.503** |
| Detalhes OBTV por `NR_MOV_FIN` do conjunto de pagamentos | 3.113.841 | **395** |
| DL por `ID_DL` selecionado ou `ID_PROPOSTA` no universo RMRP | 7.710.768 | **28.256** |
| Itens de DL por `ID_DL` retido | 10.079.834 | **39.498** |

Os pagamentos selecionados pertencem a **1.286 convênios distintos**; há **28.503 movimentos financeiros distintos** no conjunto selecionado. Não foi usada junção com OBTV para multiplicar pagamentos. Os valores individuais foram convertidos para centavos com `Decimal`, guardando as representações originais e sem agregação numérica ou classificação automática como capital.

**QA executado:** zero movimentos de pagamento repetidos, zero filhos OBTV órfãos, zero itens DL órfãos, zero erros de valor monetário nos registros selecionados, zero IDs de DL repetidos, `PRAGMA integrity_check=ok` e `foreign_key_check` vazio. Os vínculos de OBTV possuem cardinalidade e natureza próprias; `ID_DL` não é ligação direta a GND4 pago e não prova realização do investimento.

## Persistência do recorte privado

[ZIP de staging FED03C/FED04B e QA JSON](https://drive.google.com/file/d/1ZXhCXe-nDMadChIoV2QzoYHczBTigJsJ/view), ID `1ZXhCXe-nDMadChIoV2QzoYHczBTigJsJ`, 5.448.932 bytes, SHA-256 original `8184c1e06d4e4258d9c1bdd01daa407e7c7387f3251b80fb0a9cba7db60f36ea`; o upload foi confirmado em pasta privada com `shared=false` e tamanho correto. O pacote inclui SQLite e `RMRP_FED03C_REAL_QA_2026-11-15.json`, com contagens e avisos. ZIP local da fonte derivada com CRC correto.

## Pendências metodológicas

1. Não equiparar pagamentos aos favorecidos, desembolsos ao convenente, valores de DL e itens de DL: são estágios e granularidades distintos, com possíveis retenções e devoluções.
2. Necessário auditar estornos, movimentos negativos, documentos de mesma operação e diferença entre pagamento bruto e líquido, incluindo a etapa CGU/OBTV.
3. **Natureza de despesa efetivamente paga** não está homologada. O catálogo de PAD aprovado com GND4 não basta para inferir GND4 pago sem ponte por item e documento.
4. Para localização física, FED04B possui coordenadas **candidatas** associadas a 218 projetos, porém requer interseção e validação documental com municípios IBGE EPSG:4674 e inspeção de seis registros anômalos.
5. Os indicadores de investimentos da API v3 continuam nulos/não homologados; `public_release_authorized=false` e a base produtiva não foi alterada.


### Encerramento da persistência dos sete ZIPs oficiais — 15/11/2026

Após dividir a verificação em **quatro operações independentes**, cada fonte financeira foi recuperada do Drive e seu SHA-256 integral calculado por streaming, retornando **igualdade com o hash da origem**: 

| Fonte | Arquivo Drive | Bytes após download | SHA-256 conferido |
|---|---|---:|---|
| `siconv_pagamento.zip` | [Arquivo](https://drive.google.com/file/d/1mfk_Xd3J9-lQ5B5gelb9XhgH4mRD4TSK/view) | 374.662.483 | `bf5125e6aaf1105269947b1f905ff910113574dac6edb4335ebde3ec31cd8bc7` |
| `siconv_obtv_convenente.zip` | [Arquivo](https://drive.google.com/file/d/1SoGpUlkcFBxc46bVjjg9SsGgAE4r6peA/view) | 58.726.469 | `c44f9597b73bf0e01136411326a33857f7235e932182a3f70385d6710f5ad74b` |
| `siconv_dl.zip` | [Arquivo](https://drive.google.com/file/d/1mQFm981kWQknunL-DeldIKYCj5vRMQEH/view) | 216.458.339 | `637b6da28bbe87a50306eb431c3a23979e8fe52ed34d3ecc516615999041ea64` |
| `siconv_itens_dl.zip` | [Arquivo](https://drive.google.com/file/d/1Io7ZUfE268rS-CwSEMgfrmyrlV1oe2UQ/view) | 548.549.412 | `717a743a96b116ad8e92888c0426aa3b4b333b079af91aeff4d2a0e4aa7b3566` |

Todos os quatro estão na pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`, `shared=false`, tamanhos verificados; ZIPs já tinham CRC da origem `OK`. Os três ZIPs territoriais também tinham readback SHA-256 e CRC aprovados. **GATE DE AQUISIÇÃO E PERSISTÊNCIA DOS 7 ZIPs: CONCLUÍDO.** Isto não altera os gates de classificação de investimentos pagos, estornos e localização física.
