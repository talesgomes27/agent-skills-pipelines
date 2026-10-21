---
name: audit-and-refactoring-pipeline
description: "Conduz auditoria multi-camadas e refatoração segura em 5 Gates para projetos legados/Brownfield (Arquétipos A, B e C), com handoff para execution ou release."
---

# Skill: audit-and-refactoring-pipeline

Este playbook governa a atuação em **projetos preexistentes, legados ou parcialmente implementados (*Brownfield*)**. Enquanto projetos novos seguem a linha `pre-code` ➔ `execution` ➔ `release-and-ops`, esta meta-skill opera como uma **esteira de entrada e saneamento**: realiza o reconhecimento reverso do repositório, audita código, testes, dados, gráficos e documentação de forma não-destrutiva, constrói testes de caracterização (*Golden Master*), aplica refatorações cirúrgicas polimórficas e re-injeta o projeto estabilizado na esteira principal.

---

## 0. Contrato de Enquadramento, Guardrails e Coordenação

### 0.1 Detecção e Enquadramento de Arquétipo (`docs/00_archetype.md`)
1. Verifique se `docs/00_archetype.md` já existe no projeto.
2. **Geração Retroativa (Padrão Brownfield):** Se não existir, execute no **Gate 1** a heurística determinística de reconhecimento:
   - Presença de `_quarto.yml`, `.qmd`, `.ipynb` ou pipelines de dados/ML ➔ **Arquétipo A (Data Science & Quarto)**.
   - Presença de rotas de API, frameworks web, `Dockerfile` ou componentes de UI ➔ **Arquétipo B (Software, Web & APIs)**.
   - Presença de scripts de terminal, parsers `argparse`/`click`/`typer` e automações ➔ **Arquétipo C (CLI & Scripts)**.
3. Grave `docs/00_archetype.md` com `gerado_por: audit-and-refactoring-pipeline` e confirme com o usuário no final do Gate 1. Em caso de dúvida, **PARE e pergunte**.

### 0.2 Regra de Ouro Não-Destrutiva (Gates 1 a 3)
- **Gates 1 e 2 (Somente-Leitura para Código):** É estritamente proibido alterar código de negócio, notebooks ou relatórios durante o reconhecimento e diagnóstico. Apenas `docs/00_archetype.md`, `task.md` e `docs/audit-report.md` podem ser criados/atualizados.
- **Gate 3 (Apenas Testes e Plano):** Apenas arquivos de teste em `tests/characterization/` e o plano em `task.md` / `docs/refactoring-plan.md` podem ser criados.
- **Gate 4 (Protocolo *Verify-Revert-Stop*):** Modificações no código ocorrem apenas após aprovação humana do Gate 3, em fatias atômicas verificadas por `pytest`. Se uma fatia quebrar testes de caracterização de forma não intencional, reverta imediatamente antes de prosseguir.

### 0.3 Coordenação com `writing-pipeline` e `humanizer`
- **No Gate 2 (Diagnóstico):** Invoque `writing-pipeline` (`/home/tales/.gemini/config/skills/writing-pipeline/SKILL.md`) no **Modo 2 (Revisão Editorial Não-Destrutiva)** para produzir a tabela estruturada de achados (`ID | Linha / Arquivo | Severidade | Diagnóstico Original | Sugestão de Refatoração | Racional Técnico`).
- **Nos Gates 4 e 5 (Reescrita e Sumário):** Invoque `writing-pipeline` no **Modo 1 (Geração Direta)** em coordenação com `humanizer`.

### 0.4 Orçamento e Carregamento Sob Demanda (Cold Storage)
Para preservar o orçamento global de tokens, carregue as skills de Cold Storage (`/home/tales/.gemini/config/skills-library/<skill>/SKILL.md`) via `skill-loader` apenas no Gate em que forem exigidas:
- Gate 1: `brooks-audit`, `production-code-audit`, `framework-migration-legacy-modernize`
- Gate 2: `clean-code-guard`, `logic-lens`, `security-audit`, `code-audit`, `weather-data-reproducibility`
- Gate 3: `code-refactoring-tech-debt`, `brooks-debt`
- Gate 4: `complexity-cuts`, `orchestrate-batch-refactor`, `repo-native-refactor`, `seaborn`

