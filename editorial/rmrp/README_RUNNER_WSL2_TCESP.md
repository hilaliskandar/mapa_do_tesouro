# Runner TCESP da RM de Ribeirão Preto no WSL2

## Padrão reproduzido
Host Windows/Ubuntu 24.04 WSL2 do runner Crawl4AI existente, SEM reutilizar sua instância. Instalar em diretório independente `~/actions-runner-financas/actions-runner`; registrar somente no repositório `hilaliskandar/mapa_do_tesouro`, com rótulo customizado `financas-tcesp-wsl2`. O runner Crawl4AI anterior usa `~/actions-runner-crawl4ai/actions-runner` e `crawl4ai-ci-wsl2`; o runner Skills, também independente, não deve ser afetado. Manter execução manual (`./run.sh`) nesta fase, sem instalação como serviço e sem interferência nos demais runners.

## Instalação assistida no Ubuntu WSL2

1. No GitHub: **Settings > Actions > Runners > New self-hosted runner > Linux > x64** para **este repositório**. Usar a URL e o token de registro temporário apresentados pelo GitHub (não copiá-los para logs, chats, arquivos de configuração versionados ou scripts).
2. No terminal WSL2, criar a nova pasta e nela executar **os comandos exatos** de Download/Configure mostrados pelo GitHub. Exemplo de diretório inicial:
   ```bash
   mkdir -p ~/actions-runner-financas/actions-runner
   cd ~/actions-runner-financas/actions-runner
   ```
3. Durante `./config.sh`, usar um nome exclusivo como `Desk-alexandre-2024-financas` e adicionar a etiqueta customizada `financas-tcesp-wsl2`; manter os labels padrão Linux e X64. Usar diretório de trabalho `_work` exclusivo.
4. Iniciar dentro do diretório da instalação usando `./run.sh`. Confirmar estado **Idle/Online** nas configurações do repositório. Não instalar serviço automático nesta etapa.
5. Confirmar Python >= 3.10 na distro WSL2 (Ubuntu 24.04 já fornece Python 3.12) e conectividade com `https://transparencia.tce.sp.gov.br`.
6. Na aba Actions, executar manualmente `RMRP TCESP pilot - dedicated WSL2` usando a branch main. A execução faz **somente Ribeirão Preto 2025** e valida igualdade em centavos entre programas, ações e total 44 liquidado.
7. Auditar o artifact JSON e sua origem antes de ampliar a 2023/2024 ou outros municípios. Não dar deploy automaticamente.

## Segurança e governança

- Runner autohospedado executa processos sob a identidade da conta WSL2 e pode acessar arquivos legíveis por ela. Não processar PRs não confiáveis neste executor; workflow dedicado só tem `workflow_dispatch` e `contents: read`.
- Não usar tokens de registro no YAML nem persistir credenciais no checkout. Não montar pastas sensíveis do Windows dentro do ambiente de execução; evitar segredos no runner.
- Se repositório for público, endurecer o isolamento (usuário Unix dedicado/ambiente descartável) antes de qualquer workflow de origem não confiável. O padrão manual atual é apenas fase piloto supervisionada.
- Execuções do GitHub Actions não garantem preservação indefinida do artifact (retenção: 30 dias). Após validação, arquivar originais e hashes no armazenamento persistente canônico, sem sobrescrever FINBRA/DCA.
- Registrar URL da execução, hash do ZIP oficial, status das conciliações, data da coleta e versão do extrator.
- Rotina de 102 extratos e caderno editorial não são disparados por este workflow.

## Verificações

- [ ] Runner separado registrado/online.
- [ ] Workflow na main.
- [ ] Piloto executado e artifact examinado.
- [ ] Fonte e totais conferidos com DCA.
- [ ] Próximo lote liberado.


## Atualizacao operacional — 25/10/2026

Este guia de instalacao documenta uma fase piloto superada. O runner dedicado `financas-tcesp-wsl2` foi utilizado com sucesso para os workflows de reuso dos 106 extratos historicos RMRP/Sao Carlos ([run 40228943048](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40228943048)) e coleta parcial de 2026 nos 34 municipios da RMRP ([run 40229219185](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40229219185)). Os quatro lotes de 2026 foram concluidos.

Os arquivos validados foram preservados no bucket privado R2 `financas-municipais-sp-canonico` por workflows separados de promocao: [RMRP 2026](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40230188884), [RMRP 2023–2025](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40230628954) e [Sao Carlos 2023–2026](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40231520362). As tres execucoes verificaram a recuperacao e integridade SHA-256. Nao confundir esses snapshots privados com API SQLite ou painel publicado.

A matriz inicial de cobertura estadual foi produzida no [run 40231222578](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/40231222578), antes da persistencia de Sao Carlos; atualizar esta matriz antes de gerar a fila `missing-only`. A cobertura de 2026 e parcial, com Jardinopolis (receitas) somente ate maio e os outros extratos regionais ate agosto. Nao preencher meses ausentes com zero nem extrapolar ano fechado.

**O que permanece pendente:** catalogar os artefatos RMJ/TIC-TIM; identificar pares ainda sem snapshot; construir ingestao complementar no SQLite/API e testes de regressao; promover novas coletas de forma seletiva. O README raiz concentra o estado e as chaves R2 atualizados.
