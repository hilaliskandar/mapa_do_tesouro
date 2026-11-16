# FED19 — Cinco projetos adicionais com evidências oficiais e salvaguardas de execução

**Data da auditoria:** 16/11/2026. **Base regional federal:** snapshot de 15/11/2026. **Objetivo:** continuar a homologação documental dos 19 projetos Obrasgov com divergência entre município proponente e coordenadas SICONV, sem gerar falsas localizações de execução ou equiparar contrato, empenho e pagamento.

## Resultado geral

Cinco fichas distintas foram enriquecidas nesta etapa FED19, **além dos sete projetos prioritários já documentados no FED16–FED18**. Assim, a auditoria de fontes independentes abrange **12 dos 19 projetos prioritários**; **sete** ainda necessitam busca dirigida adicional, considerando os critérios desta série. A cobertura não significa que todos tenham suas execuções físicas ou localizações homologadas.

### Monte Alto — Mercado Municipal, projeto Obrasgov `27237.35-06`

O edital oficial [Concorrência Eletrônica 99026/2025, Processo SA/DL 154/2025, Edital nº 109/2025](https://montealto.sp.gov.br/site/wp-content/uploads/2025/07/EDITAL-OBRA-DE-REFORMA-E-ADEQUACAO-MERCADO-MUNICIPAL.pdf), **Anexo II — Termo de Referência**, identifica a **reforma e adequação do Mercado Municipal** com endereço de intervenção projetada **Rua Florindo Cestari, nº 861, Centro, Monte Alto/SP**, e menciona expressamente o **Contrato de Repasse 946417/2023 MAP/CAIXA**. O memorial especifica cobertura, esquadrias, pintura e instalações. A fonte apresenta dotação `4.4.90.51`, isto é, classificação orçamentária prevista, **não pagamento GND4 efetivo**.

**Aceite:** correspondência documental de instrumento e **endereço do imóvel de intervenção prevista**, sem coordenada física georreferenciada própria nem medição ou recebimento comprovados. O processo licitatório não prova conclusão ou pagamento. A referência original do edital foi mantida na ficha; o PDF foi identificado e lido pelo extrator de documentos da fonte pública, mas o serviço de crawling retornou erro ao tentar capturá-lo e a leitura remota direta foi limitada — sem alegar cópia local persistida do PDF nesta rodada.

### Barrinha — dois contratos de repasse distintos, projetos `23598.35-24` e `9118.35-82`

A [publicação oficial da licitação TP 016/2022 em 09/12/2022](https://www.escavador.com/diarios/5596121/DOU/secao-3/2022-12-09?page=271) discrimina explicitamente:

- **Lote 1:** obras de pavimentação/recapeamento e adequação de vias urbanas, **Convênio Caixa 917013/2021**, projeto `9118.35-82`.
- **Lote 2:** objeto similar, porém **Convênio Caixa 916578/2021**, projeto `23598.35-24`.

A [publicação de 28/01/2023 no Diário Oficial de SP](https://www.escavador.com/diarios/5611006/DOESP/executivo-i/2023-01-28?page=336) confirma **rescisão amigável do Contrato Administrativo 067/B/2022**, no Processo Licitatório 067/2022, **exclusivamente para o Lote 2/Convênio 916578/2021**, com a contratada **NECA Engenharia e Construções EIRELI**, sob art. 79, II, da Lei 8.666/1993.

**Aceite:** separação dos objetos e histórico contratual do **lote 2 rescindido**. A rescisão do contrato não comprova cancelamento do convênio, inexistência da obra, ausência de eventual nova contratação nem inaplicabilidade do lote 1. As metas físicas municipais de outras tabelas **não foram convertidas em execução medida** sem confirmação de sua natureza e competência. Sem geometrias lineares efetivamente executadas para ambos.

### Cravinhos — habitação, projeto `46389.35-04`, compromisso `974453/2024`

A [publicação do aviso do Pregão Eletrônico 071/2025 em 08/12/2025](https://www.escavador.com/diarios/6179578/DOU/secao-3/2025-12-08?page=226) relaciona a contratação de **Projeto de Trabalho Social (PTS)** ao Termo de Compromisso **974453/2024/MCIDADES/CAIXA** do MCMV FNHIS Sub-50, vinculado ao projeto de moradias no **Loteamento Buenópolis I**.

O [Diário Oficial de SP de 08/04/2026](https://www.escavador.com/diarios/6248203/DOESP/municipios/2026-04-08?page=9) reproduz **parecer jurídico datado de 07/04/2026**, opinando pela anulação do Pregão 071/2025 e do contrato administrativo assinado em 30/12/2025, por razões de enquadramento na Portaria MCID 75/2025 e Lei 14.133/2021.

**Aceite:** há um **parecer jurídico de anulação de licitação de trabalho social**, mas **não foi recuperado o ato decisório final**, nem há prova de anulação, cancelamento ou paralisação das obras das unidades habitacionais. Não se aplica o parecer acessório ao estado geral do empreendimento; a localização por logradouro, lote ou quadra ainda exige documentos específicos.

### Cravinhos — recapeamento, projeto `25012.35-95`, repasse `943601/2023`

O [extrato oficial de contrato de repasse, DOU de 31/08/2023](https://www.escavador.com/diarios/5784757/DOU/secao-3/2023-08-31?page=119) identifica **943601/2023**, celebrado pelo Município de Cravinhos com Ministério das Cidades e Caixa para recapeamento asfáltico urbano. O instrumento foi publicado com **valor global de R$ 243.633,12**, dos quais **R$ 238.856,00 federais** e **R$ 4.777,12 de contrapartida**.

**Aceite:** confirmação de financiamento e objeto contratual; **valores de assinatura do contrato, não pagamentos**. Trechos viários ainda sem identificação de início/fim e sem linha georreferenciada, não se admite pin genérico.

## FED19 — persistência e regressões

Código reprodutível: [`deployment/build_rmrp_fed19_private.py`](../deployment/build_rmrp_fed19_private.py), em branch `investimentos-territoriais-sp645-20261111` do repositório. Opera apenas sobre a cópia privada FED18 com marcador de segurança, acrescentando `evidencia_documental_fed19` aos cinco projetos e o respectivo inventário de fontes/ressalvas. A cópia pública do site não foi modificada.

[**Prévia privada FED19 no Google Drive**](https://drive.google.com/file/d/1nA1ASqA7D5V9f8q9O7Lloi-vG7_wsEK-/view), arquivo `RMRP_FED19_SITE_PREVIA_PRIVADA_2026-11-16.zip`, **825.887 bytes**, SHA-256 `7ffce14c23f2a6d0eddb2a2accfeca0cdf40b0b80a5aee355293061db44ad67b`. Pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`, `shared=false`; SHA-256 e CRC **verificados após download de retorno**.

Testes executados: **1.603 verificações estruturais de API**, **288 respostas HTTP 200 em servidor localhost** com **285 JSON válidos**, mais **29 testes de aplicação/regressão aprovados**. Os seis endpoints JSON preexistentes permanecem **6/6 byte a byte idênticos**. Conservados **218 JSON de projetos**, **34/34 valores municipais GND4 pago `null`**, **0 valores de capital pago preenchidos** e **0 geometrias de execução física** nas fichas.

## Prioridades remanescentes

Há **sete projetos** que ainda precisam de pesquisa documental independente nesta frente, incluindo os demais casos habitacionais, obras de esgoto/saneamento, recapeamentos em Cravinhos e implantação de calçadas em Barrinha. Listar candidatos com IDs e instrumentos somente em artefatos privados, quando necessário, e utilizar fontes oficiais com correspondência exata antes de alterar atributos da plataforma.

As condições para homologação pública permanecem: vinculação a endereço/trecho ou geometria **da execução efetiva**; validação do estágio financeiro e GND4 efetivamente pago; tratamento de estornos; conciliação dos dois desembolsos pendentes FED11; testes visuais e versão restrita do Pages.

**Decisão:** `public_release_authorized=false`, sem deploy. Dados enriquecidos são evidências documentais verificadas ou alertas de qualidade, **não comprovantes de investimento executado**.
