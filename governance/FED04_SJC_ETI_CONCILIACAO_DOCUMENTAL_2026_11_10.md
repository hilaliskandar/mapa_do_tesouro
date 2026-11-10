# FED04 — Conciliação documental: São José dos Campos e descoberta da modalidade ETI

**Data da verificação:** 10/11/2026. **Estado:** evidência municipal independente localizada; fonte federal de pagamento ainda pendente. **Escopo:** conciliação DCA 2025, rubrica RO1.7.1.5.00.0.0, primeira posição na fila de 191 municípios.

## 1. Evidência da fonte municipal primária

No **Diário do Município de São José dos Campos**, edição **3.642**, de **30/01/2026**, páginas **13–14**, consta o **Balancete da Receita do período 01/12/2025 a 31/12/2025** (exercício de 2025), sob as seguintes classificações hierárquicas:

| Natureza | Discriminação no balancete | Arrecadação no mês (R$) | Arrecadação no ano (R$) |
|---|---|---:|---:|
| 17150000000 | Transferências de recursos de complementação da União ao Fundeb | 826.081,91 | 3.304.327,61 |
| 17155000000 | Transferências de recursos da complementação da União ao Fundeb | 826.081,91 | 3.304.327,61 |
| 17155300000 | **Transferências de recursos do Fundeb destinados à criação de matrículas ETI** | 826.081,91 | **3.304.327,61** |
| 17155301000 | **Transferências de recursos do Fundeb destinados à criação de matrículas ETI**, fonte 0005, rubrica 2027 | 826.081,91 | **3.304.327,61** |

**Fonte exata:** https://diariodomunicipio.sjc.sp.gov.br/portal/edicoes/download/2632 — texto extraído, linhas equivalentes ao bloco do balancete (páginas 13–14). Valores hierárquicos: **não somar os quatro lançamentos**, que representam agregados e desdobramento da mesma receita. O valor anual é exatamente igual ao registro de 2025 da DCA (R$3.304.327,61), obtido na matriz prévia FED04; diferença monetária observada DCA × balancete: **R$0,00**.

## 2. Interpretação da divergência anterior

A matriz prévia comparou a conta DCA agregada de complementação da União ao Fundeb exclusivamente com listas municipais **VAAT e VAAR** de 2024 e 2025. O balancete municipal evidencia **modalidade ETI (educação em tempo integral)**, que não foi coberta pelo universo VAAT/VAAR dessa triagem. A falta de correspondência em VAAT/VAAR **não indica, neste caso, falta de origem orçamentária identificada**, e o município não deve permanecer etiquetado apenas como `SEM_BENEFICIO_2024_2025_IDENTIFICADO` sem qualificar que a classificação **ETI foi identificada**.

O MEC/FNDE documenta financiamento específico para criação de matrículas em tempo integral no âmbito do Fundeb em 2025:
- Portaria MEC nº 586, 20/08/2025: https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/legislacao/2025/portaria-mec-no-586-de-20-de-agosto-de-2025
- Portaria MEC nº 605, 29/08/2025: https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/legislacao/2025/portaria-mec-no-605-de-29-de-agosto-de-2025
- Esclarecimento MEC: https://www.gov.br/mec/pt-br/acesso-a-informacao/perguntas-frequentes/programa-escola-em-tempo-integral/execucao-dos-recursos-2025-das-matriculas-em-tempo-integral-portarias-no-605-e-no-669-2025/o-recurso-da-assistencia-financeira

**Cuidado:** uma classificação orçamentária ETI não substitui confirmação de fluxo financeiro em conta específica nem valida a coincidência com cronograma de repasses MEC/FNDE. A conciliação concluída aqui é **DCA × balancete municipal**; a conciliação **DCA × repasse federal ETI** permanece aberta.

## 3. Implicações para SP645 e método

1. Ampliar o mapa de modalidades federais de complementação/transferência vinculada ao Fundeb em 2025 para incluir **ETI**, sem confundir com VAAT, VAAR ou VAAF. Comprovar natureza e enquadramento legal da ETI para cada exercício antes de atualizar o crosswalk canônico.
2. Nos **190 demais municípios** da fila original, buscar a abertura da natureza `1.7.1.5.53` ou `171553` em balancetes, RREO/MDE e demonstrativos de receita, antes de atribuir pendência a ausência de beneficiários VAAT/VAAR.
3. **Não subtrair** automaticamente R$3.304.327,61 do total dos 191 casos sem emitir a versão 2 controlada da matriz e distinguir: (a) modalidade de receita identificada, (b) valor DCA confirmado por fonte municipal, (c) pagamento federal confirmado, (d) homologação final.
4. São Vicente (R$3.271.812,78), Taboão da Serra (R$2.670.875,53) e Franca (R$2.577.016,74) permanecem pendentes de desagregação documental equivalente. Priorizar seus balancetes de receita 2025, não somente o RREO consolidado.
5. O endpoint SICONFI RREO Anexo 8 com zero registros **não é prova de que o demonstrativo não foi publicado**. São José dos Campos oferece RREO 2025/6º bimestre em https://servicos.sjc.sp.gov.br/sf/downloads/contas_publicas/cop_000009765.pdf e no portal: https://www.sjc.sp.gov.br/servicos/governanca/portal-da-transparencia/planejamento-e-prestacao-de-contas/ .

## 4. Gates

FED04 continua **em andamento**; o PR #232 permanece em rascunho. **Não executar merge, migração, deploy, alterações no SQLite ou R2 de produção, nem publicar as novas variáveis.** Esta nota é evidência de auditoria, não homologação final dos valores federais.

## 5. Ressalva de captura

A captura textual do balancete municipal via índice público do Diário foi bem-sucedida. A tentativa de extração direta do PDF completo pela instância Crawl2AI retornou erro; a inspeção da versão PDF da prefeitura via busca textual foi possível. Recomenda-se arquivar cópia imutável do documento oficial e seu SHA-256 na etapa de QA documental.