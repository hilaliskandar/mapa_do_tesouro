# S03 — recuperação dirigida e gate de publicação

S03 recuperação dirigida — 24/11/2026: cobertura inicial 611/611, 520 reconciliados e 91 inconclusivos (75 consulta_sem_totalizador, 15 resposta_ValueError, 1 ConnectionError). Implementados coletor diagnóstico 074707bc911135e1a1ab219a0f7b9c69dbbc7693 e modo recovery 0649eb54f9eec25f669fee3b6c2b1da456c4ab1e. Disparo aceito para offset=0,limit=5,year=2025,mode=recovery; resultado e readback pendentes. Não promover dados financeiros ou imputar zero por palavras-chave. Preservar fila de 91 até evidência; não avançar offset em fila mutável sem fixar o universo. Plataforma v0.4.1 preservada.

## Critérios para próxima versão

1. Validar snapshot diagnóstico e evidência HTML privada. 2. Classificar ausência explícita somente após verificar contexto, filtro e estado de resposta. 3. Consolidar registros recuperados por IBGE7/ano sem duplicar valores existentes; distinguir ausência comprovada de inconclusiva. 4. Auditar totais, cobertura, proveniência e compatibilidade com esquema da plataforma em ambiente de staging. 5. Não representar liberações/estornos como execução fiscal homologada; manter public_release_authorized=false até gate formal. 6. Só então promover versão e testar interface e regressões.
