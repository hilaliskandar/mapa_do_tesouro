# Aplicação

Frontend static-first e camada opcional de API. O núcleo da interface não deve depender de configuração específica da Cloudflare.


## Contrato documental da interface

A interface não deve duplicar definições em HTML/JavaScript. O build gera:

```text
/data/catalog/variables.json
/data/catalog/variables/{variavel_id}.json
/data/methodology/index.json
/data/methodology/{secao_id}.json
/data/references.json
```

Cartões, tabelas, gráficos e mapas devem oferecer um link contextual para a documentação da variável. A rota humana poderá ser `/indicadores/{id}` ou `/variaveis/{id}`, mas o conteúdo deverá vir deste catálogo estático.
