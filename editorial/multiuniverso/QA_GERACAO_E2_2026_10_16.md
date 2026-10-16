# Verificação da primeira geração E2 — 16/10/2026

## Resultado
- PR #198; commit corretivo b877f991e64844683a4bf2e7a19897d05e2d00dc.
- Run do gerador: https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38883975929
- Artefato: 12038244817 (dez HTMLs e manifest.json).
- Catálogo verificado: 11 universos editoriais, dos quais RM_JUNDIAI excluído por já possuir boletim.
- Dez edições produzidas, cada uma com 50 contas/indicadores do contexto em 2025.
- Conferência independente do ZIP: entre 48 e 49 medianas numéricas por edição; faltantes mantidas como indisponíveis.
- Falha do primeiro run: buscava mediana e quartis em latest, quando o contrato real usa latest.numeric. Corrigido e nova geração concluída. Nomes públicos obtidos do metadata.nome e unidades de metadata.unidade.
- A RM de Campinas tem 20 municípios. Mediana observada do IPTU 2025 no contexto: R$ 39.422.797,795 (HTML arredonda a dois decimais). Esta cifra é mediana municipal, não o total regional.

## Escopo da versão
Os dez HTMLs são **primeiras edições tabulares de referência**, ainda não equivalem ao boletim RMJ de 23+ seções. Estão presentes grupos de receitas, despesas, território, dívida/liquidez/CAPAG, quartis, cobertura e membros. Ainda faltam as fichas municipais, trajetórias interpretativas, gráficos e componentes de investimento por programa/ação. Não há inferência causal no produto.

## Gates restantes
1. Conferência de valores e unidades contra os contextos da API, por amostragem e por variável.
2. Revisão de agrupamentos e denominações no dicionário (algumas variáveis podem cair em Outros).
3. Compatibilizar interface, acessibilidade, navegação e interação com padrões públicos aprovados na RMJ.
4. Incorporar fichas municipais alimentadas por JSONs por município (sem copiar narrativa da RMJ).
5. Testes Playwright computador/celular e promoção específica para produção, preservando portal estadual e RMJ.
6. Atualizar inventário, versões e manifesto de implantação após cada edição homologada.

Não declarar a publicação dos dez novos boletins: os arquivos estão no artefato CI e no pacote disponibilizado ao usuário, não em Cloudflare Pages.

## Segunda revisão do gerador — 16/10/2026

Commit `8c8a7fa1ca0b275a55d972b037b4668437f31872`; execução https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38884429450, conclusão `success`. Artefato ID `12039211447`, SHA-256 do ZIP `5b8ae75f08011d585443983fa3720108df204329ec226473eb81e2033b38bb4f`.

Mudanças implementadas: (a) correção dos nomes municipais no campo `nome`; (b) classificação editorial passa a ler `metadata.nome`; (c) apresentação dos percentuais multiplicados por 100, uma vez que a API armazena razões decimais, mesmo quando o catálogo registra unidade percentual; (d) leitura de `yearly` como lista e inclusão de tabela de evolução das medianas por exercício. Conferência do ZIP confirmou os dez identificadores e cardinalidades: RM São Paulo 38; Baixada Santista 9; Campinas 20; Vale do Paraíba e Litoral Norte 39; Sorocaba 27; Ribeirão Preto 34; São José do Rio Preto 37; Piracicaba 24; AU Franca 19; Cidades Médias 33.

Limite verificado: os arquivos apresentam entre 122 e 123 linhas de tabelas cada, incluindo histórico disponível; NÃO devem ser considerados séries longas 2013–2025 completas nem fichas individuais. O histórico exposto depende da oferta real de cada variável na API. Antes de publicação de caráter definitivo, conferir manualmente os indicadores percentuais e a hierarquia das contas, ampliar fichas municipais e submeter à revisão editorial e funcional.

## Fichas municipais — lote concluído em 16/10/2026

- Código `editorial/multiuniverso/build_fichas.py`, commit `09ea1fc0`.
- Workflow `.github/workflows/build-editorial-universes.yml` atualizado no commit `51c2cf55`.
- Execução https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38885167876 aprovada; artefato `12038634197`, SHA-256 `4ae8a9ef9fbef3ed5295e7ba11daec983697e583fe90cfe2b7c40ce7f1d02056`.
- ZIP inspecionado: dez boletins, **280 fichas municipais**, respectivos identificadores e cardinalidades em conformidade; cada ficha aponta para o JSON individual de origem.
- As fichas contêm valores individuais, medianas intragrupo, cobertura, status, posição relativa e séries disponíveis. Exemplo conferido: Aramina (AU de Franca) com 37 das 50 variáveis observadas em 2025.
- **Não houve publicação no Cloudflare nem merge do PR #198**. Os resultados permanecem como artefato de homologação.
- Não há ainda exame editorial completo da interpretação dos indicadores, acessibilidade em navegador, revisão das séries oficiais por amostra e tipologia de métricas. Não apresentar as fichas como relatório definitivo.

## Auditoria semântica e revisão responsiva — 16/10/2026

Commit `3504de16fda51d1a58bf862020751828c2e98b92`. Geração no run https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38887742504 concluída em `success`; artefato `12040606699`, SHA-256 `fe109ebc50fb5f5fbcf4c4771f9b664161036a281dd2b7111f089077d7c0d9fa`. Conferência do ZIP: 291 arquivos (dez index.html, 280 fichas e manifesto), dez sínteses comparativas e todos os 280 links das fichas presentes. Os testes unitários de percentual (incluindo zero), cobertura e supressão de síntese incompleta foram incorporados ao fluxo. O gerador agora exige que `expected` coincida com `member_count` e só usa na síntese variáveis totalmente observadas, com n>=4 e quartis ordenados. CSS responsivo e foco de teclado acrescentados à navegação. Trata-se de QA automatizado e inspeção estrutural de pacote, não de auditoria substantiva de todas as declarações municipais nem teste visual independente em navegador. O PR permanece candidato sem publicação externa.
