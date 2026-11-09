# FED04 — Inventário de sobreposição entre FINBRA/SICONFI, STN e Banco Central

**Referência:** 09/11/2026. **Situação:** `qa_pass_2025_actual_db_only`, com inspeção de **base SQLite temporária montada a partir do arquivo canônico 2025**, não uma consulta ao banco histórico publicado de 2013–2025. **Não houve inserção nem alteração na produção.**

## 1. Problema investigado

A integração de dados federais precisa evitar cadastrar como nova receita municipal valores que já estejam nas contas do FINBRA/SICONFI. O diagnóstico separa: (i) contas municipais já disponíveis; (ii) informações federais úteis para conferência, conciliação ou maior desagregação; (iii) indicadores econômicos e eventos que efetivamente ampliam o objeto da plataforma.

A análise teve como fontes internas:
- [`data/catalogs/variables_core.yml`](../data/catalogs/variables_core.yml), definições oficiais adotadas na plataforma;
- [`data/mappings/base_multifuentes_sp645_2025.yml`](../data/mappings/base_multifuentes_sp645_2025.yml), mapeamento das variáveis de 2025;
- [`data/catalogs/publication_variables_v1.yml`](../data/catalogs/publication_variables_v1.yml), grupos expostos no frontend;
- banco temporário reconstruído com o [importador existente](../pipeline/ingest/import_multifuentes.py) a partir do XLSX **`FINBRA_SP645_BASE_MULTIFONTES_2025_GATE_C.xlsx`**, obtido no R2 canônico `sp_645/site_inputs/`, SHA-256 `ffd626cfde3fa1c79d7a552d5b3a8ad2e3509dce5efcc9c62c39eb76c3796566`.

A consulta foi feita exclusivamente sobre `build/fed04-overlap/isolate_2025.sqlite`, criado na máquina de CI e aberto posteriormente com `mode=ro` e `PRAGMA query_only=ON`. O banco isolado contém **645 municípios, 46 variáveis efetivamente importadas e 29.670 observações de 2025**; essa contagem não corresponde necessariamente a todas as variáveis e anos existentes em outros builds da plataforma.

## 2. Evidência de disponibilidade real

| Conta da base municipal | Variável existente | Observações em 2025 | Ausências | Encaminhamento |
|---|---|---:|---:|---|
| FPM — cota mensal | `dca_fpm_cota_mensal` | **643** | **2** | **Reutilizar.** Confrontar com STN, sem substituir valor declarado |
| ICMS — cota-parte | `dca_icms_cota_parte` | **644** | **1** | **Reutilizar.** Não misturar com item de formação do Fundeb |
| IPVA — cota-parte | `dca_ipva_cota_parte` | **643** | **2** | **Reutilizar.** Não misturar com item de formação do Fundeb |
| ITR — cota-parte | *não há variável específica entre as 46 importadas* | — | — | **Desagregação potencial**; verificar em contas detalhadas DCA |
| Fundeb — transferências/deduções | *não há variável específica entre as 46 importadas* | — | — | **Desagregação potencial**, exige reconciliar formação, repasse e ajustes |

As duas ausências FPM são **Rio das Pedras, IBGE 3544004**, e **Sarutaiá, IBGE 3551207**. `status='ausente'` representa falta de observação no XLSX canônico; **não imputar zero, nem copiar STN em seu lugar**, pois as séries podem empregar critérios contábeis e períodos diferentes. O diagnóstico não determinou se existe valor declarado em outro demonstrativo, retificação ou versão.

**Nota metodológica:** o catálogo já prevê agregações e indicadores baseados em FPM/ICMS/IPVA — p. ex. `fpm_pct_receita_corrente` e `transferencias_selecionadas_pct_receita_corrente`. Recriar a mesma informação como novo indicador da STN duplicaria uma perspectiva existente; o novo dado pode servir como fonte de verificação e para visualizar os decêndios, não para somar duas vezes a transferência.

## 3. Matriz de decisão de integração federal

A auditoria sistemática classifica **14 conceitos**; a **matriz completa e seu QA** estão preservados no R2. A classificação semântica abaixo é uma decisão de projeto, não validação de equivalência numérica entre fontes:

