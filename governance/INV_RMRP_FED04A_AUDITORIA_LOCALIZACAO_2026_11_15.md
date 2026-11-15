# FED04A — auditoria executada de localização Obrasgov RMRP

**Data:** 15/11/2026. **Universo:** 218 projetos candidatos relacionados pelo município proponente à RMRP; não equivale ao conjunto de intervenções fisicamente situadas na região.

## Execução
O arquivo `RMRP_Obrasgov_2026-11-15.zip` foi aberto localmente e seu objeto `obrasgov_rmrp_218_project_details.json` foi percorrido integralmente. Uma cópia da base `RMRP_FED03B_CATEGORIAS_2026-11-15.sqlite` recebeu a nova tabela `obra_evidencia_localizacao` (218 projetos por identificador, uma linha cada). Não foram geradas coordenadas, endereços nem identificação presumida de município de execução.

| Evidência consultada no objeto do projeto | Resultado |
|---|---:|
| Projetos / documentos com descrição textual | 218 / 218 |
| CEP `nr_cep` não vazio | 0 |
| Endereço `desc_endereco` não vazio | 0 |
| Entradas em `pins` | 0 |
| Entradas em `geometria` | 0 |
| Projetos sem localização física comprovada no pacote | 218 |

**QA:** `PRAGMA integrity_check=ok`, sem violação de chaves estrangeiras. SHA-256 ZIP de origem `80e1d798fc3bac5b1a4a2ae660be4855c77b0be2e48395a17779cadbfeefeac1`; SHA-256 do SQLite atualizado `3bc6248e547e255639691671d69ec922b26c79fe6ec9d9b1852908d5f33212f6`. A auditoria **não** exclui localização em documentação externa; os campos textuais exigem verificação independente.

**Drive:** [RMRP_FED04A_Auditoria_2026-11-15.zip](https://drive.google.com/file/d/1sb7dn4T4ijPiZe3Z-_M7vdmKQTPsneP_/view), ID `1sb7dn4T4ijPiZe3Z-_M7vdmKQTPsneP_`, 889.630 bytes, pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`. Upload e readback de metadados confirmados, `shared=false`; SHA-256 local do pacote `b98d840790cf3cb95b64ef9ebeddc94b824cc4a813c8b3bc4767a33f63466db2`; download de readback executado, SHA-256 idêntico ao arquivo de origem local (`b98d840790cf3cb95b64ef9ebeddc94b824cc4a813c8b3bc4767a33f63466db2`) e CRC integral aprovado.

## Gate territorial seguinte
Recuperar `siconv_coordenadas_obra` (441 linhas anteriormente associadas a propostas de proponentes RMRP no levantamento nacional), vincular `ID_PROPOSTA` à proposta e instrumento, testar cardinalidade 1:N, validar valores numéricos e ordem latitude/longitude; intersectar cada ponto válido com limites municipais oficiais, documentar CRS e precisão e separar local físico de município proponente. Não inventar ligação proposta–projeto sem ponte documental. Ampliar a consulta estadual Obrasgov para incluir executor federal/estadual.

## Estado FED03C
O projeto já possui `pipeline/acquire/inv_sp645_payment_obtv_cardinality.py` com auditoria nacional concluída em execução anterior; esse resultado apenas comprova cardinalidade, não produz recorte monetário da RMRP. A tentativa de acessar diretamente `https://api-publica.transferegov.gestao.gov.br/downloads` no ambiente local desta rodada resultou em falha DNS, portanto **nenhum pagamento/OBTV/DL novo foi recuperado ou conciliado nesta execução**. FED03C permanece pendente de obter os ZIPs em ambiente com acesso à fonte e staging privado, nunca presumir que `siconv_desembolso` equivale a pagamento final.
