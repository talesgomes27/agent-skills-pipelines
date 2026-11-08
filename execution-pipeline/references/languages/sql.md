# SQL

Leia quando o componente da tarefa escreve, muda ou roda consultas ou migrações SQL.

## Descubra no projeto

- Dialeto e versão do banco: configuração da conexão, `docker-compose`, CI e a documentação do projeto. A semântica muda entre Postgres, MySQL, SQLite, DuckDB e outros.
- Migrações: a pasta e a ferramenta que o projeto usa (Alembic, Flyway, Liquibase, Prisma, `migrations/`) e o último arquivo aplicado.
- Comandos: os scripts do projeto para subir o banco de teste, migrar e rodar os testes.

Use os comandos e o banco de teste do projeto. Não instale servidor de banco global.

## Testes e checks

Teste contra um banco de teste do mesmo dialeto e versão, com a migração aplicada do zero. SQLite ou DuckDB no lugar de Postgres muda semântica; quando usar um deles, diga isso no relatório, com o que a diferença deixa sem verificar no banco real (por exemplo, divisão inteira, tipos e fuso). Exemplos documentados: no Postgres `1 / 2` dá `0` e no DuckDB dá `0.5`; o SQLite guarda qualquer tipo em qualquer coluna, salvo em tabela `STRICT` e na coluna `INTEGER PRIMARY KEY`.

## Regras

- Confira a cardinalidade antes e depois de cada JOIN: conte as linhas e confirme que a chave do lado que deveria ser único não se repete. JOIN com chave repetida multiplica linhas e infla somas sem erro. Rode as consultas e registre os números no relatório:

  ```sql
  SELECT COUNT(*) FROM pedidos;                        -- antes do JOIN
  SELECT COUNT(*) FROM pedidos p JOIN enderecos e ON e.cliente_id = p.cliente_id;  -- depois
  SELECT cliente_id, COUNT(*) FROM enderecos GROUP BY cliente_id HAVING COUNT(*) > 1;  -- chave repetida
  ```

  Se a correção filtra para tornar a chave única, como um campo `principal`, rode a mesma consulta de chave repetida com o filtro e diga o que acontece com as linhas que ficam sem par; se a regra não está escrita, pergunte ao usuário qual é.
- NULL em `NOT IN`: se a subconsulta traz um NULL e não há igualdade, o resultado é NULL, não verdadeiro, e a linha some. Filtre os NULL da subconsulta.
- NULL em comparações: `x = NULL` e `x <> NULL` dão NULL. Use `IS NULL` ou `IS [NOT] DISTINCT FROM`.
- `COUNT(*)` conta linhas e `COUNT(coluna)` conta só os valores não nulos. `SUM` sem linhas dá NULL, não zero; use `COALESCE` quando zero é o certo.
- Divisão inteira: no Postgres, divisão entre inteiros trunca (`5 / 2` dá `2`). Converta para `numeric` antes de dividir quando quer fração.
- Fuso e tipo de data: no Postgres, `timestamp` sem fuso ignora o fuso do texto, e `timestamptz` guarda em UTC e mostra no `TimeZone` da sessão. Confira o tipo da coluna e o fuso da sessão antes de agrupar por dia.
- Consultas parametrizadas, nunca texto concatenado com entrada: montar SQL com formatação de string abre injeção de SQL.
- Exploração só com `SELECT` e `LIMIT`, com credencial só de leitura que o usuário autorizou e que o plano prevê.
- `EXPLAIN` pode rodar, com a mesma credencial autorizada. `EXPLAIN ANALYZE` executa a consulta, com todos os efeitos de um `INSERT`, `UPDATE` ou `DELETE`, e não roda em produção.
- Migração segue as regras de backup e recuperação do [contrato comum](../common-contract.md) e da referência do arquétipo, como a [B](../archetype-b.md): arquivo revisável, aplicado só na base de teste autorizada; produção é release.

## Fontes

Conferido em 08/11/2026:

- https://www.postgresql.org/docs/current/sql-explain.html
- https://www.postgresql.org/docs/current/functions-subquery.html
- https://www.postgresql.org/docs/current/functions-comparison.html
- https://www.postgresql.org/docs/current/functions-aggregate.html
- https://www.postgresql.org/docs/current/functions-math.html
- https://www.postgresql.org/docs/current/datatype-datetime.html
- https://duckdb.org/docs/stable/sql/dialect/postgresql_compatibility
- https://www.sqlite.org/datatype3.html
- https://docs.python.org/3/library/sqlite3.html (placeholders e injeção de SQL)
