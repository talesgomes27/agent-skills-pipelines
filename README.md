# Ecossistema de Meta-Skills: Engenharia, Dados e Operações

Este repositório centraliza a arquitetura, governança e manuais operacionais das **5 Meta-Skills**, da skill especialista **`quarto-expert`** e dos módulos de suporte integrados ao Google Antigravity e Gemini CLI em `/home/tales/.gemini/config/skills/`.

A arquitetura organiza o ciclo de vida técnico em esteiras polimórficas (adaptadas aos Arquétipos A, B e C), separando fluxos de desenvolvimento novo (*Greenfield*) e modernização de código legado (*Brownfield*), com garantia de qualidade contínua, governança estrita de runtimes e orçamento de contexto controlado por *progressive disclosure*.

---

### Métricas de Engenharia e Cobertura do Ecossistema

| Dimensão | Quantidade / Métrica | Observações |
| :--- | :---: | :--- |
| **Skills Totais no Repositório** | **8 skills** | 5 Meta-Skills + 1 Especialista (`quarto-expert`) + 2 Suporte (`humanizer`, `skill-loader`) |
| **Guias Modulares em `references/`** | **41 referências** | 15 nas Meta-Skills + 26 na especialista `quarto-expert` |
| **Templates Prontos (`examples/`)** | **3 suítes** | `minimal-report`, `abnt-thesis-starter` e `manuscript-binder` |
| **Scripts e Utilitários de QA** | **7 ferramentas** | Inicialização, validação estática, compilação profunda, pre-commit e auditoria |
| **Orçamento de Header por Skill** | **< 80 tokens** | Todas as 8 skills consomem entre 43 e 72 tokens no cabeçalho do prompt permanente |
| **Status de Verificação Pós-Execução** | **40 OK \| 0 WARN \| 0 FAIL** | Auditado deterministicamente via `scripts/verify_skill.sh` |

---

## 1. Topologia do Ciclo de Vida Técnico

O ecossistema divide as demandas em duas portas de entrada principais, com coordenação transversal da esteira editorial e documental, e motor especialista de publicação científica:

```text
 ┌────────────────────────────────────────────────────────┐
 │               PROJETOS GREENFIELD (Novos)              │
 └────────────────────────────────────────────────────────┘
                            │
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ 1. pre-code-pipeline (Gates 1 a 5)                     │
 │    PRD, Arquitetura, DB, TDD / CRISP-ML(Q) Data Story  │
 └────────────────────────────────────────────────────────┘
                            │ (Handoff Gate 5)
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ 2. execution-pipeline (Gates 1 a 5)                    │ ◄────────────────────────┐
 │    Implementação, Testes, Visualização e Build         │                          │
 └────────────────────────────────────────────────────────┘                          │
                            │ (Handoff Gate 5)                                       │ (Rota 2: Novas
                            ▼                                                        │  Features)
 ┌────────────────────────────────────────────────────────┐                          │
 │ 4. release-and-ops-pipeline (Gates 1 a 5)              │ ◄───────────┐            │
 │    Saneamento, SemVer, CI/CD, Deploy e Smoke Tests     │             │            │
 └────────────────────────────────────────────────────────┘             │            │
                                                                        │            │
 ┌────────────────────────────────────────────────────────┐             │ (Rota 1:   │
 │             PROJETOS BROWNFIELD (Legados)              │             │  Deploy)   │
 └────────────────────────────────────────────────────────┘             │            │
                            │                                           │            │
                            ▼                                           │            │
 ┌────────────────────────────────────────────────────────┐             │            │
 │ 5. audit-and-refactoring-pipeline (Gates 1 a 5)        │ ────────────┴────────────┘
 │    Reconhecimento, Diagnóstico, Safety Net, Refactor   │
 └────────────────────────────────────────────────────────┘
                            ▲
                            │ Modo 2 (Auditoria Tabular Não-Destrutiva)
                            │
 ┌────────────────────────────────────────────────────────┐
 │ 3. writing-pipeline (Transversal)                      │
 │    Modo 1: Redação Direta (PRDs, READMEs, ADRs, .qmd)  │
 │    Modo 2: Revisão Não-Destrutiva em Tabela            │
 └────────────────────────────────────────────────────────┘
                            │
                            ▼ Modo 1 (Geração)
    [Invocado nos Gates 4 das Pipelines de Planejamento, Execução e Release]

 ┌────────────────────────────────────────────────────────┐
 │ quarto-expert (Especialista Arquétipo A)               │
 │ Motor Quarto CLI: HTML, Typst, LaTeX/ABNT, Manuscript  │
 └────────────────────────────────────────────────────────┘
    [Acoplada nos Gates 3–4 da Pre-Code, Gates 2–4 da Execution,
     Gate 2 da Release-and-Ops e Gates 2, 4 e 5 da Audit-and-Refactoring]
```

