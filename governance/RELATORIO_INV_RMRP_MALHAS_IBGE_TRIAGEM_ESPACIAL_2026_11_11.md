# INV-RMRP — Territorialização preliminar Obrasgov e pipeline de prévia consultável

**Data:** 11/11/2026. **PR:** nº 233 (draft). **Objetivo:** tornar consultas exploratórias por município operacionalmente verificáveis, sem incorporar valores de investimento previsto às séries de despesa pública executada.

## 1. Dados espaciais oficiais recuperados

A lista de 34 códigos IBGE7, anteriormente conferidos na API de localidades do IBGE, foi usada para recuperar as geometrias pelo endpoint oficial:
`https://servicodados.ibge.gov.br/api/v3/malhas/municipios/{IBGE7}?formato=application/vnd.geo%2Bjson&qualidade=maxima`.

Foram obtidos **34/34 GeoJSON**, cada um com `properties.codarea` coincidente com a chave solicitada e sem duplicação de IBGE. Originais organizados em cinco lotes:
`governance/inv_rmrp_malhas_ibge/parte_01_2026_11_11.geojson` a `parte_05_2026_11_11.geojson`.
Coleção unificada: [malhas IBGE 34 municípios](INV_RMRP_MALHAS_IBGE_MAXIMA_34_2026_11_11.geojson). Geometria da API é referenciada em WGS84 (longitude, latitude, `EPSG:4326`). **Qualidade máxima é a maior oferecida pelo serviço API, mas ainda pode conter generalização cartográfica**; não tratar como a geometria vetorial mais detalhada possível de todas as bases IBGE, nem substituir os limites oficiais canônicos do projeto (EPSG:4674) sem uma etapa de compatibilização. Nenhuma simplificação adicional foi realizada pelo processamento.

## 2. Primeiro teste de interseção geográfica

A amostra de 224 projetos Obrasgov, obtida antes por busca textual `desc_nome` em nomes dos 34 municípios, foi submetida a ponto-no-polígono com os pontos da própria API (`pins`). Foram respeitados `Polygon` e `MultiPolygon` com anéis internos.

| Estado | Projetos |
|---|---:|
| Coordenadas de ao menos um ponto dentro de exatamente um município RMRP | **130** |
| Coordenadas com interseção em dois ou mais municípios RMRP | **1** |
| Coordenadas existentes, mas fora das 34 malhas consultadas | **61** |
| Sem coordenadas numéricas utilizáveis | **32** |
| **Total de candidatos nominais** | **224** |

**Sete divergências** entre município citado no título e interseção geométrica. Os casos precisam de revisão documental e da qualidade do georreferenciamento, não de correção automática de título, município ou valor. Exemplos:
- Barrinha no título e Sertãozinho no ponto (`23598.35-24`; `9118.35-82`);
- estabelecimento com denominação Alberto Santos Dumont em Ribeirão Preto, mas capturado em busca por Dumont (`64670.35-86`; `138992.35-29`);
- escola com Guariba no título, coordenada em Barrinha (`37841.35-64`);
- intervenção de Jaboticabal com coordenada em Sertãozinho (`27846.35-46`);
- videomonitoramento em Ribeirão Preto, coordenada em Altinópolis (`25904.35-94`).

**Importante:** o conjunto de 224 é uma amostra por nome; os 61 pontos fora e os 32 sem ponto mostram problemas de precisão/cobertura, mas não autorizam inferir que 93 projetos estejam necessariamente fora da RMRP ou sejam inválidos. A interseção classifica a posição declarada do ponto, não a identidade juridicamente comprovada do local da obra.

Artefatos: [matriz detalhada 224](INV_RMRP_OBRASGOV_224_TRIAGEM_ESPACIAL_2026_11_11.json), [malhas completas por API](INV_RMRP_MALHAS_IBGE_MAXIMA_34_2026_11_11.geojson), [JSON próprio da prévia](../app/static/data/api/v3/investimentos/rmrp/obrasgov-triagem-espacial.json).

## 3. Pipeline de ingestão Obrasgov sob QA

