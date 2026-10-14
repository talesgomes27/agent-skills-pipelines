---
name: release-and-ops-pipeline
description: "Conduz o ciclo pós-execução de entrega em 5 Gates (Saneamento, Git/SemVer, CI/CD, Deploy e Smoke Tests) para Arquétipos A, B e C. Use após o Gate 5 da execution-pipeline."
---

# Skill: release-and-ops-pipeline

Este playbook governa a fase final de entrega, empacotamento, publicação e verificação pós-deploy. A esteira recebe o projeto já testado e compilado pela `execution-pipeline` e conduz a publicação segura conforme o arquétipo do repositório.

---

## 0. Contrato de Herança, Orçamento e Coordenação

### 0.1 Leitura de Arquétipo e Fallback
1. Antes de qualquer operação, leia `docs/00_archetype.md` para identificar o arquétipo ativo (`A` = Data Science/Quarto, `B` = Software/Web/APIs, `C` = CLI/Scripts).
2. **Fallback:** Se `docs/00_archetype.md` não existir, busque a declaração de arquétipo em `docs/01-data-discovery-and-contracts.md`, `docs/02-PRD-and-specs.md` ou `docs/05-implementation-plan.md` e reconstrua `docs/00_archetype.md`.
3. **Stop Condition:** Se o arquétipo continuar ausente, **PARE imediatamente** e pergunte ao usuário. Nunca assuma o arquétipo por heurística.

### 0.2 Carregamento Sob Demanda (Cold Storage & Plugins)
Para preservar o orçamento de tokens, as skills especialistas de DevOps residem em `/home/tales/.gemini/config/skills-library/` e devem ser carregadas sob demanda via `skill-loader` apenas no Gate em que forem utilizadas:
- Gate 1: `codebase-audit-pre-push`, `dependency-management-deps-audit`, `client-secret-exposure-audit` (além de `managing-python-dependencies`, que já está ativa via plugin `data-agent-kit-plugin`).
- Gate 2: `changelog-automation`, `git-pushing`, `git-workflow`, `git-pr-review`
- Gate 3: `github-actions-templates`, `github-actions-advanced`, `github-actions-debugger`
- Gate 4: `docker-expert`, `docker-compose`, `deploy-to-vercel`, `cloudflare-pages`, `python-packaging`
- Gate 5: `shipping-and-launch`, `pre-release-review`

### 0.3 Coordenação com `writing-pipeline` e `humanizer`
Toda redação gerada nesta esteira (`CHANGELOG.md`, *Release Notes*, descrições de Pull Request e mensagens de commit) é governada pela skill ativa `writing-pipeline` (`/home/tales/.gemini/config/skills/writing-pipeline/SKILL.md`) no **Modo 1 (Geração)** em coordenação com `humanizer` (Seção 3.1 para *Conventional Commits*).

### 0.4 Checkpoints Humanos e Rastreabilidade (`task.md`)
- Atualize o arquivo `task.md` via `planning-with-files` na abertura e após a aprovação de cada Gate.
- **Guardrail de Push e Deploy:** Nunca execute `git push` para repositórios remotos nem dispare deploys em produção sem apresentar o resumo do Gate e obter autorização explícita do usuário.

---

## Fluxo Polimórfico dos 5 Gates de Release & Ops

```text
[Handoff: Gate 5 da execution-pipeline Aprovado]
                       │
                       ▼
Gate 1 (Saneamento, Segredos & Lockfiles) ──→ [Aprovação]
                       │
                       ▼
Gate 2 (Git, SemVer, Commits & Changelog) ──→ [Aprovação]
                       │
                       ▼
Gate 3 (CI/CD Workflows — GitHub Actions) ──→ [Aprovação]
                       │
                       ▼
Gate 4 (Deploy & Publicação Polimórfica)  ──→ [Aprovação de Push/Deploy]
   ├─ Arquétipo A: GitHub Pages (Quarto + freeze: auto)
   ├─ Arquétipo B: Docker / Cloud / Vercel / APIs
   └─ Arquétipo C: Build PyPI / Wheel / GitHub Release
                       │
                       ▼
Gate 5 (Smoke Tests & Verificação no Ar)  ──→ [Entrega Homologada]
```

---

## 1. Gate 1: Saneamento de Repositório, Segurança Pré-Push & Lockfiles (Comum)

- **Objetivo**: Garantir que o repositório esteja limpo, sem credenciais expostas, sem bases de dados pesadas rastreadas indevidamente e com lockfiles íntegros.
- **Skills e Referências Mobilizadas**:
  - Leitura obrigatória de `/home/tales/.gemini/config/skills/release-and-ops-pipeline/references/pre-push-sanitation.md`.
  - `codebase-audit-pre-push` *(Cold Storage)*
  - `managing-python-dependencies` *(Ativa via plugin `data-agent-kit-plugin`)*
  - `dependency-management-deps-audit` *(Cold Storage — para Arquétipos B e C)*
  - `client-secret-exposure-audit` *(Cold Storage — condicional para Frontend no Arquétipo B)*
