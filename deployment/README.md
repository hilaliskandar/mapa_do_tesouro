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


## Publicação estática inicial — Cloudflare Pages

Para a primeira publicação, a opção recomendada é **Pages Direct Upload** do diretório `build/site`.

O fluxo público e reproduzível é:

```bash
# 1. construir localmente / em ambiente autorizado
python -m pipeline.build.build_analytical_database \
  <BASE_MULTIFONTES.xlsx> \
  --database build/financas_municipais_sp.sqlite \
  --site-output build/site \
  --geojson <GEOJSON_MUNICIPAL> \
  --overwrite

# 2. autenticar o Wrangler no ambiente privado
npx wrangler login

# 3. criar o projeto apenas na primeira vez
npx wrangler pages project create

# 4. publicar a pasta pronta
npx wrangler pages deploy build/site --project-name=<PROJECT_NAME>
```

O nome real do projeto, account ID, domínio, token e demais dados operacionais permanecem fora do repositório.

### Por que Pages primeiro

A versão atual é integralmente estática. Usar Worker, D1 ou R2 agora aumentaria a superfície operacional sem requisito funcional correspondente.

A migração futura para Worker Static Assets continua possível caso surja necessidade real de API ou lógica dinâmica.

### Headers

O build gera `build/site/_headers` com proteção contra framing, `nosniff`, política de referrer, bloqueio de câmera/microfone/geolocalização, Content Security Policy restrita ao próprio site e cache HTTP controlado para dados, JS e CSS.

Não editar esse arquivo manualmente na pasta de build: ele é gerado pelo pipeline.


## CI/CD automatizado — Cloudflare Pages

A publicação estática usa dois workflows separados:

- `.github/workflows/pages-preview.yml`: materializa o snapshot de dados já aprovado, sobrepõe o frontend do ref selecionado, executa testes e QA, publica previews de PRs e releases e valida a URL publicada;
- `.github/workflows/pages-production.yml`: somente por `workflow_dispatch`, exige uma tag de release existente, materializa o snapshot aprovado e valida o candidato antes de publicar na branch de produção.

A automação depende apenas de configuração privada no GitHub Actions:

- secret `CLOUDFLARE_API_TOKEN`;
- variable `CLOUDFLARE_ACCOUNT_ID`;
- variable `CLOUDFLARE_PAGES_PROJECT`.

Os valores não são versionados.

### Regras de promoção

1. PRs contra `main` recebem alias de preview próprio, no formato `pr-N`.
2. Uma release publicada gera o alias estável `preview`.
3. Produção nunca é acionada por `push`, PR ou release.
4. Produção exige acionamento manual e uma `release_tag` existente.
5. O workflow nunca usa arquivos locais do operador; o candidato é montado no runner a partir do snapshot estático publicado e do frontend versionado no GitHub.
6. O QA verifica o SHA-256 da fonte de dados registrado no próprio snapshot e rejeita qualquer baseline diferente do aprovado.
7. O QA remoto verifica HTTP, headers de segurança, versão da aplicação, universo, anos, cartografia e indicadores sentinela.
8. Esta automação cobre deployment. A reconstrução automática da base canônica permanece uma etapa separada até existir uma fonte de build autenticável e estável para o runner.

### QA pós-deploy

O script `deployment/qa_pages.py` pode ser usado tanto localmente quanto contra uma URL:

```bash
python deployment/qa_pages.py --site build/site
python deployment/qa_pages.py --url https://<preview-ou-producao>
```

O QA não substitui revisão metodológica dos dados; ele protege o contrato de publicação e detecta regressões estruturais.
