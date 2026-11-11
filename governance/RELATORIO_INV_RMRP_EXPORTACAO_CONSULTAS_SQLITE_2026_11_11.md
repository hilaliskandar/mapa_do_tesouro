# INV-RMRP — Contrato de materialização SQLite → JSON estático

**Atualizado em:** 11/11/2026. **Situação:** pipeline implementado e testado com base sintética; **não executado em base canônica real**. PR #233 *draft*.

## 1. Cadeia operacional

1. O importador [`pipeline/build/import_inv_rmrp_obrasgov_dev.py`](../pipeline/build/import_inv_rmrp_obrasgov_dev.py) cria uma cópia não destrutiva do SQLite e associa IDs oficiais Obrasgov, pontos, relações municipais e eventos de valor **previsto** aos 224 candidatos.
2. O exportador [`pipeline/build/export_inv_rmrp_consultas_dev.py`](../pipeline/build/export_inv_rmrp_consultas_dev.py) abre essa cópia em `mode=ro`, exige `integrity_check=ok`, `foreign_key_check=[]` e os 34 códigos IBGE7 do roster. Não altera a entrada e não sobrescreve pasta existente.
3. Materializa uma ficha por município, uma ficha por projeto, índices municipais e manifesto com SHA-256 por arquivo. O identificador no caminho da ficha é derivado do SHA-256 do ID do projeto; dentro do JSON permanece o identificador original, garantindo rastreabilidade.
4. A política de exportação preserva valores de `previsto` **somente como eventos candidatos**, enquanto os campos de investimento público executado e transferências efetivamente pagas permanecem `null` quando inexistentes. Qualquer evento `pago`, `transferido` ou `liquidado` sem `qa_status=homologado` bloqueia a geração; registros rejeitados também bloqueiam.
5. O manifesto informa contagens, versão do contrato, limitações de cobertura e hashes de cada JSON. Não publicar diretamente `dev_only_non_published_candidates` como se fosse base financeira homologada.

## 2. Testes realizados

GitHub Actions: [INV RMRP QA de coletores sem rede, execução nº 43072837793](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43072837793), resultado **success**. Foram testados em SQLite sintética montada a partir do esquema oficial do repositório:

- Importação de 224 projetos, 132 vínculos territoriais e 226 eventos de previsão;
- Exportação de **34 consultas por código IBGE7** e **224 fichas individuais**;
- Manifesto, integridade referencial, precisão em centavos e arquivos com hashes;
- Campos de investimento público executado e transferências pagas permanecem `null` no recorte piloto ainda sem comprovação;
- Recusa a sobrescrever pasta de saída e preservação da SQLite de origem;
- Rejeição da exportação quando um evento é rotulado como `pago` sem homologação.

**Esses testes demonstram consistência operacional, não a existência de transferências ou pagamentos comprovados.** A prévia atual Cloudflare PR #233 usa o JSON amostral diretamente da branch; o novo exportador ainda não fornece seus arquivos à implantação remota, pois a base canônica real e a aquisição integral continuam pendentes.

## 3. Próximos gates

- **INV-RMRP-D1:** criar snapshot integral das fontes federais — Transferegov 34×2 e Obrasgov/SP — com manifestos, SHA-256 e readback. As contagens anteriores não substituem a captura dos originais.
- **INV-RMRP-D2:** adquirir convênios e liberações estaduais SIAFEM/SP, transferências especiais e ordens bancárias federais por identificador. Separar custeio/investimento, previsto/empenhado/pago/transferido.
- **INV-RMRP-D3:** disponibilizar uma cópia verificável do SQLite canônico **em ambiente autorizado**, validar seu esquema e integrar os registros sem escrever no arquivo de origem.
- **INV-RMRP-D4:** gerar JSON da base de desenvolvimento, comparar agregados fiscalmente consistentes com as séries TCESP/DCA já existentes e submeter 50 consultas de regressão.
- **INV-RMRP-D5:** homologar espacialmente coordenadas discrepantes ou ausentes, especialmente os sete casos de desacordo texto×ponto; somente após evidência financeira e territorial pertinente avaliar indicadores consolidados ou publicação.

## 4. Restrições preservadas

- A PR #233 e o FED04/PR #232 permanecem independentes e em andamento.
- Nenhum pagamento foi inferido de valor previsto, empenho ou situação de obra.
- Não foram atualizados SQLite/R2/D1 produtivos; não houve merge nem homologação financeira.
