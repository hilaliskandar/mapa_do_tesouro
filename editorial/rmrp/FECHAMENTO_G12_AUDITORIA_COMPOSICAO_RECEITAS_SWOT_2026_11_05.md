# Fechamento G1-2 — Auditoria de composição de receitas DCA 2025 e reivindicações nas SWOT

**Data:** 05/11/2026 · **Escopo auditado:** rubricas de receitas de 2025 do Volume II, Lote 98 (66 páginas), com confronto da DCA I-C e das 34 SWOT municipais. **Situação:** frente de **receitas brutas da DCA 2025 aprovada**; G1-2 e G1 integral **ainda abertos** para despesas, investimentos, datas-base e cartografia.

## 1. Fonte, recortes e método

Fonte primária **arquivo local original** `receitas orçamentárias (anexo I-C) - municípios de sp 2025.csv`, delimitado por ponto e vírgula e codificado Latin-1. Seleção: 34 códigos IBGE textuais, definidos pelo cadastro de 2025 na aba `SERIE_374` da planilha Lote 94; `Coluna = Receitas Brutas Realizadas`; contas sintéticas `siconfi-cor_RO...` selecionadas por códigos exatos. Não foram usadas inferências a partir de palavras na descrição da rubrica. A chave município-conta foi verificada contra duplicidade, mantendo 34 municípios distribuídos em sub-regiões de 15, 6, 6 e 7 municípios.

Campos auditados: Receitas correntes `RO1.0.0.0.00.0.0`, impostos/taxas/contribuições de melhoria `RO1.1.0.0.00.0.0`, ISS `RO1.1.1.4.51.0.0`, IPTU `RO1.1.1.2.50.0.0`, ITBI `RO1.1.1.2.53.0.0`, FPM total `RO1.7.1.1.51.0.0`, FPM cota mensal `RO1.7.1.1.51.1.0`, ICMS `RO1.7.2.1.50.0.0`, IPVA `RO1.7.2.1.51.0.0`, além de FPM cotas extraordinárias `RO1.7.1.1.51.2.0`. Cada participação foi recomputada como soma da rubrica para o recorte dividida pela soma da receita corrente no mesmo recorte, nunca como média aritmética simples de porcentagens municipais.

**Cobertura:** receita corrente, tributação, ISS, IPTU, ITBI, FPM total, FPM cota mensal, ICMS, IPVA aparecem em **34/34 municípios** e sem duplicidade na seleção. A conta de **cotas extraordinárias de FPM não apresenta linha em Jaboticabal e Orlândia**; não atribuir zero observado à ausência, embora total e cota mensal estejam disponíveis em ambos. 

## 2. Confronto da tabela de composição do Volume II

Foram cotejados **20 percentuais da tabela de composição** (tributação, ISS, IPTU e FPM, em RMRP e quatro sub-regiões), com tolerância de **0,0051 ponto percentual** por arredondamento a duas casas. **Resultado: 20/20 conforme, zero divergências.**

| Recorte | Tributação/receita | ISS/receita | IPTU/receita | FPM cota mensal/receita |
|---|---:|---:|---:|---:|
| RMRP | 25,44% | 9,06% | 8,53% | **12,84%** |
| Sub-região de Ribeirão Preto | 28,89% | 10,76% | 9,55% | 9,13% |
| Sub-região de Jaboticabal | 19,24% | 5,74% | 7,60% | 20,31% |
| Sub-região de Mococa | 17,27% | 5,08% | 7,03% | 24,06% |
| Sub-região de Batatais | 16,33% | 4,78% | 4,27% | 20,17% |

**Achado metodológico substantivo:** o rótulo da tabela **“FPM/receita”** corresponde inequivocamente à **cota mensal de FPM** (`RO1.7.1.1.51.1.0`), **não** à rubrica agregada do FPM total (`RO1.7.1.1.51.0.0`). Na RMRP, receita corrente total **R$11.836.161.388,56**, cota mensal FPM **R$1.519.813.720,90** (**12,8404%**) e FPM total **R$1.684.367.214,39** (**14,2307%**); diferença **R$164.553.493,49** e **1,3903 ponto percentual**. A rubrica de cotas extraordinárias explica o diferencial do agregado, observadas as duas ausências individuais da linha analítica. Para os quatro agregados sub-regionais, a escolha da cota mensal também reproduz a tabela existente.

**Encaminhamento editorial EDI-03:** explicitar “FPM — cota mensal/receita corrente” na tabela, legendas e notas quando o mesmo conceito for utilizado nas SWOT; se a discussão for de dependência total de transferências do FPM, apresentar **FPM total** de modo separado e com rótulo próprio. **Não alterar retroativamente o numerador sem nota**, porque isso mudaria o conceito da série e as comparações.

## 3. Confronto dos indicadores locais nas SWOT