- **Operação**:
  1. Auditar e atualizar `.gitignore` conforme o arquétipo (em Arquétipo A: bloquear `*.csv`, `*.parquet`, `*.pkl`, `/.quarto/`, e manter `/_freeze/` versionado quando `freeze: auto` ou `true`).
  2. Executar varredura contra segredos vazados (`.env`, chaves, tokens) e verificar se há arquivos `> 50 MB` no workspace.
  3. Validar sincronia de lockfiles (`uv.lock`, `pnpm-lock.yaml`).
- **Artefatos de Saída**: `.gitignore` blindado, lockfiles validados e parecer de saneamento pré-push.
- **Critério de Parada**: Confirmação humana do parecer de saneamento (atualizar Gate 1 como `[x]` no `task.md`).

---

## 2. Gate 2: Governança Git, Versionamento Semântico & Changelog (Comum)

- **Objetivo**: Organizar commits atômicos, definir a versão SemVer (`vX.Y.Z`) e documentar as entregas no `CHANGELOG.md`.
- **Skills Mobilizadas**:
  - `writing-pipeline` (`/home/tales/.gemini/config/skills/writing-pipeline/SKILL.md` — Modo 1)
  - `humanizer` (Regras de *Conventional Commits*: imperativo, letras minúsculas, conciso, zero adjetivação vazia)
  - `changelog-automation` *(Cold Storage)*
  - `git-workflow` & `git-pushing` *(Cold Storage)*
- **Operação**:
  1. Determinar o incremento SemVer (`PATCH`, `MINOR` ou `MAJOR`) com base nas alterações entregues.
  2. Redigir ou atualizar `CHANGELOG.md` seguindo o padrão *Keep a Changelog* via `writing-pipeline`.
  3. Estruturar commits atômicos em *staging* e preparar a tag anotada da versão (`git tag -a vX.Y.Z -m "..."`), aguardando autorização para push.
- **Artefatos de Saída**: `CHANGELOG.md` atualizado, commits locais limpos e proposta de tag SemVer.
- **Critério de Parada**: Aprovação humana do `CHANGELOG.md` e do histórico de commits (atualizar Gate 2 como `[x]` no `task.md`).

---

## 3. Gate 3: Automação de CI/CD — GitHub Actions (Polimórfico)

- **Objetivo**: Configurar ou validar os workflows de integração e entrega contínua em `.github/workflows/`.
- **Skills Mobilizadas**:
  - `github-actions-templates` *(Cold Storage)*
  - `github-actions-advanced` *(Cold Storage)*
  - `github-actions-debugger` *(Cold Storage — se houver falha em execuções prévias)*
- **Operação por Arquétipo**:
  - **Arquétipo A (Data Science & Quarto):** Configurar `.github/workflows/publish.yml` (ou validar pipeline de renderização estática com cache `_freeze/` e setup condicional de `uv`), consultando `/home/tales/.gemini/config/skills/release-and-ops-pipeline/references/archetype-a-ghpages.md`.
  - **Arquétipo B (Software, Web & APIs):** Configurar `.github/workflows/ci.yml` com cache de `uv`/`pnpm`, lint (`ruff`/`eslint`), testes (`pytest --cov`) e build de container/deploy.
  - **Arquétipo C (CLI & Scripts):** Configurar `.github/workflows/ci.yml` com matriz de testes unitários, checagem de tipos e workflow de release em tags `v*`.
- **Artefatos de Saída**: Arquivos `.github/workflows/*.yml` validados.
- **Critério de Parada**: Validação dos workflows pelo usuário (atualizar Gate 3 como `[x]` no `task.md`).

---

## 4. Gate 4: Deploy, Publicação e Empacotamento (Polimórfico)

- **Objetivo**: Executar o empacotamento final, push autorizado para o repositório remoto e publicação no ambiente de destino.
- **Operação e Skills por Arquétipo**:
  - **Arquétipo A (Relatório Quarto no GitHub Pages)**:
    - *Referência:* `/home/tales/.gemini/config/skills/release-and-ops-pipeline/references/archetype-a-ghpages.md`.
    - Garantir presença de `.nojekyll` (se publicado via `docs/`), versionar `_freeze/` e `reports/figures/`, executar `git push` (após autorização) e acionar publicação no GitHub Pages.
  - **Arquétipo B (Software, Web, APIs & Containers)**:
    - *Skills (Cold Storage):* `docker-expert`, `docker-compose`, `deploy-to-vercel` / `cloudflare-pages`, `pre-release-review`.
    - Construir e testar imagem Docker multi-stage ou executar deploy na plataforma alvo (Vercel, Netlify, Cloud Run, Render) com variáveis de ambiente validadas.
  - **Arquétipo C (CLI, Pacotes Python & Releases)**:
    - *Skills (Cold Storage):* `python-packaging`, `pre-release-review`.
    - Executar `uv build` para gerar artefatos em `dist/` (`.whl` e `.tar.gz`), validar entrypoints no `pyproject.toml` e publicar GitHub Release (ou PyPI).
