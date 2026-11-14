# INV-RMRP — FED02, cruzamento PAD GND4 e desembolsos federais

Data de implantação: 14/11/2026. Branch: `investimentos-territoriais-sp645-20261111`. Não é homologação financeira.

## Resultado territorial anterior, confirmado
Run [43561970362](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43561970362), success. Dos 7.917 itens de Plano de Aplicação Detalhado com GND4 e `SIT_ITEM=APROVADO`, 7.891 possuem nome de município indicado correspondente a um dos 34 municípios da RMRP, 20 indicam outras localidades de SP e 6 indicam outras UFs. Entre os 7.891 estão sete itens cujo município indicado é um município da RMRP **diferente** do proponente. Estes são dados de itens planejados, não execução. A relação integral dos 26 itens excepcionais, incluindo IDs de proposta e item, está no log do job 132347441150.

## Nova rotina FED02
Código: `pipeline/acquire/inv_rmrp_fed02_crosswalk.py`; workflow: `.github/workflows/inv-rmrp-fed02-crosswalk.yml`. Commit de implantação do workflow: `8a3e34ffb7a13443f0bc4bb68741a0f4f88409c9`. Execução [43610314591](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43610314591), iniciada e em andamento no primeiro checkpoint.

Fontes oficiais integrais baixadas diretamente pelo GitHub Actions no runner:
- `siconv_proposta`: `ID_PROPOSTA`, `COD_MUNIC_IBGE` e `UF_PROPONENTE`;
- `siconv_convenio`: `ID_PROPOSTA` → `NR_CONVENIO`;
- `siconv_desembolso`: `NR_CONVENIO` → `ID_DESEMBOLSO`;
- `siconv_plano_aplicacao_detalhado`: `ID_PROPOSTA` → `ID_ITEM_PAD`, natureza/GND, situação e município informado.

Saída prevista: `matriz_proposta_conv_pad_desembolso_nao_monetaria.csv`, uma linha por proposta, contagens de convênios, eventos de desembolso, itens GND4 aprovados, localização e classe de cruzamento, mais manifesto `manifest_fed02.json` com SHA256 dos ZIPs oficiais, contagem nacional, contagem regional e checklist QA. Arquivos são artefatos de Actions; não há gravação em R2 nem integração com SQLite de produção.

As quatro classes de observação são: (1) proposta com GND4 aprovado **e** desembolso vinculado por convênio; (2) GND4 aprovado, sem desembolso identificado; (3) desembolso identificado, sem GND4 aprovado; (4) nenhum dos dois. Cada categoria exige investigação própria; a primeira não autoriza tratar todo desembolso como investimento, pois instrumento misto pode conter custeio e capital. A ausência de desembolso na versão de origem não prova valor zero.

## Critérios de aprovação
A execução deve passar por: 34 códigos IBGE distintos na referência; propostas territorializadas por IBGE/UF; chaves de convênio não conflitantes; unicidade de IDs de itens e de eventos; 6.410 propostas RMRP e 7.917 itens GND4 aprovados consistentes com a última fotografia oficial (se a fonte mudar, o job deve falhar para exigir revisão); soma dos eventos por proposta igual ao número selecionado de eventos; sem geração de qualquer valor monetário presumido.

Após examinar o resultado do job, registrar contagem de propostas em cada categoria, instrumentos com despesas de natureza mista, diferenças de localização física, recuperação dos eventuais pagamentos a favorecido e validação dos fluxos que efetivamente representam investimento. Persistência R2 e readback continuam pendentes, sem alegação de execução.
