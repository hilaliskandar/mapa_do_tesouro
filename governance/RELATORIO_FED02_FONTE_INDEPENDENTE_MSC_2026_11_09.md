# FED02 — Caminho documental de conciliação FPM, ITR, Fundeb e MSC mensal

**Data de referência:** 09/11/2026. **Natureza:** levantamento de fontes primárias, teste de disponibilidade e organização dos próximos controles. **Sem homologação de valores nem alteração das séries fiscais.**

## 1. Resultado jurídico-institucional e cadeia do dado

O Tesouro Nacional descreve as retenções destinadas ao Fundeb — 20% de determinados tributos e transferências — e remete ao agente FNDE quanto à distribuição do Fundo. A página oficial [Transferências Constitucionais e Legais](https://www.gov.br/tesouronacional/pt-br/estados-e-municipios/transferencias-a-estados-e-municipios/transferencias-constitucionais-e-legais) distingue os fluxos FPM, ITR, base de cálculo, depósito bancário e distribuição Fundeb.

A Portaria Conjunta FNDE/STN nº 3/2022, [registro MEC Normas](https://mecnormas.mec.gov.br/pesquisa/detalhar/1273), dispõe sobre publicação permanente pelo Banco do Brasil de demonstrativos dos **valores disponibilizados ao Fundeb e distribuídos a cada ente**, detalhados por origem e data, em formato aberto. Isso indica o tipo de evidência documental a confrontar, mas não substitui a leitura do demonstrativo efetivo de setembro de 2026.

Fontes localizadas e **estado efetivamente examinado**:

1. [Depósito Bancário — Demonstrativo de Distribuição da Arrecadação, Banco do Brasil](https://demonstrativos.apps.bb.com.br/arrecadacao-federal), indicado diretamente pela STN. A leitura via Crawl2AI retornou tela dinâmica «Carregando...» e aviso de navegador; **sem dados de depósito extraídos**. A URL não é uma API comprovada.
2. [Gestão Fundeb — Banco do Brasil](https://www.bb.com.br/site/setor-publico/federal/gestao-fundeb/): a página identifica «Demonstrativo FUNDEB», mas o Markdown obtido não contém URL de arquivo ou tabela de dados; **sem arquivo do demonstrativo baixado**.
3. [Base de cálculo, comunicados decendiais e boletins FPM/FPE](https://www.gov.br/tesouronacional/pt-br/estados-e-municipios/transferencias-a-estados-e-municipios/transferencias-constitucionais-e-legais): páginas oficiais oferecem fontes para vincular decêndio e base de distribuição, mas ainda **não foram comparadas numericamente** às 1.935 observações.
4. [Transferências Obrigatórias da União — por Município](https://www.tesourotransparente.gov.br/ckan/dataset/transferencias-obrigatorias-da-uniao-por-municipio): catálogo CKAN retornou identificadores estáveis e tamanhos de arquivos separados para FPM, ITR e Fundeb, permitindo teste independente da série «Transferências Constitucionais para Municípios» usada no FED00. Inventário detalhado em [STN_FONTES_CONCILIACAO_FPM_ITR_2026_11_09.csv](STN_FONTES_CONCILIACAO_FPM_ITR_2026_11_09.csv). **Os layouts/conteúdos do conjunto secundário ainda não estavam homologados no início desta etapa.**
5. [SICONFI API](https://apidatalake.tesouro.gov.br/docs/siconfi/): endpoints `msc_orcamentaria`, `msc_patrimonial`, `msc_controle`, `rreo` e `extrato_entregas`, com limite público documentado de **uma requisição por segundo**.

## 2. SICONFI: setembro de 2026 e compatibilidade temporal

Em consulta direta à API `/extrato_entregas?id_ente=3543402&an_referencia=2026`, a Prefeitura Municipal de **Ribeirão Preto** consta como declarante da **MSC Agregada de setembro/2026**, identificada por `periodo=9`, `periodicidade=M`, `forma_envio=CSV`, `data_status=2026-10-26T13:32:52Z`. A Câmara apresentou outra MSC no mesmo mês, que deve ser excluída da comparação destinada ao Poder Executivo municipal.

Foram testadas, sem extrair dados, consultas `/msc_orcamentaria` com `id_ente=3543402`, `an_referencia=2026`, `me_referencia=9`, `co_tipo_matriz=MSCC` e classe 6, com e sem `id_tv`; também tentativa com `co_tipo_matriz=MSCE` e uma consulta sem filtros adicionais. As respostas tiveram `count=0`. Isso **não permite afirmar ausência da MSC**: o `extrato_entregas` comprova o envio; o endpoint ou a parametrização da consulta devem ser inspecionados a partir do Swagger oficial, inclusive `co_tipo_matriz`, `classe_conta` e `id_tv`, sem preencher valores inexistentes.

**Janela de entrega:** o calendário oficial [SICONFI](https://www.siconfi.tesouro.gov.br/) registra **30/11/2026** como prazo final do RREO do **5º bimestre**. Os extratos examinados anteriormente para Ribeirão Preto, São José do Rio Preto e Olímpia tinham RREO somente até o 4º bimestre. Logo a ausência de 5º bimestre em **09/11/2026** **não demonstra atraso** e não autoriza comparação com o arquivo STN mensal de setembro.

## 3. Fontes secundárias nacionais, somente metadados verificados

Catálogo `https://www.tesourotransparente.gov.br/ckan/api/3/action/package_show?id=transferencias-obrigatorias-da-uniao-por-municipio`, retorno `success=true` em 09/11/2026:

- **FPM**, `resource_id=d69ff32a-6681-4114-81f0-233bb6b17f58`, CSV, **30.493.612 bytes** informados pelo catálogo.
- **ITR**, `resource_id=f6ad4e51-fc7e-40bb-b35a-3686da7fde2d`, CSV, **20.858.658 bytes** informados.
- **Fundeb**, `resource_id=18d5b0ae-8037-461e-8685-3f0d7752a287`, CSV, **20.853.000 bytes** informados.

O teste read-only de FPM e ITR foi programado em [`pipeline/acquire/probe_stn_obrigatorias_fpm_itr.py`](../pipeline/acquire/probe_stn_obrigatorias_fpm_itr.py) e [workflow `fed02-independent-stn-fpm-itr.yml`](../.github/workflows/fed02-independent-stn-fpm-itr.yml), execução [42683157606](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/42683157606). O estado final, SHA de resposta e efetivo cabeçalho **devem ser confirmados no artefato de QA antes de declarar download concluído**. O script limita cada download a 35 MB, registra `resource_id`, cabeçalho, codificação, quantidade de linhas e SHA, sem salvar registros no R2 nem realizar somatórios.

## 4. Estado metodológico e encaminhamento

A conferência direta no R2 do arquivo de setembro/2026 encontrou **1.895/1.896** combinações FPM+ITR/DEDU dentro de R$0,05, exceto Guarulhos (3518800), 3º decêndio, −R$0,0525, e registrou 13 municípios sem linha ITR. Trata-se de **regularidade empírica**, não prova suficiente da equivalência contábil, de valor líquido ou receita orçamentária. Consultar o [relatório FED02 de hipóteses](RELATORIO_FED02_FPM_FUNDEB_CONCILIACAO_2026_11_09.md) e [JSON de exceção](FED02_STN_2026_09_EXCECAO_GUARULHOS.json).

**Próximos gates exatos:**

1. Conferir o QA do workflow de fontes nacionais independentes FPM e ITR e validar se o arquivo cobre setembro de 2026 e apresenta chave territorial verificável.
2. Resolver o acesso ao **Demonstrativo de Distribuição da Arrecadação** do BB e às bases de cálculo decendiais STN, conferindo bruto, Fundeb retido e líquido em amostras municipais.
3. Identificar, com documentação oficial do endpoint, o filtro correto para MSC orçamentária da Prefeitura no mês 09/2026; evitar chamar `count=0` de «não entregue».
4. Consultar o RREO do 5º bimestre **após existir entrega homologada**, sem agendar consulta recorrente sem determinação explícita.
5. Manter a migration em `governance/proposals`; **nenhuma mudança de SQLite, R2 já homologado, variáveis anuais ou frontend**.

**Distinção de evidência:** o catálogo de FPM/ITR, o extrato de entregas e a página de referência STN foram efetivamente consultados; os depósitos BB e o arquivo completo da fonte secundária ainda **não** foram examinados neste relatório inicial.
