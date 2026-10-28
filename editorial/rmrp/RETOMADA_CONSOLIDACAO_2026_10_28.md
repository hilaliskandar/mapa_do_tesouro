# Retomada de consolidação do relatório fiscal RMRP — 28/10/2026

**Status:** inventário editorial e roteiro de montagem concluídos; relatório integral e pacote de imagens não recuperados nesta diligência; nenhum deploy/publicação autorizado ou executado.

## Decisão metodológica
Conciliação compulsória TCESP–DCA encerrada (README 28/10/2026). Tratar fontes como séries oficiais distintas, sem substituir uma pela outra. TCESP para detalhamento por natureza, programa e ação; DCA/Siconfi para contas anuais federais; diferenças entre fontes entram em nota metodológica, sem atribuição causal não demonstrada.

## Arquivos de trabalho identificados no repositório
- `CADERNO_INTEGRADO_STATUS_2026_10_19.md`: registra caderno integral de 53.625 bytes e 34 fichas, mas **não contém o texto completo**; pacote original foi disponibilizado na conversa anterior, sem nova recuperação neste inventário.
- `CONTINUIDADE_CADERNO_INTEGRADO_2026_10_19.md`: síntese regional 2023–2025 e ressalvas.
- `CONSOLIDACAO_FISCAL_SUBREGIOES_2023_2025.md`: séries nominais e cobertura.
- `CONSOLIDACAO_SUBREGIOES_INVESTIMENTOS_2023_2025.md`: 102 município-ano TCESP, checagem interna.
- `ANALISE_HISTORICA_DCA_SUBREGIOES_2013_2025.md`: DCA 2013–2025, 34 municípios, 25 contas.
- `ANALISE_REAL_IPCA_SUBREGIOES_2013_2025.md`: IPCA data-base setembro/2026 e 1.625 agregados.

## Fatos-base consolidados, sem novo cálculo
- Universo: 34 municípios; SR1 15, SR2 6, SR3 6 e SR4 7.
- DCA, variação real 2023–2025: receita corrente +10,25%; despesa corrente +7,09%; investimento -42,97%; investimento/receita corrente 4,94% → 2,55%.
- TCESP, investimento liquidado 2025: R$ 302.301.895,18; 2024: R$ 500.824.152,06; variação **nominal** -39,64%. Não confundir a série TCESP com a taxa real DCA.
- Cobertura parcial em variáveis setoriais e indicadores RGF/RREO: nunca representar somas dos respondentes como total integral; escala de percentuais exige conferência.

## Proposta de integração de mapas, tabelas e gráficos por seção
| Seção editorial | Tabelas e gráficos | Mapa temático, junto à análise | Condição de QA |
|---|---|---|---|
| Delimitação e perfil territorial | 34 municípios e quatro sub-regiões | Localização, polos e limites sub-regionais oficiais | Validar geometria, chaves IBGE e CRS EPSG:4674 |
| Receita e capacidade fiscal | Evolução receita corrente/tributária nominal e real; composição e concentração | Receita per capita ou autonomia municipal, quando denominadores completos | Mesmo ano, mesma população, fonte DCA explícita |
| Despesa e investimento | Série 2013–2025; curva 2023–2025; ranking e participação municipal | Investimento liquidado por município (TCESP), com legenda, ano e conceito | 102 recortes município-ano, valores em centavos, não inferir execução física |
| Comparação entre sub-regiões | Quadros SR1–SR4, participação e razões entre somas | Diferenças relativas entre quatro sub-regiões | Integridade municipal/sub-regional, evitar média simples de razões |
| Sustentabilidade fiscal | RCL, pessoal, dívida, caixa, CAPAG e cobertura | Classes municipais de CAPAG somente se referência temporal compatível | CAPAG não é nota regional; marcar n.d. e cobertura parcial |
| Fichas municipais | 34 fichas 2023–2025, gráficos e dados-chave | Miniatura municipal apenas onde a informação espacial adicionar análise | Texto completo e QA municipal antes da publicação |

