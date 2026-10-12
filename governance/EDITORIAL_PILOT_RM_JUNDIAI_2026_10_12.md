# Caderno-piloto editorial 01 — Região Metropolitana de Jundiaí

Data de consulta: 2026-10-12. Estado: RASCUNHO ANALÍTICO — NÃO PROMOVIDO.

## Referências canônicas

- Contrato: https://finbra-tic-tim-referencia.pages.dev/data/api/v1/publication/contract.json
- Universo: https://finbra-tic-tim-referencia.pages.dev/data/api/v1/publication/universes/RM_JUNDIAI/context.json
- Municípios: https://finbra-tic-tim-referencia.pages.dev/data/api/v1/publication/universes/RM_JUNDIAI/municipalities.json
- Release: v0.4.0; build_id: multifuentes-v0.4-cef702e5edbd.
- SHA-256 da origem declarada: cef702e5edbdd8bd8d779f81ce246156dab78ee94101e6932f75d375737f71c3.
- Atenção: metadados do contrato e do contexto continuam com qa_status=candidate, apesar da release publicada. Verificar e retificar apenas após comprovação do gate adequado.

## Universo

Sete municípios: Cabreúva (3508405), Campo Limpo Paulista (3509601), Itupeva (3524006), Jarinu (3525201), Jundiaí (3525904), Louveira (3527306) e Várzea Paulista (3556503).

## Síntese preliminar — 2025

| Variável da API | Soma dos observados (R$ correntes) | Cobertura |
|---|---:|---:|
| dca_receita_corrente_bruta | 7.384.124.943,98 | 7/7 |
| dca_receita_tributaria_bruta | 2.141.085.032,54 | 7/7 |
| dca_despesa_total_liquidada | 6.606.003.131,26 | 7/7 |
| dca_despesa_corrente_liquidada | 6.174.459.378,41 | 7/7 |
| dca_investimentos_liquidada | 265.425.559,07 | 7/7 |
| dca_iptu_principal | 512.449.647,25 | 7/7 |
| dca_itbi_principal | 207.539.523,79 | 7/7 |
| dca_iss_principal | 846.718.165,52 | 7/7 |
| rreo_rcl_oficial | 6.217.920.407,26 | 7/7 |
| dca_func_urbanismo_liquidada | 555.071.897,43 | 7/7 |
| dca_func_habitacao_liquidada | 27.941.567,75 | 3/7 |
| dca_func_saneamento_liquidada | 44.706.209,18 | 3/7 |
| dca_func_transporte_liquidada | 13.972.196,74 | 3/7 |
| despesa_territorial | 85.843.429,96 | 1/7 |

Valores transcritos da API para fins de editorialização. As somas só representam os municípios observados; cobertura parcial não autoriza extrapolação aos sete municípios.

CAPAG (2025 no contrato): A+ = 1; A = 2; B = 1; C = 3, cobertura 7/7. O texto editorial deve distinguir ano-base e posição do snapshot (setembro de 2026, conforme governança), evitando atribuir à classificação uma vigência temporal não comprovada.

## Interpretação técnica preliminar

Em 2025, a receita tributária bruta equivale a aproximadamente 29,0% da receita corrente bruta somada nos sete municípios, proporção agregada que não equivale à média dos percentuais municipais. A despesa liquidada é um estágio contábil, e não deve ser comparada mecanicamente à receita como resultado orçamentário apurado.

A cobertura das funções territoriais é heterogênea. O indicador strict_complete de despesa territorial apresenta apenas 1/7 observado, situação insuficiente para caracterizar a região ou estabelecer ranking territorial. As categorias CAPAG devem ser apresentadas como classificações oficiais, não estimadas.

## Verificações editoriais obrigatórias antes da edição de referência

1. Resolver a contradição entre release pública v0.4.0 e qa_status=candidate, verificando o alcance exato do campo.
2. Validar orientação de apresentação das unidades "percentual": valores da API como 0.0314 ou 0.1929 parecem frações de 1, apesar da unidade catalogada. Não converter/publicar percentuais sem verificação do contrato de escala.
3. Examinar campos metodológicos ausentes ou nulos: cautelas e como_ler constam como null em variáveis inspecionadas.
4. Conferir proveniência em nível de variável e vínculo com as fontes primárias.
5. Gerar as fichas municipais a partir dos contextos de cada município, sem recalcular classificações oficiais.
6. Submeter interpretação e títulos a QA editorial: nenhuma ausência tratada como zero, nenhuma ordenação como mérito, e nenhuma soma parcial chamada de total regional.

## Encaminhamento

O próximo artefato editorial é uma Edição de Referência intrarregional que combine síntese da RM Jundiaí, comparação municipal com cobertura explícita, notas de método e links para a fonte original. Este documento não substitui a série analítica canônica nem constitui release publicada.