| Fonte/conceito | Diagnóstico | Prioridade |
|---|---|---|
| **STN FPM regular** | **Já cadastrado** como cota mensal DCA; a série STN mensal/decendial serve para conciliar e esclarecer diferenças | QA e divergências |
| **STN FPM extraordinário** | **Desagregação distinta**, pois `dca_fpm_cota_mensal` exclui adicionais; em setembro/2026 a fonte STN histórica agrega regular + adicional | Criar evento específico apenas quando classificado |
| **STN ITR** | **Não há variável específica** no conjunto de 46 importadas; pode constar de contas DCA mais amplas | Examinar natureza contábil DCA |
| **STN Fundeb** | **Não há variável específica** entre as 46; itens de composição, dedução, ajuste e complementação não representam automaticamente receita recebida | Conciliação contábil prioritária |
| **STN royalties** | Sem variável específica identificada no mapeamento principal; podem estar em contas de receitas correntes | Detalhamento condicionado |
| **STN LC 176/2020** | Sem variável específica identificada; verificar compensação e natureza antes da incorporação | Detalhamento condicionado |
| **DCA ICMS** | **Já disponível** como receita declarada; não confundir com origem de formação do Fundeb | Não duplicar |
| **DCA IPVA** | **Já disponível** como receita declarada; não confundir com origem de formação do Fundeb | Não duplicar |
| **BCB SGS/IPCA** | Série **nacional**, não receita municipal; útil para deflação, quando inexistir deflator homologado equivalente | Reutilizar um único deflator |
| **BCB SGS/Selic** | Série **nacional**, não receita municipal; contexto macroeconômico, com controle de datas, conceito e fonte | Contextual |
| **BCB ESTBAN** | **Nova dimensão temática**, saldos bancários, depósitos e crédito municipal; não correspondem a receita ou transferência da DCA | Expansão prioritária após QA |
| **Transferegov** | **Novos atributos de eventos**: propostas, instrumentos, empenhos e pagamentos; evitar interpretar uma proposta como receita municipal | Expansão por instrumento |
| **CGU** | Evidências federais adicionais sobre execução, emendas e instrumentos, potencialmente sobrepostas ao Transferegov | Verificação e deduplicação |
| **Obrasgov** | **Nova dimensão de projetos/obras**, localização e estágios de execução; não é receita municipal por si só | Expansão temática |

Para o bloco STN, o programa já aprovou paridade **entre duas fontes da própria STN** de setembro/2026: `FPM histórico = FPM regular + cota adicional de setembro` para 645/645 municípios; ITR histórico = ITR decendial nos 632/632 municípios com valores. [Relatório de paridade](RELATORIO_FED02_PARIDADE_STN_HISTORICO_FPM_ITR_2026_11_09.md). **Essa paridade não é conciliação contábil com a DCA e não autoriza substituir observações municipais.**

## 4. Trilha de verificação e armazenamento

- [Código da auditoria](../pipeline/qa/audit_federal_overlap_existing_db.py) e [workflow isolado](../.github/workflows/fed04-audit-existing-finbra-overlap.yml).
- **Execução final aprovada:** [GitHub Actions 42691261361](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42691261361), artefato de QA [13707656153](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42691261361/artifacts/13707656153).
- Candidato R2 `sp_645/federal/governance/overlap_2025/candidates/MATRIZ_SOBREPOSICAO_FEDERAL_FINBRA_2025_42691261361.csv`: **2.818 bytes**, SHA-256 `8173658e2bf4e4c3bae5a0c8474746f3f9bdf7dd53a5c2348fc403434aa695b2`, **readback aprovado**.
- QA JSON R2 `sp_645/federal/governance/overlap_2025/candidates/QA_FED04_SOBREPOSICAO_2025_42691261361.json`: **4.282 bytes**, SHA-256 `e519572d745b372a7c70844f66b6bc0a842bdfd40ec8bfc8d86b31c1ee271f43`, upload comprovado, **sem readback específico do JSON**.
- Uma primeira execução [42690888552](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42690888552) falhou por tratar erroneamente o arquivo CSV de status como JSON; o problema foi corrigido no script e as execuções [42691033376](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42691033376) e [42691214295](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42691214295) validaram o banco e a auditoria, seguidas pela execução de arquivamento 42691261361.

## 5. Decisão técnica e próximos gates

**Decisão:** FINBRA/SICONFI continua sendo a referência de **receitas e despesas declaradas pelo município**. Dados STN detalhados não serão copiados automaticamente para `observacao`, nem tratados como receita adicional ao que já está registrado na DCA. O uso da STN é especialmente valioso para QA, detalhamento mensal/decendial e identificação de diferenças nos conceitos de FPM/ITR e Fundeb.

**Ordem recomendada:**

1. **Auditar as duas ausências FPM de 2025**, verificando existência e classificação dos registros STN correspondentes e eventuais retificações DCA. Não completar dados por inferência.
2. **Auditar detalhamento DCA** para ITR, Fundeb, royalties e LC 176/2020, verificando códigos e estágios de receita, antes de criar variáveis distintas.
3. **Evitar duplicação do FPM** ao comparar indicadores anuais e eventos federais; manter separado regular, cotas adicionais e deduções.
4. **Priorizar fontes genuinamente complementares**, sobretudo ESTBAN (estrutura bancária municipal), Transferegov (execução de instrumentos) e Obrasgov (projetos e execução física), após validar unidade, cobertura e chave territorial.
5. **Só ampliar o SQLite e o frontend depois de confirmar novidade informacional e QA**, com linhagem por origem, sem objetos alternativos de receitas municipais.

**Limitação central:** as contagens de observações referem-se à reconstrução canônica de **2025**. A cobertura de 2013–2025 está documentada no projeto, mas **não foi recontada integralmente nesta auditoria específica**. Nenhuma alteração de produção foi realizada.
