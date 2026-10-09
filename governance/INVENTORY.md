# Inventário canônico

Atualizado em 2026-10-09.

## Núcleo aprovado

### Dados e modelo

- schema SQLite versionado;
- modelo longo de observações;
- estados `observado`, `ausente`, `nao_aplicavel` e `em_revisao`;
- tabelas de proveniência;
- crosswalk temporal;
- cobertura;
- documentação de variáveis e seções metodológicas;
- estatísticas de janela;
- classificações relativas;
- pares municipais.

### Baseline TIC_TIM_30

- 30 municípios;
- 2013–2025;
- 75 objetos documentados;
- 29.250 observações após derivados na build de referência;
- 870 pares dirigidos;
- 30 geometrias;
- regra territorial `strict_complete`;
- paridade documentada contra painel v7 e Bloco 3;
- releases v0.1.0 e v0.1.1;
- produção e preview no Cloudflare Pages.

### Frontend

- Panorama;
- Perfil/seleção municipal;
- séries históricas;
- comparação;
- mapa temático;
- análises de receitas;
- despesas e investimento;
- território;
- dívida e liquidez;
- CAPAG;
- catálogo de contas e agregações;
- indicadores;
- crosswalk;
- fontes e cobertura;
- metodologia;
- modal “Como ler”.

### CI/CD

- Core CI;
- preview automático;
- QA remoto;
- promoção controlada de produção;
- smoke estadual Siconfi;
- crosscheck Siconfi versus baseline;
- piloto SP 645;
- contrato de snapshot privado.

## Expansão SP_645

### Piloto validado

- 645 municípios;
- 2020–2023;
- 2.580 município-ano;
- 5 variáveis de receita;
- 12.900 observações;
- 12.900 registros de proveniência;
- snapshot comprimido no R2 privado;
- SHA-256 comprimido: `3f5ebf5a6482b7627cd2c1bd121c722e53e2632fed2340ae5ccae7e02290088a`;
- objeto: `sp_645/pilot_2020_2023/snapshot.csv.gz`.

### Aquisição direta disponível

- DCA I-C, I-D e I-E;
- RREO Anexo 03 / RCL anual;
- RGF Anexos 01 e 05 com normalização legal;
- RGF Anexo 02 em formato longo;
- retries exponenciais;
- preservação de artefatos brutos;
- manifestos;
- hashes;
- normalização estadual;
- execução RGF shardada de contingência;
- QA estadual automático pós-run.

## Decisões consolidadas

- `despesa_territorial = strict_complete`;
- fórmula parcial territorial é apenas `legacy_partial`;
- DTP/RCL, DC/RCL e DCL/RCL permanecem oficiais, não proxies;
- cobertura é variável a variável;
- flags estruturais legadas não provam completude;
- Engenheiro Coelho/2024 permanece ausente em DCA;
- `dca_fpm_cota_mensal` significa cota mensal e exclui cotas extraordinárias.

## Material legado relevante

- aplicação Streamlit;
- normalização histórica;
- hierarquia contábil;
- mapa semântico;
- agregações semânticas;
- cartografia histórica;
- testes de reconciliação;
- painéis HTML anteriores;
- v7 e Bloco 3 como baselines analíticos/documentais.

## Ramos superados encerrados

Os PRs #18 e #20 foram encerrados sem merge porque suas funções foram substituídas pela linha posterior já integrada à `main`.

## Gate B DCA concluído

- 645 municípios;
- 2013–2025;
- 8.385 município-ano;
- 26 variáveis;
- zero issues de normalização;
- snapshot multianual SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`;
- arquivo canônico no Drive;
- snapshot e manifesto no R2 privado;
- fila seletiva histórica encerrada;
- ausências históricas confirmadas preservadas como ausência.

## Gate C — estado atual

### RREO 2025

- 645/645 municípios consultados;
- 531 RCL observadas;
- 114 ausências preservadas;
- zero falhas;
- zero issues de normalização;
- cobertura da variável: 82,33%;
- as 114 ausências têm RCL em outra fonte oficial, mas não são imputadas ao RREO.

### CAPAG 2025

- snapshot oficial posição setembro de 2026;
- 645/645 municípios paulistas;
- classificação oficial preservada, inclusive `n.d.`;
- suplemento local RGF/CAPAG catalogado variável a variável.

### RGF

- Anexos 01/05: carga SP645 2025 concluída em 645/645;
- zero falhas e zero issues;
- composição CAPAG fill-only validada com 366 células adicionais e zero conflitos;
- SHA-256 composto `48b50b2df44eaddc2fc1c4ed096c057c2bea5d61cb850b37dc23e6037962aa24`;
- fallback automático em cinco shards disponível;
- consolidação e QA automáticos em ambos os caminhos;
- Anexo 02: carga estadual 2025 concluída; 530 municípios observados, 43.920 linhas longas, 40 códigos de conta, zero falhas e zero conflitos; SHA-256 canônico `8e4709727aa8fbf0023056982fe7927f5bd8e323354807604dbdc2a91cf8d75a`; suplemento CAPAG fill-only adiciona 100 Dívidas Consolidadas e 114 RCL brutas, zero conflitos; composto SHA-256 `0b31196dd1a692632b7c2b48a044ed64f5f56493eb8d50f818810cdd583fc139`.

## Pendências estruturais

1. reconstruir o build privado SP645 após a correção do pós-processamento do RGF Anexo 02;
2. executar regressão final de dados e interface contra TIC-TIM 30;
3. recalcular somente indicadores, tipologias e pares afetados por novos insumos válidos;
4. fechar a documentação de cobertura multifuentes por variável e exercício;
5. validar integralmente F101–F118, inclusive mapa, exportação, crosswalk, fontes e metodologia;
6. registrar manifesto, hashes e versão da candidata estadual;
7. manter a promoção pública bloqueada até QA integral e decisão explícita de release.

## Higiene do repositório

Situação em 2026-10-09:

- issues abertas: 0;
- pull requests abertos: 0;
- PRs #96–#107 incorporados à `main`;
- nenhuma pendência conhecida depende de fechamento manual de issue ou PR;
- tarefas futuras devem nascer de `governance/PENDING_TASKS.md` e só virar issue quando houver escopo executável, critério de aceite e dependências definidas.
