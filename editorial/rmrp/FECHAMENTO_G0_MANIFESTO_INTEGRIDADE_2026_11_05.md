# RMRP — Fechamento técnico G0: inventário, versões e integridade dos arquivos

**Data:** 05/11/2026. **Referência do plano:** `PLANO_FECHAMENTO_HOMOLOGACAO_VOLUME_II_2026_11_05.md`. **Marco consolidado anterior:** Lote 105. **Estado:** G0 concluído quanto ao inventário local, verificação de integridade de arquivos e persistência do pacote congelado no Drive. **Não confundir com homologação quantitativa G1 nem com decisão de publicação G5**.

## 1. Procedimento executado

Foi inspecionado diretamente o diretório de trabalho `/mnt/data`. Selecionaram-se **25 arquivos essenciais** dos Lotes 87, 93–99, 103–104 e insumos cartográficos, incluindo tanto o DOCX quanto o PDF do Volume II Lote 98, dados DCA, deflator IPCA, painel longitudinal e controles das divergências fiscais. **25/25 presentes**, com SHA-256 de conteúdo calculado em bytes, tamanho e validação estrutural compatível com o formato. O manifesto registra caminho relativo, papel, tamanho em bytes, hash, formato e, quando cabível, número de abas, fórmulas, tabelas, mídias e páginas.

Script reproduzível: `RMRP_FECHAMENTO_G0/gerar_manifesto_g0.py`. Artefatos:
- `RMRP_FECHAMENTO_G0/MANIFESTO_G0_RMRP.json`;
- `RMRP_FECHAMENTO_G0/MANIFESTO_G0_RMRP.csv` (UTF-8 com BOM; separador `;`);
- `RMRP_FECHAMENTO_G0/SHA256SUMS.txt`;
- pacote ZIP imutável por convenção de trabalho `RMRP_FECHAMENTO_G0/RMRP_G0_PACOTE_BASE_CONGELADA_2026_11_05.zip`.

**Nenhum arquivo do relatório ou das bases originais foi editado ou sobrescrito.**

## 2. Versão-base efetivamente recuperada

**DOCX:** `RMRP_VOLUME_II_QA_HOMOLOGACAO_LOTE98.docx`
- tamanho: **2.512.861 bytes**;
- SHA-256: `fffd21bb65251d89caee484c2cabf7b813a7884760f60943c95919e608249df4`;
- estrutura ZIP do DOCX íntegra;
- **321 parágrafos, 45 tabelas, 15 arquivos de mídia incorporados**.

**PDF:** `RMRP_LOTE98_RENDER/RMRP_VOLUME_II_QA_HOMOLOGACAO_LOTE98.pdf`
- tamanho: **2.293.813 bytes**;
- SHA-256: `0f366b6238d569bb206e02f0e5c64dc5ea0877ee8c11606b5a897c2325995743`;
- **66 páginas**, **66 com texto extraível**;
- conjunto de renderização já existente: **66 arquivos `page-*.png`**.

**Continuidade gráfica:** os **15 arquivos de mídia do Word** apresentam hashes SHA-256 idênticos nas edições Lotes 97 e 98. Essa verificação assegura que os arquivos binários incorporados não foram substituídos, mas **não constitui inspeção visual exaustiva das 66 páginas**.

## 3. Recuperação da planilha do deflator IPCA do Lote 94

`RMRP_LOTE94_DEFLATOR_QA/RMRP_RECEITAS_CAPITAL_REAL_IPCA_LOTE94.xlsx`
- tamanho: **87.191 bytes**;
- SHA-256: `71c03c45fd31f1767800d6682cf649c6999af15104845b14a009d700f856dc74`;
- arquivo XLSX estruturalmente íntegro;
- **12 abas**, incluindo `SERIE_374`, `IPCA_2015_2025`, `RECEITA_REAL_2025`, `RESUMO_REAL` e trilhas de QA;
- **1.278 células com fórmulas Excel** encontradas durante varredura de todas as abas; gerador `gerar_lote94.py` e `QA_IPCA_LOTE94.json` recuperados.

