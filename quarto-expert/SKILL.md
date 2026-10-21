---
name: quarto-expert
description: "Cria, configura, depura e migra documentos e projetos Quarto (.qmd, book, website, Typst, LaTeX, ABNT, RevealJS, celulas e diagramas) com uv/Python e R."
---

# Skill: quarto-expert (Engenharia, Autoria e Publicação Científica com Quarto)

> Baseado no ecossistema Quarto CLI v1.9+ e alinhado aos padrões oficiais Posit/Quarto Authoring.

Este módulo governa a arquitetura, autoria técnica, sintaxe de células, metadados YAML, compilação multi-formato, migração de ecossistemas legados (R Markdown, Bookdown, Jupyter, Xaringan) e resolução de problemas no ecossistema **Quarto CLI**, operando de forma acoplada às Meta-Skills do ambiente (`pre-code-pipeline`, `execution-pipeline`, `writing-pipeline`, `release-and-ops-pipeline` e `audit-and-refactoring-pipeline`).

---

## 1. Regras Críticas (Substituem Hábitos Legados de R Markdown / Pandoc) <!-- ## 1. Regras Criticas -->

> [!IMPORTANT]
> Estas regras têm precedência absoluta sobre dados de treino legados ou convenções de Markdown genéricas.

1. **Opções de Célula via Hashpipe (`#|`)**:
   - **R, Python, Julia:** use `#|` no início de cada linha de opção dentro da célula.
   - **Mermaid:** use `%%|`.
   - **Graphviz/DOT:** use `//|`.
   - Opções utilizam **hífens, nunca pontos** (`fig-cap` e não `fig.cap`; `fig-width` e não `fig.width`).
   - Valores booleanos estritamente em minúsculas (`true`/`false`).
   - PROIBIDO colocar opções na linha de abertura da célula (ex.: nunca use ````{r, echo=FALSE}````).
   ````markdown
   ```{python}
   #| label: fig-dispersao
   #| fig-cap: "Curva ajustada e dispersão dos resíduos."
   #| echo: false
   #| warning: false
   ```
   ````
2. **Células Executáveis vs. Blocos Estáticos**:
   - Executável (compilada pelo motor `jupyter` ou `knitr`): ````{python}```` ou ````{r}````.
   - Estática (apenas realce de sintaxe sem execução): ````python```` ou ````{.python}````.
3. **Diferença Crítica de Cache entre Motores (`knitr` vs `jupyter`)**:
   - `#| cache: true` em célula individual funciona **apenas** no motor R (`knitr`).
   - No Python/Jupyter, `#| cache: true` em células individuais é silenciosamente ignorado. O cache para Jupyter deve ser configurado no YAML do documento:
     ```yaml
     execute:
       cache: true
     ```
     (requer pacote `jupyter-cache` instalado no ambiente).
4. **Ordem Posicional de Atributos e Espaçamento Obrigatório**:
   - Insira sempre uma linha em branco antes e depois de listas (`-`, `1.`), *callouts*, *fenced divs* (`:::`) e blocos de código.
   - Dentro de `{ #id .classe key="valor" }`: **1º Identificador (`#`) ➔ 2º Classes (`.`) ➔ 3º Pares `chave="valor"`**.
5. **Prefixos Obrigatórios de Referência Cruzada (`@prefixo-id`)**:
   - Figuras: `#fig-` | Tabelas: `#tbl-` | Secções: `#sec-` | Equações: `#eq-` | Listagens: `#lst-` | Teoremas: `#thm-` | Callouts: `#nte-`, `#tip-`, `#wrn-`, `#imp-`, `#cau-`.
   - A referência no texto é feita via `@prefixo-id` (ex.: `@fig-dispersao`).
6. **Exceção de Fusão da Chave `format:`**:
   - Hierarquia de resolução (menor → maior precedência): `_quarto.yml` ➔ `_quarto-{perfil}.yml` ➔ `dir/_metadata.yml` ➔ `dir/documento.qmd` ➔ `_quarto.yml.local`.
   - Todas as chaves sofrem fusão recursiva (*deep-merge*), **EXCETO `format:` no cabeçalho de um `.qmd` individual**, que substitui integralmente a configuração herdada.
7. **Identidade Visual Unificada via `_brand.yml` (Quarto 1.5+)**:
   - O arquivo `_brand.yml` na raiz do projeto é descoberto automaticamente pelo Quarto CLI, sincronizando paletas de cores, tipografia e logotipos entre relatórios HTML, dashboards interativos, apresentações RevealJS e documentos Typst.
8. **Acessibilidade e Descrição de Gráficos (`fig-alt`)**:
   - Adicione texto alternativo descritivo em todos os gráficos gerados via `#| fig-alt: > ...` ou imagens estáticas `![legenda](path.png){fig-alt="..."}` para conformidade com leitores de tela e auditorias analíticas.
