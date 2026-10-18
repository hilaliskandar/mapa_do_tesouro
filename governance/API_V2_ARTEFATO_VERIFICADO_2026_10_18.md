# Conferência independente do pacote privado da API v2 — 18/10/2026

## Origem verificada
- GitHub Actions run 38593209824; artifact ID 11908541959 (`sp645-private-site-38593209824`), recuperado nesta execução.
- SHA-256 do ZIP confirmado: `9ca1688182eb90a02517c9664dabd4870d88a9abdaad28e6cafd82bd3be81b21`.
- ZIP contém 4.225 entradas. Caminho raiz: `site-sp645/data/api/v2/`.
- Hashes SHA-256 dos arquivos no ZIP:
  - `manifest.json`: `4431da62627c513e8f7a3d6ea4f79c47f2a8eb69a3372ed6cc947c152601649e`;
  - `catalog/variables.json`: `c04d2db4e03e4824d86f21b8d7bf2ce6c5587cc4556047a64a2e2aa74a480f22`;
  - `catalog/universes.json`: `f6901360e6b43f8d4ad354a4c87ae1b3556143a9eff67a854b29f88cf155648b`;
  - `qa/readiness.json`: `5b43bea38f7956ff115d63791fd65079b0c196054f13c1181ab8f7e5e64fbeda`.

## Resultado com leitura real de payload
- `api_version=v2-candidate`, `publication_qa=not_evaluated`, `source_snapshot_qa=candidate`.
- 645 municípios, 13 universos, 75 variáveis publicáveis, 174.795 observações.
- 48 variáveis com `cautelas` em branco no catálogo; 17 identificadores percentuais com `scale_verified=false` no readiness.
- `universes/RM_JUNDIAI/context.json` está presente no ZIP.
- Em `catalog/variables.json`, a chave identificadora é `variavel_id`. Em `qa/readiness.json`, a chave é `variable_id`: consumidores precisam adaptar explicitamente essa diferença; não assumir homogeneidade de esquema.
- `storage_scale=nao_documentada` e `display_multiplier=null` aparecem nos percentuais ainda não certificados.
- A checagem verificou conteúdo e coerência das contagens específicas; **não** executou o script recém-integrado `editorial/audit_v2_editorial_ready.py`, porque o ambiente local não tem acesso HTTP ao repositório. Testes do PR #200 foram aprovados em Core CI run 39166328916 e Pages Preview run 39166329082; PR #200 integrado por squash merge `a5817ab20ab3551a45753836db9c2ce68259e113`.

## Decisão
**CANDIDATO COM PENDÊNCIAS**. Uma construção privada tecnicamente consistente não autoriza divulgação nem certifica percentuais ou comparabilidade temporal. Reutilizar este snapshot como objeto de auditoria, não como fonte homologada para publicação definitiva. Para o próximo gate, aplicar o auditor efetivo ao pacote canônico, resolver 48 cautelas e 17 escalas por evidência, e só depois validar publicação/contrato público.
