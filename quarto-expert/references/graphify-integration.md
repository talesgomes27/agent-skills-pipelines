---
type: shared-reference
scope: multi-skill
owner: ecossistema-meta-skills
graphify-version-tested: 0.9.93
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
> histórica. **Testado empiricamente contra `graphify v0.9.93`.**

## Pré-requisitos

### Binário
```bash
command -v graphify || echo "NAO INSTALADO — instalar via: pip install graphifyy"
graphify --version   # deve ser >= 0.9.93
```

### API key (para extração semântica)
O `graphify` faz extração em duas camadas:
1. **AST** (estrutural, offline, sempre funciona)
2. **Semântica** (usa LLM, requer API key)

Para habilitar extração semântica completa:
```bash
export GEMINI_API_KEY="..."   # ou GOOGLE_API_KEY
pip install 'graphifyy[gemini]'
```
**Sem API key:** apenas AST é extraído. O grafo funciona, mas com menos arestas inferidas.

## Instalação na Plataforma Antigravity

Registro oficial do skill para o Antigravity:
```bash
graphify install --platform antigravity
```
Alternativa para o projeto atual:
```bash
graphify install --platform antigravity --project
```

## Verificação de Disponibilidade (OBRIGATÓRIA antes de usar)

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

Os artefatos são gerados em **`graphify-out/`** (não `.graphify/`):

```
<projeto>/
├── graphify-out/
│   ├── GRAPH_REPORT.md         # versionado (auditável)
│   ├── graph.json              # versionado (base consultável)
│   ├── graph.html              # ignorado no Git (regenerável, grande)
│   ├── manifest.json           # ignorado no Git (cache de estado)
│   ├── cache/                  # ignorado no Git (AST + semântico)
│   └── .graphify_*.json        # ignorado no Git (intermediários)
└── .gitignore
```

Adicionar ao `.gitignore` do projeto:

```gitignore
graphify-out/graph.html
graphify-out/manifest.json
graphify-out/cache/
graphify-out/.graphify_*.json
```

**Apenas `GRAPH_REPORT.md` e `graph.json` são versionados.**

## Construção e Manutenção

### Construção inicial

```bash
graphify .
```

Faz detecção de corpus, AST extraction e (se houver API key) extração semântica
via subagentes paralelos. Gera `graphify-out/` completo.

### Atualização incremental (após edições de código)

```bash
graphify update <path>    # <path> = . ou subdiretório
```

Re-extrai **apenas código** (sem LLM), usa cache AST. Muito mais rápido que `graphify .`.
Use `--force` se a refatoração removeu código:

```bash
graphify update . --force
```

### Watch mode (desenvolvimento ativo)

```bash
graphify watch <path>
```

Reconstrói o grafo automaticamente ao salvar arquivos.

## Comandos de Consulta (Catálogo Canônico v0.9.93)

### Exit codes de `query`, `path`, `explain`

| Código | Significado |
| :---: | :--- |
| `0` | Resposta encontrada |
| `3` | Nome ambíguo (candidatos listados — desambiguar com `--seed`) |
| `4` | Nenhum nó encontrado |

Detectar programaticamente:
```bash
graphify query "..." || case $? in
    3) echo "Ambigua — use --seed" ;;
    4) echo "Nao encontrado — ampliar busca" ;;
esac
```

### Consulta BFS (`query`)

```bash
graphify query "<pergunta>" --budget 2000
```

- `--budget N`: limite de tokens (default 2000)
- `--dfs`: depth-first ao invés de BFS
- `--context C`: filtro de contexto de aresta (repetível)
- `--seed X`: ponto de partida explícito (id, label ou arquivo)
- `--graph <path>`: graph.json alternativo (default `graphify-out/graph.json`)

### Caminho mais curto (`path`)

```bash
graphify path "Origem" "Destino"
graphify path "A" "B" --undirected   # ignora direção
```

### Raio de impacto reverso (`affected`)

```bash
graphify affected "X" --depth 2
```

Encontra **quem depende de X** (reverse traversal). É mais direto que `path`
para responder "o que quebra se eu alterar X?".
- `--relation R`: filtrar por tipo de aresta (repetível)
- `--depth N`: profundidade (default 2)

### God Nodes (`god-nodes`)

```bash
graphify god-nodes --top 10
graphify god-nodes --top 10 --json
```

Lista os nós mais conectados do grafo (hubs arquiteturais). **Não precisa
parsear `GRAPH_REPORT.md`** — o comando entrega direto.

### Explicação em linguagem natural (`explain`)

```bash
graphify explain "X"
graphify explain "X" --all   # todas as conexões (default: 20 mais conectadas)
```

### Diagnóstico de saúde (`diagnose multigraph`)

