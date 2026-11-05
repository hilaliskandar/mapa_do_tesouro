# RMRP — G1-4 — Confronto quantitativo de 2025 das matrizes SWOT municipais

Data 05/11/2026. **Corpus analisado:** texto Lote 61A, com 34 matrizes municipais. **Fonte:** FINBRA/DCA canônica SP645, Google Drive `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`, exercício 2025. População `populacao_dca`; sem coleta nova.

## Resultado dos testes
**194 afirmações percentuais testadas, 194 conformes, 0 divergentes**, com tolerância de 0,0052 p.p. para percentual exibido com duas casas.

| Indicador e numerador | Afirmações | Divergências |
|---|---:|---:|
| iss | 34 | 0 |
| icms | 34 | 0 |
| soma | 34 | 0 |
| fpm | 59 | 0 |
| tributos | 25 | 0 |
| despesa | 3 | 0 |
| investimento | 5 | 0 |

A soma ISS+ICMS é soma de montantes das rubricas observadas, dividida pela receita corrente; não representa média legal de referência do IBS nem projeção de repartição. FPM nos enunciados corresponde a **cota mensal** (`dca_fpm_cota_mensal`); a denominação genérica “FPM” exige esclarecimento editorial, pois não representa o FPM total. `dca_receita_tributaria_bruta` e `dca_receita_corrente_bruta` foram utilizados para as participações. Despesas correntes e investimento foram selecionados como valores liquidados, divididos por receita corrente bruta.

Também foram identificados **3 enunciados com investimento real por habitante em reais em 2025**, dos quais 3 conformes. Esses casos estão em [CSV complementar](G14_AUDITORIA_MONTANTES_INVESTIMENTO_PER_CAPITA_2025_SWOT.csv).

Os registros individuais dos 194 testes encontram-se em [CSV de auditoria](G14_AUDITORIA_SWOT_COMPOSICAO_2025_194_TESTES.csv). **Não se deve somar indiscriminadamente os 194 testes aos 35 indicadores longitudinais já auditados**, pois são famílias e padrões textuais distintos; a contagem mede afirmações localizadas, não abrangência da totalidade de qualquer documento.

## Achados editoriais
- O texto Lote 61A contém **0** ocorrências literais do fechamento `indeterminado..` (duplicação de ponto). Corrigir numa **cópia de trabalho**, apenas depois do QA contra o documento de referência.
- O título “ISS principal” é juridicamente e contabilmente mais restrito que “ISS total”; preservar o qualificador em qualquer tabela/legenda.
- O “FPM” no Lote 61A foi numericamente calculado como **FPM cota mensal**; expandir rótulo para evitar sua interpretação como FPM integral.
- O somatório “ISS principal + ICMS” é exposição contábil de 2025, não simulação de arrecadação de IBS.
- Nas ameaças e oportunidades do IBS, preservar caráter condicional; não inferir benefício, perda ou redução automática do FPM.

## Limites e gates
A verificação não substitui a inspeção binária do **DOCX/PDF Lote 98**, que está **preservado em ZIP congelado no Google Drive ID `1eROu1DKokcGlxwv_qRZZLYJAyo__XmeK`**, conforme G0; não declarar o relatório integral homologado a partir do Lote 61A. Não alterar original nem bases. Próxima etapa: extrair o documento de referência do pacote G0, conferir os enunciados efetivamente presentes, corrigir o rótulo FPM e pontuação numa derivação controlada, e então proceder à QA cartográfica de mapas/legendas.
