# Plano operacional — aquisição sistemática de transferências e investimentos oficiais SP645

**Data-base:** 16/11/2026  
**Repositório:** `hilaliskandar/mapa_do_tesouro` | **branch:** `investimentos-territoriais-sp645-20261111` | **PR:** #233 (draft)  
**Território de aquisição:** 645 municípios de SP; **primeiro aceite territorial:** 34 municípios e quatro sub-regiões da RMRP.  
**Estado:** plano de execução, não declaração de que as fontes pendentes estejam coletadas, conciliadas ou publicadas.  
**Prevalência:** para a ordem de prioridades e governança da aquisição sistêmica, este plano complementa e, onde conflitante, prevalece sobre o backlog inicial de 11/11. Os relatórios FED01–FED21 permanecem válidos como histórico e evidência, sem reclassificar resultados.

## 1. Objetivo e escopo

Acrescentar à base FINBRA/SICONFI e TCESP uma camada permanente e auditável de transferências constitucionais, legais, voluntárias, especiais e fundo a fundo; instrumentos e liberações estaduais; projetos/obras e execução direta territorialmente comprovada. A camada permitirá consultas por município, ano, sub-região, origem, beneficiário, executor, modalidade e estágio financeiro, sem dupla contagem de financiamento e aplicação.

**Mudança de prioridade:** consulta sistemática e exaustiva às APIs e arquivos oficiais, normalização, persistência, integração e atualização periódica são o caminho crítico. Dossiês individuais, endereço de obra e contratos específicos são uma fila de exceções; não bloqueiam a publicação de registros cadastrais e financeiros já homologáveis.

**Não alterar:** fatos FINBRA/TCESP já homologados, site público, regras de deflação existentes ou o histórico dos relatórios FED. Não declarar valor pago/executado por estimativa. Não inventar cobertura, geolocalização ou valor zero para ausências.

## 2. Fotografia operacional e ressalvas

- Transferegov RMRP: 6.410 propostas discricionárias; 743 registros Parcerias; recortes nacionais de 1.793 convênios, 2.537 desembolsos, 1.240 emendas; pacotes de aquisição de 15/11 preservados em Drive privado. Não são quatro somas aditivas nem representam o universo de pagamentos finais.
- Obrasgov: 218 candidatos associados ao município proponente, consultados; **não** equivalem a todas as obras fisicamente localizadas na RMRP. Cobertura dos módulos da nova API heterogênea; consulta global de geometria/execução física/contratos/empenhos retornou zero na verificação FED14/FED15, que deve ser tratada como indisponibilidade de cobertura daquele módulo, não inexistência de obras.
- FED07–FED21: prévia privada de API v3 e enriquecimentos documentais testados; zero coordenadas de **execução física** homologadas, 34/34 montantes municipais de GND4 efetivamente pago continuam `null`; `public_release_authorized=false`.
- Conciliação FED08B: 2.535/2.537 desembolsos com grupos de empenho reconciliados, dois casos pendentes; grupo de natureza do empenho classifica **desembolso**, não gasto final GND4.
- Fontes estaduais Sefaz-SP/SIAFEM e portal de Convênios SP: previstas no backlog, **sem comprovação de carga homologada** na documentação consultada.
- Inventário/backlog de 11/11 tem estados históricos desatualizados; não usar esses rótulos como fotografia atual sem confronto com pacotes e relatórios mais recentes.

## 3. Sequência dos lotes e gates

