# FED04 — Auditoria das 128 divergências de DCA 2025: precisão numérica

**Data:** 09/11/2026. **Estado:** QA analítico concluído; causa documental ainda pendente; sem alteração do banco canônico.

## Fontes e método

Confrontados diretamente (i) o CSV anual `receitas orçamentárias (anexo I-C) - municípios de sp 2025.csv`, de origem SICONFI, e (ii) a aba `2025-finbra` do arquivo `Receitas 2022-2025.xlsx`, ambos preservados na pasta de fontes do Google Drive identificada no relatório de cobertura do FED04. Chave composta: código IBGE de sete dígitos, identificador da conta (sem prefixo `siconfi-cor_`) e coluna de receita. Foram selecionadas quatro contas: FPM mensal `RO1.7.1.1.51.1.0`, ITR `RO1.7.1.1.52.0.0`, Fundeb recebido `RO1.7.5.1.00.0.0`, complementação federal do Fundeb `RO1.7.1.5.00.0.0`; colunas: receita bruta, deduções Fundeb e outras deduções. Os valores monetários foram comparados com aritmética decimal exata, sem tolerância oculta. O CSV tem codificação Windows-1252 e separador ponto e vírgula, com três linhas preliminares antes do cabeçalho. O suplemento foi lido com `openpyxl` em modo somente leitura.

## Resultados verificados

- Chaves analíticas: **3.596 no CSV anual**, **3.649 no suplemento**, **3.596 coincidentes**, **53 exclusivas do suplemento**, **zero exclusivas do CSV**, nenhuma chave duplicada dentro das seleções.
- **128** diferenças de valores nos registros coincidentes, distribuídas por **75 municípios**.
- Por conta: **FPM mensal 63**, **Fundeb recebido 64**, **complementação da União 1**, **ITR 0**.
- Por coluna: **127** em `Receitas Brutas Realizadas`, **1** em `Deduções - FUNDEB`; nenhuma em outras deduções.
- Diferenças absolutas: 17 de R$0,01; 15 de R$0,02; 47 de R$0,03; 28 de R$0,04; 20 de R$0,05; 1 de R$0,27.
- O único desvio acima de R$0,05 é São Paulo (IBGE `3550308`), receita bruta do Fundeb recebido: **R$8.065.438.177,73** na origem anual contra **R$8.065.438.178,00** no suplemento; diferença de **R$0,27**.
- 65 diferenças positivas e 63 negativas (suplemento menos anual). Todos os 128 valores discrepantes são compatíveis em magnitude com redução de precisão de números no XLSX. **Isto não prova a causa documental**, mas torna inadequado qualificá-los como diferenças materiais de execução.

## Decisão de QA

**Não substituir** os valores da fonte anual pelos do suplemento, **não somar diferenças** como receitas e **não interpretar** automaticamente a variação em centavos como retificação oficial. Para registros coincidentes, preservar a precisão do CSV anual e o suplemento como fonte de preenchimento exclusivo de lacunas; exigir prova de versão/geração do XLSX antes de encerrar a investigação causal. As 53 chaves exclusivas do suplemento são casos de cobertura, não divergências de valores; requerem verificação específica antes da promoção.

## Cobertura preliminar das contas no suplemento, 2022–2025

Contagens de municípios com `Receitas Brutas Realizadas` não vazia na conta selecionada, **não comparáveis como receita líquida nem como evolução econômica sem verificar o ementário vigente**:

| Ano | FPM | ITR | Fundeb recebido | Complementação federal |
|---|---:|---:|---:|---:|
| 2022 | 642 | 634 | 640 | 5 |
| 2023 | 642 | 636 | 626 | 146 |
| 2024 | 645 | 638 | 628 | 202 |
| 2025 | 641 | 631 | 621 | 451 |

A forte variação de presença da conta de complementação é **sinal para auditoria de classificação e hierarquia**, não demonstra por si evolução de beneficiários. O suplemento de 2025 não inclui todas as adições pontuais da API registradas na matriz estadual final de 645 municípios.

## Etapas seguintes

1. Confirmar o processo de geração do XLSX suplementar, especialmente arredondamento/serialização de números elevados.
2. Examinar 53 células exclusivas do suplemento por município, fonte e estágio; não confundir preenchimento candidato com retificação.
3. Investigar Rio das Pedras (anexo existente sem quatro contas selecionadas) e Sarutaiá (sem registros do anexo na última consulta documentada).
4. Revisar ementários DCA e mapeamento 2013–2024 antes de ampliar séries históricas.
5. Manter `STATUS_FED_SP645.csv` como `in_progress`, sem migration, inserção em `observacao` nem deploy público.

**Arquivo de auditoria gerado na sessão:** `FED04_DIVERGENCIAS_DCA_2025_AUDITORIA.csv`, 128 linhas, SHA-256 `6d9fb82db67414af04cb133afefc78abe39af6dcc7897b7e24845aa7e63e63a4`. A permanência desse CSV no GitHub/Drive ainda não foi comprovada; relatório e números devem permanecer rastreáveis às duas fontes originais.

## 6. Teste adicional de reprodução exata do arredondamento

Uma segunda bateria confrontou, para cada uma das 128 chaves divergentes, o valor do CSV anual com o valor do XLSX após arredondamento decimal do valor anual para **10 algarismos significativos, modo `ROUND_HALF_UP`**. Resultado: **128/128 igualdades exatas**. Controles alternativos: 10 algarismos significativos com `ROUND_HALF_EVEN` explicam 116/128, e truncamento `ROUND_DOWN`, 63/128. A regra `ROUND_HALF_UP` explica inclusive a diferença de R$0,27 do Fundeb recebido de São Paulo. A evidência permite **classificar as 128 diferenças como integralmente reproduzíveis por uma mesma transformação numérica**, mas a confirmação de que essa operação foi aplicada durante a geração/exportação original do XLSX depende dos metadados e do script gerador, não analisados nesta etapa. Não se pressupõe retificação de execução fiscal, e os valores precisos do CSV permanecem prioritários.
