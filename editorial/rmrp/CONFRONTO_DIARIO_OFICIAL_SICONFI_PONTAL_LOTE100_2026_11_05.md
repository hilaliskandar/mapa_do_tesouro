# Lote 100 — Confronto do RGF de Pontal publicado no Diário Oficial com Siconfi

**Data da diligência:** 05/11/2026. **Objeto:** auditoria fiscal interdocumental do Volume II da Região Metropolitana de Ribeirão Preto. **Estado:** encontrado documento municipal primário que diverge materialmente do RGF 2025 informado na API federal; não há homologação da situação fiscal nem decisão de substituir um dado pelo outro.

## 1. Nova fonte primária localizada

**Pontal — Diário Oficial do Município, Ano XI, Edição nº 1.906, 18 de março de 2026, 56 páginas.** URL oficial de divulgação (Diário Oficial Eletrônico): https://dosp.com.br/exibe_do.php?i=NzkyNDYw . Foi localizado por busca web e lido por extração textual da edição. **Página impressa 22/56:** RGF — Anexo 1 (Despesa com Pessoal, Poder Executivo), período janeiro a dezembro de 2025. **Páginas 14 e seguintes:** outros anexos RGF; **páginas 33–37:** RREO de 2025, contendo RCL e seus ajustes. Na tentativa de screenshot do PDF pela ferramenta web houve **cache miss**; os valores a seguir provêm de extração textual com página impressa e contexto da rubrica, e a validação visual do PDF oficial é recomendada antes da homologação.

O demonstrativo municipal publicado no RGF Anexo 1, **página 22**, registra:
- Receita Corrente Líquida (RCL): **R$ 209.571.785,24**.
- RCL ajustada para pessoal: **R$ 209.261.592,13**.
- Despesa Total com Pessoal: **R$ 101.819.534,91**.
- DTP / RCL ajustada: **48,66%**.
- Limite máximo de pessoal informado: **54,00%**.

A publicação municipal informa também RCL **R$ 209.571.785,24** em outros demonstrativos do mesmo exercício, inclusive RREO e RGF Anexo 3 (Garantias e Contragarantias). **Existe consistência interanexos quanto à RCL no documento municipal recuperado.** Isso não garante identidade com a declaração posterior transmitida ao Siconfi.

## 2. Confronto com a API oficial Siconfi

Fonte Siconfi RGF Q3/2025, Executivo, Anexos 01 e 06, município código IBGE **3540200**:
https://apidatalake.tesouro.gov.br/ords/cdwhprd/siconfi/tt/rgf?an_exercicio=2025&in_periodicidade=Q&nr_periodo=3&co_tipo_demonstrativo=RGF&no_anexo=RGF-Anexo%2006&id_ente=3540200&co_poder=E

Verificações repetidas nos Lotes 92, 97 e 99 registraram:
- RCL declarada no RGF Q3/2025: **R$ 13.494.039,69** (e RCL ajustada para pessoal na mesma magnitude).
- Despesa Total com Pessoal no Anexo 06: **R$ 108.682.695,50**.
- DTP/RCL ajustada: **805,41%**.
- DCL/RCL ajustada: **1.333,33%**.

A API RGF Anexo 01 também retorna **R$ 13.494.039,69** como RCL de cálculo, confirmando que a divergência não está limitada ao extrator do Anexo 06. O **RREO Anexo 03 do 6º bimestre de 2025 da própria API Siconfi** informa RCL **R$ 209.571.785,24**, coincidente ao centavo com a edição municipal.

| Indicador, 2025 | Diário Oficial de Pontal 18/03/2026 (RGF A01) | Siconfi RGF Q3/2025 | Diferença / observação |
|---|---:|---:|---|
| RCL | R$ 209.571.785,24 | R$ 13.494.039,69 | R$ 196.077.745,55 |
| RCL ajustada para pessoal | R$ 209.261.592,13 | R$ 13.494.039,69 | R$ 195.767.552,44 |
| DTP | R$ 101.819.534,91 | R$ 108.682.695,50 | R$ -6.863.160,59 |
| DTP/RCL ajustada | 48,66% | 805,41% | Duas bases e numeradores distintos |

