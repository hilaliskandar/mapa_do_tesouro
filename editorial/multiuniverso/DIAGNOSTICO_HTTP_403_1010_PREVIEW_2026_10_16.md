# Diagnóstico HTTP 403 / Cloudflare 1010 — ambiente de homologação E2

Data: 16/10/2026. Escopo **somente** o projeto Cloudflare Pages `financas-e2-homologacao`.

## Evidência reproduzida

- Deploy de revisão e deploy na ramificação principal do projeto **isolado** concluídos com `stage=success` no Cloudflare.
- Primeira rotina de teste usava indevidamente `revision-e2-20261016.financas-e2-homologacao.pages.dev` depois de mudar a ramificação de deploy. Corrigido no commit `ea393158` para `financas-e2-homologacao.pages.dev`.
- [GitHub Actions 38934051195](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38934051195) testou a URL corrigida `https://financas-e2-homologacao.pages.dev/data/api/v1/publication/universes.json`.
- HTTP `403`, corpo `error code: 1010`, servidor `cloudflare`, cabeçalho `CF-RAY` presente; várias tentativas repetiram o resultado.
- A documentação Cloudflare associa 1010 ao bloqueio de assinatura do navegador/cliente: https://developers.cloudflare.com/support/troubleshooting/http-status-codes/cloudflare-1xxx-errors/

## Interpretação estrita

O bloqueio foi observado **no cliente HTTP do GitHub Actions**, antes de se verificar o conteúdo da API e da página HTML. Ainda não foi demonstrado que usuários comuns em navegador sejam bloqueados. Também não há prova de que o bloqueio decorra de erro nos HTMLs ou no JSON. A implantação aprovada não equivale a acessibilidade pública aprovada.

Não desabilitar indiscriminadamente controles WAF/Bot do Cloudflare e não modificar projetos públicos existentes para contornar o teste. Examinar, se disponíveis, eventos de segurança do Cloudflare e filtros por `CF-RAY` e URL do projeto; retestar em navegador legítimo e fonte de rede independente.

## Gates remanescentes

1. Receber HTTP 200 com JSON válido da API versionada no domínio de homologação.
2. Receber HTTP 200 de cada um dos dez boletins e amostra/totalidade das fichas; conferir os vínculos JSON relativos.
3. Confirmar resultados a partir de cliente externo independente do runner de CI.
4. Declarar publicação somente após comprovação desses resultados.

**Estado:** implantação isolada concluída; liberação pública dos boletins **não homologada**. Nenhum merge nem atualização dos domínios `finbra-tic-tim-referencia` e `financas-rmj`.
