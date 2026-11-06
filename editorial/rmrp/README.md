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
