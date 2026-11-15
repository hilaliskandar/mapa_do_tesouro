# FED03A — auditoria de desembolsos da RMRP

**Data:** 15/11/2026. **Origem:** snapshot privado Transferegov de 15/11, arquivo `siconv_desembolso_rmrp.csv`. **Escopo:** somente desembolsos associados a convênios de municípios proponentes da RMRP. **Sem homologação de investimento executado.**

## Execução e evidência
A base privada da FED02 foi copiada para um novo SQLite de ensaio e recebeu a tabela `desembolso_fluxo`. Os registros têm identificador de desembolso, número de convênio, IBGE7 proponente, data, exercício, número SIAFI e valor convertido para **centavos inteiros com Decimal**. Os campos `estagio='desembolso_ao_convenente'`, `natureza_despesa='nao_classificado'` e `qa_status='documental'` impedem promover essa extração como pagamento final de investimento.

Auditoria: 2.537 registros examinados; 2.537 IDs distintos; 0 valores inválidos, negativos ou zeros no recorte; 0 conflitos de IBGE entre desembolso e convênio; `PRAGMA integrity_check=ok`; `foreign_key_check` sem erros.

Soma bruta documental: **71.498.911.447 centavos (R$ 714.989.114,47)** no período **2008–2026**. Não inferir saldo líquido: eventuais devoluções e retificações de outros conjuntos ainda precisam ser conciliadas. Não somar o valor a investimentos municipais liquidados nem atribuir à execução de obras.

Recorte recente por ano de desembolso, em valores nominais brutos:
- 2023: 102 linhas, R$ 37.755.199,86;
- 2024: 90 linhas, R$ 120.055.217,32;
- 2025: 122 linhas, R$ 85.961.124,04;
- 2026: 160 linhas, R$ 121.801.512,03 (snapshot, não exercício encerrado).

**Persistência:** [Drive privado — pacote FED03A](https://drive.google.com/file/d/13w1UsPy7rjPsEFFYqOxSQZSPL4xq5yTt/view), ID `13w1UsPy7rjPsEFFYqOxSQZSPL4xq5yTt`; 866.587 bytes, pasta `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`, leitura de metadados confirmou `shared=false`. SHA256 ZIP local `1be587513fe1f7097e7ed42fe892f601a79435e99fb08d0427872f3cac326942`; SHA256 SQLite local `aa04125f573bf237db350c91a2836aef2b31871c4859048026ad6c3bd67893d4`. Readback de hash do ZIP remoto ainda pendente.

## Próxima operação FED03B
1. Obter na fonte nacional oficial, preferencialmente de snapshot privado já preservado, `siconv_pagamento`, `siconv_obtv_convenente`, `siconv_dl`, `siconv_itens_dl` e, quando possível, ordens bancárias CGU.
2. Relacionar por `NR_CONVENIO`, `NR_MOV_FIN` e `ID_DL` conforme cardinalidades auditadas, jamais combinar montantes em um join 1:N.
3. Distinguir repasse ao convenente de pagamento a favorecido, retenções, estornos e comprovantes de despesa de capital. A ausência de `ID_ITEM_PAD` na tabela de itens DL permanece como barreira para classificar GND4 pago.
4. Só produzir indicadores monetários publicados após prova de estágio, natureza de despesa, beneficiário e vínculo territorial. Os 218 projetos Obrasgov seguem como candidatos por município proponente, sem geolocalização homologada.
