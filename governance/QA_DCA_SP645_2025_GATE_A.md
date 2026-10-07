# QA definitivo — Gate A DCA SP 645 — 2025

Data de conclusão: 2026-10-07.

## Resultado

**Gate A aprovado.**

Workflow canônico:

- nome: `SICONFI SP 645 Full DCA Gate A`;
- run ID: `37693005628`;
- commit: `48e3731b6c3b039c4a809a932b9f97d99b3a117c`;
- conclusão: `success`.

## Integridade da aquisição

- municípios na geometria: 645;
- municípios solicitados: 645;
- anexos: I-C, I-D e I-E;
- respostas brutas: 1.935;
- falhas não resolvidas: 0;
- linhas normalizadas: 645;
- variáveis normalizadas: 26;
- issues de normalização: 0.

## Hashes

CSV normalizado:

`619367dd8b2c5b3db6f7a6c902b41e2f2685616cf8560e2e852e7583f386eec7`

Árvore bruta desta execução:

`c95adaf62b87580125adda685f23363391f30fed8e8dca261529f37c1cef34f3`

A execução estadual anterior produziu o mesmo SHA-256 para o CSV normalizado. O hash da árvore bruta foi diferente entre execuções, o que é compatível com a reaquisição de artefatos brutos que incorporam metadados/serialização próprios de cada execução. A igualdade do hash normalizado comprova estabilidade do contrato analítico.

## Cobertura principal

| Variável | Observado | Cobertura |
|---|---:|---:|
| Receita corrente bruta | 644 | 99,84% |
| Receita tributária bruta | 644 | 99,84% |
| IPTU | 643 | 99,69% |
| ITBI | 641 | 99,38% |
| ISS | 643 | 99,69% |
| FPM mensal | 643 | 99,69% |
| ICMS | 644 | 99,84% |
| IPVA | 643 | 99,69% |
| Despesa total liquidada | 644 | 99,84% |
| Despesa corrente liquidada | 644 | 99,84% |
| Pessoal e encargos | 644 | 99,84% |
| Investimentos | 644 | 99,84% |
| Saúde | 644 | 99,84% |
| Educação | 644 | 99,84% |
| Urbanismo | 639 | 99,07% |
| População DCA | 644 | 99,84% |

Rubricas naturalmente esparsas permanecem com cobertura menor e não devem ser convertidas automaticamente em zero.

## Ausências centrais

Sarutaiá, código IBGE `3551207`, permanece como ausência estrutural nas principais variáveis de 2025. Os três artefatos brutos existem, mas o Siconfi retornou listas de itens vazias em I-C, I-D e I-E. Isso é ausência da fonte no recorte, não falha do pipeline.

Outras ausências tributárias pontuais decorrem da inexistência da conta exata prevista pelo mapping em determinados municípios. A regra permanece: não substituir por rubrica aproximada e não converter ausência em zero.

## Decisão

O Gate A cumpriu os critérios de aceite:

1. universo estadual completo solicitado;
2. nenhuma perda silenciosa de município;
3. três anexos adquiridos;
4. nenhuma falha de requisição;
5. cobertura variável a variável produzida;
6. hashes registrados;
7. ausência preservada;
8. resultado normalizado reproduzível;
9. nenhuma alteração automática do baseline TIC-TIM 30.

O exercício 2025 está aprovado como referência estadual de auditoria e pode ser promovido a snapshot privado versionado.
