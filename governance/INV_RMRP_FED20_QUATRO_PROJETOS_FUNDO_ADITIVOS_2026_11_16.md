# FED20 — comprovação fundiária e aditivos de quatro projetos na RMRP

**Execução:** 16/11/2026. **Snapshot original:** 15/11/2026. **Objetivo:** ampliar a cobertura documental dos 19 projetos prioritários com divergência entre município proponente e coordenadas de proposta, preservando a separação entre terreno destinado, instrumento contratual e execução efetivamente comprovada.

Após o FED19, **16 dos 19 projetos prioritários** foram examinados com algum grau de documentação independente, restando **três** sem essa evidência adicional nesta série. Esta métrica de cobertura significa somente **documentos e vínculos localizados**, não 16 obras executadas nem 16 localizações físicas homologadas.

## 1. Dumont — unidades habitacionais, termo 992467/2025

O projeto Obrasgov `113452.35-68` possui vínculo oficial ao termo de compromisso **992467/2025** do Programa Minha Casa Minha Vida.

A **[Lei Municipal nº 2.000, de 10/04/2026](https://www.dumont.sp.gov.br/portal/leis_decretos/6185/)**, publicada no portal oficial de Dumont, desafeta uma área institucional e a transforma em bem dominial municipal para implantação de moradias **expressamente vinculadas ao termo 992467/2025/MCIDADES/CAIXA**.

A norma fornece identificação imobiliária de precisão cadastral superior à simples coordenada de proposta:

- **Área Institucional 01**, loteamento **Reserva do Alto**, Dumont/SP;
- **Área total: 5.706,61 m²**;
- **Matrícula: 88.873**, Registro de Imóveis da Comarca de Sertãozinho;
- Frente para **Rua 08**, lado ímpar, e confrontações com ruas 07 e 02 e propriedades adjacentes, acompanhadas de rumos/distâncias.

**Status homologável:** identificação jurídica **do imóvel destinado** ao empreendimento, incluindo matrícula, área e descrição de perímetro. **Não homologar polígono geométrico** a partir de confrontações textuais sem planta/marcos coordenados e referencial cartográfico; a destinação legal não constitui certificado de construção ou implantação das moradias.

## 2. Barrinha — implantação de calçadas, repasse 953046/2023

Projeto Obrasgov `30843.35-03`, instrumento `953046`.

Extrato do Diário Oficial da União, de 26/12/2023, cuja cópia está hospedada por [portal municipal que conserva a edição do DOU](https://pastosbons.ma.gov.br/anexos-bkp/convenios/952783/952783_6_dou_26_12_2023.pdf), identifica o **Contrato de Repasse 953046/2023**, Ministério das Cidades/CAIXA, **implantação de calçadas**, programa Mobilidade Urbana:

- **Valor global firmado:** R$ 500.000,00;
- **Repasse federal previsto:** R$ 481.104,00;
- **Contrapartida prevista:** R$ 18.896,00.

**Não são valores de pagamento final**, e não há trechos de calçada nem geometrias lineares localizadas na fonte. Os números permanecem rotulados como valores de assinatura. É necessário obter memorial, planilha de vias e trechos medidos antes de espacialização.

## 3. Jaboticabal — construção de DAFAs, termo 969302/2024

Projeto Obrasgov `46797.35-41`, instrumento `969302`.

O [Diário Oficial da União, edição de 10/10/2025, Seção 3, p. 79](https://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?captchafield=firstAccess&data=10%2F10%2F2025&jornal=530&pagina=79), traz **termo aditivo de 07/10/2025** relativo à Prefeitura de Jaboticabal/SP com **alteração de repasse e contrapartida para R$ 1.013.465,89 e R$ 0,00**, respectivamente.

**Limite:** a informação refere-se a alteração orçamentária do instrumento; não constitui demonstração de desembolso, pagamento ou implantação física de DAFAs. O local exato dos dispositivos continua não documentado nesta etapa. Não somar o valor de termo aditivo à dotação anterior, nem reclassificar GND4 pago.

## 4. Cravinhos — pavimentação, repasse 939534/2022

Projeto Obrasgov `19211.35-11`, instrumento `939534`.

O [Diário Oficial da União de 21/08/2023, Seção 3](https://www.chapadinha.ma.gov.br/anexos-bkp/convenios/880707/880707_chapadinha_dou_ta_de_contrapartida.pdf), preservado em repositório oficial de outra Prefeitura, contém termo aditivo relativo ao Município de Cravinhos e a **contrapartida de R$ 141.016,62**, datado de **18/08/2023**.

Esse é **valor de contrapartida alterada**, não execução financeira comprovada nem identificação dos trechos da pavimentação. O projeto permanece como **objeto viário linear** a territorializar após documentação de vias e segmentos.

## 5. Qualidade da fonte e incorporação FED20

A fonte de Dumont foi obtida diretamente do site municipal por Crawl2AI, com texto integral de lei, dados registrários e vínculo expresso ao termo. Os extratos do DOU têm origem federal, consultados em arquivo hospedado por portal oficial ou no site da Imprensa Nacional; **não foram confundidos com processos municipais de execução**, e nenhum dos PDFs recebeu atribuição de medição/recibo que não consta de seu extrato. O acesso a versões PDF pelo crawler variou; a persistência nesta fase refere-se à **URL e aos campos auditados na prévia**, não a cópias integrais dos quatro PDFs.

O script [`deployment/build_rmrp_fed20_private.py`](../deployment/build_rmrp_fed20_private.py) adiciona `evidencia_fundiaria_e_aditivos_fed20` a quatro fichas de projeto, sem alterar valores GND4, registros fiscais ou pontos de execução.

[**Prévia privada FED20 no Google Drive**](https://drive.google.com/file/d/1ktBTj3wivE29hbkyaTVAZOSrrbCdf_-p), arquivo `RMRP_FED20_SITE_PREVIA_PRIVADA_2026-11-16.zip`, **828.219 bytes**, SHA-256 `149c5fe34c049bc9477004c52b68cdad7713d8979ceaa1a587e29768b5d8f4eb`. Guardado na pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`; metadados `shared=false`, download de retorno com SHA-256 e CRC verificados.

**Testes:** **1.603 checagens estruturais de API** e **288 requisições HTTP locais** com 285 JSON válidos. Permaneceram 218 projetos, 34 municípios, quatro sub-regiões e 19 exercícios na prévia. As diferenças foram apenas documentais, sem pontos de execução ou valores de GND4 pago preenchidos.

## 6. Priorização do fechamento dos 19 projetos

Restam três projetos prioritários sem fonte documental independente suficientemente ligada ao respectivo instrumento nas etapas FED16–FED20:

1. `50782.35-08`, Santa Rosa de Viterbo, termo **974564**, empreendimento habitacional;
2. `105865.35-77`, Guatapará, termo **996136**, provisão de unidades habitacionais;
3. `30158.35-25`, Jaboticabal, repasse **953339**, reforma de estação de tratamento de esgoto.

**Atenção:** foram localizadas leis de Guatapará referentes a programas habitacionais de **2018/2019**, inclusive imóvel no bairro Mombuca, mas elas **não identificam o termo 996136 de 2026**. Não transferir o endereço/terreno do programa anterior ao projeto atual. Similarmente, referências genéricas a ETE de Jaboticabal não serão associadas ao repasse 953339 sem número de contrato, projeto ou termo que estabeleça a ponte.

Para estes três casos, manter a busca de atos municipais, extratos de edital, projetos básicos e localização efetiva; identificar e classificar documentos **exatos** antes de eventual integração espacial.

**Situação de publicação:** `public_release_authorized=false`; zero pontos de execução física homologados; os indicadores municipais de capital efetivamente pago continuam `null`. A dimensão financeira exige ainda a conciliação dos dois desembolsos do FED11, classificação de GND4 realmente pago e estornos; testes de Cloudflare Pages restrito e revisão visual ainda pendentes.
