# Requisitos funcionais iniciais

## Dados e governança

- F001 — suportar universos municipais configuráveis sem listas fixas no código.
- F002 — distinguir ausência, zero observado e não aplicabilidade.
- F003 — rastrear cada variável até fonte, exercício, estágio e regra de harmonização.
- F004 — versionar schema, dados, metodologia e aplicação separadamente.
- F005 — produzir hash da base canônica e manifesto de build.
- F006 — permitir reconstrução da base por pipeline sem edição manual.

## Interface

- F101 — panorama municipal.
- F102 — perfil municipal detalhado.
- F103 — séries históricas.
- F104 — comparação entre municípios.
- F105 — mapa temático.
- F106 — receitas e autonomia.
- F107 — despesas e investimento.
- F108 — funções territoriais.
- F109 — dívida e liquidez.
- F110 — CAPAG.
- F111 — catálogo de contas e agregações.
- F112 — catálogo de indicadores.
- F113 — crosswalk temporal.
- F114 — fontes e cobertura.
- F115 — metodologia e governança.
- F116 — exportação de recortes em formato aberto.

## Arquitetura

- F201 — operar localmente sem serviços proprietários.
- F202 — servir consultas previsíveis por artefatos estáticos.
- F203 — reservar API/banco remoto para consultas dinâmicas.
- F204 — manter integrações de provedor fora do núcleo de domínio.
- F205 — permitir implantação Cloudflare sem expor configuração operacional no repositório.

- F117 — cada indicador, conta ou agregação exibida deve oferecer acesso à sua documentação canônica: fórmula/definição, componentes, fonte, período, como ler, limitações e regra de ausência.
- F118 — a interface deve expor páginas estáveis de metodologia e dicionário, alimentadas pelo catálogo versionado e não por texto duplicado nos templates.
