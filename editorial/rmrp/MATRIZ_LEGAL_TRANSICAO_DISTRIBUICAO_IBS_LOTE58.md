# Lote 58 — Transição e distribuição do IBS: matriz jurídico-fiscal aplicada aos 34 municípios da RMRP

**Data da verificação:** 02/11/2026. **Estado:** capítulo normativo e protocolo de incidência municipal para revisão jurídica, sem simulações monetárias não sustentadas. **Base fiscal:** Lotes 55–57, dados DCA canônicos já arquivados. **Fontes normativas:** EC 132/2023 (ADCT, arts. 124–133), LC 214/2025 e LC 227/2026, especialmente arts. 108–117. A LC 200/2023 permanece analisada em capítulo apartado, pois regula diretamente o regime fiscal da União.

## 1. Resultado principal

**A participação municipal observada de ISS principal não é equivalente à receita de referência da transição do IBS.** A LC 227/2026, art. 115, III, estabelece para os municípios dois componentes: **(a) arrecadação de ISS (art. 156, III, da Constituição)** e **(b) parcela creditada do ICMS na forma do art. 158, IV, 'a', da Constituição**. Portanto, examinar somente ISS, ou tratá-lo como receita de transição integral, omite componente relevante.

O art. 115, § 1º, inclui na base dos tributos indicados arrecadação do Simples Nacional e receitas ligadas a multas, juros e dívida ativa nas condições legais. O § 2º considera os valores anuais de **2019 a 2026**, corrigidos até 2026 segundo a variação nominal agregada de ICMS e ISS indicada pela lei; o § 6º define a receita média municipal de referência como soma das médias dos dois componentes corrigidos.

**Implicação para a base RMRP:** o Lote 57 contém ISS *principal* 2015–2025 e é valioso para diagnóstico longitudinal; a DCA canônica dispõe de ISS principal e cota-parte de ICMS, porém não identifica integralmente todos os acessórios e parcelas exigidos no art. 115, nem traz 2026 anual homologado. É inadequado declarar coeficiente oficial ou calcular uma "perda IBS" desses campos. A lacuna não é ausência completa de informação; é **insuficiência para reproduzir o cálculo legal integral**.

Fontes oficiais: https://www2.camara.leg.br/legin/fed/leicom/2026/leicomplementar-227-13-janeiro-2026-798657-publicacaooriginal-177770-pl.html ; https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc132.htm .

## 2. Calendário e instrumentos de repartição

| Período ou data | Dispositivo | Fato normativo | Consequência prática para municípios |
|---|---|---|---|
| 2027–2028 | ADCT art. 127 | IBS com alíquotas transitórias dos componentes estadual e municipal | Preparar contabilidade, cadastro e acompanhamento; sem substituição integral do ISS nesses exercícios |
| 2029 | ADCT art. 128 | Alíquotas de ICMS e ISS reduzidas para 9/10 das alíquotas correspondentes | Exigir análise combinada do declínio gradual do ISS/ICMS e receitas IBS efetivamente distribuídas |
| 2030 | ADCT art. 128 | Alíquotas de ICMS e ISS reduzidas para 8/10 | Atualizar sensibilidade sem extrapolar impacto financeiro linear, pois repartição e receitas não são proporcionais ao simples corte de alíquotas |
| 2029–2077 | LC 227/2026 art. 114 e ADCT art. 131 | Distribuição transitória de parcela retida do IBS segundo coeficientes vinculados à receita média de referência | Preparar base ISS + parcela ICMS e acompanhar coeficiente municipal |
| 2029–2096 | LC 227/2026 art. 117 e ADCT art. 132 | Distribuição complementar relativa a menores razões entre IBS e receita média de referência ajustada | Não presumir perda líquida sem aplicar regra e demais valores exigidos |
| Até 31/08/2027 | LC 227/2026 art. 116, § 1º | CGIBS deverá divulgar coeficientes e memória de cálculo | Criar ponto de controle municipal para conferência, inclusive Siconfi e ICMS creditado |
| Até 30 dias após publicação | LC 227/2026 art. 116, § 7º | Possibilidade de contestação fundamentada pelo município | Preparar procedimento jurídico-contábil de conferência e eventual contestação tempestiva |
| Após contestação | LC 227/2026 art. 116, § 8º | Regra de resposta e republicação de coeficientes quando alterados | Acompanhar retificações e incorporar versão oficial ao modelo de cenários |

**Nota de vigência:** esta síntese não substitui a consulta ao texto consolidado e aos atos supervenientes do CGIBS no momento da preparação final dos cenários ou da abertura dos prazos.

## 3. Condições para a receita média de referência

