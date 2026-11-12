# INV-RMRP — Triagem documental de convênios SIAFEM e projetos Obrasgov

**Data da auditoria:** 12/11/2026. **Situação:** triagem concluída, sem qualquer vínculo financeiro homologado, PR nº 233 isolada.

## 1. Ampliação efetiva da base documental

A base estadual já dispunha de 752 instrumentos distintos, 889 linhas instrumento–ano e R$ 305.521.029,20 em liberações/estornos no período 2020–12/11/2026. O detalhamento documental adicional examinou **todos os 752 instrumentos**, com extração do **objeto oficial, órgão estadual concedente e situação** de **747 páginas individuais SIAFEM**.

Foram preservados oito lotes de origem, em `governance/inv_rmrp_siafem_objetos/lote_01...lote_08_2026_11_12.json`. O arquivo consolidado `governance/INV_RMRP_SIAFEM_752_CONVENIOS_METADADOS_OBJETOS_ORGAOS_2026_11_12.csv` mantém 752 chaves e cinco exceções, sem preencher artificialmente os objetos indisponíveis.

Os cinco convênios cujas páginas individuais continuam inacessíveis são os mesmos já identificados na conciliação de pagamentos: `5128032684769\19` (Altinópolis), `5128032447861\19` (Batatais), `51010936677718 A` (Cássia dos Coqueiros), `5128031465476\19` (Guariba) e `512803165957\18C` (Monte Alto). Seus valores por instrumento/ano continuam recuperados com centavos pelo **formulário anual oficial**, embora o conteúdo do objeto e o órgão concedente não tenham sido recuperados.

A falha transitória de navegação que afetou o último lote (52 registros de Tambaú e Taquaral) foi resolvida mediante nova sessão com página do mesmo domínio e repetição controlada: **52/52 páginas recuperadas**. Não confundir essa falha transitória com os cinco erros de aplicação persistentes.

## 2. Confronto inicial com Obrasgov

O conjunto disponível de Obrasgov compreende **224 projetos capturados por pesquisa nominal**, não um inventário exaustivo de projetos metropolitanos; 130 têm ponto interseccionado com polígono de um único município da RMRP, 61 pontos ficaram fora das malhas, 32 não têm coordenadas válidas e um projeto apresenta pontos em múltiplos municípios.

Dos 130 projetos com município espacialmente único, **55 têm fonte prevista classificada como estadual**, em 22 municípios. Os oito tipos de órgãos executores identificados nesse grupo são entidades estaduais, e nenhum traz Prefeitura como organização responsável no extrato. A rubrica "fonte estadual" **não** basta para provar que se trata de transferência voluntária do SIAFEM a uma prefeitura. Sem número comum de instrumento e documentação adicional, não foi estabelecida identidade de financiamento.

A comparação literal dos números de convênios SIAFEM com nomes e descrições Obrasgov produziu **zero correspondências exatas**. A procura dos identificadores dos 284 planos federais de transferências especiais também não produziu chave literal comum nos títulos e descrições Obrasgov disponíveis. Essa ausência **não prova** que não existam vínculos nos documentos originais completos.

## 3. Revisão da similaridade textual

Após ler os objetos oficiais SIAFEM de 747 instrumentos, foram triados pares por **mesmo código IBGE do ponto atribuído a um município único, pelo menos dois termos materiais em comum e razão mínima de 0,5 dos termos distintivos do texto mais curto**. Termos administrativos genéricos, nomes dos municípios, "infraestrutura", "obra", "investimento" e afins foram removidos do vocabulário do pareamento. Resultaram **17 pares de interesse**, com **nenhum vínculo financeiro confirmado**.

| Classificação de triagem | Pares | Interpretação |
|---|---:|---|
| `CANDIDATO_SEM_CHAVE_DOCUMENTAL` | 10 | Assunto possivelmente semelhante (sobretudo recapeamento), mas não há identificador comum de projeto, convênio ou contrato |
| `OBJETOS_DISTINTOS` | 4 | Títulos revelam equipamentos ou bairros diferentes (creche versus praça, centro cultural versus centro de convivência, Jardins distintos) |
| `LOCALIZACOES_DISTINTAS` | 1 | Objeto SIAFEM cita intervenção na Avenida Liberdade; projeto Obrasgov cita ponte da Vicinal Alpheu Belodi |
| `DIVERGENCIA_TERRITORIAL` | 2 | Projeto menciona Barrinha, mas ponto foi associado ao território de Sertãozinho; requer auditoria da localização |

Os 17 pares são identificados nominalmente na matriz `governance/INV_RMRP_SIAFEM_OBRASGOV_17_PARES_CANDIDATOS_NAO_HOMOLOGADOS_2026_11_12.csv`. A classificação "objetos distintos" é fundada nos textos publicados, não em vistoria física; documentos posteriores podem modificar a interpretação. Os dez pares remanescentes são **prioridade para revisão documental**, nunca vínculos homologados.

Entre os casos que merecem verificação individual estão os recapeamentos de Guariba, Santa Rita do Passa Quatro, Serrana e Sertãozinho. A coincidência de tema e cidade é particularmente fraca para obras de pavimentação recorrentes, com possibilidade de diferentes trechos, exercícios e fontes. Os projetos Obrasgov dos 17 pares indicam fonte federal ou federal/municipal no extrato, enquanto o SIAFEM trata de convênios estaduais: cofinanciamento é possível, mas **não pode ser presumido**.

## 4. Controle de qualidade e proibição de vínculos espúrios

Os arquivos e a classificação foram verificados por `pipeline/qa/qa_inv_rmrp_candidatos_siafem_obrasgov.py`, executado no workflow `.github/workflows/inv-rmrp-candidatos-siafem-obrasgov-qa.yml`. O [GitHub Actions 43244736519](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43244736519) terminou em **success**.

O validador exige: 752 chaves únicas de convênio, 747 objetos recuperados, cinco erros explícitos, 17 pares únicos, coincidência dos textos e IDs com seus arquivos oficiais de origem, estados de triagem coerentes e **zero vínculos financeiros confirmados**. Proíbe promoção silenciosa de registros por similaridade, município, coordenada ou rubrica de origem prevista.

A matriz financeira SIAFEM **não** foi alterada: permanecem 752 convênios, 889 registros instrumento–ano, 1.017 pagamentos contabilizados e R$ 305.521.029,20, sem atribuição a projetos específicos. Tampouco foram alterados os projetos Obrasgov, a base DCA, o SQLite e a implantação produtiva.

## 5. Próximas tarefas

1. Para os dez candidatos textuais, localizar documentação de obras e convênios com **número de instrumento, contrato, processo administrativo, endereço/trecho, objeto técnico e executor**. Tratar cada par como hipótese a falsificar.
2. Nos dois casos de Barrinha/Sertãozinho, verificar coordenadas e localização oficial do projeto antes de qualquer aproximação documental.
3. Pesquisar individualmente os cinco objetos de convênios indisponíveis no SIAFEM, sem inferir objeto com base em órgão, valor ou ano.
4. Somente criar relação `inv_instrumento_projeto` se existir prova documental inequívoca, registrando origem e nível de confiança; nunca somar custo previsto, transferência, empenho e liquidação como parcelas aditivas.
5. Manter a quinta página SIAFEM em prévia isolada e usar a presente auditoria como gate de não dupla contagem.

**Governança:** PR nº 233 permanece em draft, sem merge, sem alteração do R2/D1/SQLite produtivo; PR nº 232/FED04 preservada.
