# Plano diretor de execução — Finanças da Região Metropolitana de São José do Rio Preto (RMSJRP)
**Versão:** 0.1 | **Data:** 2026-11-09 | **Situação:** PLANEJADO; nenhum dado regional homologado, texto aprovado ou publicação efetuada por este registro.  
**Universo canônico:** `RM_SAO_JOSE_RIO_PRETO`, 37 municípios. **Repositório:** `hilaliskandar/mapa_do_tesouro`. **Período analítico preferencial:** 2013–2025; foco da execução detalhada 2023–2025; cenários condicionais 2027–2030. **Fonte de verdade:** snapshots homologados de FINBRA/DCA, RREO/RGF/CAPAG, TCESP e metadados, não memória de chat.

## 0. Mandato, precedência e condições
Produzir estudo com a mesma densidade analítica e integridade documental das experiências RMJ e RMRP, abrangendo panorama metropolitano, unidades sub-regionais **somente após validação de composição**, e 37 perfis municipais. Mapas, gráficos e tabelas nos capítulos pertinentes, não em atlas apartado. Priorizar reuso: NENHUMA nova coleta estadual, scraping ou nova API quando o dado equivalente e auditado já existir no Drive, R2 ou build. Consulta oficial externa somente para lacuna material documentada na matriz. Preservar todo produto-fonte e versões prévias; trabalhar em cópias, branches e PRs. Não implantar, publicar ou divulgar automaticamente em decorrência do plano.

Hierarquia para recuperação: (1) GitHub main/commit e contratos; (2) manifesto/hashes e snapshot do dado; (3) API/endpoint realmente servido, com MIME e conteúdo confirmados; (4) Drive/R2 com readback; (5) registro do gate; (6) histórico de chats como indício. Diferenciar **disponível em armazenamento**, **integrado ao SQLite**, **homologado**, **implantado** e **acessível**. Conflitos devem ser registrados antes de escolher uma versão.

Referências já existentes: `README.md`, `governance/PROJECT_STATE.md`, `governance/INVENTORY.md`, `governance/PENDING_TASKS.md`, `governance/CONTINUIDADE_OPERACIONAL_RM_AU_2026_10_18.md`, `governance/HOMOLOGACAO_TCESP_R2_SQLITE_API_V2_20261026.md`, `editorial/rmrp/README.md`, `editorial/rmj/README.md`. Atenção à G30 da RMRP: 34 textos municipais e cinco territoriais em revisão; não confundir minuta com versão homologada. Atenção à RMJ: reconciliação em centavos, programas/ações, testes de HTML/CSV publicado.

## 1. Artefatos canônicos específicos da RMSJRP
Criar em `editorial/rmsjrp/` e atualizar **a cada gate**:
- `README.md`: estado corrente, gate ativo, próximos comandos/consultas, bloqueadores, links permanentes e último handoff.
- `PLANO_EXECUCAO_2026_11_09.md`: plano estável; revisões com justificativa.
- `STATUS_GATES.csv`: `gate;status;data_inicio;data_fim;responsavel;commit;run;artefato;hash;qa;bloqueio;proxima_acao`. Status: `not_started|in_progress|blocked|qa_pass|approved`.
- `MATRIZ_COBERTURA.csv`: `ibge;municipio;subregiao;ano;variavel;fonte;versao_fonte;conceito;estagio;valor_status;origem_objeto;hash;qa`.
- `REGISTRO_DIVERGENCIAS.csv`: discrepância, materialidade, fontes, decisão, cautela e responsável.
- `MATRIZ_ALEGACOES.csv`: cada cifra/inferência do texto por município, intervalo, fórmula, unidade, dado de origem, ID de tabela, QA e revisão.
- `MATRIZ_REVISAO_TERRITORIOS.csv`: 37 municípios + sub-regiões validadas + síntese metropolitana; status por dimensão de revisão e links.
- `MANIFESTO_ARTEFATOS.json`: caminhos Drive/R2/GitHub, IDs, versões, timestamps, SHA-256 e readback.
- `HANDOFF.md`: registro cumulativo dos gates, especialmente imediatamente antes de trocar de chat.
Esses caminhos são **contratos a implementar**, não arquivos já criados.

## 2. Sequência com gates bloqueantes

### G00 — Levantamento, imobilização do baseline e mapa de reuso
Ler documentação atual; identificar HEAD da main, releases, endpoints públicos, permissões de leitura, documentação de RMRP/RMJ, snapshots Drive/R2 e versões da API v1/v2. Registrar diferenças conhecidas entre 50/57/75 variáveis e não assumir que API homologada localmente está publicada. Selecionar versão de base por manifesto SHA-256, sem misturar extrações de datas distintas. Entregas: `INVENTARIO_REUSO.md`, manifesto preliminar, matriz fonte→indicador→estado. **Aceite:** cada variável necessária tem localização e status comprovado ou lacuna explicitada, com evidência.

