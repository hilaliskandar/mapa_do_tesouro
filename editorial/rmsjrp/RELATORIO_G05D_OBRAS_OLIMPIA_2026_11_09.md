# RMSJRP — G05-D | Auditoria do cadastro de obras de Olímpia, extrações 2024–2025
**Data:** 09/11/2026. **Situação:** fonte oficial capturada integralmente e controle de duplicações concluído; **não** constitui reconciliação de liquidações TCESP por obra, nem fechamento do G05-D.

## Fonte, execução e persistência
- Fonte primária: Prefeitura de Olímpia, `https://www.olimpia.sp.gov.br/portal/dados-abertos/obras/2024` e `https://www.olimpia.sp.gov.br/portal/dados-abertos/obras/2025`.
- Rotina reprodutível: `editorial/rmsjrp/auditar_obras_olimpia_g05d.py`, workflow `.github/workflows/rmsjrp-g05d-obras-olimpia.yml`.
- [Execução GitHub Actions 42565405140](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42565405140), status `success`, artifact temporário `13651640345`. Os dois JSONs, inventário tabular e QA foram persistidos no R2 privado sob `rmsjrp/g05d/2026_11_09/olimpia_obras/` com readback SHA-256.
- `OBRAS_OLIMPIA_2024_RAW.json`: SHA-256 `8a08da5d7c3ea9a37e36c1870321d966fef76d17f995ffbe27d5ec84e64c2bfd`.
- `OBRAS_OLIMPIA_2025_RAW.json`: SHA-256 `3afa79e32edba52b8c85eb8772ea520c97f46bdf8bf622b17128d0629d23b2dc`.
- `OBRAS_OLIMPIA_2024_2025_INVENTARIO.csv`: SHA-256 `c9c304f6a3b0e83dcd168ebd2ceb539c43c934cd08ef384ddc3d6b62eea51689`.
- `QA_OBRAS_OLIMPIA.json`: SHA-256 `3a83276c15e809004aac84f28ec710347fb1131712e7c16ef03c7f365497c810`.

## Resultados observados, conferidos no CSV integral
| Característica | Endpoint 2024 | Endpoint 2025 |
|---|---:|---:|
| Registros de origem | 57 | 25 |
| Obras concluídas conforme situação cadastrada | 52 | 24 |
| Obras em andamento | 3 | 1 |
| Obras canceladas | 2 | 0 |
| Obras com início anterior ao ano do endpoint | 27 | 15 |
| Obras atualizadas depois do ano do endpoint | 20 | 8 |

Um registro de 2024 não tem data de início informada. Todos os 82 registros têm título. Existem **70 títulos normalizados distintos**, pois **12 títulos** aparecem nas duas listagens; nesses 12 registros coincidem também os campos de valor informado. Isso é **sobreposição cadastral**, não 12 obras repetidamente liquidadas nem prova de que os valores sejam imutáveis.

Títulos observados em ambos:
1. Construção de Bosque Urbano na Av. Aurora Forti Neves;
2. Adequação da Estação Rodoviária Paschoal Lamana;
3. Reforma e Ampliação da EMEB Jardim Helio Cazarini;
4. Iluminação pública em LED;
5. Duplicação da Via de Acesso João Custódio Sobrinho — Fase 01;
6. Duplicação da Via de Acesso Wilquem Manoel Neves;
7. Implantação de Anel Viário no Jardim Alvorada;
8. Recapeamento do pavimento asfáltico com utilização de CBUQ;
9. Construção de vestiários e sanitários de apoio às areninhas;
10. Implantação de quadra de bocha coberta e playground em Baguaçu;
11. Adequação de barraca para implantação de sanitários no recinto;
12. Execução de pista de caminhada e reforma de passarela no Jardim Tropical.

## Qualificação do dado
Os registros possuem `titulo`, `dataAtualizacao`, `dataExecucaoInicio`, `dataExecucaoFim`, `categoria`, `situacao`, `valor` e `descricao`. **Os 82 registros auditados não apresentaram campos adicionais além desses oito**. Logo, o JSON não contém chave explícita de `contrato`, `numero_empenho`, `medicao`, `codigo_acao` ou `fonte_de_recursos`. Esses campos somente poderão ser obtidos de outra fonte oficial e conciliados com evidência documental.

A data de início, a situação corrente e o valor do projeto não representam a execução financeira do ano do endpoint. O cadastro de 2024 foi atualizado em pelo menos 20 registros posteriormente a 2024, e o de 2025 em pelo menos oito registros posteriormente a 2025. A data de captura consta do `QA_OBRAS_OLIMPIA.json`. **Não é adequado comparar somatórios cadastrais 2024–2025, nem atribuir a diferença às quedas do programa 45 (Concessão Água e Esgoto), do programa 31 ou à LC 200/2023.**

## Decisões para a investigação
1. O cadastro permite reconhecer empreendimentos e sua cronologia **indicativa**, não uma série financeira auditada. Ele é útil para **buscar contratos correspondentes por título, endereço, processo ou objeto**, seguido de identificação documental do empenho e da medição.
2. Os 12 títulos sobrepostos deverão ser tratados como candidatos à **mesma obra** entre as listagens, sem dupla contagem, com identificação adicional da chave contratual antes de afirmar identidade definitiva.
3. O próximo lote deve ler o cadastro oficial de **contratos** do município — `https://dadosabertos.olimpia.sp.gov.br/dataset/contratos` — e verificar se há identificadores comuns com os empreendimentos. A relação de títulos/objetos, isoladamente, só autoriza correspondências de busca, não homologação.
4. Para Monte Aprazível e São José do Rio Preto permanecem as diligências anteriores: empenhos/medições da concorrência e contrato 08/2024; execução por ação 1003/1004 e SeMAE 1029.
5. Não reabrir coleta geral FINBRA/DCA ou TCESP já homologada. Preservar status `G05-D=in_progress` enquanto não houver vínculo contábil individualizado.

## Evidência de reprodutibilidade
A execução automatizada validou a obtenção de **ambos** os endpoints e a gravacão de JSONs brutos antes da normalização. O R2 privado conserva as versões de origem, o CSV e QA, verificadas por hashes de retorno. O GitHub conserva o algoritmo e os metadados. **A conclusão técnica é restrita ao inventário cadastral e sua integridade**, não representa auditoria dos valores informados pelo município em cada contrato ou obra.
