# Frontend candidate 0.1

## Escopo

Primeira interface do novo núcleo de Finanças Municipais SP.

### Funcionalidades presentes

- seleção de município;
- seleção de exercício;
- seleção de indicador/conta;
- panorama municipal;
- cartões de indicadores prioritários;
- série histórica SVG;
- tabela da série;
- comparação anual ordenada;
- mapa temático municipal;
- dicionário de 75 objetos documentados;
- metodologia navegável;
- modal “Como ler” com fórmula, componentes, fonte, período, interpretação, limitações e regra de ausência.

### Arquitetura

A interface consome exclusivamente artefatos estáticos produzidos pelo pipeline.

Não depende, no uso básico, de:

- Cloudflare Worker;
- D1;
- R2;
- GitHub;
- APIs fiscais externas;
- bibliotecas JavaScript externas;
- serviços de mapas externos.

### Cartografia

A fonte cartográfica é pinada por commit no catálogo de cartografia e filtrada durante o build. Apenas as geometrias do universo ativo são publicadas.

### Status

**candidate**

A promoção exige:

1. CI verde;
2. inspeção visual local;
3. verificação de pelo menos um município em cada grupo de cobertura;
4. conferência de formatos monetários e percentuais;
5. conferência de links documentais;
6. mapa sem geometrias faltantes;
7. nenhuma dependência externa inesperada no runtime.