### G01 — Recorte geográfico, população e referencial temporal
Ler `data/catalogs/territorial_universes_sp_2025.yml` e `data/catalogs/publication_universes_sp.yml`; reconciliar 37 códigos IBGE únicos e nomes com a composição legal e com a versão territorial do painel. Identificar oficialmente a existência e integrantes das sub-regiões, sem importar automaticamente as quatro da RMRP; se não houver recorte oficial compatível, justificar unidades analíticas e explicitá-las como não administrativas. Registrar eventual mudança de composição temporal. Fixar denominadores populacionais por exercício e fonte, ano-base do IPCA e deflator exato; jamais misturar IPCA de setembro/2026 com outro sem rotulagem. **Aceite:** 37/37 códigos e geometria/CRS verificáveis (EPSG:4674 quando aplicável); composição e fonte rastreáveis; nenhum município duplicado.

### G02 — Extração seletiva FINBRA/DCA
Recuperar snapshot canônico `sp_645/dca/2013_2025/normalized.csv`, SHA-256 documentado `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`, ou equivalente no Drive identificado em `PROJECT_STATE.md`. Filtrar 37 códigos × 13 exercícios = **481 pares município-ano esperados como estrutura**, sem pressupor valores observados em todos. Inspecionar 26 variáveis centrais, códigos e crosswalk 2013/2014–17/2018–21/2022+; incluir dados complementares já disponíveis de IPTU, ISS, ITBI, transferências, despesa corrente, investimento e capital conforme conceito real do catálogo. Registrar cobertura variável-ano, ausência, revisão e não aplicável; NÃO preencher ausência com zero. Não somar conta-pai e conta-filha. **Aceite:** 481 chaves únicas, cobertura discriminada, nenhum join multiplicador, conciliação de valores nominais com fonte selecionada e relatórios por município.

### G03 — TCESP e fontes legais complementares
Recuperar objetos R2 já homologados `tcesp/estadual/despesas/2023/run_40263996213/`, `2024/run_40263996213/`, `2025/run_40262193781/`. Esperados **111 pares município-ano** na seleção dos 37, mas observabilidade deve ser aferida. Selecionar estágio `Valor Liquidado` e natureza/grupo 44 para investimentos seguindo contrato RMJ; separar empenhado, liquidado e pago; conferir somas por município-ano vs programas vs ações em centavos, e inspecionar recodificações interanuais. Documentar que TCESP e DCA podem diferir conceitualmente, sem impor igualdade; conciliação pontual somente em indicadores centrais ou divergência material. Recuperar RREO (RCL), RGF (pessoal, dívida, caixa/restos a pagar) e CAPAG segundo anexos/períodos/snapshots oficiais. **Aceite:** cobertura e proveniência cada indicador legal; estágio correto; totais internos TCESP conciliados; divergências classificadas; 2026 parcial excluído da série anual comparável.

### G04 — Banco regional, indicadores e reprodutibilidade
Criar derivação regional sem modificar base estadual. Separar camada observada, agregados, indicadores calculados e oficiais; usar precisão monetária em centavos. Calcular somas dos municípios, proporções como razão das somas (não média de razões), médias/medianas municipais separadas e ponderadas quando cabível. Série nominal e real e per capita; investimento/receita corrente, receita própria/receita, despesa corrente, composição tributária, dependência de transferências, dívida, pessoal, liquidez quando observados. Variações 2023→2024, 2024→2025, 2023→2025 e médias entre períodos; marcar se nominal/real e se total/per capita. Checar sinais, arredondamentos, unidades e denominadores; impedir divisão por zero ou ausência. **Aceite:** reproduzibilidade via script/config/manifesto, invariantes aprovados e matriz de diferenças.

### G05 — Diagnóstico metropolitano e territorial
Produzir tabelas consolidadas e sub-regionais, séries históricas, distribuição de investimentos, intensidade, dependência e heterogeneidade. Separar contribuição do município-polo ao montante total e comportamento dos demais; testar sensibilidade com e sem polo sem omitir nenhum município do relatório. Empregar mapas em capítulos relevantes, com fonte e legenda e checagem geográfica; gráficos com eixos, ano, preços/unidade e notas. Inventariar todos os gráficos, tabelas e mapas, numerá-los e manter referência cruzada. **Aceite:** totais regionais reconciliados; zero mapas sem base auditável; distinção entre concentração e desempenho.