---

## Fluxo dos 5 Gates de Auditoria e Refatoração (Brownfield)

```text
[Repositório Existente / Legado (Brownfield)]
                      │
                      ▼
Gate 1 (Reconhecimento & docs/00_archetype.md) ──→ [Aprovação de Escopo]
                      │
                      ▼
Gate 2 (Diagnóstico 4 Camadas — Tabela Modo 2) ──→ [Aprovação de docs/audit-report.md]
                      │
                      ▼
Gate 3 (Testes de Caracterização & Plano)      ──→ [Aprovação do Plano de Fatias]
                      │
                      ▼
Gate 4 (Refatoração Cirúrgica Polimórfica A/B/C)─→ [Validação Verify-Revert-Stop]
                      │
                      ▼
Gate 5 (Zero Regressão, Docs Sync & Handoff)   ──→ [Handoff: execution ou release-and-ops]
```

---

## 1. Gate 1: Reconhecimento, Engenharia Reversa & Enquadramento

- **Objetivo**: Compreender a arquitetura real do repositório legado sem modificar o código funcional, gerando `docs/00_archetype.md` e `task.md`.
- **Skills Mobilizadas**:
  - `planning-with-files` *(Ativa)* (Inicialização do `task.md` e estrutura `docs/`)
  - `senior-architect`, `architecture-patterns` & `domain-driven-design` *(Ativas)*
  - `brooks-audit`, `production-code-audit` & `framework-migration-legacy-modernize` *(Cold Storage — sob demanda)*
- **Operação**:
  1. Inspecionar a árvore de diretórios, `README.md`, arquivos de manifesto (`pyproject.toml`, `package.json`, `_quarto.yml`) e histórico Git recente.
  2. Executar a heurística de detecção de arquétipo (`A`, `B` ou `C`) e gravar `docs/00_archetype.md`.
  3. Verificar o estado inicial de execução da suíte de testes existente (se houver) e inicializar o `task.md`.
  4. Verificar a governança de dependências e ambiente Python: constatar se o projeto já adota o padrão obrigatório `uv + pyproject.toml + Ruff + pytest` ou se requer migração a partir de `requirements.txt` legado.
- **Artefatos de Saída**: `docs/00_archetype.md`, `task.md` e sumário de reconhecimento arquitetural.
- **Critério de Parada**: Confirmação humana do arquétipo detectado e do escopo da auditoria (marcar Gate 1 como `[x]` no `task.md`).

---

## 2. Gate 2: Diagnóstico Multi-Camadas Não-Destrutivo

- **Objetivo**: Mapear falhas de código, testes, dados/visual e documentação, consolidando tudo em `docs/audit-report.md` no formato tabular do Modo 2.
- **Referências Obrigatórias**:
  - `/home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/references/severity-matrix-and-triage.md`
  - Para Arquétipo A: `/home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/references/archetype-a-analytics-audit.md` e `/home/tales/.gemini/config/skills/pre-code-pipeline/references/quarto-quality-checklist.md`.
- **Operação nas 4 Camadas**:
  1. **Camada de Código & Segurança:** `clean-code`, `code-reviewer`, `code-review-excellence`, `simplify-code`, `systematic-debugging` *(Ativas)*, `ponytail-audit` / `ponytail-review` *(Ativas via plugin `ponytail`)*, mais `clean-code-guard`, `logic-lens` e `security-audit` *(Cold Storage)*.
  2. **Camada de Testes:** `test-guard` e `pytest-skill` *(Ativas)*. Audita lacunas de cobertura e testes frágeis.
  3. **Camada Analítica, Científica & Visual (Arquétipo A):** `data-quality-frameworks`, `data-scientist`, `analytics`, `matplotlib`, `plotly`, `quarto-expert` (`/home/tales/.gemini/config/skills/quarto-expert/SKILL.md` e a sua referência `rmd-to-quarto-migration.md`) *(Ativas)*, `ml-best-practices` e `notebook-guidance` *(Ativas via plugin `data-agent-kit-plugin`)*, mais `weather-data-reproducibility` *(Cold Storage)*. Avalia a conformidade com as **6 Seções Canônicas do CRISP-ML(Q) + Data Storytelling** (ou IMRAD se acadêmico), auditando *data leakage*, sementes (`seed`), ausência de Baseline comparativo na Seção 4, falta de explicabilidade (SHAP) na Seção 5, quebra de rastreabilidade entre hipóteses (Seção 1) e ações (Seção 6), importância `gain` vs. `split`, alinhamento de subfiguras e DPI, além de opções legadas de R Markdown, exceções de fusão da chave `format:` e problemas de compilação PDF/Typst.
  4. **Camada Documental & Editorial:** `docs-guard` *(Ativa)* e `writing-pipeline` *(Ativa — Modo 2)*. Confronta documentação com o código real e revisa estilo/citações.
