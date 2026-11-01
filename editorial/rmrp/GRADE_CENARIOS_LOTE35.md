# Lote 35 — grade executável de cenários 2027–2030

**Data:** 01/11/2026. **Estado:** grade e verificação local concluídas; projeções numéricas futuras deliberadamente nulas. **Fonte:** DCA SP645 original já arquivada (Drive `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`), cadastro territorial `editorial/rmrp/municipios_subregioes_tcesp.csv`, IPCA mensal arquivo `tabela1737.xlsx` Drive `1ZzuDCnZC1X13f51XzsyJ34dH8dDLxp2Z`.

## Artefatos gerados

- `grade_municipal_408_lote35.csv`: 34 municípios × 4 anos de 2027 a 2030 × três cenários (adverso, continuidade, favorável), chave única município-ano-cenário, com variáveis-base observadas em 2025 e parâmetros futuros em branco.
- `agregados_60_lote35.csv`: quatro sub-regiões e total RMRP para cada ano e cenário, reconstruídos a partir da grade municipal.
- `modelo_cenarios_rmrp_lote35.xlsx`: planilha com abas municipais, agregados e LEIA_ME.
- `QA_LOTE35.json`: teste de cardinalidade, cobertura, fator e conciliação, com resultado PASSOU.
- `gerar_grade_cenarios_lote35.py`: gerador reproduzível para as fontes arquivadas.

O pacote ZIP com os cinco arquivos foi gerado no ambiente da conversa: `pacote_lote35_cenarios.zip`. **A existência do pacote local não comprova depósito no GitHub ou no Drive.** A documentação deste lote está persistida neste arquivo.

## Resultado da auditoria

- Cadastro: 34 municípios, Sub-região de Ribeirão Preto (15), Sub-região de Jaboticabal (6), Sub-região de Mococa (6), Sub-região de Batatais (7).
- 408 chaves municipais distintas, sem duplicação; 60 recortes agregados, sem duplicação; soma de quatro sub-regiões igual ao total metropolitano nos campos de cobertura integral.
- Cobertura das seis bases monetárias DCA 2025: 34/34 municípios cada uma (receita corrente, receita tributária, FPM, despesa corrente liquidada, pessoal e encargos liquidados, investimento liquidado).
- Fator 2025 de atualização para setembro/2026 a partir de média dos índices mensais: `1,0541003834032834`.
- Campos futuros sem fonte verificada: 100% vazios, sem zeros de preenchimento; nenhuma anualização dos dados parciais de 2026.
- **Limite:** não houve reconciliação de premissas de RGF/RREO, passivos e carteira de capital neste lote; os cenários permanecem condicionais, não projeções homologadas.

## Próximo gate

Persistir os CSVs e a planilha em acervo permanente; povoar de maneira auditada hipóteses e fontes da carteira de projetos, transferências e RGF/RREO; elaborar testes de sensibilidade. Não confundir quocientes contábeis com DTP/RCL legais nem atribuir automaticamente restrições municipais ao arcabouço federal.
