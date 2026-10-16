---
name: pre-code-pipeline
description: "Orquestra o planejamento pré-código em 5 Gates sequenciais para Engenharia de Software (DDD, Clean Arch, TDD) e Ciência de Dados (CRISP-ML(Q) + Data Storytelling com Python/R e Quarto)."
---

# Pre-Code Pipeline (v2.1): Orquestrador de Concepção e Planejamento

Este playbook define o fluxo obrigatório de preparação técnica antes da escrita de qualquer código definitivo de aplicação ou modelagem. O objetivo é eliminar suposições, congelar contratos e estruturar o projeto em 5 portões (*Gates*) sequenciais.

---

## Regras Globais de Execução (Guardrails)

1. **Proibição Estrita de Código Precoce (com Exceção de Profiling Leitura)**:
   - Durante os Gates 1 a 5, é proibido criar arquivos de regras de negócio, rotas, pipelines definitivos de transformação, treinamento de modelos ou componentes de tela.
   - **Exceção Permitida no Gate 1:** É permitido executar comandos de terminal ou *one-liners* efêmeros e estritamente *read-only* para ler documentação local (`README.md`) e inspecionar schemas, volumetria, tipos de dados, valores nulos e chaves de *join* nas bases existentes, sem alterar os arquivos brutos.
   - No repositório, apenas arquivos de especificação (`docs/*.md`), diagramas, contratos de interface/schema, configurações base de tooling e listas de tarefas (`task.md`) são permitidos até o fim do Gate 5.

2. **Checkpoints Humanos Obrigatórios (Critérios de Parada)**:
   - Ao concluir cada Gate, apresente um resumo objetivo dos artefatos produzidos.
   - Aplique o padrão da skill `ask-questions-if-underspecified`: aponte dúvidas residuais, suposições assumidas e solicite aprovação formal do usuário.
   - **Não avance para o Gate seguinte sem autorização explícita.**

3. **Roteamento Inteligente por Arquétipo de Projeto (Prevenção de Context Bloat)**:
   - Ao iniciar o pipeline, classifique o projeto em um dos 3 arquétipos abaixo e **carregue apenas as skills pertinentes àquele arquétipo** em cada Gate:
     - **Arquétipo A — Data Science, Analytics & ML (Python/R/Quarto):** Alinha os 5 Gates à **Metodologia Híbrida CRISP-ML(Q) + Data Storytelling** (1. *Business Understanding & Hypotheses / Ask*; 2. *Data Understanding & Contracts / Prepare*; 3. *Data Prep, EDA & Feature Engineering / Process*; 4. *Statistical & ML Modeling / Construct*; 5. *Evaluation, Diagnostics & Explainability / Share*; 6. *Deployment & Executive Action / Act*), ou **IMRAD** para relatórios estritamente acadêmicos. Consulta obrigatoriamente `/home/tales/.gemini/config/skills/pre-code-pipeline/references/quarto-quality-checklist.md`. Dispensa DDD complexo, OpenAPI e SaaS MVP.
     - **Arquétipo B — Engenharia de Software, Web, APIs & SaaS:** Mobiliza o conjunto completo de arquitetura de sistemas (DDD, Clean Architecture, DB Design, API Contracts, SaaS MVP e Webapp Testing).
     - **Arquétipo C — Automação, CLI & Scripts Técnicos:** Fluxo enxuto focado em contratos de I/O, requisitos diretos, Scaffolding e TDD.

4. **Memória Persistente e Atualização Contínua (`planning-with-files`)**:
   - Acione a skill `planning-with-files` logo na abertura do pipeline (no Gate 1, ou no Gate 2 caso o Gate 1 seja pulado) para criar o diretório `docs/` e inicializar o arquivo `task.md`, rastreando o status (`[ ] Pendente`, `[/] Em andamento`, `[x] Aprovado`) dos 5 Gates.
   - **Regra de Atualização:** Atualize o `task.md` obrigatoriamente na abertura e após a aprovação humana de **cada Gate**.

