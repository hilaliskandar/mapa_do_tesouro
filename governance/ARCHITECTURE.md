# Arquitetura canônica

## Objetivo

Definir a arquitetura vigente do projeto Finanças Municipais SP e impedir regressão para a organização histórica em que aplicação, dados e metodologia ficavam acoplados.

## Camadas

### 1. Fontes

Fontes oficiais ou snapshots explicitamente aprovados. Nenhuma fonte se torna canônica apenas por existir no Drive, R2 ou repositório.

### 2. Aquisição

A camada `pipeline/acquire` preserva respostas brutas, controla retries, registra falhas e produz manifestos e hashes. Para DCA estadual, a rota preferencial é a aquisição direta do Siconfi.

### 3. Normalização e harmonização

Dados de origens distintas são convertidos para contratos estáveis. Mudanças de códigos, rubricas, estágios e campos de origem permanecem registradas no crosswalk.

### 4. Núcleo canônico

O SQLite armazena municípios, universos, variáveis, observações, cobertura, documentação, proveniência, estatísticas de janela, classificações e pares.

O modelo é longo: município + ano + variável formam a chave lógica de observações anuais.

### 5. Proveniência

Cada observação deve permitir rastrear artefato, campo, regra ou observações antecedentes. Valores ausentes também possuem linhagem quando derivam de regra de completude.

### 6. Camada analítica

Agregações, indicadores, estatísticas, tipologias e pares são calculados após a ingestão. Não devem ser importados como verdade primária quando podem ser reproduzidos.

### 7. QA

A promoção exige integridade estrutural, cobertura, regras de ausência, paridade, documentação, hashes e regressão funcional.

### 8. Static-first

As consultas previsíveis são materializadas em JSON por ano, município, catálogo, metodologia e cartografia. O frontend básico não depende de API em runtime.

### 9. Publicação

Cloudflare Pages publica o site estático. R2 mantém snapshots privados ou artefatos grandes quando necessário. D1/API só devem ser introduzidos para consultas realmente dinâmicas.

## Universos

Universos são filtros analíticos, não esquemas diferentes.

- `TIC_TIM_30`: baseline publicado;
- `SP_645`: expansão estadual;
- futuros universos metropolitanos ou por porte devem coexistir sem sobrescrever classificações de outro universo.

## Versionamento

Devem permanecer distintos:

- `app_version`;
- `schema_version`;
- `data_version`;
- `methodology_version`;
- hash da base;
- hash dos artefatos publicados.

## Regras de não regressão

1. funcionalidades canônicas têm requisito formal;
2. ausência não pode virar zero;
3. indicador legal não pode ser substituído por proxy;
4. mudança de fonte/código não pode ser ocultada;
5. snapshots privados exigem manifesto versionado e SHA-256;
6. `TIC_TIM_30` permanece baseline de regressão durante a expansão;
7. nenhuma release estadual é promovida apenas porque o pipeline escala para 645 municípios.

## Relação com o legado

O código histórico de Streamlit e as rotinas antigas de normalização, hierarquia e mapa semântico permanecem como referência e regressão. A produção atual é SQLite + static-first + Cloudflare.