### Interação entre Esteiras

- **Fluxo Greenfield:** Inicia em `pre-code-pipeline`. Passa pelo afunilamento dos 5 Gates de planejamento até o handoff formal para `execution-pipeline`. Concluída a implementação e testes, o handoff segue para `release-and-ops-pipeline` para saneamento, versionamento e deploy.
- **Fluxo Brownfield:** Repositórios legados entram exclusivamente por `audit-and-refactoring-pipeline`. A esteira cataloga o estado atual sem modificações destrutivas (Gates 1–2), estabelece testes de caracterização (*Golden Master*, Gate 3) e aplica refatorações cirúrgicas (Gate 4). No Gate 5, o projeto saneado é despachado para publicação (`release-and-ops-pipeline`) ou para desenvolvimento de novas capacidades (`execution-pipeline`).
- **Atuação Transversal da `writing-pipeline`:**
  - **Modo 1 (Geração Direta):** Invocado pelos Gates 4 da `pre-code-pipeline`, `execution-pipeline` e Gate 2 da `release-and-ops-pipeline` para redação técnica padronizada via `humanizer` (voz sênior anti-IA e burstiness balanceado).
  - **Modo 2 (Revisão Tabular Não-Destrutiva):** Invocado no Gate 2 da `audit-and-refactoring-pipeline` para registrar achados na matriz `ID | Arquivo | Severidade | Original | Sugestão | Racional`.
- **Atuação Especialista da `quarto-expert`:**
  - Governa toda a engenharia de documentos para o **Arquétipo A**: relatórios analíticos, apresentações RevealJS, livros técnicos, teses/dissertações ABNT NBR 14724:2024 (via `danielvartan/abnt` e Typst), manuscritos reprodutíveis MECA + Binder e migração de legados R Markdown, Bookdown e Jupyter.

---

## 2. As 5 Meta-Skills e seus 15 Arquivos de Referência

