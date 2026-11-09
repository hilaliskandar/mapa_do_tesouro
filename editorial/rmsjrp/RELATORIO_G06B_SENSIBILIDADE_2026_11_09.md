# RMSJRP — G06-B | Sensibilidade independente, polos e exame de extremos dos cenários
**Data:** 09/11/2026. **Estado:** teste de sensibilidade e concentração concluído com QA, sem validação econométrica das premissas. A documentação complementa `RELATORIO_G06_CENARIOS_CONDICIONAIS_2026_11_09.md` e **não substitui** os arquivos G06-v1.

## 1. Método e proveniência
- Arquivos-base recuperados do R2 privado `rmsjrp/g06/2026_11_09/cenarios_v1/`: `G06_SIMULACOES_444_MUNICIPIOS.csv`, `G06_SIMULACOES_60_TERRITORIOS.csv` e `QA_G06.json`; SHA-256 dos arquivos cotejados aos hashes registrados no próprio QA e arquivo `PARAMETROS_G06_2027_2030.json` conferido ao seu SHA na versão G06.
- Script: `editorial/rmsjrp/qa_sensibilidade_g06b.py`. Execução [GitHub Actions 42570037827](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42570037827), resultado `success`.
- **48 testes** = três cenários × quatro anos × (variação real anual de receita ou despesa corrente) × dois choques isolados, **+1 ou −1 ponto percentual** da taxa anual. A variável não perturbada e a proporção de investimento do cenário G06-v1 ficam fixas.
- **Seis recortes** = três cenários × polo São José do Rio Preto e 36 demais municípios, no ano 2030. A decomposição reconcilia receita corrente, despesa corrente e investimento com o total metropolitano, com tolerância de R$ 0,02.
- **Alertas de extremos:** inspecionadas as 444 linhas municipais originais e aplicado limiar **exploratório** de investimento/receita corrente acima de 20% ou abaixo de zero; zero alertas. Esse limiar é apenas controle para revisão, não limite legal, critério fiscal oficial ou prova de plausibilidade.
- Não foi presumida distribuição estatística, intervalo de confiança nem calibração por dados de previsão de 2026.

## 2. Sensibilidade do agregado regional em 2030
Todos os valores são **variações em relação ao mesmo cenário G06-v1**, em milhões de reais constantes de setembro de 2026, após alterar uma taxa isoladamente. Não são diferenças causais estimadas nem valores prometidos em orçamento.

| Cenário | Receita: taxa −1 p.p. | Receita: taxa +1 p.p. | Despesa corrente: taxa −1 p.p. | Despesa corrente: taxa +1 p.p. |
|---|---:|---:|---:|---:|
| Adverso | −359,86 | +374,69 | −352,77 | +366,81 |
| Continuidade | −397,80 | +413,79 | −339,14 | +352,77 |
| Favorável | −421,97 | +438,68 | −339,14 | +352,77 |

Quando a hipótese de crescimento real anual da receita corrente é aumentada em um ponto percentual, o investimento simulado também aumenta mecanicamente, **mantida a mesma razão investimento/receita**. Esse efeito mecânico sobre o investimento em 2030 é:
- adverso: **+R$ 9,14 milhões**; com −1 p.p., **−R$ 8,78 milhões**;
- continuidade: **+R$ 11,88 milhões**; com −1 p.p., **−R$ 11,42 milhões**;
- favorável: **+R$ 22,44 milhões**; com −1 p.p., **−R$ 21,58 milhões**.

A sensibilidade da despesa corrente não é convertida em queda ou aumento automático do investimento: este último foi modelado por uma proporção própria da receita, não pela diferença entre receita e custeio. Assim, o teste não cria saldo financeiro ou teto de aplicação que não existe no dado.

## 3. Efeito de concentração do município-polo, 2030
| Cenário | Participação simulada de São José do Rio Preto no investimento regional |
|---|---:|
| Adverso | **33,59%** |
| Continuidade | **33,59%** |
| Favorável | **49,21%** |

A diferença decorre do método explícito do cenário favorável: para cada município, recuperar até metade da distância positiva entre a proporção de investimento de 2025 e a de 2024 até 2030. O município-polo tinha investimento incomumente concentrado em 2024 e apresentou queda substancial em 2025; por isso o cenário favorável atribui-lhe maior participação na retomada hipotética. **Isso não projeta execução física da carteira da Prefeitura ou do SeMAE e não comprova que a recuperação ocorrerá.**

A participação do polo nos cenários adverso e de continuidade coincide com a proporção de 2025 porque ambos preservam a mesma estrutura relativa de investimentos de 2025 no recorte observado; os valores absolutos mudam com o cenário.

## 4. Verificações e persistência
Foram produzidos e preservados com leitura de retorno SHA-256 no bucket R2 privado, prefixo `rmsjrp/g06/2026_11_09/sensibilidades_v1/`:
- `G06B_SENSIBILIDADES_48.csv`, 48 registros;
- `G06B_POLO_DEMAIS_2030.csv`, seis registros;
- `QA_G06B.json`, manifesto de validação, hashes e resultados.

Não houve arquivo de alertas de extremos, porque **zero municípios-ano-cenário cruzaram o limiar estipulado**. Não se deve inferir inexistência de problemas substantivos a partir desse critério.

## 5. Revisão adversarial e próximas dependências
- O teste demonstra que **variações pequenas de premissas anuais acumulam diferenças expressivas em cinco aplicações temporais (2026–2030)**; o modelo é sensível à ponte de 2026, que não está observada.
- O cenário favorável depende fortemente da recuperação parcial da intensidade de investimento vista em **2024**, um ano possivelmente excepcional na contabilidade regional; é preciso contrastar o resultado com a média 2023–2024 e com a carteira de obras disponível antes de tratar esse ramo como hipótese central.
- O fator de sensibilidade sobre FPM é separado. Não pressupõe cortes constitucionais por LC 200/2023. O orçamento federal 2027 ainda estava em projeto em 09/11/2026.
- Não se utilizaram população projetada, estimativa de IBS, caixa, CAPAG incompleta ou transferências condicionais sem vínculo documental.
- **Próxima ação G06-C:** teste de robustez da referência de investimento (substituir recuperação parcial de 2024 por alternativa baseada em média 2023–2024), inspeção da variação municipal em taxa de investimento e classificação de sensibilidade por sub-região; manter v1 intacta. Então iniciar G07 com matriz de fatos de 37 municípios e revisão editorial independente.
- G05-D continua como frente documental paralela, sem afirmar causalidade da LC 200/2023.

**Estado:** G06-A e G06-B aprovados tecnicamente e persistidos no R2; G06 **em andamento** até calibração adicional e exame da robustez das premissas. Nenhum deploy, publicação ou divulgação foi realizado.