**Observação essencial:** esta evidência muda o diagnóstico de “divergência de denominador” para **divergência entre versões/documentos de RGF com numerador de pessoal também diferente**. Não afirmar que a publicação municipal representa a “retificação correta” ou que o Siconfi contém erro imputável ao órgão responsável: houve publicação municipal em **18/03/2026**, mas o registro anterior de extrato Siconfi do RGF Q3/2025 indica entrega/homologação em **03/04/2026**. **A cronologia sugere versões ou processamentos diferentes**, ainda não esclarecidos por termo de retificação, protocolo de envio, histórico de versões e manifestação do ente.

## 3. Restrição jurídica e de interpretação

O índice **48,66%** publicado no Diário Oficial seria superior ao patamar geral de alerta de pessoal do Poder Executivo (48,6%), mas inferior ao prudencial (51,3%) e máximo (54%). **Esta é apenas a interpretação aritmética condicional dos valores publicados**, e não um parecer de enquadramento legal, pois as versões precisam ser conciliadas e conferidas quanto aos ajustes e à abrangência institucional.

O índice de **805,41%** do Siconfi não pode ser adotado para afirmar infração, dadas as discrepâncias diretas com outros documentos oficiais. Nem o índice do Diário Oficial deve ser substituído automaticamente na base consolidada. **Manter Pontal em quarentena até auditoria de versões.**

Para dívida, permanece pendência adicional: a diferença entre o DCL reportado no Siconfi Q3/2025 e outros relatórios municipais não foi reconciliada neste lote; não converter dados do RREO de resultado nominal automaticamente em RGF Anexo 02.

## 4. Pesquisa dos outros dois municípios

Foram identificadas páginas oficiais relevantes para buscar documentos publicados:
- **Orlândia:** portal municipal https://www.orlandia.sp.gov.br/novo/transparencia e seção Contas Públicas https://www.orlandia.sp.gov.br/novo/servicos/contas-publicas ; fonte de transparência indicada pelo próprio município inclui sistema Betha. A página institucional foi recuperada pelo Crawl2AI, mas **ainda não foi localizado e lido o PDF do RGF do Executivo de 2025–2026 que permita confronto oficial com a API**.
- **Barrinha:** acesso do município ainda carece de identificação positiva de publicação executiva em PDF. A Câmara Municipal possui portal de transparência em https://www.barrinha.sp.leg.br/transparencia, mas **não substitui o RGF do Executivo**; não atribuir ao município documentos do Poder Legislativo.

## 5. Próxima diligência prioritária

1. Recuperar a **versão oficial publicada de Pontal do RGF Anexo 02 e Anexo 06** com numerador de dívida e RCL e conferir se houve edição municipal anterior/posterior à edição 1906 de março.
2. Obter o histórico completo de entregas/retificações do Siconfi (protocolo, data de aceite e versão) do RGF Q3/2025 de Pontal, confrontando temporalmente com Diário Oficial de 18/03/2026.
3. Localizar documentos RGF do Executivo publicamente disponíveis de **Barrinha (2025 S2 e 2026 S1)** e **Orlândia (2025 S2 e 2026 S1)**, sem confundir com RGFs do Legislativo.
4. Manter o controle intertemporal do Lote 99 e anexar matriz fonte-versão-período-valor, sem substituir indicadores LRF no Volume II.
5. Os arquivos editoriais DOCX/PDF do **Lote 98, 66 páginas**, permanecem **intocados** enquanto não houver saneamento documental.

## 6. Limite da diligência

Localização e leitura textual de fonte municipal primária nova em 05/11/2026, confronto com Siconfi e indicação de cronologia. **Não houve auditoria pericial de assinatura do PDF, download binário do RGF municipal ou inspeção visual da página 22**, pois screenshot web retornou cache miss. O texto extraído e o índice da publicação sustentam os valores acima, mas o controle final da edição requer validação visual e versões protocolizadas. Não se afirma culpa, falsidade, descumprimento de LRF nem homologação definitiva.
