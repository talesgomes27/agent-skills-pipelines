from app import concluir


def test_mensagem():
    assert concluir() == "Instalação concluída"
