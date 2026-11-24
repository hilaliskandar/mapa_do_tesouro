# Retomada FED03C e FED04B — aquisição nacional ainda pendente

**Situação em 15/11/2026:** a aquisição regional já foi concluída (34 municípios, 80 páginas da API e 218 candidatos Obrasgov). A execução dos dados nacionais de pagamento, OBTV, documentos de liquidação e coordenadas físicas segue **não realizada** nesta sessão. Este documento é um diagnóstico de acesso, não manifesto de captura nacional.

## Endereços e fontes observados

- Página oficial [Transferegov — download de dados Discricionárias e Legais](https://www.gov.br/transferegov/pt-br/ferramentas-gestao/dados-abertos/download-dados) confirma publicação diária das principais bases CSV, incluindo pagamentos a favorecidos, OBTV ao convenente e planos de aplicação.
- Página oficial [Transferegov — novo portal das APIs](https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br), com migração de catálogos anunciada em julho de 2026.
- O coletor versionado [`pipeline/acquire/inv_sp645_transferegov_new_source_layout.py`](../pipeline/acquire/inv_sp645_transferegov_new_source_layout.py) aponta como base `https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/`, por exemplo `siconv_coordenadas_obra.zip` e `siconv_itens_dl.zip`. Essa URL é uma **configuração de coletor**; a leitura pública dos arquivos não foi confirmada nesta rodada.
- O coletor existente [`pipeline/acquire/inv_sp645_payment_obtv_cardinality.py`](../pipeline/acquire/inv_sp645_payment_obtv_cardinality.py) registra a cardinalidade nacional de `NR_MOV_FIN` sem divulgar microdados.

## Tentativas reais desta sessão

- `getaddrinfo` no container para `api-publica.transferegov.gestao.gov.br`, `repositorio.dados.gov.br` e outros domínios: falha DNS `Temporary failure in name resolution` (bloqueio geral de rede, não prova de indisponibilidade do servidor).
- Tentativa de leitura pública de `https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/siconv_coordenadas_obra.zip`: indisponível pela ferramenta web e inadequada como leitura Markdown no crawler; **não** se pode afirmar erro 404 deste endpoint.
- O endereço legado `https://repositorio.dados.gov.br/seges/detru/siconv_pagamento.csv.zip` retornou erro **404** na consulta externa. O link da página governamental pode estar defasado ou o gateway pode redirecionar para nova estrutura; não reclassificar a fonte inteira como descontinuada sem verificação do novo portal.
- Busca pontual no Drive por `siconv_pagamento`, `siconv_obtv_convenente` e `siconv_coordenadas_obra` não localizou ZIPs nacionais com esses nomes. A busca por nome **não comprova inexistência** de arquivos dentro de outros pacotes ZIP.

## Plano exato do runner de aquisição

1. Verificar resolução DNS e HTTPS do domínio oficial, versão e tamanho do snapshot; operar com `ETag`, `Last-Modified` e SHA-256.
2. Buscar **apenas** bases nacionais faltantes: `siconv_pagamento`, `siconv_obtv_convenente`, `siconv_dl`, `siconv_itens_dl`, `siconv_coordenadas_obra`, eventualmente `siconv_contrato_cipi` e ordens bancárias CGU. Persistir ZIP original em R2 privado ou Drive privado antes de filtrar, se autorizado; não inserir microdados nacionais em commit.
3. Filtrar pagamentos pelos 1.793 convênios da tabela `convenio` no SQLite FED03; checar a unicidade de `NR_MOV_FIN` e cardinalidade filhos OBTV. `VL_PAGO` apenas no nó pai; não somar após o JOIN 1:N.
4. Atribuir `ID_DL` e identificadores de natureza da despesa apenas mediante vínculo explícito; não equiparar PAD GND4 aprovado a item financeiro pago sem ponte documental.
5. Vincular `siconv_coordenadas_obra` à proposta por `ID_PROPOSTA`; para chegar ao projeto Obrasgov exigir cadeia proposta→convênio→instrumento→projeto, com cobertura e órfãos auditados. Validar CRS, latitude/longitude, interseção e precisão, sem usar município proponente como local físico.
6. Atualizar manifestos, SHA256, datas/versões e gates, executar readback de Drive e preparar novas versões privadas API v3; a base pública continua bloqueada até homologação.

## Situação de produção

Não houve nova aquisição de pagamentos, OBTV, DL ou coordenadas nesta sessão. **FED03C/FED04B permanecem pendentes.** A dimensão oficial de quatro sub-regiões (**FED06B**) foi, em contrapartida, concluída, e sua prévia privada está [no Drive](https://drive.google.com/file/d/1gjLGe4IfK5WipARJ7SBo9WcsGWtrFoQ5/view).
