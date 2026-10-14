# Ecossistema de Meta-Skills: Engenharia, Dados e Operações

Este documento descreve a governança, topologia e protocolos operacionais das 5 Meta-Skills ativas em `/home/tales/.gemini/config/skills/`.

A arquitetura organiza o ciclo de vida técnico em esteiras polimórficas (adaptadas aos Arquétipos A, B e C), separando fluxos de desenvolvimento novo (*Greenfield*) e modernização de código legado (*Brownfield*).

---

## 1. Topologia do Ciclo de Vida Completo

O ecossistema divide o trabalho em duas portas de entrada principais, com coordenação transversal da esteira editorial e documental:

```text
 ┌────────────────────────────────────────────────────────┐
 │               PROJETOS GREENFIELD (Novos)              │
 └────────────────────────────────────────────────────────┘
                            │
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ 1. pre-code-pipeline (Gates 1 a 5)                     │
 │    PRD, Arquitetura, DB, TDD / 6 Phases Data Science   │
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
```

### Interação entre Esteiras
- **Fluxo Greenfield:** Inicia em `pre-code-pipeline`. Passa pelo afunilamento dos 5 Gates de planejamento até o handoff para `execution-pipeline`. Finalizada a execução, o handoff segue para `release-and-ops-pipeline`.
- **Fluxo Brownfield:** Repositórios existentes entram por `audit-and-refactoring-pipeline`. A esteira cataloga o estado atual sem alterações destrutivas (Gates 1–2), estabelece testes de caracterização (Gate 3) e aplica refatorações cirúrgicas (Gate 4). No Gate 5, o projeto saneado é despachado para publicação (`release-and-ops-pipeline`) ou para adição de novas features (`execution-pipeline`).
- **Atuação Transversal da `writing-pipeline`:**
  - **Modo 1 (Geração Direta):** Chamado pelos Gates 4 da `pre-code-pipeline`, `execution-pipeline` e Gate 2 da `release-and-ops-pipeline` para redação técnica padronizada via `humanizer`.
  - **Modo 2 (Revisão Tabular Não-Destrutiva):** Chamado no Gate 2 da `audit-and-refactoring-pipeline` para estruturar achados na matriz `ID | Arquivo | Severidade | Original | Sugestão | Racional`.

---

## 2. As 5 Meta-Skills e seus 15 Arquivos de Referência

