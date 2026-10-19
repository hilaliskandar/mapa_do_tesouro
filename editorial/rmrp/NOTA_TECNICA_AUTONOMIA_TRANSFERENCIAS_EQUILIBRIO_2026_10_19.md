# RMRP — módulo de receitas próprias, transferências e equilíbrio corrente, 2013–2025

Data: 19/10/2026. Status: **indicadores descritivos calculados e conciliados, não substituem os conceitos fiscais oficiais da Nota Técnica**.

Base: [DCA SP645 canônica](https://drive.google.com/file/d/1BtXY_FxydMREEbMACJtaoW2n24ohVH33/view), roster territorial em `editorial/rmrp/municipios_subregioes_tcesp.csv`. Referências metodológicas: [Nota Técnica v1.3](https://docs.google.com/document/d/1SvarT65MQMU-qmpjqFzxLjf0d4uKkXpkegmjVCIJZ14/edit), itens 5.1–5.3; [caderno metodológico consolidado](https://docs.google.com/document/d/1ak4JsDeXaAG2eIsqiJJS-y4T25wBa14YrBQ7yA73PUA/edit).

Universo 34 municípios, 13 exercícios, quatro sub-regiões de 15, 6, 6 e 7 municípios. São 442 observações municipais e 65 recortes ano–sub-região/metrópole. Foram aprovadas 234 conferências contábeis de soma sub-regional e metropolitana para 18 conceitos monetários, em cada ano. Controles de cobertura incluem n observado e n esperado em cada conta; totais integrais só quando n = universo.

## Indicadores observados em 2025, cobertura 34/34

| Recorte | IPTU+ISS+ITBI principais / receita corrente | FPM+ICMS+IPVA / receita corrente | Margem corrente aparente |
| --- | ---: | ---: | ---: |
| SR1 | 23,13% | 32,77% | 11,13% |
| SR2 | 14,77% | 45,03% | 8,79% |
| SR3 | 13,34% | 49,66% | 14,52% |
| SR4 | 10,77% | 47,56% | 10,73% |
| **RMRP** | **20,00%** | **37,18%** | **11,07%** |

`tres_tributos_principais` = IPTU principal + ISS principal + ITBI principal. **Não chamar autonomia tributária estrita**, pois faltam taxas e contribuição de melhoria. `tres_cotas_selecionadas` = FPM mensal + cota-parte ICMS + cota-parte IPVA. **Não chamar dependência geral de transferências**: o indicador exclui Fundeb, SUS, assistência e outras fontes. Nenhuma das razões utiliza RCL oficial. `margem_corrente_aparente` = receita corrente bruta DCA - despesa corrente liquidada DCA, sobre receita corrente bruta DCA; não equivale à poupança corrente CAPAG, saldo primário nem disponibilidade de caixa.

A sub-região 1 apresenta participação dos três impostos de 23,13%, enquanto na SR4 é 10,77%. No conjunto das três cotas selecionadas, a SR3 apresenta 49,66%, contra 32,77% na SR1. Essas medidas descrevem composição relativa, não eficiência fiscal ou desempenho de arrecadação.

## Outros indicadores preservados nas bases

- Receita tributária/receita corrente; participações individuais das cotas FPM, ICMS e IPVA; pressão corrente aparente; pessoal e encargos liquidados grupo 3.1/receita corrente; investimento 4.4 e receitas extraordinárias, preservando estágio e ausência.
- Pessoal 3.1/RCL ou receita corrente DCA **não é DTP/RCL legal**. RCL oficial requer RREO Anexo 03 e DTP legal requer RGF Anexo 01 da vigência.
- Não calcular indicador sintético de autonomia econômica adaptada, HHI completo de dependência ou receitas próprias ampliadas até existir mapeamento comprovadamente mutuamente exclusivo das demais contas.
- O módulo é nominal; comparações históricas de montantes exigem IPCA da data-base vigente. Razões de mesmo ano não precisam de deflator.

Arquivos gerados na execução: `/mnt/data/rmrp_nota_tecnica/modulo_autonomia_dependencia_equilibrio_municipal_2013_2025.csv`, `modulo_autonomia_dependencia_equilibrio_subregional_2013_2025.csv`, `expandir_blocos_receitas.py` e `QA_AUTONOMIA_TRANSFERENCIAS_EQUILIBRIO.json`. Salvar cópia persistente e promover a integração ao caderno após QA editorial, sem alterar API e publicação existentes.
