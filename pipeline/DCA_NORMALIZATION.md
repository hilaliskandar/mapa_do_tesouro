# Normalização DCA canônica v1

A normalização converte artefatos brutos da DCA/SICONFI em variáveis canônicas sem misturar estágios de execução ou natureza orçamentária.

## Fontes usadas

- Anexo I-C: receitas orçamentárias;
- Anexo I-D: despesas por natureza;
- Anexo I-E: despesas por função.

## Regras centrais

Receitas usam somente `Receitas Brutas Realizadas` e somente contas `RO...`. Contas `RI...` não entram nos agregados canônicos desta camada.

Despesas usam somente `Despesas Liquidadas`. Não há soma de empenhado, pago ou restos a pagar.

Funções usam a linha da função inteira, por exemplo `15 - Urbanismo`. Subfunções como `15.452 - Serviços Urbanos` não são somadas para reconstruir o total da função.

Cada variável deve encontrar exatamente uma linha compatível:

- 1 correspondência: `observado`, usando o valor da linha;
- 0 correspondências: `ausente`, valor nulo;
- mais de 1 correspondência: `em_revisao`, valor nulo e ocorrência de QA.

A população é aceita somente quando os artefatos consultados convergem para um único valor. Divergência de população produz `em_revisao`.

## Crosswalk

O crosswalk versionado está em:

`data/mappings/dca_canonical_v1.yml`

Ele registra explicitamente anexo, coluna, rótulo e conta oficial. Para funções, também registra o padrão do código funcional.

## Estado atual

A versão v1 cobre as variáveis DCA usadas pela base multifuentes atual:

- receitas correntes e tributárias;
- IPTU, ITBI e ISS;
- FPM, ICMS e IPVA;
- operações de crédito, alienação de bens e transferências de capital;
- despesa total e corrente liquidada;
- pessoal e encargos, juros, investimentos, inversões financeiras e amortização;
- Saúde, Educação, Urbanismo, Habitação, Saneamento, Gestão Ambiental e Transporte;
- população DCA.

Essa camada ainda não incorpora RREO, RGF ou CAPAG. Esses blocos permanecem separados.
