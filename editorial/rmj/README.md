# RMJ — guia operacional e metodológico canônico

**Atualização:** 15 de outubro de 2026. **Escopo:** boletim fiscal da Região Metropolitana de Jundiaí (RMJ), sem modificar o portal estadual `finbra-tic-tim-referencia.pages.dev`.

## Acesso e organização

- **Painel público:** https://financas-rmj.pages.dev/
- **HTML canônico:** `editorial/rmj/index.html`
- **Matriz integral versionada:** `editorial/rmj/dados/rmj_decomposicao_programas_acoes_2023_2025.csv`
- **Explorador:** https://financas-rmj.pages.dev/#explorador-investimentos
- **Histórias municipais:** https://financas-rmj.pages.dev/#destaques
- **Workflow de produção:** `.github/workflows/publish-rmj.yml`
- **Verificação da base:** `editorial/rmj/check_explorador_integral.py`
- **Gerador da matriz:** `editorial/rmj/build_decomposicao_integral.py`
- **Extração de origem:** `editorial/rmj/analyze_tcesp_pilot.py`
- **Testes:** `editorial/rmj/check_html.py`, `editorial/rmj/smoke_browser.js`, `editorial/rmj/qa_browser.cjs`.
- **Relatórios prévios:** `DECOMPOSICAO_QUANTITATIVA_INVESTIMENTOS_2023_2025.md` e `CONCENTRACAO_RECORRENCIA_INVESTIMENTOS_2023_2025.md`.

## Universo, fonte e definição

Sete municípios: Cabreúva, Campo Limpo Paulista, Itupeva, Jarinu, Jundiaí, Louveira e Várzea Paulista. Comparação do investimento liquidado de 2023 a 2025; contextualização histórica DCA/FINBRA 2021–2025 e indicadores complementares RGF, receitas, funções e CAPAG, segundo definições específicas do painel.

A decomposição utiliza os arquivos oficiais de **Despesa Detalhada do Tribunal de Contas do Estado de São Paulo (TCESP)**, filtrando **grupo de natureza 44** e **tipo de despesa “Valor Liquidado”**. Valores são convertidos e reconciliados em **centavos**, sem somar empenhos e pagamentos. Há dois níveis: programa (chave município + código de programa) e ação (chave município + código de programa + código de ação).

A fórmula é **variação nominal = liquidado no ano final − liquidado no ano inicial** para cada chave de classificação. Entrada, saída, repetição e alteração de nome são estados contábeis, não demonstrações de origem, continuidade material ou término de política pública. A mesma ação pode mudar de código de programa entre anos: **ação 1009, novo hospital de Várzea Paulista, programa 40 em 2023 e 70 em 2024/2025**. Não atribuir causalidade a partir das decomposições nem confundir liquidação com obra concluída.

## Cobertura e controles

- **21** extratos município × ano no período 2023–2025.
- **1.169** registros de diferenças por chave e par de anos.
- **28** decomposições, correspondentes a sete municípios × dois intervalos (2023–2024 e 2024–2025) × dois níveis (programa/ação).
- As diferenças são verificadas individualmente em centavos; os totais das decomposições por programa e por ação devem coincidir nos **14** pares município–intervalo.
- **2025 RMJ:** investimento liquidado de **R$ 265.425.559,07**; a comparação com 2024 e a análise das principais contribuições constam no próprio painel.
- Concentração: participação dos três maiores programas no total liquidado no município e exercício. Não mede qualidade ou eficiência.

O verificador `check_explorador_integral.py` é executado em `.github/workflows/pages-preview.yml`; o fluxo de produção também roda essa verificação. O explorador utiliza o CSV versionado, sem duplicação de valores manuais, disponibiliza filtros por município/período/programa ou ação, pesquisa por código/descrição, classificação de movimentos, ordenação, valores de ambos os exercícios e exportação em CSV. A tabela exibe até 150 linhas por filtro; a exportação contém todos os resultados filtrados.

## Publicação e confirmação de produção

