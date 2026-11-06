# RMRP — G21 — Pendências fiscais RGF/RREO (05/11/2026)

**Objeto:** reabertura dos controles Lotes 99, 101, 102, 103 e 104; análise dos documentos disponíveis sem edição do Volume II G20 ou da base Lote 98.

## Resultado auditável
As planilhas `CONTROLE_EXCECOES_RGF_LOTE99.xlsx` e `PONTAL_RECONCILIACAO_COMPONENTES_RGF_LOTE104.xlsx` foram efetivamente reabertas. A primeira contém sete registros de combinações exercício–período e quinze fontes STN; a segunda, componentes da dívida de Pontal e fontes. Foram produzidos **21 testes aritméticos** de razões/denominadores, com `decimal.Decimal`, preservando os valores declarados. Os testes que empregam RCL bruta são **apenas controles de plausibilidade**, não substitutos normativos da RCL ajustada.

### Pontal (3540200)
- RGF Q3/2025: RCL R$ 13.494.039,69; DTP R$ 108.682.695,50 (805,41% declarado); DCL R$ 179.919.782,20 (1.333,33% declarado).
- RREO B6/2025 e saldo anterior da RCL em RGF Q1/2026: R$ 209.571.785,24, diferença **R$ 196.077.745,55**, sem conciliação de versões.
- Dívida bruta idêntica no fechamento e na abertura: R$ 173.246.915,32. Disponibilidade de caixa bruta em 2025: **R$ 28.138.160,11**; rubrica ausente no retorno da coluna histórica de 2026.
- Deduções: −R$ 6.672.866,88 em 2025 e −R$ 34.811.026,99 na coluna anterior de 2026; diferença de **R$ 28.138.160,11**. DCL: R$ 179.919.782,20 versus R$ 208.057.942,31, diferença igual ao mesmo valor. A identidade é reproduzida ao centavo, mas **não comprova preenchimento errado nem retificação**.
- **Bloqueio P0:** sem versão protocolizada, memória de deduções e explicação da divergência RCL, não homologar índices 2025 Q3 para juízo de conformidade LRF.

### Barrinha (3505609)
- S2/2025: A02 DCL R$ 42.986.801,45, RCL ajustada para endividamento R$ 161.507.819,10, razão **26,62%**; A06 registra **31,40%**. Diferença não sanada por denominador observado.
- S1/2026: A02 DCL **positiva R$ 712.553,65** e razão 0,41%; A06 conserva 0,41%, mas informa linha monetária de DCL **−R$ 19.085.508,85**.
- Extrato STN do S2/2025 registra status `RE`, sem histórico de versões recuperado. PDF municipal encontrado no índice tem nome de “2º quadrimestre”, insuficiente para comprovar identidade com demonstrativo simplificado semestral.
- **Bloqueio P0:** documento Executivo correspondente, versão retificada e componentes de cálculo pendentes.

### Orlândia (3534302)
- S2/2025: A02 DCL **−R$ 17.264.485,35**, razão **−6,55%** com RCL ajustada de dívida R$ 263.501.501,04; A06 **−6,59%** é aritmeticamente compatível com RCL de pessoal R$ 261.870.013,04. Compatibilidade aritmética não equivale a conformidade normativa.
- Jornal Oficial nº 2238, **29/01/2026, p. 5**, registra DCL **−R$ 19.720.109,67** (−7,48%) e DTP **R$ 139.863.791,37** (53,40%), versus DCL **−R$ 17.264.485,35** e DTP **R$ 139.797.400,92** (53,38%) na API. Diferenças monetárias de R$ 2.455.624,32 (módulo DCL) e R$ 66.390,45 (DTP). Publicação textual oficial novamente localizada em https://www.dosp.com.br/exibe_do.php?i=NzY5NTky ; captura visual da página PDF falhou por cache.
- S1/2026: A02 DCL **−R$ 18.765.801,54** (−6,92%); A06 **−R$ 24.285.593,30** (−7,49%). Há divergência de numeradores, não explicável só pelo denominador.
- **Bloqueio P0:** extrato de versões STN, publicação original/Audesp, conciliação de numeradores e notas explicativas pendentes.

## Revisão do Volume II G20
Os parágrafos 12, 94, 309 e 320 já consignam a segregação dos casos, distinguem cobertura RGF de homologação de percentuais e evitam juízos de solvência ou descumprimento LRF. Os valores anômalos não foram empregados nesses trechos para conclusão legal. **Nenhuma edição do DOCX é indicada com os elementos atuais.**

## Deliberação
G21 **aprova a reexecução aritmética delimitada**, não a conformidade fiscal das declarações. Preservam-se as quatro pendências FIS-01 a FIS-04 da matriz anterior e os limites de divulgação do G20. Não se atribuem infrações ou erros a agentes sem manifestação e provas de versões.

**Arquivos locais reproduzíveis:** `RMRP_G21_PACOTE_CONCILIACAO_FISCAL_2026_11_05.zip`, com relatório integral, CSV de 21 razões, matriz de diligências, QA JSON e script.

### Evidências históricas
- [Lote 99](AUDITORIA_INTERTEMPORAL_RGF_LOTE99_2026_11_05.md)
- [Lote 101](CONFRONTO_RGF_PUBLICADO_ORLANDIA_PONTAL_LOTE101_2026_11_05.md)
- [Lote 102](CRONOLOGIA_SICONFI_PORTAL_BARRINHA_LOTE102_2026_11_05.md)
- [Lote 103](CONCILIACAO_SALDOS_RGF_PORTAL_BARRINHA_LOTE103_2026_11_05.md)
- [Lote 104](COMPONENTES_DEDUCOES_PONTAL_RGF_LOTE104_2026_11_05.md)
