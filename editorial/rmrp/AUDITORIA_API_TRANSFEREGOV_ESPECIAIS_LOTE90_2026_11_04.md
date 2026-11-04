# Lote 90 — Verificação direta da API oficial de transferências especiais e delimitação dos dados FNDE

**Data:** 04/11/2026. **Escopo:** RMRP Volume II, fase de pré-homologação; consulta efetiva, com filtros em endpoints oficiais da API de Dados Abertos do Transferegov, de dois planos de transferência especial de Guariba que originaram rendimentos empregados no crédito para o terreno da escola, e mapeamento verificável do acesso aos CSVs do módulo Discricionárias e Legais. **Não houve mudança de séries fiscais, SWOT, valores prospectivos nem arquivo final DOCX/PDF.**

## 1. Fontes e atualização dos dados

Portal oficial https://api-publica.transferegov.gestao.gov.br/ ; Swagger API especiais https://api-publica.transferegov.gestao.gov.br/especiais e especificação https://api-publica.transferegov.gestao.gov.br/especiais/openapi.json . A consulta efetiva a `/especiais/data-atualizacao` retornou **2026-11-03T00:00:00**. Todas as consultas foram realizadas com filtros explícitos de código ou identificador; os retornos foram extraídos via Crawl2AI. Foram omitidos dados bancários e identificadores de pessoas físicas do registro editorial.

O novo portal também publica, em https://api-publica.transferegov.gestao.gov.br/downloads , **65 arquivos ZIP/CSV** do módulo Discricionárias e Legais, cuja página consultada informa atualização em **03/11/2026**, inclusive:
- `siconv_convenio.zip` (17,6 MB);
- `siconv_desembolso.zip` (16,1 MB);
- `siconv_empenho.zip` (22,6 MB);
- `siconv_pagamento.zip` (356,4 MB);
- `siconv_ingresso_contrapartida.zip` (3,4 MB);
- `siconv_termo_aditivo.zip` (confirmar o nome exato na lista antes do download);
- outros arquivos para obras, metas, contratos e aditivos.

**O módulo API Discricionárias e Legais em 04/11/2026 expõe apenas 13 endpoints**, verificados em https://api-publica.transferegov.gestao.gov.br/discricionarias/openapi.json , referentes a dados de atualização, programas, proponentes, propostas, seus elementos preliminares e atos preparatórios. **Não apresenta ainda endpoints de convênios, desembolsos e pagamentos**. Isso é compatível com o cronograma público de entrega da API de instrumentos até fev./2027 e da API de execução financeira até jun./2027 (https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br ). **A indisponibilidade da API não implica indisponibilidade dos CSVs.** O conjunto de arquivos foi identificado e suas URLs conferidas no portal, **mas não houve download e filtragem dos CSVs nesta rodada**.

## 2. Identificação inequívoca dos planos especiais 2022 de Guariba

GET
`/especiais/planos-acao-especiais?codigo_plano_acao=09032022-017081&tamanho_da_pagina=5` retornou **um registro**, com:
- id_plano_acao **17081**;
- id_beneficiario **3374**;
- ano 2022, situação “CIENTE”;
- investimento previsto **R$ 200.000,00**, custeio **R$ 0,00**.

GET
`/especiais/planos-acao-especiais?codigo_plano_acao=09032022-020422&tamanho_da_pagina=5` retornou **um registro**, com:
- id_plano_acao **20422**;
- mesmo id_beneficiario **3374**;
- ano 2022, situação “CIENTE”;
- investimento previsto **R$ 600.000,00**, custeio **R$ 0,00**.

GET `/especiais/beneficiarios-especiais?id_beneficiario=3374` identificou o **MUNICÍPIO DE GUARIBA, SP**, CNPJ **48.664.304/0001-80**. A fonte é pública e primária, não indexador terceirizado.

## 3. Planos de trabalho e empenhos federais

Os planos de trabalho dos planos 17081 e 20422 foram recuperados:

| Plano | ID do plano de trabalho | Situação registrada | Prazo informado | Classificação orçamentária do PT |
|---|---:|---|---|---|
| 09032022-017081 | 1312 | “Legado ADPF 854 STF / NT - TCU” | 24 meses, início cadastrado em 01/01/2025 | 02.18.01.15.451.0023.4.4.90.51 |
| 09032022-020422 | 1445 | “Legado ADPF 854 STF / NT - TCU” | 36 meses, início cadastrado em 01/01/2025 | 02.05.01.10.301.0038.2.120.000.4.4.90.51 |

