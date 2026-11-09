# FED00 — Validação territorial STN contra o SQLite canônico SP645

**Referência:** 09/11/2026. **Resultado:** `qa_pass_identity_only` — homologação **exclusivamente da identidade municipal**; não há aprovação de valores, categorias ou conciliação financeira.

## Prova da execução

- [GitHub Actions run 42661684901](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42661684901): workflow `sp645-private-site-artifact.yml`, conclusão **success**.
- [Artefato de QA 13693814005](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42661684901/artifacts/13693814005), `qa_stn_sqlite_identity_sp645.json`, recuperado e inspecionado.
- Script versionado: [`pipeline/qa/audit_stn_sp645_crosswalk.py`](../pipeline/qa/audit_stn_sp645_crosswalk.py).
- Fonte R2 existente: `financas-municipais-sp-canonico/sp_645/federal/stn/2026_09/candidates/STN_IBGE_SP_MATCH_CANDIDATE_20c80f6464de.csv`; SHA-256 `20c80f6464de30f899430327db569fd7a52610c14bfc88678b769638572f036c`.
- **Banco realmente consultado:** `build/sp645_private.sqlite`, materializado pelo procedimento original `pipeline.build.build_sp645_private_site`, a partir dos mesmos inputs canônicos R2 utilizados no processo de publicação privada. O script de QA usa conexão SQLite `mode=ro` com `PRAGMA query_only=ON`; não cria nem modifica tabelas.

## Indicadores e discrepâncias observados

| Controle | Resultado |
|---|---:|
| Registros STN no crosswalk candidato | 645 |
| Códigos STN distintos e válidos | 645 |
| Registros SP_645 do SQLite real | 645 |
| Códigos SQLite distintos | 645 |
| Códigos presentes no STN e ausentes no SQLite | **0** |
| Códigos presentes no SQLite e ausentes no STN | **0** |
| Códigos duplicados no universo SQLite | **0** |
| UF diferente de SP | **0** |
| Pareamentos exatos com normalização documentada | 643 |
| Pareamentos por alias histórico com código explícito | 2 |
| Denominações literais divergentes entre fontes | 10 |

Os dez nomes divergentes são: Aparecida DOeste (3502606), Estrela DOeste (3515202), Florínia (3516101), Guarani DOeste (3518008), Palmeira DOeste (3535200), Santa Bárbara DOeste (3545803), Santa Clara DOeste (3546108), Santa Rita DOeste (3547403), São João do Pau DAlho (3549300) e São Luís do Paraitinga (3550001). Esses dez registros diferem no **texto** entre STN e `municipio.nome` do SQLite, mas **não** no código IBGE, na UF nem na composição do universo.

As diferenças entre nomenclatura histórica do GeoJSON e nomes oficiais do IBGE permanecem documentadas em [`STN_IBGE_EXCECOES_NOMES_2026_11_09.csv`](STN_IBGE_EXCECOES_NOMES_2026_11_09.csv). Não substituir `municipio.nome` pelos valores STN; preservar nome bruto como atributo de proveniência.

## Condição de uso e próxima ação

**Decisão:** a junção por `codigo_ibge` pode ser utilizada em um **pipeline experimental** de normalização STN para os 645 municípios, sem criar tabela municipal concorrente. Toda observação deverá continuar vinculada à origem `resource_id`, `download_sha256`, competência interna `ANO/Mês`, item, classificação da transferência e estágio do pagamento.

**Não aprovado:** valor do decêndio, interpretação do campo vazio, tratamento de sinais e deduções, eventual sobreposição entre `FPM`, `FPM 1%`, `DEDU`, FUNDEB e ajustes, e conciliação com DCA/SICONFI. A competência do arquivo inspecionado é setembro/2026 apesar do título CKAN `202610`.

**Próxima operação:** homologar o perfil monetário por decêndio, com separação entre inteiros, ponto decimal, vírgula decimal e códigos não numéricos. Testar grão `UF/município/ano/mês/Transferência/Item transferência` e critérios contábeis antes de qualquer totalização. Persistir QA versionado e somente avançar para módulo de fatos federais após prova de unidade e conceito.

**Estado dos gates:** FED00 possui validação territorial `qa_pass_identity_only`, mas o gate geral segue `in_progress`. FED01 e carga fiscal estadual ainda não aprovados. Não houve publicação e nenhuma série fiscal foi escrita no SQLite.