- **Artefato de Saída**: `docs/audit-report.md` estruturado na tabela canônica (`ID | Linha / Arquivo | Severidade | Diagnóstico Original | Sugestão de Refatoração | Racional Técnico`) e classificado em `Crítico (P0)`, `Alto (P1)`, `Médio (P2)` e `Baixo (P3)`.
- **Critério de Parada**: Aprovação humana dos achados em `docs/audit-report.md` (marcar Gate 2 como `[x]` no `task.md`).

---

## 3. Gate 3: Rede de Segurança (Testes de Caracterização) & Plano de Refatoração

- **Objetivo**: Congelar o comportamento atual dos módulos que serão alterados via *Golden Master / Pinning Tests* e planejar a ordem exata das fatias de refatoração.
- **Skills e Referências Mobilizadas**:
  - Leitura obrigatória de `/home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/references/characterization-tests.md`.
  - `pytest-skill`, `tdd-workflow`, `test-guard` *(Ativas)*
  - `code-refactoring-tech-debt` & `brooks-debt` *(Cold Storage)*
  - `writing-pipeline` *(Modo 1)*
- **Operação**:
  1. Implementar testes de caracterização em `tests/characterization/` capturando saídas reais e invariantes dos módulos críticos sem cobertura.
  2. Confirmar que 100% dos testes de caracterização passam no estado atual do código.
  3. Estruturar o plano de execução em `docs/refactoring-plan.md` (e atualizar `task.md`) em fatias incrementais (*Batches*) ordenadas por severidade (`Crítico` ➔ `Alto` ➔ `Médio` ➔ `Baixo`).
- **Artefatos de Saída**: Suíte `tests/characterization/` verde e `docs/refactoring-plan.md`.
- **Critério de Parada**: Aprovação humana do plano de refatoração antes de tocar no código funcional (marcar Gate 3 como `[x]` no `task.md`).

---

## 4. Gate 4: Execução da Refatoração Cirúrgica Polimórfica (A / B / C)

- **Objetivo**: Aplicar as fatias de refatoração aprovadas, mantendo a suíte de caracterização 100% verde a cada passo (*Verify-Revert-Stop*).
- **Referência Obrigatória**:
  - `/home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/references/refactoring-patterns-abc.md`
