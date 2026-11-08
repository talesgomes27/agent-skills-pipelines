from unittest import mock
from cotacoes.cliente import cotacao


def test_cotacao():
    s = mock.Mock()
    s.get.return_value.json.return_value = {'valor': 5.1}
    assert cotacao('USD', s) == 5.1
