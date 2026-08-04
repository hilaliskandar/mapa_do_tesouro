from pathlib import Path

from nucleo.gerenciador_execucao import GerenciadorExecucao


def teste_cria_execucao_com_manifesto(tmp_path: Path) -> None:
    gerenciador = GerenciadorExecucao(tmp_path)
    contexto = gerenciador.criar_execucao("finbra.xlsx", "municipios.geojson")

    diretorio = Path(contexto.diretorio)
    assert diretorio.exists()
    assert (diretorio / "manifest.json").exists()
    assert (diretorio / "README.md").exists()
    assert (diretorio / "01_validacao_estrutural").exists()
