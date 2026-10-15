# Comparação entre programas de investimento da RMJ — 2023 e 2024
Data: 15/10/2026

Fonte: artefato GitHub Actions `11680818755`, contendo 14 arquivos de auditoria TCESP (`municipio_2023.json`, `municipio_2024.json`) e seus `sha256_zip`, URLs de origem e somatórios em centavos. Contas: despesas liquidadas do grupo 44; não usar empenhos ou pagamentos.

| Município | 2023 (R$ mi) | 2024 (R$ mi) | Diferença (R$ mi) |
|---|---:|---:|---:|
| Cabreúva | 70,24 | 57,27 | -12,97 |
| Campo Limpo Paulista | 37,92 | 83,04 | +45,12 |
| Itupeva | 48,17 | 18,80 | -29,37 |
| Jarinu | 4,19 | 14,93 | +10,74 |
| Jundiaí | 154,18 | 246,77 | +92,59 |
| Louveira | 94,37 | 70,15 | -24,22 |
| Várzea Paulista | 58,20 | 63,12 | +4,91 |

Valores acima arredondados, variações em milhões calculadas sobre totais não arredondados. Todos os 14 casos já foram conciliados com a DCA na auditoria anterior.

## Primeiro quadro explicativo por programas

- Jundiaí: Mobilidade Total (código 187) 67,37 → 128,79 milhões, variação +61,42 milhões. Identificação por mesmo código e nome, não prova física de obras.
- Campo Limpo Paulista: Campo Limpo Paulista Sustentável (código 9) 26,01 → 65,68 milhões, variação +39,67 milhões.
- Itupeva: Desenvolvimento e Ordenamento Urbano (código 4) 28,03 → 13,34 milhões, variação -14,69 milhões.
- Jarinu: Gestão de Obras e Urbanismo (código 8) 2,90 → 13,47 milhões, variação +10,57 milhões.
- Cabreúva: Desenvolvimento da Infraestrutura (código 5003) 18,27 → 10,45 milhões, variação -7,82 milhões.
- Louveira: Planejamento Urbano (código 13) 29,26 → 21,51 milhões, variação -7,75 milhões.
- Várzea Paulista: o código 40 (Gestão da Média e Alta Complexidade) aparece em 2023 com 35,43 milhões e não continua com o mesmo código em 2024; o código 70 (Saúde e Qualidade de Vida) aparece em 2024 com 35,06 milhões. **Não inferir surgimento/desaparecimento de gasto** sem conferir a equivalência de programas e ações nas LOAs, LDOs e PPAs.

## Encaminhamento metodológico

1. Examinar os programas completos e as ações em 2023–2024 para todos os municípios, preservando codigo, descrição, exercício e valor.
2. Criar um quadro de correspondências com situações `codigo_nome_estaveis`, `renumeracao_possivel`, `mudanca_de_escopo` e `sem_correspondencia_verificada`; equivalência de programas não deve ser automatizada pelo nome.
3. Recuperar a tabela completa por programas e ações de 2025. A versão pública atual contém totais conciliados e destaques, não uma matriz trienal completa.
4. Separar variação contábil por programa, identificação de contrato e aferição de entrega física.

Relatório analítico detalhado e reproduzível elaborado neste ciclo: `COMPARACAO_PROGRAMAS_RMJ_2023_2024.md`, gerado como arquivo entregue no chat. Nenhuma alteração foi realizada no boletim público.