**Não confundir datas cadastradas do plano de trabalho com início físico das obras originalmente executadas em 2023/2024**; os registros apresentam incorporação legado e devem ser contextualizados.

Consulta `/especiais/empenhos-especiais?id_plano_acao=17081`: 1 registro, empenho federal **2022NE000445**, emissão **17/05/2022**, **R$ 200.000,00** (situação “Enviado”). Para plano 20422: 1 registro, empenho federal **2022NE005816**, emissão **17/05/2022**, **R$ 600.000,00** (situação “Enviado”). **Empenhos da União em favor de transferências especiais não constituem prova de empenho municipal de despesas da escola**.

## 4. Relatórios de gestão e documentação de pagamentos dos objetos originais

A API tem registros em `/especiais/relatorios-gestao-novos-especiais` para os dois planos, com **data de relatório 30/06/2026**, situação **“Disponibilizado”** e tipo **“Parcial”**:

| Plano | ID relatório novo | Valor executado informado | Valor pendente informado | Pagamentos declarados |
|---|---:|---:|---:|---:|
| Iluminação 17081 | 21230 | **R$ 219.166,38** | R$ 0,00 | 4 registros |
| Centro Odontológico 20422 | 10762 | **R$ 1.403.917,61** | R$ 14.850,35 | 8 registros |

As consultas aos registros filhos `/especiais/relatorios-gestao-documento-liquidacao-especiais?id_relatorio_gestao_novo=21230` e `...=10762` retornaram **4/4 e 8/8 registros**. As somas de seus `vl_pagamento_relatorio_gestao_dl` reproduzem, respectivamente, **R$ 219.166,38 e R$ 1.403.917,61**, sem divergência aritmética. Iluminação: pagamentos declarados em **17/11/2023 e 26/12/2023**; centro odontológico: pagamentos declarados de **06/08/2023 a 12/06/2024**, todos descritos para o objeto odontológico.

**Distinção obrigatória:** estes são registros de pagamento **declarados em relatórios de gestão**, acessados em API oficial; a fonte não equivale por si só à conciliação dos extratos bancários independentes. Os valores executados **incluem recursos próprios municipais**, não são o mesmo que R$200 mil e R$600 mil de transferência federal. Não atribuir R$1,403 milhão integralmente à União.

A API legada `/especiais/relatorios-gestao-especiais` registra, para iluminação, o Contrato municipal **090/2023**, objeto descrito e situação “obra 100% concluída”; para centro odontológico, o Contrato municipal **051/2023** e informação do gestor de “obra 100% concluída”. São **declarações presentes no cadastro de gestão**, não vistoria independente da finalização.

### 4.1. Metas cadastradas

Consulta `/especiais/meta-especiais?id_executor=1315`: **5 metas** de iluminação LED. Consulta `?id_executor=1455`: **1 meta** para construção do centro odontológico. Nas cinco metas da iluminação, os campos de `vl_investimento_rendimento_meta` aparecem como **0,00**; no CEO também como **0,00**. **Essas metas correspondem aos planos de trabalho e seus objetos de origem**, e não constituem demonstrativo de rendimento acumulado, disponibilidade ou uso bancário de 2025 na preparação da escola.

## 5. Destinação dos rendimentos no Decreto 4.874/2025 — hipótese documental a reconciliar

O Lote 89 identificou crédito especial efetivamente aberto de **R$ 137.974,16**, via Decreto municipal **4.874/2025**, para o terreno da escola FNDE, a partir de rendimentos das transferências especiais dos planos 17081/20422. A consulta à API confirma **de forma independente** esses planos, beneficiário, valores originais, objetos e gastos originais.

No entanto, **não foi recuperada** movimentação bancária que permita repartir os R$137.974,16 entre as duas contas ou verificar:
- origem exata e data dos rendimentos;
- que valores ainda estavam disponíveis em novembro de 2025;
- eventual reprogramação de saldos e rendimentos e sua conformidade jurídica;
- empenhos, liquidações ou pagamentos da ação de preparação do terreno escolar;
- ingresso e movimentação do Termo FNDE 959097/2024.

