# Checklist de Migração: R Markdown / Bookdown / Xaringan para Quarto Nativo (`.qmd`)

Ao auditar ou refatorar documentos legados `.Rmd` ou `.ipynb` para `.qmd`, aplique estas substituições obrigatórias:

## 1. Cabeçalhos de Células de Código (*Hashpipe YAML*)
- **PROIBIDO (Legado R Markdown):** ```` ```{r setup, echo=FALSE, fig.cap="Legenda", warning=FALSE} ````
- **OBRIGATÓRIO (Quarto Nativo):**
  ````markdown
  ```{r}
  #| label: fig-setup
  #| fig-cap: "Legenda"
  #| echo: false
  #| warning: false
  ```
  ````
- Valores booleanos em `#|` devem ser escritos em minúsculas (`true` / `false`), nunca em maiúsculas (`TRUE` / `FALSE`).

## 2. Sistema de Referências Cruzadas
- Substitua `\@ref(fig:grafico)` (Bookdown) por `@fig-grafico` (exigindo `#| label: fig-grafico`).
- Substitua `\@ref(tab:tabela)` por `@tbl-tabela` (exigindo `#| label: tbl-tabela` ou `: Legenda {#tbl-tabela}`).
- Substitua `\@ref(eq:equacao)` por `@eq-equacao` (exigindo `$$...$$
{#eq-equacao}`).
- Substitua `\@ref(sec:secao)` por `@sec-secao` (exigindo `## Título {#sec-secao}`).

## 3. Fenced Divs, Callouts e Colunas
- Garanta sempre **uma linha em branco** antes e depois de qualquer `:::`, lista (`-`, `1.`) ou bloco de código.
- Ordem estrita de atributos dentro de `{}`: **1º Identificador (`#id`) ➔ 2º Classes (`.classe`) ➔ 3º Pares chave-valor (`key="val"`)**. Exemplo: `::: {#nte-aviso .callout-note collapse="true"}`.

## 4. Migração de Configuração de Projeto
- Migre `_bookdown.yml` e `_output.yml` para um único `_quarto.yml` na raiz.
- Lembre-se da **Exceção de Fusão da Chave `format:`**: enquanto todas as chaves de `_quarto.yml`, `dir/_metadata.yml` e `doc.qmd` sofrem *deep-merge*, declarar `format:` no cabeçalho de um `.qmd` individual **sobrescreve integralmente** os formatos globais do projeto para aquele ficheiro.
