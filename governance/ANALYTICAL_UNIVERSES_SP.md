# Universo analítico Cidades Médias

Data de registro: 2026-10-09.

## Definição

`CIDADES_MEDIAS` é um universo analítico composto exatamente pelos 33 municípios fornecidos pelo usuário como camada canônica do corpus Cidades Médias.

A denominação é tratada como rótulo do corpus. Este catálogo não infere nem aplica automaticamente um critério populacional ou demográfico para classificar municípios como cidades médias.

## Composição

O universo contém 33 municípios paulistas, identificados por código IBGE em `data/catalogs/analytical_universes_sp.yml`.

## Sobreposição com universos existentes

- 5 dos 33 municípios também pertencem ao `TIC_TIM_30`: Americana, Hortolândia, Indaiatuba, Jundiaí e Sumaré.
- 11 pertencem à RM de São Paulo.
- 4 pertencem à RM da Baixada Santista.
- 4 pertencem à RM de Campinas.
- 2 pertencem à RM do Vale do Paraíba e Litoral Norte.
- 1 pertence à RM de São José do Rio Preto.
- 1 pertence à RM de Jundiaí.
- 3 pertencem à RM de Piracicaba.
- 1 pertence à AU de Franca.
- 0 pertencem à RM de Sorocaba.
- 0 pertencem à RM de Ribeirão Preto.
- 6 não pertencem a nenhum dos dez recortes metropolitanos catalogados: Araçatuba, Araraquara, Bauru, Marília, Presidente Prudente e São Carlos.

Os totais metropolitanos acima são mutuamente exclusivos na composição territorial de 2025 já catalogada.

## Regra de modelagem

O universo usa a mesma relação muitos-para-muitos de `universo_municipio`. Um município pode pertencer simultaneamente a `SP_645`, `CIDADES_MEDIAS`, `TIC_TIM_30` e a um recorte metropolitano, sem duplicar observações fiscais.

Estatísticas relativas, tipologias, marcadores e pares devem ser calculados especificamente para `CIDADES_MEDIAS` quando esse universo estiver selecionado no painel.
