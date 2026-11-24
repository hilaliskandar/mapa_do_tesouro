# FED16 — evidências independentes e homologação parcial de local projetado na RMRP

**Processamento em 16/11/2026**, sobre o snapshot nacional Transferegov/Obrasgov de 15/11/2026 e documentos primários municipais e institucionais recuperados por fontes oficiais. **Status:** locais de projeto básico identificados; **local efetivo de execução física ainda não homologado**. Não houve alteração na plataforma pública.

## 1. Avanço técnico e classes distintas

O FED16 separa três noções que não podem ser confundidas:

- **Local previsto e documentado:** coordenada e/ou endereço explicitamente constantes de edital/projeto básico oficial, com vínculo inequívoco a instrumento e objeto. **Pode** integrar cadastro restrito de projeto previsto, com advertência de datum e precisão.
- **Município/local corroborado por relatório de execução:** fonte municipal ou institucional descreve a obra efetivamente em andamento, mas a vinculação ao instrumento e as coordenadas materiais podem precisar de prova adicional.
- **Local de execução física homologado:** endereço/trecho/coordenada sustentado por comprovação de efetiva execução — por exemplo, medição georreferenciada, relatório de fiscalização, termo de recebimento, as built ou foto institucional com vínculo identificável. **Nenhum novo registro atingiu esta classe**.

A auditoria segue usando o ponto cadastral SICONV somente como **candidato**, sem promover suas coordenadas automaticamente à execução.

## 2. Monte Alto — contrato de repasse 870332/2018, projeto Obrasgov 33889.35-28

O projeto Obrasgov `33889.35-28` corresponde à proposta `1347060`, instrumento `870332` e município proponente **Monte Alto (IBGE 3531308)**. O edital oficial da Prefeitura de Monte Alto, **Tomada de Preços 4/2022, Processo SA/DL 38/2022**, identifica expressamente o contrato de repasse OGU `870332/2018` e contém projeto básico com **dois componentes** nos seguintes locais:

| Componente planejado | Endereço do projeto básico | DMS da fonte | Decimal derivado somente para QA |
|---|---|---|---|
| Revitalização da Praça São Benedito | Praça São Benedito, Largo do Batismo, Centro, Monte Alto/SP | 21°15'41,46'' S; 48°29'20,80'' W | Latitude -21,26151667; longitude -48,48911111 |
| Centro de Apoio ao Turista | Rua Dr. Raul da Rocha Medeiros, 1490, Centro, Monte Alto/SP | 21°15'41,5'' S; 48°29'49,9'' W | Latitude -21,26152778; longitude -48,49719444 |

