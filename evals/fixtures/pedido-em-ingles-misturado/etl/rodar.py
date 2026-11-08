import csv
from etl.datas import ler_data


def linhas(caminho='entrada/pedidos.csv'):
    with open(caminho, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            yield {'id': r['id'], 'data': ler_data(r['data']), 'valor': float(r['valor'])}


def main():
    import pandas as pd
    novas = pd.DataFrame(list(linhas()))
    try:
        antigas = pd.read_parquet('saida/pedidos.parquet')
    except FileNotFoundError:
        antigas = novas.iloc[0:0]
    pd.concat([antigas, novas]).to_parquet('saida/pedidos.parquet')


if __name__ == '__main__':
    main()
