# Guia de Publicação: Relatórios Quarto no GitHub Pages (Arquétipo A)

Este documento define as duas estratégias canônicas e seguras para publicar relatórios Quarto (`.qmd`) no GitHub Pages sem reexecutar modelos pesados ou depender de bases `.csv` ignoradas no Git.

## Pré-requisitos Obrigatórios no `_quarto.yml`
```yaml
project:
  type: website # ou default
  output-dir: docs # se usar Estratégia 1 (Branch main/docs)

lang: pt-BR

execute:
  freeze: auto
```

## Estratégia 1: Renderização Local + Publicação via Pasta `docs/` (Mais Simples e Determinística)
Ideal quando todo o processamento de dados e gráficos (`reports/figures/` em 300 DPI) já foi concluído localmente no Gate 5 da `execution-pipeline`.
1. Execute `quarto render` localmente. O HTML compilado e os assets irão para `docs/`.
2. Crie o arquivo vazio `docs/.nojekyll` (`touch docs/.nojekyll`) para impedir que o processador Jekyll do GitHub ignore pastas iniciadas com underscore (como `site_libs` ou `_files`).
3. Versione `docs/` e `_freeze/` no commit de release e faça push para `main`.
4. Configure o GitHub Pages do repositório para servir a partir da branch `main`, diretório `/docs` (via `gh api` ou interface web).

## Estratégia 2: Publicação Automatizada via GitHub Actions (`quarto-actions/publish`)
Ideal para CI/CD contínuo a cada push na `main`.
- **Requisito Crítico:** A pasta `_freeze/` gerada localmente **deve estar commitada no Git** (com `execute: freeze: auto` no `_quarto.yml`) para que o runner não tente reexecutar treinamentos sobre bases `.csv` ausentes. Caso algum bloco leve precise de pacotes Python, os passos condicionais de `uv` abaixo instalam o ambiente a partir do `uv.lock`.

Arquivo `.github/workflows/publish.yml`:
```yaml
name: Publish Quarto Report to GitHub Pages

on:
  push:
    branches: [main, master]
  workflow_dispatch:

permissions:
  contents: write
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Quarto
        uses: quarto-dev/quarto-actions/setup@v2

      - name: Set up Python and uv (condicional)
        if: hashFiles('pyproject.toml') != ''
        uses: astral-sh/setup-uv@v3
        with:
          enable-cache: true

      - name: Install Python dependencies (condicional)
        if: hashFiles('pyproject.toml') != ''
        run: uv sync --frozen

      - name: Render and Publish to gh-pages
        uses: quarto-dev/quarto-actions/publish@v2
        with:
          target: gh-pages
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
