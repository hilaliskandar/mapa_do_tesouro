# Regressão analítica — tipologias, marcadores e pares

## Resultado principal

A regra aprovada do Bloco 3 para pares foi reconstruída a partir da base multifuentes, sem depender dos valores calculados das fórmulas do XLSX.

A assinatura comparativa utiliza **seis marcadores**:

1. base tributária;
2. investimento;
3. peso territorial;
4. pessoal;
5. dívida;
6. liquidez.

A classificação de DCL continua existindo como tipologia e indicador, mas **não entra na assinatura de pares**. CAPAG também não entra no cálculo de similaridade.

## Paridade com os pares materializados no Bloco 3

Quando são reproduzidas:

- a regra territorial legada;
- as tipologias por mediana;
- o CV como desvio-padrão amostral dividido pela média;
- o mínimo de 3 anos;
- os seis marcadores;
- a seleção por proporção > coincidências > cobertura > nome;
- mínimo de 4 marcadores comparáveis;

o resultado é:

- municípios: 30;
- posições prioritárias esperadas: 90;
- divergências entre reconstrução e aba `Pares prioritários`: **0**.

Portanto a lógica histórica dos pares está integralmente reproduzida.

## Efeito da regra territorial estrita

Ao substituir a soma parcial de funções territoriais pela regra estrita, mantendo todas as demais regras inalteradas:

- 25 dos 30 municípios mudam de marcador territorial;
- 26 dos 30 municípios mudam ao menos uma posição entre seus três pares prioritários;
- pares principais recíprocos passam de 9 para 6.

### Pares principais recíprocos no legado

- Americana — Valinhos
- Artur Nogueira — Cosmópolis
- Caieiras — Itupeva
- Campo Limpo Paulista — Vinhedo
- Francisco Morato — Paulínia
- Franco da Rocha — Santo Antônio de Posse
- Holambra — Morungaba
- Indaiatuba — Jundiaí
- Itatiba — Jarinu

### Pares principais recíprocos com regra territorial estrita

- Americana — Valinhos
- Artur Nogueira — Engenheiro Coelho
- Cabreúva — Francisco Morato
- Campinas — Campo Limpo Paulista
- Holambra — Morungaba
- Indaiatuba — Jundiaí

## Interpretação

A mudança não indica erro no algoritmo de pares. Ela decorre da redução acentuada da cobertura da dimensão territorial quando se exige presença simultânea das cinco funções.

A decisão sobre a regra territorial deve, portanto, preceder a promoção definitiva de tipologias e pares. O núcleo deve ser capaz de reproduzir ambos os cenários durante o QA:

- `legacy_partial`: baseline histórico reproduzível;
- `strict_complete`: cenário canônico candidato.

Somente um deles deve ser marcado como padrão após decisão metodológica explícita.
