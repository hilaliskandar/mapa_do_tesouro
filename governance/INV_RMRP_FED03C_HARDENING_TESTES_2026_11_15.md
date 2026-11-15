# FED03C — reforço da validação financeira e testes, 15/11/2026

**Estado:** reconciliador reforçado e testado com dados **sintéticos**; dados nacionais reais de pagamentos, OBTV e DL **não recuperados** nesta rodada. Sem homologação de pagamentos de investimento e sem alteração da plataforma pública.

## Ambiente e fontes

- Inspecionados os scripts de `RMRP_FED03C_FED04B_RUNNER_2026-11-15.zip` e a cópia do SQLite de desenvolvimento. Os scripts de produção ainda requerem ZIPs nacionais do Transferegov.
- Repetida a verificação DNS no executor para `api-publica.transferegov.gestao.gov.br`, `repositorio.dados.gov.br` e `www.gov.br`: `Temporary failure in name resolution`. Isso é uma limitação desta execução, não comprovação de indisponibilidade da fonte.
- [Portal oficial de dados abertos](https://api-publica.transferegov.gestao.gov.br/) e [comunicado de migração 2026](https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br) corroboram o catálogo atual. O cronograma governamental distingue API de instrumentos e API de execução financeira, ainda em implantação; não confundir a presença de CSVs com disponibilidade de todos os endpoints de execução.

## Alterações efetivamente implementadas

Foi criada uma variante de ensaio `fed03c_reconcile_hardened.py` do reconciliador existente para:

1. Calcular SHA-256 dos ZIPs por leitura em blocos, evitando carregar integralmente arquivos nacionais grandes em memória.
2. Validar `VL_PAGO` com `Decimal` e conversão exata para centavos, aceitando `1234,56`, `1.234,56`, `1234.56` e inteiros; rejeitar números inválidos, ambíguos, `NaN`, infinito e mais de duas casas decimais. Não é efetuada agregação monetária.
3. Registrar quantidade de valores positivos, negativos, zeros e ausentes. Negativos são conservados para revisão e potencial estorno, não descartados.
4. Preservar uma linha por `NR_MOV_FIN` na tabela `payment` e a contagem separada de linhas OBTV por movimento, sem multiplicar `VL_PAGO` após junção.
5. Bloquear o processamento quando a seleção dos convênios da RMRP não encontrar qualquer pagamento (evita status de sucesso vazio).
6. Manter `qa_status` não homologado; não inferir natureza GND4 da simples associação a `ID_DL`.

O arquivo original de produção não foi substituído; a variante e testes estão no pacote privado, para revisão e execução no runner autorizado.

## Testes realizados

- Teste pré-existente `test_reconciliadores.py` executado com sucesso: **1 pagamento com duas linhas OBTV e um DL**, coordenada candidata, ausente e inválida.
- Novo `test_hardened_fed03c.py` executado com sucesso: leitura monetária em formatos distintos, rejeição de precisão inválida, `NaN` e infinito; identificação de positivo/negativo/zero; prevenção de multiplicação 1:N; deduplicação do vínculo de DL; `PRAGMA integrity_check=ok`, zero violações FK; erro esperado em valor financeiro malformado.

**Limites dos testes:** não foram verificados valores reais do banco nacional, consistência com ordens bancárias CGU, natureza de despesa paga, estornos ou localização física. Nenhuma métrica de investimento federal executado foi produzida.

## Artefato e persistência

[ZIP privado FED03C QA reforçado](https://drive.google.com/file/d/1iMQew6peFHqCYAapipdYFORMucTgF61o/view) (ID Drive `1iMQew6peFHqCYAapipdYFORMucTgF61o`, pasta `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`), 10.144 bytes, `shared=false`. Upload e download de conferência efetuados; SHA-256 `e78d86558182887c79325f02e2b182e80ac33c75c953b3405068ab023f6ff7e3`, teste CRC integral aprovado. O pacote contém variante Python, testes, importador FED04B e README de execução.

## Próxima condição necessária

Obter em ambiente com DNS/HTTPS autorizados os ZIPs oficiais de `siconv_pagamento`, `siconv_obtv_convenente`, `siconv_dl`, `siconv_itens_dl` e `siconv_coordenadas_obra`. Registrar hash, versão, tamanho e data da fonte; executar reconciliação dos 1.793 convênios de municípios proponentes RMRP, auditoria de cardinalidade e vínculo documental. Só depois classificar com prova eventual gasto de capital, e validar coordenadas com polígonos municipais e instrumentos de projeto. **FED03C e FED04B continuam pendentes de dados nacionais reais.**
