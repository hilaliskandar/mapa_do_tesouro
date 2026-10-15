# Conciliação externa das séries RMJ contra a base DCA

Data: 15/10/2026

## Fonte conferida

Arquivo `DCA_SP_645_2013_2025_CANONICO.csv`, Google Drive ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, última atualização informada pelo Drive em 08/10/2026. SHA-256 do arquivo recuperado: `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`.

## Resultado da confrontação independente

- Universo: sete municípios da RM de Jundiaí, exercícios de 2021 a 2025.
- Chaves de confronto: `cod_ibge` + `ano` na base DCA e `id` + `ano` nas duas séries incorporadas ao HTML.
- Séries verificadas: `historical` (3 colunas fiscais) e `extra` (12 colunas fiscais).
- Registros município-ano: 35.
- Campos fiscais distintos: 15.
- Comparações monetárias: 525.
- Divergências superiores a R$ 0,01: **zero**.
- Critério: igualdade de valores nulos e diferença absoluta até R$ 0,011, para absorver apenas representação numérica de centavos. Ausência em uma base e presença na outra constitui divergência.

A auditoria ocorreu contra o conteúdo efetivamente recuperado do Drive e a versão de `editorial/rmj/index.html` na `main` em 15/10/2026. Os cálculos foram executados em leitura independente no conector, sem utilizar o código de indicadores da página como referência.

## Reprodutibilidade

Executar a ferramenta `python3 editorial/rmj/audit_against_dca_csv.py /caminho/arquivo.csv` após obter o CSV verificado. O CSV não deve ser incorporado ao repositório apenas para satisfazer o teste; a proveniência e a atualização da fonte exigem verificação explícita.

## Limites

O resultado demonstra fidelidade das 525 células aos valores do arquivo estadual consultado, e não atesta a exatidão das declarações contábeis de origem, a correção da classificação DCA ou a integridade de todos os registros de TCESP. Não avalia relações causais, programas, contratos ou entregas físicas. O controle numérico interno `audit_derived.py` e esta verificação contra arquivo externo têm finalidades distintas.