5. **Carregamento Sob Demanda (Cold Storage)**:
   - Skills arquivadas na biblioteca fria devem ser consultadas sob demanda em `/home/tales/.gemini/config/skills-library/<skill>/SKILL.md` via `skill-loader`.
   - Consulte `/home/tales/.gemini/config/skills-library/skills_index.json` quando precisar localizar skills específicas de domínio.

---

## Os 5 Gates Operacionais

```text
Gate 1 (Dados/Prepare) ──→ Gate 2 (PRD/Ask) ──→ Gate 3 (Arquitetura) ──→ Gate 4 (Scaffold) ──→ Gate 5 (Plano/TDD) ──→ [Handoff Código]
          │                       │                     │                       │                      │
     [Aprovação]             [Aprovação]           [Aprovação]             [Aprovação]            [Aprovação]
```

---

### Gate 1: Contexto Inicial, Descoberta e Contratos de Dados (*Data Understanding & Contracts / Prepare*)
*Opcional apenas quando o projeto for 100% Greenfield e não consumir fontes de dados preexistentes.*

- **Objetivo**: Ler a documentação prévia (`README.md`), inicializar o `task.md`, inspecionar fontes de dados, catalogar esquemas, verificar riscos de *data leakage* e formalizar contratos de dados.
- **Skills Mobilizadas**:
  - `planning-with-files` (Inicialização de `task.md` e estrutura `docs/`)
  - `data-scientist` (Inspeção estatística, janelas temporais e viabilidade exploratória)
  - `schema-mapping` (Matriz de mapeamento origem-destino e chaves de *join*)
  - `data-autocleaning` (Diagnóstico de anomalias, missings, outliers e regras de saneamento)
  - `data-quality-frameworks` (Contratos de dados e regras de validação prévia)
  - `discovering-gcp-data-assets` *(Condicional: apenas se o projeto usar GCP/BigQuery/Spanner)*
- **Artefato de Saída**: `docs/00_archetype.md` (com frontmatter YAML definindo archetype: A|B|C, stack, project_name, gerado_por e data) e `docs/01-data-discovery-and-contracts.md`
  - Síntese do contexto inicial extraído do `README.md` (*Business Understanding / Ask* preliminar).
  - Catálogo de tabelas/arquivos de entrada com tipos, janelas temporais e volumetria (*Data Understanding & Contracts / Prepare*).
  - Mapeamento de relacionamentos (*join keys*), identificação da variável *target* e análise de risco de *data leakage*.
  - Contratos de qualidade (*Data Contracts*) que os dados brutos devem cumprir antes da etapa *Data Prep & Feature Engineering / Process*.
- **Critério de Parada**: Confirmação pelo usuário de que o diagnóstico das fontes e os contratos de dados estão corretos (atualizar Gate 1 como `[x]` no `task.md`).

---

### Gate 2: Ideação, Escopo, Hipóteses e Especificação (*Business Understanding, Hypotheses & Specs / Ask & Plan*)

- **Objetivo**: Lapidar a proposta do projeto/pesquisa, formular hipóteses/requisitos, estipular métricas de avaliação e delimitar explicitamente o que **não** será feito.
- **Skills Mobilizadas**:
  - `planning-with-files` (Inicialização de `task.md` e `docs/` caso o Gate 1 tenha sido pulado em projetos Greenfield, ou atualização de status)
  - `brainstorming` (Exploração de hipóteses e alternativas conceituais)
  - `data-storytelling` (Narrativa do problema, público-alvo e metas de impacto)
  - `idea-os` *(Cold Storage)* (Perguntas críticas e estruturação de PRD)
  - `spec-driven-development` *(Cold Storage)* (Especificação formal sem suposições ocultas)
  - `ask-questions-if-underspecified` *(Cold Storage)* (Perguntas diretas para eliminar ambiguidades)
  - `saas-mvp-launcher` *(Cold Storage — Condicional: apenas para Arquétipo B / Produtos SaaS)*
  - `writing-pipeline` (Redação técnica do PRD e especificações conforme o arquétipo em docs/00_archetype.md)
