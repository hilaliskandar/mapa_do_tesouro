# Lote 104 — Composição das deduções da dívida consolidada de Pontal e diligência de fontes

**Data:** 05/11/2026. **Status:** conferência aritmética da divergência intra-Siconfi realizada; não constitui retificação, conclusão de infração fiscal nem homologação dos indicadores do Volume II (Lote 98, 66 páginas, preservado).

## 1. Método e fontes originais

Consultados diretamente pela API oficial STN/Siconfi os registros do **RGF Anexo 02 do Poder Executivo de Pontal (IBGE 3540200)**, nas colunas `Até o 3º Quadrimestre` de 2025 e `SALDO DO EXERCÍCIO ANTERIOR` de 2026/1º quadrimestre:
- https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2025&in_periodicidade=Q&nr_periodo=3&co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2002&id_ente=3540200&co_poder=E
- https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2026&in_periodicidade=Q&nr_periodo=1&co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2002&id_ente=3540200&co_poder=E

## 2. Resultado da decomposição das deduções

| Componente | Fechamento RGF Q3/2025 | Saldo anterior no RGF Q1/2026 |
|---|---:|---:|
| Dívida consolidada bruta | R$ 173.246.915,32 | R$ 173.246.915,32 |
| Disponibilidade de caixa bruta | **R$ 28.138.160,11** | **Conta ausente no retorno** |
| Restos a pagar processados | R$ 28.986.724,18 | R$ 28.986.724,18 |
| Depósitos restituíveis e valores vinculados | R$ 5.824.302,81 | R$ 5.824.302,81 |
| Deduções da dívida consolidada | **−R$ 6.672.866,88** | **−R$ 34.811.026,99** |
| Dívida consolidada líquida | **R$ 179.919.782,20** | **R$ 208.057.942,31** |
| Receita corrente líquida | R$ 13.494.039,69 | R$ 209.571.785,24 |
| RCL ajustada para endividamento | R$ 13.494.039,69 | R$ 209.271.785,24 |

A contabilidade do fechamento de 2025 reproduz exatamente:

`28.138.160,11 − 28.986.724,18 − 5.824.302,81 = −6.672.866,88`.

Na coluna de saldo anterior apresentada no RGF Q1/2026, as duas saídas continuam iguais, mas **a rubrica de disponibilidade de caixa bruta não aparece no retorno**:

`0 − 28.986.724,18 − 5.824.302,81 = −34.811.026,99`, **apenas como identidade aritmética de verificação**, NÃO como prova de que a disponibilidade contábil real seria zero.

Assim, a diferença entre DCL do RGF 2026 e do fechamento 2025 é exatamente **R$ 28.138.160,11**. Esse valor coincide **centavo a centavo** com a disponibilidade de caixa bruta omitida no retorno da coluna histórica de 2026.

**Conclusão sustentada:** a inconsistência monetária da DCL entre as duas declarações é integralmente explicável **aritmeticamente** pela ausência daquele componente na coluna histórica retornada pela API. Não se pode ainda discriminar se a ausência resulta de preenchimento transmitido, apresentação do RGF simplificado, mapeamento/extração da API, ou reapresentação fiscal legítima. Tal distinção exige acesso à versão protocolizada do demonstrativo e a notas explicativas.

A inconsistência da **RCL de R$ 196.077.745,55** entre o encerramento de 2025 e a coluna de saldo anterior de 2026 é **outra anomalia**, não solucionada pela análise de disponibilidades. Preservar quarentena dos índices do 3º quadrimestre de 2025.

## 3. Diligência de Barrinha

Foram verificadas as URLs oficiais:
- https://portal.barrinha.sp.gov.br/portaltransparencia/
- http://www.barrinha.sp.gov.br:50000/responsabilidade-fiscal/LRF-2025
- http://www.barrinha.sp.gov.br:50000/responsabilidade-fiscal/LRF-2025/ANEXO%20X%20RGF%202%20QUADR%202025.pdf

O portal municipal dispõe de índice e link de PDF rotulado **“RGF 2 QUADR 2025”**, mas a tentativa de recuperar e inspecionar o PDF original pelo Crawl2AI e por screenshot falhou. Não foi extraído nem confirmado qualquer número do PDF nessa rodada. Além disso, **o arquivo se refere nominalmente a quadrimestre e não comprova correspondência ao RGF simplificado semestral de encerramento**, objeto da auditoria. A descoberta e metadados do portal não equivalem à leitura da publicação oficial específica.

## 4. Dados de TCE-SP e outras fontes

A busca externa por cópia de demonstrativos originais e dados TCE-SP retornou sobretudo páginas genéricas de transparência e documentos sem relação direta com as contas controversas. **Nenhum RGF publicado novo, protocolo de retificação, ou memória detalhada da dívida do exercício anterior foi comprovadamente recuperado nesta diligência**. A ausência de localização **não significa inexistência**.

## 5. Artefatos verificáveis produzidos

- Planilha auditada: `/mnt/data/RMRP_LOTE104/PONTAL_RECONCILIACAO_COMPONENTES_RGF_LOTE104.xlsx`, abas de componentes e fontes/limites; 8 componentes, sem fórmula oculta e com valores estáticos observados.
- CSV `/mnt/data/RMRP_LOTE104/PONTAL_RECONCILIACAO_COMPONENTES_RGF_LOTE104.csv` (separador ponto-e-vírgula; decimal vírgula; IBGE string).
- Script: `/mnt/data/RMRP_LOTE104/gerar_controle.py`.
- QA: `/mnt/data/RMRP_LOTE104/QA_LOTE104.json`.

A geração confirmou por `decimal.Decimal` as duas identidades de deduções e a igualdade entre variação da DCL e disponibilidade de caixa bruta de 2025; o XLSX foi reaberto após salvar.

**Persistência confirmada no Google Drive**:
- XLSX **`1VQPUyOxEqm5HCvUOcVJT3Lqfk9WO1KpN`**: https://docs.google.com/spreadsheets/d/1VQPUyOxEqm5HCvUOcVJT3Lqfk9WO1KpN/edit
- CSV **`168tXS52IFh2YjS4Yh8U33KPQodxWiHPT`**: https://drive.google.com/file/d/168tXS52IFh2YjS4Yh8U33KPQodxWiHPT/view

## 6. Próximos gates

1. Reconstituir declaração protocolizada do RGF 2025 e saldo anterior do 2026 de Pontal, especialmente **Disponibilidade de Caixa Bruta**, além de RCL e suas exclusões legais.
2. Obter documento PDF do RGF Executivo **encerramento de 2025** de Barrinha, verificar conteúdo e histórico de retificação `RE` do Siconfi, sem confundir quadrimestre com semestre.
3. Conciliar RGF de Orlândia publicado em 29/01/2026 com declaração Siconfi de 30/01/2026, com foco em DCL e despesa de pessoal e suas versões.
4. Permanecem não sanadas a conciliação FNDE Guariba, lacunas DCA e parâmetros de coeficientes IBS. Preservar a versão editorial **Lote 98, 66 páginas**, sem alterações e em pré-homologação.

**Não atribuir erros ou descumprimentos fiscais a gestores, prefeituras ou sistemas sem evidência independente e manifestação pertinente.**
