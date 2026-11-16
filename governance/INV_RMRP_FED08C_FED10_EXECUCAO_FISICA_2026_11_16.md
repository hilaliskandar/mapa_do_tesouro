# FED08C e FED10 — evidência documental de execução física e integração privada

**Execução:** 16/11/2026. **Fonte:** cinco novos ZIPs oficiais da área de CSV do Transferegov, snapshot de 15/11/2026, mais SQLite territorial FED04D. **Escopo:** 19 projetos Obrasgov cujas 20 coordenadas cadastrais associadas divergem do município proponente. **Sem autorização de publicação.**

## Aquisição de bases de execução física

| Arquivo oficial | SHA-256 original | Drive privado |
|---|---|---|
| `siconv_execucao_fisica_cipi.zip` | `e89f063adeb40c945f0479b0c91c9ce097fe0ea9af198956a59fbd03a34a5495` | [ZIP](https://drive.google.com/file/d/1zagchT-2LG30-qC2j4qKXq4cliZMzgr7/view) |
| `siconv_acomp_obras_contratos_medicoes_modulo_empresas.zip` | `c3618b56f6175c4804cee11bd84b9fc44f78e2fd76ed792be8acbd77cf7198f1` | [ZIP](https://drive.google.com/file/d/1RBfbtdJltIH_McUSr_i3kkCZgr4UOVVB/view) |
| `siconv_acomp_obras_valores_itens_medicao_modulo_empresas.zip` | `d3eb4841cdc7bceda87e8833d59fadb36d649439689e68e257fd6abb28fd0f80` | [ZIP](https://drive.google.com/file/d/1Ntkk5mIKz7if_JHVPXBL4Ut2Pdo-6oOR/view) |
| `siconv_resumo_fisico_financeiro.zip` | `5053843fa26e322158df1760d395e183fbe4c933742715d3ee52c5ff06233ff0` | [ZIP](https://drive.google.com/file/d/1pM-N1AblfAKZjLmZHOq3ID8seWU6pdG4/view) |
| `siconv_projeto_basico_acffo_modulo_empresas.zip` | `64668b50c5ea4b034d3370effc14fe5c30ba5182d715614806f51ec3491024a9` | [ZIP](https://drive.google.com/file/d/1vi-Jk_2YZJ1aPi1K3Ilim5Sv4t3i5WPc/view) |

Os cinco arquivos nacionais foram obtidos por HTTPS e submetidos a CRC integral e SHA-256 na origem. Seus metadados no Drive indicaram a pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`, `shared=false`; o retorno de conteúdo confirmou **SHA-256 idêntico e CRC íntegro nos cinco**. O arquivo de valores dos itens de medição foi lido para documentação do esquema, mas **não** incorporado a projetos via `ID_PROPOSTA`, pois não possui essa chave diretamente; requer ponte por contrato/submeta validada antes de ratear ou agregar.

## Resultados de FED08C para os 19 projetos com coordenadas divergentes

O script reproduzível [`pipeline/qa/audit_rmrp_fed08c_physical_evidence.py`](../pipeline/qa/audit_rmrp_fed08c_physical_evidence.py) cruzou pelo ID de projeto CIPI ou ID de proposta:

| Evidência encontrada entre os 19 projetos | Projetos distintos |
|---|---:|
| Registros de execução física CIPI | **15** |
| Registros de medição | **12** |
| Pelo menos uma medição com situação `Aceita` | **7** |
| Resumo físico-financeiro cadastrado | **14** |
| Projeto básico ACFFO/SPAs cadastrados | **18** |
| Pelo menos um registro SPA com situação `Homologada` | **18** |
| Localização física efetivamente comprovada | **0** |

A estrutura original contempla 31.462 registros nacionais de execução física CIPI, 28.667 de medições, 33.140 de resumo físico-financeiro e 65.367 registros de projeto básico, além de 26.429 linhas nacionais de valores por itens de medição que requerem ponte contratual adicional. **A existência de medição, resumo e situação cadastral não prova a localização material da obra, nem sua elegibilidade como investimento de capital pago.**

A relação privada dos 19 projetos traz suas chaves, estados e indicadores de cobertura, sem divulgá-los em repositório aberto. [ZIP privado FED08C](https://drive.google.com/file/d/1yZEUy-gV2z2auUtmqDQbWjU4agU5nP7R/view), **1.942 bytes**, SHA-256 `f277a56c70587af0d0981fd6c069b830769f2559fa31c95271bf5dbf8a388c08`; readback SHA-256/CRC aprovado.

## FED10 — incorporação à prévia privada

O materializador [`deployment/build_rmrp_fed10_private.py`](../deployment/build_rmrp_fed10_private.py) incorporou, em **19 fichas de projetos** da API v3, campos separados de:

- registros de execução física CIPI;
- número de medições e medições aceitas;
- existência de resumo físico-financeiro;
- número de registros de projeto básico;
- avisos expressos de que `localizacao_fisica_efetiva_homologada=false` e `financeiro_gnd4_pago_homologado=false`.

Mantiveram-se 34 municípios, quatro sub-regiões, 19 anos, 218 projetos, a distribuição FED09 por natureza do empenho e os seis JSON legados. O arquivo `manifest.json` passou a registrar 19 projetos examinados e **zero coordenadas de execução homologadas**. Todos os valores de GND4 pago permanecem `null`.

**Regressão privada FED10:** 1.603 verificações da API aprovadas, **288 respostas HTTP 200** com 285 JSON válidos no servidor `localhost`; CRC da saída aprovado. O pacote integrado está em [**RMRP_FED10_SITE_PREVIA_PRIVADA_2026-11-16.zip**](https://drive.google.com/file/d/1OZ0Qpn6nch8R2WEQuBlsgoc1ZHu5m7HF/view), tamanho **804.144 bytes**, SHA-256 `53ebb90b0e29a8f72076fc1ac70cc1640aab484ad292893ed745cc73132f3a77`, readback SHA-256 e CRC confirmados, acesso privado.

## Condições para alteração de status e publicação

1. **Execução física:** obter documentos individualizados com endereço/local/trecho/medição georreferenciada para os 19 projetos. O campo cadastral de coordenadas não serve, isoladamente, como atestado de obra.
2. **Financeiro:** apurar a natureza do pagamento final, estornos/devoluções e eventuais registros de anulação. Os R$ 450,50 milhões associados ao prefixo `44` nos desembolsos não são GND4 pago.
3. **Desembolsos:** resolver 1 sem ponte de empenho e 1 com diferença de R$ 88 mil; não ratear automaticamente.
4. **Cronologia:** examinar definições e histórico dos 808 pagamentos anteriores à emissão atual do DL, sem atribuir irregularidade automática.
5. **Plataforma:** executar implantação **restrita** para QA visual e regressão de dados TCESP; Cloudflare Pages público não foi alterado.

**Decisão de QA:** `public_release_authorized=false`, `pontos_execucao_fisica_homologados=0`. A prévia FED10 está apta a testes privados; nenhuma publicação pública foi realizada.
