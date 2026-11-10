# FED04 — Confronto entre complementações VAAT/VAAR do FNDE e DCA/SICONFI de 2025 em SP

**Data da diligência:** 10/11/2026. **Resultado:** detecção de divergência de cobertura substancial, **sem atribuição causal ou alteração do banco canônico**. O confronto é de identidade municipal e de estrutura de fontes; **não equivale à conciliação de caixa nem à homologação de valores**.

## 1. Fontes e versões

1. **FNDE — sexta publicação referente ao Fundeb 2025**, Portaria MEC/MF nº 5, de **29 de abril de 2026**, publicada na [página oficial do Fundeb 2025](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/2025). Foram recuperados e analisados **cinco CSVs oficiais**, mediante [workflow 42839124220](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42839124220) e [workflow de identificação municipal 42839390581](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42839390581). SHA-256:
   - Anexo receita total por ente: `079dbf2933afcea039c2c6c0524bc6caa45c988f9d2cb4a585a44e4f9bb1576c` (562.531 bytes);
   - VAAF, cronograma: `848922f36508ebb2c9cb53ad35e9e196f1c0091d972338f1a4c93900a73862b5` (367.730 bytes);
   - VAAT, valor e complementação: `dcfe3cec9cf745c4348b98063e6beab92a37dae77704b2ad34660ba86b9e809b` (385.776 bytes);
   - VAAR, redes beneficiadas: `f97dea1d138f8bddbddf4c381b11bf6dea74b965d3f11dc168a0d59bc4c0f1f5` (165.891 bytes);
   - VAAR, cronograma: `0978c6a858f7ed505388bdfe02361e6992bd49b13c11544647371eff87615d54` (500.053 bytes).