### G06 — Arcabouço, mecanismos e cenários 2027–2030
Especificar incidência da LC 200/2023 sobre a **União** e mecanismos indiretos municipais; distinguir FPM constitucional, transferências voluntárias, convênios, PAC, demais transferências, reforma tributária e conjuntura econômica. Separar fatos observados, exposição (proxy documentada), hipóteses e projeções. Três cenários explícitos, com fórmulas, premissas, limites de sensibilidade e nenhum corte automático pressuposto de FPM. Não atribuir queda de investimento à LC 200/2023 sem identificação causal; investimentos por obra/programa exigem evidência documental própria. Comparabilidade com RMRP e RMJ: mesma medida, deflator, período e fonte, ou nota de não comparabilidade. **Aceite:** cada simulação reproduzível, hipóteses versionadas, afirmações jurídicas verificadas, nenhuma perda monetária inventada.

### G07 — Preparação das 37 fichas municipais
Para cada cidade: ficha de fatos (fonte/ano/variável), tabela 2013–2025, foco 2023–2025, comparação regional e sub-regional válida, composição da receita, despesa corrente e investimento, explicação do padrão singular, cautelas de caixa/dívida/transferências, análise dos programas e ações TCESP relevantes, SWOT evidenciada, exposição prospectiva e recomendações proporcionais à evidência. **Não utilizar texto-modelo repetitivo**: cada perfil deve formular uma tese municipal demonstrável, privilegiando diferenciais quantitativos e trajetória intermediária, não somente variação de extremos. Produzir primeiro um piloto heterogêneo (São José do Rio Preto, Mirassol, Olímpia, José Bonifácio, Adolfo), validar e depois avançar em lotes controlados de 5–8 municípios, com cobertura de todos os 37. **Aceite:** nenhuma ficha sem evidência citada e leitura individual aprovada.

### G08 — Redação territorial, matrizes e revisão substantiva
Redigir síntese metropolitana e todas as sub-regiões oficialmente/analiticamente validadas depois das fichas e tabelas. Incluir SWOT regional/sub-regional e municipal somente com base comprovada, sem recomendações genéricas travestidas de achados. Controlar coerência de escalas: município vs sub-região vs região vs estado; efeito de composição; razão de somas vs mediana; total vs per capita; real vs nominal; estoque vs fluxo. Revisar 100% dos números e alegações, selecionando citações primárias para afirmações normativas/causais. **Aceite:** matriz de alegações sem pendência crítica e 37/37 perfis + unidades agregadas revisados.

### G09 — Revisão editorial independente e controle adversarial
Aplicar experiência da auditoria das 34 fichas RMRP: (a) identificar argumento distintivo; (b) testar 2024 como pico/vale; (c) avaliar intensidade do investimento e receita em conjunto; (d) distinguir declínio constante de oscilação; (e) evitar confundir resultado entre pontas com trajetória; (f) ligar quadro fiscal completo à tese sem forçar causalidade. Revisão de estilo: linguagem técnica PT-BR, ritmo variado, evitar conectivos automáticos, metalinguagem, excesso de ressalvas defensivas, afirmações vagas; preservar dados, conteúdo e voz. Parecer por ficha: `aprovada|revisar|bloqueada`, motivo e rechecagem. Conferir nomes geográficos, unidades, notas, fontes, títulos e numeração. **Aceite:** 100% pareceres individuais, zero pendência crítica; revisões rastreadas sem apagar texto anterior.

### G10 — Montagem, provas e validação material
Versão DOCX editável e PDF de prova, tabelas, mapas e gráficos inseridos nos pontos relevantes; manter contagem/inventário de elementos entre versões. Congelar pacote candidato, hashes e diffs; conferir tabelas, mídias e notas, quebras, órfãs, legendas, links e overflow; inspeção visual em todas as páginas, verificação amostral reforçada de mapas e 100% dos quadros principais. Testar consistência de tabelas/textos e cruzamento com CSV de dados. Não reusar DOCX antigo como se fosse nova homologação. **Aceite:** DOCX/PDF concordantes visual e numericamente; ficha de QA e manifesto completos.

### G11 — Persistência, homologação e eventual publicação
Salvar **cada produto** no Drive, com ID/URL/readback; snapshots e matrizes grandes no R2 privado versionado, com hash e manifesto; GitHub para scripts, metadados, metodologia, relatórios de gate e textos apropriados ao repositório. Não armazenar credenciais ou arquivos protegidos no GitHub. Após aprovação editorial expressa, eventual publicação em destino definido exige CI, preview, teste em navegador, HTTP/MIME/JSON e paridade de conteúdo publicado com hash do pacote; publicação e divulgação (Buffer/LinkedIn) são gates separados, nunca presumidos por agendamento ou merge. **Aceite:** nenhum artefato final sem localização durável; produção somente com autorização, URLs, commit, deployment, QA remoto e conferência de conteúdo.