| Meta-Skill | Propósito Operacional | Arquivos de Referência (`references/`) | Comandos de Ativação |
| :--- | :--- | :--- | :--- |
| [**`pre-code-pipeline`**](file:///home/tales/.gemini/config/skills/pre-code-pipeline/SKILL.md) | Conduz o planejamento pré-código em 5 Gates sequenciais para Engenharia de Software e Ciência de Dados (Ask, Prepare, Process, Analyze, Share, Act). | 1. [`quarto-quality-checklist.md`](file:///home/tales/.gemini/config/skills/pre-code-pipeline/references/quarto-quality-checklist.md) *(1)* | `use a pre-code-pipeline`<br>`iniciar planejamento pré-código` |
| [**`execution-pipeline`**](file:///home/tales/.gemini/config/skills/execution-pipeline/SKILL.md) | Guia a implementação técnica, testes unitários/integração, visualizações e documentação em 5 Gates polimórficos pós-planejamento. | *(Herda contratos de `pre-code-pipeline` e invoca `writing-pipeline` / `release-and-ops-pipeline`)* *(0)* | `use a execution-pipeline`<br>`iniciar execução técnica` |
| [**`writing-pipeline`**](file:///home/tales/.gemini/config/skills/writing-pipeline/SKILL.md) | Autoridade editorial para redação sênior e revisão técnica. Opera no Modo 1 (geração direta) e Modo 2 (revisão tabular não-destrutiva). | 2. [`archetype-a-academic.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/archetype-a-academic.md)<br>3. [`archetype-b-software.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/archetype-b-software.md)<br>4. [`archetype-c-cli.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/archetype-c-cli.md)<br>5. [`before-after-examples.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/before-after-examples.md)<br>6. [`canonical-sources.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/canonical-sources.md)<br>7. [`metrics-and-anti-ai.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/metrics-and-anti-ai.md)<br>8. [`review-protocol.md`](file:///home/tales/.gemini/config/skills/writing-pipeline/references/review-protocol.md) *(7)* | `use a writing-pipeline`<br>`redigir documento`<br>`revisar texto em tabela` |
| [**`release-and-ops-pipeline`**](file:///home/tales/.gemini/config/skills/release-and-ops-pipeline/SKILL.md) | Governa a entrega pós-execução em 5 Gates: saneamento pré-push, versionamento Git/SemVer, CI/CD, deploy polimórfico e smoke tests. | 9. [`archetype-a-ghpages.md`](file:///home/tales/.gemini/config/skills/release-and-ops-pipeline/references/archetype-a-ghpages.md)<br>10. [`pre-push-sanitation.md`](file:///home/tales/.gemini/config/skills/release-and-ops-pipeline/references/pre-push-sanitation.md)<br>11. [`smoke-and-healthcheck.md`](file:///home/tales/.gemini/config/skills/release-and-ops-pipeline/references/smoke-and-healthcheck.md) *(3)* | `use a release-and-ops-pipeline`<br>`publicar release`<br>`executar deploy e smoke tests` |
| [**`audit-and-refactoring-pipeline`**](file:///home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/SKILL.md) | Conduz engenharia reversa, diagnóstico multi-camadas, testes de caracterização (*Golden Master*) e refatoração incremental em código legado. | 12. [`archetype-a-analytics-audit.md`](file:///home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/references/archetype-a-analytics-audit.md)<br>13. [`characterization-tests.md`](file:///home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/references/characterization-tests.md)<br>14. [`refactoring-patterns-abc.md`](file:///home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/references/refactoring-patterns-abc.md)<br>15. [`severity-matrix-and-triage.md`](file:///home/tales/.gemini/config/skills/audit-and-refactoring-pipeline/references/severity-matrix-and-triage.md) *(4)* | `use a audit-and-refactoring-pipeline`<br>`auditar projeto legado`<br>`refatorar código legado` |

### Skills de Apoio Integradas

| Skill de Apoio | Propósito Operacional |
| :--- | :--- |
| [**`humanizer`**](file:///home/tales/.gemini/config/skills/humanizer/SKILL.md) | Autoridade de micro-estilo técnico anti-IA, eliminação de fórmulas artificiais e variação métrica de ritmo (*burstiness*). Invocada pelas pipelines nas etapas editoriais. |
| [**`skill-loader`**](file:///home/tales/.gemini/config/skills/skill-loader/SKILL.md) | Protocolo de carregamento sob demanda para a biblioteca fria (Cold Storage), mantendo o orçamento de prompt permanente preservado. |

---

## 3. Instalação e Uso no Antigravity / Gemini CLI

Para instalar as meta-skills e utilitários no ambiente local:

```bash
# Clone o repositório
git clone git@github.com:talesgomes27/antigravity-meta-skills.git

# Copie as pastas para o diretório de configuração do Antigravity
cp -r antigravity-meta-skills/{pre-code-pipeline,execution-pipeline,writing-pipeline,release-and-ops-pipeline,audit-and-refactoring-pipeline,humanizer,skill-loader} ~/.gemini/config/skills/
```

---

## 4. Diretrizes de Governança e Orçamento de Contexto

Para preservar a estabilidade e a capacidade de raciocínio do modelo durante sessões longas, aplicam-se três regras estritas de arquitetura:

### 4.1 Orçamento de Tokens (< 20.000 tokens)
- O Antigravity injeta o cabeçalho de todas as skills ativas (`name` + `path` + `description`) no prompt de sistema permanente.
- O teto estabelecido para o bloco de skills é de **20.000 tokens**.
- As descrições no frontmatter de cada `SKILL.md` devem ser mantidas em linha única, concisas e abaixo de **80 tokens** (~320 caracteres).
- Estado atual do bloco de skills do sistema: **~7.128 tokens utilizados** (35,6% do limite), mantendo **~12.872 tokens livres**.

### 4.2 Carregamento Sob Demanda via `skill-loader` (Cold Storage)
- O ecossistema mantém um acervo de **2.675 skills arquivadas** na biblioteca fria em `/home/tales/.gemini/config/skills-library/` (indexadas em `skills_index.json`).
- Nenhuma skill especialista de nicho deve ser promovida para a pasta ativa `/home/tales/.gemini/config/skills/` sem justificativa prévia de uso contínuo.
- Quando uma tarefa exigir ferramentas como `complexity-cuts`, `brooks-audit`, `weather-data-reproducibility` ou `framework-migration-legacy-modernize`, ative-as via [**`skill-loader`**](file:///home/tales/.gemini/config/skills/skill-loader/SKILL.md):
  ```markdown
  Acesse /home/tales/.gemini/config/skills-library/<nome-da-skill>/SKILL.md sob demanda via view_file.
  ```

### 4.3 Proibição Estrita de Caminhos Relativos
- É expressamente proibido o uso de caminhos relativos (como `../`, `./` ou `references/arquivo.md`) dentro dos arquivos `SKILL.md` ou nos playbooks de referência.
- Todo link documental ou instrução de carregamento deve utilizar caminhos absolutos com esquema de URL compatível:
  `file:///home/tales/.gemini/config/skills/<meta-skill>/references/<arquivo>.md`
- Essa restrição evita falhas de resolução quando o agente executa comandos a partir de diretórios de trabalho distintos do workspace raiz.
