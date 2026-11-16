# FED12 e FED13 — reconstrução comprovada da cadeia LAE, QCI, meta e submeta

**Data de execução:** 16/11/2026. **Snapshot oficial:** 15/11/2026. **Escopo:** 19 projetos Obrasgov ligados a propostas da RMRP cujas coordenadas cadastrais divergem do município proponente. **Conclusão:** nova cadeia documental verificada para 18 projetos, sem homologação de localização física nem de GND4 pago.

## 1. Risco de junção incorreta identificado e corrigido

No diagnóstico da etapa FED11 foram recuperadas metas de projeto básico que continham `ID_QCI_ACFFO`, mas não se dispunha ainda da tabela intermediária `siconv_projeto_basico_lae_modulo_empresas`.

Uma tentativa exploratória de equivalência numérica `ID_ACFFO = ID_QCI_ACFFO` produziu descrições de obras em estados diferentes de São Paulo (entre eles Minas Gerais, Sergipe e Amazonas). **Esta igualdade numérica não é um vínculo válido.** ACFFO e QCI são identificadores de entidades distintas. O resultado falso não foi incorporado em tabelas de localização, propostas nem API.

O catálogo oficial do Transferegov revelou o arquivo [`siconv_projeto_basico_lae_modulo_empresas.zip`](https://drive.google.com/file/d/14B3jSybRdQdm-ACOZpzH33bkxyVUaldQ/view), cujas colunas incluem **simultaneamente** `ID_PROPOSTA`, `ID_ACFFO` e `ID_QCI_ACFFO`. Isso tornou possível a cadeia **explicitamente documentada**:

`obra_proponente.projeto_id → vinculo_projeto_instrumento_fed04b.id_proposta → siconv_projeto_basico_lae.ID_PROPOSTA → ID_QCI_ACFFO → siconv_projeto_basico_metas.ID_QCI_ACFFO → ID_META_PROJETO_BASICO → siconv_projeto_basico_submetas.ID_META_PROJETO_BASICO`.

Foi realizada checagem cruzada adicional com `siconv_projeto_basico_acffo_modulo_empresas` pelo par `(ID_ACFFO, ID_PROPOSTA)`: **18/18 registros ACFFO correspondem à ponte LAE**.

## 2. Novas fontes oficiais preservadas

| Arquivo | ZIP bytes | SHA-256 | Link privado |
|---|---:|---|---|
| `siconv_projeto_basico_lae_modulo_empresas.zip` | 3.354.882 | `f506204d11b5e555959384886ddcd56e2b3bba700b3459ab0761c8d305bf667b` | [LAE/QCI](https://drive.google.com/file/d/14B3jSybRdQdm-ACOZpzH33bkxyVUaldQ/view) |
| `siconv_projeto_basico_proposta_modulo_empresas.zip` | 1.081.804 | `bc5bdaf8ad52581299d26f9fa6af7061529854297c39dd0e7cba484c536b52f8` | [Propostas](https://drive.google.com/file/d/1EkRp3eZ3IQOuDxygKnpptU2WhMsSRBAj/view) |
| `siconv_historico_projeto_basico.zip` | 4.970.925 | `403f80bb8413238f9bda8aa23ea94ba8709413ef8c6bdaa83fe72f1dff8e49b9` | [Histórico](https://drive.google.com/file/d/1idKfYl1AN_kFywSV6XP9mBnQjA-Y4Swo/view) |

Os três arquivos foram baixados diretamente do repositório federal, verificados pelo CRC completo, enviados à pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9` e recuperados para conferência de conteúdo. **Todos tiveram SHA-256 e CRC idênticos aos originais**, com metadados `shared=false`. Os arquivos complementares de metas e submetas já estavam preservados desde o FED11.

## 3. Resultados consolidados sobre documentos oficiais

O programa reproduzível [`pipeline/qa/audit_rmrp_fed12_qci_bridge.py`](../pipeline/qa/audit_rmrp_fed12_qci_bridge.py) percorreu integralmente seis fontes oficiais, selecionando os registros relacionados aos 19 projetos prioritários.

| Fonte | Registros nacionais examinados | Registros vinculados ao recorte |
|---|---:|---:|
| Laudos LAE/QCI | 227.025 | **61** |
| Cadastro ACFFO | 65.367 | **18** |
| Cadastro de projeto básico por proposta | 104.681 | **18** |
| Metas do projeto básico | 283.698 | **74** |
| Submetas do projeto básico | 431.579 | **74** |
| Histórico do projeto básico | 1.095.865 | **306** |

São **19 propostas e 19 projetos** sob auditoria. O cruzamento verificou **61 QCI únicos**, com metas associadas, abrangendo **18 propostas** e **18 projetos**. Uma proposta não apresentou LAE correspondente no snapshot. As **74 submetas** são vinculadas a **74 metas** e indicam `SP` em `SIGLA_LOCALIDADE_OBRA_PROJETO_BASICO`.

Os 61 registros LAE distribuem-se entre `Viável / Sim` (34), `Viável / Não` (6) e `Inexistente / Não` (21), conforme campos de situação e emissão LAE. Esses são registros do módulo, e **não se interpretou a situação Inexistente como prova de inexistência física da obra**.

As 74 submetas têm situações codificadas `COM` (38), `HAS` (22), `ANL` (12) e `HOM` (2). As siglas foram mantidas como constam na fonte; não se extrapolaram significados jurídicos ou financeiros sem o dicionário oficial.

Os 306 eventos históricos abrangem estados de tramitação de projetos básicos em diferentes momentos. O status atual não pode ser retrospectivamente atribuído a todos os eventos.

### Validade territorial

O campo `SIGLA_LOCALIDADE_OBRA_PROJETO_BASICO=SP` identifica apenas a **unidade federativa**. Entre as 74 descrições de submeta, **uma** contém expressão semelhante a endereço/localidade específica, mencionando uma praça. Esse texto não fornece coordenada, delimitação da intervenção ou confirmação de execução. Não foi gerada geocodificação automática nem atribuído um ponto à obra. O resultado **não altera os 0 pontos de execução física homologados**.

## 4. Persistência privada e integridade

[**FED12 — banco SQLite com ligações, CSV de submetas e QA agregado**](https://drive.google.com/file/d/1Kgm1U0Trm0mPPo17F2aFC9O8hwbKuBP-/view), **5.744.635 bytes**, SHA-256 `e2fb0e6ca9b2386e918c609aadc01cc6a67593e07bbfd8877b7192c1bc623660`. O SQLite adicionou tabelas explícitas para projetos prioritários, LAE, ACFFO, metas, submetas, proposta básica e histórico. `PRAGMA integrity_check=ok`, **0 violações de chave estrangeira**. ZIP, upload e readback SHA-256/CRC aprovados.

## 5. Integração privada FED13

O [materializador `deployment/build_rmrp_fed13_private.py`](../deployment/build_rmrp_fed13_private.py) adicionou aos **19 JSON de projetos** a disponibilidade documental real: contagem de QCI/LAE, metas, submetas, históricos e ACFFO SPA, com referência explícita à cadeia utilizada. Os 18 projetos com ponte e um sem ponte permanecem distinguíveis.

- Não alterou as contagens nem os valores monetários FED09 por natureza de empenho.
- Os 218 projetos continuam sem coordenada física comprovada; nenhum valor `GND4 pago` foi promovido.
- Manteve os seis JSON legados do diretório da API v3, 34 municípios, quatro sub-regiões e 19 arquivos anuais.
- O manifesto registra **18 projetos com QCI**, **74 metas**, **74 submetas** e **0 locais físicos homologados**.
- O pacote passou em **1.603 verificações da API** e **288 requisições HTTP locais**, incluindo 285 JSON válidos, sem erro.

[**FED13 — prévia privada integrada**](https://drive.google.com/file/d/1GZPfd5gXAnI5-6pGuGxRcFpJyb--H46-/view), **809.181 bytes**, SHA-256 `37a4935c47713ca86817e19573a87cde0d8ccd486c62105f0ea85e9b5b6fd8cb`; CRC e readback SHA-256 confirmados. Armazenada em pasta privada, `shared=false`.

## 6. Condições restantes para homologação

1. Recuperar **documento de execução com endereço, trecho ou localização georreferenciada** para cada projeto, priorizando os 19 com divergência cadastral. Submetas e SPA não substituem essa comprovação.
2. Examinar individualmente a proposta sem LAE, sem presumir que não possui obra.
3. Reconstituir documentos oficiais para os **dois desembolsos** do FED11, sem acrescentar empenho apenas por coincidência monetária; classificar a natureza do pagamento final, não apenas do empenho.
4. Auditar estornos e a cronologia dos 808 pagamentos anteriores à emissão do DL para distinguir recodificações históricas de inconsistências de dados.
5. Testar build privado real do Cloudflare Pages e regressão visual/TCESP antes de qualquer release.

**Gate:** `public_release_authorized=false`. Não houve alteração no ambiente público, nem homologação indevida de localização ou investimento efetivamente pago.
