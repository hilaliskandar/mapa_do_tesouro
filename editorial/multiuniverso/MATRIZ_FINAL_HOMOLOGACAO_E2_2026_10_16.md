# Matriz final de homologação editorial E2 — 16/10/2026

| Frente | Evidência | Resultado | Decisão |
|---|---|---|---|
| DCA 2025 independente | Siconfi, cinco sentinelas; run 38896144224 | 68 cotejos, zero diferenças | Aprovado no recorte |
| RGF 2023–2024, integração | Gate E SHA fixo; build privado 38905063653 | 3.068 monetários observados; 802 ausentes, sem imputação | Aprovado na base privada |
| RGF Gate E versus API E2 privada | Run 38906383979 | 2.742 numéricos, zero divergência; zero conflitos de disponibilidade | Aprovado |
| RREO 2025, Anexo 03, sexto bimestre | Gate C 37728745160 versus SQLite privado | 531 observados, 114 ausentes; zero divergência | Aprovado no recorte |
| CAPAG classificação oficial | posição setembro/2026, ano-base 2025, SHA 1b1379a5... | 645 municípios, zero divergência individual; n.d. preservado | Aprovado na classificação |
| CAPAG indicadores 1, 2, 3 | XLSX oficial setembro/2026 × SQLite privado; auditoria documentada | 1.909 valores e 26 ausências idênticos, zero divergência | Aprovado no recorte |
| Demais anos/anexos RREO e RGF | Fora dos recortes confrontados | Não aferidos | **Não afirmar homologação** |
| API E2 × SQLite privado | Build 38905063653 | 1.722 registros E2 monetários históricos coerentes | Aprovado no recorte |
| Editorial E2 | Run 38909719070 | 10 boletins, 280 fichas, QA e navegador verdes | Aprovado tecnicamente |
| Publicação das fontes | Gerador alimentado por file:// em CI, links removidos dos HTMLs | Ainda sem URL canônica pública da API privada | **Bloqueado para release** |
| Proteção do portal atual | PR 198 sem merge/deploy | Portal e RMJ preservados | Manter |

## Regras de transição
1. Preservar a homologação individual CAPAG 1–3 e seus arquivos-fonte com SHA; testar novamente em qualquer nova reconstrução. Não confundir as duas tabelas da aba `Prévia da CAPAG`.
2. Criar pacote de pré-publicação com API e HTMLs com referência versionada idêntica, manifestos, hashes e links públicos funcionais; homologar sem sobrescrever o domínio atual.
3. Concluir revisão de segurança e acessibilidade, garantir reversão e somente publicar mediante decisão explícita.
4. Não ampliar a afirmação de aderência externa além dos campos efetivamente testados.

As aprovações referem-se a resultados da etapa candidata, não a uma liberação de produção.
