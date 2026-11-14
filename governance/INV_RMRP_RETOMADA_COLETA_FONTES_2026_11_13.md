# Retomada da coleta sistemática de investimentos — RMRP

Data de registro: 13/11/2026. Escopo: 34 municípios, quatro sub-regiões, expansão futura SP645. Este documento não comprova nova ingestão ou disponibilidade pública.

## Prioridade de execução

A tarefa prioritária é recuperar dados oficiais de Transferegov, Obrasgov, Portal da Transparência federal, Portal de Convênios SP e Sefaz-SP/SIAFEM, por ingestão reproduzível e incremental, preservando snapshots nacionais/estaduais sempre que possível. A conferência IBGE7/SQLite é requisito auxiliar e não substitui a coleta.

## Reutilização obrigatória

Consultar `governance/PLANO_EXECUTIVO_INVESTIMENTOS_RMRP_PILOTO_CONSULTAS_2026_11_11.md`, `editorial/rmsjrp/discover_transferegov_g06f.py`, `editorial/rmsjrp/consultar_37_transferegov_g06f.py`, `editorial/rmsjrp/RELATORIO_G06F_APIS_TRANSFEREGOV_2026_11_09.md`, `governance/RELATORIO_FED00_INVENTARIO_2026_11_09.md` e `governance/RELATORIO_FED04_SOBREPOSICAO_FINBRA_FEDERAIS_2026_11_09.md`. Não replicar dados FPM/DCA já integrados como novas receitas.

## Ordem operacional

1. Validar contratos e campos reais das APIs; enumerar Discricionárias/Legais, Parcerias, Especiais e Obrasgov. Nos módulos sem cobertura financeira completa, capturar CSV oficial histórico e cruzar com documentos da CGU quando existir chave verificável.
2. Capturar arquivos estaduais de convênios e liberações Sefaz-SP/SIAFEM, distinguindo objeto, valor pactuado, parcela liberada, estorno e classificação econômica.
3. Persistir o bruto em R2 privado com URL, competência, carimbo de extração, checksum SHA-256, contagem e readback; registrar sucesso, vazio, erro ou cobertura indeterminada por fonte/município.
4. Normalizar IDs e relacionamentos documentados, preservando proposta, instrumento, empenho, transferência, pagamento, liquidação e execução física como fatos diferentes. Classificar capital/investimento versus custeio e indeterminado; não somar financiamento com gasto executado.
5. QA em SQLite de desenvolvimento: paginação completa, chaves estáveis, ausência != zero, N:M territorial, duplicidade e retificações; só depois construir API estática e prévia isolada.

## Verificação desta retomada

O portal oficial comunica que a API Discricionárias/Legais disponibilizou a primeira entrega (atos preparatórios) em 28/10/2026; demais módulos estão sujeitos ao cronograma de implantação, não se presumindo cobertura financeira completa. Referências: https://www.gov.br/transferegov/pt-br/noticias/noticias/2026/outubro/transferegov-disponibiliza-nova-api-de-dados-abertos ; https://www.gov.br/transferegov/pt-br/ferramentas-gestao/api-de-dados-abertos-transferegov.br ; https://www.gov.br/obrasgov/pt-br/ferramentas-de-gestao-e-transparencia/api-de-dados-abertos-obrasgov-br_novo .

As tentativas diretas desta sessão de consultar os endereços de API pelo conector Crawl2AI falharam com erro interno; a sessão de execução local também não resolveu DNS público. Verificou-se apenas informação publicada em páginas governamentais via pesquisa web, sem recuperação de novo lote de registros. Não registrar estes testes como captura de dados.

Próximo gate: executar os coletores existentes em runner com conectividade externa, iniciar por um conjunto pequeno com comprovante de paginação e hashes, expandir para todo o estado onde houver download integral, filtrar RMRP por IBGE7 e documentar cobertura real por módulo. Não alterar produção nem afirmar carga homologada sem evidência do run.

## Adendo de reconciliação com resultados anteriores (14/11/2026)

A leitura integral de `governance/INV_RMRP_REORIENTACAO_TRANSFEREGOV_INVESTIMENTOS_2026_11_12.md` identificou que o gate INV-FED00 e as junções dos arquivos nacionais **já avançaram substancialmente em 13/11**, superando a descrição preliminar acima. NÃO reiniciar essas aquisições sem justificativa.

- Run 43409135374: 288.852 linhas nacionais Convênio, 386.864 Desembolso e 298.538 Emenda.
- Run 43410911718: 1.160.558 propostas nacionais; 6.410 vinculadas a proponentes RMRP (34/34).
- Run 43411132741: junções oficiais RMRP por chaves administrativas: 1.793 linhas de convênio, 2.537 eventos de desembolso e 1.240 linhas de emenda.
- Run 43411550312: 4.917.545 itens nacionais PAD, 28.456 vinculados às propostas dos proponentes RMRP.
- Run 43411817563: 16.156 candidatos GND4, 287 GND5, 50 GND6, 11.920 correntes e 43 natureza indeterminada; SIT_ITEM aprovado 15.342, em complementação 217, vazio 12.897. Estes totais de GND e situação são distribuições marginais, NÃO uma contagem cruzada GND4 + aprovado.
- SIAFEM, 2020-12/11/2026: 238 combinações município-ano auditadas, 1.017 pagamentos e R$305.521.029,20 de liberações líquidas classificadas na consulta como investimento; não equivalem à execução municipal.

O novo arquivo `pipeline/acquire/collect_inv_rmrp_transferegov.py` e workflow `inv-rmrp-transferegov.yml` são somente instrumentos complementares de sondagem dos endpoints ainda não cobertos pelos downloads nacionais. **Não substituem** `inv_rmrp_transferegov_zip.py`, `inv_rmrp_transferegov_join.py`, `inv_rmrp_transferegov_plano.py` e os workflows existentes.

**Gate prioritário efetivo:** persistir no R2 os snapshots nacionais e filtrados com hashes e readback; produzir matriz cruzada GND4 × SIT_ITEM × localização e validar a situação jurídica dos itens; resolver 43 indeterminados e 166 registros de localização fora de SP; preservar município do proponente distinto do município executor; realizar conciliação por instrumento com os 2.537 desembolsos sem rateio por percentual presumido. Em seguida processar arquivo nacional de pagamentos/OBTV, quando disponível e contratualmente vinculado. Não criar agregados monetários de investimento executado a partir de valores de planos.
