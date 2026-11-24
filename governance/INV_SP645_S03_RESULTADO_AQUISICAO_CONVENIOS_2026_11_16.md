# S03 — primeira aquisição e auditoria do ZIP oficial de convênios SP

**Referência:** 16/11/2026; **fonte:** https://www.transparencia.sp.gov.br/Dados%20Abertos/Convenios/convenio.zip; **método:** Crawl2AI para descoberta de URL/contratos HTTP + GitHub Actions como executor com conectividade.

## Evidências verificadas

- O Crawl2AI recuperou o HTML completo do portal, localizou `href="/Dados Abertos/Convenios/convenio.zip"` e verificou que a exportação alternativa `/Convenios/ExportarCsv` é um **POST** de filtro JSON. `GET` ao endpoint de exportação respondeu `405 Allow: POST`.
- Workflow `.github/workflows/sp645-convenios-auditoria.yml` executou em GitHub Actions sem modificar a produção. Execução inicial [43906787228](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43906787228) concluiu com **HTTP 200**, ZIP de **188.630 bytes**, integridade ZIP/CRC aprovada e hash **SHA-256 `1cca0556f08a1378bae52465796188788a5b3bb21e1b26c30c8c5c7d9a6b2b8f`**.
- A inspeção de CSV ocorreu em [43906969870](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43906969870), revelando **ausência de cabeçalho convencional**: leitor `DictReader` havia incorretamente tratado a primeira linha de dados como nomes de colunas. Após correção do leitor e da expressão regular de detecção, a execução [43907251543](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43907251543) concluiu com a contagem correta.
- Arquivo interno: `convenio.csv`, `UTF-8-SIG`, delimitador `;`, **10 campos em 100% das 3.618 linhas**. O **primeiro campo** contém o ano e o **segundo** vale `TRANSFERENCIA VOLUNTARIA` em todos os registros. A quinta posição registra texto de beneficiário, com **1.121 denominações distintas**, que não podem ser interpretadas como municípios sem normalização.
- Contagem pelo primeiro campo: **2023: 323; 2024: 938; 2025: 1.912; 2026: 445**. Total **3.618**.
- Fonte tem escopo estadual e classe única de transferência voluntária no arquivo disponibilizado. **Não comprova cobertura histórica antes de 2023 nem de outras modalidades, e não fornece por si só os valores efetivamente liberados na Sefaz-SP**.

## Gate de persistência e integração

**Download e QA estrutural realizados; persistência privada e normalização ainda pendentes.** O ZIP foi obtido em diretório temporário do GitHub Actions e **não foi salvo no R2/Drive** nem disponibilizado como artefato público (evita disseminação inadvertida de microdados). O arquivo continua recuperável da URL oficial, mas necessita captura canônica com manifesto em depósito privado.

Próximos passos:

1. Configurar o workflow de persistência em **R2 privado** usando credenciais já geridas pelo ambiente, sem incluí-las no código. Reexecutar aquisição, verificar hash e gravar em prefixo versionado; registrar URI e SHA no manifesto.
2. Recuperar o **dicionário oficial** https://www.transparencia.sp.gov.br/Dicionarios/Dicion%C3%A1rio%20de%20dados_conv%C3%AAnios.xlsx e confirmar a correspondência semântica exata das dez colunas; não presumir que o primeiro registro seja cabeçalho.
3. Construir `stg_sp_convenios` com dez colunas de origem + índice de linha + SHA do snapshot, normalização de ano, identificador de instrumento/beneficiário, valor e natureza após QA do dicionário.
4. Auditar cobertura de **645 municípios** e da **RMRP34**, com associação por IBGE7/CNPJ quando existir prova; não tratar 1.121 denominações de beneficiários como municípios distintos.
5. Enfrentar lacuna de **2007–2022** e eventuais 2026 incompletos via Sefaz-SP/SIAFEM e/ou arquivo histórico; comparar instrumento celebrado com liberações efetivas e estornos.
6. Só depois produzir agregado anual e integração privada com FINBRA/TCESP, sem somar origem e aplicação, ou considerar valores celebrados como pagos.

**Status: `qa_status=validado_estrutura`, `qa_financeiro=pendente`, `persistencia_privada=pendente`, `public_release_authorized=false`.**

## Atualização — dicionário e staging confirmados

A execução [43907596415](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43907596415) recuperou com **HTTP 200** o dicionário oficial XLSX de 14.383 bytes. A planilha `Dicionário_convênios` descreve, entre outros, `Número do Convênio`, `CNPJ do Beneficiário`, `Objeto`, `Valor Total do Convênio` (previsto) e `Valor Concedido` (efetivamente repassado). Como a planilha descreve **mais campos do que as dez posições do arquivo ZIP**, os títulos não devem ser aplicados posicionalmente sem verificação adicional.

Criado [`pipeline/coleta/stage_sp_convenios.py`](../pipeline/coleta/stage_sp_convenios.py), que importa o ZIP em SQLite de desenvolvimento sob o grão `(source_sha256,row_num)`, com `year` e `col_01` a `col_10` brutas. O teste local sintético foi executado duas vezes com o mesmo ZIP e não duplicou linhas. A execução real [43907818400](https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/43907818400) concluiu com **3.618 registros** e anos **2023: 323, 2024: 938, 2025: 1.912, 2026: 445**, preservando `financial_schema_homologated=false` e `physical_location_homologated=false`.

**Restrição importante:** o SQLite gerado e o ZIP continuam nos diretórios **temporários** do runner de CI, sem persistência em R2. Logo, o estágio foi **testado com dados reais**, mas ainda não foi incorporado ao banco canônico privado nem à plataforma. A aprovação da estrutura não implica aprovação da semântica financeira.
