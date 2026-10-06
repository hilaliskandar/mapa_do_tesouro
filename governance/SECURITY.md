# Segurança e separação de configuração

## Objetivo

Preservar simultaneamente reprodutibilidade, auditabilidade e segurança operacional.

## O que deve permanecer público

- esquema de dados;
- migrações SQL;
- pipeline;
- fórmulas e regras metodológicas;
- testes;
- frontend;
- contratos da API;
- exemplos de configuração sem credenciais;
- documentação de como executar localmente;
- requisitos funcionais e de QA.

## O que deve permanecer privado

- tokens e chaves;
- credenciais de qualquer serviço;
- configuração real de produção;
- IDs operacionais quando não forem necessários à reprodução;
- nomes internos de recursos;
- procedimentos administrativos de conta;
- arquivos de ambiente reais;
- detalhes de DNS e rotas não destinados ao público.

## Separação arquitetural

```text
núcleo reproduzível
├── pipeline
├── SQLite
├── regras
├── testes
├── frontend
└── contratos HTTP
        │
        ▼
adapter de implantação
        ├── Cloudflare
        ├── ambiente local
        └── outro provedor futuro
```

A aplicação nunca deve exigir Cloudflare para validar cálculos ou reconstruir a base.

## Segredos

Segredos devem ser armazenados apenas em mecanismos próprios do ambiente de execução, como secret stores, variáveis protegidas ou configurações locais ignoradas pelo Git.

## Incidentes

Se qualquer segredo for commitado, removê-lo do histórico não é suficiente: ele deve ser revogado e substituído.
