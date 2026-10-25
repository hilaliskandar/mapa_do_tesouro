# Auditoria do dicionário editorial — 16/10/2026

## Resultado conferido
No artefato produzido pela execução https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38889729968 (commit `ad7db6d14dfdd804164b03e131075af2c746c22b`), `qa_dicionarios.json` registra **10 dicionários com 50 variáveis cada**, sem divergências de metadados entre universos. O ZIP inclui 280 fichas municipais. Artefato `12041103648`, digest SHA-256 `e43f4c666ccb0c90e44a597edcc8a507396c2916aae25133d170584616c14b76`.

Completude por variável (universos compartilham o mesmo catálogo): nome 50/50; unidade 50/50; grupo 50/50; definição 50/50; tipo 50/50; periodicidade 50/50; fonte preferencial 35/50; fórmula explícita 18/50; cautelas 3/50; orientação específica de leitura 0/50.

Unidades: 32 BRL; 12 percentuais; duas BRL por habitante; três razões; uma categoria. Grupos: receitas 15; despesas 8; território 10; dívida/liquidez 13; CAPAG 4.

## Correção crítica
O código anterior apresentava percentuais multiplicando por 100 valores que o catálogo já expressa na escala de porcentagem (por exemplo `investimento_pct_receita_corrente = 100 * dca_investimentos_liquidada / dca_receita_corrente_bruta`). A duplicação foi removida no commit `6a73d271` e o teste corrigido no commit `28f1a626`. O teste automatizado passou na execução identificada acima. Versões anteriores dos pacotes E2 devem ser consideradas **superadas para interpretação de indicadores percentuais**.

## Pendências da origem
O campo de fonte preferencial não está preenchido em 15 indicadores compostos ou derivados. Isso não autoriza supor ausência de fonte das parcelas; significa somente que o metadado `fonte_preferencial_id` não foi atribuído a esses itens. As fórmulas explícitas aparecem em 18 indicadores; nos restantes, quando se tratar de conta oficial ou classificação CAPAG, não se deve inventar expressão algébrica. O trabalho seguinte deve documentar a proveniência por dependências e conferir escalas dos indicadores legais fonte a fonte.

## Status
Geração dos dez boletins, 280 fichas, dicionários e QA automatizado aprovados. Ainda não concluída a conferência integral dos demonstrativos oficiais, interpretação editorial e eventual publicação externa. PR #198 permanece candidato isolado.
