# RMSJRP — G05-D | Aditivos, execução contratual e bloqueio da prova de liquidação
**Data da diligência:** 09/11/2026. **Status:** confronto dos aditivos de três contratos de Olímpia com suas fichas oficiais executado; **sem prova de empenhos/medições/liquidações por contrato**. Distinguir diligência documental e reconciliação contábil.

## 1. Ponto de partida e escopo
Continuação de [RELATORIO_G05D_CONTRATOS_OLIMPIA_2026_11_09.md](RELATORIO_G05D_CONTRATOS_OLIMPIA_2026_11_09.md), posterior ao PR #222. Não repetir a recuperação dos 82 cadastros de obras, dos 2.512 registros nas duas listagens de contratos, do DCA ou dos dados TCESP. As três correspondências entre contrato e ficha de licitação já haviam sido aprovadas por chave composta; a presente diligência **examinará justificativas e datas de aditivos** para avaliar se a ausência de uma rubrica de investimento é sinônimo de paralisação física.

## 2. Fichas oficiais examinadas
- Contrato **558/2023**, processo **136344/2023**, obra de implantação do anel viário entre Distritos Industriais I e II e Jardim Alvorada/Santa Fé. Fonte primária: https://www.olimpia.sp.gov.br/portal/editais/0/1/3878/ .
- Contrato **189/2024**, processo **137300/2023**, recapeamento do pavimento asfáltico com CBUQ. Fonte primária: https://www.olimpia.sp.gov.br/portal/editais/0/1/3927/ .
- Contrato **115/2024**, processo **140113/2023**, duplicação da Via de Acesso João Custódio Sobrinho. Fonte primária: https://www.olimpia.sp.gov.br/portal/editais/0/1/3999/ .

A recuperação direta pelo Crawl2AI conectado falhou tecnicamente para essas páginas. Foi feita leitura por mecanismo alternativo de recuperação web; as fichas HTML foram inspecionadas. O download dos arquivos anexos de aditivos das fichas retornou erro de cache na tentativa de leitura: **não afirmar que os PDFs anexados foram baixados ou visualmente auditados**. As datas, justificativas e valores apresentados abaixo são os *metadados e descrições exibidos nas fichas oficiais*, não transcrições homologadas dos documentos em PDF.

O CSV [G05D_ADITIVOS_OLIMPIA_2024_2025.csv](G05D_ADITIVOS_OLIMPIA_2024_2025.csv) registra **oito ocorrências documentais selecionadas**, não uma coleção exaustiva de todos os aditivos desses contratos.

## 3. Resultado por contrato
### 3.1. Anel viário — 558/2023
A ficha municipal registra **cinco aditivos datados de 2025**:
- **27/01/2025:** prorrogação atribuída ao período de chuvas e à adequação de projetos de drenagem e fechamento provisório de propriedades;
- **29/03/2025:** prorrogação por chuvas intensas, com dificuldades para execução de serviços externos;
- **27/06/2025:** prorrogação por serviços finais ainda necessários, como acabamentos da drenagem e plantio de grama;
- **26/08/2025:** prorrogação, acréscimos e supressões decorrentes de adequações de drenagem, greide, movimentos de solo e paisagismo. A justificativa menciona explicitamente **reprogramação contratual sem necessidade de novo empenho** para determinada execução;
- **24/09/2025:** reajuste contratual relacionado à data-base.

**Interpretação sustentada:** havia ajustes técnicos e de cronograma **registrados administrativamente em 2025**, e a justificativa de junho menciona serviços finais por executar. A observação sobre execução de alterações *sem necessidade de novo empenho* impede supor correspondência 1:1 entre cada aditivo e novo empenho orçamentário. Também não autoriza afirmar que não existiram liquidações ou pagamentos naquele ano. O sinal administrativo de “licitação concluída” na ficha de editais é estado do procedimento licitatório, **não certificado de conclusão física da obra**.

### 3.2. Recapeamento CBUQ — 189/2024
A ficha oficial identifica:
- **15/04/2025:** acréscimo quantitativo de **R$ 1.198.286,05**, justificado por novas demandas durante a execução dos serviços;
- **13/06/2025:** prorrogação, com justificativa expressa de que a vigência existente seria insuficiente para o encerramento da obra.

**Interpretação sustentada:** o contrato sofreu alterações quantitativas e de prazo em 2025. Isso enfraquece hipótese de conclusão integral antes de 2025, mas **não mede despesa liquidada** no período; a reprogramação pode coexistir com empenhos anteriores, pagamentos posteriores e diferentes fontes de financiamento.

