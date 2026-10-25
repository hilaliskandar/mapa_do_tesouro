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

## Requisito obrigatório — investimentos por programa e ação

A integração estadual TCESP deve preservar a **decomposição dos investimentos por programa e ação orçamentária** como dado de primeira classe, não apenas o agregado do grupo 44. Este requisito se aplica a todos os municípios e exercícios disponíveis (2023–2026, sendo 2026 parcial e identificado por meses presentes).

Granularidade recomendada: `codigo_ibge, exercicio, mes_referencia, orgao, unidade_orcamentaria, funcao, subfuncao, codigo_programa, descricao_programa, codigo_acao, descricao_acao, tipo_acao, classificacao_natureza, fonte_recurso, estagio_despesa, valor_centavos, proveniencia`, **somente para dimensões efetivamente presentes no arquivo original**. Campos não publicados pela fonte permanecem nulos; não inferir códigos ou a classificação projeto/atividade/operação especial a partir do nome.

Manter separados empenhos, liquidações, pagamentos, reforços e anulações conforme a semântica e o sinal do registro TCESP; **não somar movimentações heterogêneas**. Identificar investimentos de maneira auditável, respeitando o grupo de natureza `44` e verificando o layout do arquivo para não confundir o código com outra classificação.

Controle obrigatório por município/ano/mês/estágio:
1. Soma dos programas = soma das ações = agregado de investimento na mesma base, filtro e estágio.
2. Chaves de programa/ação incluem escopo institucional e exercício, pois códigos locais podem ser reutilizados.
3. A classificação da ação e a descrição original são conservadas; agregações de programa e ação não podem apagar o detalhamento.
4. Distinguir ausências, movimentos negativos e dados parciais; reportar discrepâncias em centavos sem correção silenciosa.
5. Usar os 21 extratos da RMJ (2023–2025), com decomposições já reconciliadas, como amostra de regressão; conferir paridade com o arquivo estadual antes de promover seus derivados.
6. Materializar no SQLite tabelas separadas de dimensão programa/ação e fatos de execução TCESP, preservando a DCA/FINBRA canônica. API de análise por programas e ações deve permitir filtros por município, exercício, estágio, órgão e natureza, com proveniência e cobertura explícitas.

**Critério de aceite:** não declarar concluída a importação de investimentos apenas com totais municipais. Exigir reconciliação das ações e programas e preservar a possibilidade de análise detalhada sem nova coleta TCESP.

## Primeiro gate operacional de programas e ações — validado em 25/10/2026
- Script `governance/auditar_investimentos_programas_acoes_2025.py`; workflow `.github/workflows/tcesp-investimentos-programas-acoes-2025.yml`; [execução 40241111155](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40241111155); artifact QA `12616033273`, recuperado e lido.
- Dados de referência: artifact preexistente `rmj-tcesp-2025-full-raw`, run `38719698652`. O job comprovadamente reutilizou esse acervo (sem recalculá-lo para definir resultados esperados).
- **Jundiaí 2025:** 157.171 linhas do ZIP despesas; 19 programas e 71 ações com investimentos liquidados; 13.733.386.984 centavos (R$ 137.333.869,84). Somatório por programa e ação idênticos entre si e ao artifact RMJ de referência, incluindo igualdade de todas as chaves e valores dos desdobramentos. `bad_values=0`.
- **Louveira 2025:** 41.595 linhas; 27 programas e 40 ações; 1.629.685.457 centavos (R$ 16.296.854,57), mesma paridade integral de totais/chaves e valores. `bad_values=0`. Não houve linha de `valor liquidado` do grupo 44 em janeiro; não imputar zero de outras naturezas.
- O script discrimina `empenhado`, `anulação`, `valor pago` e `valor liquidado` e não soma estágios heterogêneos. SHA-256 dos ZIPs originais ficam no QA para versionamento.
- `all_pass=true` nos dois municípios. Resultado demonstra a reprodutibilidade do desdobramento por programa e ação e reduz o risco de regressão frente ao acervo já validado da RMJ; **não comprova ainda o processamento do ZIP estadual completo de despesas, nem a ingestão em R2/SQLite**.
- Próximo teste: identificar as colunas institucionais e classificações do consolidado estadual de despesas 2025 e avaliar ingestão particionada, aproveitando a validação aqui feita como teste de regressão obrigatório.
