# Política de persistência analítica

## Regra geral

A base canônica distingue quatro níveis:

1. **observação oficial** — valor recebido de fonte oficial ou artefato integrado validado;
2. **agregação analítica** — combinação determinística de observações;
3. **indicador derivado/legal** — razão, valor per capita ou indicador oficial;
4. **avaliação relativa** — estatística de janela, tipologia, marcador ou relação entre municípios.

## Persistência

### Tabela `observacao`

Recebe contas oficiais, classificações oficiais, agregações analíticas e indicadores anuais quando seu valor está associado a um município-ano.

### Tabela `estatistica_janela`

Recebe resultados temporais como média, CV, mudança, amplitude, persistência relativa e posição pela média.

### Tabela `classificacao_relativa`

Recebe nível relativo, estabilidade e quadrante para cada dimensão e janela.

### Tabela `par_municipal`

Recebe relações dirigidas entre municípios, cobertura comparável, coincidências, prioridade e reciprocidade.

## Recalcular ou importar?

Resultados derivados devem ser **recalculados pelo pipeline** a partir das observações canônicas. Os valores dos workbooks legados serão usados como baseline de regressão.

Essa política evita que uma fórmula antiga e um valor persistido divergente coexistam silenciosamente.