- **Artefatos de Saída**:
  - *A:* Site/Relatório publicado no GitHub Pages.
  - *B:* Aplicação/API ou container em execução no ambiente alvo.
  - *C:* Artefatos `dist/` compilados e Release publicada.
- **Critério de Parada**: Confirmação de conclusão do deploy/build sem erros de execução (atualizar Gate 4 como `[x]` no `task.md`).

---

## 5. Gate 5: Smoke Tests Pós-Deploy & Homologação Final (Polimórfico)

- **Objetivo**: Verificar empiricamente que o artefato publicado está no ar, íntegro e respondendo conforme esperado.
- **Skills e Referências Mobilizadas**:
  - Leitura obrigatória de `/home/tales/.gemini/config/skills/release-and-ops-pipeline/references/smoke-and-healthcheck.md`.
  - `shipping-and-launch` *(Cold Storage)*
  - `webapp-testing` *(Ativa — para interfaces web no Arquétipo B)*
  - `writing-pipeline` (Para redação do sumário final de entrega)
- **Operação por Arquétipo**:
  - **Arquétipo A:** Checagem de integridade das imagens `<img src>` no HTML compilado e validação de status HTTP 200 na URL pública do GitHub Pages.
  - **Arquétipo B:** Healthcheck HTTP 200 (`< 2s`) nas rotas da API e smoke test com Playwright na interface web.
  - **Arquétipo C:** Execução isolada do pacote/binário confirmando funcionamento de `--help`, `--version` e exit code `0`.
  - *Contingência:* Se o smoke test falhar, aplicar imediatamente o protocolo de rollback da Seção 4 de `smoke-and-healthcheck.md`.
- **Artefatos de Saída**: Relatório de homologação pós-deploy e todos os Gates marcados como `[x] Aprovado` no `task.md`.
- **Critério de Parada**: Aceite final do usuário encerrando oficialmente o ciclo do projeto.

---

## 6. Matriz de Rastreabilidade Arquétipo × Gate × Skill

| Arquétipo | Gate 1 (Saneamento & Segredos) | Gate 2 (Git, SemVer & Changelog) | Gate 3 (CI/CD GitHub Actions) | Gate 4 (Deploy & Empacotamento) | Gate 5 (Smoke Tests & Homologação) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A: Data Science & Quarto** | `pre-push-sanitation.md`<br>`codebase-audit-pre-push`*<br>`managing-python-dependencies`<br>*(.gitignore + _freeze/)* | `writing-pipeline`<br>`humanizer`<br>`changelog-automation`*<br>`git-pushing`*<br>*(CHANGELOG.md + tag)* | `archetype-a-ghpages.md`<br>`github-actions-templates`*<br>`github-actions-advanced`*<br>*(publish.yml)* | `archetype-a-ghpages.md`<br>`git-pushing`*<br>*(GitHub Pages deploy)* | `smoke-and-healthcheck.md`<br>`shipping-and-launch`*<br>*(HTTP 200 + img check)* |
| **B: Software, APIs & Web** | `pre-push-sanitation.md`<br>`codebase-audit-pre-push`*<br>`dependency-management-deps-audit`*<br>`client-secret-exposure-audit`* | `writing-pipeline`<br>`humanizer`<br>`changelog-automation`*<br>`git-workflow`*<br>*(CHANGELOG.md + PR/tag)* | `github-actions-templates`*<br>`github-actions-advanced`*<br>*(ci.yml + matrix)* | `docker-expert`*<br>`docker-compose`*<br>`deploy-to-vercel`*<br>`pre-release-review`* | `smoke-and-healthcheck.md`<br>`webapp-testing`<br>`shipping-and-launch`*<br>*(/health + Playwright)* |
| **C: CLI & Scripts** | `pre-push-sanitation.md`<br>`codebase-audit-pre-push`*<br>`managing-python-dependencies`<br>`dependency-management-deps-audit`* | `writing-pipeline`<br>`humanizer`<br>`changelog-automation`*<br>`git-pushing`*<br>*(CHANGELOG.md + tag)* | `github-actions-templates`*<br>`github-actions-advanced`*<br>*(ci.yml + release)* | `python-packaging`*<br>`pre-release-review`*<br>*(uv build + dist/)* | `smoke-and-healthcheck.md`<br>`shipping-and-launch`*<br>*(uv tool run + exit 0)* |

*(Itens com `*` residem em `/home/tales/.gemini/config/skills-library/` e são carregados sob demanda via `skill-loader`).*