Esta é a **planilha efetiva com fórmulas**; não depende da reconstrução das contas com uma nova ferramenta ou da planilha somente de valores do Lote 95. **A validação aritmética e do cache de cada fórmula pertence ao G1**, não foi declarada concluída neste gate.

## 4. Repositório e Drive — persistência

Foi criado pacote de base congelada `RMRP_G0_PACOTE_BASE_CONGELADA_2026_11_05.zip`, **4.397.963 bytes**, contendo **15 entradas**:
- DOCX e PDF do Volume II Lote 98;
- JSON de QA Lote 98;
- planilhas auditadas Lotes 93, 94, 95, 99 e 104;
- script gerador e QA do deflator Lote 94;
- CSV de conciliação Pontal Lote 103;
- manifesto JSON, CSV, lista SHA-256 e script de inventário.

**Integridade do pacote ZIP verificada localmente por `ZipFile.testzip()`, sem erro.**

Uploads confirmados por resposta positiva do Drive e leitura posterior de metadados de nome, tamanho e pasta:
- Pacote congelado: https://drive.google.com/file/d/1eROu1DKokcGlxwv_qRZZLYJAyo__XmeK/view — ID `1eROu1DKokcGlxwv_qRZZLYJAyo__XmeK`, **4.397.963 bytes**;
- Manifesto CSV: https://drive.google.com/file/d/1ftn53gAhbO0ODbiyirJ9FMjWA2URNjVU/view — ID `1ftn53gAhbO0ODbiyirJ9FMjWA2URNjVU`, **4.387 bytes**.

Ambos estão na pasta de trabalho conhecida `1ywdJpIzgXWC9otX9Rq0HBQqYTjzUnRSK`. **O confronto remoto foi feito por metadados e tamanho, não por retransferência e re-hash completo dos bytes remotos**; para exigir identidade remota criptográfica, deve-se baixar o pacote e confrontar seu SHA-256 com o local. Nenhuma afirmação de verificação de bytes remotos foi feita.

## 5. Checklist de aceite G0

| Verificação | Resultado |
|---|---|
| Volume II DOCX recuperado | Conforme |
| DOCX ZIP válido | Conforme |
| Volume II PDF recuperado | Conforme |
| PDF com 66 páginas | Conforme |
| Texto presente nas 66 páginas | Conforme |
| 45 tabelas e 15 mídias | Conforme |
| Mídias sem alteração binária L97→L98 | Conforme |
| 66 imagens de páginas existentes | Conforme |
| Lote 94 XLSX com fórmulas recuperado | Conforme |
| Todos os 25 arquivos do escopo localizados | Conforme |
| SHA-256 de todos os 25 arquivos | Conforme |
| Pacote ZIP criado e validado | Conforme |
| Arquivamento Drive com ID e tamanho confirmado | Conforme |
| Re-hash do arquivo ZIP após download remoto | Pendente opcional para prova forte de identidade remota |
| Auditoria de valores, fórmulas e conclusões | **Não é G0; integrar a G1** |
| Revisão jurídica e visual integral | **Não é G0; integrar a G3/G4** |

**Decisão:** **G0 aceito** quanto a inventário local, disponibilidade e preservação do conjunto de arquivos de referência. O manifesto e os artefatos permitem testar alterações futuras. Não interpretar este aceite como homologação fiscal ou aprovação para público externo.

## 6. Início lógico de G1

1. Validar chaves município–ano e contagem 374/369/5 entre Lotes 93–95.
2. Conferir as 132 observações mensais IPCA e os fatores anuais, inclusive células de fórmulas e valores armazenados em cache da planilha Lote 94.
3. Reproduzir os totais 2024–2025 dos universos 30 e 34 e suas taxas reais, com controle de arredondamento.
4. Estabelecer, para cada número da conclusão do Volume II, fonte, fórmula, ano, universo, unidade, data-base, localização textual e possível ressalva.
5. Manter os campos RCL/DCL/DTP sob quarentena dos Lotes 99–104, sem imputar correções.

**A edição Lote 98 do Volume II permanece preservada.**