2. **DCA/SICONFI — matriz estadual 2025, quatro contas × três colunas × 645 municípios**, originalmente [preservada no Drive](https://drive.google.com/file/d/1Tik1vEa5tSIIHp0GLPEjgJi_M6HUdP_d/view). SHA-256 documentado da matriz `9e34296a0aa9abdcd8fa5c8af9432bcb52d1cd8e550c4ae377c3efcf5947afe7`. Filtrada a chave **`cod_conta=RO1.7.1.5.00.0.0` + `coluna=Receitas Brutas Realizadas` + `valor > 0`**.
3. Os CSVs FNDE são da **publicação de ajuste anual 2025 em 2026**; o cronograma VAAR contém `Janeiro/2026` e `Ajuste`. Não atribuir diretamente as dotações ou valores do cronograma à receita arrecadada em 2025. A DCA é declaração de receita contábil; a referência temporal, o regime e ajustes podem diferir.

## 2. Conciliação interna dos anexos FNDE

A modalidade VAAR foi confrontada, por código IBGE de sete dígitos, entre o **anexo de redes beneficiadas** e o **cronograma de distribuição**. O cronograma utiliza a coluna `Total`, que inclui as demais parcelas e o ajuste declarados.

- **VAAR SP:** **154** códigos IBGE com valor; **154/154** presentes no cronograma com **mesmo valor até R$0,01**, zero diferenças, zero códigos duplicados.
- **Total VAAR SP no par de anexos:** **R$ 151.614.172,45**, em ambos os arquivos.
- **VAAT SP:** **26** registros com valor positivo na coluna de complementação selecionada; soma **R$ 85.618.598,76**. Os CSVs de VAAT possuem 643 linhas paulistas com identidade de UF, mas **apenas 26 valores monetários positivos na coluna selecionada**. Não tratar as 643 linhas como beneficiários.
- Os conjuntos VAAT e VAAR compartilham **oito códigos**: união **172 municípios**.
- **VAAF não está conciliado nesta etapa:** o cronograma tem outra estrutura de cabeçalhos e o parser preliminar não extraiu beneficiários paulistas dessa modalidade. **Zero registros extraídos pelo parser não significa ausência de complementação-VAAF**; sua natureza e cobertura exigem validação própria.

## 3. Comparação de identidades com a DCA 2025

Conjuntos utilizados: A = **453** municípios com valor positivo na conta específica `RO1.7.1.5.00.0.0` da DCA; B = **172** códigos na união dos beneficiários positivos de VAAT e VAAR da publicação oficial referida.

| Comparação | Municípios |
|---|---:|
| Conta DCA complementar com receita bruta positiva | **453** |
| FNDE VAAT positivo | **26** |
| FNDE VAAR positivo | **154** |
| Interseção FNDE VAAT ∩ VAAR | **8** |
| União FNDE VAAT ∪ VAAR | **172** |
| **DCA ∩ (VAAT ∪ VAAR)** | **156** |
| **DCA sem ocorrência nessas duas relações FNDE** | **297** |
| **FNDE VAAT/VAAR sem receita positiva na conta DCA selecionada** | **16** |

Somas **apenas dos valores DCA** e exclusivamente para classificação diagnóstica, **sem soma com FNDE**:

| Partição DCA | Valor de receitas brutas DCA |
|---|---:|
| Todos os 453 municípios | **R$ 487.348.518,81** |
| 156 municípios também identificados em VAAT/VAAR FNDE | **R$ 221.860.862,85** |
| 297 municípios não identificados nessas duas modalidades FNDE | **R$ 265.487.655,96** |

Os códigos IBGE foram usados literalmente como texto, não convertidos por número. Os valores da DCA foram somados por centavos inteiros após seleção de apenas uma conta/coluna, sem somar contas-pai, outras colunas ou repasses externos.

**A comparação não demonstra erro:** 297 posições DCA sem correspondência nos anexos VAAT/VAAR podem refletir VAAF, lançamentos/ajustes de competências anteriores, diferenças de reconhecimento, alterações/retificações, coberturas ou erro classificatório. Os 16 casos inversos também não demonstram omissão contábil isoladamente. **Não extrapolar a contagem de duas modalidades para a totalidade da complementação da União**.

## 4. Exemplos da partição pendente

Municípios com rubrica DCA positiva e sem correspondência nas relações positivas VAAT/VAAR extraídas incluem:
- Adamantina (`3500105`): **R$ 196.800,92**;
- Águas da Prata (`3500402`): **R$ 107.848,43**;
- Águas de São Pedro (`3500600`): **R$ 33.990,48**;
- Americana (`3501608`): **R$ 205.810,89**;
- Araçatuba (`3502804`): **R$ 1.540.109,59**.

Esses casos são **alvos de verificação da origem**, não afirmações de que o município não recebeu complementação da União. Deve-se buscar sua presença no VAAF e em demonstrativos de repasse/ajuste por competência.

## 5. Impacto no gate FED04 e próximos controles

1. **Bloquear qualquer uso automático de `municipios_com_receita` da DCA como «municípios beneficiários da complementação 2025»** até fechar a conciliação por modalidade, fonte e competência.
2. Em primeiro lugar, **analisar o esquema e os valores do cronograma oficial VAAF**, com filtro por SP e código municipal (sem presumir VAAF igual a zero), e recalcular a união completa `VAAF ∪ VAAT ∪ VAAR`.
3. Comparar valores por município entre FNDE (cronogramas/ajustes) e DCA, separando previsão, pagamento efetivo, competência anual e reconhecimento da receita.
4. Examinar os 297 municípios DCA não correspondentes a VAAT/VAAR e os 16 casos inversos por estratos, incluindo os exemplos documentados; testar se a conta DCA contém complementos ou ajustes de ano anterior.
5. Conservar a variável DCA `dca_fundeb_complementacao_uniao_bruta` como **receita declarada em rubrica**, com metadados e ressalva; **não convertê-la** em variável de elegibilidade VAAF/VAAT/VAAR sem validação independente.
6. Manter [PR #232](https://github.com/hilaliskandar/mapa_do_tesouro/pull/232) como rascunho e as quatro variáveis candidatas sem publicação. **Nenhum SQLite canônico, R2, série ou API pública foi alterado**.

**Código de QA:** [`pipeline/qa/probe_fnde_fundeb_2025_csv.py`](https://github.com/hilaliskandar/mapa_do_tesouro/blob/fed04-catalog-safety-20261110/pipeline/qa/probe_fnde_fundeb_2025_csv.py), na branch isolada. Os relatórios foram registrados no GitHub, mas a matriz completa das correspondências municipais FNDE-DCA ainda não foi persistida como CSV externo: os números desta etapa podem ser reproduzidos pelo código de extração FNDE e pela matriz DCA preservada no Drive.
