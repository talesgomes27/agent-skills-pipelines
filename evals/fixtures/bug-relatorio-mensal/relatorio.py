"""Total de vendas por região a partir de um CSV exportado pelo ERP."""
import csv
import sys


def totais_por_regiao(linhas):
    totais = {}
    for linha in linhas:
        regiao = linha['regiao']
        totais[regiao] = totais.get(regiao, 0.0) + float(linha['valor'])
    return totais


def main(caminho):
    with open(caminho, newline='', encoding='utf-8') as f:
        totais = totais_por_regiao(csv.DictReader(f))
    for regiao, total in sorted(totais.items()):
        print(f'{regiao};{total:.2f}')


if __name__ == '__main__':
    main(sys.argv[1])
