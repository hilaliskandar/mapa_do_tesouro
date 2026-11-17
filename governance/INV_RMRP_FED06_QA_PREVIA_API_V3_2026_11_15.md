# FED06 — Auditoria e ampliação da prévia JSON API v3 da RMRP

**Executado em 15/11/2026.** Base: ZIP privado FED05 e SQLite isolado FED04A, ambos já auditados. Nenhuma alteração da base fiscal canônica, do Cloudflare Pages, R2 ou da edição pública.

## Trabalho realizado

1. Reabertura da prévia privada de **56 arquivos JSON**. Auditoria inicial de **213 testes**: 208 controles de integridade aprovados, zero falhas de integridade, cinco bloqueios de publicação.
2. Em cópia isolada da prévia, criação de **218 fichas individuais de projetos Obrasgov** `projetos/{id_url_seguro}.json`, com ID de origem, título, situação, município **proponente** e ausência explícita de localização comprovada; sem inferir pagamentos, instrumentos ou coordenadas.
3. Ampliação dos **34 arquivos municipais** com `codigo_ibge`, `universo_id`, `status=preview_not_published` e `totais_por_dimensao` com `null` para valores não homologados. Inclusão de links relativos para as fichas individuais.
4. Manifesto enriquecido com SHA-256 dos ZIPs originais Transferegov `dcffa72828ac5d7275eed0958b89467f1cf5bcc5480b1b9b1cb2c2bc5d30adca` e Obrasgov `80e1d798fc3bac5b1a4a2ae660be4855c77b0be2e48395a17779cadbfeefeac1`, mantendo `public_release_authorized=false`.
5. Auditoria final do pacote ampliado: **432 verificações**, das quais **427 controles de integridade aprovados, zero falhas de integridade e dois bloqueios de publicação**. Saída final contém **274 arquivos JSON** (56 originais + 218 fichas). Inclui mais de 50 verificações de consulta e acesso, abrangendo todos os 34 municípios, 19 exercícios e 218 projetos.

## Consistência comprovada

| Variável | Total no SQLite e nos JSON |
|---|---:|
| Municípios | 34 |
| Propostas discricionárias | 6.410 |
| Convênios | 1.793 |
| Desembolsos ao convenente | 2.537 |
| Vínculos de emendas | 1.240 |
| Propostas de Parcerias | 743 |
| Projetos Obrasgov por proponente | 218 |
| Exercícios de desembolso | 2008–2026 (19) |
| Desembolsos nominais brutos, centavos | 71.498.911.447 |

Valores representam somente desembolsos brutos ao convenente, **não** pagamentos finais ao favorecido, investimento de capital ou investimento municipal liquidado. Não se atribuiu obra ao município de execução com base na sede do proponente.

## Bloqueios de publicação (deliberadamente não aprovados)

- **Quatro sub-regiões da RMRP:** falta a vinculação municipal à subdivisão metropolitana oficial no JSON. A dimensão SP645 existente no repositório comprova RM/RA/RG, mas não constitui, por si só, uma classificação das quatro sub-regiões. Não deduzir sub-região a partir de RA ou RG.
- **Homologação:** FED03C (pagamento/OBTV/DL) e FED04B (coordenadas/execução física) não foram concluídos com arquivos nacionais e validação documental. `public_release_authorized=false`.

**Fonte de reprodução:** arquivo `RMRP_FED06_PREVIEW_API_V3_PRIVADA_2026-11-15.zip`, contendo `data/api/v3/investimentos/rmrp/` (274 JSON), `qa_rmrp_api_v3.py`, `enrich_rmrp_api_v3.py`, `qa_fed06_enriched.json` e relatório. SHA-256: `f9823c325c5e56df1707d37205b1071ad1c06b320163e364ba9e55d074d50957`; CRC ZIP válido. **Pacote gerado no ambiente desta execução; upload ao Drive não comprovado.** O arquivo original FED05 continua preservado no Drive.

## Continuidade

1. Obter a tabela oficial município–sub-região RMRP, validar 34/34 e gerar os quatro JSON.
2. Executar coleta nacional FED03C em runner autorizado com DNS/HTTP funcionais, sem repetir aquisição regional; conciliar pagamentos e OBTV em nível de `NR_MOV_FIN`, com controle 1:N, estorno e natureza da despesa.
3. Retomar FED04B a partir de `siconv_coordenadas_obra`, documentação de vínculo `ID_PROPOSTA`, geometria municipal e CRS.
4. Apenas com aceite dos gates, realizar QA visual e funcional da prévia em hospedagem privada, sem publicação automática.
