"""Manda o lembrete de vencimento por WhatsApp a cada cliente do CSV."""
import csv
import datetime
import os
import sys
from pathlib import Path

import whatsapp

TEMPLATE = Path(__file__).with_name('templates') / 'cobranca.txt'


def main(caminho):
    linhas = list(csv.DictReader(open(caminho, encoding='utf-8')))
    modelo = TEMPLATE.read_text(encoding='utf-8')
    log = Path('logs') / f'envios-{datetime.date.today()}.log'
    with open(log, 'a', encoding='utf-8') as saida:
        for i, cliente in enumerate(linhas):
            # pula o cabeçalho
            dados = linhas[i - 1]
            texto = modelo.format(**dados)
            status = whatsapp.enviar(cliente['telefone'], texto, os.environ['WHATSAPP_TOKEN'])
            saida.write(f"{datetime.datetime.now().isoformat()} id={cliente['id']} status={status} texto={texto!r}\n")


if __name__ == '__main__':
    main(sys.argv[1])
