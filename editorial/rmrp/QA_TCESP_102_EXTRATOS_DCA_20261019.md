# Coleta RMRP TCESP 2023-2025 — QA regional e confronto FINBRA/DCA

Execução GitHub Actions: 39203495737. Four jobs succeeded. Origem: 4 artifacts Github Actions IDs 12164512559 (sub-região 1), 12164945873 (2), 12164992449 (3), 12164872696 (4). 34 municípios × 3 exercícios = 102 JSONs. Auditoria dos relatórios das quatro sub-regiões: 102 válidos, 0 falhas. Todos os JSONs conferidos novamente: igualdade entre soma dos programas, soma das ações e total de despesas liquidadas no grupo 44.

Confronto externo: investimentos liquidados TCESP grupo 44 em centavos versus `dca_investimentos_liquidada` do CSV canônico SP645 2013–2025, matriz município IBGE × ano. 2023 33/34 pares exatos; 2024 34/34; 2025 34/34; total 101/102 pares exatos.

Única diferença: Guatapará (3518859), 2023: TCESP R$ 2.118.940,79, DCA R$ 2.108.764,79, diferença TCESP − DCA = R$ 10.176,00. Não substituir qualquer valor nem presumir causa. Conservar o registro e investigar documentos originais, classificação 44 e datas de atualização.

Totais TCESP regionais em centavos: 2023 48.495.857.524; 2024 50.082.415.206; 2025 30.230.189.518. Totais DCA regionais: 2023 48.494.839.924; 2024 50.082.415.206; 2025 30.230.189.518.

O arquivo local `/mnt/data/RMRP_TCESP_34M_2023_2025_CONSOLIDADO.zip` reúne os 102 extratos e inventário com hashes por documento. A conciliação separada está em `/mnt/data/rmrp_tcesp_regional_consolidado/conciliacao_tcesp_dca_102.csv`. Nenhuma API ou produção pública foi alterada. Ainda falta aprovação editorial da decomposição programas/ações e armazenamento persistente fora da retenção de 30 dias do Actions.
