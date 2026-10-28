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