- **Artefato de Saída**: `docs/00_archetype.md` e `docs/02-PRD-and-specs.md`
  - Gravação obrigatória de `docs/00_archetype.md` com frontmatter YAML contendo os metadados de herança:
    ```yaml
    ---
    archetype: A # A|B|C
    stack: <string>
    project_name: <string>
    gerado_por: pre-code-pipeline
    data: <ISO8601>
    ---
    ```
  - `docs/02-PRD-and-specs.md`:
    - Definição do problema central, questões norteadoras e hipóteses de negócio/pesquisa.
    - Requisitos funcionais (RF) e não-funcionais (RNF).
    - **Para Arquétipo A (Data Science):** Justificativa matemática da métrica primária de avaliação (ex: RMSLE vs. RMSE vs. MAE), estratégia de validação (temporal vs. K-Fold) e matriz 1:1 ligando cada pergunta/hipótese de *Business Understanding / Ask* a uma visualização e diagnóstico planejados em *Evaluation & Storytelling / Share*.
    - Seção obrigatória de **Non-Goals** (escopo negativo).
- **Critério de Parada**: Aprovação explícita do PRD/Especificação, gravação validada de `docs/00_archetype.md` e encerramento das dúvidas conceituais (atualizar Gate 2 como `[x]` no `task.md`).

---

### Gate 3: Arquitetura do Pipeline: Data Prep, Modeling, Evaluation & Storytelling (*Process, Construct & Share*)

- **Objetivo**: Definir padrões arquiteturais, limites modulares, modelo de dados ou arquitetura do pipeline analítico e plano visual.
- **Skills Mobilizadas (Selecione conforme o Arquétipo)**:
  - *Comuns:* `planning-with-files`, `software-architecture`, `architecture-decision-records`, `writing-pipeline` (Governança de redação de docs/03 e ADRs), `mermaid-expert` *(Cold Storage)*.
  - *Arquétipo A (Data Science/Quarto):* `data-scientist`, `data-storytelling` + leitura obrigatória de `/home/tales/.gemini/config/skills/pre-code-pipeline/references/quarto-quality-checklist.md`.
  - *Arquétipo B (Software/Web/API):* `domain-driven-design`, `senior-architect`, `architecture-patterns`, `database-architect`, `database-design`, `architect-review`, `api-design-principles` *(Cold Storage)*, `c4-architecture-c4-architecture` *(Cold Storage)*.
- **Artefato de Saída**: `docs/03-architecture-and-schema.md` e pasta `docs/adr/`
  - Diagrama de arquitetura ou fluxo do pipeline de dados em Mermaid/C4.
  - *Para Arquétipo A:* Arquitetura das etapas **Data Prep, EDA & Feature Engineering / Process** (limpeza e transformações), **Statistical & ML Modeling / Construct** (modelos candidatos e baselines), **Evaluation, Diagnostics & Explainability / Share** (storyboard de figuras obedecendo ao `quarto-quality-checklist.md`) e **Deployment & Executive Action / Act** (deploy/publicação).
  - *Para Arquétipo B:* Esquema de banco de dados (DDL/ERD) e contratos de API (OpenAPI/Pydantic/TS).
  - Registros de decisão arquitetural (`docs/adr/0001-*.md`).
- **Critério de Parada**: Aprovação da topologia técnica, contratos e storyboard analítico (atualizar Gate 3 como `[x]` no `task.md`).

---

### Gate 4: Scaffolding, Estrutura de Pastas e Convenções

