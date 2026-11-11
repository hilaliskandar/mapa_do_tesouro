# Resultado da reconstrução privada com Gate E — 16/10/2026

Execução GitHub Actions: https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38903521858. Conclusão: success. Artefato `sp645-private-site-38903521858`, ID `12046993006`, SHA-256 `0471fb4ce5395ed64b81d1ee5722754af755a870808873b69d94f571fb8c2b44`.

O `qa_rgf_gate_e_integration.json` informa: arquivo aprovado SHA-256 `7faef8188fd56bff6bb8031dfe3a8eeec11fe56e67f986bdc0007a4ee7646eeb`, 1.290 linhas município-ano, 3.068 observações monetárias alteradas para `observado`, 802 referências sem valor, zero registros previamente observados substituídos.

Foi aberto o SQLite do artefato e confrontado diretamente com o CSV Gate E aprovado. Resultado: **3.068 comparações com valor, zero divergências; 802 combinações sem valor na referência permanecem como `nao_aplicavel`**.

Distribuição reconstruída:

| Exercício | Conta | observado | nao_aplicavel |
|---|---|---:|---:|
| 2023 | Dívida consolidada | 472 | 173 |
| 2023 | Dívida consolidada líquida | 527 | 118 |
| 2023 | Despesa total com pessoal | 527 | 118 |
| 2024 | Dívida consolidada | 482 | 163 |
| 2024 | Dívida consolidada líquida | 530 | 115 |
| 2024 | Despesa total com pessoal | 530 | 115 |

**Ressalva metodológica pendente:** os 802 valores não disponíveis na referência foram preservados como `nao_aplicavel`, mas a ausência na referência, isoladamente, não demonstra não aplicabilidade legal. É necessário reclassificar segundo evidência documental de disponibilidade e distinguir `ausente` de `nao_aplicavel` antes de homologar status. O novo site está apenas no artefato privado; a API pública e os boletins publicados continuam na versão anterior. Os testes do workflow privado e da API v2 passaram, mas a verificação do contrato editorial E2 contra a **API reconstruída** ainda não foi efetuada.
