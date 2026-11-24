# FED11 — auditoria de origem dos dois desembolsos pendentes e novas fontes de metas

**Data:** 16/11/2026. **Universo:** 2.537 desembolsos vinculados a convênios cujos proponentes pertencem à RMRP; 19 projetos Obrasgov com divergência espacial. **Status de aceite:** fonte documental conferida; duas exceções financeiras mantidas abertas, sem homologação de localização física nem de GND4 pago.

## Recuperação de fontes oficiais — snapshots de 15/11/2026

Quatro ZIPs nacionais do repositório oficial `https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/` foram obtidos por HTTPS, examinados integralmente e persistidos no Drive privado, pasta `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`:

| Base | Tamanho em bytes | SHA-256 da origem | Arquivo no Drive |
|---|---:|---|---|
| `siconv_desembolso.zip` | 16.863.271 | `ec66d2557a6a6842c8415daf520ab7f1d26886bd138a0e05f5d5ec1b877f6f9d` | [ZIP](https://drive.google.com/file/d/1rH7WC_pkIvrFlVeWSr8DWKPTTS78jy72/view) |
| `siconv_inst_cont_metas_submetas_po_modulo_empresas.zip` | 2.247.267 | `149e167fe3fb1175ed06ca4886c05a8f69532fef1e3a9b23eecc742f4d67fc09` | [ZIP](https://drive.google.com/file/d/1O1J8Kkl8hh3CR8AxwqPXCSnDG2Mk0xjy/view) |
| `siconv_projeto_basico_metas_modulo_empresas.zip` | 7.408.950 | `f4f91ceb3e64de2fee67a0d74092e166c7883e6fbc5f3ed29de202a0909c1d99` | [ZIP](https://drive.google.com/file/d/1J_8d6mi0aLGHiGUHEIUGDR5B9huwNMxb/view) |
| `siconv_projeto_basico_submetas_modulo_empresas.zip` | 16.567.290 | `3f64f185f03a669deae6d7cdf2dcef0828a7ef80ad3802c643742979a9fc3dd9` | [ZIP](https://drive.google.com/file/d/1e63p00GA4n6IGUIjmRKtZ0bOgmghCYKq/view) |

A conferência individual por download de retorno confirmou os quatro tamanhos, SHA-256 idênticos aos da origem e CRC íntegro. Os metadados do Drive confirmam pasta privada e `shared=false`.

## Análise dos dois desembolsos pendentes

Os dois eventos já identificados no FED08B foram localizados por `ID_DESEMBOLSO` no **CSV nacional original**. Para ambos, foram conferidos número do convênio, data do desembolso, ordem bancária `NR_SIAFI` e observações `OBSERVACAO_DH`. Os valores do arquivo nacional coincidem com o staging do FED08B.

**Primeiro caso — diferença exata de R$ 88 mil:** registro de desembolso de R$ 475.000,00, com apenas R$ 387.000,00 em grupos de empenho ligados por `ID_DESEMBOLSO`. Há no **mesmo convênio** um empenho adicional de **R$ 88.000,00**, natureza de despesa iniciada por `44`, identificado no cadastro nacional de empenhos, mas **sem vínculo explícito a esse desembolso** no arquivo `siconv_empenho_desembolso`. A diferença coincide em valor, mas **a hipótese de vínculo omitido não pode ser convertida em correção automática**. É necessária prova documental via SIAFI/convênio/ordem bancária ou registro oficial complementar.

**Segundo caso — ausência total de ponte:** desembolso de **R$ 194.720,80**, com `NR_SIAFI` e observação sobre parcela do convênio identificados. O mesmo convênio possui empenhos em seu cadastro, mas o arquivo oficial de vínculos **não apresenta grupo para esse desembolso**. A situação de prestação de contas do convênio está registrada como concluída, o que não resolve a lacuna documental do vínculo de natureza.

As duas ocorrências seguem em `divergente` e `sem_ponte`, respectivamente. **Os 2.535 desembolsos conciliados permanecem íntegros; nenhum centavo pendente foi artificialmente reclassificado.**

## Novas fontes de metas e limites de localização

O arquivo nacional de metas e submetas de instrumento contratual foi percorrido integralmente: **47.595 linhas**. Nenhuma linha contém `ID_PROPOSTA_INSTRUMENTO_CONTRATUAL` correspondente às **19 propostas** da carteira de projetos espacialmente divergentes. Esse resultado é **negativo apenas para a ligação direta nessa tabela e nesse snapshot**; não significa que as obras não tenham metas, projeto básico ou instrumento contratual em outros módulos.

Os CSV de metas e submetas de projeto básico trazem referências a `ID_QCI_ACFFO` e `ID_META_PROJETO_BASICO`, respectivamente. A associação ao `ID_PROPOSTA` exige **ponte intermediária verificada**, e não pode ser inferida por descrição ou coincidência nominal. Sua coleta preserva o material para a etapa de rastreabilidade documental.

Não se recuperou prova de endereço, trecho executado ou coordenada física. **FED10 permanece com zero locais físicos homologados.**

## Persistência das evidências individuais

[**RMRP_FED11_EXCECOES_DESEMBOLSO_PRIVADO_2026-11-16.zip**](https://drive.google.com/file/d/1bbAOkWv9C8XgvhvDnR5I6POvUDnFAQwz/view), 1.678 bytes, SHA-256 `8c7733adb8d85cea474c30d7fd5a1116c5cfaf49eb61042549e90479d732524c`, readback SHA-256 e CRC aprovados. Contém o QA agregado e identificadores individuais/observações SIAFI dos dois eventos; armazenado somente no Drive privado.

## Estado da plataforma e próximas homologações

1. **Finanças:** manter 2 desembolsos em revisão e documentação dos 2.535 conciliados; classificação por natureza do empenho não equivale a GND4 pago; requer documento financeiro final e estornos.
2. **Território:** prosseguir na ponte entre projeto básico e metas por identificadores oficiais; obter peças com localização explícita dos 19 projetos. Não usar proposta rejeitada, coordenadas de cadastro ou percentual físico como local executado sem prova.
3. **Release:** a última prévia FED10 do site continua no Drive privado, com 1.603 validações de API e 288 HTTP locais já aprovados. Testes browser/Cloudflare Pages restrito ainda não foram realizados. Verificação do runner remoto atual: não há Chromium, Firefox ou Playwright instalados — portanto não se afirma homologação visual.
4. **Governança:** `public_release_authorized=false`; sem alteração do site produtivo nem das séries TCESP.

