# Caderno fiscal de referência — modelo piloto

**Situação:** minuta estrutural, sem números. **Não publicar** antes da validação do índice e dos contextos de produção.

## Identificação
- Universo editorial: Região Metropolitana de Jundiaí (proposta, `publication_id` pendente de validação).
- Fonte obrigatória: `/data/api/v1/publication/universes/{publication_id}/context.json`.
- Fichas: `/data/api/v1/publication/universes/{publication_id}/municipalities/{codigo_ibge}.json`.
- Regra: não se acrescentam municípios nem se excluem integrantes sem respaldo no payload.

## 1. Caracterização do universo
Descrever membros, exclusões editoriais, recortes territoriais e cobertura dos exercícios; citar o identificador do universo.

## 2. Panorama fiscal comparativo
Apresentar mediana, quartis, dispersão, extremos observados e número de municípios com observação. É proibido denominar soma parcial de 'total da região' sem cobertura explicitada.

## 3. Receitas e autonomia
Tratar separadamente receita corrente, tributária, IPTU, ITBI, ISS e transferências, conforme campos efetivamente disponíveis. Diferenciar evolução nominal, valores relativos e autonomia financeira.

## 4. Despesas e investimento
Diferenciar despesas correntes, capital, investimentos e indicadores relativos ao denominador apropriado. Verificar estágios e possibilidade de comparação.

## 5. Dimensão territorial
Discriminar Urbanismo, Habitação, Saneamento, Gestão Ambiental e Transporte. O agregado territorial `strict_complete` somente existe com os cinco componentes observados.

## 6. Endividamento, pessoal, caixa e CAPAG
Preservar a natureza oficial de DTP/RCL, DC/RCL e DCL/RCL. Distinguir posição do snapshot CAPAG e ano-base; não inferir avaliação normativa a partir da classificação.

## 7. Heterogeneidade intragrupo
Examinar concentração, quartis, extremos, padrões de distribuição e efeitos da cobertura. Evitar interpretação causal sem evidência adicional.

## 8. Fichas municipais
Uma ficha para cada integrante efetivamente indexado: síntese, receitas, despesa/investimento, território, dívida/liquidez/CAPAG, trajetória, posição no grupo, fontes e lacunas. Os percentis devem corresponder ao universo editorial selecionado.

## 9. Metodologia, fontes e cobertura
Registrar versão de dados, data do build, períodos, origem oficial, cobertura variável-ano, estado de observabilidade, restrições de série histórica e eventuais mudanças de regime contábil.

## Requisitos para preencher o modelo
1. JSON de índice, contexto e fichas obtidos e validados.
2. Tabela de verificações quantitativas: `variavel_id`, ano, campo do JSON, valor, cobertura, afirmação, status de revisão.
3. Revisão editorial e metodológica independente do processamento.
4. Manifesto + SHA-256, com status explícito `candidate`.
5. Aprovação expressa antes de publicação externa.

## Registro da tentativa de validação — 2026-10-14
O endpoint público `https://finbra-tic-tim-referencia.pages.dev/data/api/v1/publication/universes.json` não foi recuperado: o acesso pelo mecanismo web falhou, o Crawl2AI retornou erro interno e uma tentativa de consulta HTTP no ambiente local apresentou falha de resolução DNS. Essas ocorrências não comprovam indisponibilidade do serviço para usuários externos. **Gate E1.1 permanece não aprovado.**
