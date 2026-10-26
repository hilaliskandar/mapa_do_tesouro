-- Complementary TCESP investments: independent of DCA/FINBRA canonical observations.
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS tcesp_lote (
 lote_id TEXT PRIMARY KEY, exercicio INTEGER NOT NULL, source_sha256 TEXT NOT NULL,
 artifact_run INTEGER NOT NULL, qa_status TEXT NOT NULL CHECK(qa_status='pass'),
 imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 UNIQUE(exercicio,source_sha256)
);
CREATE TABLE IF NOT EXISTS tcesp_investimento_programa (
 lote_id TEXT NOT NULL REFERENCES tcesp_lote(lote_id),
 codigo_ibge TEXT NOT NULL REFERENCES municipio(codigo_ibge),
 mes INTEGER NOT NULL CHECK(mes BETWEEN 1 AND 12),
 estagio TEXT NOT NULL, orgao TEXT NOT NULL, cd_programa TEXT NOT NULL,
 ds_programa TEXT NOT NULL, valor_centavos INTEGER NOT NULL,
 PRIMARY KEY(lote_id,codigo_ibge,mes,estagio,orgao,cd_programa,ds_programa)
);
CREATE TABLE IF NOT EXISTS tcesp_investimento_acao (
 lote_id TEXT NOT NULL REFERENCES tcesp_lote(lote_id),
 codigo_ibge TEXT NOT NULL REFERENCES municipio(codigo_ibge),
 mes INTEGER NOT NULL CHECK(mes BETWEEN 1 AND 12),
 estagio TEXT NOT NULL, orgao TEXT NOT NULL, cd_programa TEXT NOT NULL,
 ds_programa TEXT NOT NULL, cd_acao TEXT NOT NULL, ds_acao TEXT NOT NULL,
 valor_centavos INTEGER NOT NULL,
 PRIMARY KEY(lote_id,codigo_ibge,mes,estagio,orgao,cd_programa,ds_programa,cd_acao,ds_acao)
);
CREATE INDEX IF NOT EXISTS idx_tcesp_prog_city_year ON tcesp_investimento_programa(codigo_ibge,lote_id,estagio);
CREATE INDEX IF NOT EXISTS idx_tcesp_acao_city_year ON tcesp_investimento_acao(codigo_ibge,lote_id,estagio);
CREATE VIEW IF NOT EXISTS v_tcesp_investimento_municipal AS
SELECT l.exercicio,p.codigo_ibge,p.estagio,SUM(p.valor_centavos) AS valor_centavos
FROM tcesp_investimento_programa p JOIN tcesp_lote l ON l.lote_id=p.lote_id
GROUP BY l.exercicio,p.codigo_ibge,p.estagio;
