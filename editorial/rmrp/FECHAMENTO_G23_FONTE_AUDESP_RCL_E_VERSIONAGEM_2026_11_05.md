# RMRP — G23 — Descoberta de fonte Audesp para conciliação RGF/RCL (05/11/2026)

## Objeto
Diligência complementar aos fechamentos G21–G22: localizar fonte oficial **independente do Siconfi** apta a examinar a divergência entre RCL municipal, dívida consolidada líquida e despesa com pessoal de **Pontal (3540200), Barrinha (3505609) e Orlândia (3534302)**. O DOCX/PDF G20 permanece intacto, sem homologação externa.

## Achado principal — base mensal de RCL do TCE-SP
Foi lido diretamente pelo Crawl2AI o índice de dados abertos do Tribunal de Contas do Estado de São Paulo:
https://www.transparencia.tce.sp.gov.br/conjunto-de-dados

Na seção **“RCL mensal”**, o TCE-SP informa:
- fonte **Audesp**, informações dos **balancetes entregues pelo município**;
- referência temporal **mensal**, desde janeiro/2015;
- frequência de atualização **semanal**;
- formato CSV;
- recurso `RCL`, atualizado em **05/11/2026**, tamanho anunciado **843,81 KB**;
- URL canônica de download: https://www.transparencia.tce.sp.gov.br/sites/default/files/conjunto-dados/rcl_completo.zip

O próprio portal adverte que a RCL foi calculada com os balancetes recebidos e que a completude de entrega dos órgãos deve ser verificada nos relatórios de remessa.

**Resultado de acesso:** descoberta e metadados da fonte **confirmados**; **bytes do ZIP e suas linhas municipais não foram recuperados nesta execução**. Download direto no contêiner falhou por DNS; tentativa de exportação pelo navegador remoto não produziu resposta utilizável. Portanto, **não foram obtidas nem atribuídas cifras do Audesp para dezembro/2025**. Quando o arquivo estiver acessível, filtrar municípios pelo código oficial e competência 12/2025, confrontando RCL do TCE-SP com a RCL do RREO B6, RGF e Diário de cada município, sem pressupor identidade de metodologia/ajustes.

## Metodologia fiscal Audesp
Também foi lido o índice de documentação técnica oficial:
https://www.tce.sp.gov.br/audesp/documentacao

Identificada página de **modelos e metodologias dos demonstrativos da LRF em 2026**:
https://www.tce.sp.gov.br/audesp/documentacao/demonstrativos-audesp-modelos-e-metodologias-demonstrativos-calculo-lrf-2026

Ela disponibiliza planilhas de modelo de **RCL**, **Dívida Consolidada Líquida** e **Despesa com Pessoal — Poder Executivo**. Esses modelos servem para documentar códigos, bases e ajustes, **não contêm, por si, os valores dos três municípios em 2025**. A URL de documentação de 2025 testada redirecionou a uma página genérica de atualização, sem modelo recuperado.

## Extrato Siconfi e limites da versionagem
Foi localizado e lido diretamente o catálogo oficial do Tesouro:
https://www.tesourotransparente.gov.br/ckan/dataset/api-extrato-entes

O catálogo descreve a API de extrato dos relatórios homologados e retificados, além de suas matrizes. A documentação disponível no catálogo registra publicação de metadados em 2019; os retornos usados nas auditorias G21–G22 contêm status `HO`/`RE` e datas, **não um histórico completo de versões protocolizadas**. Os status não autenticam a equivalência entre uma edição municipal e uma transmissão específica. Assim, a recuperação do **protocolo e da versão efetivamente entregue** continua necessária.

## Matriz de pendências resultante

| Caso | Evidência adicional em G23 | Avanço de status |
|---|---|---|
| Pontal FIS-01 — RCL/DTP | Base oficial Audesp RCL 2025 localizada, mas sem valores lidos | P0 aberto |
| Pontal FIS-02 — DCL/deduções | Modelo Audesp de DCL 2026 localizado, sem demonstrativo individual de 2025 | P0 aberto |
| Barrinha FIS-03 — RGF A02/A06 | Fonte Audesp de RCL identificada, sem PDF de RGF retificado | P0 aberto |
| Orlândia FIS-04 — DO/Siconfi | Modelos Audesp de RCL/DCL/DTP identificados, sem registros do município | P0 aberto |

## Decisão e próxima diligência
A investigação **encontrou uma nova trilha probatória oficial e específica**, mas **não solucionou nenhuma das quatro divergências numéricas**. Priorizar obtenção binária do CSV mensal `rcl_completo.zip` e leitura de RCL de dezembro/2025; simultaneamente, recuperar modelos Audesp com codificação de RCL/DCL/DTP e os protocolos transmitidos. Não alterar RGF/RSF no Volume II por presunção. Não atribuir infração ou erro a gestores, municípios, Audesp ou Siconfi sem fonte primária e contraditório.

**Referências anteriores:** [G21](FECHAMENTO_G21_CONCILIACAO_FISCAL_RGF_RREO_2026_11_05.md); [G22](FECHAMENTO_G22_DILIGENCIA_DOCUMENTAL_RGF_2026_11_05.md); [Matriz G21](G21_MATRIZ_PRIORIDADES_CONCILIACAO_RGF_2026_11_05.csv).