- **Operação e Skills por Arquétipo**:
  - **Arquétipo A (Data Science, Analytics & Quarto)**:
    - *Skills:* `code-refactoring-refactor-clean`, `polars`, `data-scientist`, `matplotlib`, `plotly`, `quarto-expert` (`/home/tales/.gemini/config/skills/quarto-expert/SKILL.md`), `writing-pipeline` (Modo 1), `humanizer` *(Ativas)*, `seaborn` *(Cold Storage)*.
    - Eliminar *data leakage*, fixar `seed` global, extrair funções de notebooks para `src/`, vetorizar rotinas lentas com Polars/NumPy, reestruturar o relatório `.qmd` nas 6 seções canônicas do CRISP-ML(Q) + Data Storytelling caso esteja fora do padrão e refatorar gráficos e documentos conforme `/home/tales/.gemini/config/skills/pre-code-pipeline/references/quarto-quality-checklist.md` e `quarto-expert` (300 DPI, `set_box_aspect(1)`, `sns.despine()`, `lang: pt-BR`, zero numeração manual duplicada, migração de opções de chunk `#|` e compilação Typst/PDF). Conduzir validação contínua da fatia via `uv run pytest`, `uv run ruff check .` e `quarto render`.
  - **Arquétipo B (Software, Web & APIs)**:
    - *Skills:* `code-refactoring-refactor-clean`, `clean-code`, `simplify-code`, `architecture-patterns`, `writing-pipeline` (Modo 1) *(Ativas)*, `complexity-cuts`, `orchestrate-batch-refactor`, `repo-native-refactor` *(Cold Storage)*.
    - Desacoplar controladores/rotas extraindo serviços e repositórios, reduzir complexidade ciclomática, otimizar queries de banco e atualizar contratos de API.
  - **Arquétipo C (CLI & Scripts)**:
    - *Skills:* `code-refactoring-refactor-clean`, `simplify-code` *(Ativas)*, `ponytail-audit` *(Plugin)*, `complexity-cuts`, `repo-native-refactor` *(Cold Storage)*, `writing-pipeline` (Modo 1).
    - Modularizar scripts monolíticos em subcomandos, substituir dependências supérfluas pela biblioteca padrão e padronizar `stdout`/`stderr` e exit codes POSIX.
- **Artefatos de Saída**: Código, testes, figuras e documentos refatorados com commits/fatias verificados.
- **Critério de Parada**: Conclusão validada de todas as fatias planejados (marcar Gate 4 como `[x]` no `task.md`).

---

## 5. Gate 5: Verificação de Regressão, Sincronização Documental & Handoff

- **Objetivo**: Auditar a ausência total de regressões, sincronizar documentação/ADRs e encaminhar o projeto para a pipeline de destino.
- **Skills Mobilizadas**:
  - `test-guard`, `docs-guard`, `architecture-decision-records`, `writing-pipeline` (Modo 1) *(Ativas)*
  - `clean-code-guard` *(Cold Storage)*
- **Operação**:
  1. Executar a suíte completa de testes (`pytest`) e compilação (`quarto render` no Arquétipo A) confirmando exit code `0`.
  2. Rodar `docs-guard` para atestar que docstrings, `README.md`, relatórios e ADRs refletem o código pós-refatoração.
  3. Registrar o sumário de encerramento dos achados em `docs/audit-report.md` e marcar todos os Gates como `[x] Aprovado` no `task.md`.
- **Protocolo de Handoff Pós-Gate 5**:
  Conforme o objetivo do usuário após o saneamento:
  - **Rota 1 (Pronto para Release e Publicação):** Ativar **`release-and-ops-pipeline`** (`/home/tales/.gemini/config/skills/release-and-ops-pipeline/SKILL.md`) no **Gate 1** para saneamento pré-push, SemVer/`CHANGELOG.md`, CI/CD e publicação no GitHub Pages/Cloud.
  - **Rota 2 (Desenvolvimento de Novas Features sobre a Base Saneada):** Ativar **`pre-code-pipeline`** (`/home/tales/.gemini/config/skills/pre-code-pipeline/SKILL.md`) ou **`execution-pipeline`** (`/home/tales/.gemini/config/skills/execution-pipeline/SKILL.md`), que herdarão automaticamente o `docs/00_archetype.md` já consolidado.

---

## 2.1 Integração `graphify` (GraphRAG Estático — OPCIONAL)

Referência completa: `/home/tales/.gemini/config/skills/quarto-expert/references/graphify-integration.md`

**Requer `graphify >= 0.9.93`.** Detecte antes de usar:

```bash
if ! command -v graphify > /dev/null 2>&1; then
    echo "AVISO: graphify indisponivel. Fallback: read_file/grep."
    USE_GRAPHIFY=0
else
    USE_GRAPHIFY=1
fi
```

### Gate 1 (Reconhecimento) — com `graphify`

Se `USE_GRAPHIFY=1`, antes de `read_file` em massa:

```bash
graphify .                          # construcao inicial (uma vez por projeto)
cat graphify-out/GRAPH_REPORT.md    # comunidades, god nodes, ciclos
```

Preencher `docs/00_archetype.md` com contagem de módulos, acoplamento e
comunidades detectadas.

