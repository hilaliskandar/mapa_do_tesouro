# Matriz preliminar de comparabilidade TCESP 2025 × DCA

Base empírica: auditoria integral do ZIP `receitas-2025.zip` TCESP, 896.299 registros, hash SHA-256 `16df083d2088127108957a028f6c824265813c74542f528108526b44a392b84b`; workflow [40240402859](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40240402859), artifact `12616102256`. Inspeção efetiva de `taxonomia.json`.

## Classificação encontrada
Quatro categorias econômicas, 23 subcategorias, 63 fontes, 113 valores em `ds_d1`, 280 em `ds_dd2`, 339 em `ds_d3` e 642 em `ds_tipo`. Há receitas correntes, de capital e intraorçamentárias. Das 896.299 linhas, 896.283 indicam Poder Executivo e 16 Legislativo. **Não somar categorias hierárquicas distintas nem assumir que a mesma designação seja sempre equivalente ao campo da DCA.**

## Códigos TCESP identificados e candidatos a confrontação

| Variável DCA | Código integral em `ds_tipo` (8 primeiros dígitos) | Denominação fonte | Quantidade de registros TCESP | Critério |
|---|---|---|---:|---|
| `dca_iptu_principal` | `11125001` | IPTU - Principal | 12.792 | Comparar somente principal |
| `dca_itbi_principal` | `11125301` | ITBI - Principal | 10.305 | Comparar somente principal |
| `dca_iss_principal` | `11145111` | ISSQN - Principal | 13.056 | Comparar somente principal |
| `dca_fpm_cota_mensal` | `17115111` | FPM - Cota Mensal - Principal | 18.337 | Excluir cotas distintas |
| `dca_icms_cota_parte` | `17215001` | Cota-parte do ICMS - Principal | 17.743 | Examinar estágio bruto/líquido |
| `dca_ipva_cota_parte` | `17215101` | Cota-parte do IPVA - Principal | 17.974 | Examinar estágio bruto/líquido |

**Nota:** As quantidades são registros para todo o universo TCESP 2025, não municípios, tampouco valores monetários.

## Controles exigidos para comparação
1. Identificar a receita pela chave `ds_tipo` com código de oito dígitos e não por correspondência textual imprecisa.
2. Somar `vl_arrecadacao` em centavos por município/ano/rubrica, conservando retificações negativas.
3. Vincular município ao código IBGE pela tabela homologada, com a grafia Florínea (3516101), sem perder a origem nominal no TCESP.
4. Examinar `ds_orgao` e `ds_poder` antes de concluir equivalência de universo institucional; verificar deduções, FUNDEB, restituições, receitas intraorçamentárias, estágio contábil e classificações bruta/líquida entre fontes.
5. Diferenciar divergência real de diferença conceitual; não transformar ausência em zero nem sobrescrever DCA.
6. Registrar diferenças em reais/centavos e razão TCESP/DCA; manter os resultados apenas em ambiente de auditoria até homologação.

## Estado
**A identificação dos códigos é empiricamente confirmada no arquivo TCESP. A equivalência integral de definição contábil com os campos DCA ainda é hipótese a testar**, não homologação. Não houve ingestão ou alteração do SQLite/API ou R2.
