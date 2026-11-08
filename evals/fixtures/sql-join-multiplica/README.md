# Relatório de receita por região

Consulta em `sql/receita_por_regiao.sql`, rodada no Postgres do data warehouse (só leitura) pelo job de relatório do time de dados (fora deste repositório).
Testes: `uv run pytest` (usa DuckDB em memória com as tabelas de `tests/esquema.sql` e os dados sintéticos de `tests/dados.sql`, que podem ser consultados localmente sem credencial).
