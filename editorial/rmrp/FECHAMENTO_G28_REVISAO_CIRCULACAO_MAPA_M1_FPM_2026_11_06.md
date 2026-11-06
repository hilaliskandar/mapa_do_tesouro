# RMRP — G28 — Revisão final de circulação e mapa M1

**Data:** 06/11/2026. **Base preservada:** Volume II G27 e Lote 98 original.

## Resultados concretos
- **Mapa M1** de localização territorial inserido na página 3, sem atlas separado. Composição: **34 municípios, quatro sub-regiões** (Ribeirão Preto 15, Jaboticabal 6, Mococa 6, Batatais 7), malha municipal IBGE 2022 com **EPSG:4674**. Conferidos 34 códigos únicos, geometrias válidas e 0 geometrias vazias; o mapa não é temático fiscal.
- **FPM — cota mensal**: nota técnica inserida na página 7, estabelecendo que a rubrica de receita da DCA anual contabiliza o total do exercício daquela classificação, sem equivalência a um único mês de transferências. A classificação distingue a cota mensal das cotas extraordinárias. Nenhuma cifra ou classe temática foi recalculada.
- Abertura atualizada para mencionar **8 mapas fiscais, M1 de localização e 6 figuras analíticas**, e rodapé G28 em todas as páginas.
- Ressalvas de Pontal/Barrinha/Orlândia (G26) e Guariba/projetos (G27) permanecem no documento, sem revogação dos limites de inferência.

## QA e preservação
Cópia DOCX: **45 tabelas, 16 arquivos de mídia** (15 mídias idênticas à G27 + novo M1), 15 objetos inline; 66 páginas PDF geradas. Os 66 rodapés estão identificados como G28; o PDF tem texto extraível em todas as páginas; não foram localizados blocos textuais fora do papel. Páginas 3 e 7 examinadas individualmente; 66 páginas inspecionadas em montagens de contato, o que **não equivale à conferência tipográfica linha a linha**.

SHA256 DOCX: `5dfef3fa84dc1ba05b8172e37ce89d995b9a6b7f3337c8acff9aa6fa4159d1e1`.
SHA256 PDF: `21c71bd4585ff19612e8dadaa3850db2c468040db40d4e42c448888f831c00ad`.

## Resultado editorial
Pendência cartográfica **M1 resolvida**. O tratamento dos dados FINBRA/DCA, das divergências RGF/RREO e dos projetos permanece o mesmo dos lotes aprovados e ressalvados. **Volume II G28 preparado para validação editorial final**, mas não se afirma que tenha recebido homologação institucional externa ou revisão jurídica exaustiva; Volume I fora do escopo desta etapa.

Artefatos produzidos e confirmados no ambiente:
- `/mnt/data/RMRP_VOLUME_II_REVISAO_FINAL_G28.docx`
- `/mnt/data/RMRP_VOLUME_II_REVISAO_FINAL_G28.pdf`
- `/mnt/data/RMRP_G28_PACOTE_REVISAO_CIRCULACAO_2026_11_06.zip`
- `/mnt/data/RMRP_G28/G28_QA_FINAL.json`
- `/mnt/data/RMRP_G28/G28_MAPA_M1_MUNICIPIOS.csv`

**Observação de persistência:** relatório e controle do G28 no GitHub não implicam que os binários DOCX, PDF ou cartografia tenham sido enviados para o repositório.
