-- dados sintéticos de teste, carregados depois de esquema.sql no DuckDB em memória
INSERT INTO pedidos VALUES (1, 10, 100.00, DATE '2026-10-05'), (2, 11, 50.00, DATE '2026-10-07'), (3, 12, 30.00, DATE '2026-10-09');
-- o cliente 10 tem dois endereços (um de cobrança e um de entrega); o 12 não tem principal
INSERT INTO enderecos_cliente VALUES (10, 'Sul', true), (10, 'Norte', false), (11, 'Norte', true), (12, 'Sul', false);
