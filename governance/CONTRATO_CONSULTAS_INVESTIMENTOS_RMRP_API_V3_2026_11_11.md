# Contrato de consulta JSON — Investimentos territoriais, piloto RMRP

**Data:** 11/11/2026. **Status:** proposta versionada, sem exportação de dados ou interface em produção. Base: SQL proposto `proposals/INV_RMRP_SCHEMA_EXTENSAO_SQLITE_2026_11_11.sql`, consultas `proposals/INV_RMRP_CONSULTAS_SQL_PILOTO_2026_11_11.sql`.

## 1. Vocabulário e status

- `valor_centavos`: inteiro monetário, preserva precisão; `null` = valor não informado. Zero somente se observação efetiva de zero.
- `etapa`: `previsto`, `aprovado`, `celebrado`, `empenhado`, `liquidado`, `pago`, `transferido`, `estornado`. Eventos de etapas distintas não podem ser somados em indicador único.
- `natureza_fluxo`: `execucao_direta`, `transferencia_intergovernamental`, `financiamento`, `contrapartida`, `outro`.
- `natureza_despesa`: `investimento`, `custeio`, `misto`, `nao_classificado`. `nao_classificado` não contribui para investimento agregado.
- `municipio_papel`: `local_execucao`, `abrangencia`, `beneficiario`, `recebedor`, `sede_executor`.
- `qa_status`: `candidato`, `em_revisao`, `homologado`, `rejeitado`.
- `origem`: literal namespace de sistema e módulo, ID de origem, URL pública, documento e artefato SHA-256 quando recuperado.

## 2. Endpoints materializados propostos

| Path | Unidade/uso | Cardinalidade máxima |
|---|---|---|
| `/data/api/v3/investimentos/rmrp/manifest.json` | fontes, schema, versão, hash e cobertura | 1 |
| `/data/api/v3/investimentos/rmrp/municipios.json` | lista de municípios e índices de sumários | 34 |
| `/data/api/v3/investimentos/rmrp/municipios/{ibge7}.json` | carteira local, valores por estágio e cobertura por fonte | 34 arquivos |
| `/data/api/v3/investimentos/rmrp/projetos/{id_url_seguro}.json` | documento de projeto, instrumentos vinculados, pins e eventos | quantidade variável |
| `/data/api/v3/investimentos/rmrp/anos/{ano}.json` | séries anuais por município, fonte, etapa e natureza, com universos compatíveis | 1 por ano |
| `/data/api/v3/investimentos/rmrp/pendencias.json` | contagens e exemplos auditáveis de lacuna, sem divulgação de dados confidenciais | 1 |

**Padrão de resposta de um município** (modelo ilustrativo sem dados inventados):

```json
{
  "codigo_ibge": "3543402",
  "universo_id": "RMRP_34",
  "ano_referencia": 2025,
  "status": "preview_not_published",
  "cobertura": {
    "obrasgov": "nao_carregado",
    "transferegov_parcerias": "nao_carregado",
    "transferencias_estaduais": "nao_carregado",
    "investimentos_municipais_tcesp": "disponivel_em_base_preexistente"
  },
  "totais_por_dimensao": {
    "municipal_investimento_liquidado_centavos": null,
    "federal_pagamentos_diretos_investimento_centavos": null,
    "estadual_pagamentos_diretos_investimento_centavos": null,
    "transferencias_federais_creditadas_centavos": null,
    "transferencias_estaduais_liberadas_centavos": null,
    "carteira_prevista_centavos": null
  },
  "projetos": [],
  "fontes": [],
  "observacoes": [
    "A estrutura representa um contrato, nao dados carregados."
  ]
}
```

O código `3543402` é **apenas exemplo de formato IBGE7** e não deve ser usado como filtro fixo, nem considerado município demonstrado no piloto sem validação. O exportador real deverá buscar `municipio` e impedir saída com base em exemplo de documentação.

## 3. Critérios de publicação dos valores

- **Carteira prevista:** somente projeto com `qa_status=homologado`, com etapa prevista, valor na origem e regra de não duplicação por projeto.
- **Pagamentos federais diretos:** evento `pago`, `execucao_direta`, `investimento`, local de execução confirmado; sem transferência intergovernamental.
- **Liberações federais e estaduais ao município:** somente evento `transferido` com beneficiário juridicamente identificado, estornos compensados e município recebedor; não somar aos pagamentos de execução direta.
- **Investimento municipal liquidado:** consulta existente `tcesp_investimento_programa` para o estágio e período homologados, sem reconverter repasses federais em despesas independentes.
- **Valor contratado / aprovado:** categoria própria de carteira e compromissos, não gasto executado.
- **Projeto plurimunicipal:** valor indivisível não será repetido integralmente por município; sem rateio comprovado, registrar `nao_alocado` e permitir consultar o projeto na região.

## 4. Filtros da experiência

- Município (34 códigos IBGE oficiais) e sub-região;
- período (ano, eventualmente mês para eventos reais);
- esfera financiadora, esfera executora e origem do recurso;
- eixo/tema, setor e tipo de intervenção;
- instrumento jurídico, situação cadastral, execução física;
- etapa financeira e valor;
- identificação da localização (ponto, polígono, município sem ponto);
- confiabilidade documental e atualização.

**Desempenho:** lista regional de no máximo 34 municípios; detalhe local carregado sob demanda, índice de projetos com paginação cliente quando necessário. GeoJSON de polígonos em camada pública própria, não duplicado em cada ficha; coordenadas originais preservadas, geometria simplificada não deve substituir o arquivo territorial canônico.

## 5. Testes obrigatórios antes de qualquer prévia

1. **34/34 IBGE7 únicos** e quatro sub-regiões, cruzamento com cadastro SQLite; fonte oficial IBGE 645.
2. **50 consultas**: 34 municípios, quatro sub-regiões, filtros de ano, fonte, estágio, projeto com duas fontes, projeto plurimunicipal, ausente, estorno e cidade com zero projetos documentados.
3. Pagamentos federais não são somados com transferências ao município; soma dos valores `previsto`, `contratado` e `pago` não aparece como total único.
4. Regressão do TCESP 2023–2025 e da interface de investimentos existente; ressalva de Guatapará/2023 não desaparece.
5. A página não deve mostrar dados `candidato`, `em_revisao` ou `rejeitado` como homologados.
6. Manifesto contém origem, hash, data, cobertura e versões; links de origem e prova documental funcionam.
7. Controle de formato JSON, integridade de IDs, ausência de vazamento de credenciais/URLs privadas e cache correto; invalidar versão após retificação.
8. Sem D1 até se comprovar necessidade operacional; avaliar tamanho, latência e experiência real na prévia static-first.

**Estado:** este contrato ainda não fornece consultas operacionais nem resultados inventariados; a camada é tecnicamente implementável a partir da extração, migração de desenvolvimento e exportação homologadas.
