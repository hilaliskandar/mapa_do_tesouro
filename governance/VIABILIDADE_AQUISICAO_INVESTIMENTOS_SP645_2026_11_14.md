# Verificação de viabilidade da aquisição de investimentos para os 645 municípios paulistas

**Data:** 14/11/2026. **Escopo:** verificar a possibilidade de iniciar já a aquisição SP645, antes da homologação monetária do piloto RMRP. **Decisão:** **SIM para coleta nacional/estadual e staging reversível; NÃO para publicar 645 indicadores de investimento efetivamente executado sem os gates financeiros e territoriais.** Nenhuma nova aquisição em escala ou promoção foi realizada neste registro.

## Evidências técnicas existentes

1. **Universo territorial validado:** `governance/RELATORIO_FED00_SQLITE_TERRITORIO_2026_11_09.md`, run 42661684901, comprova 645 registros SP no SQLite canônico, 645 no crosswalk STN, zero ausentes e zero duplicados. O código IBGE7 já é a chave territorial, e a RMRP34 é um recorte de um único universo estadual.
2. **Staging estadual STN já materializado no R2:** `governance/RELATORIO_FED00_STN_NORMALIZACAO_SP645_2026_11_09.md` documenta fonte nacional de 126.807 linhas da competência 09/2026 e extração estadual de 13.889 linhas distribuídas pelos 645 municípios, sem valores monetários homologados. Esse dado é sobre transferências obrigatórias e **não** comprova investimento GND4.
3. **Arquivos nacionais Transferegov:** catálogo https://api-publica.transferegov.gestao.gov.br/downloads . Execuções regionais já processaram **1.160.558 propostas nacionais, 288.852 registros nacionais de convênio, 4.917.545 itens PAD, 386.864 linhas de desembolso, 7.575.512 linhas de pagamentos, 3.113.841 linhas de OBTV convenente, 7.710.768 DL e 393.062 registros empenho-desembolso**. Essas linhas nacionais foram **lidas em runners**; não equivalem a snapshots nacionais persistidos no R2. A aquisição estadual **não requer 645 downloads**, apenas uma extração por versão e seleção dos municípios de proponente/destino.
4. **Obrasgov:** `governance/PLANO_EXECUTIVO_INVESTIMENTOS_RMRP_PILOTO_CONSULTAS_2026_11_11.md` documenta OpenAPI com `uf_principal=SP` e paginação até 200; contagem **anunciada** de 20.942 projetos de SP em 11/11/2026, **não auditada como coleta completa**. Recolher todas as páginas e deduplicar `id_projeto_investimento` antes de filtrar RMRP; registrar projetos sem UF principal SP cujo local de execução ou município beneficiário seja paulista se a API permitir a descoberta.
5. **SIAFEM-SP:** existem séries auditadas para a RMRP, mas não foi comprovada extração íntegra de todas as liberações estaduais classificadas como investimento dos 645 municípios. Necessário testar exportação estadual em lote ou executar varredura por território com checkpoints; preservar valores negativos como estornos.
6. **Parcerias, especiais, TED, fundo a fundo, execução estadual direta e CGU:** alcance SP645 depende de coletores e cobertura específicos, não se presume cobertura completa a partir de um módulo Transferegov.

## Regra de arquitetura SP645-first

- **Uma captura nacional por dataset e versão**, armazenada com SHA256, timestamp, URL, layout, número de registros, validação CRC e readback num prefixo privado e imutável do bucket existente. Reutilizar a captura para RMRP34, RMSJRP37, SP645 e outras divisões.
- Normalizar grãos distintos `proposta`, `instrumento`, `PAD`, `movimento`, `DL`, `item-DL`, `empenho`, `desembolso`, `obra`, `liberacao-estadual`; preservar chaves de origem e cardinalidade. Não reconstruir o mesmo acervo por centenas de chamadas municipais quando há download oficial nacional.
- **Territórios com papel explícito:** `municipio_proponente`, `beneficiario`, `municipio_destino_plano`, `municipio_obra`, `municipio_pagador` e `municipio_favorecido` não são intercambiáveis. Se o papel de local físico não tiver prova, status `territorializacao_pendente`; projeto plurimunicipal sem fração provada fica `nao_rateado`.
- **Recorte SP645 em duas passagens:** a primeira identifica proponentes/beneficiários nos 645 códigos; a segunda busca intervenções **localizadas em SP independentemente da sede do proponente** via projetos Obrasgov, município do PAD e demais campos. Isso evita subcobertura de obras executadas no estado por órgãos federais, estatais e entidades sediadas fora do município.
- **Sem soma de estágios:** valor proposto, pactuado, empenhado, transferido, movimentado, liquidado, pago e executado fisicamente são atributos ou fatos distintos. Indicadores monetários do GND4 somente após ligação documental comprovada, classificação de estorno/status e teste da natureza econômica.
- **Sem 645 indicadores com zero falso:** ausência de propostas/atos é `nao_observado` até cobertura de fonte demonstrada; (N=645) no cadastro não comprova que existam valores de investimento observados para todos.