### 3.3. Duplicação da Via João Custódio Sobrinho — 115/2024
A ficha apresenta aditivo de **26/11/2024**, com **R$ 696.890,47** de acréscimo e **R$ 114.336,90** de supressão, por alterações em rotatória, prolongamento viário e serviços de drenagem/escavação. A descrição registra prorrogação de prazo de execução, mas esta diligência não encontrou novos valores de liquidação em 2025, nem comprovação financeira de medição vinculada ao aditivo.

**Interpretação sustentada:** alterações de escopo e prazo efetivamente documentadas em 2024; **a mera vigência até março de 2025 não é prova de desembolso ou liquidação em 2025**.

## 4. Tentativa de localizar despesas e bloqueios
O site oficial da Prefeitura mantém uma página de **Transparência** que encaminha para o Portal de Acesso à Informação SMARAPD e os balancetes municipais. Endereços úteis: https://transparencia-olimpia.smarapd.com.br/ e https://www.olimpia.sp.gov.br/portal/contas_publicas . A consulta de despesas por fornecedor, número de empenho ou vínculo de contrato **não pôde ser comprovada nesta rodada**:
- Em ferramenta de navegação com JavaScript, a aplicação permaneceu em “Carregando Portal de Acesso à Informação”; uma segunda observação não apresentou conteúdo interativo.
- O serviço conectado Crawl2AI retornou erro interno para as fichas licitatórias e página de transparência.
- A pesquisa documental dirigida aos processos 136344/2023, 137300/2023 e 140113/2023, combinados a “empenho”, “liquidação” e “medição”, não revelou documento primário com chave explícita em fonte acessível.
- A tentativa de recuperar o texto de documentos anexados em PDF às fichas não foi concluída devido a erro de cache. Não houve extração validada dos balancetes de dezembro de 2024 e 2025.

**Status de cada contrato em 09/11/2026:** objeto e vínculo ao contrato na ficha de licitação = comprovados; aditivos e justificativas na ficha oficial = verificados; **empenho individual, medição e liquidação ano a ano = não verificados**. Não imputar zero e não classificar a ausência como descumprimento do município.

## 5. Implicações para o diagnóstico metropolitano
O caso de Olímpia demonstra que **a dinâmica física e contratual das obras não pode ser inferida apenas da diferença de investimentos liquidados por exercício**. Existe documentação de prorrogações e aditivos posteriores ao início dos contratos e à data inicial de vigência, mas o nexo contábil com a DCA/TCESP continua ausente. Esses três contratos são de **obras viárias/urbanas**, e não se deve associá-los automaticamente ao programa municipal 45 — Concessão Água e Esgoto ou ao programa 31 — Projetos e Obras Públicas.

As variações fiscais metropolitanas e a interpretação sobre impactos indiretos da LC 200/2023 devem conservar, portanto, a separação entre:
1. fenômeno fiscal observado (liquidações agregadas DCA/TCESP);
2. evento administrativo comprovado (contratação, aditamento e ajustes de prazo);
3. mecanismo de financiamento identificado (quando houver documento primário);
4. inferência causal não identificada (não apresentar como conclusão).

## 6. Continuidade e decisão operacional
A nova prova permite **fechar o sublote de leitura das fichas dos três contratos**, mas **não fecha a conciliação financeira G05-D**. Para ultrapassar esse limite será preciso dispor da execução analítica por empenho/credor/contrato, de notas de medição ou de documentos vinculados aos processos. Há duas vias tecnicamente adequadas:
- exportação pública da consulta detalhada de despesas do sistema SMARAPD, caso se torne acessível;
- solicitação administrativa/e-SIC das notas de empenho, liquidações, pagamentos e medições dos três processos para 2024 e 2025.

Em paralelo permanece o G05-D de Monte Aprazível, contrato 08/2024, e São José do Rio Preto, ações 1003/1004 e SeMAE 1029. **Não repetir** o inventário DCA/TCESP nem as matrizes já persistidas.

**Próxima ação exata:** documentar a indisponibilidade das consultas SMARAPD; decidir eventual pedido documental dos processos prioritários; preparar G06 com cenários condicionais, sem atribuir causalidade onde não existe vínculo orçamentário demonstrado. Atualizar README e HANDOFF a cada mudança de chat. Estado final deste lote: `G05-D=in_progress, evidence_partially_verified`.