**Diretriz editorial:** não produzir seção isolada de atlas. Inserir mapas nas seções que explicam e limitar mapas a variáveis com base geográfica oficial e conteúdo verificável. Não gerar mapas ilustrativos por IA.

## Próxima execução verificável
1. Localizar e recuperar o caderno completo `CADERNO_RMRP_INTEGRADO_34_MUNICIPIOS_2026_10_19.md` e pacote `CADERNO_RMRP_CANDIDATO_E_EVIDENCIAS_2026_10_19.zip`; conferir hash SHA-256 declarado `bf8399d532240b5f97a3833b4f1b97fea13224e73b4bba302f27f0100d1c3d53` para o MD.
2. Recuperar os arquivos já produzidos de gráficos, mapas e bases, sem recriar artefatos existentes. Distinguir comprovados de apenas referidos em registros.
3. Montar o caderno em uma única versão persistida, eliminar duplicações e inserir figuras diretamente nas seções.
4. Rodar QA quantitativo, cobertura, espacial, temporal e editorial. Não homologar nem publicar automaticamente.

**Limite documental:** este inventário foi produzido a partir dos seis registros listados, não corresponde a uma nova verificação dos 34 perfis, da base original ou dos arquivos gráficos.


## CORREÇÃO E RECUPERAÇÃO PRIORITÁRIA — 28/10/2026
**O inventário inicial acima tornou-se desatualizado quanto à localização do relatório integral.** A busca no Drive identificou não apenas o caderno de 19/10, mas um relatório editorial nativo substancialmente posterior e as provas cartográficas de 25/10. Prevalecem os documentos abaixo para a retomada; não reconstruir nem substituir o acervo por versões de 19/10.

