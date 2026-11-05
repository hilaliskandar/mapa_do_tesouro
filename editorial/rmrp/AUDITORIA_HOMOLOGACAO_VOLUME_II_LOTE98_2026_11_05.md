# Lote 98 — Auditoria de consistência editorial e matriz de bloqueios para homologação do Volume II

**Data da diligência:** 05/11/2026. **Estado:** revisão documental de consistência concluída, nova cópia Lote 98 produzida e renderizada; **Volume II não homologado para divulgação externa**.

## 1. Fonte preservada e objetivo da intervenção

Documento-fonte: `/mnt/data/RMRP_VOLUME_II_VERIFICACAO_JURIDICA_LOTE97.docx`, 321 parágrafos e 45 tabelas; PDF Lote 97 com 65 páginas. O Lote 98 tratou de contradições editoriais comprovadas ao confrontar seu conteúdo com os dossiês dos Lotes 92–97; **não realizou reextração monetária nem novas afirmações sobre pagamentos FNDE ou retificação de RGF**. O objetivo não foi reeditar as 39 SWOT nem atribuir valor futuro às grades de cenário.

Nova cópia independente: `/mnt/data/RMRP_VOLUME_II_QA_HOMOLOGACAO_LOTE98.docx`. PDF correspondente: `/mnt/data/RMRP_LOTE98_RENDER/RMRP_VOLUME_II_QA_HOMOLOGACAO_LOTE98.pdf`. Documento-fonte do Lote 97 permanece sem alterações.

## 2. Cinco alterações textuais efetivas e correção de rodapé

O diff estrutural do DOCX localizou alterações **exclusivamente** nos parágrafos de índice técnico 2, 9, 12, 263 e 320; todas as 45 tabelas preservam o texto original. A correção do rodapé mantém identidade Lote 98 e atualiza a data para 05/11/2026.

| Trecho | Constatação na edição anterior | Correção incorporada ao Lote 98 |
|---|---|---|
| Identificação | Lote 97 datado como 04/11/2026, embora verificação jurídica tenha ocorrido em 05/11 | Lote 98 (05/11/2026) na abertura e rodapé |
| Critérios de leitura | Nota geral de que todos os valores reais estariam a preços de **setembro de 2026**, ao mesmo tempo em que a nova série de receitas de capital foi deflacionada para **preços médios de 2025** | Nota distingue explicitamente as datas-base e proíbe comparação/soma sem nova conversão |
| Limites iniciais | Texto dizia genericamente que RGF/RREO possuíam lacunas, enquanto Lote 93 já recuperara **RGF de 34/34 municípios** em 2025 | Cita cobertura documental de 34/34 e salienta inconsistências não resolvidas de **Pontal, Barrinha e Orlândia** |
| Limites normativos | Formulação anterior ainda tratava LC 227/2026 como norma apenas identificada, embora o Lote 97 tenha examinado diretamente os arts. 109–117 | Redação registra exame dirigido, sem se apresentar como exegese integral nem como simulação de receitas |
| Nota metodológica final | Formulação ambígua sobre RGF/RREO “parciais” | Diferencia cobertura de entrega da validação dos percentuais e registra as duas bases temporais do IPCA |

**Dados deliberadamente preservados:** 369/374 observações DCA 2015–25; painel equilibrado de 30 municípios; corte 34 municípios em 2024/2025; valores e percentuais de receitas e investimentos; 39 SWOT; 45 tabelas; 15 arquivos de mídia incorporados; mapas e cenários não quantitativos.

## 3. QA técnico efetivamente executado

