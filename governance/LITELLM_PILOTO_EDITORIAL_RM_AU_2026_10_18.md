# LiteLLM na produção dos cadernos fiscais — avaliação e piloto controlado

Data: 18/10/2026. Estado: PROPOSTA TÉCNICA; nenhuma API, gateway, chave ou deploy alterado.

## Premissas observadas

- A API fiscal estadual v2 já dispõe de pipeline canônico e artefatos privados; a geração de cadernos deve consumir somente um snapshot validado, não fazer consultas fiscais externas na etapa editorial.
- O repositório não apresentou integração LiteLLM identificável nas buscas por `litellm`.
- Há histórico de testes do usuário com gateway LiteLLM em Windows e modelos OpenRouter, mas os ensaios anteriores retornaram erros HTTP 400 para saídas em JSON. **Não considerar compatibilidade de JSON Schema/structured outputs comprovada.**
- A documentação oficial LiteLLM descreve proxy compatível com OpenAI, roteamento, retries, fallbacks e acompanhamento de consumo. Os recursos variam por modelo/provedor; o controle de orçamento por chaves/equipes exige banco de dados e não pode ser presumido sem PostgreSQL. Referências: https://docs.litellm.ai/docs/ ; https://docs.litellm.ai/docs/routing ; https://docs.litellm.ai/docs/proxy/users

## Separação de responsabilidades

1. **Determinístico (sem LLM):** ingestão, classificação contábil, harmonização, somas, razões, IPCA, cobertura, status, agregação, CAPAG e cálculos estatísticos. Não aceitar reinterpretação numérica por modelo.
2. **LiteLLM opcional:** transformar JSON fiscal *congelado* da API em propostas de narrativa, resumos municipais, comparações e sinais de inconsistência que exijam revisão humana.
3. **Validador determinístico:** rejeitar qualquer número, ano, município, variável, unidade ou referência inexistente na evidência; verificar percentuais com metadados certificados e impedir causalidade sem prova.
4. **Editor humano:** aprovar linguagem, ressalvas, inferências e pertinência pública; só então compor PDF ou HTML.
5. **Pipeline de publicação:** gerar índices, numeração, remissões e checksums; homologação separada de renderização/deploy.

## Contrato mínimo de entrada para uma tarefa LLM

`run_id`, `snapshot_sha256`, `api_contract_version`, `universe_id`, `codigo_ibge` (opcional), `ano_inicio`, `ano_fim`, `variables` com `variable_id`, `value`, `status`, `unit`, `storage_scale`, `display_multiplier`, `source_ref`, `coverage`, `comparability_status`; `evidence_ids` válidos.

Não enviar identificadores pessoais, credenciais ou payloads além do necessário. Preferir redução para fatos/medidas autorizados. Registrar política de retenção e destino dos dados por provedor antes do uso externo.

## Contrato mínimo de saída

`section_id`, `claims[]` com `claim_id`, `text`, `evidence_ids[]`, `risk_tags[]`, `confidence_label` e `requires_human_review`; `limitations[]`, `unanswered_questions[]`. Cada frase quantitativa deve apontar a uma evidência existente. Todo conteúdo gerado permanece `draft` até dupla revisão.

`confidence_label` é qualificação editorial; não representa probabilidade calibrada de acerto.

## Portões do piloto

- L0: snapshot API v2 publicado ou privado validado, com metadados e hash; nenhuma mistura de releases.
- L1: teste de gateway LiteLLM já existente (`/health`, `/v1/models`, teste mínimo); não registrar chaves no GitHub. Modelos selecionados por evidência real de funcionamento.
- L2: ensaio de JSON Schema em **cada modelo e provedor**; se retornar 400, usar outro modelo certificado ou geração de texto seguida de parser e validação estrita, sem presumir sucesso.
- L3: conjunto ouro de 21 perguntas da RMJ (completamente documentadas) + 9 não respondíveis; falso positivo na resposta de pergunta sem evidência é falha bloqueante. Não exigir redação literal sem fonte recuperada.
- L4: 100% de cifras, anos, unidades, nomes, referências e coberturas na saída reconciliados com os dados de entrada; qualquer citação inexistente ou percentual de escala não certificada bloqueia publicação.
- L5: medir custo, tempo, taxa de saídas JSON válidas, alucinações, revisão editorial e cobertura de questões. Comparar: (a) texto atual sem LLM, (b) LiteLLM com modelo primário, (c) modelo alternativo somente quando autorizado.
- L6: não inserir texto no site/PDF nem promover API até aprovação humana e QA integral.

## Políticas de fallback e segurança

- Fallback pode alterar qualidade/segurança de dados: permitir só modelos com testes e política de dados equivalente, com `model_id` e `provider` registrados.
- Retries devem ser limitados por tarefa e idempotentes, sem alteração de evidência.
- Cache por (`snapshot_sha256`, `prompt_version`, `model_id`, `parameters_hash`) e nunca reusar sobre revisão fiscal distinta.
- Logs: conservar identificadores técnicos, tokens, custo, tempo e status; não armazenar sem necessidade a íntegra de payload fiscal em fornecedores.
- Orçamento: se não houver PostgreSQL no proxy, depender de limite externo do provedor e contabilidade local; não anunciar limite LiteLLM efetivo.
- A prioridade é uso editorial assistido, não produzir interpretações autônomas definitivas.

## Entrega seguinte

Executar auditoria do gateway do ambiente do usuário e contrato API v2 mais recente, sem assumir acesso local ao servidor Windows. Criar protótipo `editorial/llm_draft` isolado, sem alterar `pipeline/accounting`, mantendo um conjunto ouro de perguntas e 1-2 seções regionais. Somente depois considerar integração a Skills `boletim-fiscal-universo` e `boletim-fiscal-municipal`.
