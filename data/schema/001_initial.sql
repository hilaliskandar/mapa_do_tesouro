PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT OR IGNORE INTO schema_metadata(key, value) VALUES
    ('schema_version', '0.1.0'),
    ('model', 'long'),
    ('absence_policy', 'absence_is_not_zero');

CREATE TABLE IF NOT EXISTS municipio (
    codigo_ibge TEXT PRIMARY KEY
        CHECK (length(codigo_ibge) = 7 AND codigo_ibge NOT GLOB '*[^0-9]*'),
    nome TEXT NOT NULL,
    uf TEXT NOT NULL CHECK (length(uf) = 2),
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0,1))
);

CREATE TABLE IF NOT EXISTS universo (
    universo_id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    descricao TEXT,
    tipo TEXT NOT NULL DEFAULT 'analitico',
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0,1))
);

CREATE TABLE IF NOT EXISTS universo_municipio (
    universo_id TEXT NOT NULL REFERENCES universo(universo_id),
    codigo_ibge TEXT NOT NULL REFERENCES municipio(codigo_ibge),
    vigencia_inicio INTEGER,
    vigencia_fim INTEGER,
    PRIMARY KEY (universo_id, codigo_ibge),
    CHECK (vigencia_fim IS NULL OR vigencia_inicio IS NULL OR vigencia_fim >= vigencia_inicio)
);

CREATE TABLE IF NOT EXISTS fonte (
    fonte_id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    orgao TEXT,
    sistema TEXT,
    demonstrativo TEXT,
    url_publica TEXT,
    observacao TEXT
);

CREATE TABLE IF NOT EXISTS variavel (
    variavel_id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    grupo TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (
        tipo IN (
            'conta_oficial',
            'agregado_analitico',
            'indicador_derivado',
            'indicador_legal',
            'classificacao_oficial',
            'contextual'
        )
    ),
    natureza TEXT,
    unidade TEXT NOT NULL,
    definicao TEXT NOT NULL,
    formula TEXT,
    como_ler TEXT,
    cautelas TEXT,
    fonte_preferencial_id TEXT REFERENCES fonte(fonte_id),
    periodicidade TEXT NOT NULL DEFAULT 'anual',
    publicavel INTEGER NOT NULL DEFAULT 1 CHECK (publicavel IN (0,1)),
    ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0,1))
);

CREATE TABLE IF NOT EXISTS crosswalk_variavel (
    crosswalk_id INTEGER PRIMARY KEY AUTOINCREMENT,
    variavel_id TEXT NOT NULL REFERENCES variavel(variavel_id),
    ano_inicio INTEGER NOT NULL,
    ano_fim INTEGER NOT NULL,
    fonte_id TEXT NOT NULL REFERENCES fonte(fonte_id),
    demonstrativo TEXT,
    estagio TEXT,
    codigo_conta TEXT,
    descricao_conta TEXT,
    campo_bruto TEXT,
    finalidade TEXT NOT NULL DEFAULT 'indicador'
        CHECK (finalidade IN ('totalizacao','decomposicao','indicador','auditoria')),
    regra_harmonizacao TEXT NOT NULL,
    prioridade INTEGER NOT NULL DEFAULT 100,
    confianca TEXT NOT NULL DEFAULT 'documentada'
        CHECK (confianca IN ('documentada','alta','media','baixa','em_revisao')),
    CHECK (ano_fim >= ano_inicio)
);

CREATE TABLE IF NOT EXISTS observacao (
    codigo_ibge TEXT NOT NULL REFERENCES municipio(codigo_ibge),
    ano INTEGER NOT NULL CHECK (ano BETWEEN 1900 AND 2200),
    variavel_id TEXT NOT NULL REFERENCES variavel(variavel_id),
    fonte_id TEXT REFERENCES fonte(fonte_id),
    valor_num REAL,
    valor_texto TEXT,
    status TEXT NOT NULL DEFAULT 'observado'
        CHECK (status IN ('observado','ausente','nao_aplicavel','em_revisao')),
    referencia_origem TEXT,
    build_id TEXT,
    PRIMARY KEY (codigo_ibge, ano, variavel_id),
    CHECK (
        (status = 'observado' AND ((valor_num IS NOT NULL) <> (valor_texto IS NOT NULL)))
        OR
        (status <> 'observado' AND valor_num IS NULL AND valor_texto IS NULL)
    )
);

CREATE TABLE IF NOT EXISTS cobertura (
    variavel_id TEXT NOT NULL REFERENCES variavel(variavel_id),
    ano INTEGER NOT NULL,
    universo_id TEXT NOT NULL REFERENCES universo(universo_id),
    esperado INTEGER NOT NULL CHECK (esperado >= 0),
    observado INTEGER NOT NULL CHECK (observado >= 0),
    ausente INTEGER NOT NULL CHECK (ausente >= 0),
    nao_aplicavel INTEGER NOT NULL DEFAULT 0 CHECK (nao_aplicavel >= 0),
    PRIMARY KEY (variavel_id, ano, universo_id),
    CHECK (observado + ausente + nao_aplicavel <= esperado)
);

CREATE TABLE IF NOT EXISTS build (
    build_id TEXT PRIMARY KEY,
    build_timestamp TEXT NOT NULL,
    data_version TEXT NOT NULL,
    methodology_version TEXT NOT NULL,
    app_version TEXT,
    schema_version TEXT NOT NULL,
    data_sha256 TEXT NOT NULL,
    qa_status TEXT NOT NULL CHECK (qa_status IN ('candidate','approved','rejected')),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS build_source (
    build_id TEXT NOT NULL REFERENCES build(build_id),
    fonte_id TEXT NOT NULL REFERENCES fonte(fonte_id),
    source_version TEXT,
    retrieved_at TEXT,
    source_sha256 TEXT,
    PRIMARY KEY (build_id, fonte_id)
);

CREATE INDEX IF NOT EXISTS idx_observacao_ano_variavel
    ON observacao (ano, variavel_id);

CREATE INDEX IF NOT EXISTS idx_observacao_municipio_ano
    ON observacao (codigo_ibge, ano);

CREATE INDEX IF NOT EXISTS idx_observacao_variavel_municipio
    ON observacao (variavel_id, codigo_ibge);

CREATE INDEX IF NOT EXISTS idx_crosswalk_variavel_ano
    ON crosswalk_variavel (variavel_id, ano_inicio, ano_fim);

CREATE VIEW IF NOT EXISTS v_observacao_publicavel AS
SELECT
    o.codigo_ibge,
    m.nome AS municipio,
    o.ano,
    o.variavel_id,
    v.nome AS variavel,
    v.grupo,
    v.tipo,
    v.unidade,
    o.valor_num,
    o.valor_texto,
    o.status,
    o.fonte_id,
    o.referencia_origem,
    o.build_id
FROM observacao o
JOIN municipio m USING (codigo_ibge)
JOIN variavel v USING (variavel_id)
WHERE v.publicavel = 1;
