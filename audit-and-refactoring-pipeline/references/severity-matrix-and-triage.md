# Matriz de Severidade e Triagem de Dívida Técnica

Todo achado diagnosticado no **Gate 2** da `audit-and-refactoring-pipeline` deve ser classificado segundo esta matriz em `docs/audit-report.md`.

## 1. Critérios Objetivos de Severidade

| Severidade | Critérios Técnicos, Analíticos e Editoriais | Regra de Triagem e Execução |
| :--- | :--- | :--- |
| **Crítico (P0)** | - **Dados/ML (Arq. A):** *Data leakage* temporal/grupo ou *target leakage*; números no texto contradizendo tabelas/código; ausência de validação.<br>- **Software/CLI (Arq. B/C):** Credenciais/segredos expostos; vulnerabilidades de segurança (SQLi, auth bypass); corrupção silenciosa de dados; falha de build.<br>- **Editorial:** Citações `[@chave]` inventadas (alucinação bibliográfica). | **Bloqueante.** Deve ser corrigido obrigatoriamente na Fatia 1 (Batch 1) do Gate 4 antes de qualquer outra alteração. |
| **Alto (P1)** | - **Dados/ML (Arq. A):** Ausência de `seed`/`random_state` global; falta de `execute: freeze: auto` em relatórios pesados; quebra da estrutura CRISP-ML(Q) + Storytelling (hipóteses da Seção 1 sem resposta/gráfico na Seção 5, ausência de Baseline comparativo na Seção 4 ou falta de Recomendações Executivas na Seção 6); importância `split` contradizendo a narrativa; diagramas em code blocks sem chaves (```mermaid / ```dot) que não renderizam no Quarto; documentos com diagramas usando extensão .md em vez de .qmd.<br>- **Software/CLI (Arq. B/C):** Módulos críticos sem testes (`0%` cobertura); dependências cíclicas; queries N+1; complexidade ciclomática `> 20`. | **Obrigatório no ciclo atual.** Exige Teste de Caracterização no Gate 3 antes da refatoração no Gate 4. |
| **Médio (P2)** | - **Dados/ML (Arq. A):** Figuras com `dpi < 300`, subfiguras desalinhadas (falta de `set_box_aspect(1)`), numeração manual duplicada com `number-sections: true`, falta de `lang: pt-BR`, ausência de padronização com `uv + pyproject.toml + Ruff` quando o projeto for Python puro; cell options de diagrama (%%| ou //|) fora da posição canônica; diagramas referenciados por @fig- sem label: fig-* correspondente.<br>- **Software/CLI (Arq. B/C):** *Code smells* moderados (complexidade `10–20`), código morto isolado, docstrings defasadas (`docs-guard`), testes com *over-mocking* (`test-guard`).<br>- **Editorial:** Vícios de IA detectados pela `writing-pipeline` / `humanizer`. | **Recomendado no ciclo atual.** Agrupar em fatias temáticas (código, visual, documentação) no Gate 4. |
| **Baixo (P3)** | - Formatação cosmética, ordenação de imports, variáveis locais pouco descritivas ou comentários óbvios. | **Opcional / Batch Final.** Automatizar via linter (`ruff check --fix` / `ruff format`). |

## 2. Template Obrigatório para `docs/audit-report.md` (Modo 2 da `writing-pipeline`)

| ID | Linha / Arquivo | Severidade | Diagnóstico Original | Sugestão de Refatoração | Racional Técnico |
| :--- | :--- | :---: | :--- | :--- | :--- |
| `AUD-01` | `src/pipeline.py:42` | `Crítico` | `StandardScaler().fit_transform(df)` antes do split temporal | Mover para `Pipeline` ajustado apenas em `X_train` | Elimina *data leakage* da distribuição futura no conjunto de validação. |
