# Implantação e portabilidade

Este diretório documenta apenas o contrato público de implantação da plataforma.

A aplicação deve ser reproduzível sem depender de uma conta Cloudflare específica. Detalhes operacionais de produção — credenciais, IDs de conta, IDs de banco, IDs de buckets, rotas, zonas DNS, tokens, nomes internos, subdomínios não públicos e procedimentos administrativos — não pertencem ao repositório público.

## Princípio

O núcleo da plataforma possui quatro contratos:

1. arquivos estáticos gerados pelo build;
2. uma API HTTP opcional para consultas dinâmicas;
3. um banco SQL compatível com o esquema publicado;
4. armazenamento de objetos opcional para snapshots e exportações.

A implementação inicial poderá usar Cloudflare, mas outro ambiente deve poder reproduzir esses contratos.

## Desenvolvimento local

A referência local usa:

- Python para pipeline;
- SQLite para a base canônica;
- servidor HTTP local para o frontend e API;
- diretório local para artefatos equivalentes ao armazenamento de objetos.

## Produção

A configuração de produção deve ser injetada por variáveis de ambiente, bindings ou secret stores do provedor.

Nunca versionar:

- tokens;
- chaves;
- senhas;
- account IDs associados à operação privada quando desnecessários;
- database IDs reais;
- bucket IDs ou nomes privados;
- zone IDs;
- rotas administrativas;
- conteúdo de `.dev.vars`;
- `wrangler.toml` de produção.

## Cloudflare

O repositório pode conter apenas:

- `wrangler.example.toml`;
- nomes lógicos de bindings;
- documentação da interface esperada;
- instruções genéricas de build/deploy.

A configuração real deverá existir apenas no ambiente privado de operação.

## Regra de portabilidade

Nenhum módulo de domínio ou pipeline pode depender diretamente de APIs Cloudflare. Integrações de provedor devem ficar confinadas à camada de deployment/adapters.
