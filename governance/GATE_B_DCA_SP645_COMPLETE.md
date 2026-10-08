# Gate B DCA SP 645 — conclusão 2013–2025

Data de conclusão: 2026-10-08.

## Resultado

O Gate B DCA está concluído para o universo estadual de São Paulo.

- universo: 645 municípios;
- exercícios: 2013–2025;
- município-ano: 8.385;
- variáveis normalizadas: 26;
- issues de normalização: 0;
- política: ausência não é zero;
- merge de complementos: fill-only;
- SHA-256 multianual: `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`;
- tamanho do CSV multianual: 2.096.525 bytes.

## Fontes

A reconstrução histórica utilizou prioritariamente o acervo FINBRA/DCA local do Google Drive. O Siconfi externo foi usado apenas para auditoria independente, confirmação de lacunas e complementação seletiva.

Exceções aprovadas:

- 2022: Guaraçaí, I-C, complementado pela planilha local consolidada de receitas;
- 2024: snapshot anual + suplemento local de receitas + delta seletivo Siconfi I-D/I-E, com zero conflitos;
- 2025: Gate A estadual independente do Siconfi.

## Ausências confirmadas

Os deltas seletivos atuais não recuperaram dados para lacunas históricas de 2013, 2014, 2015, 2016, 2018 e 2019. Nesses casos, os pares município–anexo consultados retornaram `items=[]`.

Essas células permanecem ausentes. Não foram convertidas em zero e não devem ser reconsultadas automaticamente sem nova evidência ou nova versão oficial da fonte.

## Crosswalk temporal

As receitas foram harmonizadas por quatro regimes explícitos:

1. 2013 — códigos antigos + `Receitas Realizadas`;
2. 2014–2017 — códigos antigos + `Receitas Brutas Realizadas`;
3. 2018–2021 — códigos intermediários + `Receitas Brutas Realizadas`;
4. 2022–2025 — códigos atuais + `Receitas Brutas Realizadas`.

As despesas centrais mantiveram contrato compatível ao longo da série analisada.

## Hashes anuais

| Ano | SHA-256 |
|---|---|
| 2013 | `4a3d7520ba163bde158091813cc2860a5eca5fe0ab588b817560a8c4219a6a59` |
| 2014 | `1167fbb26ee435bf326f03a879b3b3c5e247f45b2e29303f57a4804d1ce7a4ab` |
| 2015 | `27fb359a6d67a131d5a878dadf383fe3c39ca65531a9bd743bc1340e6c542e79` |
| 2016 | `6b528933efc7ef43665c721ca29085e90e7a8229e4191a76edf5635116a71d9c` |
| 2017 | `43dbb0f99fbae994a763e5f3d0103a0eec28e4344c175a7a27140d137204cbcc` |
| 2018 | `e66c306cd76034fa879033f7c06b8c96ba606ea4a56d81efe78570e090bf1206` |
| 2019 | `11faa69d046bfef7403dee8756df2097f8d2a4f13dbe6b190f24e18a888b726d` |
| 2020 | `9f3e884471a4fef64196f252d6477f25f65c6963d08337a85975b3c8fd8e4a6e` |
| 2021 | `1679ed4ec7e074be9a7b031c153d5e716fdb7a107bcc4dcc544c767e07629242` |
| 2022 | `387b61416817db342f94c86759811000ef40a627320308651ccd6e34cec7d9d0` |
| 2023 | `ee190ca21c4f5bcb2f51577a3fdf2bdfde2fa6832a98e44c2a51131f0f6af572` |
| 2024 | `81804ece28290ddaec5360b1ff57059fbb3f53ceb15e466c940f4db467f68c63` |
| 2025 | `619367dd8b2c5b3db6f7a6c902b41e2f2685616cf8560e2e852e7583f386eec7` |

## Armazenamento canônico

Google Drive:

- arquivo: `DCA_SP_645_2013_2025_CANONICO.csv`;
- file ID: `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`.

R2 privado, bucket `financas-municipais-sp-canonico`:

- `sp_645/dca/2013_2025/normalized.csv`;
- `sp_645/dca/2013_2025/manifest.json`.

O objeto multianual no R2 foi verificado após upload.

## Próximo gate

A conclusão do DCA não promove automaticamente o SP645 ao painel público.

Os próximos blocos são:

1. integrar e validar RREO;
2. integrar RGF;
3. integrar CAPAG;
4. consolidar denominadores/população quando não cobertos pelo contrato DCA;
5. recalcular indicadores legais, derivados, tipologias e pares;
6. executar paridade contra o baseline TIC-TIM 30;
7. somente então decidir a primeira release pública estadual.
