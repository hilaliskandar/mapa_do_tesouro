# INV-RMRP — Verificação das fontes estaduais de convênios e liberações

**Consulta:** 11/11/2026, fontes oficiais, busca web e extração Crawl2AI. **Caráter:** inventário operacional, ainda sem extração de linhas financeiras.

## Fonte A — Portal da Transparência SP
- URL: https://www.transparencia.sp.gov.br/Convenios/Index
- Atualização anunciada: 10/11/2026 11:03.
- Filtros de órgão, unidade, beneficiário, CNPJ, tipo de instrumento e ano de celebração. Portal oferece exportação CSV/PDF, Dados Abertos e dicionário: https://www.transparencia.sp.gov.br/Dicionarios/Dicion%C3%A1rio%20de%20dados_conv%C3%AAnios.xlsx
- O Crawl2AI confirmou esses controles e dicionário, mas não recuperou nesta leitura o endereço exato do CSV de dados abertos. **Status: descoberta confirmada; link e esquema real de descarga pendentes.**
- Gate: verificar endpoint real do CSV com navegador/JS, obter amostra, ler dicionário e conferir universo.

## Fonte B — Sefaz-SP/SIAFEM, Transferências Voluntárias
- URL: https://www.fazenda.sp.gov.br/TransferenciaVoluntaria/Sistema/Novo/PesquisaComposta.aspx
- Busca pública informou atualização em 11/11/2026; mostra instrumentos com alguma liberação financeira desde agosto de 2007, distingue custeio/investimento e registra valores negativos associados a cancelamentos ou estornos.
- **Falha de extração direta:** Crawl2AI recebeu página ASP.NET de erro de aplicação. Nenhuma tabela de liberações foi recuperada nem homologada nesta etapa.
- A Região Administrativa de Ribeirão Preto NÃO equivale ao universo de 34 municípios da RMRP; usar sempre códigos IBGE7 do cadastro do piloto.

## Contrato conceitual
1. Instrumento: órgão, convenente, identificador, objeto, modalidade, data, valor previsto e proveniência.
2. Evento financeiro: identificador de instrumento, data de liberação, valor em centavos, sinal, deduções/estornos e prova de origem, se disponíveis.
3. Territorialização: separar sede do convenente, município beneficiário, executor e localização da obra. Proibir rateio arbitrário.
4. Integridade: versionar fontes, capturas, hashes, contagem de linhas, chaves e atualização declarada. Ausência não equivale a zero.
5. Não aditividade: convênio, liberação e despesa municipal subsequente não são três investimentos independentes.
6. Persistência: aquisição e staging isolados na PR #233; sem alterações no banco canônico.

**Próximo gate:** localizar o CSV completo na fonte A e seu dicionário; testar lote municipal RMRP; depois procurar alternativa confiável de acesso aos lançamentos da fonte B. A mera existência do botão Exportar CSV não é prova de download concluído.
