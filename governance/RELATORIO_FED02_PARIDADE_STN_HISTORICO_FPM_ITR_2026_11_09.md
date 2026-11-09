# FED02 — Paridade de FPM e ITR entre duas séries oficiais da STN em setembro de 2026

**Data da verificação:** 09/11/2026. **Status:** `qa_pass_diagnostic_only` para comparação monetária entre as **duas fontes STN**, não equivale a homologação de receita municipal declarada no RREO/DCA nem valida os 27 pares restantes.

## 1. Identificação, versionamento e execução dos arquivos comparados

Fonte A: STN [Transferências Constitucionais para Municípios](https://www.tesourotransparente.gov.br/ckan/dataset/transferencias-constitucionais-para-municipios), `resource_id=63b5f470-135f-4431-9158-ca8b7a43f61b`, registro interno `ANO=2026/Mês=09` apesar do nome de recurso `202610`. Original nacional: SHA `097638cec48145ac0f509d526be49d40929d177ef3a2ae3b7f77c0acd990cf24`, 126.807 registros Brasil, 13.889 SP. Extrato SP645 imutável arquivado em R2 privado `financas-municipais-sp-canonico/sp_645/federal/stn/2026_09/candidates/STN_SP645_ITEMS_2026_09_FROM_097638ce.csv`, SHA `3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb`.

Fonte B: STN [Transferências Obrigatórias da União — por Município](https://www.tesourotransparente.gov.br/ckan/dataset/transferencias-obrigatorias-da-uniao-por-municipio), arquivos nacionais históricos no formato **município e mês por linha, anos de 1996 a 2026 em colunas**:
- **FPM por município**, `resource_id=d69ff32a-6681-4114-81f0-233bb6b17f58`, 30.493.612 bytes, 66.848 registros nacionais, codificação `cp1252`, separador `;`, SHA `a86cad831115e02518198f4873967785a82eb3cbae651ef8505aa498c2cab088`.
- **ITR por município**, `resource_id=f6ad4e51-fc7e-40bb-b35a-3686da7fde2d`, 20.858.658 bytes, 66.842 registros nacionais, `cp1252`, `;`, SHA `9c93138d30b3c384ccb05ea91edbb8e6ee6f807f26ee2ce359e0a3e5b25f44ec`.
- Ambos possuem coluna literal `COD_MUN` com **quatro dígitos, código da própria fonte; não converter em código IBGE por suposição**. Verificar versão do cadastro SIAFI antes de utilizar como chave.

A execução [42683157606](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42683157606) fez o primeiro download e a auditoria de layout de ambos, resultando em `qa_pass_layout_only`, artefato [13704036051](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42683157606/artifacts/13704036051), aberto e inspecionado. A execução inicial de confronto [42683716402](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42683716402) comprovou paridade integral de **ITR** nos 630 nomes diretamente coincidentes e diferença sistemática entre FPM histórico e **apenas FPM regular**.

A execução corretiva [42684120155](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42684120155), artefato [13702934544](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42684120155/artifacts/13702934544), foi concluída `success` e seu QA JSON foi recuperado e inspecionado. Comparou `FPM/FPM + FPM 1%/FPM 1%` contra FPM histórico, e `ITR/ITR` contra ITR histórico, preservando códigos históricos literais.

## 2. Regras de equivalência EMPÍRICAS confirmadas

| Comparação de setembro de 2026, para SP | Observações verificadas | Valor máximo de diferença absoluto | Resultado |
|---|---:|---:|---|
| Histórico FPM 2026, mês 9 = `STN FPM/FPM` + `STN FPM 1%/FPM 1%`, soma dos três decêndios | **645/645** | **R$ 0,00** | Paridade fonte–fonte aprovada |
| Histórico ITR 2026, mês 9 = `STN ITR/ITR`, soma dos três decêndios, nos casos com valor | **632/632** | **R$ 0,00** | Paridade fonte–fonte aprovada |
| Histórico ITR com `-`/célula sem valor em 2026, mês 9 | **13/645** | Não aplicável | Coincide com 13 municípios sem linha ITR no snapshot decendial; **não imputar zero** |

Dois nomes na Fonte B não eram equivalentes por normalização estrita, mas foram conciliados **somente com código histórico `COD_MUN` específico e código IBGE confirmado na Fonte A**:
- `COD_MUN=6401` «Embu» → `IBGE=3515004` «Embu das Artes»;
- `COD_MUN=6717` «Moji Mirim» → `IBGE=3530805` «Mogi-Mirim».

O confronto final apresentou **645 códigos/fontes FPM com valor e sem nomes pendentes**, 632 ITR com valor e 13 células em branco ou placeholder. Os hashes de ambos arquivos nacionais foram novamente checados na execução. **Esta verificação não reatribuiu automaticamente todos os códigos `COD_MUN` a IBGE**: utilizou nome municipal normalizado mais UF=SP e apenas as duas exceções controladas. O uso produtivo de `COD_MUN` como chave exige cadastro de equivalências separado e versionado.

A [página oficial da STN](https://www.gov.br/tesouronacional/pt-br/estados-e-municipios/transferencias-a-estados-e-municipios/transferencias-constitucionais-e-legais) documenta as cotas adicionais de FPM, inclusive a de setembro associada à EC 112/2021. **Conclusão de dados:** para setembro/2026, **somar o adicional ao FPM do arquivo histórico provocaria dupla contagem**, porque este último já incorpora a parcela adicional. Em sentido inverso, a variável anual `dca_fpm_cota_mensal` permanece definida no catálogo da plataforma como distinta das cotas extraordinárias e **não deve ser redefinida pelo agregado histórico de setembro**.

## 3. Pendências contábeis e de operação

1. As duas séries são editadas pela mesma instituição (STN) e sua paridade é **consistência interconjuntos**, não confirmação independente de liquidação bancária ou de receita municipal escriturada.
2. O arquivo mensal histórico é uma grade longa 1996–2026 com `Mês` por linha; **não declarar cobertura real completa dos 31 anos sem QA por ano, município, valores ausentes e retificações**.
3. Confirmar com documento efetivo do Banco do Brasil o depósito FPM, retenção destinada ao Fundeb e crédito líquido. O portal BB apresenta interface dinâmica e não entregou tabela estruturada na extração anterior.
4. Homologar Fundeb e todos os demais 27 pares mediante documentos e contas municipais de estágios e períodos comparáveis. O RREO do 5º bimestre 2026 tem prazo oficial de entrega em 30/11/2026.
5. A estrutura SQL federal continua apenas proposta; **não promover valores a `observacao` ou indicadores públicos**.
6. O arquivamento dos dois originais históricos no **R2 canônico existente** foi acionado pelo workflow [42684426884](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42684426884), para as chaves `sp_645/federal/stn/historical/1996_2026/source/FPM_NACIONAL_a86cad83.csv` e `ITR_NACIONAL_9c93138d.csv`. **A persistência e a leitura de retorno SHA só podem ser declaradas quando seu log de QA estiver concluído.**

**Próxima ação objetiva:** conferir workflow de arquivamento, inspecionar cadastro SIAFI→IBGE por código com 645 entradas, construir QA de cobertura histórica por ano e aprofundar demonstrativos BB e MSC de setembro, sem sobrescrever as séries DCA.
