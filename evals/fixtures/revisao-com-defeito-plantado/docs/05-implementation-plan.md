# Plano: tabela de pedidos

Esforço rigoroso: migração num banco com dados reais.

- R-001 A tabela `pedidos` existe com `id`, `cliente_id`, `valor` e `criado_em`.
- R-002 A migração faz backup do banco antes de criar a tabela e testa a restauração num banco temporário; sem esse passo, ela não roda.
- R-003 `POST /pedidos` recusa valor negativo com 422.

Tarefas: T-001 migração 0002 com o passo de backup (R-001, R-002); T-002 rota e validação (R-003); cada requisito com teste que afirma o resultado.
