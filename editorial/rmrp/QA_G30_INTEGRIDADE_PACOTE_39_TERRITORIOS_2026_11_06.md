# G30 — Auditoria de integridade do pacote de incorporação — 2026-11-06

## QA estrutural executado
- Matriz CSV (separador ponto e vírgula, UTF-8 com BOM): 39 linhas; 34 municipais, quatro sub-regionais, uma metropolitana.
- Cobertura municipal: Ribeirão Preto 15, Jaboticabal 6, Mococa 6, Batatais 7; sem municípios repetidos.
- Todos os 39 registros possuem `texto_proposto` e `fonte_de_confronto`.
- DOCX G30: 116 parágrafos; os 39 territórios mencionados; 0 tabelas e 0 imagens, porque é caderno analítico, não Volume II.
- PDF G30: 13 páginas.
- Pacote ZIP: integridade testada, nenhum erro de compressão.
- G29: 69 páginas, 45 tabelas e 16 mídias conforme fechamento anterior; DOCX exato não recuperado. **Não houve integração** e não se inferiu sua preservação no pacote G30.

## Manifesto SHA-256 dos artefatos de trabalho
| Arquivo | SHA-256 |
|---|---|
| RMRP_G30_REVISAO_SUBSTANTIVA_2026_11_06.md | d8451f7de52fa85c413cde47dd0daab4a8ae15ea675e8196142484f470f77381 |
| RMRP_G30_MATRIZES_REGIONAIS_E_SINTESE_2026_11_06.md | 18b53552c275a98589189f4e294c048d37f96e581fdfbe8cbd9e22d0688330d5 |
| RMRP_G30_CADERNO_ANALITICO_CONSOLIDADO_2026_11_06.docx | 1d6640ecfcd55760361b3696b653700384defd388bfaaae48d5ee47dd070e66d |
| RMRP_G30_CADERNO_ANALITICO_CONSOLIDADO_2026_11_06.pdf | e602b56e1a3aa1008920ff473a724d3cc84ea26ea7c876ab2df32db78dbcf8e8 |
| RMRP_G30_MATRIZ_INCORPORACAO_39_TERRITORIOS_2026_11_06.csv | b38363a5c2234daa836ffd9da6d36a8fc4d405646397fda08108cef8e11d959f |
| RMRP_G30_RELATORIO_GATE_INCORPORACAO_2026_11_06.md | bcd44d6cb0e5521d6c5a5f89972f3315cdebdb22f4e355a2eb5006f8dbfe220c |

Os arquivos completos continuam no ambiente de trabalho do ChatGPT; hashes no GitHub **não significam** que seus binários estejam depositados no repositório.

## Bloqueio
A pesquisa do histórico da conversa recuperou os nomes de caminhos sandbox temporários para `RMRP_VOLUME_II_REVISAO_PUBLICA_G29.docx`, `.pdf` e ZIP G29, mas **nenhum identificador estável de Drive/Actions/R2**. A pesquisa atual no Google Drive por nomes G29/G28/Lote98 tampouco localizou esses binários. Não copiar G30 sobre Lote 85/G28. Recuperar G29 antes de produzir Volume II completo G30.

## Próximo gate
Confrontar 39 textos propostos com G29, preservar 45 tabelas e 16 mídias, notas fiscais G26, projetos G27 e ajustes cartográficos G28, renderizar e inspecionar cópia derivada antes de circulação.
