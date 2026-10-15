# Extração integral dos investimentos de 2025 por programa e ação — RMJ

**Executada:** 15 de outubro de 2026.  
**Fonte:** Despesa Detalhada, Portal da Transparência do TCESP, arquivos municipais `despesas-{slug}-2025.zip`.  
**Extrator existente reutilizado:** `editorial/rmj/analyze_tcesp_pilot.py`.  
**Execução:** GitHub Actions `RMJ TCESP 2025 Full Backfill`, run `38719698652`.  
**Artefato:** `rmj-tcesp-2025-full-raw`, ID `11963767921`, contendo sete JSONs completos, arquivos stderr e estado de recuperação.  
**SHA-256 do ZIP do artefato baixado:** `0c1d36e14748a15581384c482665f7b448e27c44cad5a0707634a0480fe2844c`.

## Método

Para cada município, o extrator leu a Despesa Detalhada de 2025, filtrou `tp_despesa = Valor Liquidado` e grupo de natureza econômica `44` identificado em `ds_elemento`, preservando código e descrição de programas e ações. Os totais foram calculados em centavos, sem misturar empenho ou pagamento. A soma independente de cada conjunto de programas e de cada conjunto de ações foi confrontada ao total extraído e ao campo `dca_investimentos_liquidada` do arquivo `DCA_SP_645_2013_2025_CANONICO.csv` preservado no Google Drive.

| Município | Programas | Ações | Investimentos liquidados em 2025 | Resultado |
|---|---:|---:|---:|---|
| Cabreúva | 26 | 40 | R$ 19.052.602,58 | Conciliado |
| Campo Limpo Paulista | 10 | 22 | R$ 9.946.853,59 | Conciliado |
| Itupeva | 14 | 34 | R$ 19.953.447,78 | Conciliado |
| Jarinu | 15 | 25 | R$ 11.395.809,12 | Conciliado |
| Jundiaí | 19 | 71 | R$ 137.333.869,84 | Conciliado |
| Louveira | 27 | 40 | R$ 16.296.854,57 | Conciliado |
| Várzea Paulista | 17 | 27 | R$ 51.446.121,59 | Conciliado |
| **RMJ** | **128** | **259** | **R$ 265.425.559,07** | **7/7 conciliados** |

Em cada município: `soma(programas) = soma(ações) = valor extraído TCESP = DCA`; as diferenças apuradas são zero centavo. O gate da nova rotina falha quando faltam registros ou quando a soma de programas e ações diverge do valor extraído.

## Série consolidada 2023–2025

- 2023–2024: 301 registros de programas, 678 de ações, 14/14 conciliações, artefato TCESP `11680818755`.
- 2025: 128 registros de programas, 259 de ações, 7/7 conciliações, artefato `11963767921`.
- Total das listas integrais: **429 registros de programas** e **937 registros de ações** relativos a 21 observações município–exercício.
- Foi gerado `rmj_programas_comparacao_2023_2025.csv` com **188 pares município+código** (agregados ao longo dos anos). Desses, **146 pares** têm código e denominação iguais em pelo menos dois exercícios; 42 aparecem apenas em um ano. Há **99 pares** com código e denominação constantes entre 2024 e 2025. Essa estabilidade nominal e numérica **não comprova permanência do escopo das ações**.
- Arquivos tabulares produzidos na análise: `rmj_programas_investimentos_2025.csv`, `rmj_acoes_investimentos_2025.csv`, `rmj_conciliacao_tcesp_dca_2025.csv` e `rmj_programas_comparacao_2023_2025.csv`. Os arquivos CSV foram entregues na conversa; a evidência bruta e reexecutável reside no artefato e no extrator versionado no GitHub.

## Limitações e decisão editorial

A reconciliação contábil do investimento é completa para 2023–2025, mas a correspondência substantiva de programas de códigos distintos permanece pendente de verificação nas leis orçamentárias e nos conjuntos de ações. Não inferir que o desaparecimento de um código implique o encerramento de uma política pública. Em Várzea Paulista, examinar prioritariamente os programas de saúde 40 (2023) e 70 (2024/2025), sem atribuir equivalência automática. Investimentos liquidados não provam execução física de obras.

**Publicação:** esta entrega é de auditoria e tratamento de dados, sem modificação do boletim público. O próximo estágio é testar correspondências de ações/objetos e produzir decomposições explicativas dos três exercícios sob critérios explícitos.
