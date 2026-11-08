"""Preços do pedido. Desde 2026-11-06 (mudança da Ana na main), os valores são Decimal."""
from decimal import ROUND_HALF_UP, Decimal


def arredondar(valor: Decimal) -> Decimal:
    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def total(itens):
    return arredondar(sum((Decimal(str(p)) * q for p, q in itens), Decimal('0')))
