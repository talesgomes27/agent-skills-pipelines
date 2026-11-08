import importlib.util
import io
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('numero_cnj', REPO / 'jurimetria/scripts/numero_cnj.py')
nc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nc)


def run(*args, stdin=''):
    import sys
    out, err = io.StringIO(), io.StringIO()
    old = sys.stdin
    sys.stdin = io.StringIO(stdin)
    try:
        with redirect_stdout(out), redirect_stderr(err):
            code = nc.main(list(args))
    finally:
        sys.stdin = old
    return code, out.getvalue(), err.getvalue()


class Digito(unittest.TestCase):
    # Exemplos calculados pelo Anexo VIII da Resolução CNJ 65/2008 (números fictícios).
    def test_calcula_o_digito(self):
        self.assertEqual(nc.digito('0000100', '2008', '8', '14', '0000'), '13')
        self.assertEqual(nc.digito('0801234', '2023', '8', '14', '0301'), '84')

    def test_valida_com_e_sem_mascara(self):
        for n in ('0000100-13.2008.8.14.0000', '00001001320088140000', '100-13.2008.8.14.0000', ' 0801234-84.2023.8.14.0301 ',
                  '0000100-13.2008.814.0000', '0000100 13 2008 8 14 0000', '0000100.13.2008.8.14.0000'):
            with self.subTest(n=n):
                self.assertTrue(nc.valido(n))

    def test_recusa_digito_errado_e_formato_errado(self):
        for n in ('0000100-14.2008.8.14.0000', '0801234-84.2023.8.14.030', 'abc', '', '0000100-13.2008.0.14.0000', '0000100x13y2008z8.14.0000'):
            with self.subTest(n=n):
                self.assertFalse(nc.valido(n))

    def test_normaliza_para_20_digitos(self):
        self.assertEqual(nc.normalizar('100-13.2008.8.14.0000'), '00001001320088140000')
        self.assertIsNone(nc.normalizar('12.2008'))

    def test_formata_e_separa(self):
        self.assertEqual(nc.formatar('00001001320088140000'), '0000100-13.2008.8.14.0000')
        self.assertEqual(nc.partes('0801234-84.2023.8.14.0301'),
                         {'N': '0801234', 'D': '84', 'A': '2023', 'J': '8', 'TR': '14', 'O': '0301'})

    def test_verificacao_mod_97_igual_a_1(self):
        # Anexo VIII, item VI: NNNNNNN AAAA J TR OOOO DD mod 97 = 1
        self.assertEqual(int('0000100' '2008' '8' '14' '0000' '13') % 97, 1)


class Cli(unittest.TestCase):
    def test_csv_separa_validos_e_invalidos(self):
        code, out, _ = run('--coluna', 'numero', stdin='numero\n0000100-13.2008.8.14.0000\n0000100-14.2008.8.14.0000\n\n')
        self.assertEqual(code, 1)
        self.assertIn('00001001320088140000,valido', out)
        self.assertIn('0000100-14.2008.8.14.0000,invalido', out)

    def test_tudo_valido_sai_com_zero(self):
        code, out, _ = run(stdin='0801234-84.2023.8.14.0301\n')
        self.assertEqual(code, 0, out)

    def test_csv_com_bom_e_entrada_com_virgula(self):
        code, out, _ = run('--coluna', 'numero', stdin='\ufeffnumero\n"0000100-14.2008.8.14.0000, ver"\n')
        self.assertEqual(code, 1)
        self.assertIn('"0000100-14.2008.8.14.0000, ver",invalido', out)

    def test_recusa_digitos_fora_do_ascii(self):
        self.assertFalse(nc.valido('\uff10\uff10\uff10\uff10\uff11\uff10\uff10-13.2008.8.14.0000'))

    def test_coluna_ausente_sai_com_dois(self):
        code, _, err = run('--coluna', 'processo', stdin='numero\n1\n')
        self.assertEqual(code, 2)
        self.assertIn('coluna', err)


if __name__ == '__main__':
    unittest.main()
