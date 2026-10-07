# QA — Engenheiro Coelho 2024 — DCA

Data da verificação: 2026-10-07

## Achado

Para o município de Engenheiro Coelho, código IBGE 3515152, exercício 2024, a planilha canônica multifuentes contém uma linha estrutural na aba `Base multifuentes`, mas todos os campos DCA usados pelo pipeline estão nulos.

Na aba `Cobertura`, o mesmo município-ano registra:

- Receitas — registros: 0
- Despesas — registros: 0
- Funções — registros: 0

Nas abas de origem `Receitas`, `Despesas` e `Despesa por função`, a linha de Engenheiro Coelho 2024 contém município e ano, sem registros financeiros preenchidos.

Apesar disso, a aba `Base multifuentes` registra:

- `dca_status_nucleo = "OK"`
- `tem_dca_30m = "SIM"`

Essas duas flags são inconsistentes com o conteúdo efetivamente disponível para o município-ano.

## Efeito sobre a base analítica

O importador canônico não usa `dca_status_nucleo` nem `tem_dca_30m` para fabricar valores. Cada variável DCA é importada individualmente. Campo vazio dentro da janela de disponibilidade é classificado como `ausente`, com valor nulo.

Portanto, a base analítica publicada não transforma a ausência DCA de Engenheiro Coelho 2024 em zero e não considera os campos vazios como observados.

## Decisão

1. Manter os valores DCA de Engenheiro Coelho 2024 como `ausente`.
2. Não imputar valores.
3. Não alterar RREO, RGF ou RGF02 de 2024, que possuem registros independentes.
4. Tratar `dca_status_nucleo` e `tem_dca_30m` como flags de integração defeituosas para este caso.
5. Corrigir essas flags na próxima geração da planilha multifuentes, usando presença efetiva de registros/valores como condição, não mera existência da linha estrutural.

## Regra recomendada para regeneração

Para cada município-ano:

- `tem_dca_30m = "SIM"` somente quando houver pelo menos um registro DCA efetivo nas bases de receitas, despesas ou funções;
- `dca_status_nucleo = "OK"` somente quando o conjunto mínimo definido para o núcleo DCA estiver observado segundo a regra de cobertura;
- uma linha estrutural sem registros deve resultar em ausência, nunca em presença.

Este documento é diagnóstico de QA. Ele não substitui nem corrige silenciosamente a fonte canônica.