| Lote | Prioridade | Atividade executável | Produto verificável | Gate para concluir |
|---|---|---|---|---|
| S00 | P0 | Consolidar arquivos, hashes, logs, manifestos e FED01–FED21; confrontar backlog com objetos Drive/R2 | Inventário de fontes e matriz cobertura × município × exercício | Status evidenciado por artefatos, nenhuma carga já feita tratada como pendente sem motivo |
| S01 | P0 | Levantar contratos OpenAPI/CSV, filtros, parâmetros, limites, temporalidade, autenticação e política de retificação | `fontes.csv`, `endpoints.csv`, dicionário de campos e testes sentinela | Fontes prioritárias com método de extração documentado ou bloqueio explícito |
| S02 | P0 | Fechar cobertura federal: Discricionárias/Legais, Parcerias, Especiais; CGU e ordens bancárias por chaves oficiais; Tesouro constitucional | Snapshots reutilizáveis SP645, derivados RMRP34, relatório de cobertura | Paginação/deduplicação/volumes/IDs reconciliados ou divergências registradas; não exigir GND4 final |
| S03 | P0 | Adquirir convênios SP e liberações Sefaz-SP/SIAFEM (inclusive estornos), verificar possibilidade de CSV/API e alternativa legal de extração | Snapshot estadual, catálogo de instrumentos e parcelas efetivamente liberadas | Origem, data, valor, sinal, beneficiário, chave e modalidade verificáveis; não confundir celebrado com liberado |
| S04 | P1 | Obrasgov: completar paginação do universo SP; derivar RMRP por papéis territoriais distintos; obter entidades de projeto/execução disponíveis | Inventário estadual e regional, indicadores de cobertura de módulos | Contagem de páginas/IDs, filtro territorial justificado e geolocalização classificada por precisão |
| S05 | P1 | Modelar e importar fatos em SQLite de desenvolvimento, preservando arquivos brutos no R2 e proveniência | Tabelas de eventos, instrumentos, localidades, fontes e vínculos, QA SQL | FK, unicidade, somas por estágio, órfãos, valores `null`, nenhum impacto no banco público |
| S06 | P1 | Produzir agregações e JSON API v3 static-first por município, sub-região, ano e modalidade; usar dados homologados parciais | Prévia integrada FINBRA/TCESP × União × Estado | 34/34 municípios e 4 sub-regiões, contratos/testes de regressão, rastreabilidade de cada número |
| S07 | P1 | Homologação funcional e visual privada, depois decisão explícita de publicação | Relatório de aceite, lista de limitações e decisão de release | Sem publicação automática; comparabilidade e conceitos financeiros checados |
| S08 | P1 | Automatizar coletas, retificações e expansão de consultas SP645 | Workflows, alertas, histórico de execução e relatório mensal | Duas rodadas sucessivas idempotentes, diffs auditáveis e 645 municípios no universo, inclusive sem registros |
| E01 | P3 | Tratar casos/documentos individuais cuja exceção afeta publicação ou evidência relevante | Fila de exceções por impacto, não por curiosidade investigativa | Correção verificável; não bloquear S02/S03/S05/S06 quando dados independentes são aptos |

**Dependências:** S00→S01; S01→S02/S03/S04 em paralelo; S02+S03→S05; S05→S06→S07; S02/S03/S04→S08. E01 ocorre paralelamente, com limite de capacidade, e somente bloqueia o indicador ou registro específico sob contestação.

## 4. Fontes e ordem de aquisição

| Família | Modalidades/dados | Estratégia e cuidado |
|---|---|---|
| FINBRA/SICONFI e TCESP | Receitas de transferências, receitas próprias, despesas e investimento municipal por estágio | Reutilizar base aprovada; conciliar como comparação contábil e nunca igualar diretamente pagamento externo e lançamento municipal |
| Transferegov D/L | Propostas, instrumentos, empenhos, desembolsos, pagamentos/OBTV/DL | Preferir CSV nacionais completos; APIs paginadas para incrementos e campos ausentes; `NR_MOV_FIN` uma vez no fato-pai |
| Transferegov Especiais | Beneficiários, planos, emendas, empenhos e OB | Cadeia documental exata; GND e valores de plano não provam gasto final |
| Transferegov Parcerias | Proposta, parceria, empenho, ordem | Preservar `id_proposta`/`id_parceria`; não associar ordem por valor/data |
| Tesouro Nacional | FPM e outras constitucionais/legais | Conferir API oficial, códigos e séries temporais; separar de transferências voluntárias |
| Transparência SP | Convênios estaduais e instrumentos | Testar exportação oficial e dicionário; histórico e beneficiário/CNPJ |
| Sefaz-SP/SIAFEM | Liberações e estornos de transferências voluntárias | Extração periódica; separar capital/custeio e assinado/liberado |
| CGU/Portal da Transparência | OB, empenhos, pagamentos e transferências | Arquivos oficiais e chaves SIAFI; controle de duplicação com Transferegov |
| Obrasgov/Novo PAC | Cadastro de projetos, intervenções e execução física informada | Inventário completo por SP quando viável; proponente ≠ beneficiário ≠ localização física |
| Fundo a fundo e setoriais | Saúde, educação e outras transferências | Descobrir endpoints oficiais, períodos e granularidade; priorizar após fontes P0 |
| Despesa direta estadual | Execução de obra/serviço por órgãos estaduais | Identificar origem auditável territorial; nunca atribuir por sede do órgão |