A API oferece endpoints de gestão financeira e saldo por agência/conta, mas a imputação rigorosa requer confrontar datas, lançamentos e vínculo com o crédito municipal, sem expor dados bancários em documentação pública. **Não usar saldo instantâneo como prova de execução de 2025.**

**Atenção:** os relatórios de gestão dos objetos originais podem indicar obras concluídas e pagamentos em 2023–2024; isso não invalida por si a existência de rendimentos bancários posteriores nem comprova sua destinação à escola. A tese de irregularidade ou de execução financeira da escola permanece não demonstrada.

## 6. FNDE 959097/2024 — fonte diferente e gate específico

O FNDE **959097/2024** (escola de nove salas) não integra, automaticamente, o módulo especial de emendas 2022. No Lote 88 foram lidos contrato 043/2025, ordem de início, termo original e parte de aditivos; a Prefeitura declarou **R$ 2.340.800,05 repassados até 24/04/2026**, **sem conciliação oficial de extratos**. Uma consulta à base das transferências especiais **não prova nem refuta** pagamentos desse termo FNDE.

A conciliação direta exige filtrar os CSVs de Discricionárias/Legais por identificador **959097**, confrontar número interno **ID_CONVENIO** e os registros de desembolso/OB/pagamento por chave, com data e situação. O portal oficial fornece as URLs, mas este passo **ainda não foi realizado**. Manter a divergência **953042/2024** citada na página municipal como pendência cadastral a resolver no mesmo banco.

## 7. Situação dos demais gates

A presente rodada avançou especificamente na comprovação da **execução declarada dos objetos originais das duas transferências especiais** e na disponibilidade de endpoints e CSVs. Não completou:
- conferência dos oito RGF/RREO ausentes e da escala dos outros 26;
- tratamento de valores anômalos Pontal (três indicadores em quarentena);
- extração da receita de capital bruta DCA I-C de 2020 a 2024, embora as bases tenham sido inventariadas no Lote 39;
- análise integral dos contratos e execução de Cravinhos, Orlândia, Santa Cruz e convênio FID de Cássia;
- inspeção visual integral de 63 páginas do Volume II e revisão jurídica final.

**Não há homologação do Volume II nesta rodada.**

## 8. Próximo gate operacional

1. Obter e filtrar `siconv_convenio.zip`, `siconv_desembolso.zip`, `siconv_empenho.zip` e `siconv_pagamento.zip` com teste de integridade por chave ID_CONVENIO, identificando 959097 e 953042 e versões; persistir linhas amostrais **sem dados pessoais ou bancários**.
2. Confrontar as duas emendas especiais com gestão financeira, rendimentos e saldos **históricos** e, sobretudo, conferir os empenhos e liquidações municipais vinculados ao Decreto 4.874/2025.
3. Recuperar RGF/RREO oficiais de Pontal e oito municípios ausentes, refazer teste de escala sem substituir dado suspeito arbitrariamente.
4. Completar série de receita de capital 2020–2024 e checagem documental dos casos municipais prioritários.
5. Completar QA gráfico e jurídico e somente então produzir nova versão de circulação externa.

**Referências normativas complementares:** https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br ; https://api-publica.transferegov.gestao.gov.br/especiais ; https://api-publica.transferegov.gestao.gov.br/downloads . Consulta realizada em 04/11/2026. Registro de origem: `CONCILIACAO_CREDITOS_TRANSFERENCIAS_LOTE89_2026_11_04.md`.


## 9. Teste de transferência efetiva dos ZIPs oficiais — bloqueio de execução

Foi tentado acessar `https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/siconv_convenio.zip` e `.../siconv_desembolso.zip`. A página HTML do catálogo e os respectivos URLs foram acessados via Crawl2AI, mas o download binário via serviço de contêiner não foi habilitado porque o verificador de URLs não conseguiu abrir o ZIP; o teste HTTP na área de execução retornou **falha DNS (Could not resolve host)**. Portanto, **não existe CSV do novo catálogo baixado, filtrado nem conciliado neste Lote 90**; nenhuma relação de pagamentos do FNDE 959097/2024 foi obtida a partir desses ZIPs. Fica reservado para o Lote 91 o download por conector com suporte efetivo a binários ou ambiente de rede com DNS válido. Essa restrição **não afeta a validação via API JSON** dos planos especiais 17081/20422 já efetivamente realizada.
