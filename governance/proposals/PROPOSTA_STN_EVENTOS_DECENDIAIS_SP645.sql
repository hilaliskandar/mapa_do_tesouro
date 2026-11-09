-- FED01 DRAFT ONLY - NOT AN AUTOMATIC MIGRATION.
-- Source: STN cash-basis municipal constitutional transfers, monthly with three decendial columns.
-- Do not move to data/schema without versioned review and read-only regression.
-- sqlite3 foreign_keys ON. Intended to extend existing municipio table.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS stn_transferencia_lote (
    lote_id TEXT PRIMARY KEY,
    fonte_sistema TEXT NOT NULL CHECK(fonte_sistema='STN_CKAN'),
    resource_id TEXT NOT NULL,
    recurso_nome TEXT,
    competencia_ano INTEGER NOT NULL CHECK(competencia_ano BETWEEN 1997 AND 2200),
    competencia_mes INTEGER NOT NULL CHECK(competencia_mes BETWEEN 1 AND 12),
    source_sha256 TEXT NOT NULL CHECK(length(source_sha256)=64),
    r2_object_key TEXT NOT NULL,
    qa_territorial TEXT NOT NULL DEFAULT 'candidate'
        CHECK(qa_territorial IN ('candidate','approved','rejected')),
    qa_contabil TEXT NOT NULL DEFAULT 'candidate'
        CHECK(qa_contabil IN ('candidate','approved','rejected')),
    criado_em_utc TEXT NOT NULL,
    notes TEXT,
    UNIQUE(resource_id,source_sha256)
);

CREATE TABLE IF NOT EXISTS stn_transferencia_item_decendial (
    lote_id TEXT NOT NULL
        REFERENCES stn_transferencia_lote(lote_id) ON DELETE RESTRICT,
    codigo_ibge TEXT NOT NULL
        REFERENCES municipio(codigo_ibge) ON DELETE RESTRICT,
    municipio_nome_origem TEXT NOT NULL,
    transferencia_origem TEXT NOT NULL,
    item_origem TEXT NOT NULL,
    decendio_1_raw TEXT NOT NULL,
    decendio_2_raw TEXT NOT NULL,
    decendio_3_raw TEXT NOT NULL,
    status_semantico TEXT NOT NULL DEFAULT 'em_revisao'
        CHECK(status_semantico IN ('em_revisao','documentado','rejeitado')),
    natureza_operacao TEXT
        CHECK(natureza_operacao IS NULL OR natureza_operacao IN (
          'principal','componente','deducao','ajuste','complementacao','outro'
        )),
    regra_classificacao_id TEXT,
    PRIMARY KEY(lote_id,codigo_ibge,transferencia_origem,item_origem),
    CHECK(length(codigo_ibge)=7),
    CHECK(status_semantico!='documentado'
          OR (natureza_operacao IS NOT NULL AND regra_classificacao_id IS NOT NULL))
);

CREATE INDEX IF NOT EXISTS idx_stn_item_cod_lote
    ON stn_transferencia_item_decendial(codigo_ibge,lote_id);
CREATE INDEX IF NOT EXISTS idx_stn_item_rubrica
    ON stn_transferencia_item_decendial(transferencia_origem,item_origem);

-- No view of summed amounts or implicit publication from the candidates.
-- No modification of observacao, variavel, v_observacao_publicavel or regional universes.