O fluxo `.github/workflows/publish-rmj.yml`, acionado por mudanças de HTML, arquivos de teste, CSV ou pelo comando manual GitHub Actions, deve:

1. Validar sintaxe HTML/JavaScript, testes simulados e integridade da matriz.
2. Copiar para o mesmo diretório de publicação **`index.html` e `dados/rmj_decomposicao_programas_acoes_2023_2025.csv`**; manter o cabeçalho de segurança `_headers`.
3. Publicar **exclusivamente** no projeto Cloudflare Pages `financas-rmj`.
4. Consultar os endereços públicos do HTML e CSV e verificar a identidade byte a byte do CSV publicado com o versionado.

Não tratar aprovação de CI ou de prévia como prova de produção. Confirmar o *run* de `Publicar boletim RMJ` e o conteúdo publicado. **Evidência de êxito:** execução GitHub Actions [#38770047802](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38770047802) para o commit `240f71bd`, incluindo conferência de HTML e CSV. Edição de histórias municipais, [PR #195](https://github.com/hilaliskandar/mapa_do_tesouro/pull/195), também teve publicação de produção concluída no *run* [#38770880666](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38770880666). Para alterações posteriores, consultar o run correspondente em vez de reutilizar essa evidência.

**Incidente resolvido:** o smoke test de produção não implementava `Element.closest`; a execução [#38769573474](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38769573474) falhou antes de publicar. Corrigido no [PR #194](https://github.com/hilaliskandar/mapa_do_tesouro/pull/194). A publicação anterior copiava só `index.html`; corrigida no [PR #193](https://github.com/hilaliskandar/mapa_do_tesouro/pull/193).

## Histórico resumido das entregas

- **#173–#183:** governança editorial, auditoria dos indicadores, conciliação de fontes e extração municipal de programas/ações; diligências normativas apenas quando alterem interpretação material.
- **#184:** decomposição anual de programas e ações, com conciliação das diferenças.
- **#185:** concentração e recorrência; atenção às recodificações.
- **#186–#189:** introdução da concentração e dos rankings de variação no painel.
- **#190:** gerador reproduzível dos extratos e fluxo de versionamento da matriz.
- **#191:** explorador integral consumindo o CSV versionado.
- **#192:** revisão de rótulos e verificação automatizada dos 1.169 registros.
- **#193–#194:** correção da publicação do CSV e do teste simulado, com confirmação em produção.
- **#195:** integração das principais contribuições dos programas às histórias dos sete municípios.
- **#196:** revisão da hierarquia e da redação editorial (consultar estado final do PR e o run de produção para confirmar sua publicação).

## Critérios de continuidade e prevenção de regressões

- Manter indicadores, notas, padrões visuais e funcionalidades aprovados; fazer mudanças localizadas, sem reescrever o HTML inteiro a partir de uma versão antiga.
- Nunca inventar valores, citações ou vínculos entre receitas de capital e despesas específicas.
- Priorizar evidências contábeis e interpretações substantivas, **não** buscas normativas extensivas.
- Não confundir `financas-rmj.pages.dev` com o portal estadual `finbra-tic-tim-referencia.pages.dev`.
- Para toda mudança: criar ramo, PR, verificar Core CI, Pages Preview, QA no navegador, incorporar e checar o fluxo de produção `publish-rmj.yml`, inclusive conteúdo do CSV.
- Registrar nova fonte, transformação, comparação, ressalva e resultado da implantação neste guia e no inventário; conservar a versão anterior para comparação.

## Pendências e limitações

- Conferir se a revisão editorial #196 consta efetivamente da publicação de produção.
- Atribuição causal, contratos e resultados físicos exigem documentação adicional específica. Não os inferir do detalhamento TCESP.
- O histórico de 2023–2025 é nominal; comparações em preços constantes devem observar a metodologia de inflação do painel.
- Quando se requer reextração, manter registro de origem, datas, *hashes* e diferenças para detectar alterações retroativas das fontes.
