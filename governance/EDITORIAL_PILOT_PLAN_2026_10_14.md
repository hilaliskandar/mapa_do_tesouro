# Plano de retomada editorial — Finanças Municipais SP

Data: 2026-10-14. Estado: plano operacional; publicação NÃO autorizada por este documento.

## Ponto de partida confirmado
- Repositório de referência: `hilaliskandar/mapa_do_tesouro`, branch `main`.
- Release registrada: `v0.4.0` (2026-10-09), Cloudflare Pages, API editorial estática v1.
- 13 universos analíticos no painel e 11 universos editoriais.
- 287 contextos município × universo.
- Baseline `TIC_TIM_30` preservado para regressão e rollback.
- P0/P1/P2 de expansão estadual concluídos segundo `governance/PROJECT_STATE.md`.
- `governance/PENDING_TASKS.md` encontra-se desatualizado na seção de prioridade corrente (ainda aponta v0.3.1); atualizar antes de novo release.

## Próximo gate editorial — E1, edição de referência piloto

### E1.1 Integridade do contrato público
1. Recuperar `/data/api/v1/publication/universes.json`.
2. Conferir 11 universos editoriais e unicidade de `publication_id`.
3. Conferir 287 contextos municipais indexados, inclusive sobreposições.
4. Registrar URL, horário, identificadores de build, hashes e resultados; não presumir disponibilidade a partir do README.
5. Validar um `context.json` com `scripts/validate_context.py universe`.

### E1.2 Caderno-piloto
Escolher como primeiro piloto o universo editorial correspondente à Região Metropolitana de Jundiaí, após identificar seu `publication_id` no índice. É uma escolha editorial proposta, não um identificador verificado.

Estrutura:
1. Apresentação e escopo do universo;
2. Panorama fiscal e cobertura;
3. Receitas e autonomia;
4. Despesas e investimento;
5. Funções territoriais;
6. Endividamento, liquidez e CAPAG;
7. Distribuição intragrupo: mediana, quartis e extremos;
8. Fichas municipais;
9. Dicionário, fontes e cautelas.

### E1.3 Regras editoriais obrigatórias
- Usar somente variáveis observadas no contexto de produção validado.
- Distinguir `observado`, `ausente`, `nao_aplicavel` e `em_revisao`.
- Não reconstituir indicadores legais com proxies.
- Não classificar desempenho a partir de rankings, percentis ou notas CAPAG.
- Não tomar soma de municípios observados por total do universo sem cobertura suficiente e explicitada.
- Distinguir agregados analíticos de demonstrativos oficiais.
- Para `despesa_territorial`, preservar `strict_complete` e a ausência se algum dos cinco componentes faltar.
- Identificar ano, universo, estatística, número observado/esperado e versão de dados em cada quadro.
- Revisar individualmente afirmações interpretativas; correlação e posição não demonstram causalidade.

### E1.4 QA editorial
- [ ] Contrato do índice e do contexto validado.
- [ ] Coberturas e exclusões verificadas.
- [ ] Todos os números do texto reconciliados com JSON de origem.
- [ ] Medianas e quartis comparados somente dentro do mesmo universo/ano.
- [ ] Links de fonte e versão presentes.
- [ ] Nenhuma ausência tratada como zero.
- [ ] Fichas municipais consistentes com análise transversal.
- [ ] Revisão autoral, metodológica e de legibilidade concluída.
- [ ] Artefato piloto arquivado com SHA-256 e manifesto.
- [ ] Publicação externa condicionada a aprovação específica.

## Gate E2 — congelamento do modelo
Somente após E1 aprovado: congelar template editorial, regras de narrativa e QA, expandindo gradualmente para os demais 10 universos.

## Limitação desta retomada
Em 2026-10-14, o acesso direto ao JSON público não pôde ser confirmado no ambiente de execução utilizado. Portanto, este documento não declara o caderno produzido, os valores conferidos ou publicação realizada.
