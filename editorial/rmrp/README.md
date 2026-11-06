# Finanças municipais da RMRP — README operacional

**Atualizado em 06/11/2026.** Documento de continuidade e trilha de auditoria. A referência de procedimentos detalhados é o [README nativo do projeto no Google Drive](https://docs.google.com/document/d/1e4G6zFFG6bxz_NKJj6yOwiJbkMb2i_MuQ4JLo3DrwlU/edit).

## Regra obrigatória de persistência

Todo produto produzido ou alterado neste projeto deve ser salvo no **Google Drive** e ter o seu **ID, URL, versão e resultado da verificação de existência** incluídos neste README ou no README de continuidade do Drive. Abrange DOCX/PDF, tabelas, CSV, mapas, imagens, ZIP, matrizes, scripts, cadernos e relatórios. Caminhos `sandbox:/` e arquivos temporários não são armazenamento permanente. Não concluir uma etapa como persistida sem upload confirmado e readback de metadados, com conferência de conteúdo quando pertinente. Em caso de falha, informar explicitamente pendência e não inventar link.

Cada gate registra: **data; objetivo; fontes e documentos-base; procedimentos executados; achados quantitativos; produtos e IDs do Drive; hash/manifesto quando cabível; QA; ressalvas; decisões; pendências e próxima etapa**. Preservar versão original e trabalhar em cópia. A cada produto final gerar DOCX editável e prova PDF, quando pertinente, salvar ambos no Drive e reabrir para validação. O histórico de execução deve ser escrito para permitir retomada sem depender de mensagens do chat.

## Volume II — estado em 06/11/2026

- **G29**: última edição integral comprovada no fechamento GitHub, 69 páginas, 45 tabelas, 16 mídias; DOCX/PDF não foram encontrados no Drive. Não substituir por Lote 85. Ver [fechamento G29](FECHAMENTO_G29_REVISAO_PUBLICA_2026_11_06.md).
- **G30**: caderno analítico complementar, com propostas para 34 municípios, quatro sub-regiões e RMRP (39 entradas), 13 páginas. Não incorporado à edição integral G29; pendente de confronto documentado e QA final.
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

**Nota de controle:** os quatro primeiros tiveram readback de metadados no momento da gravação; os cinco restantes ainda devem ser individualmente reabertos em QA. O pacote ZIP não equivale a uma versão G30 do Volume II integral.

## Procedimentos e resultados já registrados

- [G29 — revisão pública](FECHAMENTO_G29_REVISAO_PUBLICA_2026_11_06.md): 39 matrizes, correção de comentários internos, preservação de 45 tabelas e 16 mídias.
- [G30 — caderno municipal](FECHAMENTO_G30_CADERNO_REVISAO_SUBSTANTIVA_2026_11_06.md): análises de 34 municípios.
- [G30 — matrizes territoriais](FECHAMENTO_G30_MATRIZES_TERRITORIAIS_E_SINTESE_2026_11_06.md): quatro sub-regiões e RMRP.
- [G30 — matriz de incorporação](FECHAMENTO_G30_GATE_INCORPORACAO_39_TERRITORIOS_2026_11_06.md): cobertura, cautelas e dependência G29.
- [G30 — QA e hashes](QA_G30_INTEGRIDADE_PACOTE_39_TERRITORIOS_2026_11_06.md): integridade do conjunto.
- [G30 — confronto Drive Lote 85](G30_CONFRONTO_DRIVE_LOTE85_E_GATES_2026_11_06.md): conflitos aparentes de denominadores e cautelas para incorporação.

## Próximo gate

Recuperar **o DOCX exato G29** por identificador permanente (Drive, R2, GitHub Actions ou outro acervo); comparar 39 textos; aplicar mudanças seletivas sobre cópia, sem perder 45 tabelas, 16 mídias, notas fiscais G26 e ajustes G27–G29; renderizar, examinar, armazenar versão DOCX/PDF e anexos no **Drive**, verificar todos os IDs e atualizar os dois READMEs. Não declarar Volume II G30 integral nem homologação enquanto não cumprido.
