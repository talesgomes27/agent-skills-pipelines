#!/usr/bin/env python3
"""Valida e normaliza números únicos de processo (Resolução CNJ 65/2008).

Estrutura NNNNNNN-DD.AAAA.J.TR.OOOO. O dígito DD segue o Anexo VIII da resolução:
DD = 98 - (NNNNNNN AAAA J TR OOOO 00 mod 97), e o número completo, na ordem
NNNNNNN AAAA J TR OOOO DD, tem resto 1 na divisão por 97.

Uso: python numero_cnj.py [--coluna NOME] < arquivo
Lê um número por linha, ou um CSV com cabeçalho quando --coluna é dado, e escreve
"numero,valido" (normalizado em 20 dígitos) ou "entrada,invalido". Sai com 0 quando
todos são válidos, 1 quando algum é inválido e 2 em erro de uso. Só biblioteca
padrão, sem rede.
"""
import argparse
import csv
import re
import sys

# Sequencial sem os zeros à esquerda (art. 1º, § 1º), separado por espaço, ponto ou hífen
MASCARA = re.compile(r'^(\d{1,7})[\s.-]+(\d{2})[\s.-]+(\d{4})[\s.-]+(\d)[\s.-]*(\d{2})[\s.-]+(\d{4})$')


def digito(n, a, j, tr, o):
    """Dígito verificador, pelo Anexo VIII (Python tem inteiro de precisão arbitrária)."""
    resto = int(n.zfill(7) + a + j + tr + o + '00') % 97
    return '%02d' % (98 - resto)


def normalizar(numero):
    """Número em 20 dígitos sem máscara, ou None quando o formato não é o da resolução."""
    s = numero.strip()
    m = MASCARA.match(s)
    if m:
        n, d, a, j, tr, o = m.groups()
        return n.zfill(7) + d + a + j + tr + o
    digitos = re.sub(r'\D', '', s)
    return digitos if len(digitos) == 20 and not re.search(r'[^\d\s.\-]', s) else None


def partes(numero):
    s = normalizar(numero)
    if s is None:
        return None
    return {'N': s[:7], 'D': s[7:9], 'A': s[9:13], 'J': s[13], 'TR': s[14:16], 'O': s[16:]}


def valido(numero):
    p = partes(numero)
    if p is None or p['J'] == '0':  # segmentos 1 a 9 (art. 1º, § 4º)
        return False
    return digito(p['N'], p['A'], p['J'], p['TR'], p['O']) == p['D']


def formatar(numero):
    p = partes(numero)
    return None if p is None else '%(N)s-%(D)s.%(A)s.%(J)s.%(TR)s.%(O)s' % p


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--coluna', help='nome da coluna, quando a entrada é CSV com cabeçalho')
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    if args.coluna:
        leitor = csv.DictReader(sys.stdin)
        if args.coluna not in (leitor.fieldnames or []):
            print('coluna não encontrada: %s' % args.coluna, file=sys.stderr)
            return 2
        entradas = (linha[args.coluna] or '' for linha in leitor)
    else:
        entradas = (linha.rstrip('\n') for linha in sys.stdin)
    algum_invalido = False
    for e in entradas:
        if not e.strip():
            continue
        if valido(e):
            print('%s,valido' % normalizar(e))
        else:
            algum_invalido = True
            print('%s,invalido' % e.strip())
    return 1 if algum_invalido else 0


if __name__ == '__main__':
    sys.exit(main())