9. **Seleção Estratégica do Motor PDF**:
   - **`format: typst`** (nativo, ultra-rápido, zero dependências externas) para relatórios técnicos, notas de margem e livros modernos.
   - **`format: pdf` (`pdf-engine: lualatex` ou `xelatex` via TinyTeX)** para teses ABNT NBR 14724:2024, depósitos arquivísticos PDF/A-1b e periódicos acadêmicos rígidos.
10. **Integração com o Ambiente Operacional e Runtimes**:
   - Binários canônicos: Quarto em `/opt/quarto/bin/quarto`, R em `/usr/bin/R`, Python via `/home/tales/.local/bin/uv` ou `miniforge3`.
   - Para renderização de cadernos Python no Quarto, defina o interpretador com Jupyter:
     ```bash
     export QUARTO_PYTHON=/home/tales/miniforge3/envs/science/bin/python
     ```
     Ou execute via `uv`: `uv run --with jupyter,matplotlib quarto render`.

---

## 1.1 Árvore de Decisão: Escolha do Motor e Formato <!-- ## 1.1 Arvore de Decisao -->

| Necessidade do Projeto | Formato / Motor Recomendado | Guia de Referência |
| :--- | :--- | :--- |
| **TCC / Dissertação ABNT NBR 14724:2024** | LaTeX (`danielvartan/abnt`) ou Typst | `/home/tales/.gemini/config/skills/quarto-expert/references/abnt-thesis-guide.md` |
| **PDF Técnico de Alta Velocidade (sem LaTeX)** | Typst (`format: typst`) | `/home/tales/.gemini/config/skills/quarto-expert/references/typst-and-templates.md` |
| **Layout com Notas de Margem (Estilo Tufte)** | Typst (`marginalia` / `bookly`) | `/home/tales/.gemini/config/skills/quarto-expert/references/typst-and-templates.md` |
| **Identidade Corporativa Unificada (Cores/Fontes)** | `_brand.yml` (HTML, Typst, RevealJS) | `/home/tales/.gemini/config/skills/quarto-expert/references/brand-yml.md` |
| **Portal Web / Documentação Navegável** | HTML (`project.type: website`) | `/home/tales/.gemini/config/skills/quarto-expert/references/yaml-front-matter.md` |
| **Apresentações com Código e Gráficos** | RevealJS (`format: revealjs`) | `/home/tales/.gemini/config/skills/quarto-expert/references/yaml-front-matter.md` |
| **Manuscrito Reprodutível com Cadernos + Binder** | `project.type: manuscript` + MECA | `/home/tales/.gemini/config/skills/quarto-expert/references/yaml-front-matter.md` |
| **Migração de R Markdown legada (.Rmd)** | Quarto (.qmd) + Hashpipe `#|` | `/home/tales/.gemini/config/skills/quarto-expert/references/conversion-rmarkdown.md` |
| **Conversão de Cadernos Jupyter (.ipynb)** | `quarto convert` ou pareamento `.qmd` | `/home/tales/.gemini/config/skills/quarto-expert/references/conversion-jupyter.md` |
| **Migração de Bookdown / Blogdown / Distill** | Quarto Book ou Quarto Website | `/home/tales/.gemini/config/skills/quarto-expert/references/conversion-bookdown.md` |

---

## 2. Referências Modulares e Guias Especializados <!-- ## 2. Referencias Modulares -->

Todas as instruções detalhadas, tabelas de mapeamento e runbooks foram modularizados no diretório `references/` para preservar o orçamento de contexto (*progressive disclosure*):

### 2.1 Normas Acadêmicas e Templates Especiais
- **Teses e Dissertações ABNT NBR 14724:2024:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/abnt-thesis-guide.md`
- **Typst, Marginalia e Criação de Templates Customizados:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/typst-and-templates.md`

### 2.2 Sintaxe QMD, Elementos e Recursos Visuais
- **Células de Código e Sintaxe Hashpipe (`#|`, `%%|`, `//|`):**
  `/home/tales/.gemini/config/skills/quarto-expert/references/code-cells.md`
- **Referências Cruzadas e Prefixos Oficiais:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/cross-references.md`
- **Blocos Callouts (5 tipos, colapsáveis e títulos):**
  `/home/tales/.gemini/config/skills/quarto-expert/references/callouts.md`
- **Figuras, Subfiguras, Alinhamento e Lightbox:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/figures.md`
- **Tabelas (Pipe, Grid, Estilização e Cross-ref):**
  `/home/tales/.gemini/config/skills/quarto-expert/references/tables.md`
- **Diagramas Nativos (Mermaid e Graphviz/DOT):**
  `/home/tales/.gemini/config/skills/quarto-expert/references/diagrams.md`
