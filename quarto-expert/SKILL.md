---
name: quarto-expert
description: "Cria, configura e depura documentos e projetos Quarto (.qmd, manuscript, book, website, Typst, LaTeX/TinyTeX, ABNT NBR 14724 e RevealJS) com Python/uv e R."
---

# Skill: quarto-expert (Engenharia e Publicação Científica com Quarto)

Este módulo governa a arquitetura, sintaxe avançada, configuração de metadados, compilação multi-formato e resolução de problemas no ecossistema **Quarto CLI**, operando em conjunto com as 5 Meta-Skills do ambiente.

---

## 1. Regras Críticas (Substituem Hábitos Legados de R Markdown / Pandoc) <!-- ## 1. Regras Criticas -->

> [!IMPORTANT]
> Estas regras têm precedência absoluta sobre dados de treino antigos do modelo.

1. **Opções de Célula via Hashpipe (`#|`)**: Nunca coloque opções de execução dentro das chavetas do cabeçalho (PROIBIDO ```` ```{r, echo=FALSE} ````). Use exclusivamente comentários YAML `#|` no topo da célula com booleanos em minúsculas (`true`/`false`):
   ````markdown
   ```{python}
   #| label: fig-regressao
   #| fig-cap: "Curva de calibração e resíduos."
   #| echo: false
   #| warning: false
   ```
   ````
2. **Células Executáveis vs. Blocos Estáticos**:
   - Executável (avaliada por `jupyter` ou `knitr` em ordem sequencial estrita): ```` ```{python} ```` ou ```` ```{r} ````.
   - Estática (apenas realce sintático): ```` ```{.python} ```` ou ```` ```python ````.
3. **Ordem Posicional de Atributos e Espaço em Branco**:
   - Insira uma linha em branco antes e depois de listas (`-`, `1.`), *fenced divs* (`:::`) e blocos de código.
   - Dentro de `{#id .classe key="valor"}`: **1º Identificador (`#`) ➔ 2º Classes (`.`) ➔ 3º Pares `chave="valor"`**.
4. **Prefixos Obrigatórios de Referência Cruzada (`@prefixo-id`)**:
   - Figuras: `#fig-` | Tabelas: `#tbl-` | Secções: `#sec-` | Equações: `#eq-` | Listagens: `#lst-` | Teoremas: `#thm-` | Callouts: `#nte-`, `#tip-`, `#wrn-`, `#imp-`, `#cau-`.
5. **Exceção de Fusão da Chave `format:`**:
   - Hierarquia (menor → maior precedência): `_quarto.yml` ➔ `_quarto-{perfil}.yml` ➔ `dir/_metadata.yml` ➔ `dir/documento.qmd` ➔ `_quarto.yml.local`.
   - Todas as chaves sofrem fusão recursiva (*deep-merge*), **EXCETO `format:` no cabeçalho de um `.qmd` individual**, que substitui integralmente.
6. **Seleção do Motor PDF**:
   - **`format: typst`** (embutido, instantâneo, zero dependências) para relatórios, livros modernos e notas de margem.
   - **`format: pdf` (`pdf-engine: lualatex` ou `xelatex` via TinyTeX)** para periódicos, PDF/A-1b e ABNT NBR 14724.
7. **Integração com o Ambiente Global**:
   - Binários canônicos: Quarto em `/opt/quarto/bin/quarto`, R em `/usr/bin/R`, Python gerido via `/home/tales/.local/bin/uv`.
   - **Jupyter/Knitr obrigatórios:** o Python padrão (`/usr/bin/python3`) **NÃO** possui `jupyter`/`nbformat`/`matplotlib`. Para render com células Python, exporte antes do `quarto render`:
     ```bash
     export QUARTO_PYTHON=/home/tales/miniforge3/envs/science/bin/python
     ```
     Alternativa robusta com `uv`: `uv run --with jupyter,matplotlib quarto render`.
   - **Auto-detecção:** `scripts/validate_skill_deep.sh` detecta automaticamente o primeiro Python com Jupyter disponível (`miniforge science` → `miniforge base` → `python3` do PATH).
   - Para relatórios analíticos do **Arquétipo A**, aplique sempre o checklist `/home/tales/.gemini/config/skills/pre-code-pipeline/references/quarto-quality-checklist.md` (`lang: pt-BR`, `execute: freeze: auto`, zero numeração manual nos títulos com `number-sections: true`, `dpi=300`, `sns.despine()` e `set_box_aspect(1)` em subfiguras lado a lado).

---

## 1.1 Árvore de Decisão: Escolha do Motor de Renderização <!-- ## 1.1 Arvore de Decisao -->

- Template de periódico estrito / validação LaTeX? ➔ **LaTeX (`pdf-engine: lualatex` via TinyTeX)**
- Depósito PDF/A-1b arquivístico? ➔ **LaTeX (`cnam-thesis`)**
- TCC / Dissertação ABNT NBR 14724:2024? ➔ **LaTeX (`danielvartan/abnt`)**
- Velocidade máxima em PDF sem LaTeX? ➔ **Typst (`format: typst`)**
- Notas de margem / layout Tufte? ➔ **Typst (`marginalia` / `bookly`)**
- Documento web navegável / site? ➔ **HTML (`type: website`)**
- Slides interativos com código executável? ➔ **RevealJS + `quarto-live`**

---

## 2. Referências Modulares e Scripts Sob Demanda <!-- ## 2. Referencias Modulares -->

- **Teses e TCCs Brasileiros:** `/home/tales/.gemini/config/skills/quarto-expert/references/abnt-thesis-guide.md`
- **Typst, Marginalia e Templates:** `/home/tales/.gemini/config/skills/quarto-expert/references/typst-and-templates.md`
- **Migração `.Rmd` → `.qmd`:** `/home/tales/.gemini/config/skills/quarto-expert/references/rmd-to-quarto-migration.md`
- **Inicialização de Projeto:** `/home/tales/.gemini/config/skills/quarto-expert/scripts/init_quarto_project.sh`
- **Validação Rápida:** `/home/tales/.gemini/config/skills/quarto-expert/scripts/validate_skill.sh`

---

## 3. Arquiteturas de Projeto e Workflows

| Tipo (`project.type`) | Diretório de Saída | Caso de Uso Primário |
| :--- | :---: | :--- |
| **`default`** | Mesmo diretório (ou `output-dir`) | Relatórios independentes com `_quarto.yml` partilhado |
| **`website` / `blog`** | `_site/` (ou `docs/`) | Árvore de diretórios mapeada em URLs; `index.qmd` como landing page |
| **`book`** | `_book/` | Estrutura hierárquica (`chapters:`, `appendices:`) |
| **`manuscript`** | `_manuscript/` | Artigo + cadernos em `notebooks/` + MECA bundle |

### Workflow A: Relatório HTML Mínimo

Referência: `examples/minimal-report/`.

### Workflow B: Manuscrito Científico (`type: manuscript` + MECA + Binder)

Referência: `examples/manuscript-binder/`.

Regra do Binder: `quarto use binder` **não inspeciona `.qmd`**; exige manifesto (`requirements.txt`, `environment.yml`, `renv.lock`, `install.R`).

### Workflow C: Apresentações (RevealJS, Touying, Beamer, PPTX)

Slide boundaries via `## Título` ou `---`. Colunas via `:::: {.columns}` + `::: {.column width="50%"}`.

---

## 4. Perfis, Variáveis de Ambiente e Scripts

- **Perfis (`--profile`):** `_quarto-{perfil}.yml` + `_environment-{perfil}`.
- **Conteúdo condicional:** `::: {.content-visible when-profile="advanced"}`.
- **Scripts Deno/Lua:** `quarto run script.ts`; verifique `QUARTO_PROJECT_RENDER_ALL`.

---

## 5. Resolução de Problemas e Armadilhas Conhecidas <!-- ## 5. Resolucao de Problemas -->

1. **Bug de Preview em Extensões PDF de Livros (Quarto CLI Issue #14582)**: `quarto preview --to <ext>-pdf` num `type: book` entrega PDF bruto. *Solução:* `quarto render --to <ext>-pdf` ou preview de capítulos.
2. **Falha de CI/CD com `freeze: true/auto`:** edite `.qmd` exige `quarto render` local antes de commit.
3. **Ignorância Silenciosa de Perfis Inexistentes:** `quarto render --profile <nome>` falha silenciosamente se `_quarto-<nome>.yml` não existe.
4. **Preview de Ficheiro Isolado vs. Projeto:** botão *Preview* na IDE roda apenas `quarto preview doc.qmd --to default`.

---

## 6. Exemplos de Prompts de Ativação <!-- ## 6. Exemplos de Prompts -->

- "Crie um projeto Quarto para o meu TCC seguindo a norma ABNT NBR 14724:2024."
- "Configure um manuscrito científico com MECA bundle, cadernos embutidos e Binder."
- "Migre meu relatório legado R Markdown (.Rmd) para Quarto nativo (.qmd)."
- "Preciso de um relatório PDF rápido com notas laterais na margem, sem instalar LaTeX."
- "Transforme estes cadernos Jupyter (.ipynb) em um website Quarto responsivo."

---

## 7. Projetos de Exemplo (Copy-Paste Ready)

- `/home/tales/.gemini/config/skills/quarto-expert/examples/minimal-report/` — Relatório HTML mínimo.
- `/home/tales/.gemini/config/skills/quarto-expert/examples/abnt-thesis-starter/` — TCC/dissertação ABNT via Typst.
- `/home/tales/.gemini/config/skills/quarto-expert/examples/manuscript-binder/` — Manuscrito com MECA + Binder.

---

## 8. Autovalidação

Antes de finalizar qualquer alteração nesta skill:

```bash
/home/tales/.gemini/config/skills/quarto-expert/scripts/validate_skill.sh
```

---

## 9. Validação Profunda e Hooks de Git <!-- ## 9. Validacao Profunda -->

### 9.1 Validação em Dois Níveis

- **Rápida** (`scripts/validate_skill.sh`): frontmatter, caminhos, YAML, `bash -n`.
- **Profunda** (`scripts/validate_skill_deep.sh`): rápida + binários + render headless.

### 9.2 Pre-commit Hook (Versionado)

Instalação:
```bash
/home/tales/.gemini/config/skills/quarto-expert/scripts/install_hooks.sh
```

### 9.3 Backup Automático de `examples/`

```bash
/home/tales/.gemini/config/skills/quarto-expert/scripts/backup_examples.sh
```

---

## 10. Verificação Pós-Execução (`verify_skill.sh`) <!-- ## 10. Verificacao Pos-Execucao -->

Script de segunda camada que audita 6 etapas: estrutura, referências, scripts, exemplos, conteúdo do `SKILL.md` e integridade Git.

```bash
# Modo humano (ANSI)
/home/tales/.gemini/config/skills/quarto-expert/scripts/verify_skill.sh

# Modo JSON (CI/CD)
/home/tales/.gemini/config/skills/quarto-expert/scripts/verify_skill.sh --json
```

**Códigos de saída:** `0` = OK, `1` = falha crítica, `2` = aviso.
