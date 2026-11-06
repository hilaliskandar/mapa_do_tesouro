# RMRP — G25 — Recuperação efetiva de dados Audesp 2025 e conciliação dirigida

**Execução:** 06/11/2026. **Estado:** duas bases oficiais obtidas, auditadas e preservadas em artefato GitHub; quatro restrições FIS-01 a FIS-04 continuam abertas. Lote 98 e Volume II G20 não alterados.

## Prova de coleta
O runner isolado [42158788986](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42158788986) concluiu com êxito e produziu artefato **13476001241** (`rmrp-audesp-g25-evidencias`). Os dois ZIPs oficiais foram baixados por HTTPS **com validação de certificado**, corrigindo o hostname para `transparencia.tce.sp.gov.br` sem `www`, e passaram por `zipfile.testzip()`:
- **RCL mensal:** 90.803 registros CSV; recurso `https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/rcl_completo.zip`; SHA-256 `282969601507190e7e147d514d56fa3178c74f0dd53d649f227644a3aaae6576`.
- **Resultado das análises Audesp:** 6.440 registros CSV; recurso `https://transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/resultado_analises_audesp.zip`; SHA-256 `fe1254d15400706c180450aa76f7350e929c249fe2d3714006d782475f0abaa2`.

CSVs originais usam separador `;` e codificação `cp1252`. O filtro inicial continha falso positivo **Pontalinda** e omissão de **Orlândia** por acentuação; o coletor foi corrigido, reexecutado e validado: **36 linhas mensais RCL em 2025 (12 por município) e 3 linhas anuais de análises em 2025**, sem duplicação das chaves exatas.

## Indicadores realmente observados nas bases (R$)
| Município | IBGE | RCL Audesp, dez./2025 | Pessoal Executivo, análises Audesp 2025 |
|---|---|---:|---:|
| Pontal | 3540200 | **209.571.785,24** | **101.153.171,46** |
| Barrinha | 3505609 | **163.137.716,10** | **81.810.937,42** |
| Orlândia | 3534302 | **263.831.501,04** | **139.863.791,37** |

**Pontal:** RCL Audesp coincide ao centavo com RREO B6/2025 e saldo do exercício anterior RGF Q1/2026. Difere do RGF Q3/2025 (R$ 13.494.039,69) em **R$ 196.077.745,55**. Pessoal Audesp difere do Diário Oficial (R$ 101.819.534,91) em **R$ −666.363,45**, e do RGF Q3 Siconfi (R$ 108.682.695,50) em **R$ −7.529.524,04**. FIS-01 aberta. A DCL continua com diferença aritmeticamente explicada de **R$ 28.138.160,11** por componente ausente na coluna histórica de 2026; causa documental não provada (FIS-02 aberta).

**Barrinha:** RCL Audesp **R$ 163.137.716,10** versus RCL **ajustada para dívida** do RGF S2/2025 **R$ 161.507.819,10**, diferença **R$ 1.629.897,00**. **Não tratar como erro**, pois RCL mensal e ajustada são conceitos diferentes. Pessoal Executivo Audesp 2025 **R$ 81.810.937,42**, ainda sem numerador documental equivalente homologado. FIS-03 aberta.

**Orlândia:** RCL Audesp **R$ 263.831.501,04** difere da RCL ajustada para dívida **R$ 263.501.501,04** em **R$ 330.000,00**, e da RCL ajustada para pessoal **R$ 261.870.013,04** em **R$ 1.961.488,00**; diferenças podem refletir exclusões distintas. **Pessoal Audesp R$ 139.863.791,37 coincide exatamente com o Diário Oficial nº 2238 (29/01/2026)** e difere do pessoal no RGF S2 Siconfi **R$ 139.797.400,92** em **R$ 66.390,45**. A concordância de Audesp com jornal municipal não prova independência de lançamentos contábeis; a causa da diferença entre versões não está comprovada. Divergência da DCL DO versus Siconfi (R$ 2.455.624,32 em módulo) permanece, FIS-04 aberta.

## Limites e decisão
Os campos Audesp de percentual de pessoal nos três registros anuais estão vazios; não imputar percentuais calculados como valores oficiais. Comparações de RCL mensal com RCL ajustada são **diagnósticos de diferença**, não prova de erro. Estas bases dependem de dados prestados pelas prefeituras e não constituem auditoria contábil independente.

**Resultado:** o obstáculo de download G23–G24 está resolvido, com prova binária e rastreabilidade; as quatro divergências de versão RGF ainda carecem de documentação e **não autorizam juízo de descumprimento LRF nem edição do Volume II G20**.

O pacote local `RMRP_G25_PACOTE_CONCILIACAO_AUDESP_2026_11_06.zip` inclui artefato bruto do runner, CSV de comparação, QA JSON, relatório integral e script reprodutível.

**Próximos atos:** recuperar protocolos e versões dos RGF de Pontal e Orlândia, demonstrativo semestral retificado de Barrinha, e memórias de RCL/DTP/DCL. Manter restrições FIS-01 a FIS-04.
