# API fiscal — contrato de completude v2 (proposta)
Data: 2026-10-12. Estado: projeto técnico, não publicado.

## Lacuna comprovada
O exportador atual utiliza publication_variables_v1.yml e só gera fichas municipais dentro de 11 universos editoriais. Os 287 contextos município × universo não são equivalentes a 645 consultas estaduais independentes. Uma variável presente no SQLite não está necessariamente exposta na API.

## Contratos de consulta planejados
- /data/api/v2/catalog/variables.json — catálogo de todas as contas, agregações, indicadores, classificações e suas escalas, fórmulas, unidades, fonte e situação de qualidade.
- /data/api/v2/catalog/universes.json — universos analíticos estaduais e regionais, com identificação de recortes editoriais.
- /data/api/v2/municipalities/{codigo_ibge}.json — contexto independente de grupo para cada um dos 645 municípios.
- /data/api/v2/universes/{universe_id}/context.json — agregações, estatísticas, séries, cobertura e lista de membros.
- /data/api/v2/universes/{universe_id}/municipalities/{codigo_ibge}.json — comparação do município exclusivamente no universo escolhido.
- /data/api/v2/coverage/{universe_id}.json — matriz de estados por variável, ano, fonte e universo.
- /data/api/v2/methodology/{variable_id}.json — definição, fórmula, crosswalk, proveniência e cautelas.
- /data/api/v2/manifest.json — versões, hashes, contagens, QA de dados e QA de publicação separados.

## Integridade obrigatória
1. 645 códigos IBGE únicos na API municipal estadual, incluindo municípios sem observações.
2. Quatro estados distintos: observado, ausente, nao_aplicavel, em_revisao; zero observado não é ausência.
3. Todas as variáveis do catálogo canônico identificadas como publicadas, não publicadas, insuficientes ou em revisão, com motivo.
4. Metadados obrigatórios por variável: natureza, fórmula, unidade, storage_scale, display_multiplier, fonte, periodicidade, como_ler e cautelas.
5. Razões percentuais: distinguir armazenamento decimal da exibição em percentual; nunca aplicar conversão heurística silenciosa.
6. CAPAG: ano-base e posição do snapshot separados; indicadores legais não substituídos por aproximações.
7. Estatísticas regionais reproduzíveis a partir de membros observados, com cobertura; nunca somar percentuais como se fossem recursos.
8. Crosswalk histórico por fonte, ano, código e estágio para demonstrar comparabilidade temporal.
9. Valores nulos acompanhados de estados; sem NaN ou Infinity.
10. QA automático da paridade TIC_TIM_30, interface e API anterior; regressões explicadas antes da promoção.
11. Manifesto com hash e status separados para snapshot, build e publicação.
12. Fonte e referência de cada observação rastreáveis até documentos ou artefatos de origem.

## Sequência de implementação
P0 — inventariar catálogo integral e mapear diferenças frente à API editorial v1; resolver escala e metadados de QA.
P1 — publicar API municipal SP_645 por código IBGE e disponibilizar matrizes de disponibilidade.
P2 — estender universos regionais a todo o catálogo elegível; metadados, crosswalk e proveniência por variável.
P3 — testes automatizados de contratos, paridade, cobertura, tamanho e desempenho; publicação sob nova versão.

Manter a versão v1 e a publicação atual intocadas até QA e promoção formal. Usar JSON materializado do SQLite canônico sem Worker/D1 obrigatório em runtime.