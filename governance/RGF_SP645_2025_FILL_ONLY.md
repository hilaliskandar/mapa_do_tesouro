# RGF SP645 2025 — composição fill-only com suplemento CAPAG

A carga estadual RGF 2025 dos Anexos 01/05 foi concluída sem falhas e sem issues.

Antes de qualquer delta externo, cinco campos do Anexo 05 foram comparados ao `Datalake` do snapshot oficial CAPAG de setembro de 2026.

## Paridade observada

Em todos os valores sobrepostos, a diferença absoluta foi zero:

- caixa bruta não vinculada: 526 sobreposições;
- demais obrigações não vinculadas: 93;
- RP não liquidados anteriores: 411;
- RP liquidados anteriores: 404;
- RP liquidados do exercício: 412.

Conflitos acima de R$ 0,01: **zero**.

## Fill-only autorizado

Somente células vazias da base RGF são preenchidas, e apenas nos cinco conceitos semanticamente idênticos.

Preenchimentos adicionais:

- caixa bruta não vinculada: +109;
- demais obrigações não vinculadas: +15;
- RP não liquidados anteriores: +79;
- RP liquidados anteriores: +74;
- RP liquidados do exercício: +89.

Total: **366 células**.

Cobertura após composição:

- caixa bruta não vinculada: 635/645;
- demais obrigações não vinculadas: 108/645;
- RP não liquidados anteriores: 490/645;
- RP liquidados anteriores: 478/645;
- RP liquidados do exercício: 501/645.

Permanecem sem qualquer preenchimento por suplemento:

- DTP legal: 530/645;
- RCL denominador legal: 530/645;
- percentual oficial DTP/RCL: 530/645;
- caixa líquida antes RPNP: 528/645;
- RP não liquidados do exercício: 410/645;
- caixa líquida após RPNP: 528/645.

## Hashes empíricos

- base RGF API: `9f3ced721fa2c767d24cdec8e464215b30932e820e01601f24bac9b1e76486ba`;
- snapshot CAPAG: `1b1379a5a531920223f1d448be155b70f51eb50180d8c819f1b7da3575a8eb11`;
- composto fill-only: `48b50b2df44eaddc2fc1c4ed096c057c2bea5d61cb850b37dc23e6037962aa24`.

O composto permanece privado e não altera o painel público.
