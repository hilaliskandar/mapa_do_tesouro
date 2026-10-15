# Auditoria das ausências por função na DCA — 2025

Data: 14/10/2026.

## Origem

- Fonte: respostas brutas do Anexo I-E da DCA, execução GitHub Actions Gate A [#37693005628](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/37693005628).
- Artefato bruto: `sp645-full-dca-2025-raw`, ID GitHub `11517325899`.
- Árvore bruta aprovada: `sha256:c95adaf62b87580125adda685f23363391f30fed8e8dca261529f37c1cef34f3`.
- Total: 645 arquivos do Anexo I-E; o pacote abrange 1.935 arquivos de três anexos.
- Critério de correspondência: coluna `Despesas Liquidadas`; rótulo `Total Geral da Despesa por Função`; código `TotalDespesas`; prefixo da função 15, 16, 17, 18 ou 26.

## Resultado verificável

| Função | Observado não zero | Linha não encontrada | Valor zero explícito | Campo vazio | Correspondências múltiplas |
|---|---:|---:|---:|---:|---:|
| Urbanismo | 639 | 6 | 0 | 0 | 0 |
| Habitação | 146 | 499 | 0 | 0 | 0 |
| Saneamento | 330 | 315 | 0 | 0 | 0 |
| Gestão ambiental | 527 | 118 | 0 | 0 | 0 |
| Transporte | 458 | 187 | 0 | 0 | 0 |

Os números correspondem à cobertura já observada na planilha multifuentes e no SQLite: a passagem pelo normalizador não gerou perda adicional nas cinco funções. Para as linhas ausentes **não se pode inferir que o valor seja zero**.

## Diagnóstico

A ausência já se manifesta no arquivo bruto do Anexo I-E, **sob o critério exato do mapeamento**. Isso não exclui eventual informação em outra conta, subfunção, estágio, anexo ou versão retificada. O acervo de respostas preservadas constitui evidência para a versão e o recorte consultados, não uma afirmação de inexistência de despesa municipal.

A regra de agregação `strict_sum` exige as cinco funções. Como apenas 65 municípios possuem as cinco observadas, o agregado completo fica ausente para 580 municípios; essa regra é cautelosa mas limita a cobertura do índice.

## Encaminhamento

1. Preservar `ausente` no conjunto canônico; proibir imputação automática de zero.
2. Verificar se a DCA oferece subfunções ou linhas alternativas oficialmente conciliáveis para os casos sem linha de função.
3. Identificar eventuais declarações retificadoras e versões posteriores com controle de fonte e data.
4. Publicar indicadores das cinco funções individualmente, com cobertura e estado de disponibilidade.
5. Considerar uma soma parcial **somente como indicador distinto e explicitamente incompleto**, com contagem de funções observadas, jamais como substituição silenciosa do agregado completo.

O workflow `audit-dca-function-missingness.yml` passa a reutilizar diretamente o artefato aprovado do Gate A, em lugar de depender de um snapshot bruto inexistente no caminho esperado do R2. A mudança não modifica produção pública.
