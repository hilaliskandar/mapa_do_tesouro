# Paridade DCA historica versus API v2 privada — 18/10/2026

Artefatos comparados: CSV canonico DCA SP645 2013-2025 SHA-256 `67a94313e0f0557bc23f48c78a1396fd02ae10ad7923ea2ac2e5c9f2726f65d5`, convertido sem alteracao de valores em 645 JSONs historicos pelo exportador PR203; pacote privado API v2 `sp645-private-site-38593209824` (execucao Actions 38593209824).

A auditoria percorreu 26 contas DCA x 645 municipios x 13 anos, ou 218010 posicoes. Resultado: 2013-2020, 134160 posicoes nao expostas no artefato API v2; 2021-2024, 67080 posicoes com status `nao_aplicavel` na API v2; 2025, 13712 observacoes numericas exatamente iguais (comparacao Decimal) e 3058 posicoes `ausente` em ambas as fontes. Diferencas monetarias entre valores comparaveis em 2025: zero. Diferencas de status em 2025: zero.

Interpretacao: paridade integral de valor e estado em 2025 para essas 26 variaveis. Nao e prova de paridade para 2013-2024, pois nesses anos a API v2 nao expoe a serie DCA. Os valores de 2013-2025 ja existem no CSV historico. Nao inferir `zero` para ausencias; nao confundir `nao_aplicavel` introduzido pela janela da API com inexistencia do dado historico. A reconciliacao nao aborda demais variaveis RGF, RREO ou CAPAG nem valida comparabilidade historica dos conceitos.

Proximo gate: testar a funcao real `stage()` do PR204 sobre o pacote historico, elaborar contrato de descoberta e QA de paridade das 26 variaveis e so entao habilitar publicacao da extensao, sem sobrescrever os endpoints da API v2.
