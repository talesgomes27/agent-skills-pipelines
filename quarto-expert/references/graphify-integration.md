---
type: shared-reference
scope: multi-skill
owner: ecossistema-meta-skills
consumers:
  - audit-and-refactoring-pipeline
  - execution-pipeline
  - pre-code-pipeline
  - release-and-ops-pipeline
  - writing-pipeline
  - quarto-expert (referência passiva)
---

# Integração `graphify` (GraphRAG Estático Local) nas Meta-Skills

> **Nota de proveniência:** este arquivo é uma **referência compartilhada** entre
> múltiplas Meta-Skills. Ele vive sob `quarto-expert/references/` por convenção
> histórica, mas é referenciado por 5 pipelines adicionais. NÃO remover sem
> atualizar todos os `SKILL.md` que apontam para ele.

O `graphify` é uma dependência **opcional** que atua como GraphRAG estático local:
roda AST parsing no terminal e expõe consultas via teoria dos grafos, **a custo
zero de tokens de LLM**.

## Verificação de Disponibilidade (OBRIGATÓRIA antes de usar)

Toda Meta-Skill que invocar `graphify` **deve** primeiro executar:

```bash
if ! command -v graphify > /dev/null 2>&1; then
    echo "AVISO: graphify nao disponivel. Usando fallback (read_file/grep)."
    USE_GRAPHIFY=0
else
    USE_GRAPHIFY=1
fi
```

Se `USE_GRAPHIFY=0`, o pipeline **prossegue normalmente** com as técnicas
tradicionais (`read_file`, `grep`, inspeção manual). A skill nunca falha por
ausência de `graphify`.

## Estrutura Canônica de Artefatos

Todo projeto que use `graphify` **deve** armazenar os artefatos em `.graphify/`:

```
<projeto>/
├── .graphify/
│   ├── GRAPH_REPORT.md    # versionado (auditável, revisável)
│   ├── graph.html         # ignorado no Git (regenerável)
│   ├── graph.svg          # ignorado no Git (regenerável)
│   └── cache/             # ignorado no Git
└── .gitignore             # deve incluir: .graphify/graph.html, .graphify/graph.svg, .graphify/cache/
```

Adicionar ao `.gitignore` do projeto analisado:

```gitignore
.graphify/graph.html
.graphify/graph.svg
.graphify/cache/
```

## Comandos Canônicos por Pipeline

### `audit-and-refactoring-pipeline`

- **Gate 1 (Reconhecimento):** `graphify .` (gera `.graphify/GRAPH_REPORT.md`). Usar para preencher `docs/00_archetype.md` antes de `read_file` em massa.
- **Gate 2 (Diagnóstico):**
  - God Nodes: extrair da seção de centralidade do `GRAPH_REPORT.md`.
  - Dependências circulares: `graphify query "ciclos" --budget 500`.
  - Mapeamento de impacto: `graphify path "Origem" "Destino"`.

### `execution-pipeline`

- **Consultas cirúrgicas (preferir a `read_file` em massa):** `graphify query "<pergunta>" --budget 1000`.
- **Gate 5 (saneamento pós-execução):** `graphify --update` (detecta código morto, órfãos e acoplamento acidental).

### `pre-code-pipeline`

- **Gate 3 (bounded contexts DDD — Arquétipo B):** usar comunidades Leiden/Louvain do `graphify` para validar separação Domínio/Aplicação/Infraestrutura.

### `release-and-ops-pipeline`

- **Artefatos visuais para docs vivos:**
```bash
graphify export html   # .graphify/graph.html
graphify export svg    # .graphify/graph.svg
```
Copiar para `docs/graph/` antes de publicar em GitHub Pages ou incorporar em relatórios Quarto.

### `writing-pipeline`

- Não invoca `graphify` diretamente. Consome passivamente `.graphify/GRAPH_REPORT.md` (quando existir) para gerar descrições arquiteturais auditáveis em relatórios Quarto.

## Fallback Gracioso — Regra de Ouro

| Etapa | Sem `graphify` (`USE_GRAPHIFY=0`) |
| --- | --- |
| Reconhecimento | `read_file` sobre `pyproject.toml`, `package.json`, `README.md`, `src/` |
| Impacto de alteração | `grep -r "<simbolo>"` + leitura pontual |
| God Nodes | Inspeção via `git log --stat` e `wc -l` |
| Documentação arquitetural | Diagramação manual em `docs/00_archetype.md` |

## Smoke Test Rápido

```bash
graphify --version && graphify . && test -f .graphify/GRAPH_REPORT.md && echo "OK: graphify operacional"
```
