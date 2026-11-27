# Transferegov financeiro — staging estadual de SP

**Data da execução:** 27/11/2026  
**Branch:** `investimentos-territoriais-sp645-20261111`  
**Workflow:** SP645 Transferegov financial staging  
**Execução final:** [GitHub Actions run 46006854691](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/46006854691) — `success`  
**Commit do ajuste:** `85a864f7710276abab95ac750698d23fcef2e040`

## Resultado e correção aplicada

A execução anterior ([run 46003482093](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/46003482093)) falhou porque o coletor esperava nomes de colunas incompatíveis com os arquivos financeiros atuais. O desembolso passou a exigir `DATA_DESEMBOLSO` e `VL_DESEMBOLSADO`; o pagamento, `DATA_PAG` e `VL_PAGO`. Após o ajuste, a coleta, a persistência temporária no R2 com leitura de retorno e a geração do artefato de QA terminaram com sucesso.

O recorte é estadual: os registros foram selecionados pelo **município proponente** (645 municípios de SP), não pela localização física das intervenções. Os totais abaixo são valores nominais observados nas respectivas bases financeiras.

| Etapa financeira | Eventos nacionais | Eventos selecionados | Municípios com registros | Instrumentos | Soma nominal selecionada |
|---|---:|---:|---:|---:|---:|
| Desembolso | 388.937 | 47.392 | 645 | 24.391 | R$ 16.435.561.213,55 |
| Pagamento | 7.601.965 | 945.970 | 644 | 22.598 | R$ 14.883.472.846,25 |

Bases de identificação associadas: 1.161.499 propostas nacionais e 289.183 convênios nacionais; o recorte associou 134.538 propostas e 34.492 convênios.

## Manifesto e persistência

| Conjunto | Tamanho ZIP | SHA-256 do ZIP |
|---|---:|---|
| `siconv_proposta` | 206.420.148 bytes | `87171c9ee363871646c6a475362c66763158b5281f0711611349c88026255d5b` |
| `siconv_convenio` | 18.538.941 bytes | `357e012a3e76e502135e94241529ec30bde623f12493366405f9c3cd671e3496` |
| `siconv_desembolso` | 16.981.452 bytes | `4107f6f78a95a99b03254173f08d1ada9b53de937eaede34824c016bfd8737ca` |
| `siconv_pagamento` | 376.114.517 bytes | `5972b050f7a9ad9c0038befc6f4d605474e6d88e0f9d80dc0b4e8d59b2d108d5` |

O arquivo compactado de staging foi gravado no R2 e lido de volta com hash correspondente:

- Chave: `sp_645/federal/transferegov/financial/staging/run_46006854691/d7c0d8758fca9434e5c348e8f2be8905d443b1737ecc31b6aaffa33ddeaf77cc.tar.gz`
- SHA-256: `d7c0d8758fca9434e5c348e8f2be8905d443b1737ecc31b6aaffa33ddeaf77cc`

O artefato de QA da execução está associado ao run indicado acima (`sp645-transferegov-financial-qa`, artifact ID `15201482957`).

## Limites de interpretação e pendências

- Desembolso e pagamento são etapas financeiras distintas. **Não somar os valores**: isso duplicaria fluxos e não produziria uma medida de investimento.
- O recorte territorial indica o proponente. Ele não demonstra onde a obra, bem ou serviço foi executado.
- Os arquivos não informam natureza de capital nesse conjunto; portanto, os totais não podem ser rotulados como investimento executado, obra entregue ou benefício territorial.
- O QA encontrou **5 pagamentos com valor negativo**, **2.194 pagamentos de valor zero** e registros de pagamento para **644 dos 645 municípios** do universo estadual. Esses casos e a diferença de cobertura precisam ser examinados antes de consolidação analítica.
- O campo `natureza_capital_pago` permanece nulo. Na data deste relatório, a publicação ainda não estava autorizada e não houve alteração de produção. A autorização posterior refere-se à divulgação dos resultados agregados desta auditoria; não classifica os fluxos como investimento executado.

## Próximas verificações

1. Inspecionar individualmente os cinco registros negativos e caracterizar os lançamentos zerados, distinguindo ajustes/estornos de pagamentos efetivos.
2. Investigar a diferença entre as coberturas municipais das etapas, incluindo a ausência de registros selecionados de pagamento para um município.
3. Conciliar as chaves e a cronologia entre pagamento, desembolso e convênio, sem somar etapas.
4. Definir e validar a classificação de natureza de capital e a ligação com localização de execução antes de produzir qualquer indicador de investimento territorial.
5. Após a QA, avaliar a agregação regional mantendo explícita a dimensão de município proponente e as limitações de cobertura.

**Estado do staging:** workflow de coleta validado; classificação de capital e localização da execução permanecem pendentes. A autorização posterior para publicar os resultados desta auditoria está registrada no complemento abaixo.


## Auditoria agregada complementar e autorização de divulgação — 27/11/2026

A auditoria foi executada sobre o pacote de staging identificado pelo SHA-256 acima, sem reexportar registros individuais. A execução [GitHub Actions 46015207806](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/46015207806) concluiu com sucesso, verificou a integridade do banco e confirmou a correspondência das contagens com o QA de origem. O resumo agregado foi preservado no R2 com leitura de retorno e no artefato [sp645-transferegov-financial-aggregate-audit](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/46015207806/artifacts/15205168746), sem identificadores de transação ou convênio, nomes de fornecedores, números de linha ou valores individuais.

- Os cinco pagamentos negativos e os 2.194 pagamentos zerados compartilham a categoria genérica “pagamento a favorecido com OBTV”; a categoria não caracteriza estorno ou cancelamento.
- Os cinco pagamentos negativos foram ligados aos campos de documento de liquidação presentes na fonte. Nenhum encontrou pagamento positivo no mesmo documento e convênio, nem contraparte positiva de igual valor no mesmo convênio. Isso não basta para concluir que os lançamentos sejam inválidos ou estornos.
- Pirapora do Bom Jesus é o único município sem evento de pagamento selecionado. O staging contém 13 convênios e dois eventos de desembolso associados ao município, de modo que a lacuna observada é específica da etapa de pagamento.
- Há 22.557 instrumentos presentes nas duas etapas; as distribuições cronológicas foram calculadas apenas como descrição. Pagamento e desembolso continuam sendo etapas distintas e não aditivas.

**Autorização:** foi autorizada a publicação destes resultados agregados e a integração dos agregados municipais ao site. Permanecem fora da divulgação os registros individuais e qualquer afirmação de investimento executado, localização física ou natureza de capital. O branch operacional agora contém o exportador agregado, a página interativa e a etapa correspondente no workflow `pages-sp645-production`. O site de produção ainda não foi atualizado: o workflow implanta uma versão marcada por release, e as alterações precisam integrar um release novo.

**Pendência analítica:** classificar individualmente os cinco pagamentos negativos com documentação oficial complementar e validar natureza de capital e localização antes de qualquer indicador de investimento territorial.
