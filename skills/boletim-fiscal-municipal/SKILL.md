---
name: boletim-fiscal-municipal
description: Gera boletins fiscais municipais auditáveis a partir da API editorial estática do projeto Finanças Municipais SP. Use quando o usuário pedir ficha, boletim, análise fiscal ou publicação de um município dentro de um dos 11 universos editoriais (9 regiões metropolitanas, AU de Franca ou Cidades Médias), com comparação intragrupo, séries históricas, posição relativa, cobertura e cautelas metodológicas.
---

# Boletim fiscal municipal

Produzir uma ficha fiscal municipal comparativa usando o contexto já calculado pela API editorial. Não refazer indicadores oficiais ou harmonizações fora do payload.

## Fluxo

1. Identificar `publication_id` e `codigo_ibge`.
2. Obter o contexto municipal em `.../data/api/v1/publication/universes/{publication_id}/municipalities/{codigo_ibge}.json`.
3. Validar o payload. Se houver arquivo local, executar `scripts/validate_context.py municipality <arquivo>`.
4. Ler `references/api.md` para os campos e `references/editorial.md` para as regras de redação.
5. Produzir a ficha usando somente fatos sustentados pelo payload.
6. Informar explicitamente período, universo de comparação e cobertura relevante.
7. Não tratar ausência como zero. Não converter ranking, quartil, percentil ou CAPAG em julgamento normativo.

## Estrutura padrão

# Boletim fiscal de [Município]

## Síntese
Apresentar 4–7 achados descritivos, priorizando mudanças relevantes e posição intragrupo.

## Receitas e autonomia
Cobrir receita corrente, receita tributária, IPTU, ITBI, ISS e transferências quando observados. Diferenciar valores absolutos de participações relativas.

## Despesas e investimento
Cobrir despesa total/corrente, pessoal, investimento e despesas de capital quando disponíveis.

## Território
Cobrir Urbanismo, Habitação, Saneamento, Gestão Ambiental e Transporte com a regra estrita de disponibilidade do projeto.

## Dívida, liquidez e CAPAG
Usar RCL, DTP/RCL, DC/RCL, DCL/RCL, caixa e CAPAG somente quando observados e conforme a fonte oficial indicada no payload.

## Posição no universo
Comparar com mediana, quartis e posição relativa do `publication_id`. Explicar que a posição é contextual ao grupo.

## Trajetória
Usar a série histórica disponível. Não interpolar anos ausentes.

## Fontes, cobertura e cautelas
Registrar universo, anos disponíveis, fonte preferencial e lacunas materiais.

## Regras obrigatórias

- Preservar a distinção entre `observado`, `ausente`, `nao_aplicavel` e `em_revisao`.
- Não inventar valores para variáveis ausentes.
- Não substituir indicadores legais por proxies.
- Tratar `saldo_corrente_simplificado` e outros agregados analíticos como tais; não chamá-los de resultado orçamentário oficial.
- Para Cidades Médias, usar as 33 cidades como grupo de comparação, inclusive as que também pertencem a RM/AU.
- Para RMSP, usar o universo editorial de 38 municípios; a capital está deliberadamente excluída desse comparativo.
- Quando o mesmo município aparecer em dois universos, produzir leituras separadas; os valores básicos podem ser iguais, mas percentis, quartis e diferenças para a mediana pertencem ao universo selecionado.
