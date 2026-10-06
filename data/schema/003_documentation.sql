PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS variavel_documentacao (
    variavel_id TEXT PRIMARY KEY REFERENCES variavel(variavel_id),
    titulo_publico TEXT NOT NULL,
    unidade_publica TEXT,
    formula_publica TEXT,
    componentes_publicos TEXT,
    fonte_publica TEXT,
    periodo_publico TEXT,
    como_ler TEXT NOT NULL,
    limitacoes TEXT,
    regra_ausencia TEXT,
    url_fonte TEXT,
    grupo_publico TEXT,
    natureza_publica TEXT,
    ordem_prioridade INTEGER,
    origem_documental TEXT NOT NULL,
    documentation_version TEXT NOT NULL,
    atualizado_em TEXT
);

CREATE TABLE IF NOT EXISTS documentacao_secao (
    secao_id TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    resumo TEXT,
    corpo_markdown TEXT NOT NULL,
    ordem INTEGER NOT NULL DEFAULT 100,
    publico INTEGER NOT NULL DEFAULT 1 CHECK (publico IN (0,1)),
    origem_documental TEXT,
    documentation_version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS referencia_documental (
    referencia_id TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    url TEXT,
    descricao TEXT,
    tipo TEXT NOT NULL DEFAULT 'fonte',
    origem_documental TEXT,
    documentation_version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS variavel_referencia (
    variavel_id TEXT NOT NULL REFERENCES variavel(variavel_id),
    referencia_id TEXT NOT NULL REFERENCES referencia_documental(referencia_id),
    papel TEXT NOT NULL DEFAULT 'fonte'
        CHECK (papel IN ('fonte','metodologia','norma','apoio','crosswalk')),
    PRIMARY KEY (variavel_id, referencia_id, papel)
);

CREATE VIEW IF NOT EXISTS v_catalogo_publico AS
SELECT
    v.variavel_id,
    v.nome AS nome_tecnico,
    v.tipo,
    v.grupo AS grupo_tecnico,
    v.unidade AS unidade_tecnica,
    v.formula AS formula_tecnica,
    d.titulo_publico,
    d.unidade_publica,
    d.formula_publica,
    d.componentes_publicos,
    d.fonte_publica,
    d.periodo_publico,
    d.como_ler,
    d.limitacoes,
    d.regra_ausencia,
    d.url_fonte,
    d.grupo_publico,
    d.natureza_publica,
    d.ordem_prioridade,
    d.documentation_version
FROM variavel v
LEFT JOIN variavel_documentacao d USING (variavel_id);
