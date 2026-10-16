# Homologação RGF Gate E versus API editorial privada — 16/10/2026

O confronto agora usa somente a API reconstruída privada proveniente da execução `38905063653`, cujo relatório de integração registra `changed=3068` e `reclassified_absent=802`. A fonte histórica é o CSV Gate E validado, SHA-256 `7faef8188fd56bff6bb8031dfe3a8eeec11fe56e67f986bdc0007aee7646eeb` (a verificação de SHA efetiva é feita pelo workflow; conferir valor completo no código do workflow).

A auditoria `38906383979` terminou com conclusão **success**. Artefato `qa-rgf-gate-e-api-e2`, ID `12047529149`. O relatório `qa_rgf_api_e2.json` apresenta:
- 2.742 comparações entre dois valores numéricos na mesma escala;
- zero divergências numéricas;
- zero conflitos de disponibilidade;
- `missing_reasons={}`.

A metodologia compara valores oficiais do histórico aprovado com a API E2 privada e distingue ausências sem imputação. As contagens incluem repetições de códigos municipais pertencentes a múltiplos universos; não equivalem a municípios únicos. Os percentuais legais são convertidos de fração para pontos percentuais apenas no cotejo.

**Situação:** Gate de paridade histórica RGF aprovado para a API privada corrigida. Isso não certifica, por si, RREO, CAPAG ou publicação externa. Antes de publicar os boletins, revisar URLs e fontes acessíveis; para artefatos de homologação, links locais `file://` foram substituídos por identificação textual, não por links falsos para a API pública antiga. O PR #198 permanece sem merge e sem deploy.
