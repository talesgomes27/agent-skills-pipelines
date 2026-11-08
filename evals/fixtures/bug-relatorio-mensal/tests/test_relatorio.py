import unittest

from relatorio import totais_por_regiao


class Totais(unittest.TestCase):
    def test_soma_por_regiao(self):
        linhas = [{'regiao': 'Norte', 'valor': '10.5'}, {'regiao': 'Norte', 'valor': '4.5'}, {'regiao': 'Sul', 'valor': '1'}]
        self.assertEqual(totais_por_regiao(linhas), {'Norte': 15.0, 'Sul': 1.0})


if __name__ == '__main__':
    unittest.main()
