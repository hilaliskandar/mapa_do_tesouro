# FED04D e FED03E — hierarquia de evidência territorial e triagem financeira

**Data do snapshot:** 15/11/2026. **Execução:** dados oficiais Transferegov, Obrasgov e malha municipal IBGE 2024 SIRGAS 2000 (EPSG:4674), sobre a cópia privada FED04C. Todos os identificadores individuais e pares de coordenadas estão somente no Drive privado. **Não é homologação de execução física, de investimento de capital nem análise de irregularidades.**

## FED04D — qualidade das 441 coordenadas

A auditoria distinguiu a **coordenada cadastrada na proposta** dos instrumentos e projetos a que pode ser vinculada por chaves oficiais. O resultado conserva exatamente 441 linhas:

| Nível da evidência | Coordenadas |
|---|---:|
| Proposta associada documentalmente a projeto Obrasgov, via instrumento e convênio | **336** |
| Proposta com convênio, mas sem projeto Obrasgov identificado no universo de 218 | **24** |
| Proposta sem convênio identificado na base de 1.793 instrumentos | **81** |
| **Total** | **441** |

**Nenhuma dessas categorias comprova, isoladamente, execução física no ponto.** Os 336 registros são evidências candidatas documentalmente mais fortes, não pontos cartográficos homologados. Nesse subconjunto, **331 coordenadas intersectam a RMRP** e **216 dos 218 projetos** possuem ao menos uma dessas coordenadas na região.

### Reclassificação das divergências espaciais

Das **60 coordenadas** que não coincidem com o município proponente, 36 pertencem a propostas **sem convênio identificado**: 34 em outro município da RMRP e 2 em outro município paulista. Outras 4 pertencem a propostas com convênio, sem projeto Obrasgov no recorte (2 fora de São Paulo e 2 com coordenadas `0,0`). As **20 restantes** pertencem a propostas documentalmente associadas a projetos Obrasgov (15 em outros municípios da RMRP, 3 em outros municípios paulistas e 2 fora de SP).

Uma única proposta da Prefeitura de Ribeirão Preto, referente à aquisição de equipamentos de videomonitoramento, concentra **30 coordenadas localizadas em Altinópolis**. A situação registrada no Transferegov é `Proposta/Plano de Trabalho Rejeitados`; essa proposta **não possui convênio nem projeto Obrasgov associado no recorte**. Portanto, tais 30 coordenadas não podem ser apresentadas como obras executadas em Altinópolis. Este caso representa concentração cadastral a ser examinada, não demonstra fraude, erro intencional ou efetiva execução intermunicipal.

Há **34 pontos distribuídos entre cinco propostas rejeitadas** (incluindo situações com impedimento técnico). Propostas rejeitadas devem permanecer como evidência histórica, fora de qualquer mapa de investimentos executados até documentação que comprove situação posterior diversa. A correção cartográfica anterior de 381/49/5/4/2 continua válida como interseção geográfica; o novo controle acrescenta a situação administrativa e os elos documentais.

## FED03E — revisão preliminar de DL não ativo

Dos **34 pagamentos** vinculados a documentos de liquidação com status diferente de `Ativo`:
- **26 movimentos possuem valor zero**, todos ligados a documentos `Inativo`;
- **8 movimentos apresentam valor positivo**, sendo 6 vinculados a DL `Em Elaboração` e 2 a DL `Inativo`, somando **27.212.091 centavos (R$ 272.120,91)**.

A soma corresponde a R$ 272.120,91 em movimentos com status documental a verificar, não a prejuízo nem a pagamento indevido comprovado.

A classificação observada nos dois recortes elimina a falsa equivalência entre `DL Inativo` e pagamento necessariamente irregular: 26 dos 28 movimentos associados a DL inativo têm valor zero. Os oito casos com valor positivo foram segregados em planilha privada de triagem para revisão documental e cronológica.

## QA e persistência

O SQLite de desenvolvimento `RMRP_FED04D_EVIDENCIAS_STAGING_2026-11-15.sqlite` conserva as tabelas anteriores e adiciona `classificacao_evidencia_coordenada_fed04d` (441 linhas). `PRAGMA integrity_check=ok`, zero violações de chave estrangeira. O pacote inclui dois CSV privados de casos individuais: `FED04D_COORDENADAS_PENDENCIAS_PRIVADO.csv` e `FED03E_DL_NAO_ATIVO_POSITIVOS_PRIVADO.csv`, além de `RMRP_FED04D_FED03E_QA_2026-11-15.json`.

[**Pacote privado FED04D/FED03E no Drive**](https://drive.google.com/file/d/1qQ2nidb5u3M8fXEULYhQoHBVKI_g4ETH/view) — 5.553.517 bytes, SHA-256 `e398a4aed54867a218b5e8a3b37c688d621bc360cb7839e347dedc2c029f86f3`, upload e readback SHA-256/CRC aprovados, acesso `shared=false` na pasta privada `186Cxxs2wZas55LlEPPoD-G2_nJfGmfU9`.

## Próximos gates

1. Auditar especificamente as **20 divergências com vínculo a projetos Obrasgov**, inspecionando a documentação da execução. Tratar as 36 divergências sem convênio como registros de proposta, não como obras.
2. Confrontar os **8 pagamentos positivos** associados a DL não ativo com situação do instrumento, emissão, fornecedor, eventuais anulações, estornos/devoluções e documentos oficiais. Não extrapolar para universo inteiro.
3. Para cálculo de investimento de capital efetivamente pago, localizar e validar ponte de natureza de despesa GND4 nos itens/documentos; a soma nominal dos pagamentos (R$ 627,29 milhões) não é indicador de investimento pago homologado.
4. Manter `public_release_authorized=false`, separar componentes de prévia dos produtos homologados e preservar cronologia de evidências.
