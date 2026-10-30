# RMRP — Verificação da paginação após integração do mapa 15 — 29/10/2026

Documento editável: https://docs.google.com/document/d/19qwSxQuy_1N4XEPqfpWgJrNB371WxiJwLfQad6oaIsI/edit

## Correção executada

Na prova inicial desta etapa, de 73 páginas, a última página continha apenas duas linhas finais do comentário de Santo Antônio da Alegria. A inspeção da estrutura Google Docs identificou um parágrafo municipal com entrelinha 150%, seguido de dois parágrafos vazios finais.

Na cópia de trabalho foram realizados: ajuste localizado do comentário final para entrelinha de 120% e espaçamento acima/abaixo reduzido, remoção de parágrafo vazio excedente e eliminação da quebra final que gerava página suplementar. Nenhum dado numérico ou texto substantivo foi modificado.

## QA de retorno

Nova exportação PDF: **72 páginas**. A página final contém o comentário completo de Santo Antônio da Alegria, encerrando com a participação de 3,32% dos investimentos da sub-região 4. A 73ª página vazia foi eliminada.

Leitura programática de PDF por PyMuPDF identificou **16 páginas com imagens**, todas com ocorrência de legenda "Figura" na própria página: 5, 7, 11, 15, 17, 18, 20, 31, 32, 34, 35, 36, 37, 38, 39 e 41. Não foram identificadas páginas com menos de 220 caracteres de texto que estivessem desprovidas de imagens. A verificação heurística também não encontrou excesso de repetição de cabeçalho anual na mesma página. Isso é controle de estrutura, **não certificação visual integral de todas as tabelas e legendas**.

Google Docs já havia registrado 52 tabelas nativas, 16 imagens e 34 fichas; recomenda-se reler o documento para assegurar as contagens após o ajuste.

## Pendências

1. Inspeção visual final das tabelas municipais que cruzam páginas, evitando fragmentação de cabeçalhos e linhas isoladas; divisão legítima com cabeçalho repetido pode ser aceita.
2. Revisão editorial de duplicações e ordem de capítulos: abertura inicial (1–9), análises complementares (10–13) e fichas; não reorganizar sem comparar referências internas e sumário.
3. Prova final de legibilidade em tamanho de impressão, inclusive dos cinco intervalos numéricos do mapa 15.
4. Homologação e publicação somente após decisão expressa; preservar documento original.
