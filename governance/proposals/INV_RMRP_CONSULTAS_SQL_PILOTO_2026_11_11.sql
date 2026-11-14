-- CONSULTAS PROPOSTAS, NAO EXECUTADAS / NAO PUBLICADAS.
-- Requer migracao de desenvolvimento: INV_RMRP_SCHEMA_EXTENSAO_SQLITE_2026_11_11.sql
-- Filtros :codigo_ibge, :ano, :setor, :estagio, :estagio_tcesp e :universo_id.
-- Todos os eventos de valor devem ter QA homologado; centavos inteiros.
-- NUNCA somar valores 'previsto'+'empenhado'+'transferido'+'liquidado'+'pago'.

-- Q1: projetos por municipio de EXECUCAO, nao pela sede de convenente.
SELECT p.projeto_id, p.titulo, p.setor, p.natureza_intervencao,
       p.situacao_cadastral, pm.qualidade AS qualidade_localizacao,
       (SELECT COUNT(*) FROM inv_localizacao g WHERE g.projeto_id=p.projeto_id) AS pontos,
       (SELECT COUNT(*) FROM inv_projeto_instrumento pi
        WHERE pi.projeto_id=p.projeto_id AND pi.qa_status='homologado') AS instrumentos_comprovados
FROM inv_projeto p
JOIN inv_projeto_municipio pm ON pm.projeto_id=p.projeto_id
WHERE pm.codigo_ibge=:codigo_ibge
  AND pm.papel='local_execucao'
  AND p.qa_status='homologado'
  AND (:setor IS NULL OR p.setor=:setor)
ORDER BY p.setor, p.titulo, p.projeto_id;

-- Q2: série de eventos de um projeto, estagio visivel, sem converter empenho em pagamento.
SELECT e.data_evento, e.ano_competencia, e.fonte_sistema,
       e.documento_origem, e.natureza_fluxo, e.natureza_despesa,
       e.estagio, e.valor_centavos, a.url AS url_artefato
FROM inv_evento_financeiro e
JOIN artefato_fonte a ON a.artefato_id=e.artefato_id
WHERE e.projeto_id=:projeto_id AND e.qa_status='homologado'
ORDER BY COALESCE(e.data_evento,'9999-12-31'), e.evento_id;

-- Q3: pagamentos EXECUTADOS diretamente por ente, sem incluir transferencias intergovernamentais
-- e sem somar recursos previstos, empenhos, estornos separados.
SELECT m.codigo_ibge,m.nome,e.ano_competencia,
       a.tipo_ente AS nivel_pagador,
       e.natureza_fluxo,e.estagio,
       SUM(e.valor_centavos) AS total_centavos,
       COUNT(*) AS quantidade_documentos
FROM inv_evento_financeiro e
JOIN inv_projeto p ON p.projeto_id=e.projeto_id
JOIN inv_projeto_municipio pm ON pm.projeto_id=p.projeto_id
JOIN municipio m ON m.codigo_ibge=pm.codigo_ibge
LEFT JOIN inv_ator a ON a.ator_id=e.pagador_ator_id
WHERE pm.papel='local_execucao' AND pm.codigo_ibge=:codigo_ibge
  AND pm.qualidade IN ('identificador_oficial','intersecao_geometrica','documento')
  AND e.qa_status='homologado' AND p.qa_status='homologado'
  AND e.ano_competencia=:ano
  AND e.natureza_despesa='investimento'
  AND e.natureza_fluxo='execucao_direta'
  AND e.estagio='pago'
  AND (SELECT COUNT(*) FROM inv_projeto_municipio px
       WHERE px.projeto_id=p.projeto_id AND px.papel='local_execucao')=1
GROUP BY m.codigo_ibge,m.nome,e.ano_competencia,a.tipo_ente,
         e.natureza_fluxo,e.estagio;

-- Q4: valor de repasses efetivamente transferidos a recebedores identificados,
-- evento distinto e NUNCA adicionado ao Q3 como gasto final independente.
SELECT e.ano_competencia,ap.tipo_ente AS origem,
       ar.tipo_ente AS nivel_beneficiario, e.fonte_sistema,
       SUM(e.valor_centavos) AS transferencias_centavos
FROM inv_evento_financeiro e
JOIN inv_ator ap ON ap.ator_id=e.pagador_ator_id
JOIN inv_ator ar ON ar.ator_id=e.recebedor_ator_id
WHERE e.qa_status='homologado' AND e.estagio='transferido'
  AND e.natureza_fluxo='transferencia_intergovernamental'
  AND e.ano_competencia=:ano
  AND ar.codigo_ibge_sede=:codigo_ibge
GROUP BY e.ano_competencia,ap.tipo_ente,ar.tipo_ente,e.fonte_sistema;
-- ATENCAO: codigo_ibge_sede e apenas do ator; Q4 nao prova local da obra.
-- O dashboard deve rotular "recebido por ente sediado" salvo prova explicita
-- de credito ao ente municipal ou vinculo de destino juridico.

-- Q5: despesa de investimento municipal TCESP EXISTENTE como comparação fiscal,
-- nunca incorporada novamente como evento financeiro federal.
SELECT l.exercicio,p.codigo_ibge,p.estagio,
       SUM(p.valor_centavos) AS valor_centavos
FROM tcesp_investimento_programa p
JOIN tcesp_lote l ON l.lote_id=p.lote_id
WHERE p.codigo_ibge=:codigo_ibge AND l.exercicio=:ano
  AND p.estagio=:estagio_tcesp
GROUP BY l.exercicio,p.codigo_ibge,p.estagio;

-- Q6: cobertura de municipios no universo regional contra projetos homologados.
SELECT um.codigo_ibge,m.nome,
       COUNT(DISTINCT CASE WHEN p.qa_status='homologado' THEN p.projeto_id END) AS projetos_homologados,
       COUNT(DISTINCT CASE WHEN pm.qualidade='inferido_revisao'
                             THEN p.projeto_id END) AS projetos_localizacao_em_revisao
FROM universo_municipio um
JOIN municipio m ON m.codigo_ibge=um.codigo_ibge
LEFT JOIN inv_projeto_municipio pm
  ON pm.codigo_ibge=um.codigo_ibge AND pm.papel='local_execucao'
LEFT JOIN inv_projeto p ON p.projeto_id=pm.projeto_id
WHERE um.universo_id=:universo_id
GROUP BY um.codigo_ibge,m.nome
ORDER BY m.nome;

-- Q7: lista de itens para QA: vínculo fraco, geografia e pagamento.
SELECT p.projeto_id,p.titulo,pm.codigo_ibge,pm.qualidade,
       pi.instrumento_id,pi.tipo_vinculo,pi.qa_status AS qa_vinculo
FROM inv_projeto p
JOIN inv_projeto_municipio pm ON pm.projeto_id=p.projeto_id
LEFT JOIN inv_projeto_instrumento pi ON pi.projeto_id=p.projeto_id
WHERE pm.qualidade='inferido_revisao'
   OR pi.qa_status IN ('em_revisao','rejeitado')
ORDER BY p.projeto_id,pi.instrumento_id;
