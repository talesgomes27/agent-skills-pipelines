from loja.precos import aplicar_desconto


def aplicar_cupom(pedido, corpo):
    # corpo vem do JSON enviado pelo cliente
    return aplicar_desconto(pedido['total'], float(corpo['percentual']))
