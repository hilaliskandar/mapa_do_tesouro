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
