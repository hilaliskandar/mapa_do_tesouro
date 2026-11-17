# FED06C — prévia local de verificação privada da API v3

**Executado em 15/11/2026.** A partir do ZIP FED06B com 280 JSON e dimensão oficial de 34 municípios nas quatro sub-regiões da RMRP, foi gerada uma interface HTML inteiramente **local, autocontida e somente leitura**.

## Funcionamento entregue

- `preview_rmrp_offline.html` pode ser aberto no navegador diretamente, após extrair o ZIP, sem servidor nem acesso à rede.
- Seletores de sub-região (todas, 01, 02, 03 e 04), busca municipal e ordenação por município, número de convênios, projetos Obrasgov candidatos e linhas de desembolso.
- Indicadores de **contagem** por município proponente: propostas discricionárias, convênios, obras candidatas, desembolsos (linhas) e propostas de Parcerias. Não representam o conjunto territorial de obras nem somatório de investimento executado.
- Série histórica **regional**, independente dos filtros municipais nesta primeira prévia, dos desembolsos brutos ao convenente em 2008–2026; valores em centavos inteiros na fonte, formatados em reais, sem correção monetária, estornos ou devoluções.
- Avisos visíveis de privacidade, não homologação financeira, ausência de georreferenciamento físico, ausência de autorização de publicação e impossibilidade de somar estágios distintos.

## Verificações realizadas

| Teste | Resultado |
|---|---|
| Municípios | 34/34 |
| Sub-regiões | 15, 6, 6 e 7 |
| Exercícios | 19 (2008 a 2026) |
| Manifesto de autorização pública | `false` |
| Dependências externas de execução HTML | 0 |
| Sintaxe JavaScript no Node `--check` | Aprovada |
| CRC dos membros ZIP | Aprovado |
| Arquivos JSON da API preservados | 280 |
| Publicação na plataforma pública | Não realizada |

**Nota:** a validação é documental, lógica e de sintaxe; não corresponde a teste visual automatizado em navegadores variados, nem a teste de hospedagem em Cloudflare Pages.

## Persistência

O pacote [RMRP_FED06C_PREVIA_LOCAL_PRIVADA_2026-11-15.zip](https://drive.google.com/file/d/1twgK_RpEKkLvCQ8-Xbsdu-5ieWy35m4c/view), ID `1twgK_RpEKkLvCQ8-Xbsdu-5ieWy35m4c`, foi gravado na pasta privada do projeto `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`. Após upload, download de conferência comprovou 625.145 bytes, `shared=false`, SHA-256 idêntico ao local `4ecfb4ff6c7fc504ea5f09a878b184b9195aee0507dc958eff4bd94cd3fa3d23` e CRC integral válido.

O pacote inclui os arquivos JSON, o HTML, roteiro `README_PREVIA_LOCAL.txt`, `QA_FED06C_OFFLINE.json` e `build_rmrp_fed06c_preview.py`. O FED06B permanece preservado como etapa anterior imutável.

## Bloqueios pendentes

**FED03C:** pagamentos nacionais, OBTV, DL, itens DL e classificação GND4 paga exigem aquisição e conciliação em runner com acesso às fontes. **FED04B:** as coordenadas de propostas e os vínculos com projetos Obrasgov exigem auditoria documental e geométrica. **Implantação:** sem autorização até homologação dos resultados e testes de segurança/compatibilidade em prévia restrita. Os filtros de sub-região não atribuem obras ao local de execução, apenas organizam registros de proponentes.
