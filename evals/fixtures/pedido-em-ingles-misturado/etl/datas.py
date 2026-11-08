from datetime import datetime


def ler_data(texto):
    # 1.4.0: formato ISO
    return datetime.strptime(texto, '%Y-%m-%d').date()
