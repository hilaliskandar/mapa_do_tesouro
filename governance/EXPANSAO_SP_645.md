# Preparação para expansão aos 645 municípios de São Paulo

## Objetivo

Permitir que o mesmo pipeline usado no universo TIC-TIM 30 processe outros universos municipais, inclusive o conjunto dos 645 municípios paulistas, sem duplicar código ou alterar a semântica dos indicadores.

## Mudanças estruturais desta etapa

- o mapping declara explicitamente o universo de carga;
- o importador aceita universo definido no mapping ou sobrescrito por parâmetro;
- o orquestrador propaga o universo efetivamente importado para estatísticas, tipologias, marcadores, pares, exportação estática e cartografia;
- o SQLite continua armazenando todos os pares dirigidos para auditoria;
- o JSON municipal publica apenas pares com `ordem_prioritaria`, que são os únicos consumidos pela interface.

## Escala esperada

Para um universo com 645 municípios, a tabela analítica de pares pode conter até:

`645 × 644 = 415.380` pares dirigidos por janela.

Esse volume é aceitável para SQLite e processamento em lote, mas não deve ser replicado integralmente nos arquivos JSON municipais. Com `top_n=3`, o payload público passa a conter no máximo 1.935 pares prioritários no conjunto do estado.

## Condições ainda necessárias antes da primeira carga estadual

1. produzir uma base multifuentes estadual com cobertura e hashes próprios;
2. criar um mapping estadual, por exemplo com `universe.id = SP_645`;
3. validar a cartografia dos 645 códigos IBGE;
4. revisar tempo e memória do cálculo de pares em escala estadual;
5. definir se as medianas e tipologias estaduais devem usar todos os 645 municípios ou universos estratificados adicionais;
6. manter o universo TIC-TIM 30 como baseline de regressão.

Esta etapa não altera o baseline publicado de 30 municípios.