O DOCX Lote 98 possui 34 matrizes SWOT municipais, além de cinco matrizes de síntese RMRP/sub-regionais. As rubricas tributárias e a cota mensal FPM foram identificadas por expressões específicas nos textos das SWOT e reconciliadas com os códigos dos municípios na DCA 2025.

- **50 afirmações numéricas individuais** de tributação/receita e FPM cota mensal/receita encontradas e recalculadas;
- **50/50 conformes** à precisão publicada de duas casas;
- **98 ocorrências de porcentagem nas 34 matrizes municipais** contadas de modo exploratório. As demais 48 ocorrências não são automaticamente classificadas como inconformes: são variações reais, despesas e investimentos ou outras medidas que requerem bases específicas, e **não foram validadas nesta frente**.

Nota: os 50 testes representam **afirmações de indicadores extraídas**, não 50 municípios distintos. As 34 SWOT continuam presentes e preservadas na versão de referência.

## 4. Recortes ainda não homologados nesta frente

| Conteúdo | Evidência ou insumo disponível | Bloqueio |
|---|---|---|
| Despesa corrente liquidada/receita corrente | Denominador DCA receitas 2025 disponível | Base de despesa liquidada por município/ano e natureza ainda não incluída no pacote de inventário G0 |
| Investimento liquidado/receita corrente | Denominador DCA disponível; mapas no Volume II | Base de investimento liquidado 2023–2025 e 2015–2025 para confrontar eventos e variações |
| Receita real por habitante de 2025 | Receita nominal e campo de população no CSV DCA | Deflator a preços de **setembro de 2026** e compatibilidade de população não reproduzidos neste ciclo |
| Crescimento real de receita por habitante 2015–2025 | Indicadores no quadro e nas SWOT | Base de 2015 e tratamento de população/deflator da série geral ainda não conciliados |
| Investimento real por habitante 2023–2025 | Tabela e mapa, 34 SWOT | Base anual de investimento liquidado e deflator original das despesas |
| Mapas IPTU/ISS/ITBI, FPM/ICMS/IPVA | 34/34 contas brutas encontradas em 2025 | Comparação célula–feição de cada mapa, legenda, universo e unidade ainda não executada |
| RGF/RREO e conformidade LRF | Evidências dos Lotes 99–104 | Pontal/Barrinha/Orlândia sob quarentena, tratado separadamente no G2 |
| Repasses federais e reforma tributária | Registro FNDE e textos LC 227/2026 | G2/G3, não suprir com DCA receita bruta |

**Não é apropriado declarar “todas as receitas e despesas do Volume II homologadas” com base nos 70 testes desta etapa.**

## 5. Artefatos e rastreabilidade

- `/mnt/data/RMRP_FECHAMENTO_G1/auditar_g12_composicao.py` — rotina reproduzível baseada no arquivo DCA 2025 e DOCX Lote98.
- `/mnt/data/RMRP_FECHAMENTO_G1/G12_CONFERENCIA_TABELA_2_2025.csv` — **20 testes**, fonte/conta, cálculo e resultado.
- `/mnt/data/RMRP_FECHAMENTO_G1/G12_CONFERENCIA_SWOT_2025.csv` — **50 testes** por município, código IBGE, conta e texto contextual.
- `/mnt/data/RMRP_FECHAMENTO_G1/G12_MATRIZ_PROVENIENCIA_AMPLIADA.csv` — **17 eixos** de proveniência e pendências, em complemento às nove entradas do G1-1.
- `/mnt/data/RMRP_FECHAMENTO_G1/QA_G12_RECEITAS_2025.json` — QA detalhado, cobertura e totais por sub-região.

**Drive:** arquivos CSV arquivados com referência original de bytes e confirmação de metadados (não realizada retransferência para verificar SHA remoto):
- Quadro composição: https://drive.google.com/file/d/1HmclVw1Vt1-KwjrlQWoMSFlV_TELPh8x/view (5.801 bytes).
- SWOT: https://drive.google.com/file/d/1AqytTJD03pEnFJhKyS1fQPLlwz1xdpl1/view (20.067 bytes).
- Matriz de proveniência ampliada: https://drive.google.com/file/d/1TOz689OEczWeBkMiP405PVbQq5S7dlnc/view (6.539 bytes).

## 6. Decisão e próximo trabalho

**Aceite parcial G1-2 para composição da receita corrente DCA 2025:** os 20 percentuais dos cinco recortes e 50 alegações de tributação/FPM das SWOT estão reconciliados, sem divergências de arredondamento. **Pendência editorial EDI-03 aberta:** definir rótulo de FPM cota mensal versus FPM total. **G1-2 e G1 integrais ainda abertos** para despesas, investimentos, série real per capita, mapas e fontes das afirmações restantes. A versão do Volume II Lote98 (66 páginas) não foi modificada.

**Próxima frente G1-3:** localizar base auditável de despesa **liquidada** por município em 2023–2025, validar rubricas de despesa corrente/investimento contra quadro inicial e SWOT, e depois reconciliar séries reais per capita com o deflator histórico especificado.
