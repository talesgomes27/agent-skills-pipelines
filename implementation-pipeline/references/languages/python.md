# Python

Leia quando o componente da tarefa é escrito em Python.

## Descubra no projeto

- Versão e dependências: `pyproject.toml` e o lock do projeto (`uv.lock`, `poetry.lock` ou `requirements*.txt` com versões fixas), além de `.python-version`.
- Configuração dos checks: `[tool.pytest.ini_options]`, `[tool.ruff]` e `[tool.mypy]` no `pyproject.toml`, ou `pytest.ini`, `ruff.toml` e `mypy.ini`.
- Comandos: `Makefile`, `noxfile.py`, `tox.ini` e o workflow de CI.

Use os comandos do projeto e o ambiente isolado que ele já usa (`.venv` do uv, Poetry ou outro). Não instale nada global nem com o `pip` do sistema.

## Testes e checks

Exemplos a confirmar no projeto:

- `uv run --locked --no-python-downloads pytest`: com o lock já aceito, o `uv run` sincroniza o ambiente a partir dele, o `--locked` faz falhar se o lock não bate com o `pyproject.toml`, em vez de reescrevê-lo, e o `--no-python-downloads` impede que o uv baixe sozinho o Python pedido pelo `.python-version` ou pelo `requires-python` quando a máquina não o tem. Se faltar o Python, pare e peça A2 com a versão, a origem e onde fica, ou use o ambiente que já existe e diga qual. Sem `uv.lock`, ou com o lock desatualizado, o `uv run` resolve e instala dependências e grava o lock: isso é instalar dependência, um efeito do catálogo do contrato comum, e pede A2 antes.
- `uv run --locked --no-python-downloads ruff check .` e o mesmo com `ruff format --check .`: o segundo só aponta arquivos fora do formato e sai com código 1.
- `uv run --locked --no-python-downloads mypy <pacote>` quando o projeto usa tipos.

## Armadilhas

- Dependência sem lock: a mesma instalação resolve versões diferentes em outra máquina. Fixe pelo lock do projeto e não adicione pacote fora dele.
- Mutável como valor padrão: o default é avaliado uma vez, e `def f(x, acc=[])` acumula entre chamadas. Use `None` e crie o objeto dentro da função.
- `float` para dinheiro: `1.1 + 2.2` dá `3.3000000000000003`. Use `decimal.Decimal` criado a partir de texto, ou centavos em inteiro.
- Data sem fuso: `datetime` ingênuo não identifica um instante, e muitos métodos o tratam como hora local. `datetime.utcnow()` está obsoleto desde o 3.12; use `datetime.now(UTC)`.
- Exceção engolida: `except Exception: pass` esconde a falha e grava saída incompleta. Capture o erro específico e registre o que falhou.

## Fontes

Conferido em 08/11/2026:

- https://docs.python.org/3/tutorial/controlflow.html (valor padrão avaliado uma vez)
- https://docs.python.org/3/library/decimal.html
- https://docs.python.org/3/library/datetime.html
- https://docs.astral.sh/uv/concepts/projects/sync/
- https://docs.astral.sh/ruff/configuration/ e https://docs.astral.sh/ruff/formatter/
- https://docs.pytest.org/en/stable/reference/customize.html
- https://mypy.readthedocs.io/en/stable/config_file.html
