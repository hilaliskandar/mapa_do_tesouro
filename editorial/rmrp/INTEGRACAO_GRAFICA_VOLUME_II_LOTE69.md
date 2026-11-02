# Lote 69 — Integração gráfica ampliada do Volume II RMRP

**Data:** 02/11/2026. **Status:** nova prova editável e paginada, com QA visual panorâmico e verificações estruturais; ainda não homologada para publicação.

## Entrega

Foi utilizada diretamente a edição DOCX do Lote 68 (texto completo e oito mapas) e acrescentadas as figuras F1–F6. Os três gráficos fiscais F2/F3/F4 foram refeitos a partir das mesmas tabelas-fonte dos Lotes 12 e 31 e inseridos no lugar dos marcadores textuais de SVG. A F1 apresenta comparação de **2015 e 2025 por variação percentual**, não a série anual completa — legenda evita denominar incorretamente o gráfico como curva 2015–2025. F5 e F6 são esquemas originais de mecanismos federais/IBS e de cenários condicionais, sem valores financeiros projetados.

### Fontes das figuras
- F1: tabela de variação real das receitas da Parte I, seção 2, cinco territórios (quatro sub-regiões e RMRP), calculadas conforme a documentação anterior; não foram fabricados valores anuais.
- F2: `MATRIZ_EXPOSICAO_FISCAL_RMRP_2025_LOTE12.md`, sete municípios contrastantes, receitas tributárias, FPM e investimentos como percentuais distintos de RC.
- F3: mesma matriz, 34 municípios x quatro sub-regiões, dispersão receita tributária/RC versus FPM/RC.
- F4: `MATRIZ_TRAJETORIAS_MUNICIPAIS_LOTE31.md`, oito municípios, investimentos reais per capita 2023 e 2025 em preços set./2026.
- F5: diagrama conceitual de duas cadeias institucionais (arcabouço fiscal federal e transição ISS/ICMS–IBS), não modelo causal provado.
- F6: três cenários qualitativos condicionais, sem preços ou montantes inventados.

### Artefatos
- `RMRP_VOLUME_II_INTEGRADO_GRAFICOS_MAPAS_LOTE69.docx` — editável, 45 tabelas estruturadas, 14 figuras incorporadas ao objeto DOCX (oito mapas + seis gráficos/diagramas).
- `RMRP_VOLUME_II_INTEGRADO_GRAFICOS_MAPAS_LOTE69.pdf` — 56 páginas formato Letter, PDF de prova; quatro Partes e 39 matrizes SWOT de trabalho preservadas.
- Salvos na Biblioteca em `/RMRP/Volume_II/`, IDs `libfile_bf3e610a9c2c81918b872b882482504c` (DOCX), `libfile_bdf679c895f081918c71147b1e122294` (PDF).
- Fonte da montagem em `/mnt/data/make_lote69.py`; não foi transferida ainda ao repositório.

## Controle de qualidade

`render_docx.py` gerou 56 PNGs e PDF; todos os 56 foram incluídos em prova panorâmica (montagem), que foi examinada para erros grosseiros de diagramação. Conferência estrutural do PDF confirmou 56 páginas e os quatro capítulos presentes. Não equivale à leitura de cada página em 100%; a disposição densa das SWOT e alguns espaços em branco ainda exigem auditoria tipográfica completa. A primeira edição Lote 68 tinha 54 páginas. O documento não foi homologado externamente.

**Limitações:** (1) base ISS principal + ICMS não produz estimativa legal IBS; (2) mapa de variação de investimentos conserva classe cruzando zero; (3) F1 é variação entre 2015 e 2025, e não curva com 11 observações anuais; (4) ainda existem metadados operacionais e linguagem repetitiva no manuscrito; (5) não foram atualizados coeficientes oficiais CGIBS ou base 2026.

## Próximas ações

Conferir cada página em tamanho de impressão; revisar edição e quadros SWOT (sem redução do conteúdo); substituir títulos/legendas obsoletos; verificar fonte/escala dos mapas e exatidão das tabelas; elaborar seção de conclusões e recomendações finais com distinção entre diagnóstico, hipótese e proposta. Não publicar antes da homologação jurídica e gráfica.