- **Objetivo**: Inicializar a árvore física do repositório, configurações de ambiente, templates de relatório e regras de agentes.
- **Skills Mobilizadas**:
  - `planning-with-files` (Atualização do `task.md`)
  - `agy-customizations` (Ajustes locais do ambiente Antigravity/Gemini)
  - `python-development-python-scaffold` *(Para projetos Python: `uv`, `pyproject.toml`, `ruff`, `pytest`)*
  - `javascript-typescript-typescript-scaffold` *(Para projetos JS/TS: `pnpm`, Vite/Next/Astro, `eslint`, `typescript`)*
  - `agents-generator` *(Cold Storage)* (Geração de `AGENTS.md` customizado para o domínio)
- **Artefato de Saída**:
  - Documento `docs/04-scaffolding-and-conventions.md` registrando a árvore de diretórios e padrões adotados.
  - Estrutura física de pastas instanciada e arquivos de configuração (`pyproject.toml`/`package.json`).
  - *Para Arquétipo A (Quarto):* Inicialização de `_quarto.yml` (com `lang: pt-BR`, `execute: freeze: auto`, tema customizado e regras de numeração) e esqueleto `.qmd` seguindo `/home/tales/.gemini/config/skills/pre-code-pipeline/references/quarto-quality-checklist.md`.
  - Guia de convenções e guardrails do repositório em `AGENTS.md`.
- **Critério de Parada**: Repositório inicializado, configurações validadas e `docs/04-scaffolding-and-conventions.md` + `AGENTS.md` aprovados (atualizar Gate 4 como `[x]` no `task.md`).

---

### Gate 5: Plano de Implementação, Validação & Action (*Deployment / Act*)

- **Objetivo**: Fragmentar a implementação em passos atômicos ordenados por dependência, com verificação automatizada definida antes do código.
- **Skills Mobilizadas**:
  - `planning-with-files` (Atualização do `task.md`)
  - `writing-plans` (Elaboração do plano sequencial com passos verificáveis)
  - `tdd-workflow` (Definição dos ciclos Red-Green-Refactor para código e testes de integridade de dados)
  - `planning-and-task-breakdown` *(Cold Storage)* (Mapeamento do grafo de precedência entre tarefas)
  - `writing-pipeline` (Redação clara e contratual de docs/05-implementation-plan.md)
  - `spec-driven-loop` *(Cold Storage)* (Critérios de aceite estritos por entrega)
  - `webapp-testing` *(Condicional: apenas para projetos com interface web/frontend)*
- **Artefato de Saída**: `docs/05-implementation-plan.md`
  - Grafo de precedência técnica (ordem exata de construção).
  - Checklist atômico de tarefas (referenciando arquivos-alvo exatos, testes e artefatos de saída).
  - Comandos exatos de verificação automatizada (testes unitários, validação de contratos de dados e `quarto render` quando aplicável).
- **Critério de Parada**: Validação final do plano pelo desenvolvedor. **Somente após este aceite o projeto está liberado para escrita de código.**

---

## Handoff para Execução (Pós-Gate 5)

Assim que o usuário aprovar formalmente o **Gate 5**:
1. Marque todos os 5 Gates do ciclo pré-código como `[x] Aprovado` no `task.md` e adicione a lista de tarefas atômicas de implementação.
2. Ative a Meta-Skill **`execution-pipeline`** (`/home/tales/.gemini/config/skills/execution-pipeline/SKILL.md`), que lerá automaticamente `docs/00_archetype.md` e conduzirá os 5 Gates polimórficos de implementação em conjunto com `tdd-workflow` e `writing-pipeline`.
3. Execute o plano descrito em `docs/05-implementation-plan.md` de forma estritamente incremental (uma tarefa atômica por vez), rodando os comandos de verificação automatizada e atualizando o `task.md` a cada passo concluído.

---

## Gatilho de Ativação

Para iniciar um ciclo pré-código em um projeto novo ou existente, declare no prompt:

```text
Ative a skill pre-code-pipeline (Arquétipo [A / B / C]) para o projeto [Nome/Caminho do Projeto].
Inicie pelo Gate [1 ou 2].
```
