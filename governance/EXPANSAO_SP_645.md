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


## Piloto estadual de escala

Foi preparado um primeiro snapshot estadual para testar a infraestrutura com os 645 municípios sem alterar a semântica do painel publicado.

Características do piloto:

- 645 municípios;
- exercícios 2020–2023;
- 2.580 pares município-ano;
- cinco variáveis de receita compatíveis com o contrato atual: receita corrente, receita tributária, IPTU, ITBI e ISS;
- armazenamento do snapshot em objeto privado;
- manifesto público com tamanho e SHA-256 de cada parte, hash do arquivo comprimido e hash do CSV descomprimido;
- ingestão esperada de 12.900 observações e 12.900 registros de proveniência.

O piloto não inclui despesas. O ativo estadual disponível usa despesa empenhada reconstruída, enquanto variáveis centrais do painel vigente usam despesa liquidada. Misturar os estágios violaria o contrato semântico.

Também não inclui população, RREO, RGF, RGF02 ou CAPAG. Esses componentes deverão ser incorporados somente quando houver fonte estadual compatível e auditada.

## Fonte privada e reconstrução automatizada

Snapshots canônicos de dados podem ser mantidos em armazenamento privado, enquanto o GitHub conserva apenas:

- código de ingestão;
- mappings;
- manifestos de integridade;
- definições metodológicas;
- testes;
- hashes e metadados de proveniência.

O workflow de prova estadual:

1. obtém o snapshot privado com credencial de leitura do CI;
2. verifica SHA-256 de cada parte;
3. recompõe e valida o arquivo comprimido;
4. valida o SHA-256 do CSV;
5. confere 645 municípios, anos, colunas e unicidade município-ano;
6. converte o recorte para o formato aceito pelo importador;
7. carrega o SQLite com `universo_id=SP_645`;
8. valida contagens de observações, cobertura e proveniência;
9. preserva o SQLite apenas como artefato temporário do GitHub Actions.

O nome do bucket, credenciais e demais parâmetros operacionais privados não são versionados no repositório.

## Distinção entre piloto e baseline estadual

O piloto 2020–2023 é uma prova de escala e de infraestrutura. Ele não é uma release estadual e não deve substituir o baseline TIC-TIM 30.

A primeira release estadual exige ainda uma base multifuentes 2013–2025 com o mesmo contrato conceitual do baseline, incluindo os demonstrativos oficiais necessários, cobertura variável a variável e QA de paridade.
