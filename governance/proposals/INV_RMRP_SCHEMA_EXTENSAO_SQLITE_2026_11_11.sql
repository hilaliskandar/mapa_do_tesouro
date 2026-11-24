-- PROPOSTA NAO APLICADA: extensao da base de investimento por empreendimento.
-- Executar somente em copia de desenvolvimento apos QA de schema e fonte.
-- Preserva: observacao, tcesp_lote, tcesp_investimento_acao e suas chaves.
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS inv_projeto (
  projeto_id TEXT PRIMARY KEY,
  titulo TEXT NOT NULL,
  descricao TEXT,
  setor TEXT,
  natureza_intervencao TEXT,
  situacao_cadastral TEXT,
  id_fonte_preferencial TEXT REFERENCES fonte(fonte_id),
  criado_em_origem TEXT,
  atualizado_em_origem TEXT,
  qa_status TEXT NOT NULL DEFAULT 'candidato'
    CHECK(qa_status IN ('candidato','em_revisao','homologado','rejeitado')),
  CHECK(length(projeto_id)>0)
);

CREATE TABLE IF NOT EXISTS inv_identificador_externo (
  sistema TEXT NOT NULL,
  modulo TEXT NOT NULL,
  identificador TEXT NOT NULL,
  projeto_id TEXT NOT NULL REFERENCES inv_projeto(projeto_id),
  artefato_id TEXT REFERENCES artefato_fonte(artefato_id),
  PRIMARY KEY (sistema, modulo, identificador)
);
CREATE INDEX IF NOT EXISTS idx_inv_external_project ON inv_identificador_externo(projeto_id);

CREATE TABLE IF NOT EXISTS inv_ator (
  ator_id TEXT PRIMARY KEY,
  nome TEXT NOT NULL,
  tipo_ente TEXT NOT NULL
    CHECK(tipo_ente IN ('uniao','estado','municipio','estatal','privado','outro','nao_identificado')),
  cnpj TEXT,
  codigo_ibge_sede TEXT REFERENCES municipio(codigo_ibge),
  CHECK(cnpj IS NULL OR (length(cnpj)=14 AND cnpj NOT GLOB '*[^0-9]*'))
);

CREATE TABLE IF NOT EXISTS inv_instrumento (
  instrumento_id TEXT PRIMARY KEY,
  fonte_sistema TEXT NOT NULL,
  fonte_modulo TEXT NOT NULL,
  id_origem TEXT NOT NULL,
  numero_publico TEXT,
  tipo_juridico TEXT,
  objeto TEXT,
  situacao TEXT,
  data_assinatura TEXT,
  data_publicacao TEXT,
  inicio_vigencia TEXT,
  fim_vigencia TEXT,
  concedente_ator_id TEXT REFERENCES inv_ator(ator_id),
  beneficiario_ator_id TEXT REFERENCES inv_ator(ator_id),
  valor_global_centavos INTEGER,
  qa_status TEXT NOT NULL DEFAULT 'candidato'
    CHECK(qa_status IN ('candidato','em_revisao','homologado','rejeitado')),
  UNIQUE(fonte_sistema, fonte_modulo, id_origem)
);

CREATE TABLE IF NOT EXISTS inv_projeto_instrumento (
  projeto_id TEXT NOT NULL REFERENCES inv_projeto(projeto_id),
  instrumento_id TEXT NOT NULL REFERENCES inv_instrumento(instrumento_id),
  tipo_vinculo TEXT NOT NULL
    CHECK(tipo_vinculo IN ('explicito_id','documental','candidato')),
  evidencia TEXT,
  artefato_id TEXT REFERENCES artefato_fonte(artefato_id),
  qa_status TEXT NOT NULL DEFAULT 'em_revisao'
    CHECK(qa_status IN ('em_revisao','homologado','rejeitado')),
  PRIMARY KEY(projeto_id,instrumento_id)
);

CREATE TABLE IF NOT EXISTS inv_projeto_municipio (
  projeto_id TEXT NOT NULL REFERENCES inv_projeto(projeto_id),
  codigo_ibge TEXT NOT NULL REFERENCES municipio(codigo_ibge),
  papel TEXT NOT NULL
    CHECK(papel IN ('local_execucao','abrangencia','beneficiario','recebedor','sede_executor')),
  qualidade TEXT NOT NULL
    CHECK(qualidade IN ('identificador_oficial','intersecao_geometrica','documento','inferido_revisao')),
  percentual_rateio_ppm INTEGER
    CHECK(percentual_rateio_ppm IS NULL OR percentual_rateio_ppm BETWEEN 0 AND 1000000),
  artefato_id TEXT REFERENCES artefato_fonte(artefato_id),
  PRIMARY KEY(projeto_id,codigo_ibge,papel)
);
CREATE INDEX IF NOT EXISTS idx_inv_proj_municipio ON inv_projeto_municipio(codigo_ibge,papel,projeto_id);