**Fonte original:** [Edital e Anexo II — Projeto Básico de Monte Alto, 2022](https://montealto.sp.gov.br/site/wp-content/uploads/2022/04/EDITAL-REV-PCA-S.-BENEDITO-C.-APOIO.pdf), **páginas 36 e 37**. O arquivo PDF original foi baixado, validado como PDF e lido diretamente por página; a cópia consta do ZIP privado FED16. SHA-256 da fonte: `7e8f320a91c740d779250f50aeb7bb25907dfa501ea79cf1bb5e653a12fc72`.

O PDF **não declara o datum geodésico** dessas coordenadas. A transformação textual DMS→graus decimais, portanto, **não constitui reprojeção para EPSG:4674**, nem garante acurácia submétrica absoluta.

### Confronto com os dois registros de coordenada da proposta

- Ponto SICONV `(-21,26152; -48,49719)`, dentro do município de Monte Alto, coincide numericamente, por distância de Haversine, a aproximadamente **0,98 m** da coordenada DMS informada no projeto básico para o **Centro de Apoio ao Turista**. A proximidade demonstra forte **consistência entre cadastros do local projetado**, sem provar a execução nem a precisão geodésica real.
- Outro ponto SICONV `(-7,16775; -35,35091)`, fora de São Paulo, está aproximadamente **2.109 km** da coordenada municipal oficial da **Praça São Benedito**. O ponto é **incompatível com o local projetado** no documento municipal. Conservar o original no staging; recusar seu uso como localização da obra.
- A Praça São Benedito tem coordenada planejada distinta da do Centro de Apoio ao Turista. Não usar o ponto cadastral do CAT como ponto único de todo o empreendimento.

**Resultado homologável:** dois **locais projetados documentalmente**, um deles corroborado por coordenada cadastrada em proposta. **Não homologar dois pontos de obra executada**, pois falta a prova da implantação efetiva nos locais/termos documentados.

## 3. Sertãozinho — projeto 125271.35-26, instrumento 839481

O projeto `125271.35-26`, proposta `1122551`, instrumento `839481`, município proponente **Sertãozinho (IBGE 3551702)** refere-se à cobertura e arquibancada de quadra na **Praça Franco**.

A [notícia oficial da Prefeitura de Sertãozinho de 22/09/2017](https://www.sertaozinho.sp.gov.br/portal/noticias/0/3/3145/prefeitura-investe-em-infraestrutura-esportiva-em-diferentes-regioes-da-cidade) identifica **Praça Franco Montoro**, **Conjunto Habitacional Antônio Pedro Ortolan (Cohab 3)**, e relata a **execução** de adequações, cobertura e arquibancada por empresa contratada, com valor jornalístico de R$ 386.387,77. A matéria foi recuperada e preservada como HTML no ZIP privado. SHA-256 da cópia: `cf3e3cf90428d19d9584c20ce0dc4567420003d8de2d7da4f904eb391e27fde6`.

A fonte oficial corrobora **município e instalação** com alta correspondência do objeto, e é incompatível com tratar o ponto SICONV `(-23,50675; -46,28242)`, situado em **Suzano**, como a quadra de Sertãozinho. **Ressalva:** a notícia não informa o número de contrato de repasse `839481`; logo, não está comprovado por essa peça isolada que o relato da execução corresponda financeiramente ao mesmo instrumento, ainda que objeto/local coincidam. Não atribuir este valor jornalístico a pagamento de fonte federal nem criar ponto geográfico artificial.

**Resultado:** corroborado **local municipal descritivo**, pendente elo explícito com instrumento e documento de conclusão/medição georreferenciada. Coordenada de Suzano mantida como **não utilizável para execução**.

## 4. Ribeirão Preto — projeto 31534.35-57, instrumento 953325

O projeto `31534.35-57`, proposta `1950015`, instrumento `953325`, refere-se à reforma de unidade de hematologia/hemoterapia da Fundação Hemocentro de Ribeirão Preto.

O [Relatório de Controle Interno da Fundação Hemocentro de Ribeirão Preto, exercício 2023](https://www.hemocentro.fmrp.usp.br/wp-content/uploads/2024/05/Relatorio-de-Controle-Interno-Exercicio-2023.pdf) relaciona o instrumento **953325/2023** e o objeto de reforma, com valor aprovado de **R$ 385.460,00**. A instituição também menciona o instrumento em suas demonstrações contábeis posteriores. São **evidências de financiamento/objeto**, não de endereço exato ou execução georreferenciada.

O SICONV apresenta dois pontos candidatos associados à proposta: um em **Ribeirão Preto** e outro em **Fernandópolis**. Não foi recuperado documento capaz de atribuir execução física específica ao endereço de qualquer dos dois. Ambos permanecem como candidatos, sem promoção geográfica. **Não confundir esse instrumento de 2023 com o convênio 905339/2020**, também relativo a reforma de unidade de hematologia/hemoterapia.

## 5. FED16 — integração e persistência

Código de execução reprodutível: [`pipeline/qa/build_rmrp_fed16_independent_local_evidence.py`](../pipeline/qa/build_rmrp_fed16_independent_local_evidence.py). O script valida os identificadores de três projetos, verifica o texto das páginas 36/37 do edital de Monte Alto, converte as coordenadas DMS para decimais sem assumir datum, calcula distâncias aproximadas e acrescenta aos três JSON individuais o objeto `evidencia_independente_fed16`.

**Gate técnico da prévia**: 1.603 verificações da API aprovadas; 288 respostas HTTP 200 locais, com 285 JSON válidos. Foram preservados **218 projetos**, dos quais **3** receberam evidência independente; **2 coordenadas de projeto básico**, **0 pontos de execução física** e **0 valores de GND4 pago não nulos**. `public_release_authorized=false`.

Arquivos privados preservados no Google Drive, pasta `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`, ambos com `shared=false` e readback SHA-256/CRC conferidos:

- [**FED16 — fontes originais, fichas dos três casos e QA**](https://drive.google.com/file/d/16RezW3GmpRqKOn25maIAJ0HcpCKWTxH1/view): **5.916.124 bytes**, SHA-256 `145b17544c23d58343f2d9af63b996f2767081b5901b30d5ef50ced8311113e6`.
- [**FED16 — prévia privada integrada da plataforma**](https://drive.google.com/file/d/1mZ5DVmfI4QXWM3HqvO9yQL0pa1OyEIq1/view): **816.711 bytes**, SHA-256 `8928105d255cf2c5df78b123d649c151fbef22397070d73a9f66bfefa0028d78`.

## 6. Próximos gates de homologação

1. Para Monte Alto, buscar **termo de recebimento, medições, relatório da fiscalização ou comprovação de execução** vinculado ao contrato 870332/2018 e aos dois componentes. Apenas então avaliar pins de execução; manter a distinção entre locais planejados e executados.
2. Para Sertãozinho, obter **edital, contrato, ART, medições ou termo de conclusão** que vincule explicitamente o contrato de repasse 839481 à quadra da Praça Franco Montoro. Não usar ponto localizado em Suzano.
3. Para a Fundação Hemocentro, recuperar projeto executivo/medições do instrumento 953325/2023 e seus locais de intervenção, distinguindo sede, unidade beneficiária e eventual rede descentralizada; não inferir Ribeirão Preto como ponto único.
4. Continuar o exame dos outros **16 projetos** espacialmente divergentes por documentos individualizados; não reduzir a pendência a zero com inferências cadastrais.
5. Na dimensão financeira, avançar na evidência SIAFI dos dois desembolsos não conciliados, natureza de despesa de pagamento final e estornos; os grupos de empenho por natureza não equivalem a capital efetivamente pago.
6. Executar teste visual e release de prévia restrita Pages antes de qualquer modificação pública.

**Publicação pública não autorizada.** A mudança nesta etapa é qualitativa: **dois locais previstos do projeto básico** têm coordenadas de origem oficial e rastreabilidade documental verificadas; **zero locais de execução física** atingiram a prova substantiva exigida.
