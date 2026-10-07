PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS janela_analitica (
    janela_id TEXT PRIMARY KEY,
    ano_inicio INTEGER NOT NULL,
    ano_fim INTEGER NOT NULL,
    descricao TEXT,
    CHECK (ano_fim >= ano_inicio)
);

CREATE TABLE IF NOT EXISTS metrica_janela (
    metrica_id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    unidade TEXT,
    definicao TEXT NOT NULL,
    direcao TEXT,
    observacao TEXT
);

CREATE TABLE IF NOT EXISTS estatistica_janela (
    codigo_ibge TEXT NOT NULL REFERENCES municipio(codigo_ibge),
    universo_id TEXT NOT NULL REFERENCES universo(universo_id),
    variavel_id TEXT NOT NULL REFERENCES variavel(variavel_id),
    janela_id TEXT NOT NULL REFERENCES janela_analitica(janela_id),
    metrica_id TEXT NOT NULL REFERENCES metrica_janela(metrica_id),
    valor_num REAL,
    status TEXT NOT NULL DEFAULT 'observado'
        CHECK (status IN ('observado','ausente','nao_aplicavel','em_revisao')),
    n_observacoes INTEGER,
    build_id TEXT REFERENCES build(build_id),
    PRIMARY KEY (codigo_ibge, universo_id, variavel_id, janela_id, metrica_id),
    CHECK (
        (status='observado' AND valor_num IS NOT NULL)
        OR
        (status<>'observado' AND valor_num IS NULL)
    )
);

CREATE TABLE IF NOT EXISTS dimensao_tipologia (
    dimensao_id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    variavel_id TEXT NOT NULL REFERENCES variavel(variavel_id),
    sentido_interpretativo TEXT NOT NULL CHECK (sentido_interpretativo IN ('maior','menor','neutro')),
    min_anos_observados INTEGER NOT NULL DEFAULT 3 CHECK (min_anos_observados >= 1),
    regra_nivel TEXT NOT NULL,
    regra_estabilidade TEXT NOT NULL,
    observacao TEXT
);

CREATE TABLE IF NOT EXISTS classificacao_relativa (
    codigo_ibge TEXT NOT NULL REFERENCES municipio(codigo_ibge),
    universo_id TEXT NOT NULL REFERENCES universo(universo_id),
    dimensao_id TEXT NOT NULL REFERENCES dimensao_tipologia(dimensao_id),
    janela_id TEXT NOT NULL REFERENCES janela_analitica(janela_id),
    media REAL,
    cv REAL,
    n_anos INTEGER,
    mediana_nivel REAL,
    mediana_cv REAL,
    nivel_relativo TEXT,
    estabilidade TEXT,
    quadrante TEXT,
    status TEXT NOT NULL DEFAULT 'observado'
        CHECK (status IN ('observado','ausente','nao_aplicavel','sem_classificacao','em_revisao')),
    build_id TEXT REFERENCES build(build_id),
    PRIMARY KEY (codigo_ibge, universo_id, dimensao_id, janela_id)
);

CREATE TABLE IF NOT EXISTS marcador_comparavel (
    codigo_ibge TEXT NOT NULL REFERENCES municipio(codigo_ibge),
    universo_id TEXT NOT NULL REFERENCES universo(universo_id),
    janela_id TEXT NOT NULL REFERENCES janela_analitica(janela_id),
    marcador_id TEXT NOT NULL,
    valor_texto TEXT,
    status TEXT NOT NULL DEFAULT 'observado'
        CHECK (status IN ('observado','ausente','sem_classificacao','em_revisao')),
    build_id TEXT REFERENCES build(build_id),
    PRIMARY KEY (codigo_ibge, universo_id, janela_id, marcador_id)
);

CREATE TABLE IF NOT EXISTS par_municipal (
    codigo_ibge_referencia TEXT NOT NULL REFERENCES municipio(codigo_ibge),
    codigo_ibge_comparado TEXT NOT NULL REFERENCES municipio(codigo_ibge),
    universo_id TEXT NOT NULL REFERENCES universo(universo_id),
    janela_id TEXT NOT NULL REFERENCES janela_analitica(janela_id),
    dimensoes_comparaveis INTEGER NOT NULL,
    dimensoes_coincidentes INTEGER NOT NULL,
    proporcao_coincidencia REAL NOT NULL,
    ordem_prioritaria INTEGER,
    reciproco INTEGER NOT NULL DEFAULT 0 CHECK (reciproco IN (0,1)),
    dimensoes_coincidentes_lista TEXT,
    observacao TEXT,
    build_id TEXT REFERENCES build(build_id),
    PRIMARY KEY (
        codigo_ibge_referencia,
        codigo_ibge_comparado,
        universo_id,
        janela_id
    ),
    CHECK (dimensoes_comparaveis >= 0),
    CHECK (dimensoes_coincidentes >= 0),
    CHECK (dimensoes_coincidentes <= dimensoes_comparaveis),
    CHECK (proporcao_coincidencia BETWEEN 0 AND 1)
);

CREATE INDEX IF NOT EXISTS idx_estatistica_janela_variavel
    ON estatistica_janela (variavel_id, janela_id, universo_id);

CREATE INDEX IF NOT EXISTS idx_classificacao_dimensao
    ON classificacao_relativa (dimensao_id, janela_id, universo_id);

CREATE INDEX IF NOT EXISTS idx_par_prioritario
    ON par_municipal (codigo_ibge_referencia, ordem_prioritaria);

INSERT OR IGNORE INTO janela_analitica(
    janela_id,ano_inicio,ano_fim,descricao
) VALUES (
    '2021_2025',2021,2025,
    'Janela de cinco exercicios usada para medias, volatilidade, mudanca e perfis relativos.'
);

INSERT OR IGNORE INTO metrica_janela(metrica_id,nome,unidade,definicao) VALUES
('media','Media da janela',NULL,'Media aritmetica dos valores observados na janela.'),
('desvio','Desvio-padrao',NULL,'Desvio-padrao amostral dos valores observados; requer pelo menos duas observacoes.'),
('cv','Coeficiente de variacao','razao','Desvio-padrao dividido pelo valor absoluto da media; vazio quando media zero ou observacoes insuficientes.'),
('mudanca','Mudanca ponta a ponta',NULL,'Valor do ultimo exercicio menos valor do primeiro exercicio, quando ambos observados.'),
('amplitude','Amplitude da janela',NULL,'Maior valor observado menos menor valor observado na janela.'),
('anos_acima_mediana_grupo','Anos acima ou iguais a mediana do grupo','anos','Numero de exercicios da janela em que o municipio apresentou valor igual ou superior a mediana do universo.'),
('rank_media_desc','Posicao pela media decrescente','posicao','Posicao relativa pela media da janela; maior media recebe posicao 1. Nao e nota de desempenho.');
