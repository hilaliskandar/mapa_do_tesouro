# Finanças municipais da RMRP — README operacional

**Atualizado em 06/11/2026, após recuperação da G29.** Documento de continuidade e trilha de auditoria. A referência de procedimentos detalhados é o [README nativo do projeto no Google Drive](https://docs.google.com/document/d/1e4G6zFFG6bxz_NKJj6yOwiJbkMb2i_MuQ4JLo3DrwlU/edit).

## Regra obrigatória de persistência

Todo produto produzido ou alterado neste projeto deve ser salvo no **Google Drive** e ter o seu **ID, URL, versão e resultado da verificação de existência** incluídos neste README ou no README de continuidade do Drive. Abrange DOCX/PDF, tabelas, CSV, mapas, imagens, ZIP, matrizes, scripts, cadernos e relatórios. Caminhos `sandbox:/` e arquivos temporários não são armazenamento permanente. Não concluir uma etapa como persistida sem upload confirmado e readback de metadados, com conferência de conteúdo quando pertinente. Em caso de falha, informar explicitamente pendência e não inventar link.

Cada gate registra: **data; objetivo; fontes e documentos-base; procedimentos executados; achados quantitativos; produtos e IDs do Drive; hash/manifesto quando cabível; QA; ressalvas; decisões; pendências e próxima etapa**. Preservar versão original e trabalhar em cópia. A cada produto final gerar DOCX editável e prova PDF, quando pertinente, salvar ambos no Drive e reabrir para validação. O histórico de execução deve ser escrito para permitir retomada sem depender de mensagens do chat.

## Volume II — estado em 06/11/2026

- **G29**: última edição integral, 69 páginas, 45 tabelas, 16 mídias; arquivos originais recuperados do usuário e **arquivados no Drive em 06/11/2026**. Preservar a versão imutável e editar G30 apenas em cópia. Ver [fechamento G29](FECHAMENTO_G29_REVISAO_PUBLICA_2026_11_06.md).
- **G30 v1**: versão integral de trabalho produzida a partir da G29, com 39 parágrafos analíticos incorporados (34 municípios, quatro sub-regiões e RMRP), 74 páginas; 45 tabelas e 16 mídias preservadas. **Salva no Drive; ainda não homologada para circulação**. O caderno G30 anterior de 13 páginas permanece como fonte da intervenção.
- **Lote 85**: DOCX anterior localizado no Drive para confronto [ID 1kMn6AnvCQ10OfZErDUVWtQ61dbvmznpl](https://docs.google.com/document/d/1kMn6AnvCQ10OfZErDUVWtQ61dbvmznpl/edit), sem alteração.
- Distinção metodológica crítica: queda do investimento real **total** G30 = -43,12% em 2023–2025; queda real **por habitante** da versão Lote 85 = -39,52%. Não intercambiar. Razão das somas difere de mediana municipal; ISS e ICMS contábeis observados não equivalem à receita de referência legal do IBS.

## Produtos G30 salvos no Google Drive

| Produto | Link permanente | Verificação |
| --- | --- | --- |
| Pacote ZIP completo | [Drive](https://drive.google.com/file/d/1V1q2WZF8_hQSBHGjvUE67IKYviIyaMyx/view) | Upload e metadados |
| Caderno G30 editável DOCX | [Drive](https://docs.google.com/document/d/1QdfoP_B4gpNbM6ruMeYMcXC21hChPx9T/edit) | Upload e metadados |
| Caderno G30 PDF | [Drive](https://drive.google.com/file/d/1xULzGZBEv5ek_mipxzn6YZpmo8GFQCqs/view) | Upload e metadados |
| Matriz de incorporação CSV | [Drive](https://drive.google.com/file/d/1oiIzQVBorTJLaf3t3SAmMRiF8D-jl0Nr/view) | Upload e metadados |
| Textos municipais Markdown | [Drive](https://drive.google.com/file/d/1lblrXI0qmZoCyviCWoKX4oNcPRwqu2fv/view) | Upload confirmado |
| Cinco análises territoriais Markdown | [Drive](https://drive.google.com/file/d/1ga1wfwmpizuWiNT8KL5eLbVomBazVF_W/view) | Upload confirmado |
| Relatório gate G30 | [Drive](https://drive.google.com/file/d/1zuamN-u_tEzxSfXs4YEfOS8esRrU7r1w/view) | Upload confirmado |
| Confronto G30 × Lote 85 | [Drive](https://drive.google.com/file/d/17Z69gMxqwbMDhkcfqIsBP4i4VKuJpbiy/view) | Upload confirmado |
| Manifesto SHA-256 | [Drive](https://drive.google.com/file/d/1BY99Hcw5JPlhaMSA021Kl9tR0HjyX-UY/view) | Upload confirmado |

**Nota de controle:** os nove produtos tiveram upload confirmado e readback individual de existência e identidade por metadados do Drive. A inspeção aprofundada de conteúdo permanece etapa de QA antes de homologação. O pacote ZIP não equivale a uma versão G30 do Volume II integral.

## Procedimentos e resultados já registrados

- [G29 — revisão pública](FECHAMENTO_G29_REVISAO_PUBLICA_2026_11_06.md): 39 matrizes, correção de comentários internos, preservação de 45 tabelas e 16 mídias.
- [G30 — caderno municipal](FECHAMENTO_G30_CADERNO_REVISAO_SUBSTANTIVA_2026_11_06.md): análises de 34 municípios.
- [G30 — matrizes territoriais](FECHAMENTO_G30_MATRIZES_TERRITORIAIS_E_SINTESE_2026_11_06.md): quatro sub-regiões e RMRP.
- [G30 — matriz de incorporação](FECHAMENTO_G30_GATE_INCORPORACAO_39_TERRITORIOS_2026_11_06.md): cobertura, cautelas e dependência G29.
- [G30 — QA e hashes](QA_G30_INTEGRIDADE_PACOTE_39_TERRITORIOS_2026_11_06.md): integridade do conjunto.
- [G30 — confronto Drive Lote 85](G30_CONFRONTO_DRIVE_LOTE85_E_GATES_2026_11_06.md): conflitos aparentes de denominadores e cautelas para incorporação.

## Próximo gate

**G30 v1 foi integrada em cópia da G29**. Próximo gate: conferir individualmente as 39 passagens contra indicadores e fontes, revisar coesão editorial, manter dados, 45 tabelas, 16 mídias e notas fiscais G26–G29. Revisar a prova PDF e produzir G30 v2, salvar DOCX/PDF e anexos no Drive, conferir todos os IDs e atualizar ambos READMEs. Não homologar G30 v1 para circulação sem revisão temática final.


## G29 — arquivos originais recuperados e preservados no Drive em 06/11/2026

| Arquivo | ID e endereço permanente | Tamanho | SHA-256 |
| --- | --- | ---: | --- |
| DOCX G29 (original; referência editável, não sobrescrever) | [1rCaJZ7ops1uWl-2OsLS8Te1FTNs34DUO](https://docs.google.com/document/d/1rCaJZ7ops1uWl-2OsLS8Te1FTNs34DUO/edit) | 2.785.116 bytes | `ef9d9828a61bec6ca70a7844925de5c0e969b0cf3aeafdf90cb2aa1c395aef17` |
| PDF G29 recebido separadamente | [1l_9CydZsOJsUR2_B5iknJX7ojelJPKYh](https://drive.google.com/file/d/1l_9CydZsOJsUR2_B5iknJX7ojelJPKYh/view) | 2.448.514 bytes | `107d89b7bf3323f929381570962dafefa17eb16921576155c70752f9c374b468` |
| ZIP G29 com DOCX, PDF e QA | [1dOUXtEqf33S8P4EJPrGKCPq9ZpRYfDls](https://drive.google.com/file/d/1dOUXtEqf33S8P4EJPrGKCPq9ZpRYfDls/view) | 4.615.643 bytes | `8f1b79b8443375a6f206d0efd39da961ac157a0b517ce5931937cc9d24aa5c52` |
| PDF G29 interno ao ZIP, preservado separadamente | [1ZPmS6FKMBfYeNVwP6S2ueLu-3sszEYKL](https://drive.google.com/file/d/1ZPmS6FKMBfYeNVwP6S2ueLu-3sszEYKL/view) | 2.423.377 bytes | `28d494099d226bb8ef014040a1e105879aa75b05b3861d7aaed269211e9e1f76` |

**Procedimento:** os três anexos foram recebidos, suas dimensões e hashes apurados, a integridade do ZIP testada e o PDF interno extraído. Quatro arquivos enviados e confirmados por leitura de metadados no Drive. O DOCX avulso coincide com o DOCX do ZIP. **O PDF avulso não coincide, em bytes, com o PDF interno**, cujo hash consta no `G29_QA.json`. Não excluir nenhuma variante nem afirmar que são visualmente equivalentes sem confronto. ZIP: cinco itens, teste sem erro; QA interno informa 69 páginas, 45 tabelas, 16 imagens e 39 SWOT. Ambos os PDFs e o DOCX G29 permanecem intocados. A pendência de recuperação da versão-base foi resolvida; o gate seguinte é integrar seletivamente G30 sobre **uma nova cópia** de G29, arquivando novos DOCX/PDF, diff e QA no Drive.


## Integração G30 v1 — executada e arquivada em 06/11/2026

Cópia derivada do DOCX G29 original, que **não foi sobrescrito**. Foram substituídos seletivamente 39 parágrafos analíticos imediatamente posteriores às matrizes SWOT, preservados os indicadores contábeis tabulados e as notas documentais. As cinco análises agregadas foram organizadas em parágrafos temáticos; formulações metatextuais foram reduzidas nos textos municipais. A prova PDF resultante possui **74 páginas**.

**QA executado:** 45 de 45 tabelas com XML byte a byte idêntico ao G29; 16 de 16 mídias OOXML com hashes idênticos; 15 figuras inline nas duas versões; ressalvas fiscais de Barrinha, Pontal e Orlândia conservadas; nenhum bloco de texto encontrado fora dos limites geométricos do PDF; inspeção visual das montagens. Revisão temática individual dos 39 textos permanece pendente. Estado: **minuta G30 v1, não homologada**.

| Produto | Google Drive | SHA-256 |
| --- | --- | --- |
| DOCX integral G30 v1 | [Abrir](https://docs.google.com/document/d/1oRABLHnoG3kk0acY2wIsO25KJLlkBBZS/edit) | `86a9849f64bc286d87e92f6cfed34c673998d3ad4d0aeeca110fe3fdc50b88e2` |
| PDF G30 v1 (74 páginas) | [Abrir](https://drive.google.com/file/d/1mJ4DYNdI_-58npl3fHGdb_oCdEVSpAQ8/view) | `52f3bcefb27ad2c6a550e4529137e0f71445b87dcb4ba5a38d991441c9b577c9` |
| Diferenças 39 SWOT JSON | [Abrir](https://drive.google.com/file/d/1-sDg4CvlmDcuwNYh4D4Do8rwdHNOBH8-/view) | `1ce44b47c1ab17c3f1b95f5828a70a2fb79c324a9396ec05ed973199146c39a1` |
| QA estrutural JSON | [Abrir](https://drive.google.com/file/d/1YOTXDRyYZIe0hR333hLQeDDPsnTn-nfD/view) | `1a44dd2ca3c69c9bdf53e63ebb2205175e0f2b75cd0e3b5f9b805372dc904fba` |
| Relatório técnico de integração | [Abrir](https://drive.google.com/file/d/1Mm0x_qP9fEZgWAWtpT4SMy6XPD-KHrvH/view) | `3451f0a4fca43925caa4098df53c789648fdeda380d5d79f8272ad9cb1b7ca27` |
| ZIP G30 v1 (conjunto) | [Abrir](https://drive.google.com/file/d/1qa0EABWscsBxQew3Ob9cihygh5DY3bv6/view) | `a66e43fad7f3e8cfbd577c76b05cdf6e755191e32c6ed6ba82e9730d1c41a1c2` |

**Persistência:** seis uploads aceitos e seis readbacks de metadados concluídos. Os hashes referem-se aos arquivos gerados localmente, previamente ao envio. Nenhuma ação desta integração modificou o DOCX G29 armazenado no Drive. Próximo gate editorial: revisão detalhada dos 39 parágrafos, validação de consistência dos indicadores, inspeção final, versão G30 v2 e novo ciclo de arquivamento no Drive.


## G30 v2 — revisão dos municípios e arquivamento — 06/11/2026

A partir de **G30 v1**, em nova cópia do Volume II, realizaram-se **34 ampliações analíticas municipais**, relacionando trajetórias de investimento com oportunidades, riscos e serviços documentados nas tabelas SWOT, e **duas revisões** da síntese metropolitana. Foram preservados 45 quadros/tabelas (XML idêntico), 16 mídias OOXML (hash idêntico), notas fiscais de Barrinha, Pontal e Orlândia e distinção entre projetos anunciados, contratos, empenhos e pagamentos. **75 páginas** renderizadas; cinco montagens de 15 páginas examinadas, sem anomalias grosseiras; zero páginas quase vazias e zero blocos textuais além dos limites geométricos. O ZIP foi testado sem erros. A G29 e G30 v1 originais não foram modificadas. **Estado: minuta G30 v2 não homologada para circulação.**

| Produto | Local no Google Drive | SHA-256 |
| --- | --- | --- |
| Word integral G30 v2 | [Drive](https://docs.google.com/document/d/12hog0AKEoFDWF54TcjURU5muIGUI-w5e/edit) | `bbd438577246c287c05126a75a31f9b1de23a01b6805356a8c5f76e08218b3d1` |
| Prova PDF G30 v2 | [Drive](https://drive.google.com/file/d/1o7tYJrQsUM6OwN0yMWYZjdiF7KF3HZum/view) | `b4faeab9080af8bcaa09c9685bebebf79502cb3074873262bd07ba62341a824e` |
| Registro de 36 alterações e QA | [Drive](https://drive.google.com/file/d/1ydtfiTf-GK1jMSTPYWuJQC42ASaE9CEN/view) | `756f0495d0451bb6508e2d4f08c6bf0557d5bfaa44e5ba52229cae1e4ba9e740` |
| Relatório de revisão G30 v2 | [Drive](https://drive.google.com/file/d/16CYolmoExw1V1LfezVE7fxNI3n_NFqdY/view) | `83662c02ee9e5a7944d399b18635f312e71fad1519d1f7a0477af05272bd5e87` |
| Pacote técnico ZIP G30 v2 | [Drive](https://drive.google.com/file/d/1-8Pa5tJHOxumC-MFi5L65Fo1rhVjtMJm/view) | `211eca717ee5bf74f92b2ab08aa0f4b53b837fa4314151e06f6fa7fac8631b0a` |

**Persistência:** cinco uploads e cinco leituras de metadados confirmadas. O README nativo do Drive deve ser atualizado com esses mesmos registros se a edição não estiver disponível na sessão. **Próximo controle:** revisar em escala de leitura as 39 análises, quadros e conclusões; não converter a G30 v2 em versão de circulação sem fechamento temático e gráfico.


## G30 v3 — revisão fina, 06/11/2026

**Status:** versão integral de trabalho, não homologada para circulação. A partir de cópia da G30 v2, foram realizadas **24 correções localizadas** em parágrafos analíticos posteriores às matrizes SWOT municipais. Objetivos: reduzir redundâncias, retirar metalinguagem sobre a pesquisa, tornar o argumento fiscal mais direto e corrigir um resíduo de marcação `**não**` no comentário de Jaboticabal. Cada troca contém antes/depois no JSON de diferenças.

**QA:** 45 tabelas idênticas em XML à G30 v2; 16 mídias preservadas byte a byte; 15 imagens inline; ressalvas fiscais de Barrinha, Pontal e Orlândia presentes. DOCX renderizado com **75 páginas**; zero blocos de texto além dos limites geométricos e zero páginas com menos de 90 caracteres. Cinco montagens, cobrindo todas as páginas, examinadas. **Limitação:** montagens não equivalem à inspeção a 100% de todas as páginas e dos quadros partidos; análise final de coerência entre partes I–IV e conclusões ainda é necessária. Sem nova conferência Siconfi, sem homologação de projetos ou cenários. ZIP validado sem erro.

| Produto | Identificador e link do Drive | SHA-256 |
| --- | --- | --- |
| DOCX G30 v3 | [15mW1pD9Wg5kK-z7-GyDfysxsm7Sh8_2Y](https://docs.google.com/document/d/15mW1pD9Wg5kK-z7-GyDfysxsm7Sh8_2Y/edit) | `0cca838102f1bb99870a61d4e51e2c102bf36f927be026cf56d3f650958f63ca` |
| PDF G30 v3 | [1vEBOVZakuszocwOadSmBCb4xSK--R2VQ](https://drive.google.com/file/d/1vEBOVZakuszocwOadSmBCb4xSK--R2VQ/view) | `cdec38a66d0c97d16f3e3fd6cdf6ae45b0e5edcc1db4c39e883a8a00fe0a6e87` |
| Diff 24 intervenções | [1wGUYsfNx8hmYdskBBJUwJCl-XpEV90cR](https://drive.google.com/file/d/1wGUYsfNx8hmYdskBBJUwJCl-XpEV90cR/view) | `564a9ac197441febe6b07398a3371e70d172def4b42a5e0b78875f5f2263a31b` |
| QA PDF/estrutura | [1kNtSYU5fNG2QB2gFa7BMJQnoe-o0lYsl](https://drive.google.com/file/d/1kNtSYU5fNG2QB2gFa7BMJQnoe-o0lYsl/view) | `3f2d92a530863f27d0619cf703cd634286448b482b2b512924ea3b005111dc6f` |
| Relatório de revisão | [1JRIkqoQc8Wii8VgZUHVpz9hHv5DAHOel](https://drive.google.com/file/d/1JRIkqoQc8Wii8VgZUHVpz9hHv5DAHOel/view) | `ae79c7fa455c9c343447f3692471fa46c6f2a11f0845e4ecb773987b1b36df32` |
| ZIP G30 v3 | [1R_sfzb_CLlNzO3bm1_uqmD1KepUnUZ0F](https://drive.google.com/file/d/1R_sfzb_CLlNzO3bm1_uqmD1KepUnUZ0F/view) | `1e24b05b7b53e84785b26f4f86a755796a99e8e449be881cba38f634a6377251` |

**Persistência:** seis uploads aceitos e seis leituras de metadados confirmadas. Arquivos e hashes correspondem à versão gerada localmente. A G29, G30 v1 e G30 v2 não foram sobrescritas. **Próximo gate:** revisar coesão e remissões entre diagnóstico, reforma tributária, cenários 2027–2030, conclusões e matrizes, verificar em tamanho integral páginas com tabelas partidas e produzir eventual versão G30 v4.


## G30 v4 — revisao transversal do Volume II — 06/11/2026

**Estado:** minuta integral, ainda não homologada para circulação institucional. Trabalho realizado sobre **cópia da G30 v3**, sem alterar G29 ou outras versões.

Procedimentos: oito correções textuais e uma mudança de posição de referência bibliográfica (total de nove intervenções documentadas em JSON). A referência STN da rubrica FPM, antes localizada após o sumário, passou à seção de referências; a Parte IV teve corrigida a numeração da seção 7; duas passagens introdutórias redundantes dos cenários foram reformuladas; as conclusões passaram a citar dados concretos: 31 de 34 municípios com queda real per capita dos investimentos em 2023–2025, retração agregada de 39,52%, relação investimento/receita corrente de 4,94% em 2023 e 2,55% em 2025; sub-regiões de Ribeirão Preto (tributação 28,89%), Mococa (FPM ordinário 24,06%), Jaboticabal (investimento/receita 2,08%) e Batatais (receita corrente real per capita R$ 8.418,05).

QA: **45 tabelas XML idênticas**, **16 mídias com hashes idênticos**, **15 imagens inline**, ressalvas de Barrinha, Pontal e Orlândia e convenções populacionais e de IPCA preservadas. Renderizado DOCX em 75 páginas; sem páginas de texto quase vazias nem blocos além dos limites geométricos. Cinco folhas de contato de 15 páginas foram examinadas; permanece a necessidade de revisar em tamanho de leitura os quadros SWOT quebrados entre páginas antes de homologação. Não se atribui causalidade à LC 200/2023 nem se estima impacto líquido municipal do IBS. A grade metodológica dos cenários não constitui previsão monetária.

| Produto | Link no Drive | SHA-256 |
| --- | --- | --- |
| DOCX G30 v4 | [Drive](https://docs.google.com/document/d/1IL_cE753pivlMnP38oZXec4vq6FVgVza/edit) | `78a9c51374395802b999f88260e6e06d189297a9222ca385da3ded7cd04ed811` |
| PDF G30 v4 (75 páginas) | [Drive](https://drive.google.com/file/d/1W3fysJ76qOvQ4wJ-Y7-EBV5lwDz75nRL/view) | `bf1eba0dcd12dd7bd030c1bbf70141009d0c8362e1122247593d919111d474b8` |
| Diferenças e QA detalhado | [Drive](https://drive.google.com/file/d/1CnSDY6YoThnARooLxdbwKfBZ4h_550pw/view) | `92158f479205bb1008eb8d25aaa6d13c6687f2decdf33d647980e6bb35203a20` |
| QA de paginação | [Drive](https://drive.google.com/file/d/1iW_ZQ7fxl6hE5kP6yGE5xQKUF7_RMISO/view) | `6da1a3bef064734bb073ab1d79c2353178207df306cc8034cf32d3042a1868ff` |
| Relatório editorial G30 v4 | [Drive](https://drive.google.com/file/d/1XUxvRKvEf2NhHy2KjwfFgD76k08AS0AK/view) | `4c4ff43ccc52270c1bb30fba7673693a5afcba3a1030ad0ffcbbcd912d567811` |
| Manifesto de hashes | [Drive](https://drive.google.com/file/d/1S3g8VUT-859UfVmrmKoBy0Sb3bAZU1Kd/view) | `9caef32120891bd3df89fa63815a34253ef3391f7ae8db4de8d8721c99ea8ac2` |
| Pacote ZIP completo | [Drive](https://drive.google.com/file/d/172K1Ww_7F4ZWcV8ie9B9vv7eNQkTY7-O/view) | `8daeb1ff82d0ab04edf67ec12f4dd472ea0929f65b507c85c2d7d0e04271bed9` |

**Persistência:** sete uploads confirmados e sete readbacks de metadados; cada arquivo possui identificador permanente do Drive. Próximo gate: conferência visual integral das páginas com quebra de tabela, consistência entre legenda, gráfico e seção conclusiva, revisão de linguagem final. Após eventuais ajustes, produzir cópia G30 v5 e arquivar todos os produtos novamente.


## G30 v5 — Pranchas em paisagem — 06/11/2026

**Resultado:** versão integral de trabalho com **103 páginas**, sendo **43 páginas de texto em retrato** e **60 páginas de pranchas em paisagem**, derivada de cópia da G30 v4. As matrizes e demais quadros ficam editáveis no DOCX. Abrange 45 quadros Q1–Q45, nove mapas M1–M9 e seis figuras F1–F6. Os títulos e chamadas foram normalizados para permitir que o texto refira cada peça numerada.

**Decisão de paginação:** o protótipo de inserção rigidamente imediata de cada prancha após sua menção gerou 131 páginas, com várias páginas retrato quase vazias. Para respeitar o objetivo de leitura e economia gráfica, a edição v5 **agrupa pranchas de um bloco analítico** em páginas paisagem consecutivas; o texto percorre um bloco antes de abrir a seção gráfica, retomando retrato após o grupo. Assim, o quadro nem sempre aparece literalmente na página seguinte à primeira menção. A relação sequencial e a numeração dos artefatos foram preservadas. A alteração é editorial e não altera os dados.

**Auditoria comparativa G30 v4 × v5:** 45 tabelas com texto integral idêntico; 16 mídias OOXML bit a bit idênticas; 15 imagens inline. No PDF, 60 de 60 pranchas paisagem identificadas por título e número, Q1–Q45/M1–M9/F1–F6 completos, zero página retrato com menos de 450 caracteres e zero blocos de texto além dos limites geométricos. A produção incluiu rasterização das 103 páginas e inspeção visual de amostras e folhas de contato. Isso **não substitui revisão humana de todas as páginas ampliadas** antes de homologação institucional. Os 39 quadros SWOT são apresentados sem quebra entre páginas. Nenhuma nova pesquisa fiscal ou alteração de ressalvas foi executada.

**Produtos depositados e individualmente verificados por metadados no Google Drive:**

| Produto | Endereço no Drive | SHA-256 |
| --- | --- | --- |
| DOCX integral G30 v5 | [Drive](https://docs.google.com/document/d/12bRAHqmifToUaWWS2pQEAWx0ZckgKnSN/edit) | `f3b17cb2b6460177c1903cc93d99035bc48f9b3c1c8f19c782a79965a2c45a8d` |
| PDF G30 v5 (103 páginas) | [Drive](https://drive.google.com/file/d/1lVfAqKz9yCOouuajCLstS52lTdZ9Cbts/view) | `42d63806f42c08c0b14f88bd40e610620d5379b54ba9541b4b2f091cae01c0b3` |
| QA de 60 pranchas | [Drive](https://drive.google.com/file/d/1D_ehJ8p9ptTcmibg24Wu2zlr2gb1iqXM/view) | `a591fade0a2964eae035c3e208a798197f7997c31ecb9dfc012333de001dcbc6` |
| Relatório metodológico/diagramação | [Drive](https://drive.google.com/file/d/17nsYij8IYWlhIAO_Noi5CELcI-hau1Gx/view) | `4038496d4bf8f5257f21b576606a6fce88cd4ac90fb610751c56d8185e8cea84` |
| Manifesto de integridade | [Drive](https://drive.google.com/file/d/177Mm2TzAkxZ_C-RkzqjhKKJ6_WrTXNp1/view) | `ed2f228e52179e0424659984b804508b583eb35d5e5586a104f574f7ff4ac6cb` |
| Agrupamento das pranchas | [Drive](https://drive.google.com/file/d/1tx2sOfJ3bgJ1cVPoSuGUo78c0aR6PD-H/view) | consultar manifesto |
| Pacote de produtos ZIP (sem scripts executáveis) | [Drive](https://drive.google.com/file/d/1dzGbNl0ZecBiH8tiY0LYfrFXTve4kUqz/view) | `ed1510c56e94b5f6a163ee56b2db710039d475bf32735092903b2405a2b70fec` |

**Persistência:** 7 de 7 uploads úteis confirmados por readback individual de nome/tipo/tamanho. Um ZIP técnico contendo scripts teve upload recusado pelo serviço; a alternativa sem executáveis foi enviada e verificada. As fontes G29 e versões G30 v1–v4 permanecem preservadas. **Estado:** G30 v5, minuta diagramada, ainda não homologada para circulação. Próximo gate: revisão visual ampliada de páginas densas, avaliação editorial da distância entre chamada e prancha e controle de remissões do documento integral.


## G30 RC1 — verificação pré-circulação — 06/11/2026

O Volume II G30 v5 foi submetido a controle adicional de **remissões, legibilidade, ocupação vertical e integridade documental**, sem reabrir a auditoria fiscal. A versão RC1 deriva de cópia de G30 v5 e corrige **uma formulação interna** na seção de referências, substituindo a menção a "escopo homologado deste diagnóstico" por uma formulação dirigida à leitura pública. G29 e G30 v1–v5 mantidas sem sobrescrita.

**Resultado verificado:** 103 páginas (43 retrato, 60 paisagem); Q1–Q45, M1–M9 e F1–F6 completos; **60/60 chamadas em página de texto anterior**, separação de 1–3 páginas (32 a uma página, 18 a duas, 10 a três); texto das 45 tabelas preservado; 16 mídias intactas por hash; nenhuma extrapolação geométrica de texto. As 15 imagens inline apresentam resolução efetiva de aproximadamente 158–284 dpi, sem teste de impressão física. Amostragem ampliada de tabelas densas e mapas confirma legibilidade, mas não constitui inspeção humana individual exaustiva de 103 páginas.

**Descoberta na auditoria:** o teste anterior de "páginas retrato com mais de 450 caracteres" não detectava baixíssima ocupação vertical. Novo teste identificou páginas **3 (37%), 25 (41%), 38 (26%) e 103 (33%)** com ocupação de menos de 52% da altura útil; em particular, página 38 contém final de análise antes de prancha e página 103, encerramento metodológico. São ressalvas gráficas explícitas. Um teste alternativo de agrupamento com limiar de 2.600 caracteres resultou em 110 páginas e numerosas transições vazias; rejeitado. Uma realocação pontual de Q8 apenas deslocou a baixa ocupação para outra página, também rejeitada. Não há perda de conteúdo, tabela dividida ou bloqueio estrutural comprovado.

**Decisão:** a G30 RC1 é **candidata de circulação**, sujeita à chancela editorial e à aceitação consciente das quatro páginas subocupadas ou a novo ajuste final de paginação. Não declarar homologação institucional automática.

| Produto | Link Google Drive | SHA-256 do original local |
| --- | --- | --- |
| DOCX RC1 editável | [Drive](https://docs.google.com/document/d/1WC7_pxbDFe76RtEmFRYCVQs4hxVrXfSP/edit) | `b5963e67547c8700de5ceee4928461f990fe3b7ce95672c3f8282f27c55b16e0` |
| Prova PDF RC1 | [Drive](https://drive.google.com/file/d/1sDNZpnRzGSwcqTRZDZWztTHWFFNUu9Dc/view) | `c1468c5c55796cc2d28db15ca64d21f688bd69e7df8386cc9f2d14c3f5cb98ef` |
| Diff redacional | [Drive](https://drive.google.com/file/d/1rAOqzFK8t-tQo3mnk4ZNrwMwst4KgF3X/view) | `10016d4a36bc711052080470343121ae0a8bc9be04898585ae65d7eca515120c` |
| QA estruturado e remissões | [Drive](https://drive.google.com/file/d/1gs8uNcPWvLDaImoQEjMbVQgU2qDy1MRZ/view) | `413c8373f1eba9e3a701e130ff1b812bf65b3c75ede7ab88ad06b6a933655703` |
| Parecer de pré-circulação | [Drive](https://drive.google.com/file/d/1bnbE5obQ4tdpaqHOjRjVxywsGV9Iumae/view) | `2940f3165974bcd6b035ea3bf579ea7a2bac9a3c0e4b1b07e6562701529f4d90` |
| Pacote ZIP | [Drive](https://drive.google.com/file/d/1y8CWH-8-aAzGOKbyVpRF1OLPnS4Vyk6a/view) | `767cc32a8dca75ee27274726fe80d9e6c7c5e1eaffaf64312044b6d8dff312ac` |

Seis uploads e seis consultas de metadados confirmados. O PDF avulso precisou de segunda tentativa, concluída. **Próximo gate:** aceite editorial de quatro páginas com espaço não utilizado, seguido de eventual homologação da RC1 sem outra intervenção no conteúdo fiscal, ou correção tipográfica seletiva em cópia RC2.


## EmDash — imagens e mapas do Volume II — 06/11/2026

Foram extraídos, sem alterações, 16 arquivos PNG do pacote Word G30 RC1, com identificação por vínculos OOXML e hashes SHA-256. Destes, **15 são imagens exibidas no relatório** (M1–M9, F1–F6) e **uma é um mapa adicional sem chamada no corpo da RC1**, que exige conferência antes de divulgação. Os 45 quadros não foram convertidos: continuam editáveis no DOCX.

**Procedimento:** extração dos arquivos binários do DOCX; atribuição de código/título, alt text e legenda; upload dos 16 PNG para pasta dedicada do Google Drive; envio autenticado para a biblioteca de mídia do **EmDash Radar Regulatório**, pelo conector radar/media_upload; leitura posterior da biblioteca e conferência entre conteúdo original e servidor.

**Resultados verificados:** 16/16 itens com status ready; 16/16 hashes SHA-1 correspondentes à origem; 16/16 tamanhos exatos; 16/16 textos alternativos e legendas preenchidos. Os identificadores retornados pelo EmDash foram persistidos em catálogo. A operação não publicou posts, páginas ou versões HTML.

**Pasta de preservação no Drive:** https://drive.google.com/drive/folders/1du7654ezGKWV7HTEfUX3leVVq0Kh198C

**Produtos persistidos:**
- Catálogo JSON com identificadores EmDash, caminhos relativos das imagens, dimensões, hashes e IDs Drive: https://drive.google.com/file/d/1WOrRhK2obl5iTLWKfVCOisNYyiIpI6BK/view
- Catálogo CSV, delimitado por ponto e vírgula: https://drive.google.com/file/d/1c3pJcZtzJS9sgvJVAsTcS9eE8mVF8Qon/view
- Orientações e exemplos para HTML: https://drive.google.com/file/d/1mQC35jQ79EpZRhCA2tR3Jnialagi3ZFN/view
- ZIP dos 16 PNG originais e catálogos: https://drive.google.com/file/d/16H0HcNFJ5xs_pa5W9cfZiGn89S9E09DW/view
- Catálogo de texto para validação cruzada: https://drive.google.com/file/d/1UNZdq2-1PZbS-Pmtmb8Tr3p8DWUsZdqy/view

**Exemplo:** figura F1, ID EmDash 01M6RVNETJBEC8DBA2C5W2YV18, caminho relativo /_emdash/api/media/file/01M6RVNE9DYDM06A8P6QDPGESE.png. Preferir mediaId e caminho do CMS em HTML. A URL pública absoluta no domínio boletim.radarregulatorio.org **não teve verificação HTTP externa conclusiva**; não declarar acesso público verificado até executar essa etapa.

**Ressalvas:** a imagem ANEXO é um mapa de evolução real dos investimentos sem vínculo de exibição na RC1 e não deve ser divulgada sem validação de versão/legenda. Verificar o contexto estatístico de cada mapa, os créditos e a legibilidade móvel antes de usar em chamadas.

**Próximo gate:** validação pública das URLs, adaptação responsiva e incorporação em HTML, quando a versão editorial for escolhida. A G30 RC1 DOCX/PDF permanece imutável.


## Galeria HTML das mídias G30 RC1 — 06/11/2026

**Objetivo:** validar a reutilização dos mapas e figuras já cadastrados na biblioteca de mídia EmDash, sem publicar a edição integral do relatório. Foram produzidos dois arquivos HTML5 responsivos, ambos com 15 elementos visuais (M1–M9 e F1–F6), identificações originais, legendas, textos alternativos e links de referência ao relatório RC1. O mapa ANEXO, sem chamada no corpo, foi deliberadamente omitido. As 45 tabelas editáveis do DOCX não integram a galeria e ainda exigem conversão semântica própria em uma edição HTML integral.

**Produtos no Google Drive:** pasta de mídias e catálogos [RMRP Volume II](https://drive.google.com/drive/folders/1du7654ezGKWV7HTEfUX3leVVq0Kh198C).

- [Galeria HTML autônoma, com imagens incorporadas](https://drive.google.com/file/d/1ZvYMT1JVyIStMr68hwX2kMMuiDhN_w3S/view): 3.492.183 bytes; SHA-256  obtido no manifesto local do gate.
- [Galeria HTML com caminhos relativos da biblioteca EmDash](https://drive.google.com/file/d/1tvqvF0mQAZTO2S7o6nRJDYdNgXAit2yJ/view): 13.948 bytes; endereços internos exatos do CMS, a serem testados no site.
- [Relatório da prova HTML](https://drive.google.com/file/d/1AJp1ltyCxDeUaZok5RwCQ7ybpdlsj3cF/view).
- [QA estruturado](https://drive.google.com/file/d/1Vu5Mk2-zO-ArXtlJ9Y-ucb2mHXd4A8cA/view): 15 SHA-256, 15 SHA-1 e 15 tamanhos confirmados.
- [Pacote completo ZIP](https://drive.google.com/file/d/1G4doU25PHEMyw9plWDP7LxrRU6UoF4sL/view).

**Persistência:** cinco uploads no Drive concluídos e cinco leituras de metadados confirmadas; os HTML são artefatos arquivados, **não publicados** como páginas no EmDash. Foi validada por análise estática a existência de 15 figuras, 15 imagens e 15 descrições alternativas em cada HTML. A variante autônoma incorpora os PNG como data URI; a variante EmDash resolve imagens por URL relativa e funciona quando servida no domínio do CMS.

**Validação HTTP externa:** **inconclusiva**. O teste HTTPS em ambiente container falhou por resolução DNS de boletim.radarregulatorio.org; dois endpoints de imagem foram rejeitados pela ferramenta pública de consulta. Isso **não demonstra indisponibilidade do site** e tampouco confirma entrega pública. Os 16 objetos estavam em status ready no EmDash, com hashes e legendas validados pelo conector. Próximo gate: consultar URLs externamente de navegador com acesso; comprovar HTTP 200 e image/png, testar viewport móvel e integrar figuras com 45 tabelas semânticas ao texto integral antes de publicar.


## Publicação de 34 estudos municipais na seção Estudos e Análises do EmDash — 06/11/2026

**Status: 34 publicações individuais + 1 índice, todos com `status=published` confirmado por leitura de retorno do CMS.** A coleção é `posts`, pois a categoria `estudos-e-analises` está vinculada a posts, e não à coleção `pages`. Cada endereço segue `/posts/financas-rmrp-{municipio}-2026`. O índice é `/posts/financas-rmrp-indice-34-estudos-municipais-2026`.

**Fonte documental:** [Volume II G30 RC1](https://docs.google.com/document/d/1WC7_pxbDFe76RtEmFRYCVQs4hxVrXfSP/edit), recorte Parte II, seção "As 34 matrizes municipais integradas". Foram extraídos os parágrafos específicos de cada município e a tabela SWOT Q8–Q41 na íntegra; títulos, seis componentes da matriz, números e ressalvas não foram reinventados. As notas explícitas de Barrinha, Pontal e Orlândia foram preservadas. Texto comum de método e vínculo para [Volume II em PDF](https://drive.google.com/file/d/1sDNZpnRzGSwcqTRZDZWztTHWFFNUu9Dc/view) acompanha os 34 posts. Este é um recorte municipal, não uma nova pesquisa independente.

**Auditoria pós-publicação:** 34/34 itens localizados por slug com `published`; 34/34 títulos correspondem ao manifesto; 34/34 possuem os seis subtítulos de SWOT, composição fiscal e link para a íntegra; 3/3 ressalvas sensíveis preservadas. Índice adicional encontrado com `published` e todos os 34 links. **Ressalva:** o acesso por URL pública externa ainda não foi demonstrado neste ambiente, apesar de os registros constarem publicados no CMS. Não confundir confirmação de publicação no sistema com prova HTTP 200.

**Inventário canônico com os 34 municípios, Q, CMS IDs e URLs:** [INVENTARIO_EMDASH_ESTUDOS_34_MUNICIPIOS_2026_11_06.md](INVENTARIO_EMDASH_ESTUDOS_34_MUNICIPIOS_2026_11_06.md). Fonte Markdown completa arquivada em [ZIP no Drive](https://drive.google.com/file/d/1pB2biUpmzBXafDm-dhFRT2EU6hu8Kz-L/view); [manifesto original](https://drive.google.com/file/d/1Ha-IzUzVjcTBXOGseLpd1peN0zGdGYA3/view). Navegação: https://boletim.radarregulatorio.org/posts/financas-rmrp-indice-34-estudos-municipais-2026

**Próximo controle:** verificar acesso público HTTP, confirmar apresentação da categoria e navegação a partir da seção do site, avaliar legibilidade móvel e eventual imagem de destaque específica. Preservar versões de fonte e dados metodológicos.


## Fechamento gráfico dos 34 estudos municipais — 06/11/2026

Após trabalhar em lotes reduzidos, o EmDash confirma **34/34 publicações municipais com quatro imagens na revisão live**: 1 matriz SWOT individual (Q8–Q41) e 3 mapas metropolitanos M1/M5/M6. Em todos os 34 casos, `content_compare` retornou `hasChanges=false` e quatro imagens na versão publicada. Foi corrigida a pendência da publicação da revisão de Santa Rita do Passa Quatro. Não foram alterados os slugs.

As 34 matrizes SWOT também conservam a transcrição acessível dos seis componentes. A conversão Markdown do CMS não cria tabelas HTML nativas; por esse motivo, utiliza-se prancha PNG + texto. Os mapas são contexto regional, não cartografia individual. Os capítulos gerais da RC1 não são repetidos em cada publicação. Ressalvas de Barrinha, Pontal e Orlândia preservadas. HTTP público, leitura em dispositivos móveis e indexação externa ainda não foram comprovados.

**QA canônico e inventário no Google Drive:** https://docs.google.com/document/d/1BoLYbvVrn-T9jyEZ8f_fPHaAqDjQjQ12gBkB4hqPN5U/edit. **Pasta de mídia com as 34 pranchas:** https://drive.google.com/drive/folders/1du7654ezGKWV7HTEfUX3leVVq0Kh198C. **Índice publicado no CMS:** https://boletim.radarregulatorio.org/posts/financas-rmrp-indice-34-estudos-municipais-2026. Próximo gate: verificação visual externa da apresentação e legibilidade das imagens, preservando as publicações já confirmadas.


### G30 — auditoria externa, revisão editorial e imagens das 34 páginas (06/11/2026)

- Acesso ao índice e aos 34 artigos municipais confirmado pela extração pública do Crawl2AI. As 34 páginas apresentaram transcrição textual das seis dimensões SWOT e remissão ao Volume II.
- Revisão editorial localizada aplicada aos 34 artigos publicados: removido H1 redundante ao título automático da página, retirada da duplicação da chamada de composição fiscal e eliminados asteriscos literais de itálico em legendas e notas. Em Taiúva, Pitangueiras e Monte Alto, legendas passaram a citar explicitamente M1, M5 e M6. A publicação de Ribeirão Preto foi usada como piloto, com confronto live/draft sem pendências. Slugs, indicadores fiscais, ressalvas, conteúdo SWOT e referências documentais preservados.
- Controle estrutural após as atualizações: **34/34 publicações com quatro blocos gráficos**, totalizando **136 referências de imagens**, todas com URL e `alt`. Correspondência de **136/136** nomes de arquivo do endpoint com `storageKey` de mídia cadastrado e com status `ready`; **34 pranchas SWOT Q8-Q41** e **mapas M1/M5/M6** estão presentes. **34/34** possuem legenda numerada para cada mapa, não repetem H1 interno nem as marcas literais detectadas.
- **Limite de verificação:** a correspondência entre CMS e biblioteca de mídia não certifica acesso HTTP 200, carregamento no navegador nem responsividade em celular. Tentativas externas tiveram bloqueio de DNS e limite de unidades Browserless; a captura Crawl2AI só abrangeu a abertura da página. Não declarar homologação visual completa. Permanecem a prova desktop/móvel e eventual substituição de pranchas por tabelas HTML semânticas para acessibilidade e reprodução integral das fichas.
- Persistência: README de continuidade do Google Drive, seção 22, https://docs.google.com/document/d/1e4G6zFFG6bxz_NKJj6yOwiJbkMb2i_MuQ4JLo3DrwlU/edit. As publicações foram atualizadas in loco no EmDash, com seus mesmos slugs; versão G30 RC1 não foi alterada.
