# FED04 — Retificação do fomento ETI e triagem das exceções, SP645

**Data da auditoria:** 10/11/2026. **Fonte primária vigente examinada:** Portaria MEC nº 823, de 12/12/2025, publicada no DOU em 16/12/2025, que altera a Portaria MEC nº 605/2025 e atualiza o Anexo II anteriormente divulgado na Portaria MEC nº 669/2025. **Estado da auditoria:** documental/monetário, sem verificação bancária individual.

## 1. Controle de versão normativa

- [Anexo II — Portaria MEC nº 669/2025](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/legislacao/2025/portaria-mec-no-669-de-1o-de-outubro-de-2025/@@display-file/file): previa 42,5% outubro, 21,25% novembro, 21,25% dezembro de 2025 e 15% janeiro 2026, com ajustes possíveis.
- [Anexo II retificado — Portaria MEC nº 823/2025](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/legislacao/2025/portaria-mec-no-823-de-12-de-dezembro-de-2025/@@display-file/file): apresenta **dezembro de 2025 e janeiro de 2026 retificados**; janeiro passa a corresponder ao **valor remanescente**, e não se deve aplicar cegamente 15% como pagamento efetivo.
- A extração dos dois PDFs oficiais produziu **452 chaves IBGE7 únicas das redes municipais paulistas em cada edição**. Os valores totais de fomento por rede são estáveis entre as duas versões examinadas, mas os cronogramas individuais sofreram retificação: o confronto de dezembro deve utilizar a Portaria nº 823/2025.

**Regra:** confronto monetário em centavos de `DCA_2025` com `outubro_2025 + novembro_2025 + dezembro_2025_retificado`, preferível a simplesmente arredondar 85% do total. **A proximidade monetária com uma parcela não identifica efetivamente o mês do crédito sem fonte financeira.**

## 2. QA reprocessado

| Universo | Municípios | Listados no ETI | DCA igual à soma mensal 823 | DCA dos exatos |
|---|---:|---:|---:|---:|
| Subgrupo dos 191 | 191 | 191 | **183** | R$ 64.091.050,56 |
| Grupo dos 297 | 297 | 277 | **185** | R$ 65.087.745,47 |
| SP645 | 645 | 452 | **189** | R$ 65.743.889,18 |

**Correção de Cajobi:** `3509304`, DCA R$41.067,45; soma do cronograma retificado `20535,47 + 10267,73 + 10264,25 = 41067,45`. Diferença **R$0,00**, eliminando a diferença de R$3,50 produzida pela aplicação da regra anterior de 85% ao total.

No grupo dos 191, **oito registros** ainda não igualam a soma das três parcelas mensais previstas. A soma de DCA desses oito é **R$1.262.908,45**, parcela do grupo original de R$65.353.959,01. Esse total representa **receitas sob diligência**, não saldo de erro, nem valor de repasse comprovadamente ausente.

## 3. Oito diligências: decomposição ao centavo

| Município | IBGE7 | DCA 2025 (R$) | Soma outubro–dezembro retificada (R$) | Diferença (R$) | Observação |
|---|---|---:|---:|---:|---|
| Itapetininga | 3522307 | 607.329,76 | 809.773,03 | -202.443,27 | DCA coincide com outubro+novembro previstos |
| Cubatão | 3513504 | 340.019,75 | 453.359,66 | -113.339,91 | DCA é compatível, a até R$0,02, com mais de uma combinação de duas parcelas; não atribuir meses sem extrato |
| Iracemápolis | 3521408 | 99.456,88 | 83.707,73 | 15.749,15 | DCA superior ao cronograma; requer abertura das naturezas 171553 e outras |
| Ibirarema | 3519501 | 87.438,17 | 116.584,22 | -29.146,05 | DCA é compatível, a até R$0,02, com mais de uma combinação de duas parcelas; não atribuir meses sem extrato |
| Santo Antônio do Jardim | 3548104 | 58.179,27 | 77.572,36 | -19.393,09 | DCA coincide com outubro+novembro previstos |
| Águas de São Pedro | 3500600 | 33.990,48 | 67.980,96 | -33.990,48 | DCA coincide com outubro previsto |
| Itirapuã | 3523701 | 33.438,02 | 133.752,09 | -100.314,07 | DCA coincide com novembro previsto |
| Santa Rita d'Oeste | 3547403 | 3.056,12 | 4.074,82 | -1.018,70 | DCA é compatível, a até R$0,02, com mais de uma combinação de duas parcelas; não atribuir meses sem extrato |
**Controles anti-inferência:** a dedução de `janela de parcela compatível` é hipótese baseada em valor, não constatação de mês. Em municípios com outubro equivalente à soma de novembro e dezembro, combinações distintas podem resultar em valores quase iguais. Os registros municipais e o SIGEF devem determinar cronologia real.

