# FED02 — Conciliação preliminar STN × SICONFI/DCA à luz do Ementário 2026

**Data de referência:** 09/11/2026. **Situação:** inventário 27/27 `qa_pass_inventory_only`; ementário 2026 recuperado integralmente e preservado; correspondências **candidatas**, não homologadas contabilmente. Sem migration, sem totais, sem alteração do SQLite ou da publicação.

## 1. Provas e escopo das fontes

1. **Origem STN:** dataset oficial `Transferências Constitucionais para Municípios`, recurso CKAN `63b5f470-135f-4431-9158-ca8b7a43f61b`, competência interna **2026/09**, 13.889 registros paulistas. Extrato codificado IBGE no bucket `financas-municipais-sp-canonico`, chave `sp_645/federal/stn/2026_09/candidates/STN_SP645_ITEMS_2026_09_FROM_097638ce.csv`, SHA-256 `3b9b5bf22748579a0f90912c160159b8d50a7664294a750fc74b2f98a59657fb`.
2. **Inventário exaustivo:** [`MATRIZ_STN_SICONFI_CROSSWALK_RUBRICAS_2026_09.csv`](MATRIZ_STN_SICONFI_CROSSWALK_RUBRICAS_2026_09.csv), **27 combinações rubrica–item e 13.889 linhas**. Código de auditoria [`audit_stn_siconfi_crosswalk_matrix.py`](../pipeline/qa/audit_stn_siconfi_crosswalk_matrix.py), [run 42668763749](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42668763749), **success**, `qa_pass_inventory_only`. Nenhum par foi omitido; nenhuma classificação de natureza orçamentária é automaticamente promovida.
3. **Ementário oficial das naturezas de receita 2026:** [página STN](https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/federacao/ementario-da-classificacao-por-natureza-de-receita-tabela-de-codigos), link de [documento 2026](https://thot-arquivos.tesouro.gov.br/publicacao-anexo/27870). XLSX baixado e inspecionado: **311.650 bytes**, SHA-256 **`97cd8bd31da8d5e5d62174d4296c779df4cf7bb89db0eb58c701c7035f6eeffa`**. Quatro abas: `Tabelas` (8 linhas), `ENR - 2026` (1.729), `Alterações - ENR 2025` (29), `Alterações ENR - 2026` (46). Busca seletiva obteve 108 linhas candidatas, não 108 equivalências verificadas. [Run 42669178291](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42669178291) `qa_pass_source_inspection_only`, origem arquivada em `sp_645/federal/stn/ementario/2026/source/EMENTARIO_RECEITAS_2026_97cd8bd3.xlsx` com **readback SHA aprovado**; candidatos em `sp_645/federal/stn/ementario/2026/candidates/EMENTARIO_2026_TERMS_CANDIDATES.csv`.
4. **Manual de Contabilidade Aplicada ao Setor Público, 11ª edição:** [página oficial STN](https://www.gov.br/tesouronacional/pt-br/contabilidade-e-custos/manuais/manual-de-contabilidade-aplicada-ao-setor-publico-mcasp-1). A documentação contábil é necessária para identificar a dedução da receita e o Fundeb, não apenas o nome de rubricas.
5. **Cadastro da plataforma:** [`variables_core.yml`](../data/catalogs/variables_core.yml), com `dca_fpm_cota_mensal` explicitamente **sem cotas extraordinárias**; `dca_icms_cota_parte` e `dca_ipva_cota_parte` são receitas estaduais diferentes e **não** correspondem automaticamente aos itens de composição do Fundeb.
6. **Arquivo de correspondências candidatas:** [`CODIGOS_CANDIDATOS_EMENTARIO_STN_2026.csv`](CODIGOS_CANDIDATOS_EMENTARIO_STN_2026.csv), com código, descrição, linha exata da aba `ENR - 2026`, SHA do ementário e alerta de natureza não conciliada. **Nenhuma linha foi liberada para totalização**.

## 2. Exemplos documentados de natureza de receita de 2026

**As naturezas abaixo aparecem no Ementário 2026; isto NÃO comprova equivalência automática entre o valor STN/SIAFI de um item e receita municipal reconhecida no SICONFI/DCA.** A descrição representa a natureza orçamentária **do ente recebedor**, distinta do código de receita federal arrecadada pela União e dos itens auxiliares de composição do Fundeb.

| STN: transferência/item | Código e descrição em Ementário 2026 | Linha ENR - 2026 | Situação |
|---|---|---:|---|
| FPM / FPM | `17115110` — Cota-Parte do Fundo de Participação dos Municípios - Cota Mensal | 1211 | Correspondência nominal candidata à variável `dca_fpm_cota_mensal`, valores não reconciliados |
| FPM 1% / FPM 1% | `17115120` — Cota-Parte do FPM - Cotas Extraordinárias | 1212 | Natureza agregada, **não** identifica isoladamente setembro, julho ou dezembro |
| ITR / ITR | `17115200` — Cota-Parte do Imposto Sobre a Propriedade Territorial Rural | 1215 | Natureza nominal candidata |
| Royalties / CFEM | `17125100` — Cota-parte da Compensação Financeira pela Exploração de Recursos Minerais | 1223 | Natureza candidata, diferenciar receita do ente |
| Royalties / FEP | `17125240` — Cota-Parte do Fundo Especial do Petróleo | 1228 | Natureza candidata |
| FUNDEB / COUN VAAT | `17155000` — Complementação da União ao Fundeb – VAAT | 1262 | Natureza candidata da complementação; não equivale ao Fundeb total |
| FUNDEB / COUN VAAR | `17155200` — Complementação da União ao Fundeb – VAAR | 1264 | Natureza candidata da complementação; não equivale ao Fundeb total |
| FUNDEB / FPM | `17515000` — Transferências de Recursos do Fundeb | 1337 | **Categoria ampla** e não identidade com o componente FPM isolado |
| FUNDEB / DEDU | Sem natureza unívoca estabelecida | — | Componente de formação/dedução, não uma receita extra a adicionar |
| AJUSTE FUNDEB / FPM | Sem natureza unívoca estabelecida | — | Ajuste: requer vínculo com o lançamento original e regra de sinal |

Foram identificadas também linhas antigas **marcadas “Excluído”** (p.ex. `17180120` cota mensal do FPM, linha 1064, e `17180130`, linha 1065). Tais códigos **não podem ser usados como equivalentes vigentes em 2026**. A matriz de candidatos dá preferência às linhas vigentes na documentação 2026, preservando linha, texto e versão exata.

## 3. Regras de equivalência e pendências

- **Não confundir código da arrecadação federal com natureza de receita municipal.** `11120100` (ITR arrecadado pela União), por exemplo, não é automaticamente o código de cota-parte da transferência recebida pelo município; conferir `17115200` do ementário municipal.
- **Fundeb é multicomponente.** Itens `FPE`, `FPM`, `ICMS`, `IPI-EXP`, `IPVA`, `ITCMD`, `ITR`, `DEDU`, complementações VAAT/VAAR e ajustes não devem ser somados sem prova dos respectivos fluxos e retenções.
- **Deduções, estornos, bases brutas/líquidas e eventos negativos** exigem validação no MCASP e nos metadados STN; a razão empírica `FUNDEB/DEDU ÷ FPM/FPM` possui mediana 0,253369 e máximo 0,535015, sem identidade uniforme.
- **FPM extraordinário não é FPM mensal**: a variável existente `dca_fpm_cota_mensal` exclui expressamente cotas extraordinárias.
- **Não existem, ainda, códigos de natureza validados para todos os 27 pares**, e nenhuma igualdade entre os valores do STN e contas da DCA foi comprovada.
- **Competência e estágio diferem:** STN/SIAFI em caixa decendial (setembro/2026), DCA municipal com escrituração própria e recorte anual. Não declarar paridade monetária com bases de competências distintas.
- **Fonte temporal controlada:** usar ementário **2026**, não as edições 2025 ou 2027, e preservar os códigos históricos marcados como excluídos apenas para rastreabilidade.

## 4. Continuidade exata

1. Investigar o mapeamento real DCA/SICONFI `codigo_conta`, `natureza`, `estagio`, ano 2026, para as sete correspondências nominais candidatas; não preencher contas ausentes do catálogo atual por especulação.
2. Validar em MCASP 11ª edição a regra de dedução da receita para Fundeb e transferências; confrontar valores brutos/líquidos por município (sem antecipar soma estadual).
3. Confrontar série histórica de FPM regular e cotas extraordinárias nos registros STN e SICONFI para excluir dupla contagem.
4. Manter `FED00=in_progress` quanto à semântica financeira e `FED01=in_progress` quanto à proposta de tabelas, **sem aplicar migration**.

**Integridade e segurança:** a existência de código no ementário **não autoriza** transferência de valores diretamente para `observacao`. Não alterar SQLite, variáveis da plataforma, R2 histórico ou frontend durante este gate.