A edição foi realizada sobre cópia DOCX por alteração localizada; executado `render_docx.py` e verificados seus PNGs e PDF. Resumo:
- **66 páginas** (Lote 97: 65; uma página adicional decorre do fluxo de texto aumentado pelas notas de consistência);
- **66/66 páginas com palavras**;
- **zero caixas de palavras identificadas fora da folha**, em inspeção geométrica por PyMuPDF;
- **321 parágrafos, 45 tabelas**, iguais ao documento-fonte;
- **15 arquivos de mídia Word com os mesmos hashes SHA-256**, o que demonstra preservação binária dos mapas e imagens incorporados;
- **45/45 tabelas com conteúdos idênticos**, conferidas por comparação de matrizes de células;
- parágrafo inicial do limite `Limites:` mantém o prefixo em negrito e texto restante em formatação normal, após correção da primeira renderização;
- inspeção visual em prancha de páginas 1, 2, 16, 56, 57, 58, 65 e 66: sem sobreposições evidentes nos trechos revistos;
- integridade e controle automatizado `/mnt/data/RMRP_LOTE98_RENDER/QA_LOTE98.json`;
- matriz de bloqueios `/mnt/data/RMRP_LOTE98_RENDER/MATRIZ_PENDENCIAS_LOTE98.csv`.

**Limite do QA:** inspeção visual manual ampliada apenas das páginas selecionadas, não de cada uma das 66 em zoom integral. Este lote não substitui verificação exaustiva de fontes, dispositivos, mapas, figuras e anexos antes da homologação externa.

## 4. Matriz de homologação substantiva

| Prioridade | Tema | Comprovação atual | Bloqueio |
|---|---|---|---|
| P0 | Pontal | RGF Q3/2025 informa RCL de R$ 13.494.039,69; RREO B6 informa RCL de R$ 209.571.785,24 | Divergência de R$ 196.077.745,55 entre fontes oficiais, sem retificação conciliada |
| P0 | Barrinha | RGF A02 DCL/RCL 26,62% versus A06 31,40% | Divergência de 4,78 p.p. entre anexos para mesmo encerramento |
| P1 | Orlândia | RGF A02 DCL/RCL -6,55% versus A06 -6,59% | Divergência de 0,04 p.p.; investigar denominador e retificação |
| P0 | Guariba | FNDE Termo 959097/2024, Contrato 043/2025 (R$ 8.576.160,36) e ordem de início de 12/09/2025 documentados | Falta conciliação dos desembolsos e pagamentos com CSV/extrato oficial e execução municipal |
| P1 | DCA I-C | 369/374 observações; cinco ausências de conta sintética, apesar de declarações disponíveis | Confirmar registros originais/retificações; não imputar valor zero |
| P0 | IBS | Art. 115 LC 227/2026 exige ISS e cota-parte ICMS em 2019–2026 com atualização legal própria; art. 116 define publicação dos coeficientes | Ano 2026 não encerrado no momento da diligência, coeficientes de 2027 não publicados; sem parametrização monetária autorizada |
| P1 | Volume II | QA estrutural básico aprovado (66 páginas; mídia/tabelas íntegras) | Falta QA visual integral e revisão jurídica completa antes de circulação |

Classificação P0/P1 neste quadro é **prioridade de resolução editorial**, não atribuição de irregularidade a ente público. As pendências não impedem uma versão de revisão, mas **impedem interpretações categóricas de solvência, de violação de limites fiscais e de ganhos/perdas com IBS**.

## 5. Sequência racional de fechamento

1. Obter provas de retificação ou explicação dos RGF/RREO para Pontal, Barrinha e Orlândia, sem substituir números oficiais por cálculos próprios.
2. Conciliar por chave de instrumento e por data os extratos e CSV de desembolso e execução orçamentária do FNDE 959097/2024; distinguir fonte da União, crédito adicional local, empenho, liquidação e pagamento.
3. Consolidar base municipal 2019–2026 de ISS e cota-parte ICMS com todos os componentes da LC 227/2026; esperar as publicações oficiais necessárias em 2027 para parametrização de coeficientes.
4. Definir editorialmente o tratamento das cinco lacunas DCA por decisão documentada, preservando painel completo de 30 e cortes integrais 34/34 em 2024–25.
5. Fazer QA jurídico e visual final página a página, amarrando cada recomendação à prova e ao dispositivo legal. **Somente após** homologar nova versão de circulação.

**Persistência:** o dossiê foi produzido como texto permanente no repositório GitHub. Os binários da nova edição e arquivos QA estão disponíveis como arquivos gerados na conversa; **não foi confirmado upload ao Google Drive**. Não declarar que os originais do Lote 97 foram sobrescritos ou que houve homologação.