## 4. Pesquisa de fontes de caixa

O FNDE indica em sua [página pública de perguntas frequentes](https://www.gov.br/fnde/pt-br/acesso-a-informacao/perguntas-frequentes) o sistema **SIGEF — Liberações**: https://www.fnde.gov.br/sigefweb/index.php/liberacoes . A interface foi efetivamente recuperada pelo Crawl2AI, porém **exige CAPTCHA** para realizar consulta parametrizada por ano, UF, município, CNPJ ou programa. **Nenhuma série de liberações individualizada foi recuperada nesta rodada**; o bloqueio não deve ser contornado por declaração de pagamento presumido.

O [Portal da Transparência do TCESP](https://transparencia.tce.sp.gov.br/municipio/iracemapolis/2025) oferece **Receita Detalhada em CSV compactado**, atualizado em 07/03/2026, URL: https://transparencia.tce.sp.gov.br/sites/default/files/csv/receitas-iracemapolis-2025.zip . O portal também publica [lançamentos de receita paginados](https://transparencia.tce.sp.gov.br/municipio/iracemapolis/2025/receitas). O pacote ZIP não pôde ser baixado pela infraestrutura atual; **a disponibilidade do link foi confirmada no portal, mas seu conteúdo não foi inspecionado**. O demonstrativo DCA é conhecido, mas não há identificação documental da diferença positiva de Iracemápolis nesta etapa.

## 5. Plano de conclusão e integridade

1. Priorizar **Iracemápolis**, cuja diferença positiva DCA–ETI retificado é R$15.749,15; consultar abertura de receitas e histórico mensal a partir do arquivo TCESP e fonte municipal.
2. Para os outros sete, consultar pagamentos individualizados no SIGEF e confrontar a receita municipal 2025 com parcelas e datas bancárias. Registrar ausência de evidência como `nao_verificado`, nunca zero.
3. Dos 297 inicialmente apenas DCA, **20 não aparecem no ETI** e **92 aparecem com diferença de valor** após revisão da Portaria 823. Verificar se têm receitas combinadas de modalidades, exercícios anteriores ou classificações diversas; não supor anomalia.
4. Manter as versões 669 e 823 e respectivo anexo na trilha de proveniência. A reclassificação de QA deve **preservar** a matriz original e produzir nova versão, sem edição silenciosa.
5. FED04 permanece `in_progress`; PR #232 `draft`; **sem merge, migração de esquema, alteração do SQLite/R2 produtivo, ou publicação de novas variáveis**.

## 6. Matrizes da revisão 823
- `governance/FED04_ETI_PORTARIA_823_CRUZAMENTO_191_2026_11_10.csv`
- `governance/FED04_ETI_PORTARIA_823_CRUZAMENTO_297_2026_11_10.csv`
- `governance/FED04_ETI_PORTARIA_823_CRUZAMENTO_SP645_2026_11_10.csv`

Essas matrizes registram parcelas do cronograma por município e seu valor de confronto. As matrizes da Portaria 669 são preservadas para comparação de versões; não as empregar como última referência em dezembro/2025.
