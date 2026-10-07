PRAGMA foreign_keys = ON;

INSERT INTO schema_metadata(key, value)
VALUES ('schema_version', '0.2.0')
ON CONFLICT(key) DO UPDATE SET value=excluded.value;

CREATE TABLE IF NOT EXISTS artefato_fonte (
    artefato_id TEXT PRIMARY KEY,
    fonte_id TEXT NOT NULL REFERENCES fonte(fonte_id),
    nome TEXT NOT NULL,
    source_version TEXT,
    url TEXT,
    retrieved_at TEXT,
    sha256 TEXT,
    mime_type TEXT,
    observacao TEXT,
    UNIQUE (fonte_id, sha256)
);

CREATE TABLE IF NOT EXISTS observacao_proveniencia (
    codigo_ibge TEXT NOT NULL,
    ano INTEGER NOT NULL,
    variavel_id TEXT NOT NULL,
    sequencia INTEGER NOT NULL CHECK (sequencia >= 1),
    tipo TEXT NOT NULL
        CHECK (tipo IN ('campo_fonte','observacao','regra')),
    artefato_id TEXT REFERENCES artefato_fonte(artefato_id),
    origem_codigo_ibge TEXT REFERENCES municipio(codigo_ibge),
    origem_ano INTEGER,
    origem_variavel_id TEXT REFERENCES variavel(variavel_id),
    origem_aba TEXT,
    origem_campo TEXT,
    origem_referencia TEXT,
    regra_transformacao TEXT,
    build_id TEXT REFERENCES build(build_id),
    PRIMARY KEY (codigo_ibge, ano, variavel_id, sequencia),
    FOREIGN KEY (codigo_ibge, ano, variavel_id)
        REFERENCES observacao(codigo_ibge, ano, variavel_id)
        ON DELETE CASCADE,
    CHECK (
        (
            tipo='campo_fonte'
            AND artefato_id IS NOT NULL
            AND origem_variavel_id IS NULL
        )
        OR
        (
            tipo='observacao'
            AND artefato_id IS NULL
            AND origem_codigo_ibge IS NOT NULL
            AND origem_ano IS NOT NULL
            AND origem_variavel_id IS NOT NULL
        )
        OR
        (
            tipo='regra'
            AND artefato_id IS NULL
            AND origem_variavel_id IS NULL
            AND regra_transformacao IS NOT NULL
        )
    )
);

CREATE INDEX IF NOT EXISTS idx_artefato_fonte_sha
    ON artefato_fonte (sha256);

CREATE INDEX IF NOT EXISTS idx_proveniencia_origem_variavel
    ON observacao_proveniencia (
        origem_variavel_id,
        origem_codigo_ibge,
        origem_ano
    );

CREATE INDEX IF NOT EXISTS idx_proveniencia_artefato
    ON observacao_proveniencia (artefato_id);

CREATE VIEW IF NOT EXISTS v_observacao_proveniencia AS
SELECT
    p.codigo_ibge,
    m.nome AS municipio,
    p.ano,
    p.variavel_id,
    v.nome AS variavel,
    p.sequencia,
    p.tipo,
    p.artefato_id,
    a.nome AS artefato,
    a.sha256 AS artefato_sha256,
    p.origem_codigo_ibge,
    p.origem_ano,
    p.origem_variavel_id,
    vo.nome AS origem_variavel,
    p.origem_aba,
    p.origem_campo,
    p.origem_referencia,
    p.regra_transformacao,
    p.build_id
FROM observacao_proveniencia p
JOIN municipio m
  ON m.codigo_ibge=p.codigo_ibge
JOIN variavel v
  ON v.variavel_id=p.variavel_id
LEFT JOIN artefato_fonte a
  ON a.artefato_id=p.artefato_id
LEFT JOIN variavel vo
  ON vo.variavel_id=p.origem_variavel_id;
