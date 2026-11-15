# Diagnóstico da falha de aquisição nacional — RMRP

**Data do teste:** 15/11/2026. **Escopo:** determinar por que a aquisição pelo coletor Python no container da sessão falhou, apesar de operações semelhantes terem funcionado anteriormente. **Resultado:** problema de conectividade do **ambiente executor local**, não indisponibilidade do repositório Transferegov.

## Evidências observadas

### Ambiente local do container

- Código inspecionado: `/mnt/data/rmrp_next/collect_siconv_official_zips.py`, que usa `urllib.request.urlopen` para `https://api-publica.transferegov.gestao.gov.br/downloads/dadosgov/<arquivo>.zip` e calcula hash + CRC em arquivo temporário.
- Resolver configurado em `/etc/resolv.conf`: `168.63.129.16`. Não há proxy HTTP/HTTPS/ALL configurado nas variáveis de ambiente; `HTTP_PROXY`, `HTTPS_PROXY` e `ALL_PROXY` estão vazios. Isso descreve apenas este container.
- `socket.getaddrinfo(host,443)` retorna `[Errno -3] Temporary failure in name resolution` para `api-publica.transferegov.gestao.gov.br`, `www.gov.br`, `www.google.com` e `repositorio.dados.gov.br`. A falha é **generalizada**, não específica da fonte federal.
- Tentativas TCP via `socket.connect` para o resolvedor `168.63.129.16:53`, o IP `150.171.110.151:443` verificado em outro ambiente e `1.1.1.1:53` retornaram `Connection refused`. Logo, fixar IP ou trocar DNS manualmente não constitui solução demonstrada. O componente exato responsável pelo bloqueio (política de sandbox, rede virtual, firewall ou proxy) **não foi identificado** e não deve ser atribuído a um fabricante sem acesso às regras de infraestrutura.
- A execução anterior do coletor falhou antes de receber uma resposta HTTP; não houve resposta 404/429/403 nem dados incompletos na conexão local.

### Ambiente remoto independente — teste de controle

Foi executado no ambiente remoto de processamento Composio um teste de resolução DNS e de solicitação HTTPS ao **mesmo hostname**. Resultado:
- DNS `api-publica.transferegov.gestao.gov.br` resolveu para `150.171.110.151`.
- Requisição HEAD a `siconv_coordenadas_obra.zip` retornou **HTTP 200**, `Content-Length: 2996307` e `Content-Type: application/octet-stream`.
- Download integral de três ZIPs **concluído nesse ambiente remoto**, com SHA-256 e `zipfile.testzip()` comprovados:

| Arquivo oficial | Bytes | SHA-256 | CRC | Last-Modified UTC |
|---|---:|---|---|---|
| `siconv_coordenadas_obra.zip` | 2.996.307 | `c974e80db5b31e5682816ee66042c501d57782caf572966a8b911c991953337c` | OK | 2026-11-15 11:16:11 |
| `siconv_contrato_cipi.zip` | 4.275.091 | `19f6312d70508c5242bf08a984d662e0041fc8caff82eda482689461e0b07745` | OK | 2026-11-15 11:16:16 |
| `siconv_dados_obrasgov_geral.zip` | 785.514 | `b5d50a7aa6716df1565d1c9283200904cf234ea0c8971c3685e9f61476c77795` | OK | 2026-11-15 11:16:25 |

Os ZIPs continham, respectivamente, um CSV de 13.756.208 bytes, 22.422.227 bytes e 9.201.380 bytes descompactados. A aquisição foi **real**, não sintética. Esses arquivos estão no **filesystem remoto Composio** (`/home/user/rmrp_national_qa/`), não no container original nem no Google Drive. A persistência privada externa desses três arquivos **ainda deve ser executada e verificada**; não considerá-los disponíveis na pasta Drive.

### Outros canais

- Crawl2AI conseguiu renderizar a página `https://api-publica.transferegov.gestao.gov.br/downloads` e extrair os 65 arquivos e as URLs corretas. Isso confirma a disponibilidade do catálogo, mas sua interface de extração HTML não transfere automaticamente bytes ZIP ao container.
- Uma tentativa anterior de navegador Browserless falhou com `401` por limite de unidades do plano. Falha de cota de um terceiro serviço, **independente** da falha de DNS local.
- A integração Drive funcionou para armazenar ZIPs já disponíveis como arquivos de sessão, mas não transforma URL pública em arquivo ZIP por conta própria.

## Diagnóstico causal

**Causa imediata comprovada:** incapacidade do container da sessão de resolver DNS e estabelecer conexões TCP externas. **Hipótese de infraestrutura:** restrição de rede/sandbox do ambiente executor, não erro de lógica no coletor nem indisponibilidade do servidor de origem. O nível exato de bloqueio (gateway/firewall/proxy/configuração do orquestrador) permanece indeterminado.

**Por que operações anteriores funcionaram:** as aquisições anteriores utilizavam conectores remotos, Crawl2AI, navegador remoto ou outro executor com acesso à Internet; o script Python diretamente nesse container não compartilha necessariamente as permissões de rede dessas ferramentas. A diferença entre as redes foi reproduzida empiricamente neste diagnóstico, mas a rota interna histórica de cada transferência anterior não foi integralmente reconstituída.

## Encaminhamento

1. **Usar o runner remoto funcional** para baixar arquivos oficiais, registrar SHA-256/CRC, data, headers e contagem de CSV; não reiterar requisições do container bloqueado como se fossem uma falha da fonte.
2. **Transferir e conferir** os três ZIPs já baixados do filesystem remoto para Drive/R2 privado por um mecanismo autorizado; o acesso à pasta Drive não implica acesso automático ao filesystem remoto.
3. Executar FED04B com o cruzamento `ID_PROPOSTA` e `ID_CONTRATO_CIPI` no runner com acesso aos ZIPs; manter separadas localização candidata e execução física homologada.
4. Para FED03C, adquirir `siconv_obtv_convenente`, `siconv_dl`, `siconv_pagamento` e `siconv_itens_dl` preferencialmente em runner remoto com armazenamento privado e espaço/duração adequados, sem publicar microdados nacionais.
5. Se o objetivo operacional exigir execução local, solicitar liberação/ajuste de egress DNS/HTTPS ao administrador do ambiente da sessão; trocar nameserver ou usar IP fixo **não** demonstrou resolver o bloqueio.

**Produção:** não houve publicação de pagamentos como investimento executado, nem atribuição automática de pontos de obras. API pública permanece inalterada.
