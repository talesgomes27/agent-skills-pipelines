-- Receita por região no mês
SELECT e.regiao, SUM(p.valor) AS receita
FROM pedidos p
JOIN enderecos_cliente e ON e.cliente_id = p.cliente_id
WHERE p.data_pedido >= :inicio AND p.data_pedido < :fim
GROUP BY e.regiao
ORDER BY e.regiao;
