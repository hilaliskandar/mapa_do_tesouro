# RMSJRP — G06-F2 | Paginação, unicidade e situação dos registros de propostas federais
**Data:** 9 de novembro de 2026. **Natureza:** auditoria da API pública Transferegov; **não** é auditoria integral de pagamentos nem estimativa de efeitos da LC 200/2023.

## 1. Achado inicial e correção da fase G06-F1
A fase anterior verificou 74/74 consultas com código IBGE, mas ainda **não havia auditado a paginação**. O experimento preliminar, executado em [run 42632491178](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42632491178), confirmou, a partir da documentação OpenAPI oficial, que ambas as rotas aceitam os parâmetros inteiros opcionais **`pagina` e `tamanho_da_pagina`**.

Em duas consultas de teste, a resposta JSON do serviço trouxe metadados `total_pages`, `total_items`, `page_number` e `page_size`. Exemplo da primeira página de São José do Rio Preto na Gestão de Parcerias: **50 registros retornados, 85 itens declarados em duas páginas**. Exemplo de Adolfo na API Discricionárias e Legais: **50 registros retornados, 195 itens declarados em quatro páginas**. Assim, os **437 candidatos anteriores permanecem apenas amostrais**; não devem ser publicados como contagem integral.

As demais consultas diagnósticas demonstraram 14 propostas declaradas em uma página na Gestão de Parcerias para Adolfo, enquanto uma tentativa na API de Discricionárias para São José do Rio Preto retornou HTTP 502. O erro constitui **instabilidade técnica pontual**, não ausência de registros.

## 2. Método de enumeração reprodutível
O script `editorial/rmsjrp/enumerar_propostas_g06f2.py`, workflow `.github/workflows/rmsjrp-g06f2-enumeracao.yml`, foi desenvolvido para:
1. Recuperar novamente os OpenAPI oficiais `/parcerias/openapi.json` e `/discricionarias/openapi.json`, verificando a declaração dos filtros IBGE e da paginação;
2. Consultar as **37 localidades por módulo**, com `pagina=1` e `tamanho_da_pagina=50`, continuar até `total_pages` informado, sob limite operacional de até 60 páginas por combinação e até três tentativas por chamada em caso de falha;
3. Registrar URL, página, número de itens, totais declarados e hash SHA-256 de cada resposta, verificando coerência entre `total_items`, páginas e número de linhas de cada consulta;
4. Exigir que o código IBGE de cada item seja compatível com o município solicitado, sem correspondência por texto livre da descrição;
5. Preservar cada `id_proposta` uma única vez **por módulo e município**, sem pressupor que IDs de dois módulos representem a mesma identidade jurídica;
6. Extrair apenas campos de identificação, situação original da proposta, ano/data, órgão concedente quando informado, evento de celebração e valores **rotulados expressamente como propostos, não pagos**;
7. Marcar consulta com contagem divergente, problema de esquema, registro sem identificador ou erro como **cobertura não homologada**, sem imputar ausência de recursos.

Arquivos planejados do lote: `G06F2_COBERTURA_74_CONSULTAS.csv`, `G06F2_AUDITORIA_PAGINAS.csv`, `G06F2_PROPOSTAS_CANONICAS.csv`, `G06F2_SITUACOES_OBSERVADAS.csv` e `QA_G06F2.json`. Persistência prevista no R2 privado `rmsjrp/g06/2026_11_09/instrumentos_api_f2/` mediante readback de hash.

## 3. Hierarquia de evidências e limites
**Proposta localizada ≠ instrumento celebrado ≠ empenho federal ≠ pagamento federal ≠ receita creditada ao município ≠ liquidação da despesa municipal.** Metadados de evento de celebração serão conservados como **candidatos de vínculo documental** e não classificados automaticamente como instrumento com prova de assinatura. Sem documento de celebração e registros financeiros, os valores `vl_global_prop` e `vl_repasse_prop` permanecem montantes **propostos**.

As seguintes informações ainda são necessárias para passar do mapeamento documental à análise econômica de exposição: situação jurídica de cada instrumento, concedente, identificação federal, valor/cronograma autorizado, empenho, pagamento e data de crédito, cotejo com receita municipal e aplicação em despesa local. A LC 200/2023 não rege diretamente o teto municipal, e a existência da proposta não comprova qualquer mecanismo de corte do repasse.