- **Citações, Arquivos BibTeX/CSL e Notas de Rodapé:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/citations.md`
- **Divs e Spans Fenced (`:::`, `.class`, raw blocks):**
  `/home/tales/.gemini/config/skills/quarto-expert/references/divs-and-spans.md`
- **Layout de Página, Colunas e Conteúdo de Margem:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/layout.md`
- **Shortcodes Nativos (`meta`, `var`, `env`):**
  `/home/tales/.gemini/config/skills/quarto-expert/references/shortcodes.md`
- **Conteúdo Condicional por Perfil ou Formato:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/conditional-content.md`

### 2.3 Configuração de Projetos, Motores e Identidade Visual
- **Metadados YAML de Documentos e Projetos (`_quarto.yml`):**
  `/home/tales/.gemini/config/skills/quarto-expert/references/yaml-front-matter.md`
- **Identidade Visual com Brand.yml (`_brand.yml`):**
  `/home/tales/.gemini/config/skills/quarto-expert/references/brand-yml.md`
- **Acessibilidade e Texto Alternativo (`fig-alt`):**
  `/home/tales/.gemini/config/skills/quarto-expert/references/alt-text.md`
- **Motores Computacionais (`knitr`, `jupyter`, `julia`):**
  `/home/tales/.gemini/config/skills/quarto-expert/references/engines.md`
- **Extensões Quarto (Instalação, Uso e Criação):**
  `/home/tales/.gemini/config/skills/quarto-expert/references/extensions.md`
- **Linting de Markdown e Boas Práticas Estruturais:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/markdown-linting.md`

### 2.4 Migração de Ecossistemas Legados para Quarto
- **R Markdown (.Rmd) para Quarto (.qmd):**
  `/home/tales/.gemini/config/skills/quarto-expert/references/conversion-rmarkdown.md`
- **Cadernos Jupyter (.ipynb) para Quarto:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/conversion-jupyter.md`
- **Projetos Bookdown para Quarto Books:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/conversion-bookdown.md`
- **Apresentações Xaringan para RevealJS:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/conversion-xaringan.md`
- **Artigos Distill para Quarto:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/conversion-distill.md`
- **Websites Blogdown para Quarto Websites:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/conversion-blogdown.md`
- **Guia Complementar de Migração Rmd:**
  `/home/tales/.gemini/config/skills/quarto-expert/references/rmd-to-quarto-migration.md`

### 2.5 Utilitários e Scripts de Automação
- **Inicializador de Projetos:** `/home/tales/.gemini/config/skills/quarto-expert/scripts/init_quarto_project.sh`
- **Validador Rápido de Skill:** `/home/tales/.gemini/config/skills/quarto-expert/scripts/validate_skill.sh`
- **Validador Profundo com Compilação:** `/home/tales/.gemini/config/skills/quarto-expert/scripts/validate_skill_deep.sh`
- **Verificador Pós-Execução:** `/home/tales/.gemini/config/skills/quarto-expert/scripts/verify_skill.sh`
- **Integração `graphify` (referência compartilhada entre 5 Meta-Skills):** `/home/tales/.gemini/config/skills/quarto-expert/references/graphify-integration.md`

---

## 3. Síntese dos Fundamentos QMD (QMD Essentials)

### 3.1 Anatomia Canônica de um Arquivo `.qmd`
Todo documento Quarto combina metadados estruturados e corpo markdown rico:
```markdown
---
title: "Relatório de Análise"
author: "Nome do Autor"
date: today
format:
  html:
    toc: true
    code-fold: true
    theme: cosmo
execute:
  echo: false
  warning: false
---

## Introdução {#sec-intro}

Conforme demonstrado em @sec-intro e detalhado em @fig-metricas...
```

### 3.2 Chamadas de Destaque (*Callouts*)
Existem 5 tipos padronizados de callouts, que suportam colapso e títulos customizados:
```markdown
::: {.callout-note}
Nota explicativa padrão.
:::

