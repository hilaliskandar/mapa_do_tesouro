# Inventário canônico

Atualizado em 2026-10-08.

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

- DCA I-C;
- DCA I-D;
- DCA I-E;
- retries exponenciais;
- preservação de artefatos brutos;
- manifestos;
- hashes;
- normalização estadual;
- clientes iniciais para RREO/RGF.

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

## Pendências estruturais

1. integrar RREO estadual com QA;
2. integrar RGF estadual com QA;
3. integrar CAPAG;
4. consolidar denominadores anuais complementares;
5. recalcular indicadores derivados e legais;
6. recalcular tipologias e pares por `universo_id`;
7. produzir cartografia estadual canônica;
8. executar paridade completa contra TIC-TIM 30;
9. criar release estadual somente após aprovação multifuentes.