## 4. Registro de execução
- [G06-F1 descoberta 76 rotas — run 42629593944](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42629593944), validado e arquivado.
- [G06-F1 consultas iniciais 74/74 — run 42630345679](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42630345679), validado e arquivado, **somente primeira página**.
- [G06-F2 auditoria de paginação — run 42632491178](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42632491178), `success`, parâmetros e metadados confirmados.
- [G06-F2 enumeração das 74 combinações — run 42632869767](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42632869767). **Consultar conclusão e QA antes de afirmar exaustividade ou totais observados.**

## 5. Próximo ponto de retomada
Após conferir o run 42632869767 e os arquivos de QA, atualizar o total efetivamente paginado e a cobertura por módulo/município; onde houver erros, refazer **apenas** as páginas necessárias e versionar novos snapshots sem sobrescrever provas anteriores. A fase seguinte deve concentrar-se em demonstrar quais propostas se converteram em instrumentos celebrados e em cruzar seus identificadores com registros de empenho e pagamento federal, recebimentos na prefeitura e investimentos liquidados. **Nenhuma dessas inferências está autorizada somente pela enumeração.**

## 6. Fechamento efetivo da enumeração — QA posteriormente concluído em 09/11/2026

A execução [GitHub Actions 42632869767](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42632869767) terminou **`success`** e produziu o manifesto `QA_G06F2.json` com **`status=pass`**. O resultado substitui a classificação preliminar do item 4 (em execução), sem apagar a sequência de evidências.

| Controle | Resultado validado |
|---|---:|
| Combinações município–módulo esperadas | **74** |
| Combinações com QA `pass` | **74** |
| Páginas consultadas e reconciliadas | **231** |
| Identificadores de propostas deduplicados dentro de cada módulo–município | **9.338** |
| Registros Gestão de Parcerias | **508** |
| Registros Discricionárias e Legais | **8.830** |
| Arquivos produzidos com readback SHA no R2 | **5** |

As 231 páginas foram obtidas com parâmetros de paginação declarados no próprio OpenAPI; cada combinação teve seus `total_pages`, `total_items`, `page_number` e códigos IBGE conferidos. A deduplicação foi feita **somente por identificador de proposta no mesmo município e módulo**. **Não houve deduplicação jurídica entre os módulos**, nem inferência de identidade de instrumentos jurídicos, pois os esquemas podem representar objetos e períodos diferentes.

**Situações de propostas no módulo Gestão de Parcerias:** `Aprovada` (480), `Em Análise` (9), `Em Elaboração` (7), `Inativada` (1) e `Rejeitada` (11), totalizando 508. No módulo Discricionárias e Legais foram observados diferentes estágios, incluindo `Proposta/Plano de Trabalho Enviado para Análise` (3.703), `Rejeitados` (1.677), `Aprovados` (1.275), `em Análise` (1.003), `Cadastrados` (607), entre outras situações específicas. **Situação de proposta aprovada NÃO demonstra contrato assinado nem pagamento.** Os registros do mesmo módulo têm situações distintas; não somar essas categorias aos repasses financeiros.

**Persistência auditada no R2 privado**, prefixo `rmsjrp/g06/2026_11_09/instrumentos_api_f2/`, com leitura de retorno e igualdade de SHA-256 para os cinco objetos:
- `G06F2_COBERTURA_74_CONSULTAS.csv`;
- `G06F2_AUDITORIA_PAGINAS.csv`;
- `G06F2_PROPOSTAS_CANONICAS.csv`;
- `G06F2_SITUACOES_OBSERVADAS.csv`;
- `QA_G06F2.json`.

**Limitação da completude:** QA `pass` significa que todas as páginas informadas pelas APIs foram recuperadas e reconciliadas **na data da captura**, não que o universo jurídico de convênios/transferências federais tenha sido integralmente capturado. Alguns registros podem ter sido alterados ou reclassificados posteriormente; a versão tem data/hora e hashes de páginas. As bases não demonstram por si valores de empenhos, pagamentos, repasses creditados ou liquidações municipais.

**Próxima etapa G06-F3:** identificar instrumentos efetivamente celebrados — preferencialmente documentos contratuais e campos específicos de instrumentos — por chave vinculada ao `id_proposta`; reconciliar execução financeira federal e crédito/execução municipal. Preservar separadamente a condição de proposta e nunca classificar `Aprovada` como `Paga`. G06 permanece `in_progress`, sem estimativa de impacto da LC 200/2023.
