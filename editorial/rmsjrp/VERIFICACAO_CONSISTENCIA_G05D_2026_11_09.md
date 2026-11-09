# RMSJRP — Verificação de consistência e retificação documental (09/11/2026)

## Objeto
Verificar o último registro do G05-D (PR #219), a coerência do controle de gates e a recuperabilidade das fontes de obras de Olímpia. **Não é execução da reconciliação contrato–empenho–medição–liquidação nem novo fechamento de gate.**

## Achados verificados
1. **Persistência GitHub:** PR #219 incorporado à `main`, commit `fb97fca60a0b4702005ffe4a25720a98dfb48c21`. `README.md`, `editorial/rmsjrp/README.md`, `HANDOFF.md`, `STATUS_GATES.csv`, matriz de sete fontes e relatório de segunda diligência existem e foram lidos novamente. Nenhuma conclusão de G05-D integralmente aprovado consta do controle.
2. **Portal oficial de Olímpia:** conjunto `Relação de Obras Públicas` em https://dadosabertos.olimpia.sp.gov.br/pt_BR/dataset/relacao-de-obras-publicas, recursos JSON oficiais https://www.olimpia.sp.gov.br/portal/dados-abertos/obras/2024 e https://www.olimpia.sp.gov.br/portal/dados-abertos/obras/2025. Ambos respondem com estrutura JSON `dados`, conforme recuperação web em 09/11/2026; tentativa de acesso isolado ao recurso 2024 retornou erro em uma chamada, mas acesso pelo vínculo do catálogo resultou em documento legível. A instabilidade deve constar em qualquer rotina de coleta.
3. **Ressalva decisiva dos JSON:** cada entrada exposta possui campos como `titulo`, `dataAtualizacao`, `dataExecucaoInicio`, `dataExecucaoFim`, `categoria`, `situacao`, `valor` e `descricao`. Na amostra lida do recurso `2024`, há obras iniciadas ou concluídas em **2021–2023**, e até `dataAtualizacao` de **2025/2026**. Consequentemente, `2024` caracteriza a listagem indexada sob esse ano e atualizada retrospectivamente, **não um snapshot histórico de movimentações financeiras ocorridas em 2024**. `valor` tampouco é necessariamente pagamento ou liquidação, e os campos examinados não oferecem chave comum `empenho`, `contrato`, `codigo_acao_TCESP` ou `fonte_recursos`. Não somar esses valores para estimar despesa municipal anual, nem inferir recodificação 45→31.
4. **Concessão confirmada:** o contrato municipal 398/2023 com Sabesp Olímpia S/A é identificável no endereço oficial https://www.olimpia.sp.gov.br/portal/contrato/4095, com vigência 11/10/2023–10/10/2053, classificado como receita na ficha do contrato. O Formulário 20-F de 2024 da Sabesp na SEC (https://www.sec.gov/Archives/edgar/data/1170858/000129281425001804/sbsform20f_2024.htm) sustenta o contexto da outorga. Nenhum deles prova vinculação com despesa liquidada do programa TCESP 45.
5. **Monte Aprazível:** Diário Oficial Municipal, edição 1606A, 04/11/2024, p. 8, confirmou referência ao 1º termo aditivo do contrato 08/2024, objeto de recapeamento, acréscimo de 22,35% (R$ 395.147,63) e vigência até 07/06/2025: https://www.dosp.com.br/exibe_do.php?i=NTY2Njk2. Mesmo com documentação contratual, não há identificação do evento de liquidação TCESP por contrato.
6. **G01 desatualizado:** o arquivo `STATUS_GATES.csv` ainda declarava pendente geometria EPSG:4674, embora G05-C tenha homologado recorte 37/37 com malha municipal oficial IBGE 2022, geometrias válidas, sem simplificação, no [run 42562450625](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42562450625). A pendência geométrica foi retirada. Mantêm-se a cautela sobre deflator de média anual e a equivalência populacional 2025/2024 da DCA, sem afirmar atualização independente do denominador.
7. **Estado de execução:** G05-A/B/C = QA técnico e persistência aprovados; G05-D = documentos e conformidade de dez chaves contábeis registrados, **vínculo contrato–empenho–medição–liquidação permanece parcial**. Qualquer explicação causal da LC 200/2023 permanece não demonstrada.

## Recomendações operacionais para retomada
- Recuperar os JSON oficiais de obras 2024 e 2025 com captura de data/hora, contagem de registros, hash e identificadores. **Não assumir que o ano do endpoint é o exercício da despesa ou que a edição é congelada.** Comparar por título e datas apenas para busca de candidatos; exigir chave de contrato/processo e empenho para afirmar vínculo financeiro.
- Para Olímpia: conferir receitas municipais decorrentes de outorga, destinação orçamentária e a compatibilidade das ações/programas 45 e 31, sem imputações.
- Para Monte Aprazível: reunir empenhos e medições do contrato 08/2024 e ligar à ação 1010 se houver identificador documental.
- Para São José do Rio Preto: recuperar execução financeira e contratos ligados às ações 1003/1004 e SeMAE 1029.
- Manter G05-D `in_progress` enquanto essas correspondências não forem demonstradas; não repetir coleta estadual FINBRA/DCA ou TCESP.

## Fontes de referência
- https://dadosabertos.olimpia.sp.gov.br/pt_BR/dataset/relacao-de-obras-publicas
- https://www.olimpia.sp.gov.br/portal/dados-abertos/obras/2024
- https://www.olimpia.sp.gov.br/portal/dados-abertos/obras/2025
- https://www.olimpia.sp.gov.br/portal/contrato/4095
- https://www.sec.gov/Archives/edgar/data/1170858/000129281425001804/sbsform20f_2024.htm
- https://www.dosp.com.br/exibe_do.php?i=NTY2Njk2
