# Plano de cobertura incremental TCESP na plataforma estadual

Data: 2026-10-25. Estado: DIAGNOSTICO/ARQUITETURA; nenhuma publicacao autorizada.

## Escopo e cobertura demonstrada
- Plataforma: SP_645, FINBRA/Siconfi DCA 2013–2025 ja consolidada na base canônica. TCESP e fonte COMPLEMENTAR, nunca substituicao automatica da DCA.
- RMRP: 34 municipios x 2023–2025 = 102 extratos TCESP previamente coletados e validados; paridade 101/102 versus DCA; Guatapara 2023 difere R$ 10.176,00.
- Sao Carlos: extratos TCESP de despesas e receitas 2023–2026 coletados em 2026-10-25; 2026 somente meses efetivamente presentes. Despesas de 2024 diferem da DCA por aproximadamente R$ 3,16 milhoes.
- NAO existe inventario comprovado de cobertura TCESP permanente de todos os 645 municipios. Nao inferir 610 ausencias como faltantes definitivas sem inspecionar acervos, R2 e outputs existentes.

## Regra de levantamento de lacunas
Inventariar pares (codigo_ibge, ano, dominio: despesas/receitas), nao apenas nomes de municipios; construir roster a partir do catalogo territorial SP_645 aprovado; mapear slug oficial do TCESP com verificacao de identidade. Status por par: `presente_validado`, `presente_nao_validado`, `so_artifact_temporario`, `ausente`, `falha_transitoria`, `indisponivel_na_fonte`, `conflito`.
Antes de qualquer GET TCESP: consultar manifesto permanente no R2; verificar existencia fisica e checksum SHA256; importar/validar acervos existentes RMRP, RMJ e Sao Carlos. Nao confundir arquivo hospedado em GitHub Actions com armazenamento permanente.

## Pipeline incremental proposto
1. Inventario de cobertura (somente leitura, sem download) dos snapshots validados, historicos e artifacts de Actions.
2. Materializar e promover primeiro os 102 pares RMRP ja obtidos, mais Sao Carlos e demais acervos existentes; validar checksums e metadados.
3. Fila `missing-only` por municipio-ano-dominio; particoes controladas para runner `financas-tcesp-wsl2`; retries com limite, checkpoint e reentrancia.
4. Salvar extratos oficiais, agregados por mes/orgao/programa/acao/fonte e codigo de receita, com registro do tipo de movimentacao, hash original, data e versao do extrator. Preservar estruturas detalhadas em armazenamento privado.
5. Aplicar QA de cardinalidade, somas de componentes, impossibilidade de duplicatas, cobertura dos meses e estagios. Registrar divergencias TCESP x DCA sem alterar base principal.
6. Publicar snapshots versionados em R2 privado e manifesto Git versionado; testar leitura e SHA256 apos upload. So entao sinalizar `persistido`.
7. Integrar ao SQLite analitico em tabelas TCESP complementares separadas; gerar JSON estatico particionado por municipio/ano e/ou agregado para API v2. Nova publicacao depende de teste de regressao e decisao explicita.
8. Nova coleta futura: apenas anos novos, registros ausentes e atualizacao intencional de exercicios parciais; nunca reconsultar pares fechados e validados por rotina normal.

## Modelo minimo de registro
`codigo_ibge, municipio, slug_tcesp, ano, dominio, meses_presentes, source_url, source_sha256, normalized_sha256, schema_version, extractor_commit, collected_at, valor_centavos, dca_comparison_status, object_key_r2, persisted_verified_at, qa_status`.

## Persistencia
- Artefatos de GitHub Actions expiram em 30 dias: nao podem ser base da plataforma.
- R2 privado ja existe na arquitetura, usando `deployment/upload_r2_source.py`, `download_r2_source.py` e manifesto em `data/snapshots`.
- Dados completos NAO devem ser versionados no Git. Registrar no Git apenas codigo, testes, manifesto/hashes e indicadores de cobertura.
- Nao colocar credenciais em runners ou repositório; runner de coleta com contents:read. Promocao para R2 por job separado, com permissao controlada e validacao de hashes.

## Proximas verificacoes tecnicas
- Localizar acervo permanente preexistente de TCESP (se houver), inclusive RMJ e RMRP.
- Resolver roster estadual de 645 códigos IBGE e slugs oficiais.
- Verificar contrato de tabela e JSON/API de investimento para nao quebrar consumidores atuais.
- Teste inicial: importar acervo existente de dois municipios, provar reutilizacao sem GET ao TCESP e confirmar ausencia de alteracoes em producao.
- Somente depois autorizar lotes complementares e eventual ampliacao 2026 para os 645 municipios.