## 3. Matriz de QA obrigatória
- **Território:** 37 códigos únicos, cobertura das unidades agregadas e integridade geográfica.
- **Dados:** fonte/arquivo/hash/ano/estágio/conceito/ausência documentados por célula; fonte original jamais sobrescrita.
- **Contabilidade:** contas hierárquicas não duplicadas; TCESP grupo 44 liquidado; conciliação de agregados em centavos; RCL e DTP legais não aproximadas por DCA.
- **Séries:** IPCA e população com referências explícitas; percentual de variação tem denominador verificável; escalas `ratio_0_1` vs `percent` certificadas.
- **Narrativa:** cada valor do texto vinculado a tabela e registro; inferência limitada; contraexemplos e ano intermediário inspecionados.
- **Comparação:** região/sub-região/município, ano-base, real/nominal, total/per capita e média/mediana não se confundem.
- **Documentos:** preservação de 100% das tabelas/mídias esperadas, renderização sem cortes, diff de texto, referências cruzadas.
- **Persistência:** arquivos Drive/R2 realmente recuperáveis, não apenas upload; manifesto e links canônicos.
- **Publicação:** preview ≠ produção; CI ≠ implantação; HTTP 200 HTML ≠ JSON; revisão substantiva ≠ aprovação final.

## 4. Lotes de execução e priorização
Lote P0: G00–G03, exclusivo de inventário e recuperação das fontes existentes; bloquear aquisição nova sem relatório de lacuna. Lote P1: G04–G06 (cálculos, geografia, interpretação e cenários). Lote P2: G07 piloto de 5 municípios, revisar metodologia antes dos demais. Lotes P3–P7: municípios remanescentes em grupos de 5–8, com QA por lote; o agrupamento final deve ser fixado após matriz de cobertura e composição sub-regional. Lote P8: G08–G10; lote P9: G11. Nenhum gate pode ser declarado `approved` pela mera existência de rascunho ou de run `success`.

## 5. Protocolo de handoff entre chats
**Primeira ação de todo novo chat:** ler `README.md`, este plano, `editorial/rmsjrp/README.md`, `editorial/rmsjrp/HANDOFF.md`, `STATUS_GATES.csv`, manifestos e `governance/PROJECT_STATE.md`; verificar HEAD e últimos PRs, uploads Drive/R2 e job real. Reconstituir exatamente o último artefato homologado; nunca pedir recompilação do que já foi persistido. **Última ação de cada sessão/gate:** salvar produto em armazenamento durável e verificar readback; atualizar status do gate, números, QA, bloqueios, IDs, hash e próximo comando/consulta concreta. Se persistência falhar, status `blocked`, disponibilizar artefato local e relatar o bloqueio; não chamar concluído.

Modelo de handoff:
```
Data/hora (America/Sao_Paulo):
Objetivo; gate; lote; situação:
GitHub branch/commit/PR/CI:
Snapshot fonte e hash; objetos R2; Drive ID/URL/readback:
Municípios/anos/variáveis observados e ausentes:
Arquivos produzidos; versão; hash:
QA executado (comandos, resultados, divergências):
Textos aprovados / em revisão / bloqueados:
Decisões metodológicas e riscos:
Ação exata seguinte; dependências e impedimentos:
```
Uma mudança de chat não autoriza mudar hipótese, deflator, base, texto homologado ou universo. Se houver divergência entre memória e manifesto, conferir fonte primária e registrar decisão.

## 6. Decisões pendentes, sem bloquear o inventário
Definir composição sub-regional apropriada à RMSJRP e documentar sua fonte; escolher um único deflator/base monetária coerente com o estudo RMRP (incluindo eventual atualização); definir destino de publicação, formato final de boletins e necessidade de Volume I/II, mantendo relatório fiscal e estudo do arcabouço distinguíveis. Definir parâmetros dos cenários somente depois dos dados; nenhuma suposição de impacto comprovado.

## 7. Referências de experiência acumulada
- RMRP `editorial/rmrp/README.md`: G29/G30, controle de 45 tabelas/16 mídias, 39 textos territoriais, rechecagem de conceitos e necessidade de revisão individual.
- RMJ `editorial/rmj/README.md`: investimentos liquidados do grupo 44, reconciliação de programas/ações em centavos, cuidado com recodificações e verificação HTML/CSV publicado.
- `governance/CONTINUIDADE_OPERACIONAL_RM_AU_2026_10_18.md`: divergência de catálogos, distinção API local/API pública e regras de retomada.
- `governance/HOMOLOGACAO_TCESP_R2_SQLITE_API_V2_20261026.md`: R2 2023–2025, importador SQLite, preview isolada e ausência de deploy público TCESP.
- `governance/PROJECT_STATE.md`: CSV DCA estadual 2013–2025 e fonte operacional Drive.
