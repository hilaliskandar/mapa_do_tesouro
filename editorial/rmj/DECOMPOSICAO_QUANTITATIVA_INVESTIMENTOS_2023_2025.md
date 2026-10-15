# Decomposição quantitativa de investimentos da RMJ — 2023–2025

**Data:** 15/10/2026. **Fonte:** extratos da Despesa Detalhada do TCESP, grupo de natureza 44, estágio Valor Liquidado. **Universo:** Cabreúva, Campo Limpo Paulista, Itupeva, Jarinu, Jundiaí, Louveira e Várzea Paulista.

## Decisão metodológica

Analisar prioritariamente dados contábeis já recuperados e conciliados, preservando diligências legais apenas para ambiguidades relevantes que mudem a interpretação. Não tomar a coincidência de código e denominação como identidade de projetos, nem a ausência de código como extinção de política.

Foi elaborado o script `decompor_rmj.py` e duas saídas CSV entregues no chat: `rmj_decomposicao_programas_acoes_2023_2025.csv` (1.169 linhas de diferenças por chave e período, incluindo entradas/saídas) e `rmj_sintese_variacoes_2023_2025.csv` (28 linhas: sete municípios × dois pares de anos × dois níveis, programa e ação).

As chaves usadas são:
- Programa: município, exercício e código de programa, com descrições preservadas em cada ano.
- Ação: município, exercício, código de programa e código de ação, com descrições preservadas em cada ano.

O resultado indica `mesmo_codigo_mesmo_nome`, `mesmo_codigo_nome_alterado`, `somente_ano_inicial` ou `somente_ano_final`. As descrições são comparadas com espaços e acentos normalizados, não por correspondência semântica automática.

A soma das variações individuais de cada conjunto de programas e ações foi confrontada com a diferença de investimentos total do município no período: **28 de 28 verificações fechadas em centavos**.

## Variação nominal do investimento liquidado (R$ milhões, aproximados)

| Município | 2023→2024 | 2024→2025 |
|---|---:|---:|
| Cabreúva | −12,97 | −38,22 |
| Campo Limpo Paulista | +45,12 | −73,09 |
| Itupeva | −29,37 | +1,16 |
| Jarinu | +10,74 | −3,54 |
| Jundiaí | +92,59 | −109,44 |
| Louveira | −24,22 | −53,86 |
| Várzea Paulista | +4,91 | −11,67 |

## Programas associados aos maiores movimentos em 2024→2025

- **Jundiaí:** Mobilidade Total −R$ 59,14 milhões; Município Seguro −R$ 23,49 milhões; Pacto pela Saúde −R$ 14,13 milhões; Cidade Limpa e Bem Cuidada −R$ 13,46 milhões.
- **Campo Limpo Paulista:** Campo Limpo Paulista Sustentável −R$ 57,67 milhões; Humaniza Saúde −R$ 5,31 milhões; Cultura e Turismo Vive −R$ 4,46 milhões.
- **Cabreúva:** Desenvolvimento da Infraestrutura de Governo −R$ 8,25 milhões; Mobilidade Urbana Sustentável −R$ 6,46 milhões; MAC −R$ 5,72 milhões.
- **Louveira:** Programas Habitacionais −R$ 18,03 milhões; Planejamento Urbano −R$ 16,52 milhões; Média e Alta Complexidade Ambulatorial e Hospitalar −R$ 8,82 milhões.
- **Itupeva:** Desenvolvimento e Ordenamento Urbano −R$ 7,09 milhões, compensado parcialmente por Creches e Pré-Escolas com Qualidade +R$ 2,89 milhões; Ensino Fundamental com Qualidade +R$ 2,76 milhões; Humanização e Ampliação da Saúde +R$ 1,55 milhão.
- **Jarinu:** Gestão de Obras e Urbanismo −R$ 5,46 milhões, parcialmente compensada por outras áreas.
- **Várzea Paulista:** Escola do Futuro −R$ 12,93 milhões; Saúde e Qualidade de Vida +R$ 8,70 milhões; Gestão do Avança Várzea Paulista −R$ 6,66 milhões.

## Advertência substantiva

Variações de programa podem refletir cronograma de liquidação, composição ou reclassificação; não demonstram, por si mesmas, ganhos ou perdas de entregas físicas. No par Várzea Paulista 2023→2024 a mudança do programa 40 para 70 deve ser tratada como reorganização de classificação contábil em investigação; a ação 1009 — Construção Novo Hospital aparece nos três exercícios.

## Produto editorial subsequente

Transformar a base em: (1) decomposição dos maiores aumentos e quedas de cada município; (2) concentração por programa e ação e exposição à excepcionalidade; (3) composição dos investimentos, com explicações metodológicas e ligações às fontes já consolidadas. Reutilizar as seções existentes do boletim e submeter alterações públicas a auditorias e testes visuais. Não retomar pesquisa exaustiva de LOA/PPA.
