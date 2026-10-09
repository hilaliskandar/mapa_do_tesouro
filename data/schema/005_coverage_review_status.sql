PRAGMA foreign_keys = OFF;

ALTER TABLE cobertura RENAME TO cobertura_legacy;

CREATE TABLE cobertura (
    variavel_id TEXT NOT NULL REFERENCES variavel(variavel_id),
    ano INTEGER NOT NULL,
    universo_id TEXT NOT NULL REFERENCES universo(universo_id),
    esperado INTEGER NOT NULL CHECK (esperado >= 0),
    observado INTEGER NOT NULL CHECK (observado >= 0),
    ausente INTEGER NOT NULL CHECK (ausente >= 0),
    nao_aplicavel INTEGER NOT NULL DEFAULT 0 CHECK (nao_aplicavel >= 0),
    em_revisao INTEGER NOT NULL DEFAULT 0 CHECK (em_revisao >= 0),
    PRIMARY KEY (variavel_id, ano, universo_id),
    CHECK (observado + ausente + nao_aplicavel + em_revisao <= esperado)
);

INSERT INTO cobertura(
    variavel_id,ano,universo_id,esperado,
    observado,ausente,nao_aplicavel,em_revisao
)
SELECT
    variavel_id,ano,universo_id,esperado,
    observado,ausente,nao_aplicavel,0
FROM cobertura_legacy;

DROP TABLE cobertura_legacy;

INSERT OR REPLACE INTO schema_metadata(key, value)
VALUES ('schema_version', '0.3.0');

PRAGMA foreign_keys = ON;
