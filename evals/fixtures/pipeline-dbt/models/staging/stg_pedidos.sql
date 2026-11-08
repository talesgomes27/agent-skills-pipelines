select
    id as pedido_id,
    cliente_id,
    criado_em,
    valor_total,
    canal as canal_venda
from {{ source('loja', 'pedidos') }}
