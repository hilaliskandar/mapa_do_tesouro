# Validação de paridade municipal e regional — 16/10/2026

O PR #198 passou a executar `editorial/multiuniverso/qa_paridade_municipal.py`, confrontando valores municipais observados nos JSONs `municipalities/{codigo_ibge}.json` com contagens, medianas e somas publicadas nos respectivos `context.json`. A comparação usa tolerância absoluta de R$ 0,011 e relativa de 1e-9 para arredondamentos e representação numérica. A regra não imputa observações ausentes.

A execução https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38895136490, commit `58d12ccadfb222fef0ec571193c66c266650b8a6`, concluiu `success`, incluindo esta paridade, estrutura, dicionário, rastreabilidade e QA navegador. O arquivo `qa_paridade_municipal.json` preserva os resultados por universo. Artefato ZIP ID `12043537308`, SHA-256 `e0c87a520a26fe0b7220485c5623e01fab5063305c33c80208fea73daf30190f`.

**Limite de evidência:** a prova valida consistência interna do contrato editorial e não faz conferência documental independente com o arquivo bruto Siconfi/DCA/RGF/RREO ou extratos originais do Tesouro. Não se declara homologação externa dos valores oficiais. Não houve merge do PR #198 nem publicação em produção.
