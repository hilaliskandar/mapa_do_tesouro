# FED05 — primeira prévia estática da API v3 de investimentos RMRP

**Data da execução:** 15/11/2026. **Status:** pacote de prévia privado preparado, **não publicado e não homologado como investimento executado**. **Fonte:** SQLite de desenvolvimento `RMRP_FED04A_STAGING_2026-11-15.sqlite`, SHA256 `3bc6248e547e255639691671d69ec922b26c79fe6ec9d9b1852908d5f33212f6`. A tentativa de consultar diretamente a API nacional Transferegov por DNS no container continuou indisponível. A preparação de FED05 não substitui FED03C nem FED04B.

## Produto

A rotina reproduzível `build_rmrp_fed05_preview.py` gerou 56 JSON da API estática no prefixo `data/api/v3/investimentos/rmrp/`, contendo:
- `manifest.json` com versões, cobertura e restrições;
- `municipios.json` com as 34 entradas e respectivas coberturas;
- 34 arquivos `municipios/{IBGE7}.json` com propostas, convênios, obras vinculadas a proponentes, classificações declaradas de parcerias e desembolsos brutos **rotulados** por ano;
- 19 arquivos `anos/{ano}.json` para a série 2008–2026 de desembolsos brutos ao convenente;
- `pendencias.json` com critérios que impedem publicação como investimento executado.

Os valores mantêm inteiros de centavos, exclusivamente no estágio de desembolso ao convenente, e não são somados aos investimentos municipais. Projetos são etiquetados pelo município **proponente** e a localização física permanece `nao_comprovada`. A natureza declarada da proposta de Parcerias não homologa o pagamento correspondente.

## QA automático realizado

- 34 municípios identificados e todas as chaves de município das seis entidades contidas nesse universo;
- contagens conservadas: 6.410 propostas, 1.793 convênios, 2.537 desembolsos, 1.240 vínculos de emendas, 218 projetos Obrasgov, 743 propostas de Parcerias; 218 registros adicionais de evidência territorial (tabela auxiliar, não projetos adicionais);
- contagens municipais agregadas coincidem exatamente com as tabelas SQLite;
- contagem anual de desembolsos = 2.537, soma bruta = **71.498.911.447 centavos**, valor ainda não conciliado com estornos/devoluções;
- `PRAGMA integrity_check=ok`, 0 violações FK;
- `public_release_authorized=false` no manifesto; nenhum deploy ou escrita na base produtiva.

## Persistência

[Pacote privado FED05 — ZIP contendo JSON, QA e script reprodutível](https://drive.google.com/file/d/1RVeCJwRJmaHuZBFrV4b6qIehcLfVYTzb/view), ID `1RVeCJwRJmaHuZBFrV4b6qIehcLfVYTzb`, 446.529 bytes, pasta `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`, verificação de metadados `shared=false` e pasta de destino correta. SHA256 do ZIP original local: `3fb737777f2e5a0b7695f9d7700e47c49ec32e46b085688a4322659d51830ffa`. O arquivo foi recuperado do Drive após upload: SHA256 remoto idêntico ao original local (`3fb737777f2e5a0b7695f9d7700e47c49ec32e46b085688a4322659d51830ffa`) e teste CRC integral do ZIP aprovado.

## Próximos gates

**FED03C:** executar o reconciliador em runner com acesso ao catálogo oficial e ZIPs nacionais `siconv_pagamento`, `siconv_obtv_convenente` e `siconv_dl`, filtrados por instrumento e com auditoria de cardinalidade; preservar dados no Drive/R2 privados. **FED04B:** inspecionar `siconv_coordenadas_obra`, relacionar via `ID_PROPOSTA` e comprovar localização física por interseção com polígonos oficiais. **FED06:** comparar contrato dos JSON e testar o painel em preview isolado, depois de aprovação da classificação e dos vínculos; não implementar mapa com pontos presumidos.
