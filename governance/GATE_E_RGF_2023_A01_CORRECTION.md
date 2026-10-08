# Gate E — correção do RGF Anexo 01 de 2023

O smoke de Americana confirmou que a API 2023 contém os três conceitos legais, mas os rótulos da conta diferem de 2025:

- RCL ajustada: código `ReceitaCorrenteLiquidaAjustada`, coluna `Valor`;
- DTP: código `DespesaComPessoalTotal`, coluna `Valor`;
- percentual DTP/RCL: código `DespesaComPessoalTotal`, coluna `% sobre a RCL Ajustada`.

A numeração romana da linha mudou entre exercícios e não pode integrar a chave de normalização.

A chave canônica do Anexo 01 passa a ser `cod_conta + coluna`. O texto de `conta` permanece evidência descritiva, não chave.

Para corrigir o Gate E, será recolhido apenas o Anexo 01 de 2023, em cinco shards. O Anexo 02 de 2023 já validado não será consultado novamente.
