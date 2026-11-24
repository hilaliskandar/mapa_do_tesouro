# QA FED01/FED02 — RMRP — 15/11/2026

Execução local realizada sobre os ZIPs privados recuperados do Google Drive; nenhuma escrita na produção, R2 ou Cloudflare Pages. **Arquivos originais não republicados no GitHub.**

## Integridade das aquisições

| Fonte | SHA-256 ZIP | Arquivos internos com hash conferido | CRC |
|---|---|---:|---|
| Transferegov | `dcffa72828ac5d7275eed0958b89467f1cf5bcc5480b1b9b1cb2c2bc5d30adca` | 88/88 | PASS |
| Obrasgov | `80e1d798fc3bac5b1a4a2ae660be4855c77b0be2e48395a17779cadbfeefeac1` | 8/8 | PASS |

Transferegov: 34 municípios, 68 pares município–módulo, 80 páginas, 743 registros de Parcerias e 6.410 de Discricionárias; total de 7.153 registros **entre módulos**, sem deduplicação cruzada. O texto `7.153` do README interno do pacote não contradiz a contagem anterior de 743 parcerias. Cobertura 68/68 com esperado=obtido, sem erro e sem duplicidade intramódulo.

Os CSVs conferidos contêm 6.410 propostas, 1.793 convênios, 2.537 linhas de desembolso e 1.240 registros de emendas. Obrasgov: 218 projetos com chaves únicas, sem registros atuais de contratos/empenhos na respectiva rota, sem geometria e com estados 91 concluídos, 77 cadastrados, 42 em execução, seis cancelados, dois inacabados.

## Integridade das relações

| Join verificado | Correspondências | Órfãos | Conflitos do código IBGE do proponente |
|---|---:|---:|---:|
| convênio→proposta por ID_PROPOSTA | 1793 | 0 | 0 |
| desembolso→convênio por NR_CONVENIO | 2537 | 0 | 0 |
| emenda→proposta por ID_PROPOSTA | 1240 | 0 | 0 |
| Obrasgov projeto→lista candidata por ID | 218 | 0 | 0 |

Proposta, convênio, desembolso e projeto não tiveram identificadores primários duplicados no recorte. **Essas relações são documentais e de proponente**, não prova de localização física, recebimento final ou natureza capital.

## Banco isolado de ensaio FED02

Arquivo de desenvolvimento local `RMRP_FED02_STAGING_2026-11-15.sqlite`, **não enviado ao repositório ou produção**. Contém apenas campos selecionados, sem valor monetário: `proposta` 6410, `convenio` 1793, `desembolso` 2537, `emenda` 1240 e `obra_proponente` 218. `PRAGMA integrity_check` retornou `ok` e `foreign_key_check` retornou zero erros; 34 códigos IBGE7 distintos nas propostas. Tamanho 2.609.152 bytes; SHA-256 `3fdcec4af82493dd459f93f9ea8bb2d47f10b297ff2c207e6bf36302b4eaf037`.

## Encaminhamento G-FED-03

1. Capturar/recuperar em staging privado as tabelas nacionais `siconv_pagamento`, `siconv_obtv_convenente`, `siconv_dl`, `siconv_itens_dl` e ordens bancárias CGU, incluindo origem, competência e esquema.
2. Em `NR_MOV_FIN`, preservar pagamento único e tabela OBTV filha 1:N; nenhum valor monetário pode ser somado após join sem controle de fan-out.
3. Demonstrar classificação GND4 por documento independente; `ID_ITEM_PAD` ausente no arquivo `siconv_itens_dl`.
4. Isolar projetos propostos dos projetos efetivamente situados na RMRP; o recorte dos 218 não encerra o universo físico de obras.
5. Salvar o banco de desenvolvimento e relatórios no Drive privado com readback e atualizar IDs no README; **persistência externa do banco e do relatório deste gate ainda pendente**.

Este gate aprova integridade e chaves dos recortes examinados, **não** investimento federal pago/executado.

## Persistência Drive após a execução

O pacote de ensaio (SQLite local, scripts e manifestos JSON de QA) foi enviado ao Drive privado: [RMRP_FED01_FED02_Ensaio_2026-11-15.zip](https://drive.google.com/file/d/1syKGsg5F1xlfLnwpskYw_HfMRDtTfZ5O/view), ID `1syKGsg5F1xlfLnwpskYw_HfMRDtTfZ5O`, pasta `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`. Readback de metadados: 786.705 bytes, `shared=false`, permissão só do proprietário; hash SHA-256 local do pacote `85e9a814fa3d4466e7c1805da23ddfbb58827e4bc62d49e18c614c9d4a3ec9cd`. A cópia foi baixada novamente do Drive após o upload: hash SHA-256 remoto conferido e idêntico ao original local (`85e9a814fa3d4466e7c1805da23ddfbb58827e4bc62d49e18c614c9d4a3ec9cd`); teste CRC do ZIP remoto aprovado. Preservar o pacote como cópia de desenvolvimento, sem publicação de microdados.