| Componente municipal | Campo existente no acervo | Limitação para cálculo legal | Próximo teste de QA |
|---|---|---|---|
| ISS principal, 2019–2025 | `dca_iss_principal` | Exclui acessórios; não representa integralmente ISS do art. 115 | Conciliar com receitas detalhadas e dados de Simples, dívida ativa, multas e juros |
| Cota-parte de ICMS, 2019–2025 | `dca_icms_cota_parte` | Confirmar compatibilidade com parcela do art. 158, IV, 'a', inclusive classificações | Comparar valores com fontes pagadoras e relatórios oficiais |
| ISS e ICMS 2026 | DCA canônica arquivada até 2025 | Ano anual de referência ainda não encerrado em 02/11/2026 | Não anualizar execução parcial nem imputar 2026 fictício |
| Correção nominal 2019–2026 | Não calculada na série do Lote 57 | Regra da LC 227 usa evolução nominal agregada de ICMS + ISS, **não IPCA** | Construir fator legal específico quando séries agregadas estiverem disponíveis |
| Coeficientes CGIBS | Ainda não publicados para a janela legal prevista | Não se pode emitir coeficiente oficial próprio | Conferir divulgação oficial de 2027 e abertura de contestação |
| Base de destino e IBS por município | Não comprovada neste acervo | Falta estimativa de base geográfica de operações | Não estimar benefício/distribuição sem base e método |

## 4. Interpretação das exposições municipais

A **exposição contábil inicial** consiste em três eixos separados: (1) participação observada de ISS principal na receita corrente em 2025, descrita pelo Lote 55; (2) série de ISS principal 2015–2025, com cinco lacunas documentadas no Lote 57; (3) participação da cota-parte de ICMS e sua trajetória municipal, a recuperar da mesma base canônica já arquivada, no recorte 2019–2025. A **exposição distributiva líquida do IBS** permanece indeterminada até a aplicação do art. 115, distribuição transitória, destino e eventuais mecanismos complementares. A intensidade de ISS não é classificação de ganhador/perdedor.

Em particular, municípios de menor ISS principal/receita não podem ser rotulados automaticamente beneficiários do IBS; municípios de maior ISS principal/receita não podem ser classificados automaticamente prejudicados. As duas leituras ignoram ICMS creditado, critérios legais de coeficiente, distribuição e diferença entre origem e destino.

O indicador composto ISS principal + ICMS cota-parte **não deve** ser denominado "receita média legal de referência" enquanto não incluir correções normativas e todos os componentes devidos. Pode ser apresentado, com ressalva explícita, apenas como **proxy contábil preliminar** ou composição de receitas observadas.

## 5. SWOT: orientações por perfil fiscal, sem confundir fato e hipótese

### Perfil de maior ISS observado
Ribeirão Preto (13,14% da receita corrente em ISS principal em 2025), São Simão (11,44%) e Sertãozinho (9,99%) devem ter prioridade de *conferência documental do ISS e do ICMS de referência*, e não atribuição antecipada de perda. O investimento é variável adicional separada e não efeito causado pela reforma. A estratégia municipal é preparar a memória 2019–2026, identificar fontes complementares e estruturar conferência de coeficientes em 2027.

### Perfil de menor ISS observado e FPM relativamente elevado
Santa Cruz da Esperança (0,44% do ISS principal e 47,35% da receita corrente em FPM), Cássia dos Coqueiros (1,06% do ISS principal) e Taquaral (2,66% de ISS principal e FPM de 50,92%) precisam de avaliação de ambos os componentes da receita de referência, não inferência de benefício automático. Uma matriz de decisão simples para controle contábil pode ser mais executável do que uma modelagem autônoma sofisticada.

### Perfil de elevada oscilação do investimento
Cravinhos, Jardinópolis, Nuporanga e Sales Oliveira requerem separar exposição à reforma tributária de riscos de financiamento e calendário de obras. A LC 200/2023 não institui teto municipal automático, e um recuo de investimentos não identifica por si a origem federal do choque.

## 6. Produto administrativo imediatamente útil

**Para cada uma das 34 prefeituras:** (a) conciliar ISS total e ICMS creditado de 2019–2026; (b) verificar as fontes consideradas no coeficiente oficial; (c) indicar servidor ou unidade de Finanças/Tributos e Controle Interno responsável por acompanhar o CGIBS; (d) preparar protocolo de contestação fundamentada quando houver divergência; (e) integrar coeficientes efetivamente publicados ao planejamento fiscal 2027–2030, sem inventar valores antes de sua publicação.

**Para coordenação metropolitana:** painel técnico comum com códigos IBGE, série de ISS e ICMS, cobertura de acessórios e fontes de comprovação, data do coeficiente oficial, status de contestação, versão do modelo, data de atualização e indicadores de confiança. Cooperação técnica pode apoiar prefeituras de menor estrutura, sem presumir competências institucionais não documentadas.

## 7. Gates e auditoria

**Concluído no Lote 58:** identificação do mecanismo jurídico central que faltava na SWOT — a referência municipal da transição inclui **ISS e cota-parte do ICMS**; definição do calendário, controle dos coeficientes e procedimento de contestação; protocolo para leitura municipal dos dados.

**Pendente:** quantificação por ente, ISS total com acessórios e Simples, cota-parte ICMS validada em toda a série, correção nominal legal 2019–2026, 2026 anual e modelo de distribuição por destino. A matriz é suficientemente fundamentada para revisar **qualitativamente** as SWOT, mas não para publicar estimativas de perdas e ganhos.

**Próximo lote 59:** incorporar o mecanismo combinado ISS + ICMS e o marco de 2027 nas 39 SWOT, mantendo as capacidades internas e estratégias específicas; em paralelo, recuperar o componente ICMS municipal 2019–2025 da base já existente e classificar a cobertura. Não repetir extrações de FINBRA/DCA.