As URLs do backlog inicial são **candidatas verificadas historicamente**, não garantia de que endpoint, resposta, esquema ou disponibilidade permaneçam idênticos. Toda execução deve registrar contrato e verificação recente.

## 5. Contrato dos registros de controle

Manter em `governance/controls/investimentos_sp645/` arquivos versionados, separados do README narrativo:

- `fontes.csv`: `fonte_id;orgao;sistema;modalidade;url_oficial;formato;granularidade;periodo_inicio;periodo_fim;escopo;status;verificado_em`.
- `endpoints.csv`: `endpoint_id;fonte_id;url_template;filtros;paginacao;tamanho_pagina;auth;limite;schema_version;ultima_verificacao;estado`.
- `execucoes.csv`: `run_id;endpoint_id;inicio_utc;fim_utc;status;paginas_esperadas;paginas_recebidas;linhas_recebidas;duplicatas;erros;artefato_manifesto`.
- `snapshots.csv`: `snapshot_id;fonte_id;competencia;extracao_utc;url;storage_uri;bytes;sha256;linhas;versao;qa_status`.
- `cobertura.csv`: `fonte_id;modalidade;ibge7;ano;consulta_status;registros;ultima_observacao;ultima_coleta;motivo_lacuna`.
- `pendencias.csv`: `id;fonte_id;escopo;criticidade;tipo;descricao;evidencia;acao;bloqueia_campo;status`.
- `conciliacoes.csv`: `regra_id;run_id;fonte_a;fonte_b;chaves;cardinalidade;pares;orfãos;divergencias;resultado;relatorio`.

Criar linha por fonte/modalidade/município/ano mesmo que a consulta retorne legitimamente zero, com `consulta_status=sucesso_sem_registro`; falha de rede/API usa `erro`, fonte não coberta usa `nao_coberto`, ausência ainda não examinada usa `nao_consultado`. Valores financeiros ausentes devem continuar `null`.

Cada snapshot inclui manifesto de requisições, parâmetros, HTTP, páginas, totais declarados/observados, hashes e versão de código. R2 privado é depósito canônico de arquivos; GitHub contém controles pequenos, código, contratos e QA; Drive privado mantém cópias de continuidade conforme política existente.

## 6. Modelo financeiro, vínculo e regras de agregação

1. **Grão da tabela de eventos:** um documento/evento por ID de origem, tipo de estágio, data, favorecido e moeda, valor em centavos; parcelas e detalhes em tabela filha sem replicar valor pai.
2. **Famílias de medidas não aditivas entre si:** previsto/celebrado, empenhado, desembolsado/transferido, pago ao fornecedor, liquidado municipal e execução física. Mostrar em colunas distintas.
3. **Papéis territoriais:** município proponente, beneficiário, executor e local da intervenção em relações diferentes, N:M quando houver prova; município sede do órgão não determina execução no território.
4. **Capital/custeio:** classificar pela natureza da operação comprovada; PAD GND4 aprovado e natureza de empenho não bastam para declarar pagamento final de investimento. Em casos inconclusivos, `natureza=indeterminada`.
5. **Transferegov×CGU×SIAFI:** preferir chaves oficiais e conservar evidência da aresta; proibir junções por valor, data ou semelhança do nome como vínculo confirmado.
6. **Período:** competência, evento financeiro, atualização na fonte e ingestão são campos distintos; mudanças retrospectivas preservadas por versionamento de snapshot.
7. **Comparação TCESP/FINBRA:** demonstrar transferências e investimentos liquidados lado a lado, sem soma e sem causalidade presumida; tratar diferenças de exercício e regime contábil.

