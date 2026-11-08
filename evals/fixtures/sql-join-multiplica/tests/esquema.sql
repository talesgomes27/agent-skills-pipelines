CREATE TABLE pedidos (pedido_id INTEGER PRIMARY KEY, cliente_id INTEGER, valor DECIMAL(12,2), data_pedido DATE);
-- um cliente pode ter vários endereços; principal = true marca o de cobrança
CREATE TABLE enderecos_cliente (cliente_id INTEGER, regiao TEXT, principal BOOLEAN);