Foi preparado o script [`pipeline/acquire/collect_obrasgov_sp_rmrp.py`](../pipeline/acquire/collect_obrasgov_sp_rmrp.py) para **captura integral de SP por páginas de 200** com armazenamento original em `gzip`, hash dos bytes de origem, verificação dos contadores declarados, bloqueio de IDs duplicados, retomada após interrupção e espera exponencial para HTTP 429/503. Foram incluídos [testes offline](../pipeline/acquire/test_collect_obrasgov_sp_rmrp.py), junto ao QA do coletor Transferegov [`pipeline/acquire/collect_investimentos_rmrp.py`](../pipeline/acquire/collect_investimentos_rmrp.py) e seus testes. **Os testes sintáticos e unitários executados na PR passaram**, sem chamadas à API, no workflow INV RMRP QA.

**Limitação operacional nesta rodada:** tentativa de paginação de Obrasgov em uma sessão ampla excedeu o tempo da ferramenta, sem gerar snapshot. Uma tentativa posterior recebeu HTTP 429 por limitação do serviço intermediário de navegação. O único lote explicitamente completado em sessão foi a leitura de dez páginas, **2.000 registros SP**, com 281 pontos no retângulo aproximado pesquisado; o conteúdo das dez páginas **não foi persistido integralmente**. Nenhuma contagem de 20.942 registros deve ser interpretada como censo concluído. O coletor ainda necessita de execução integral em ambiente com acesso HTTP e staging persistente.

## 4. Consulta de prévia e alteração isolada na publicação

Foi atualizada a página [`app/static/obrasgov-rmrp-preview.html`](../app/static/obrasgov-rmrp-preview.html): seleção por município do polígono, estado de QA espacial, situação cadastral, fonte prevista e texto. O arquivo JSON da prévia diferencia `MUNICIPIO_CONFIRMADO_POR_POLIGONO`, `MULTIPLOS_MUNICIPIOS_POR_PONTOS`, `FORA_DAS_MALHAS_RMRP` e `SEM_PONTO`. Em nenhum caso a interface soma valores previstos como execução.

O materializador ordinário de Cloudflare Pages (`deployment/materialize_preview.py`) copiava somente `index.html`, `styles.css` e `app.js`, excluindo as novas páginas e arquivos JSON. A solução adotada **não altera a lógica de produção**: uma sobreposição específica para **PR #233** foi implementada em [`deployment/materialize_investimentos_preview.py`](../deployment/materialize_investimentos_preview.py), com QA local e remoto em [`deployment/qa_investimentos_preview.py`](../deployment/qa_investimentos_preview.py), acrescentando explicitamente dois HTML e dois JSON apenas no build da PR 233. O workflow `.github/workflows/pages-preview.yml` recebeu condição `pull_request.number == 233`. Essa ação produz uma **prévia separada**, não um merge ou publicação do painel principal. A validação remota dessa alteração deve ser registrada somente após o workflow passar.

## 5. Gates obrigatórios antes de homologação

1. **Censo Obrasgov/SP:** executar aquisição integral por páginas, verificar `total_items`, `total_pages`, unicidade e hash/readback de todas as páginas; documentar 429, retries e retificações.
2. **Vínculo territorial:** cruzar todos os pontos de SP com o cadastro vetorial municipal oficialmente adotado pelo projeto; tratar projetos sem ponto, pontos genéricos e intervenções regionais. Separar localização confirmada, candidata e inconclusiva.
3. **Transferegov:** executar aquisição de 34 municípios (Parcerias + Discricionárias/Legais) com armazenamento integral e manifesto. As 7.153 propostas lidas na varredura de categorias **não foram arquivadas integralmente**.
4. **Fluxos financeiros:** adquirir transferências especiais, convênios, empenhos e ordens bancárias, além de liberações estaduais SIAFEM, por documento e período, sem inferir pagamento da existência de projeto ou instrumento.
5. **SQLite desenvolvimento:** testar extensões, chaves e filtros; manter `tcesp_investimento_*` intactas e revisar aglomeração regional e prevenção de dupla contagem.
6. **Consulta:** homologar interface, exigir 34 IBGE e 50 filtros, conferir ausência/zero, acesso público à fonte e estado de qualidade, antes de produção.

**Status:** aquisição espacial oficial 34/34 concluída, triagem de 224 candidatos concluída e QA de coletores offline aprovado; **censo estadual, comprovação financeira, ingresso em banco canônico e homologação do painel não realizados**. FED04/PR #232 preservados.
