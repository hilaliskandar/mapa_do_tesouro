# Expansao editorial multiuniverso — plano E2
Data: 2026-10-15
Estado: inicio de implantacao; nenhuma publicacao adicional autorizada ou realizada neste documento.

## Ponto de partida
RM_JUNDIAI possui boletim independente em https://financas-rmj.pages.dev, HTML em editorial/rmj/index.html, dados TCESP 2023–2025 e QA documentados. A edicao publicada nao deve ser sobrescrita ou usada como fonte de valores de outro universo.

API editorial v1: 11 universos, dos quais RM de Jundiai ja tem boletim. O portal analitico tem 13 universos, numero distinto da camada editorial.
Fonte do contrato: governance/PUBLICATION_API.md; release governance/RELEASE_NOTES_V0_4_0.md.

## Ordem de expansao proposta
1. RM Campinas (proxima prova de replicacao).
2. RM Piracicaba.
3. RM Sorocaba.
4. RM Sao Paulo, 38 municipios, excluida a capital editorialmente.
5. RM Baixada Santista.
6. RM Vale do Paraiba e Litoral Norte.
7. RM Ribeirao Preto.
8. RM Sao Jose do Rio Preto.
9. AU Franca.
10. Cidades Medias, 33 municipios e sobreposicoes mantidas.

Essa ordem e uma prioridade editorial, nao decorre de hierarquia de desempenho dos municipios.

## Trilha comum de geracao
- Validar indice e contextos de universo/municipio da API editorial publicada, incluindo publication_id, member_count, cobertura, years e build.
- Gerar a edicao de referencia a partir de contexto JSON, com estrutura de panorama, receitas, despesas, investimentos, territorio, divida/liquidez/CAPAG, heterogeneidade e fichas municipais.
- Reaproveitar layout, navegacao, linguagem publica, exportacoes e controles comprovadamente gerais do boletim RMJ. Nao copiar valores ou narrativas especificas da RMJ.
- Distinguir DCA/FINBRA, RGF, RREO e CAPAG. Nao inferir ausencia como zero; nao usar proxy para indicadores legais; nao tomar soma incompleta como total regional.
- Detalhamento TCESP por programa/acao: modulo opcional por universo, somente com extratos efetivamente recuperados, conciliados e considerados relevantes. Nao condicionar edicao fiscal basica a novas coletas de TCESP para todos os territorios.
- Usar identificadores estaveis; suportar a sobreposicao intencional de municipios entre grupos.
- Separar no produto publico texto interpretativo e fontes compreensiveis de logs, hashes, CI e metainformacao interna.

## Gates de aceite
E2-A contrato e cobertura: indice/JSON acessiveis e validados; totais e denominadores auditados.
E2-B modelo parametrizado: nenhum nome ou dado RMJ residual; conteudo de cada universo provido por dados validados.
E2-C regressao: verificar que RMJ e plataforma SP645 permanecem intactos; HTML/JS e navegador desktop/mobile.
E2-D deploy isolado: publicar preview separado, conferir recursos externos e exportacoes; promover apenas com QA completo.
E2-E edicao final: linguagem publica e interpretacoes revisadas; manter manifesto interno, commit e rollback.

## Pendencia inicial concreta
Recuperar o indice de publicacao da API com evidence de conteudo (a consulta web direta nao o entregou neste ambiente). Alternativa: artefato v0.4.0 do GitHub Actions ID 11610521760 com SHA-256 3052e27b68f34d61df878ee4af43886453784e09e99ec07f5459fdec3c566b7e, ja auditado no piloto. Nao inventar publication_id nem cardinalidades por universo antes da leitura do indice.

O inicio da RM Campinas pode gerar template parametrico e teste de contrato sem tocar producao. A publicacao final depende da validacao dos JSONs e testes.
