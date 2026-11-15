# FED03C/FED04B — preparo operacional de execução dos ZIPs nacionais

**15/11/2026 — execução verificável.** Foram inspecionados diretamente o SQLite de desenvolvimento `RMRP_FED04A_STAGING_2026-11-15.sqlite` e os ZIPs regionais `RMRP_Transferegov_Aquisicao_2026-11-15.zip` e `RMRP_Obrasgov_2026-11-15.zip`. O ZIP regional Transferegov contém 89 membros (cobertura de 34 municípios, consultas municipais e 4 CSV regionais), **não contém** `siconv_pagamento`, `siconv_obtv_convenente`, `siconv_dl` ou `siconv_coordenadas_obra` nacionais. Os arquivos detalhados devem ser baixados separadamente em ambiente com acesso ao repositório oficial.

## Resultado operacional desta rodada

1. Verificada em SQLite a existência das tabelas de propostas, convênios, desembolsos, emendas, projetos por proponente, natureza proposta de Parcerias e evidência de localização. A base de convênios possui **1.793 identificadores**, a base territorial RMRP34 está preservada.
2. Confirmado novamente que o container executor não resolve `api-publica.transferegov.gestao.gov.br` ou `repositorio.dados.gov.br` por DNS (`Temporary failure in name resolution`). Isso não significa indisponibilidade institucional das fontes. A página governamental [API de Dados Abertos Transferegov](https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br) confirma a nova área de download Discricionárias e Legais. O [aviso do Obrasgov](https://www.gov.br/obrasgov/pt-br/noticias/2026/comunicado-23-2026-mudancas-nos-acessos-as-apis-de-dados-abertos-do-transferegov-br-e-do-obrasgov-br) descreve a transição.
3. Reutilizado `fed03c_reconcile_local.py` e implementado `fed04b_coordinates_local.py`. O segundo leitor importa apenas coordenadas de propostas `ID_PROPOSTA` presentes na base local, registra vínculos candidatos com convênios e classifica latitude/longitude como candidata, ausente ou inválida, **sem atribuí-las aos projetos Obrasgov** ou publicá-las no mapa.
4. Novo `test_reconciliadores.py` constrói uma base e CSVs sintéticos, testa um pagamento com **duas linhas filhas OBTV** e um documento DL (sem somar novamente o pagamento), além de coordenadas válidas, ausentes e inválidas. Ambos os testes passaram, com `integrity_check=ok` e nenhuma violação FK.
5. Testes sintéticos não constituem observações reais de recursos ou de obras no território da RMRP. Nenhuma linha nacional de pagamento/OBTV/DL ou coordenadas novas foi adquirida neste turno. **FED03C e FED04B continuam parcialmente preparados, não homologados**.

## Pacote de execução

[Download privado no Drive — RMRP_FED03C_FED04B_RUNNER_2026-11-15.zip](https://drive.google.com/file/d/1JgQksYyudLpszduwiR26gvLeixugdSHk/view); ID `1JgQksYyudLpszduwiR26gvLeixugdSHk`, pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`. Contém scripts Python, teste sintético autocontido e README com comandos de execução local. Após upload, leitura de metadados confirmou 8.148 bytes e `shared=false`; download de conferência retornou mesmo tamanho e hash SHA-256 `3d100985d832c74239ac907b458e869beaa6be4c505447cbe376d6368102e5ff`, CRC íntegro.

## Próximos requisitos de aceite

- Executar em runner com DNS e HTTPS verificados, usando snapshot oficial identificado por data, hash, ETag/Last-Modified quando disponíveis, sem divulgar microdados nacionais no GitHub.
- Em FED03C, conferir `NR_MOV_FIN` único em pagamentos, a cardinalidade 1:N dos registros OBTV, `ID_DL`, estornos e valores sem somar eventos de estágios distintos. A classificação GND4 paga depende de ponte documental adicional; não equiparar desembolso ao convenente a gasto executado.
- Em FED04B, cruzar coordenadas de propostas com limites municipais oficiais EPSG:4674; confrontar chaves de instrumentos e CIPI com Obrasgov. Não usar sede do proponente para inferir local de execução.
- Atualizar manifestos em Drive/R2 e reexportar JSON da prévia privada; manter `public_release_authorized=false` até homologação financeira, territorial e funcional.

**Nada foi implantado no site público nesta rodada.**
