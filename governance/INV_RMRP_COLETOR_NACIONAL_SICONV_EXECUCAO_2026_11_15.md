# RMRP — aquisição dos ZIPs nacionais SICONV: estado real em 15/11/2026

**Solicitação:** preservar os ZIPs no Google Drive e prosseguir na aquisição, conciliação FED03C e territorialização FED04B.

## Persistência conferida

A pasta Drive privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9` contém 13 ZIPs previamente armazenados: aquisições regionais Transferegov e Obrasgov, QA FED01/FED02, FED03A/B/C, FED04A, API FED05 e prévias FED06/B/C. A leitura dos metadados constatou os nomes, IDs, tamanhos e a situação `shared=false`. Os ZIPs regionais originais não foram substituídos.

**Novo ZIP gravado e verificado:** [RMRP_COLETOR_NACIONAL_SICONV_2026-11-15.zip](https://drive.google.com/file/d/1L_aQ1Zdh-_rNj_Hojg2f4vQzlIZ3bYO6/view), ID `1L_aQ1Zdh-_rNj_Hojg2f4vQzlIZ3bYO6`, 6.181 bytes, `shared=false`, SHA-256 local e de readback `f4fed0ce64a9854d6f02c935522a15182b8c5f6dc4f1c0f36ce4b10de95e5b95`, CRC de todos os membros íntegro.

Esse **ZIP contém somente código, testes, instruções e um manifesto de tentativas malsucedidas**, não os sete ZIPs nacionais brutos. Não o confundir com a aquisição nacional concluída.

## Rotina incremental testada

O arquivo `collect_siconv_official_zips.py` implementa:
- catálogo de sete URLs de arquivos nacionais oficiais, verificados no portal em 15/11/2026;
- default de três arquivos menores: `siconv_coordenadas_obra.zip`, `siconv_contrato_cipi.zip`, `siconv_dados_obrasgov_geral.zip`;
- opção explícita `--include-large` para os conjuntos financeiros `siconv_obtv_convenente`, `siconv_dl`, `siconv_pagamento`, `siconv_itens_dl`;
- aquisição por streaming, proteção por limite de tamanho, `ETag`/`Last-Modified` quando informados, SHA-256 e CRC integral, verificação de CSV presente;
- retomada idempotente: ZIP já existente somente é reutilizado após SHA-256/CRC. Arquivo corrompido prévio não é sobrescrito; downloads parciais são eliminados após falha; manifesto incremental persiste estados reais;
- nenhum envio automático de microdados nacionais ao GitHub, Cloudflare Pages ou API pública.

`python -m unittest -v test_collect`: **3 testes passaram** (download controlado e reutilização sem redownload, detecção de ZIP existente inválido, falha de rede com eliminação de parcial). Testes utilizaram ZIP **sintético** injetado por mock, não dados federais reais.

## Tentativa real de aquisição

O comando executado `python collect_siconv_official_zips.py --out-dir ... --attempts 1` retornou:
- `siconv_coordenadas_obra`: `failed`, erro `[Errno -3] Temporary failure in name resolution`;
- `siconv_contrato_cipi`: `failed`, mesmo erro DNS;
- `siconv_dados_obrasgov_geral`: `failed`, mesmo erro DNS.

O manifesto de tentativas foi incluído no ZIP. **Nenhum dos três arquivos foi baixado**; não foi realizado CRC/QA de ZIP nacional nesta rodada. Os quatro arquivos financeiros maiores não foram requisitados automaticamente, para evitar operações volumosas quando o DNS está bloqueado.

## Execução no ambiente com conectividade

Descompactar o ZIP privado em pasta de aquisição autorizada e executar:

```powershell
python -m unittest -v test_collect
python collect_siconv_official_zips.py --out-dir D:\RMRP\siconv_nacional
```

Depois de conferir `status=all_verified` e os hashes no manifesto, persistir os **ZIPs originais** em Drive/R2 privado com readback e realizar FED04B sobre coordenadas/ponte CIPI. Para os conjuntos financeiros:

```powershell
python collect_siconv_official_zips.py --out-dir D:\RMRP\siconv_nacional --include-large
```

Depois, executar os reconciliadores privados existentes para FED03C com os 1.793 convênios de proponentes RMRP. Evitar duplicação `NR_MOV_FIN` após junção 1:N com OBTV. O vínculo de `siconv_coordenadas_obra` com proposta não demonstra localização física de projeto Obrasgov.

**Controle de publicação:** FED03C e FED04B continuam não homologados. `public_release_authorized=false`; produção e base fiscal canônica não foram alteradas.