CREATE TABLE IF NOT EXISTS inv_localizacao (
  projeto_id TEXT NOT NULL REFERENCES inv_projeto(projeto_id),
  sequencia INTEGER NOT NULL,
  latitude REAL CHECK(latitude IS NULL OR latitude BETWEEN -90 AND 90),
  longitude REAL CHECK(longitude IS NULL OR longitude BETWEEN -180 AND 180),
  descricao TEXT,
  precisao TEXT NOT NULL
    CHECK(precisao IN ('coordenada_fonte','endereco_geocodificado','municipio','regional','indeterminada')),
  crs_origem TEXT,
  artefato_id TEXT REFERENCES artefato_fonte(artefato_id),
  PRIMARY KEY(projeto_id,sequencia)
);

CREATE TABLE IF NOT EXISTS inv_evento_financeiro (
  evento_id TEXT PRIMARY KEY,
  fonte_sistema TEXT NOT NULL,
  fonte_modulo TEXT NOT NULL,
  documento_origem TEXT NOT NULL,
  linha_origem TEXT NOT NULL DEFAULT '',
  data_evento TEXT,
  ano_competencia INTEGER CHECK(ano_competencia IS NULL OR ano_competencia BETWEEN 1900 AND 2200),
  projeto_id TEXT REFERENCES inv_projeto(projeto_id),
  instrumento_id TEXT REFERENCES inv_instrumento(instrumento_id),
  pagador_ator_id TEXT REFERENCES inv_ator(ator_id),
  recebedor_ator_id TEXT REFERENCES inv_ator(ator_id),
  estagio TEXT NOT NULL CHECK(estagio IN
    ('previsto','aprovado','celebrado','empenhado','liquidado','pago','transferido','estornado')),
  natureza_fluxo TEXT NOT NULL CHECK(natureza_fluxo IN
    ('execucao_direta','transferencia_intergovernamental','financiamento','contrapartida','outro')),
  natureza_despesa TEXT NOT NULL CHECK(natureza_despesa IN
    ('investimento','custeio','misto','nao_classificado')),
  valor_centavos INTEGER NOT NULL,
  artefato_id TEXT NOT NULL REFERENCES artefato_fonte(artefato_id),
  qa_status TEXT NOT NULL DEFAULT 'candidato'
    CHECK(qa_status IN ('candidato','em_revisao','homologado','rejeitado')),
  UNIQUE(fonte_sistema,fonte_modulo,documento_origem,linha_origem,estagio),
  CHECK (natureza_fluxo!='transferencia_intergovernamental' OR natureza_despesa IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS idx_inv_evento_projeto_estagio ON inv_evento_financeiro(projeto_id,estagio,ano_competencia);
CREATE INDEX IF NOT EXISTS idx_inv_evento_instrumento ON inv_evento_financeiro(instrumento_id,estagio);
CREATE INDEX IF NOT EXISTS idx_inv_evento_fonte ON inv_evento_financeiro(fonte_sistema,fonte_modulo,ano_competencia);

CREATE TABLE IF NOT EXISTS inv_execucao_fisica (
  sistema TEXT NOT NULL,
  id_origem TEXT NOT NULL,
  projeto_id TEXT NOT NULL REFERENCES inv_projeto(projeto_id),
  data_referencia TEXT,
  situacao TEXT,
  percentual_concluido_bp INTEGER CHECK(percentual_concluido_bp IS NULL OR percentual_concluido_bp BETWEEN 0 AND 10000),
  descricao_marco TEXT,
  artefato_id TEXT NOT NULL REFERENCES artefato_fonte(artefato_id),
  PRIMARY KEY(sistema,id_origem)
);

CREATE TABLE IF NOT EXISTS inv_vinculo_documental (
  vinculo_id TEXT PRIMARY KEY,
  entidade_origem TEXT NOT NULL,
  id_origem TEXT NOT NULL,
  entidade_destino TEXT NOT NULL,
  id_destino TEXT NOT NULL,
  modalidade TEXT NOT NULL CHECK(modalidade IN ('id_compartilhado','documento_oficial','proposto_sem_prova')),
  evidencia_url TEXT,
  artefato_id TEXT REFERENCES artefato_fonte(artefato_id),
  qa_status TEXT NOT NULL CHECK(qa_status IN ('candidato','em_revisao','homologado','rejeitado')),
  UNIQUE(entidade_origem,id_origem,entidade_destino,id_destino)
);

-- OBRAS: valor previsto pertence a evento 'previsto', nao a 'pago'.
-- PUBLICACAO: consulta apenas qa_status='homologado' e etapa pertinente.
-- DUPLA CONTAGEM: nao agregar transferido com gasto executado financiado pelo mesmo repasse.
-- TERRITORIO: papel='local_execucao' ou 'abrangencia' explicitado; sede do recebedor nao e local da obra.
-- RATEIO: NULL nao implica 100%; projeto multi-municipal sem rateio permanece nao_alocado.