1. **Fonte de verdade editorial segundo README operacional do Drive:** [RMRP — Consolidação editorial integrada — minuta de trabalho — 23-10-2026](https://docs.google.com/document/d/1UXpfCAllRc84nj49yeRyT14H2Neij_S8elZzq79MxyY/edit), ID `1UXpfCAllRc84nj49yeRyT14H2Neij_S8elZzq79MxyY`; verificar versão nativa e mudanças recentes antes de editar.
2. **README de continuidade detalhado:** [00_README_CONTINUIDADE_FINANCAS_RMRP_2026-10-23](https://docs.google.com/document/d/1e4G6zFFG6bxz_NKJj6yOwiJbkMb2i_MuQ4JLo3DrwlU/edit), ID `1e4G6zFFG6bxz_NKJj6yOwiJbkMb2i_MuQ4JLo3DrwlU`. Lido; traz protocolos, QA, instrução de tipografia 12 pt/1,5/justificado, e registros até 25/10.
3. **Relatório consolidado adicional, integral:** [RMRP — Relatório consolidado integrado — 23-10-2026](https://docs.google.com/document/d/1-M-HKvexFFra_k7j-R_kXAzd5BzfSl1q4A3E_BbxU5s/edit), ID `1-M-HKvexFFra_k7j-R_kXAzd5BzfSl1q4A3E_BbxU5s`. Texto integral acessível no Drive, com nove capítulos e fichas municipais. Não confundir com o documento editorial canônico definido no README anterior sem verificar a relação de versões.
4. **Prova de integração cartográfica independente:** [RMRP — PROVA de integração cartográfica — 25-10-2026](https://docs.google.com/document/d/1FF5nX64MwOcX3oF5SKIl72w-4zG0MD74tzmtFsyMxAg/edit), ID `1FF5nX64MwOcX3oF5SKIl72w-4zG0MD74tzmtFsyMxAg`. Registros do README indicam 63 páginas, 51 tabelas nativas, 34 fichas e quatro imagens individuais de maior legibilidade, cada uma junto de seu capítulo; é **prova não homologada** e cobre quatro dos 16 mapas anteriores.
5. **Caderno de 19/10 recuperado:** [CADERNO_RMRP_INTEGRADO_34_MUNICIPIOS_2026_10_19.md](https://drive.google.com/file/d/1Pw0Zft2h68IP0lvM5v8KtZ5WNHvssp5v/view), ID `1Pw0Zft2h68IP0lvM5v8KtZ5WNHvssp5v`, versão antecedente, não canônica atual.
6. **Fonte cartográfica matriz:** [RMRP_VOLUME_PUBLICO_MAPAS_E_ANALISES_16_INDICADORES_2026_10_19.pdf](https://drive.google.com/file/d/10vbnQ_eBNsSmpWekFrrgJyeyTeNlm3YN/view), ID `10vbnQ_eBNsSmpWekFrrgJyeyTeNlm3YN`: quatro mosaicos originais 3000×2500 px nas páginas 2,3,6,7. README registra 16 recortes individuais sem reamostragem, mas seus caminhos locais não devem ser presumidos persistentes.

**Decisões de montagem:** preservar 51 tabelas, 34 fichas e cobertura dos 16 indicadores cartográficos; usar mapas ampliados *nos capítulos correspondentes*, sem atlas separado. Antes de promover a prova de quatro imagens, resolver o acesso/posicionamento dos outros 12 mapas; evitar substituir o documento principal automaticamente. QA de paginação, legendas, fontes, escalas e impressão obrigatória. Nenhuma edição nativa ou publicação efetuada nesta diligência.


## Conferência estrutural nativa executada — 28/10/2026
Leitura direta pela API Google Docs, sem alteração (revisões observadas preservadas no inventário de execução):

| Documento | ID | Elementos do corpo | Tabelas nativas | Objetos de imagem | Aba |
|---|---|---:|---:|---:|---|
| Minuta editorial 23/10 | `1UXpfCAllRc84nj49yeRyT14H2Neij_S8elZzq79MxyY` | 342 | 35 | 2 | `t.0` |
| Consolidado 23/10 | `1-M-HKvexFFra_k7j-R_kXAzd5BzfSl1q4A3E_BbxU5s` | 621 | 51 | 4 | `t.0` |
| Prova cartográfica 25/10 | `1FF5nX64MwOcX3oF5SKIl72w-4zG0MD74tzmtFsyMxAg` | 622 | 51 | 4 | `t.0` |

**Interpretação:** o arquivo chamado 'minuta editorial principal' no README de continuidade é estruturalmente menor que o consolidado e a prova de 25/10. Não o promover nem utilizá-lo para sobrescrever as versões mais completas sem conciliar editorialmente as diferenças. A cópia de prova de 25/10 preserva 51 tabelas/4 imagens e é o suporte recomendado para futuras edições cartográficas experimentais, respeitada a integridade da fonte consolidada e a necessidade de cobertura dos 16 indicadores. A conferência nativa não substitui renderização nem teste de impressão.

**Plano de preservação dos 16 indicadores:** manter os quatro mapas ampliados atuais como figuras de leitura principal, selecionar os demais 12 e inserir por blocos temáticos no ponto de discussão correspondente ou como material complementar diretamente vinculado à seção (sem atlas autônomo); conservar referência e acesso à matriz original completa de 16 mapas. Fazer qualquer inclusão em **nova cópia de teste** para não degradar a prova validada. Conferir ao fim 51 tabelas, 34 fichas, índices de objetos, legenda/citação e paginação. Não publicar, promover nem modificar originais nesta fase.


### Cópia de trabalho nativa criada e validada — 28/10/2026
- Criada a partir da prova de 25/10, sem alterar qualquer original: [RMRP — Trabalho cartográfico 16 indicadores — 28-10-2026](https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit), ID `19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI`.
- Leitura nativa após a cópia: **51 tabelas, 4 objetos de imagem, 622 elementos de corpo, aba `t.0`**, idêntica à estrutura contada na prova de origem. A cópia constitui ambiente de trabalho, não uma versão homologada; ainda não contém 16 mapas individuais nem foi submetida a nova prova de impressão.
- Próximo passo é inserir *seletivamente* os mapas remanescentes com legendas compatíveis e inspecionar a renderização. Não substituir automaticamente os quatro mapas já bem posicionados nem eliminar o acesso ao mosaico original de 16 indicadores.
