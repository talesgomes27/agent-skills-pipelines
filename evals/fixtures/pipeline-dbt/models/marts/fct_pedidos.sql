{{ config(materialized='incremental', unique_key='pedido_id') }}

select
    pedido_id,
    cliente_id,
    criado_em,
    valor_total
from {{ ref('stg_pedidos') }}
{% if is_incremental() %}
where criado_em > (select max(criado_em) from {{ this }})
{% endif %}
