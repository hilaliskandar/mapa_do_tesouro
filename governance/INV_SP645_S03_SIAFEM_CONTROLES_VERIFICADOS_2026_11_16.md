# S03 — Inspeção de controles oficiais Sefaz-SP/SIAFEM via Crawl2AI

**Data:** 16/11/2026. **Estado:** contrato de interface obtido em HTML real; extração dos dados ainda não executada.

Fonte: https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx

A ferramenta `crawl` do Crawl2AI recuperou o HTML integral da consulta, com aproximadamente 82 mil caracteres. Página informa **dados atualizados até 16/11/2026**, convênios do SIAFEM com alguma liberação financeira desde agosto de 2007 e valores negativos para estornos/cancelamentos.

**Contrato técnico observado:** `<form name="form1" method="post" action="PesquisaComposta.aspx">`, estado ASP.NET `__VIEWSTATE`, `__EVENTVALIDATION`, `__EVENTTARGET`, `__EVENTARGUMENT`, `__LASTFOCUS`, `__VIEWSTATEGENERATOR`. A troca de `RegiaoAdministrativa`, `Municipio`, `Item` e `Tipo` pode gerar `__doPostBack`. Não usar valores de estado extraídos desta sessão em requisições futuras.

## Campos operacionais reais

| Grupo | Campos HTML identificados |
|---|---|
| Território e concedente | `RegiaoAdministrativa`, `Municipio`, `Orgao` |
| Datas | `ConvenioInicio`, `ConvenioFim`, `LiberacaoInicio`, `LiberacaoFim` |
| Valor do convênio | `ConvenioMinimo`, `ConvenioMaximo` |
| Valor de liberação | `LiberacaoMinimo`, `LiberacaoMaximo` |
| Total liberado no convênio | `LiberacaoConvenioMinimo`, `LiberacaoConvenioMaximo` |
| Saldo | `ValorSaldoMinimo`, `ValorSaldoMaximo` |
| Beneficiário | rádio `Beneficiado`: vazio, `Entidades`, `Prefeituras` |
| Natureza | rádio `Tipo`: vazio, `Custeio`, `Investimento` |
| Totais | rádio `Totais`: `Não` ou `Sim` |
| Classificação auxiliar | `Item`, sujeito a postback |

**Atenção metodológica:** opção `Tipo=Investimento` da consulta estadual é classificação declarada no próprio sistema e **não** comprovação de pagamento final GND4 pelo município, devendo ser exposta com nomenclatura de origem.

## Estratégia de coleta reproduzível ainda pendente de teste

1. Criar sessão HTTP e GET da página para obter cookies e estado ASP.NET atualizado.
2. Construir payload POST incluindo todos os campos reais e estado obtido na **mesma sessão**, selecionando inicialmente `Beneficiado=Prefeituras`, intervalo anual de `LiberacaoInicio` a `LiberacaoFim`, sem filtrar natureza; somente depois, opcionalmente, segmentar por `Tipo`.
3. Caso seleção de município dependa de postback, enviar evento de `RegiaoAdministrativa`/município, atualizar viewstate e eventvalidation a cada resposta. Registrar identificadores do botão de consulta após leitura adicional da interface.
4. Validar resposta tabular com números de convênio, CNPJ, datas, parcelas e estornos. Comparar totais anuais com consultas agregadas oficiais.
5. Registrar manifestos e scripts após execução remota e teste de QA. Não atribuir falha de DNS no ambiente do agente ao portal oficial.

**Dependência:** o ambiente local desta conversa não conseguiu resolver DNS de `www.transparencia.sp.gov.br` em tentativa HTTPS para o ZIP, apesar de o Crawl2AI remoto recuperar a página e apontar início de download. Sem arquivos, não há linhas a contabilizar em `snapshots.csv`.

**Próximo gate:** inspeção de campos de ação e resultado de consulta efetiva em sessão remota, seguida de extração de parcelas de um exercício e generalização por município e período.