## 7. Rotina e qualidade

**Cadência inicial proposta, condicionada à publicação real:** pagamentos e novas ordens: diária/semanal; instrumentos federais: semanal; liberações estaduais: semanal/mensal; Tesouro: mensal; Obrasgov: semanal; auditoria de consistência: mensal. Agendamento só após validar volume, limite e janela de atualização real de cada fonte.

Requisitos: checkpoint por página/período, retry com backoff, proteção contra rate-limit, idempotência por chave natural + snapshot, controle de schema drift, cargas atômicas, reconciliação `total_items` vs itens únicos, diffs de retificações e alertas de falha. Falha do executor local de DNS não deve ser tratada como indisponibilidade oficial: usar o ambiente remoto já validado, preservando hashes e proveniência.

**Aceite de integração parcial:** publicar cadastros, instrumentos e desembolsos documentalmente verificados mesmo quando `gnd4_pago=null`, sem PIN físico de execução presumido; bloquear somente métricas e mapas não homologados. A prévia existente continua privada até decisão formal. Nada neste plano autoriza deploy ou mutação produtiva.

## 8. Agenda de execução sugerida

- **Ciclo 1 — governança e fontes P0:** S00 e S01; cadastrar lacunas estaduais e confirmar arquivos federais já existentes; criar controles CSV e donos de verificação.
- **Ciclo 2 — coleta sistemática:** S02 e S03 em paralelo, com prioridade executiva para liberações Sefaz-SP e convênios estaduais; executar paginadores estaduais/nacionais reaproveitáveis.
- **Ciclo 3 — integração:** S04 e S05; QA de cobertura e joins; demonstrar colunas União/Estado/município sem dupla contagem.
- **Ciclo 4 — prévia e automação:** S06–S08; consulta RMRP34 e quatro sub-regiões, homologação por campo e extensão SP645.
- **Trilha E01:** manter 19 casos divergentes e duas exceções de desembolso em controle próprio; retomar apenas sob relevância mensurável para as medidas ou evidência física publicada.

## 9. Primeiras tarefas na próxima execução

1. Ler pacotes e manifestos já persistidos; não refazer 80 páginas Transferegov nem 218 consultas Obrasgov.
2. Consolidar planilha de lacunas por fonte e modalidade, com o estado confirmado de R2/Drive, e normalizar backlog histórico.
3. Executar teste e primeira extração oficial de **convênios SP** e **liberações Sefaz-SP**, registrar resultado HTTP, formato e campos disponíveis.
4. Planejar/rodar captura de modalidades federais faltantes (Especiais, Tesouro e CGU), priorizando lote e API por chaves.
5. Preparar consulta piloto anual RMRP que mostre lado a lado FINBRA/TCESP, recursos federais e estaduais documentados, sem esperar localização física de todos os projetos.
6. Submeter logs, QA e resultados ao README por **resumo conciso**, enquanto detalhes ficam em controles e relatórios próprios.

## 10. Critério de conclusão do programa

A frente sistêmica estará operacional quando: (a) todos os municípios SP645 integrarem o cadastro; (b) fontes P0 tiverem método reproduzível, snapshots com hashes, metadados e lacunas explicitadas; (c) RMRP34 oferecer comparações federais, estaduais e municipais por exercício com conceitos financeiros separados; (d) two runs consecutivas comprovarem idempotência e registro de retificações; (e) dashboards exibirem cobertura, data e fonte; e (f) publicação pública tiver gate de homologação e autorização explícita. Cobertura não é sinônimo de registros positivos em todos os municípios.

**Referências internas:** `editorial/rmrp/README.md`; `governance/PLANO_EXECUTIVO_INVESTIMENTOS_RMRP_PILOTO_CONSULTAS_2026_11_11.md`; `governance/INV_RMRP_BACKLOG_AQUISICAO_CONSULTAS_2026_11_11.csv`; relatórios FED03–FED21; PR #233.
