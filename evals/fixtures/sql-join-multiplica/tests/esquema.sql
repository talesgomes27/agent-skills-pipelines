CREATE TABLE pedidos (pedido_id INTEGER PRIMARY KEY, cliente_id INTEGER, valor NUMERIC, data_pedido TEXT);
-- um cliente pode ter vários endereços; principal = 1 marca o de cobrança
CREATE TABLE enderecos_cliente (cliente_id INTEGER, regiao TEXT, principal INTEGER);
