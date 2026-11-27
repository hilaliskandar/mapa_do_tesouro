# Resultado da correção de status RGF — 16/10/2026

A execução privada [38905063653](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38905063653) terminou com sucesso, a partir do commit `0d38cb7a011c1fe4dce1a3d6b276e60b38a282c6`.

Artefato `sp645-private-site-38905063653`, ID `12048275648`, digest SHA-256 ZIP `c5b9a64e574a2a7e70d3e1eec333e9d046d648b39377026d1ce88af857721920`. O campo `qa_rgf_gate_e_integration.json` registra 1.290 municípios–ano, 3.068 contas monetárias recuperadas do histórico Gate E verificado por SHA e **802 referências sem valor reclassificadas de `nao_aplicavel` para `ausente`**.

Conferência direta do SQLite do artefato:
- `observado`: 3.068 combinações ano–município–variável.
- `ausente`: 802 combinações.
- `nao_aplicavel`: zero combinações nas três contas monetárias históricas 2023–2024.
- Nenhuma ausência preenchida numericamente.

Conferência direta dos JSONs municipais **privados** da API editorial E2, para dez universos, contra as linhas SQLite:
- 1.722 combinações válidas de universo–município–ano–variável, incluídas sobreposições de municípios entre universos.
- 1.413 situações `observado`, 309 `ausente`, zero `nao_aplicavel`.
- **Zero divergências** de status ou valor em relação ao SQLite.

A reconstrução preservou proveniência da referência Gate E, ano e fonte específica RGF Anexos 01/02. A classificação `ausente` significa falta de valor na referência aprovada e não dispensa análise futura de original RGF para julgar motivos de cada ausência. **A API pública permanece inalterada**. Como a rotina editorial corrente lê a URL pública, novos boletins E2 **não podem ser considerados atualizados com a base reconstruída** até uma geração isolada que consuma os JSONs desta execução privada. O PR nº 198 não foi mesclado nem publicado.
