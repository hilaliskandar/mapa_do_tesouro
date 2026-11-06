# RMRP — G20: revisão de homologação do Volume II (05/11/2026)

**Situação:** cópia derivada de revisão interna, **não homologada para circulação externa**. A versão-base Lote 98 permanece intacta; G19 também foi preservado. O Volume I não foi objeto de nova auditoria integral neste lote.

## Correção executada na cópia G20
A Figura F2 (composição fiscal de sete municípios em 2025) foi reproduzida a partir de **21 valores da FINBRA/DCA canônica SP645**. O rótulo interno da legenda passou de “FPM / RC” para **“FPM — cota mensal / RC”** e investimentos foram qualificados como **liquidados**; cifras e escala não foram alteradas conceitualmente. Foi reparada a separação entre o título da F2 e a imagem (antiga quebra p. 9/10); ambos aparecem na página 10.

Cabeçalho introdutório e rodapé passaram a indicar G20. A comparação de conteúdo do DOCX G19×G20 apresenta só três partes internas alteradas: `word/document.xml`, `word/footer1.xml` e `word/media/image9.png`; as demais partes mantêm conteúdo idêntico.

## Provas de QA
- **321 parágrafos, 45 tabelas e 15 mídias** no DOCX.
- **66 páginas** na prova PDF, todas com rodapé G20 e texto extraível.
- Inspeção da página 10 mostrou legenda e imagem F2 juntas, sem cortes.
- Varredura de caixas de texto: **nenhum bloco extrapolou o limite físico de tolerância**. Isso não é certificação visual de todas as letras a 100%.
- Dados e script reproduzíveis estão no pacote técnico local `RMRP_G20_PACOTE_REVISAO_2026_11_05.zip`, com DOCX/PDF, fontes intermediárias, CSV e QA JSON. **A persistência deste relatório no GitHub não significa upload dos binários DOCX/PDF.**

## Matriz única de aceite e decisão
**G1 fiscal/quantitativo:** permanecem como prova os 273 testes delimitados do G14, os 272 pareamentos dos mapas do G16 e as verificações gráficas G17; não foram novamente executados integralmente no G20.

**G2 fiscal-documental:** RGF/RREO de Pontal, Barrinha e Orlândia sob quarentena e instrumentos de projetos/transferências sem conciliação final. Não inferir conformidade LRF, execução financeira de obras ou repasses comprovados.

**G3 jurídico:** revisão dirigida G19 de LC 200/2023 e LC 227/2026, sem parecer integral ou homologação do efeito do IBS.

**G4 editorial/cartográfico:** F2 corrigida nesta versão; F3 e F6 corrigidas em versões anteriores. IPCA de dezembro nos mapas e IPCA médio anual nas séries, assim como diferentes fontes populacionais para indicadores per capita, permanecem explicitados; eventual padronização total exige decisão editorial fundamentada. Mapa M1 específico ainda depende de decisão sobre escopo.

**G5 de circulação externa:** **não autorizado**. G20 é entregue para revisão interna condicionada aos controles substantivos remanescentes.

A matriz completa de **17 controles** está no pacote G20. Não ampliar esta decisão para o Volume I, que não foi integralmente reinspecionado nesta etapa.

## Referências de histórico
- [G19 — revisão jurídico-editorial](FECHAMENTO_G19_REVISAO_JURIDICO_EDITORIAL_2026_11_05.md)
- [G16 — auditoria dos oito mapas](FECHAMENTO_G16_AUDITORIA_OITO_MAPAS_2026_11_05.md)
- [G17 — auditoria das figuras](FECHAMENTO_G17_AUDITORIA_FIGURAS_2026_11_05.md)
- Base FINBRA/DCA: Drive ID `1BtXY_FxydMREEbMACJtaoW2n24ohVH33`.
