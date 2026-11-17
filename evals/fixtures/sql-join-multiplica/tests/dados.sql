-- dados sintéticos de teste, carregados depois de esquema.sql no SQLite em memória
INSERT INTO pedidos VALUES (1, 10, 100.00, '2026-10-05'), (2, 11, 50.00, '2026-10-07'), (3, 12, 30.00, '2026-10-09');
-- o cliente 10 tem dois endereços (um de cobrança e um de entrega); o 12 não tem principal
INSERT INTO enderecos_cliente VALUES (10, 'Sul', 1), (10, 'Norte', 0), (11, 'Norte', 1), (12, 'Sul', 0);
