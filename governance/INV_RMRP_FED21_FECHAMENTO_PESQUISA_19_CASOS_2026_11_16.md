# FED21 — fechamento da pesquisa dos 19 casos de divergência territorial

**Execução:** 16/11/2026. **Base nacional:** snapshot de 15/11/2026. **Objeto:** completar a revisão documental individual dos 19 projetos Obrasgov com coordenadas de proposta que divergem do município proponente e separar documentação de localização prevista, evidência institucional e execução física.

## Cobertura e categorias

A busca direcionada aos três casos restantes encerra o **primeiro ciclo de pesquisa** sobre os 19 projetos, com a seguinte gradação:

| Classificação documental | Casos | Interpretação |
|---|---:|---|
| Alguma fonte independente de contexto/objeto/contrato ou imóvel, FED16–FED20 | **16** | Força probatória variável: nem todos os documentos citam expressamente o número do instrumento; nenhum está automaticamente homologado como localização de execução física |
| Fonte institucional adicional descreve equipamento e programação compatíveis, FED21 | **1** | Fonte não vincula explicitamente contrato ao local |
| Pesquisa dirigida sem documento municipal específico do imóvel ou local, FED21 | **2** | Registro federal permanece, mas não se obteve confirmação independente do terreno da obra |

**Não equiparar 19 projetos pesquisados a 19 obras homologadas, nem 16 documentos a 16 vínculos contratuais explícitos.** A mensuração de completude de pesquisa é diferente da de comprovação física.

## ETE de Jaboticabal — repasse 953339/2023

Projeto Obrasgov `30158.35-25`, proposta `1944870`, contrato de repasse **953339/2023**, objeto federal registrado **Reforma da Estação de Tratamento de Esgoto — ETE**.

Foram recuperadas e efetivamente lidas com Crawl2AI as seguintes fontes institucionais primárias:

- [Prefeitura de Jaboticabal — Tratamento de Esgoto](https://www.jaboticabal.sp.gov.br/portal/secretarias-paginas/83/tratamento-de-esgoto/), que identifica a ETE **“Dr. Adelson Taroco”** próxima da **Rodovia Carlos Tonani**, em área concedida pela Unesp — Campus Jaboticabal, e descreve as tecnologias da estação;
- [Serviço Autônomo de Água e Esgoto de Jaboticabal — Tratamento de Esgoto](https://www.saaej.sp.gov.br/tratamento-de-esgoto/), que confirma a estação municipal e sua operação;
- [Câmara Municipal de Jaboticabal — LDO de 2025](https://www.jaboticabal.sp.leg.br/imprensa/noticias/camara-municipal-de-jaboticabal-aprova-ldo-2025-por-unanimidade), que inclui a **reforma da ETE** entre as prioridades de investimento, com previsão aproximada de **R$ 7,1 milhões**.

**Limite central:** essas páginas municipais **não mencionam o contrato 953339/2023**. O local da ETE é uma informação institucional relevante e a ação orçamentária é compatível com o objeto do instrumento federal, mas falta cadeia documental com número de repasse, projeto executivo, licitação ou medição que comprove incidência e implantação efetiva da reforma. O valor indicado na LDO é **planejamento**, não empenho ou despesa paga. O ponto SICONV da proposta situa-se no município de **Sertãozinho** e permanece não homologado. Não criar pin na ETE por analogia com seu nome.

Uma busca adicional identificou referências a edital de contratação semi-integrada de diversas obras em Jaboticabal, inclusive de tratamento preliminar da ETE. Todavia, o resultado foi encontrado em portais de agregação de licitações **sem recuperação de edital municipal contendo número de contrato federal**, razão pela qual não foi considerado prova suficiente de execução do repasse 953339.

## Santa Rosa de Viterbo — termo 974564

Projeto `50782.35-08`, proposta `2032353`, termo de compromisso **974564**, objeto federal **implantação de unidades habitacionais MCMV FNHIS Sub-50**.

A coordenada associada à proposta incide no município vizinho de **Cajuru**; não deve ser tratada como a localização da obra. Nas buscas efetuadas não foi localizada fonte municipal que identifique expressamente terreno, loteamento, matrícula, endereço ou projeto de implantação relacionado ao termo `974564`. O resultado da pesquisa é **negativo quanto à comprovação municipal de localização**, não quanto à existência do projeto cadastral federal.

**Pendente:** obtenção de ato de destinação ou aquisição de terreno, matrícula, planta aprovada, licença e documentação que cite explicitamente o termo.

## Guatapará — termo 996136/2026

Projeto `105865.35-77`, proposta `2115363`, termo federal **996136**, objeto **provisão de unidades habitacionais**.

O cadastro federal apresenta **duas coordenadas de proposta** situadas em **Serra Azul** e **Cássia dos Coqueiros**, não em Guatapará. A busca pública não localizou ato municipal ou certidão registrária que vincule diretamente imóvel específico ao termo 996136. O levantamento identificou documentos de programas habitacionais **anteriores**, que **não podem** ser transportados para a localização do instrumento atual sem correspondência documental explícita. Registros agregados de portal privado com valores do termo foram tratados apenas como **pista de pesquisa**, e não como fonte primária de comprovação de terreno ou execução.

**Pendente:** plano de trabalho com imóvel, lei municipal de destinação, matrícula ou arquivo de implantação oficialmente vinculados ao termo 996136.

## FED21 — base privada e testes

O [script `deployment/build_rmrp_fed21_private.py`](../deployment/build_rmrp_fed21_private.py) adicionou notas de evidência documental aos três JSON prioritários sem promover localização, alterar repasses ou classificar GND4 pago.

**Arquivo:** [RMRP_FED21_SITE_PREVIA_PRIVADA_2026-11-16.zip](https://drive.google.com/file/d/1FMLBwCL8jo5n3LReVRpQ-pLphGR7tJWI/view), **830.177 bytes**, SHA-256 `e504f27ca72e83da89de10a3925ce06f9a7701775d37cd91d113094ec7332694`. Armazenado em pasta privada da RMRP `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`, metadados `shared=false`, **readback SHA-256 e CRC aprovados**.

**Validação executada:** 1.603 verificações da API; 288 requisições HTTP locais com 285 JSON válidos; **29 testes de regressão de aplicação aprovados**; 6/6 endpoints legados idênticos byte a byte; 218 projetos; 34/34 indicadores municipais GND4 pago `null`; 0 coordenadas de execução física; 0 valores de capital pago preenchidos.

## Encaminhamento

O ciclo de **pesquisa documental inicial** sobre os 19 projetos está concluído; a **homologação territorial e financeira substantiva não está concluída**. Próximas prioridades:

1. Documentos diretamente ligados ao termo `953339` para identificar precisamente onde se executará/executou a reforma da ETE, incluindo memorial da frente de serviço e medições.
2. Documentação fundiária identificada por `974564` e `996136`, evitando correspondências por proximidade ou por programa habitacional de período distinto.
3. Para os 16 casos com fontes independentes, fechar vínculo ao instrumento quando ausente, localizar geometrias de execução (polígonos e trechos, não pontos genéricos) e identificar medições/recebimentos.
4. Conciliar dois desembolsos excepcionais FED11, os alertas de cronologia de DL e os pagamentos efetivamente classificados como capital/GND4 líquido.
5. Só após aceites individualizados e QA visual/Pages restrito deliberar sobre publicação pública.

**`public_release_authorized=false`**. Nenhuma modificação em produção.
