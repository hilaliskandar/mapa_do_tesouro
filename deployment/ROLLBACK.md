# Rollback de publicação

Este procedimento se aplica à publicação estática no Cloudflare Pages.

## Princípio

O rollback deve restaurar uma release já publicada e validada. Não reconstruir dados ad hoc durante a reversão e não alterar `VERSION` apenas para executar rollback.

## Procedimento

1. identificar a última release estável aprovada e sua tag;
2. confirmar que a tag possui manifesto e notas de release versionados;
3. acionar manualmente `Pages Production` informando a tag estável anterior;
4. o workflow deve materializar o candidato a partir do preview aprovado, validar localmente e publicar em produção;
5. executar `deployment/qa_pages.py` contra a URL de produção;
6. confirmar versão da aplicação, universo, anos, cartografia, headers e indicadores sentinela;
7. registrar a reversão no changelog operacional privado, incluindo tag restaurada, commit, horário, motivo e resultado do QA.

## Regras

- produção nunca deve ser revertida por edição manual de arquivos no Pages;
- nenhuma credencial deve ser adicionada ao repositório;
- snapshots e hashes da release restaurada devem permanecer os mesmos da release original;
- se o QA pós-rollback falhar, interromper novas promoções e tratar como incidente;
- a candidata SP645 não substitui o baseline TIC_TIM_30 sem decisão explícita de release.
