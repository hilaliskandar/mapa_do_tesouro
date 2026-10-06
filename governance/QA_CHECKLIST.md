# Checklist de QA

Uma versão só pode ser promovida quando:

## Integridade
- [ ] esquema válido;
- [ ] chaves municipais válidas;
- [ ] anos esperados presentes;
- [ ] duplicidades críticas ausentes;
- [ ] ausência não convertida em zero;
- [ ] cobertura registrada.

## Metodologia
- [ ] variáveis com definição e unidade;
- [ ] indicadores com fórmula e componentes;
- [ ] indicadores legais usam demonstrativos próprios quando aplicável;
- [ ] crosswalk temporal documentado;
- [ ] alterações metodológicas versionadas.

## Paridade
- [ ] resultados reconciliados com a base canônica anterior;
- [ ] divergências explicadas;
- [ ] SHA-256 registrado.

## Funcional
- [ ] requisitos F101–F116 testados;
- [ ] mapa funcional;
- [ ] séries funcionais;
- [ ] exportação funcional;
- [ ] fontes e metodologia acessíveis.

## Segurança e implantação
- [ ] nenhum segredo no Git;
- [ ] configuração de produção fora do repositório;
- [ ] ambiente local reproduzível sem Cloudflare;
- [ ] exemplo de configuração atualizado;
- [ ] rollback documentado.