## Matriz de prontidão

| Fonte | Podemos adquirir SP645 hoje? | Limite |
|---|---|---|
| Transferegov discricionárias CSV nacional | SIM; coleta nacional uma única vez e filtragem | Falta staging nacional durável/R2 e classificação monetária GND4 confirmada por DL/item |
| Transferegov pagamentos/OBTV/DL | SIM; arquivos reais e esquemas conferidos | Cruzamento de cardinalidade e semântica financeira ainda pendentes |
| Obrasgov | SIM para inventário de projetos com `uf_principal=SP` após paginação e QA | Contagem SP de 11/11/2026 não comprova captura integral; execução no território requer geometria/ID |
| TCESP, DCA/SICONFI | Existente em múltiplas séries SP645 | Não representa automaticamente financiamento federal/estadual ou execução direta |
| STN transferências obrigatórias | SIM; um staging SP645 do mês 09/2026 já arquivado | Não representa investimentos GND4 |
| SIAFEM-SP liberações | Viável condicionalmente; testar disponibilidade lote estadual | Série piloto RMRP não é fotografia dos 645 |
| Especiais/Parcerias/Fundo a Fundo/TED | Viável tecnicamente por APIs, condicionado a contrato/paginação | Não afirmar cobertura financeira homogênea sem QA por modalidade |
| SIGEO/SIAFEM execução direta | Pesquisa da fonte e captura possíveis, territorialização incerta | Sede da UG não é local da obra; não distribuir valores por população |
| CGU, FNS, FNDE, Novo PAC | Fontes complementares estaduais/nacionais | Deduplicar com instrumentos e projetos já presentes |

## Sequência antes da expansão operacional

**E0 — pronto:** usar crosswalk SP645 existente sem duplicar municípios e fixar procedimentos `governance/PROCEDIMENTO_REVISTO_INVESTIMENTOS_FEDERAIS_ESTADUAIS_RMRP_2026_11_14.md`.

**E1 — primeiro gate novo:** construir captura imutável para os ZIPs nacionais e um recorte SP645 por `COD_MUNIC_IBGE` + município do item; gerar QA nacional, SP e RMRP com conservação de registros, municípios observados e ausentes, sem somar valores. Não refazer download por município.

**E2:** executar inventário SP completo de Obrasgov paginado, com checkpoint e cobertura por município de execução efetivamente localizado. Não substituir todos os projetos por amostra RMRP.

**E3:** expandir SIAFEM-SP por todas as localidades, comparando exportação estadual única versus coleta municipal incremental, com estornos separados. Confrontar com TCESP/DCA sem produzir total de despesa dupla.

**E4:** completar módulos especiais/Parcerias e bases complementares, com ingestão por módulo e período.

**E5:** publicar somente matrizes de cobertura e qualidade primeiro; valores de investimentos pagos/executados após gates documentais, financeiros, territoriais, R2/readback e homologação.

## Referências de continuidade

- `governance/PLANO_PRIORIZACAO_INVESTIMENTOS_TERRITORIAIS_SP645_2026_11_11.md`
- `governance/PLANO_EXECUTIVO_INVESTIMENTOS_RMRP_PILOTO_CONSULTAS_2026_11_11.md`
- `governance/RELATORIO_FED00_SQLITE_TERRITORIO_2026_11_09.md`
- `governance/RELATORIO_FED00_STN_NORMALIZACAO_SP645_2026_11_09.md`
- `governance/PROCEDIMENTO_REVISTO_INVESTIMENTOS_FEDERAIS_ESTADUAIS_RMRP_2026_11_14.md`
- https://api-publica.transferegov.gestao.gov.br/
- https://api-publica.transferegov.gestao.gov.br/downloads
- https://api-publica.obrasgov.gestao.gov.br/

**Estado deste documento:** análise de viabilidade e decisão metodológica. Nenhuma nova carga dos 645 municípios, nem leitura live R2 ou atualização canônica foi executada na presente verificação.
