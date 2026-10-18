# Gate de integração — API v2 e cadernos metropolitanos

Data do registro: 18/10/2026. Situação: análise de evidências, não homologação nem autorização de publicação.

## Propósito

Vincular produção dos cadernos RM/AU à API fiscal existente, sem reconsultar fontes oficiais durante a fase editorial, sem reconstruir cálculos e sem presumir que o contrato v2 esteja publicado.

## Evidências recuperadas e limites

| Prova | Referência | Resultado | Não demonstra |
|---|---|---|---|
| Contrato proposto | governance/API_COMPLETENESS_V2_PROPOSAL.md | Endpoints catalog, municipalities, universes, coverage, methodology e manifest | Implantação |
| Build canônico | governance/API_V2_REAL_DATA_AUDIT_2026_10_13.md; run 38355047393 | 645 fichas, 13 universos, 75 variáveis, 174795 observações 2021-2025 | Publicação v2 |
| Prontidão | governance/API_V2_READINESS_REBUILD_2026_10_13.md; run 38360896979 | 75 variáveis; 48 cautelas incompletas; 17 percentuais não certificados | Homologação editorial |
| Paridade da importação | governance/API_V2_PERCENT_SCALE_PARITY_2026_10_14.md; run 38562576850 | 11374 valores conciliados; zero divergências de ingestão | Escala final ou comparabilidade |
| Paridade de derivados | governance/API_V2_DERIVED_RATIO_PARITY_2026_10_14.md; run 38589671843 | 5420 razões de 2025 conciliadas; zero divergências | Histórico anterior ou classificação das fontes |
| Proveniência | governance/API_V2_PERCENT_PROVENANCE_2026_10_14.md; run 38593209824 | 3 percentuais com 2021-24 importados e 2025 calculado; 3 RGF importados 2023-25; 11 calculados apenas 2025 | Séries homogêneas |
| Contrato editorial anterior | data/catalogs/publication_variables_v1.yml na main | 50 variáveis | Completude API v2 |
| Catálogo do PR 198 | refs/pull/198/head | 57 variáveis | Merge/deploy |
| Portal público | https://finbra-tic-tim-referencia.pages.dev | URL do portal conhecida | Presença atual da v2, ainda sem verificação independente do payload |

## Regras obrigatórias ao gerador

1. **Somente API/snapshot homologado e congelado**, com commit, versão, URL ou caminho de artefato e hash no manifesto. Nenhuma busca externa na fase de composição editorial.
2. Não misturar v1, v2, PR 198 e dados do boletim RMJ em uma mesma tabela sem reconciliação de versão e definição. Manter separado desenvolvimento, integração, homologação, implantação e acessibilidade.
3. Indicadores percentuais: só mostrar percentuais com evidência individual de storage_scale, display_multiplier, proveniência e janela temporal. Não aplicar 100 automaticamente por nome.
4. Comparações 2021-2025: bloquear série contínua dos 3 indicadores híbridos sem prova de equivalência entre importação e cálculo; indicadores somente 2025 não devem receber histórico inventado.
5. Indicadores legais seguem RGF/RREO/CAPAG e períodos oficiais. CAPAG: ano-base e posição de snapshot distintos.
6. Agregações regionais só são totais integrais quando cobertura observada equivale aos municípios esperados. Para despesa territorial, strict_complete exige cinco funções presentes.
7. Ausente, não aplicável, em revisão e sem registro não são zero; preservar estado e fonte.
8. As perguntas dos cadernos usam respostas apenas quando evidência permite, com identificação de variável, exercício, universo, versão e posição final no PDF.
9. Nenhum gate de publicação é encerrado sem inspeção de payload público e manifesto; CI e deploy aprovados não substituem essa inspeção.

## Critérios de saída do gate

- [x] Localizada evidência documental de build API v2 e suas contagens.
- [x] Identificadas provas parciais dos 17 indicadores percentuais e suas limitações.
- [x] Recuperadas as diferenças de catálogo 50/57 e 75 sem presumir equivalência.
- [ ] Recuperar contrato e manifesto v2 da última construção e registrar hashes por arquivo.
- [ ] Certificar escala/exibição dos 17 indicadores, por origem e exercício.
- [ ] Revisar as 48 cautelas específicas.
- [ ] Certificar homogeneidade temporal ou indicar quebra metodológica.
- [ ] Confirmar qual API está efetivamente acessível/publicada, com conteúdo e build.
- [ ] Elaborar matriz variável × componente do caderno RMJ usando o contrato validado.
- [ ] Regenerar caderno-piloto e executar QA documental, visual e substantivo.
- [ ] Obter autorização separada para eventual release.

## Próxima execução exata

Verificar a última execução de build privada que inclua a API v2, extrair manifest.json, readiness.json e catalog/variables.json, comparar hashes e estados com os registros de 13-14/10; só depois implementar o adaptador de geração do caderno. Preservar o PDF RMJ v3.10 como referência editorial, não como fonte de dados da API.

## Registro de continuidade

O resultado desta execução deve ser acrescentado a README, PROJECT_STATE, INVENTORY e PENDING_TASKS apenas com fatos e evidências. Evitar narrativa de conclusão quando faltarem prova do payload e revisão substantiva.
