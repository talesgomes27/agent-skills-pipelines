# Padrões Canônicos de Refatoração por Arquétipo (A, B e C)

Este guia orienta a execução cirúrgica no **Gate 4** da `audit-and-refactoring-pipeline`.

## 1. Arquétipo A — Data Science, Analytics & Quarto
1. **Extração de Lógica de Notebooks para `src/`:** Mova funções longas de limpeza, *feature engineering* e plotagem de dentro de células `.ipynb`/`.qmd` para módulos testáveis em `src/`, importando-as de forma limpa no relatório.
2. **Vetorização e Performance (`polars` / `numpy`):** Substitua loops explícitos (`iterrows()`, `.apply(..., axis=1)`) por operações vetorizadas ou expressões *lazy* em Polars.
3. **Padronização Gráfica 300 DPI:** Centralize a configuração estética do Matplotlib/Seaborn (paleta, `sns.despine()`, `dpi=300`, `constrained_layout=True`, `set_box_aspect(1)`) em um módulo utilitário de estilo.
4. **Reestruturação Editorial CRISP-ML(Q) + Storytelling:** Reorganize relatórios `.qmd` legados ou fragmentados nas 6 seções canônicas, removendo numeração manual duplicada dos cabeçalhos Markdown, adicionando Callout Blocks (`.callout-note`, `.callout-tip`, `.callout-important`) e corrigindo referências cruzadas `@fig-` e `@tbl-`.
5. **Modernização de Ambiente Python (uv + Ruff + pytest):** Em projetos Python sem dependências C++/R exclusivas do Conda, migre `requirements.txt` soltos para `pyproject.toml` + `uv.lock` e configure `ruff` e `pytest`.
6. **Correção de Renderização de Diagramas Quarto:** Converter code blocks ` ```mermaid ` e ` ```dot ` em executable cells ` ```{mermaid} ` e ` ```{dot} `. Mover opções para cell options (`%%|` ou `//|`), adicionar `label: fig-*` e `fig-cap: "..."`, atualizar referências cruzadas no texto via `@fig-*` e renomear arquivos `.md` para `.qmd` se contiverem células executáveis.

## 2. Arquétipo B — Engenharia de Software, Web & APIs
1. **Desacoplamento de Controladores/Rotas:** Extraia regras de negócio e chamadas diretas ao banco de dentro das rotas HTTP para casos de uso/serviços e repositórios isolados.
2. **Inversão de Dependência e Contratos:** Introduza schemas estritos (Pydantic / TypeScript) nas fronteiras de entrada e saída e elimine acoplamento circular entre pacotes.
3. **Saneamento de Banco e I/O:** Elimine queries N+1, adicione índices ausentes e garanta fechamento seguro de conexões/transações.

## 3. Arquétipo C — Automação, CLI & Scripts Técnicos
1. **Decomposição de Scripts Monolíticos:** Separe o parsing de argumentos (`argparse`/`click`/`typer`) da lógica pura de processamento, permitindo testar o núcleo sem invocar o shell.
2. **Enxugamento de Dependências (`ponytail`):** Substitua bibliotecas externas pesadas ou desnecessárias por módulos nativos da biblioteca padrão (`pathlib`, `json`, `csv`, `urllib`, `subprocess`).
3. **Conformidade POSIX:** Padronize mensagens de erro no `stderr` (`erro: <causa>. <ação sugerida>.`), resultados limpos no `stdout` e códigos de saída (`0` sucesso, `>0` falha).
