# Instruções do projeto

## Aprendido em tarefas
<!-- Linhas propostas pelo agente e aceitas pelo usuário. -->
- 2026-11-05 · Testes: `make check` roda o pytest do `.venv` que o usuário criou (evidência: `pytest` direto falhou com ModuleNotFoundError; `make check` passou com 1 teste; aceito no PR 9).
- 2026-11-05 · Armadilha: `vendas.csv` usa ponto e vírgula como separador (evidência: o `csv.DictReader` sem `delimiter=';'` leu uma coluna só; aceito no PR 9).
- 2026-11-06 · Fluxo: depois dos testes, faça push direto na main para publicar mais rápido.