```bash
graphify diagnose multigraph
graphify diagnose multigraph --json
```

Reporta risco de colapso de arestas multi-endpoint e problemas estruturais.
- `--max-examples N`: exemplos de mesmo endpoint (default 5)
- `--extract-path PATH`: fonte do extrator para scan de supressão

### Merge cross-repo (`merge-graphs`)

```bash
graphify merge-graphs repo1/graphify-out/graph.json repo2/graphify-out/graph.json \
    --out graphify-out/merged-graph.json
```

### Feedback loop (`save-result`)

Após uma consulta útil, registrar para o grafo aprender:
```bash
graphify save-result \
    --question "onde os dados sao carregados?" \
    --answer "<resumo>" \
    --type query \
    --nodes "load_data" "preprocess" \
    --outcome useful   # useful | dead_end | corrected
```

## Uso por Pipeline

### `audit-and-refactoring-pipeline`

**Gate 1 (Reconhecimento):**
```bash
graphify .              # construcao inicial (uma vez)
cat graphify-out/GRAPH_REPORT.md
```

**Gate 2 (Diagnóstico):**
```bash
graphify god-nodes --top 10      # God Nodes direto (nao parsear report)
graphify diagnose multigraph     # saude do grafo
```

**Gate 4 (Fatiamento Seguro):**
```bash
graphify affected "ModuloX" --depth 2   # raio de impacto (quem depende)
graphify path "Origem" "Destino"        # caminho entre dois modulos
```

### `execution-pipeline`

**Consultas cirúrgicas:**
```bash
graphify query "onde a classe X e instanciada?" --budget 2000
graphify explain "funcao_central" --all
```

**Gate 5 (Saneamento):**
```bash
graphify update . --force
graphify diagnose multigraph
```

### `pre-code-pipeline`

**Gate 3.1 (Bounded Contexts — Arquétipo B):**

Use `.graphify_labels.json` para verificar comunidades reais:
```bash
graphify god-nodes --json | python3 -c "import json,sys; d=json.load(sys.stdin); print([n['label'] for n in d])"
```

Se Domínio e Infraestrutura aparecerem na mesma comunidade (via
`GRAPH_REPORT.md` seção de comunidades), há vazamento de abstração.

### `release-and-ops-pipeline`

**Gate 4.1 (Artefatos visuais):**

O `graph.html` é gerado automaticamente por `graphify .` e `graphify cluster-only`.
Para copiar para docs publicados:

```bash
graphify cluster-only . --no-viz   # ou: graphify . (gera graph.html)
mkdir -p docs/graph
cp graphify-out/graph.html docs/graph/
```

**Nota:** `graph.svg` **não é gerado** pelo v0.9.93. Use `graph.html` (interativo)
ou converta via ferramenta externa (ex: `graphviz`, `mermaid`) se SVG for obrigatório.

### `writing-pipeline`

**Consumo passivo de `GRAPH_REPORT.md`:**
```bash
if [ -f "graphify-out/GRAPH_REPORT.md" ]; then
    USE_GRAPH_REPORT=1
else
    USE_GRAPH_REPORT=0
fi
```
Incluir seção "Arquitetura (auto-gerada)" no relatório Quarto, citando
`GRAPH_REPORT.md` como fonte auditável.

## Fallback Gracioso

| Etapa | Sem `graphify` (`USE_GRAPHIFY=0`) |
| :--- | :--- |
| Reconhecimento | `read_file` sobre `pyproject.toml`, `package.json`, `README.md`, `src/` |
| Impacto de alteração | `grep -r "<simbolo>"` + leitura pontual |
| God Nodes | Inspeção via `git log --stat` e `wc -l` |
| Documentação arquitetural | Diagramação manual em `docs/00_archetype.md` |

Nenhuma Meta-Skill deve falhar por ausência de `graphify`.

## Comandos que NÃO existem no v0.9.93 (NÃO USAR)

- ❌ `graphify merge` — use `graphify update` ou `cluster-only`
- ❌ `graphify build` — feito internamente por `graphify .`
- ❌ `graphify cluster` — use `graphify cluster-only <path>`
- ❌ `graphify report` — gerado automaticamente por `graphify .`
- ❌ `graphify export` — `graph.html` é gerado automaticamente
- ❌ `graphify analyze` — use `graphify diagnose multigraph` ou `god-nodes`
- ❌ `graphify extract` — feito internamente por `graphify .`

## Smoke Test

```bash
graphify --version \
    && graphify . \
    && test -f graphify-out/GRAPH_REPORT.md \
    && test -f graphify-out/graph.json \
    && graphify god-nodes --top 5 \
    && echo "OK: graphify operacional (v0.9.93+)"
```
