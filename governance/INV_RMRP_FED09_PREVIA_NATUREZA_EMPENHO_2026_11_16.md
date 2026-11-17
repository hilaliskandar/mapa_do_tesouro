# FED09 — integração privada de desembolsos por natureza de empenho

**Data:** 16/11/2026. **Status:** camada estática de desenvolvimento gerada, conservada e testada; **nenhum indicador de investimento de capital pago homologado** e nenhum deploy público.

## Base metodológica

A integração utiliza a cadeia oficial `siconv_empenho.ID_EMPENHO + NR_CONVENIO → siconv_empenho_desembolso.ID_EMPENHO/ID_DESEMBOLSO → desembolso_fluxo.id_desembolso`, documentada no [FED08B](INV_RMRP_FED08B_EMPENHOS_DESEMBOLSOS_NATUREZA_2026_11_16.md). A chave composta é mandatória porque dois IDs de empenho foram reutilizados em convênios diferentes. Os três ZIPs oficiais e o staging FED08B estão preservados no Drive privado, cada um com SHA-256/CRC de readback aprovados.

De **2.537 desembolsos**, **2.535** possuem todos os grupos conciliados em centavos com o valor pai. Um permanece sem ponte e outro difere em **R$ 88.000,00**; ambos ficam fora da distribuição de natureza e seguem classificados como pendentes.

## Dados incorporados em prévia privada

O código reproduzível [`deployment/build_rmrp_fed09_private.py`](../deployment/build_rmrp_fed09_private.py) opera **somente sobre cópia isolada** do site FED07, com marcador privado. Acrescenta aos 34 JSON municipais, quatro JSON de sub-região e 19 JSON anuais um objeto de diagnóstico rotulado como **desembolso transferido vinculado à natureza do empenho**. Não modifica `totais_por_dimensao.federal_pagamentos_diretos_investimento_centavos`, que continua `null`. Não promove `localizacao_fisica` de projetos.

| Prefixo do código de natureza dos grupos de empenho | Total dos grupos em 2.535 desembolsos conciliados |
|---|---:|
| `44` — categoria 4 e grupo 4 conforme classificação orçamentária usual | R$ 450.501.858,85 |
| `33` — categoria 3 e grupo 3 | R$ 263.567.534,82 |
| `34` — código que requer revisão documental | R$ 250.000,00 |
| **Soma somente dos grupos dos desembolsos conciliados** | **R$ 714.319.393,67** |

Esses grupos **não** podem ser somados novamente aos R$ 714.989.114,47 do conjunto integral de desembolsos, nem aos R$ 627.287.678,10 dos eventos de pagamento a favorecidos. `44` constitui atributo da **natureza orçamentária do empenho relacionado ao desembolso**, não prova de **despesa de capital paga diretamente a fornecedor ou executada no município**. As duas ocorrências pendentes não foram rateadas.

O `manifest.json` registra 2.535 desembolsos conciliados e duas pendências, mais os hashes dos três ZIPs oficiais novos. `pendencias.json` identifica a ausência de GND4 final pago. `qa_status=em_revisao` e `public_release_authorized=false` persistem. Os 218 JSON de projetos continuam sem ponto de execução comprovado e com valor pago de investimento igual a `null`.

## QA e regressões

- Conservação regional dos prefixos **33/34/44** ao agregar os 34 municípios, quatro sub-regiões e 19 anos, sem somar eventos de estágios distintos; 2.535 conciliados e 2 pendentes.
- Validação de API FED07 reutilizada: **1.603 verificações** aprovadas.
- Servidor local restrito `127.0.0.1`: **288 respostas HTTP 200**, **285 JSON parseáveis**, nenhuma resposta de erro.
- Os seis JSON preexistentes da plataforma permaneceram **idênticos byte a byte** depois do overlay.
- Fonte SQLite FED08B: `PRAGMA integrity_check=ok`, zero violações FK; ZIP de saída com CRC e SHA-256 conferidos após download do Drive.

## Arquivo integrado no Drive

[**RMRP_FED09_SITE_PREVIA_PRIVADA_2026-11-16.zip**](https://drive.google.com/file/d/1BpoxzYgVfTIQ7rIhsEQQGNUhG563EoHQ/view), ID `1BpoxzYgVfTIQ7rIhsEQQGNUhG563EoHQ`, **799.437 bytes**, SHA-256 `9f4e63092048068277e8cc30c3eaccf29661c2579fd6b22861ff4b2f74253d72`, CRC aprovado após readback. Acesso `shared=false`, pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`. O pacote contém a árvore local de frontend, **285 endpoints JSON da API v3** e QA técnico; não foi implantado no Cloudflare Pages.

## Condições para publicação

1. Resolver com documentação oficial os **dois desembolsos** sem ponte ou com soma divergente; confirmar a semântica do código `34`.
2. Buscar/validar ponte da classificação orçamentária até **pagamentos finais** para permitir afirmar eventual GND4 pago, estornos e valor líquido, sem reutilizar etapas de transferência como gasto executado.
3. Rever os **808 casos** de cronologia `pagamento < emissão DL` do FED08, incluindo histórico dos oito positivos ligados a DL não ativo; investigar, sem prejulgamento de irregularidade.
4. Confrontar os 19 projetos com coordenadas de proposta divergentes com documentação do local real e status de execução.
5. Executar homologação funcional/visual num build restrito Cloudflare Pages, QA de regressão de séries TCESP 2023–2025, segurança/cache e aceite de release.

**Gate de produção:** bloqueado; `public_release_authorized=false`. Os valores classificados pela natureza dos empenhos são utilizáveis apenas como **diagnóstico de desembolsos em prévia privada**, nunca como indicador homologado de investimentos executados.
