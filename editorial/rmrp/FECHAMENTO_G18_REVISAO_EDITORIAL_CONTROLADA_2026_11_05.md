# RMRP — G18 — Revisão editorial controlada do Volume II — 05/11/2026

**Status: versão derivada para QA interno, não homologada para circulação externa.** Fonte: DOCX congelado Lote 98 do G0, SHA-256 `fffd21bb65251d89caee484c2cabf7b813a7884760f60943c95919e608249df4`. O original permaneceu intacto.

## Alterações concluídas na cópia G18
1. Identificada **cota mensal do FPM** em cabeçalho da tabela de composição e nas remissões ao indicador, sem alterar numeradores nem percentuais.
2. Explicitado que tabelas e séries reais per capita utilizam `populacao_dca`, enquanto os quatro mapas de 2025 de valores por habitante usam estimativa IBGE/SIDRA 6579 (FPM, receita corrente, investimento e ISS). Não houve nova coleta populacional.
3. Diferenciado IPCA médio anual nas séries analíticas dos mapas com IPCA de dezembro por exercício; preservado o mapa 15 validado conforme o método originalmente utilizado.
4. Redesenhada apenas a **Figura F3** (dispersão tributação/receita × FPM cota mensal/receita, 34 municípios), reposicionando a legenda para fora do painel e desobstruindo a observação de Ribeirão Preto.

## Provas técnicas
- Cópia editável `RMRP_VOLUME_II_REVISAO_CONTROLADA_LOTE_G18.docx` gerada localmente; renderizada em PDF de trabalho, **66 páginas**.
- DOCX: 321 parágrafos, 45 tabelas, 15 mídias; **única mídia alterada = word/media/image10.png**.
- Verificação visual das páginas 2, 4, 7, 10 e 59, com montagem de contato das 66 páginas para conferência global; nenhuma palavra fora de limites nas cinco páginas detalhadas.
- Matriz `G18_MATRIZ_CORRECOES_EDITORIAIS.csv`, `G18_QA_EDICAO.json` e script `gerar_lote_g18.py` preservados no pacote local `RMRP_G18_PACOTE_REVISAO_CONTROLADA_2026_11_05.zip`. A gravação do relatório no GitHub **não equivale à transferência do DOCX/PDF binário**.

## Pendências
Rótulo FPM/RC ainda incorporado ao raster da Figura F2 (a legenda do documento explicita cota mensal); decidir se sua imagem deve ser refeita. Confirmar opção editorial pela coexistência de dois métodos de IPCA ou padronização da cartografia. Executar verificação jurídica dos diagramas e cenários, respeitando quarentenas RGF/RREO de Pontal, Barrinha e Orlândia. A inspeção em miniaturas das 66 páginas não substitui uma QA manual detalhada de cada página.

**Não declarar G18 final/publicável.** A base Lote 98 permanece preservada, auditável e diferenciada da cópia G18.