Se `USE_GRAPHIFY=0`, manter `read_file` sobre arquivos-chave.

### Gate 2 (Diagnóstico) — com `graphify`

Se `USE_GRAPHIFY=1`:

```bash
graphify god-nodes --top 10         # God Nodes direto (candidatos P0/P1)
graphify diagnose multigraph        # arestas orfas, colapsos multi-endpoint
```

Não parsear `GRAPH_REPORT.md` manualmente — `god-nodes` retorna direto.

Se `USE_GRAPHIFY=0`, análise heurística manual.

### Gate 4 (Fatiamento Seguro) — com `graphify`

Se `USE_GRAPHIFY=1`, antes de alterar qualquer módulo:

```bash
graphify affected "ModuloX" --depth 2   # quem depende de X (raio de impacto)
graphify path "Origem" "Destino"        # caminho entre dois modulos
```

Ordenar testes *Golden Master* dos nós mais dependentes (mais profundos no
grafo) para os mais rasos.

Se `USE_GRAPHIFY=0`, ordem baseada em dependências inferidas por `grep`.

---

## 6. Matriz de Rastreabilidade Arquétipo × Gate × Skill

---

| Arquétipo | Gate 1 (Reconhecimento) | Gate 2 (Diagnóstico Modo 2) | Gate 3 (Safety Net & Plano) | Gate 4 (Refatoração Cirúrgica) | Gate 5 (Verificação & Handoff) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A: Data Science & Quarto** | `planning-with-files`<br>`senior-architect`<br>`production-code-audit`*<br>*(00_archetype.md)* | `archetype-a-analytics-audit.md`<br>`quarto-expert`<br>`severity-matrix-and-triage.md`<br>`ml-best-practices`<br>`notebook-guidance`<br>`writing-pipeline` (Modo 2)<br>*(audit-report.md)* | `characterization-tests.md`<br>`pytest-skill`<br>`test-guard`<br>`code-refactoring-tech-debt`*<br>*(refactoring-plan.md)* | `refactoring-patterns-abc.md`<br>`code-refactoring-refactor-clean`<br>`polars` / `quarto-expert`<br>`quarto-quality-checklist`<br>`writing-pipeline` (Modo 1) | `docs-guard`<br>`test-guard`<br>`clean-code-guard`*<br>`quarto-expert`<br>`quarto render`<br>*(Handoff Execution/Release)* |
| **B: Software, APIs & Web** | `planning-with-files`<br>`senior-architect`<br>`architecture-patterns`<br>`domain-driven-design`<br>`brooks-audit`* | `severity-matrix-and-triage.md`<br>`clean-code` / `code-reviewer`<br>`clean-code-guard`*<br>`security-audit`* / `docs-guard`<br>`writing-pipeline` (Modo 2) | `characterization-tests.md`<br>`pytest-skill`<br>`test-guard`<br>`brooks-debt`*<br>*(refactoring-plan.md)* | `refactoring-patterns-abc.md`<br>`code-refactoring-refactor-clean`<br>`simplify-code`<br>`orchestrate-batch-refactor`*<br>`writing-pipeline` (Modo 1) | `clean-code-guard`*<br>`test-guard` / `docs-guard`<br>`architecture-decision-records`<br>*(Handoff Execution/Release)* |
| **C: CLI & Scripts** | `planning-with-files`<br>`senior-architect`<br>`production-code-audit`*<br>*(00_archetype.md)* | `severity-matrix-and-triage.md`<br>`ponytail-audit`<br>`simplify-code`<br>`clean-code-guard`*<br>`writing-pipeline` (Modo 2) | `characterization-tests.md`<br>`pytest-skill`<br>`test-guard`<br>`code-refactoring-tech-debt`*<br>*(refactoring-plan.md)* | `refactoring-patterns-abc.md`<br>`simplify-code`<br>`complexity-cuts`*<br>`repo-native-refactor`*<br>`writing-pipeline` (Modo 1) | `docs-guard`<br>`test-guard`<br>`clean-code-guard`*<br>*(Handoff Execution/Release)* |

*(Itens com `*` residem em `/home/tales/.gemini/config/skills-library/` e são carregados sob demanda via `skill-loader`).*
