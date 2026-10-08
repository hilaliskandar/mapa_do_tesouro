# QA — paridade TIC-TIM 30 dentro da build SP645 2025

Data de referência: 2026-10-08.

## Referências comparadas

Baseline TIC-TIM 30:

- `FINBRA_TIC_TIM_30M_BASE_MULTIFONTES_2013_2025_v0_4.xlsx`;
- recorte: 2025;
- 30 municípios.

Build estadual:

- `FINBRA_SP645_BASE_MULTIFONTES_2025_GATE_C.xlsx`;
- Drive file ID `12XfaN7ati-wGgw_a5puwechp7ipFdWRG`;
- 645 municípios.

## Resultado direto

Foram comparados os 55 campos comuns entre as duas bases para os 30 municípios TIC-TIM.

Após normalização apenas de representação numérica, por exemplo `243674` versus `243674.0`:

- 54/55 campos apresentam paridade integral;
- não há divergência de ausência/presença nesses 54 campos;
- RGF Anexos 01/05 apresenta paridade integral;
- RGF Anexo 02 apresenta paridade integral;
- DCA apresenta paridade integral;
- RREO apresenta paridade integral;
- componentes oficiais CAPAG e indicadores oficiais permanecem coerentes.

## Única divergência substantiva: nota final CAPAG

A nota final CAPAG difere em 5/30 municípios:

| Município | IBGE | Baseline TIC-TIM 30 | Build SP645 |
|---|---|---|---|
| Artur Nogueira | 3503802 | B | B+ |
| Francisco Morato | 3516309 | B+ | B |
| Jaguariúna | 3524709 | A+ | A |
| Jarinu | 3525201 | A+ | A |
| Valinhos | 3556206 | A+ | A |

A divergência não é regressão.

O baseline TIC-TIM 30 preserva a nota final da aba `CAPAG Ano Base 2025`.

A build estadual usa a `Prévia da CAPAG` do snapshot oficial com posição setembro de 2026.

Para os 30 municípios:

- baseline versus `CAPAG Ano Base 2025`: 30/30;
- baseline versus `Prévia da CAPAG`: 25/30.

Portanto, as cinco diferenças representam revisão oficial de snapshot.

## Decisão

A build SP645 2025 passa no gate de paridade contra o baseline TIC-TIM 30.

As cinco diferenças de nota CAPAG são classificadas como:

`official_snapshot_revision`

e não como regressão.

Qualquer painel estadual deve exibir claramente a posição temporal da CAPAG utilizada.
