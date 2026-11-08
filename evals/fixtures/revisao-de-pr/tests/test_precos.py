import pytest
from loja.precos import aplicar_desconto


def test_desconto_simples():
    assert aplicar_desconto(100, 10) == 90


def test_percentual_invalido():
    with pytest.raises(ValueError):
        aplicar_desconto(100, 150)