::: {.callout-tip collapse="true"}
## Dica de Otimização (Clique para expandir)
Conteúdo recolhido por padrão.
:::
```

### 3.3 Subfiguras e Layouts em Grade
```markdown
::: {#fig-comparativo layout-ncol=2}
![Distribuição A](fig-a.png){#fig-sub-a}

![Distribuição B](fig-b.png){#fig-sub-b}

Comparativo das distribuições de dados antes e após a normalização.
:::
```

### 3.4 Diagramas Nacionais (Mermaid e Graphviz)
````markdown
```{mermaid}
%%| label: fig-pipeline
%%| fig-cap: "Pipeline de engenharia de features."
flowchart LR
    A[Dados Brutos] --> B(Tratamento)
    B --> C{Validação}
    C -->|OK| D[Modelo]
```
````

---

## 4. Arquiteturas de Projeto e Workflows

| Tipo (`project.type`) | Saída Padrão | Cenário Principal de Aplicação |
| :--- | :---: | :--- |
| **`default`** | Diretório local (ou `output-dir`) | Relatórios independentes com `_quarto.yml` compartilhado |
| **`website` / `blog`** | `_site/` (ou `docs/`) | Portais de documentação, landing pages e blogs analíticos |
| **`book`** | `_book/` | Livros técnicos e teses em múltiplos capítulos |
| **`manuscript`** | `_manuscript/` | Artigo científico com cadernos em `notebooks/` + pacote MECA |

---

## 5. Resolução de Problemas e Armadilhas Conhecidas <!-- ## 5. Resolucao de Problemas -->

1. **Incompatibilidade de Cache no Jupyter:**
   - *Problema:* Adicionar `#| cache: true` em célula Python não gera erro mas não funciona.
   - *Solução:* Use `execute: cache: true` no topo do YAML do documento e assegure `jupyter-cache` instalado.
2. **Bug de Preview em Extensões PDF de Livros (Quarto CLI Issue #14582):**
   - *Problema:* `quarto preview --to <ext>-pdf` num `type: book` exibe PDF bruto no navegador.
   - *Solução:* Use `quarto render --to <ext>-pdf` ou execute preview por capítulo individual.
3. **Falha de CI/CD com `freeze: auto`:**
   - *Problema:* Células executadas em máquina local quebram a pipeline se o `.qmd` for editado sem renderizar.
   - *Solução:* Execute `quarto render` antes do commit para regenerar o cache em `_freeze/`.
4. **Espaçamento e Linting de Fenced Divs:**
   - *Problema:* O renderizador falha em detectar classes se `:::` estiver colado a parágrafos ou títulos.
   - *Solução:* Mantenha rigorosamente uma linha vazia antes e depois de blocos delimitados.
5. **Configuração de Interpretador Python:**
   - Se o Quarto acusar falta de Jupyter, verifique a variável `QUARTO_PYTHON` apontando para o ambiente adequado.

---

## 6. Exemplos de Prompts de Ativação <!-- ## 6. Exemplos de Prompts -->

- "Crie um projeto Quarto para tese ABNT NBR 14724:2024 com bibliografia BibTeX."
- "Migre este script R Markdown (.Rmd) antigo para Quarto (.qmd) adotando sintaxe hashpipe."
- "Configure um manuscrito reprodutível com cadernos Jupyter vinculados e pacote MECA."
- "Preciso de um relatório executivo em PDF gerado via Typst com notas de margem."
- "Configure um arquivo `_brand.yml` para padronizar cores, logotipo e fontes corporativas."
- "Adicione referências cruzadas e diagramas Mermaid neste relatório Quarto."

---

## 7. Projetos de Exemplo (Copy-Paste Ready)

- `/home/tales/.gemini/config/skills/quarto-expert/examples/minimal-report/` — Relatório HTML mínimo auto-contido.
- `/home/tales/.gemini/config/skills/quarto-expert/examples/abnt-thesis-starter/` — Tese acadêmica segundo a ABNT NBR 14724:2024.
- `/home/tales/.gemini/config/skills/quarto-expert/examples/manuscript-binder/` — Manuscrito com cadernos e Binder.

---

## 8. Autovalidação

Antes de finalizar qualquer alteração nesta skill, execute a validação estática:

```bash
/home/tales/.gemini/config/skills/quarto-expert/scripts/validate_skill.sh
```

---

## 9. Validação Profunda e Hooks de Git <!-- ## 9. Validacao Profunda -->

### 9.1 Validação em Dois Níveis
- **Rápida** (`scripts/validate_skill.sh`): frontmatter, caminhos internos, sintaxe YAML e `bash -n`.
- **Profunda** (`scripts/validate_skill_deep.sh`): validação rápida + checagem de binários + compilação headless de exemplos.

### 9.2 Pre-commit Hook
Para instalar o hook local:
```bash
/home/tales/.gemini/config/skills/quarto-expert/scripts/install_hooks.sh
```

### 9.3 Backup Automático de `examples/`
```bash
/home/tales/.gemini/config/skills/quarto-expert/scripts/backup_examples.sh
```

---

## 10. Verificação Pós-Execução (`verify_skill.sh`) <!-- ## 10. Verificacao Pos-Execucao -->

Audita a integridade de todas as etapas da skill:
```bash
/home/tales/.gemini/config/skills/quarto-expert/scripts/verify_skill.sh
```
Modo estruturado para automação:
```bash
/home/tales/.gemini/config/skills/quarto-expert/scripts/verify_skill.sh --json
```
