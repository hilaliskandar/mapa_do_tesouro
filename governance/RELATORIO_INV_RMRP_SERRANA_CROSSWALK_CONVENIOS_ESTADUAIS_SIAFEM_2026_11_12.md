# INV-RMRP — Conciliação de dois convênios estaduais de Serrana por identificadores externos e SIAFEM

**Data:** 12/11/2026. **Escopo:** Convênios municipais estaduais 100540/2024 e 101375/2024, Contratos municipais 078/2024 e 126/2024, com identificação de possíveis números internos SIAFEM/SP. **Status:** correspondência documental composta de alta confiança para 101375; candidato forte para 100540. **Não é uma conciliação por chave literal oficial entre sistemas.**

## 1. Fonte jurídica principal: termo 101375/2024

Documento original da Secretaria de Governo e Relações Institucionais, firmado em **28/05/2024**, disponibilizado no SAPL da Câmara Municipal de Serrana:

- [PDF integral do Termo 101375/2024](https://sapl.serrana.sp.leg.br/media/sapl/public/documentoacessorio/2024/1714/termo_de_convenio.pdf), **152.222 bytes**, SHA-256 **`76c21571b2108c69ebe3d53c57d966e9b08f3a03c552044d7822f668a626483f`**; referência documental do Governo SP **SGRITER2024101463DM**.
- Objeto: recapeamento nas **Ruas Estrela Matutina, Luiz Borges e Francisco Joaquim Rizzotti**, conforme cláusula primeira.
- Valor total previsto **R$ 303.501,56**, sendo **R$ 300.000,00 estaduais** e **R$ 3.501,56 de responsabilidade municipal**. O repasse depende das condições do termo; **valor do termo não é valor pago**.
- Órgão estadual: Secretaria de Governo e Relações Institucionais; convenente: Município de Serrana, CNPJ **44.229.813/0001-23**. A data e o órgão foram confrontados ao SIAFEM.

## 2. Fonte financeira: páginas individuais SIAFEM/SP de 12/11/2026

O portal SIAFEM pode identificar um mesmo instrumento por número **interno**, distinto do número público do termo; essa correspondência não está explicitamente mapeada entre bases, motivo pelo qual os dois casos permanecem classificados quanto à qualidade da prova.

| Elemento | Convênio municipal 100540/2024 | Convênio municipal 101375/2024 |
|---|---|---|
| Contrato municipal | 078/2024, JTR Construções | 126/2024, JTR Construções |
| Concorrência | 007/2024 | 015/2024 |
| Identificador SIAFEM candidato | **51010120240419991** | **51010120240581081** |
| Valor do contrato municipal | **R$ 678.955,71** | **R$ 258.624,91** |
| Celebração cadastrada SIAFEM | 11/04/2024 | **28/05/2024** |
| Valor do convênio SIAFEM | R$ 678.955,71 | R$ 300.000,00 |
| Contrapartida SIAFEM | R$ 0,00 | **R$ 3.501,56** |
| Total SIAFEM | R$ 678.955,71 | **R$ 303.501,56** |
| Liberações registradas | 23/08/2024: **R$ 474.977,26**; 30/04/2025: **R$ 203.978,45** | 10/01/2025: **R$ 258.624,91** |
| Total liberado/estornado | **R$ 678.955,71** | **R$ 258.624,91** |
| Saldo a liberar no SIAFEM | R$ 0,00 | **R$ 41.375,09** |
| Situação declarada na página | EM EXECUÇÃO | EM EXECUÇÃO |
| Classificação | **Candidato forte**, sem termo estadual integral recuperado | **Correspondência composta de alta confiança** |

Fontes oficiais SIAFEM:
- [Ficha interna 51010120240419991](https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/Convenio.aspx?Convenio=51010120240419991).
- [Ficha interna 51010120240581081](https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/Convenio.aspx?Convenio=51010120240581081).

Os valores por ano correspondem exatamente ao arquivo versionado `governance/INV_RMRP_SIAFEM_889_CONVENIO_ANO_EXATO_2026_11_12.csv`: 2024: R$ 474.977,26; 2025: R$ 203.978,45 no primeiro ID; 2025: R$ 258.624,91 no segundo. Entre os **35 instrumentos SIAFEM vinculados à Prefeitura de Serrana** presentes no snapshot, **cada uma das duas somas é única**.

### Testes de identidade e restrições

O **101375/2024** apresenta uma convergência que vai além de coincidência de valor: documento estadual com **data 28/05/2024**, objeto e CNPJ da Prefeitura, órgão concedente, convênio no valor **R$ 300.000,00 + contrapartida R$ 3.501,56 = R$ 303.501,56**; todos esses elementos são exatamente os declarados na ficha SIAFEM **51010120240581081**, mais a liberação de mesmo valor do contrato municipal 126. Classificação: **correspondência documental composta de alta confiança**, embora ainda não exista documento publicado que associe explicitamente os números `101375/2024` e `51010120240581081`.

Para o **100540/2024**, o contrato municipal 078 tem objeto de recapeamento, beneficiário e órgão estadual compatíveis e **R$ 678.955,71** de valor contratado, igual ao total de duas liberações do SIAFEM **51010120240419991**. Porém o termo completo 100540 não foi recuperado, e o cadastro SIAFEM não cita esse número público. Classificação: **candidato forte, não homologado por chave documental**. O [Diário Oficial municipal nº 1.651 de 27/06/2024](https://www.serrana.sp.gov.br/media/uploads/diario_oficial/diario_oficial_1651.pdf) informa o Convênio 100540/2024, Demanda **062650**, e designa responsáveis; [Decreto nº 071/2024 no Diário nº 1.618](https://www.serrana.sp.gov.br/media/uploads/diario_oficial/diario_oficial_1618.pdf) indica dotação inicial para recapeamento sob o convênio. Isso ainda não associa o número interno financeiro do SIAFEM ao número externo.

## 3. O que NÃO deve ser inferido

- **R$ 937.580,62** é a soma das liberações de **dois IDs SIAFEM já existentes** na série RMRP. Esse total é um **subtotal descritivo, NÃO uma receita ou investimento adicional** aos R$ 305.521.029,20 já contabilizados.
- Liberação estadual ao Município de Serrana **não é pagamento à empreiteira**, nem liquidação da despesa municipal, nem medição ou conclusão física. A coincidência com os valores dos contratos deve ser utilizada como pista de identificação e controle, nunca como prova de execução financeira municipal.
- A categoria `EM EXECUÇÃO` informada pelo SIAFEM não confirma execução física, medições ou recebimento definitivo.
- **Não criar `inv_instrumento_projeto` como vínculo financeiro homologado para o projeto federal Obrasgov 30461.35-22** apenas porque há contratos semelhantes em Serrana. Os dois contratos estaduais são objetos específicos e distintos do contrato federal 117/2024.
- O ZIP de dados abertos de convênios disponibilizado no Portal da Transparência SP em 11/11/2026 contém CSV simplificado de aproximadamente 3.618 linhas, mas **não apresenta números públicos de convênio como coluna** e seus campos históricos do período analisado são incompletos para Serrana. Não usar o ZIP como prova de crosswalk; exigir documento estadual com número externo e interno, caso disponível.

## 4. Governança e QA

Registro estruturado: `governance/INV_RMRP_SERRANA_CROSSWALK_100540_101375_SIAFEM_510101_2026_11_12.json`. O validador `pipeline/qa/qa_inv_rmrp_candidatos_siafem_obrasgov.py` exige:
- presença dos dois convênios externos e dois IDs internos SIAFEM;
- totais exatos em centavos e unicidade das somas entre 35 instrumentos de Serrana;
- conferência dos registros anuais reais do SIAFEM já versionados;
- equivalência orçamentária termo 101375 × ficha SIAFEM;
- controle explícito de **zero vínculos homologados por identidade literal**;
- preservação de não aditividade e inexistência de prova de pagamento à contratada.

**Próximos gates:** localizar o termo completo 100540/2024, eventualmente em plataforma de demandas SP Sem Papel/Câmara; buscar referência interna SIAFEM nos anexos de prestação de contas e balancetes; conferir os trechos físicos dos três contratos pela documentação técnica; manter PR nº 233 draft sem escrita produtiva.