| Meta-Skill | Propósito Operacional | Arquivos de Referência (`references/`) | Comandos de Ativação |
| :--- | :--- | :--- | :--- |
| [**`pre-code-pipeline`**](file:///home/tales/.gemini/config/skills/pre-code-pipeline/SKILL.md) | Conduz o planejamento pré-código em 5 Gates sequenciais para Engenharia de Software e Ciência de Dados (CRISP-ML(Q) + Data Storytelling: Ask, Prepare, Process, Construct, Share, Act). | 1. [`quarto-quality-checklist.md`](file:///home/tales/.gemini/config/skills/pre-code-pipeline/references/quarto-quality-checklist.md) *(1)* | `use a pre-code-pipeline`<br>`iniciar planejamento pré-código` |
| [**`execution-pipeline`**](file:///home/tales/.gemini/config/skills/execution-pipeline/SKILL.md) | Guia a implementação técnica, testes unitários/integração, visualizações e documentação em 5 Gates polimórficos pós-planejamento. | *(Herda contratos de `pre-code-pipeline` e orquestra `writing-pipeline`, `quarto-expert` e `release-and-ops-pipeline`)* *(0)* | `use a execution-pipeline`<br>`iniciar execução técnica` |
| [**`writing-pipeline`**](file:///home/tales/.gemini/config/skills/writing-pipeline/SKILL.md) | Autoridade editorial para redação sênior e revisão técnica. Opera no Modo 1 (geração direta) e Modo 2 (revisão tabular não-destrutiva). | 2. [`archetype-a-academic.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/archetype-a-academic.md)<br>3. [`archetype-b-software.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/archetype-b-software.md)<br>4. [`archetype-c-cli.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/archetype-c-cli.md)<br>5. [`before-after-examples.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/before-after-examples.md)<br>6. [`canonical-sources.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/canonical-sources.md)<br>7. [`metrics-and-anti-ai.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/metrics-and-anti-ai.md)<br>8. [`review-protocol.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/review-protocol.md) *(7)* | `use a writing-pipeline`<br>`redigir documento`<br>`revisar texto em tabela` |
| [**`release-and-ops-pipeline`**](file:///home/tales/.gemini/config/skills/release-and-ops-pipeline/SKILL.md) | Governa a entrega pós-execução em 5 Gates: saneamento pré-push, versionamento Git/SemVer, CI/CD, deploy polimórfico e smoke tests. | 9. [`archetype-a-ghpages.md`](file:///home/tales/.gemini/config/skills/release-and-ops-pipeline/references/archetype-a-ghpages.md)<br>10. [`pre-push-sanitation.md`](file:///home/tales/.gemini/config/skills/release-and-ops-pipeline/references/pre-push-sanitation.md)<br>11. [`smoke-and-healthcheck.md`](file:///home/tales/.gemini/config/skills/release-and-ops-pipeline/references/smoke-and-healthcheck.md) *(3)* | `use a release-and-ops-pipeline`<br>`publicar release`<br>`executar deploy e smoke tests` |
| [**`audit-and-refactoring-pipeline`**](file:///home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/SKILL.md) | Conduz engenharia reversa, diagnóstico multi-camadas, testes de caracterização (*Golden Master*) e refatoração incremental em código legado. | 12. [`archetype-a-analytics-audit.md`](file:///home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/references/archetype-a-analytics-audit.md)<br>13. [`characterization-tests.md`](file:///home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/references/characterization-tests.md)<br>14. [`refactoring-patterns-abc.md`](file:///home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/references/refactoring-patterns-abc.md)<br>15. [`severity-matrix-and-triage.md`](file:///home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/references/severity-matrix-and-triage.md) *(4)* | `use a audit-and-refactoring-pipeline`<br>`auditar projeto legado`<br>`refatorar código legado` |

---

## 3. Skills Especialistas e de Apoio Integradas

| Skill | Tipo | Propósito Operacional | Componentes e Referências Modulares |
| :--- | :--- | :--- | :--- |
| [**`quarto-expert`**](file:///home/tales/.gemini/config/skills/quarto-expert/SKILL.md) | Especialista (Arquétipo A) | Governa a arquitetura Quarto CLI v1.9+, autoria técnica oficial (Posit/Quarto Authoring), opções `#|`/`%%|`/`//|`, compilação Typst/LaTeX/HTML/RevealJS, ABNT NBR 14724:2024, `_brand.yml`, acessibilidade `fig-alt`, manuscritos MECA + Binder e migração de R Markdown/Bookdown/Jupyter. | **26 Guias Modulares em `references/`:**<br>• *Normas:* [`abnt-thesis-guide.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/abnt-thesis-guide.md), [`typst-and-templates.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/typst-and-templates.md)<br>• *Sintaxe & Células:* [`code-cells.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/code-cells.md), [`cross-references.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/cross-references.md), [`callouts.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/callouts.md), [`figures.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/figures.md), [`tables.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/tables.md), [`diagrams.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/diagrams.md), [`citations.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/citations.md), [`divs-and-spans.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/divs-and-spans.md), [`layout.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/layout.md), [`shortcodes.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/shortcodes.md), [`conditional-content.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/conditional-content.md)<br>• *Configuração & Identidade:* [`yaml-front-matter.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/yaml-front-matter.md), [`brand-yml.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/brand-yml.md), [`alt-text.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/alt-text.md), [`engines.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/engines.md), [`extensions.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/extensions.md), [`markdown-linting.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/markdown-linting.md)<br>• *Migrações Legadas:* [`conversion-rmarkdown.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/conversion-rmarkdown.md), [`conversion-jupyter.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/conversion-jupyter.md), [`conversion-bookdown.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/conversion-bookdown.md), [`conversion-xaringan.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/conversion-xaringan.md), [`conversion-distill.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/conversion-distill.md), [`conversion-blogdown.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/conversion-blogdown.md), [`rmd-to-quarto-migration.md`](file:///home/tales/.gemini/config/skills/quarto-expert/references/rmd-to-quarto-migration.md)<br><br>**Scripts & Hooks:**<br>• `init_quarto_project.sh` (scaffold)<br>• `validate_skill.sh` (validação rápida)<br>• `validate_skill_deep.sh` (render headless)<br>• `verify_skill.sh` (auditoria 6 etapas)<br>• `install_hooks.sh` / `pre-commit`<br>• `backup_examples.sh`<br><br>**Exemplos Prontos:**<br>• `minimal-report/`<br>• `abnt-thesis-starter/`<br>• `manuscript-binder/` |
| [**`humanizer`**](file:///home/tales/.gemini/config/skills/humanizer/SKILL.md) | Apoio Editorial | Autoridade de micro-estilo técnico anti-IA, eliminação de fórmulas artificiais e variação métrica de ritmo (*burstiness*). Invocada pelas pipelines nas etapas de escrita e commit. | Playbooks internos de limpeza lexical, proibição de clichês de IA e controle de cadência sintática (frases curtas intercaladas com períodos compostos). |
| [**`skill-loader`**](file:///home/tales/.gemini/config/skills/skill-loader/SKILL.md) | Apoio de Infraestrutura | Protocolo de carregamento sob demanda para a biblioteca fria (Cold Storage com 2.676 skills), mantendo o orçamento de prompt permanente preservado. | Mecanismo de busca e leitura pontual via `view_file` em `/home/tales/.gemini/config/skills-library/`. |

---

## 4. Os 3 Arquétipos de Projeto (A, B e C)

As 5 Meta-Skills operam de forma polimórfica, ajustando seus critérios de parada, ferramentas e artefatos conforme o arquétipo técnico do repositório:

| Dimensão | Arquétipo A (Data Science, Analytics & Quarto) | Arquétipo B (Software Engineering, Web & APIs) | Arquétipo C (CLI, Automação & DevOps) |
| :--- | :--- | :--- | :--- |
| **Metodologia Base** | CRISP-ML(Q) + Data Storytelling (Ask, Prepare, Process, Construct, Share, Act) | Domain-Driven Design (DDD), Clean Architecture e TDD estrito | Unix Philosophy, Automação Minimalista e 12-Factor CLI |
| **Stack Principal** | Python via `uv`, Quarto CLI (`/opt/quarto/bin/quarto`), Polars, Seaborn/Matplotlib (300 DPI), Great Tables | Python (`uv`, FastAPI, Pydantic v2) ou TypeScript/Node (`pnpm`, Vite/Next), SQLAlchemy/Prisma | Python (`uv`, Typer, Rich), Bash (`bash -n`, ShellCheck), `just`, `pre-commit` |
| **Garantia de Qualidade** | `quarto-quality-checklist.md`, `quarto-expert`, `uv run pytest`, `uv run ruff check .` | Pytest com fixtures/mocks (`pytest-skill`), contratos OpenAPI/Pydantic, testes de integração | Testes de flags/saída CLI, testes idempotentes, validação de lint e formatação |
| **Artefato Final** | Relatório `.qmd` compilado em HTML/Typst/PDF, MECA bundle ou website em GitHub Pages | API REST documentada, microsserviço containerizado ou biblioteca versionada | Executável CLI empacotado, script testado ou GitHub Action com SemVer |
| **Governança de Build** | `_freeze/` mantido no Git quando `freeze: auto/true`; artefatos temporários (`*_files/`, `.quarto/`, `*.html`) ignorados no `.gitignore` | `dist/`, `.venv/`, `.pytest_cache/` rigorosamente ignorados; builds reprodutíveis via lockfiles | Binários e caches locais isolados; validação pré-push sem resíduos no repositório |

---

## 5. Instalação e Uso no Antigravity / Gemini CLI

Para instalar as meta-skills, a skill especialista `quarto-expert` e os utilitários de suporte no ambiente local:

```bash
# 1. Clone o repositório
git clone git@github.com:talesgomes27/antigravity-meta-skills.git

# 2. Copie os pacotes para o diretório de configuração do Antigravity
cp -r antigravity-meta-skills/{pre-code-pipeline,execution-pipeline,writing-pipeline,release-and-ops-pipeline,audit-and-refactoring-pipeline,quarto-expert,humanizer,skill-loader} ~/.gemini/config/skills/

# 3. (Opcional) Instale o hook de pre-commit para validação contínua da quarto-expert
~/.gemini/config/skills/quarto-expert/scripts/install_hooks.sh
```

### Validação de Saúde do Ecossistema

Para auditar o pacote `quarto-expert` e certificar que todos os runtimes, referências e caminhos estão operacionais:

```bash
# Validação rápida (frontmatter, caminhos, sintaxe YAML e bash)
~/.gemini/config/skills/quarto-expert/scripts/validate_skill.sh

# Validação profunda (inclui render headless real de relatório HTML com Quarto)
~/.gemini/config/skills/quarto-expert/scripts/validate_skill_deep.sh

# Verificação pós-execução (auditoria completa em 6 etapas)
~/.gemini/config/skills/quarto-expert/scripts/verify_skill.sh
```

---

## 6. Diretrizes de Governança e Orçamento de Contexto

Para preservar a estabilidade e a capacidade de raciocínio do modelo durante sessões longas, aplicam-se regras estritas de arquitetura:

### 6.1 Orçamento de Tokens (< 20.000 tokens)
- O Antigravity injeta o cabeçalho de todas as skills ativas (`name` + `path` + `description`) no prompt de sistema permanente.
- O teto estabelecido para o bloco de skills é de **20.000 tokens**.
- As descrições no frontmatter de cada `SKILL.md` devem ser mantidas em linha única, concisas e abaixo de **80 tokens** (~320 caracteres).
- Estado atual do bloco de skills do sistema: **~3.250 tokens utilizados em 54 skills ativas** (16,2% do limite), mantendo **~16.750 tokens livres** para contexto dinâmico.
- Métrica dos cabeçalhos das skills do repositório:
  - `quarto-expert`: ~62 tokens
  - `writing-pipeline`: ~66 tokens
  - `audit-and-refactoring-pipeline`: ~71 tokens
  - `pre-code-pipeline`: ~72 tokens
  - `execution-pipeline`: ~72 tokens
  - `release-and-ops-pipeline`: ~72 tokens
  - `humanizer`: ~56 tokens
  - `skill-loader`: ~43 tokens

### 6.2 Carregamento Sob Demanda via `skill-loader` (Cold Storage)
- O ecossistema mantém um acervo de **2.676 skills arquivadas** na biblioteca fria em `/home/tales/.gemini/config/skills-library/` (indexadas em `skills_index.json`).
- Nenhuma skill especialista de nicho deve ser promovida para a pasta ativa `/home/tales/.gemini/config/skills/` sem justificativa prévia de uso contínuo.
- Quando uma tarefa exigir ferramentas especializadas como `complexity-cuts`, `brooks-audit` ou `framework-migration-legacy-modernize`, ative-as via [**`skill-loader`**](file:///home/tales/.gemini/config/skills/skill-loader/SKILL.md):
  ```markdown
  Acesse /home/tales/.gemini/config/skills-library/<nome-da-skill>/SKILL.md sob demanda via view_file.
  ```

### 6.3 Proibição Estrita de Caminhos Relativos
- É expressamente proibido o uso de caminhos relativos (como `../`, `./` ou `references/arquivo.md`) dentro dos arquivos `SKILL.md` ou nos playbooks de referência.
- Todo link documental ou instrução de carregamento deve utilizar caminhos absolutos com esquema de URL compatível:
  `file:///home/tales/.gemini/config/skills/<meta-skill>/references/<arquivo>.md`
- Essa restrição evita falhas de resolução quando o agente executa comandos a partir de diretórios de trabalho distintos do workspace raiz.

### 6.4 Runtimes Canônicos e Governança de Ambiente
- **Git:** `/usr/bin/git`
- **Quarto CLI:** `/opt/quarto/bin/quarto` (versão 1.10+)
- **R / Rscript:** `/usr/bin/R` e `/usr/bin/Rscript`
- **uv:** `/home/tales/.local/bin/uv` (gerenciador de pacotes e virtualenvs padrão)
- **Miniforge / Conda:** `/home/tales/miniforge3/bin/conda` (exclusivo para dependências nativas C/C++/CUDA ou drivers sem wheels confiáveis)
- **QUARTO_PYTHON:** Para compilação de relatórios com células executáveis Python, o Quarto exige interpretador com `jupyter`, `nbformat` e `matplotlib`. Configure via `export QUARTO_PYTHON=/home/tales/miniforge3/envs/science/bin/python` ou utilize `uv run --with jupyter,matplotlib quarto render`.
