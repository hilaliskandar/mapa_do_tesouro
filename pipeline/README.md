# Pipeline

O pipeline implementará os estágios lógicos definidos em `governance/METHODOLOGY.md` e produzirá a base SQLite canônica, artefatos estáticos e manifesto de build.


## Reconstrução ponta a ponta

A base analítica inicial pode ser reconstruída por:

```bash
python -m pipeline.build.build_analytical_database \
  FINBRA_TIC_TIM_30M_BASE_MULTIFONTES_2013_2025_v0_4.xlsx \
  --database data/financas_municipais_sp.sqlite \
  --overwrite
```

A sequência executada é:

```text
ingestão
→ documentação
→ agregações/indicadores anuais
→ estatísticas 2021–2025
→ tipologias transparentes
→ seis marcadores comparáveis
→ pares prioritários/recíprocos
```

A promoção para `approved` continua condicionada aos QA de paridade e à decisão metodológica sobre o agregado territorial.
