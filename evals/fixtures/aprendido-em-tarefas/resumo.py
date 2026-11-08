import csv
import sys


def total(caminho):
    with open(caminho, newline='', encoding='utf-8') as f:
        return sum(float(l['valor']) for l in csv.DictReader(f, delimiter=';'))


if __name__ == '__main__':
    print(total(sys.argv[1]))
