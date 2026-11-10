# FED04 — Triagem dos 191 casos remanescentes e verificação direta dos 16 inversos

**Data:** 10/11/2026. **Escopo:** DCA/SICONFI de 2025 × publicações oficiais FNDE VAAT/VAAR de 2024 e 2025. **Situação:** auditoria de cobertura, não homologação de receita.

## 1. Bases canônicas de auditoria e reprodutibilidade

A [matriz SP645 DCA × FNDE](FED04_MATRIZ_MUNICIPAL_FNDE_DCA_FUNDEB_2025_SP645_2026_11_10.csv), publicada em `governance/`, contempla exatamente **645 municípios**. A conta DCA rastreada é `RO1.7.1.5.00.0.0`, exclusivamente na coluna `Receitas Brutas Realizadas`, fonte [matriz original QA no Drive](https://drive.google.com/file/d/1Tik1vEa5tSIIHp0GLPEjgJi_M6HUdP_d/view).

A [matriz com 297 casos](FED04_297_CASOS_DCA_SEM_FNDE_2025_COM_RECLASSIFICACAO_2024_2026_11_10.csv) registra **106 municípios com antecedente FNDE VAAT/VAAR de 2024**, representando **R$200.133.696,95 em DCA 2025**, e **191 ainda sem antecedente nas fontes consultadas de 2024 e 2025**, representando **R$65.353.959,01**. Associação de beneficiário 2024 **não prova que o valor DCA 2025 corresponde a pagamentos de 2024**. Todos os montantes são valores DCA; não se somaram montantes FNDE.

## 2. Ranking integral dos 191 casos: seleção auditável

Foi criado [`FED04_191_CASOS_REMANESCENTES_RANKING_PRIORIDADE_2026_11_10.csv`](FED04_191_CASOS_REMANESCENTES_RANKING_PRIORIDADE_2026_11_10.csv), **191 registros, uma chave IBGE7 por município**, classificados por valor declarado em DCA 2025 sem correspondência positiva VAAT/VAAR nas publicações específicas examinadas de 2024/2025.

- Os primeiros **18 municípios concentram 50,5683%** do valor pendente; os primeiros **64 concentram 80,0758%**. A prioridade de investigação é uma fila por relevância monetária, **não um escore de irregularidade**.
- Entre os 10 maiores constam: São José dos Campos R$3.304.327,61, São Vicente R$3.271.812,78, Taboão da Serra R$2.670.875,53, Franca R$2.577.016,74, Franco da Rocha R$2.389.643,17, Embu das Artes R$2.265.628,90, Praia Grande R$1.861.363,29, Caraguatatuba R$1.745.520,08, Jacareí R$1.731.254,16 e Mogi Guaçu R$1.617.746,78.
- Mesmo no grupo de maior valor, é necessário verificar fonte/competência antes de concluir erro de rubrica, omissão, pagamento indevido ou insuficiência de receita declarada.

## 3. Conferência de versões anteriores do VAAR referentes a 2025

O [workflow de PDFs históricos FNDE](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42845975109) obteve e analisou os anexos oficiais de **agosto de 2025** (3ª publicação, Portaria MEC/MF nº 5 de 28/08/2025, PDF de 49 páginas) e **dezembro de 2025** (5ª publicação, Portaria MEC/MF nº 13 de 29/12/2025, PDF de 41 páginas), com parser textual por UF SP e código IBGE7.

- Em cada documento, o parser recuperou **154 municípios paulistas com VAAR positivo**, sem duplicação detectada.
- **Nenhum dos 297 municípios originalmente classificados como somente DCA** foi recuperado nesses dois arquivos anteriores. A busca por versões anteriores **não produziu novos casos de VAAR que expliquem os registros da DCA**.
- Esses anexos são previsões e listas de beneficiários, não demonstrativos contábeis de caixa. A conclusão refere-se **apenas ao VAAR**, não às versões anteriores do VAAT nem a ajustes de outros exercícios.
- Reforço de QA por commit posterior na branch: o parser passa a comparar literalmente o conjunto IBGE7 com os **154 códigos VAAR da sexta publicação (abril/2026)**. Essa comparação está sujeita ao resultado CI posterior e **não deve ser considerada aprovada sem log da execução**.

Fontes oficiais: [FNDE — publicações de 2025](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2025), [anexo VAAR de agosto/2025](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/vaat/3-publicacao/redes-beneficiadas-coeficientes-de-distribuicao-e-complementacao-vaar-prevista.pdf/@@display-file/file), [anexo VAAR dezembro/2025](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2025-1/5a-publicacao-2013-portaria-mec-mf-no-13-de-29-de-dezembro-de-2025/6-redes-beneficiadas-coeficientes-de-distribuicao-e-complementacao-vaar-pre.pdf/@@display-file/file).

## 4. Os 16 casos inversos: busca em DCA oficial individual

A [tabela de verificação individual](FED04_16_INVERSOS_FNDE_DCA_SP_2025_VERIFICACAO_API_2026_11_10.csv) registra **16 códigos IBGE7** em que a lista FNDE 2025 aponta VAAT/VAAR positivo, mas não há receita positiva na **conta específica** DCA de complementação `RO1.7.1.5.00.0.0`.

Consultou-se o endpoint oficial `/ords/siconfi/tt/dca?an_exercicio=2025&no_anexo=DCA-Anexo%20I-C&id_ente={codigo_ibge}`; **15 respostas retornaram registros e `hasMore=false`**, e **uma consulta foi bloqueada pela camada de acesso e permanece não verificada (Emilianópolis, IBGE 3515129)**. Nas 15 consultas completas, **não foi localizada a rubrica específica de complementação**.

Entretanto, **oito dos 15 municípios apresentam receita bruta positiva na conta geral de Fundeb recebido `RO1.7.5.1.00.0.0`**, isto é, a ausência de complementação não significa ausência de receitas do Fundeb em sua declaração. Esses oito são: Barra do Chapéu, Estrela do Norte, Guaraci, Iporanga, Palestina, Santana de Parnaíba, Sebastianópolis do Sul e Tejupá. Os sete restantes (Floreal, Gastão Vidigal, Nipoã, São João de Iracema, São José do Barreiro, Terra Roxa, Turiúba) não apresentam **essas duas contas específicas** nos registros consultados — não afirmar receita zero, ausência completa de DCA ou inexistência de outros lançamentos.

**Não corrigir por soma ou transferência de conta:** a relação entre o Fundeb distribuído, complementação federal e valores líquidos ainda exige validação do ementário, das colunas e do regime de receita efetiva. A existência de conta geral positiva não comprova que o benefício FNDE foi contabilizado corretamente ou incorretamente.

## 5. Próxima etapa operacional e gates

1. Para os 191 casos remanescentes, auditar primeiro os **18 de maior valor**, confrontando DCA, RREO/MDE e fonte bancária de repasses; expandir gradualmente aos 64 que abrangem 80% do montante.
2. Para os 16 inversos, verificar se existe desagregação sob outra conta, divergência temporal, reconhecimento em exercício posterior, atraso/retificação de DCA e declarações dos órgãos de educação. Repetir a consulta de Emilianópolis quando disponível; **não registrar sua rubrica como definitivamente ausente na API sem nova verificação**.
3. Para todos os grupos, preservar estritamente `ano_referencia_fundeb` separado de `ano_do_recebimento`, `publicacao_fnde`, `modalidade`, `receita_bruta`, `deducao` e `fonte`.
4. Não afirmar que a ausência de correspondência documental indica irregularidade, nem promover valores da lista de beneficiários FNDE como receita efetivamente recebida.
5. O [PR #232](https://github.com/hilaliskandar/mapa_do_tesouro/pull/232) permanece em **rascunho**, e o FED04 permanece **em andamento**. **Nenhuma migração de dados canônicos, escrita no R2, mudança do SQLite de produção ou alteração na publicação pública** foi realizada nesta diligência.
