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
