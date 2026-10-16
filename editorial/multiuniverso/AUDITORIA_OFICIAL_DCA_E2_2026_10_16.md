# Auditoria documental independente — Siconfi DCA 2025

## Procedimento e resultado
A rotina existente `.github/workflows/siconfi-baseline-crosscheck.yml` foi ampliada para recuperar a DCA diretamente do Siconfi e confrontá-la com os registros `publication/universes/{universo}/municipalities/{codigo_ibge}.json` da API editorial E2.

A verificação seleciona Americana (3501608), Campinas (3509502), Indaiatuba (3520509), Jundiaí (3525904) e Valinhos (3556206). Confronta contas selecionadas de receitas, tributos, investimentos e despesas por funções. Aceita apenas registros oficiais disponíveis e valores classificados como observados na API; aplica tolerância absoluta de R$ 0,01 e relativa de 1e-10.

**Resultado:** 5 municípios, 68 comparações efetivas, nenhuma divergência. GitHub Actions https://github.com/hilaliskandar/mapa_do_tesouro/actions/runs/38896144224, execução concluída com sucesso no commit `9f60cceb086aabce043a7eeb13605a71ca076257`. Artefato `auditoria-dca-oficial-e2` ID `12044136799`, SHA-256 `1353a8e283719e86802ee68f152ba6586d3ae9f4f6cecfa04a2103d0649e2465`. O relatório JSON inclui as 68 observações e o conjunto de divergências vazio.

## Limites
Não se deve extrapolar a aprovação às 280 fichas completas, a todos os exercícios ou aos demonstrativos RGF/RREO/CAPAG. O teste compara fonte oficial DCA reextraída em 2025 contra a API E2 para combinações elegíveis, sem produzir prova sobre registros ausentes ou alterações futuras na fonte. A documentação integra o PR nº 198 e não altera produção.

## Próxima fase
Selecionar amostra RREO/RGF/CAPAG por anexo, município e exercício; conservar captura original, data, status, identificador de origem e tolerância adotada. Exigir auditoria de disponibilidade e ausência antes de declarar conformidade integral.
