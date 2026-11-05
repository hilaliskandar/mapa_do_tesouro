# RMRP — Fechamento G1-3: conciliação da série DCA de despesas liquidadas, 2023–2025

**Data:** 05/11/2026. **Status:** coleta nominal 2023–2025 concluída; deflação, indicadores per capita e QA dos mapas ainda pendentes. **Volume II Lote 98 preservado.**

## Fontes e método
- 2023–2024: [CSV integral — DCA Anexo I-D](G13_DESPESAS_INVESTIMENTOS_2023_2024_34_MUNICIPIOS_COMPLETO.csv), extração de 68 pares município-ano diretamente da API do Siconfi pelo Crawl2AI, com URLs individuais; colunas `Despesas Liquidadas`, contas `DO3.0.00.00.00.00` e `DO4.4.00.00.00.00`.
- 2025: base já conferida no fechamento [G1-3 anterior](FECHAMENTO_G13_AUDITORIA_DESPESAS_2025_2026_11_05.md), CSV no Drive ID `1RL02DEObzOQaehQeQzffdjjc1vswWpQm`.
- Valores em reais **correntes**, não comparações reais. Agregação por somatório municipal; sub-regiões definidas na matriz canônica de 34 municípios.

## Síntese metropolitana conferida

| Exercício | Despesa corrente liquidada (R$) | Investimento liquidado (R$) | Cobertura |
|---|---:|---:|---:|
| 2023 | 8.992.882.884,56 | 484.948.399,24 | 34/34 |
| 2024 | 9.772.551.152,88 | 500.824.152,06 | 34/34 |
| 2025 | 10.526.057.811,59 | 302.301.895,18 | 34/34 |

Valor de 2025 reconcilia com G1-3 anterior (diferença inferior a 1 centavo em cálculo de ponto flutuante).

## Investimento liquidado por sub-região, R$

| Sub-região | 2023 | 2024 | 2025 |
|---|---:|---:|---:|
| Ribeirão Preto (15 municípios) | 310.522.663,23 | 327.997.332,21 | 208.212.555,64 |
| Jaboticabal (6 municípios) | 59.821.843,31 | 58.507.463,35 | 29.313.238,96 |
| Mococa (6 municípios) | 28.733.930,90 | 29.897.759,53 | 23.837.004,17 |
| Batatais (7 municípios) | 85.869.961,80 | 84.421.596,97 | 40.939.096,41 |

## QA da sequência municipal nominal 2023 → 2024 → 2025

- **Pico em 2024 (14):** Batatais; Brodowski; Cajuru; Dumont; Jaboticabal; Luís Antônio; Mococa; Orlândia; Ribeirão Preto; Santo Antônio da Alegria; São Simão; Serrana; Sertãozinho; Taquaral.
- **Queda em ambos os intervalos (11):** Altinópolis; Barrinha; Cássia dos Coqueiros; Guariba; Jardinópolis; Morro Agudo; Nuporanga; Pitangueiras; Pontal; Sales Oliveira; Santa Cruz da Esperança.
- **Vale em 2024 (8):** Guatapará; Monte Alto; Pradópolis; Santa Rita do Passa Quatro; Santa Rosa de Viterbo; Serra Azul; Taiúva; Tambaú.
- **Crescimento em ambos os intervalos (1):** Cravinhos.

As contagens (14 + 11 + 8 + 1 = 34) reproduzem as categorias da auditoria municipal anterior, mas **não** se devem interpretar como tendências estruturais nem como variações reais.

## Ressalvas relevantes para a homologação
1. O estágio da despesa está definido: **liquidada**, não empenhada nem paga.
2. A população declarada na DCA de **2023 difere da informada em 2024 para os 34 municípios**. Antes de homologar os valores por habitante e séries per capita, conferir a série demográfica canônica do relatório e eventual mudança de fonte/ano-base. A população declarada em cada arquivo permanece preservada como metadado.
3. A deflação de investimentos precisa usar a convenção de preços de setembro de 2026 do diagnóstico geral; a planilha de receitas de capital a preços médios de 2025 não é intercambiável.
4. A validação de totais nominais **não** homologa automaticamente as variações reais municipais, o investimento per capita, as matrizes SWOT nem os mapas.
5. Não há lacunas entre os 68 registros de 2023–2024 selecionados; não se efetuaram imputações.

## Decisão
**G1-3 — extração nominal 2023–2025 e QA de cobertura: concluídas.** Continuam abertas a reprodução dos fatores de deflação por exercício, a checagem dos indicadores per capita com denominadores documentados e a conferência das figuras/afirmações no Volume II. Preservar o Lote 98 (66 páginas) e o pacote congelado do G0 até completar essas verificações.
