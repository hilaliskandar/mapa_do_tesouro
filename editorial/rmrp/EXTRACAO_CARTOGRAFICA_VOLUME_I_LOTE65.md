# Lote 65 — Recuperação direta dos 16 mapas individuais do Volume I

Data: 02/11/2026. **Resultado:** o PDF cartográfico original foi efetivamente recuperado do Drive e processado, sem recriar geometrias ou dados.

**Fonte:** `RMRP_VOLUME_PUBLICO_MAPAS_E_ANALISES_16_INDICADORES_2026_10_19.pdf`, Google Drive `10vbnQ_eBNsSmpWekFrrgJyeyTeNlm3YN`, 9 páginas, 4.666.919 bytes.

## Execução verificada

Os quatro mosaicos nas páginas 2, 3, 6 e 7 contêm imagens RGB originais de 3.000 × 2.500 pixels. As imagens foram extraídas diretamente do PDF com `pdfimages -png`. Foram separados por quadrantes 16 mapas raster, originalmente 1.500 × 1.250 pixels por painel. Foi retirada uma faixa superior de 70 pixels para não reproduzir fragmentos de títulos abrangentes do mosaico em cada painel; as imagens finais têm **1.500 × 1.180 pixels**. Esta operação não modifica classes, polígonos, valores, cores ou legendas.

O processo gerou `RMRP_16_MAPAS_VOLUME_I_RECUPERADOS_LOTE65.zip`, contendo 16 PNG e um `manifesto_16_mapas.json` com SHA-256 de cada figura e página original, em ambiente de artefatos desta conversa. Não confundir os arquivos locais com persistência já concluída no Google Drive ou no repositório; a entrega binária foi criada no ambiente desta execução.

## Correspondência dos painéis

| Nº | Indicador | Nome do PNG | Página |
|---:|---|---|---:|
| 1 | Receita corrente per capita | M01_receita_corrente_pc.png | 2 |
| 2 | IPTU, ISS, ITBI/receita | M02_tributos_receita.png | 2 |
| 3 | FPM, ICMS, IPVA/receita | M03_transferencias_receita.png | 2 |
| 4 | Saúde/receita | M04_saude_receita.png | 2 |
| 5 | IPTU per capita | M05_iptu_pc.png | 3 |
| 6 | ISS per capita | M06_iss_pc.png | 3 |
| 7 | ITBI per capita | M07_itbi_pc.png | 3 |
| 8 | FPM per capita | M08_fpm_pc.png | 3 |
| 9 | Despesa corrente per capita | M09_despesa_corrente_pc.png | 6 |
| 10 | Pessoal per capita | M10_pessoal_pc.png | 6 |
| 11 | Pessoal/receita | M11_pessoal_receita.png | 6 |
| 12 | Educação per capita | M12_educacao_pc.png | 6 |
| 13 | Educação/receita | M13_educacao_receita.png | 7 |
| 14 | Investimento per capita | M14_investimento_pc.png | 7 |
| 15 | Evolução dos investimentos | M15_evolucao_investimento.png | 7 |
| 16 | Oscilação dos investimentos | M16_oscilacao_investimento.png | 7 |

## QA e limites

- PDF verificado com `pdfinfo` e `pdfimages -list`; 9 páginas e quatro imagens matriciais de 3.000 × 2.500 pixels.
- Imagem ISS por habitante visualmente inspecionada, com as cinco classes preservadas e legenda legível no recorte. Extração não constitui auditoria visual dos demais 15 painéis.
- O mapa 15, conforme inventário anterior, tem classe de `−10,6% a +16,7%` cruzando zero. A imagem não foi reclassificada e não se pode atribuir sinal à classe por sua cor.
- **Não se localizou ou validou o arquivo vetorial original**; a entrega se limita à reutilização fiel de mapas rastreáveis, que já existiam.
- Para completar a integração no Volume II, é necessário depositar os PNG em armazenamento permanente e substituir referências editoriais por links estáveis aos arquivos efetivamente embutidos, com verificação de paginação e legendas.

**Nota:** a pasta local `/mnt/data/rmrp_cartografia` e o arquivo ZIP são artefatos criados nesta conversa. A matriz de origem continua preservada no Google Drive.
