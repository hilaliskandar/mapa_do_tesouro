# FED04B — aquisição nacional real, conciliação territorial preliminar e QA

**Executado em 15/11/2026.** Arquivos oficiais adquiridos por runner remoto com HTTPS funcional, após diagnóstico da indisponibilidade DNS/TCP do container local. **Não são dados sintéticos.** Snapshot informado pelo servidor: 15/11/2026. A seleção é por **propostas e projetos vinculados aos proponentes dos 34 municípios da RMRP**, não pelo local físico comprovado da intervenção.

## Fontes efetivamente baixadas e preservadas

| Fonte nacional | Linhas nacionais | Linhas retidas no recorte RMRP | Bytes ZIP | SHA-256 | Drive privado |
|---|---:|---:|---:|---|---|
| `siconv_coordenadas_obra` | 132.102 | 441 | 2.996.307 | `c974e80db5b31e5682816ee66042c501d57782caf572966a8b911c991953337c` | [ZIP](https://drive.google.com/file/d/1cgeuYdcFSFw2OLk77mJf8O_xMRV1EZdb/view) |
| `siconv_contrato_cipi` | 39.099 | 150 | 4.275.091 | `19f6312d70508c5242bf08a984d662e0041fc8caff82eda482689461e0b07745` | [ZIP](https://drive.google.com/file/d/1FMrB-mNFugVSzKHrVD8RHDQI2dckme3Z/view) |
| `siconv_dados_obrasgov_geral` | 48.086 | 218 | 785.514 | `b5d50a7aa6716df1565d1c9283200904cf234ea0c8971c3685e9f61476c77795` | [ZIP](https://drive.google.com/file/d/11XDOgtXOI1p_qLw6Ns-ZlLqN7_6HZ7wQ/view) |

Origem: `https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/<nome>.zip`. O servidor retornou HTTP 200, `Last-Modified` em 15/11/2026 e `ETag` para os três arquivos. Os arquivos CSV foram lidos integralmente e os ZIPs tiveram `testzip()=None`.

**Verificação de persistência:** todos os três ZIPs oficiais foram enviados à pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`. Leitura de metadados confirmou tamanhos, pasta e `shared=false`; download independente dos três a partir do Drive confirmou SHA-256 **idêntico** à origem e CRC integral.

## Correspondências executadas

O SQLite pré-existente `RMRP_FED04A_STAGING_2026-11-15.sqlite` foi recuperado do Drive e utilizado em **cópia de desenvolvimento**, mantendo 6.410 IDs de propostas, 1.793 convênios e 218 projetos Obrasgov.

1. Seleção de **441 linhas de coordenadas**, vinculadas a **265 propostas** pelo identificador `ID_PROPOSTA`.
2. Para os 218 projetos selecionados, confirmação explícita de `id_projeto_investimento → nr_instrumento → convenio.numero → convenio.proposta_id`. **218/218** encontraram ponte documental; nenhum vínculo foi inferido por nome.
3. Derivação de **336 associações candidatas projeto–coordenada**, vinculadas aos 218 projetos. A cardinalidade 1:N preserva mais de uma coordenada por projeto/proposta.
4. Seleção de **150 linhas de contrato CIPI** para **131 projetos distintos**; 19 linhas excedentes relativas a IDs de contrato repetidos. **Nenhum valor contratual foi somado**, em razão de repetições e possível divergência documental.

## QA geográfico

Dos 441 registros vinculados às propostas:
- **435** caem numa caixa geográfica **ampla de triagem** para São Paulo (lat. -26,5 a -19,5; long. -54 a -44);
- **4** estão fora dessa caixa e **2** são `0,0`; total de **6 sinalizações**;
- dos 336 pares projeto–coordenada derivados, **2** apontam para registros sinalizados na triagem.

**A caixa ampla não é um limite municipal oficial**, nem valida CRS ou precisão. Entre os casos fora da caixa há latitude com sinal aparentemente incompatível e coordenada de outro estado; não corrigir sinais nem geocodificar automaticamente. É necessário cruzar cada ponto com limites IBGE dos 34 municípios, registrando EPSG:4674 e possíveis pontos de obra situada fora do município proponente.

## Base derivada e persistência

O arquivo [`RMRP_FED04B_REAL_STAGING_2026-11-15.zip`](https://drive.google.com/file/d/1gqkOo1SkpyWaVZ75POrFZQ8zN1Tr6P8J/view), 931.639 bytes, SHA-256 `4cd3129e25f96cfb92b8faadb317035dfa7579c0fb5951dd276ffcfc5dcabd0d`, contém:
- `RMRP_FED04B_STAGING_2026-11-15.sqlite`, derivado de cópia isolada do FED04A com tabelas `coordenada_proposta_fed04b`, `vinculo_projeto_instrumento_fed04b`, `projeto_coordenada_candidata_fed04b` e `contrato_cipi_fed04b`;
- `RMRP_FED04B_REAL_QA_2026-11-15.json`, com totais, SHA-256 das fontes e restrições de classificação.

**QA SQLite:** `PRAGMA integrity_check=ok`, nenhuma violação `foreign_key_check`, 218/218 projetos na ponte documental. ZIP derivado com CRC íntegro; cópia do Drive retornou SHA-256 idêntico e `shared=false`.

## Bloqueios restantes

- **FED04B espacial:** não há homologação de localização física; requer interseção espacial com malha municipal oficial, análise dos seis pontos suspeitos e confirmação documental das coordenadas como local da obra, não apenas cadastro de proposta.
- **FED03C:** ainda faltam `siconv_pagamento`, `siconv_obtv_convenente`, `siconv_dl`, `siconv_itens_dl` com reconciliação pai–filho, estornos e classificação de GND4 paga. Nenhuma cifra federal foi promovida como investimento executado.
- **Publicação:** `public_release_authorized=false` e sem alterações na plataforma pública.

A coleta em runner remoto, com upload resumível via conector Drive e download de conferência, substitui a dependência do container local sem DNS. Não publicar microdados brutos nacionais em repositório aberto.
