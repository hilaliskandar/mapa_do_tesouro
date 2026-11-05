# RMRP — G15 — Conciliação dos métodos de IPCA no mapa 15 (05/11/2026)

## Resultado
A divergência entre a legenda do mapa 15 do Volume II (Lote 98) e o recálculo G14 foi **inteiramente explicada pela convenção de correção monetária**, não por erro da soma dos municípios.

O mapa publicado foi construído com IPCA **de dezembro de cada exercício** a preços de setembro/2026, conforme as notas `QA_MAPA_15_RECLASSIFICACAO_2026_10_29.md` e `RECUPERACAO_MAPA15_CONTRATO_GUARIBA_LOTE87_2026_11_04.md`. A rotina G14 recalculou os investimentos liquidados com a **média dos 12 números-índice mensais do ano**, conforme Lote 17. Ambos os métodos foram reproduzidos com a mesma DCA/FINBRA canônica (Drive ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`), rubrica `dca_investimentos_liquidada`, 34 municípios e anos 2020–2025.

Comparação do crescimento da média anual real de investimentos de 2023–2025 em relação a 2020–2022:

| Classe | IPCA dezembro (mapa atual) | IPCA média anual |
|---|---:|---:|
| Queda > 50% | 3 | 3 |
| Queda de 20% a 50% | 9 | 9 |
| Queda < 20% | 7 | 7 |
| Alta de 0% a 50% | 5 | 6 |
| Alta > 50% | 10 | 9 |
| **Total** | **34** | **34** |

**Única mudança de classe, de 34 municípios:** Santa Rosa de Viterbo (IBGE 3547601), cujo crescimento calculado é **+51,44568883% pelo IPCA dezembro** e **+49,9897161% pelo IPCA médio anual**.

Os outros 33 municípios preservam a mesma classe sob os dois métodos.

## Decisão técnica
1. **Não atribuir erro de contagem ao mapa existente.** A distribuição 3/9/7/5/10 é a correta sob seu método documentado (dezembro).
2. Se a convenção definitiva do Volume II para fluxos anuais for **IPCA médio anual**, atualizar a imagem e legenda do mapa 15 para 3/9/7/6/9, preservando o método, a data-base, o universo de municípios e a malha IBGE 2022 (EPSG:4674), sem simplificação.
3. Alternativamente, manter o mapa original e explicitar em legenda e remissões que ele utiliza IPCA dezembro, evitando comparação numérica direta com as taxas calculadas por média anual.
4. Não substituir o DOCX/PDF Lote 98 até aprovação da convenção editorial; original congelado intacto.
5. Para homologação cartográfica integral, permanecem necessárias validação dos demais mapas e rastreabilidade das geometrias/atributos.

## Arquivos/evidências anteriores
- [Relatório G14](RELATORIO_G14_AUDITORIA_DIRETA_LOTE98_2026_11_05.md).
- [QA da reclassificação anterior](QA_MAPA_15_RECLASSIFICACAO_2026_10_29.md).
- [Histórico de recuperação no Lote 87](RECUPERACAO_MAPA15_CONTRATO_GUARIBA_LOTE87_2026_11_04.md).
- DCA SP645: Google Drive ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`.
