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
