def aplicar_desconto(valor, percentual):
    """Preço com desconto, em reais. percentual vai de 0 a 100."""
    if not 0 <= percentual <= 100:
        raise ValueError('percentual fora de 0 a 100')
    return round(valor * (1 - percentual / 100), 2)
