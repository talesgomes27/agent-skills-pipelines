---
name: writing-pipeline
description: "Conduz a redação e revisão técnica de documentos (PRDs, Quarto, READMEs, ADRs) com voz sênior anti-IA, estilo canônico e adaptação estrita aos Arquétipos A, B e C."
---

# Skill: writing-pipeline

Este playbook governa a redação técnica, revisão editorial e
verificação de fontes dos artefatos produzidos pelas pipelines
`pre-code-pipeline` (PRDs, specs, planos) e `execution-pipeline`
(READMEs, relatórios Quarto, ADRs, docstrings). A skill não substitui
as pipelines existentes: ela é invocada nos Gates 2, 3 e 5 da pre-code-pipeline e nos Gates 1 e 4 da execution-pipeline como
sub-rotina especializada em escrita.

---

## 0. Contrato de Herança e Coordenação

### 0.1 Herança de Arquétipo

Antes de escrever qualquer documento, ler `docs/00_archetype.md`. O
arquétipo determina qual arquivo de referência carregar:

- **Arquétipo A** (Data Science/Quarto) → `/home/tales/.gemini/config/skills/writing-pipeline/references/archetype-a-academic.md` (em coordenação técnica com `quarto-expert` em `/home/tales/.gemini/config/skills/quarto-expert/SKILL.md` para formatação de manuscritos, teses ABNT NBR 14724:2024 e citações BibTeX/CSL)
- **Arquétipo B** (Software/APIs) → `/home/tales/.gemini/config/skills/writing-pipeline/references/archetype-b-software.md`
- **Arquétipo C** (CLI/Scripts) → `/home/tales/.gemini/config/skills/writing-pipeline/references/archetype-c-cli.md`

Se `docs/00_archetype.md` não existir:
1. Procure declaração explícita de arquétipo (`archetype: A|B|C` ou `Arquétipo [A/B/C]`) no contexto do prompt ativo, em `docs/01-data-discovery-and-contracts.md` ou em `docs/02-PRD-and-specs.md`.
2. Se encontrar, grave imediatamente `docs/00_archetype.md` com o frontmatter YAML padrão e prossiga.
3. Se continuar ausente, PARAR e perguntar ao usuário. Nunca inferir arquétipo por heurística.

### 0.2 Coordenação com `humanizer`

A skill `humanizer` é a autoridade de micro-estilo (vícios de IA,
travessões, falsos contrastes, tríades, gerundismos, vocabulário
clichê). Esta skill invoca `humanizer` como sub-rotina durante a
redação e nunca duplica suas regras.

Ordem de execução em qualquer redação:

1. Identificar arquétipo (0.1).
2. Carregar `/home/tales/.gemini/config/skills/writing-pipeline/references/archetype-{a,b,c}.md`.
3. Aplicar `humanizer` para micro-estilo.
4. Aplicar esta skill para macro-estrutura (argumentação, citação,
   adaptação por arquétipo).
5. Executar o checklist de entrega (Seção 4).

### 0.3 Stop Conditions

- Se `docs/00_archetype.md` não existir e o fallback de 0.1 falhar → PARAR e perguntar ao usuário.
- Se o arquivo `/home/tales/.gemini/config/skills/writing-pipeline/references/archetype-{a,b,c}.md` correspondente não
  existir → PARAR.
- Se uma citação usar `[@chave]` que não conste em
  `/home/tales/.gemini/config/skills/writing-pipeline/references/canonical-sources.md` → PARAR e reportar. Não inventar
  fontes. Substituir por link inline `[Autor, Ano](URL)` se aplicável.

---

## 1. Modo 1: Geração e Redação Direta (Invocado por Pipelines)

Use este modo ao criar ou atualizar artefatos de projeto (PRDs, ADRs, planos, index.qmd, README.md, docstrings) dentro dos Gates da pre-code-pipeline e execution-pipeline.

### 1.1 Pré-escrita

1. Ler o arquétipo (0.1).
2. Ler o documento-alvo se for revisão (não escrever do zero sobre
   algo existente sem antes entender o que está lá).
3. Consultar `/home/tales/.gemini/config/skills/writing-pipeline/references/archetype-{a,b,c}.md` para registrar as
   convenções obrigatórias (registro, pessoa gramatical, comprimento
   de frase, citação, tom).
4. Consultar `/home/tales/.gemini/config/skills/writing-pipeline/references/metrics-and-anti-ai.md` para as 5 métricas
   operacionais.

### 1.2 Escrita

Escrever seguindo as convenções do arquétipo. Cada parágrafo deve
obedecer às métricas:

- **Burstiness e Comprimento de Frase (Adaptado por Arquétipo)**:
  - *Arquétipo A e Prosa Argumentativa (PRDs/ADRs):* alternar frases curtas (3–6 palavras, ≥ 15% do parágrafo) com frases articuladas (22–32 palavras), mantendo desvio padrão ≥ 6,5 palavras.
  - *Arquétipo B (Docs de Software e Docstrings):* frases médias e contratuais de 10–18 palavras (dispensado de atingir 22–32 palavras).
  - *Arquétipo C (CLI, Manpages e Erros POSIX):* frases telegráficas e imperativas de 5–12 palavras (dispensado de burstiness longo).
- **Zero tells de IA**: consultar blacklist em
  `/home/tales/.gemini/config/skills/writing-pipeline/references/metrics-and-anti-ai.md`.
- **Zero falsos contrastes**: proibido "não apenas X, mas Y".
- **Zero gerundismos decorativos**: proibido "garantindo assim...".
- **Diagramas em Quarto (.qmd):** Diagramas Mermaid e Graphviz DEVEM ser inseridos como executable cells (` ```{mermaid} ` / ` ```{dot} `), NUNCA como code blocks comuns. O Quarto compila essas células em SVG interativo para HTML e PNG para PDF.

### 1.3 Citação

- Fontes no manifesto → usar `[@chave]`.
- Fontes fora do manifesto → usar link inline `[Autor, Ano](URL)`.
- Nunca forjar citações.

---

## 2. Modo 2: Revisão Editorial Não-Destrutiva (Invocado para Auditoria)

Use este modo exclusivamente quando o usuário solicitar auditoria ou revisão editorial de um texto existente sem reescrita direta.

Baseado em `/home/tales/.gemini/config/skills/writing-pipeline/references/review-protocol.md`. A revisão NUNCA reescreve
o conteúdo. Ela produz uma tabela:

| Linha | Original | Sugestão | Racional |
|:---:|:---|:---|:---|

Categorias verificadas (6):
1. Fatos técnicos (valores, APIs, comandos).
2. Gramática e pontuação.
3. Consistência de terminologia.
4. Estrutura e ordem das seções.
5. Tom e registro (aderente ao arquétipo).
6. Citações e referências.

---

## 3. Política Anti-Alucinação

### 3.1 Mecanismo

1. Varrer o documento com regex `\[@([a-zA-Z0-9_\.\:-]+)\]`.
2. Para cada chave capturada, consultar `/home/tales/.gemini/config/skills/writing-pipeline/references/canonical-sources.md`.
3. Chaves ausentes → marcar como não-validadas e PARAR.

### 3.2 Manifesto Canônico

`/home/tales/.gemini/config/skills/writing-pipeline/references/canonical-sources.md` lista as fontes autorizadas. Novas
fontes entram apenas via edição explícita do manifesto.

### 3.3 Fontes Externas

Se o documento precisar de fonte fora do manifesto, usar link inline:

  Segundo [Pinker, 2014](https://example.com/sense-of-style), ...

Proibido: `[@pinker_sense_style]` sem registro prévio.

---

## 4. Checklist de Entrega

Antes de considerar o documento pronto, verificar os 10 itens:

1. [ ] O parágrafo abre com o dado concreto, sem preâmbulos.
2. [ ] Há alternância nítida entre frases curtas e longas.
3. [ ] Zero adjetivos de marketing ("robusto", "vital", "inovador").
4. [ ] Zero falsos contrastes ("não apenas X, mas Y").
5. [ ] Zero travessões duplos conectando orações independentes.
6. [ ] Listas assimétricas (sem negrito obrigatório em cada item).
7. [ ] Pessoa gramatical consistente com o arquétipo.
8. [ ] Toda citação rastreável no manifesto ou como link inline.
9. [ ] Conclusão encerra no último resultado útil (sem sermão).
10. [ ] O texto soa como relato de engenheiro sênior.

---

## 5. Integração com as Pipelines

### 5.1 pre-code-pipeline

Invocada no Modo 1 (Geração) nos seguintes portões:
- **Gate 2**: redação de `docs/02-PRD-and-specs.md`.
- **Gate 3**: redação de `docs/03-architecture-and-schema.md` e ADRs (`docs/adr/`).
- **Gate 5**: redação de `docs/05-implementation-plan.md`.

### 5.2 execution-pipeline

Invocada no Modo 1 (Geração) nos seguintes portões:
- **Gate 1**: docstrings Google Style em `src/`.
- **Gate 4**: `index.qmd` (Arquétipo A), `README.md` de software e guias de API (Arquétipo B), ou `README.md` operacional POSIX (Arquétipo C).

### 5.3 Handoff

Esta skill NÃO bloqueia os Gates 5. Se a redação estiver incompleta,
o Gate 5 (`docs-guard`) detecta divergências e reporta.

---

## Consumo Opcional de `GRAPH_REPORT.md` para Relatórios Arquiteturais

Referência completa: `/home/tales/.gemini/config/skills/quarto-expert/references/graphify-integration.md`

O `writing-pipeline` **não invoca** `graphify` diretamente, mas pode **consumir passivamente** `graphify-out/GRAPH_REPORT.md` (quando existir) para enriquecer relatórios Quarto com métricas de módulos, acoplamento, comunidades funcionais e God Nodes.

```bash
if [ -f "graphify-out/GRAPH_REPORT.md" ]; then
    USE_GRAPH_REPORT=1
else
    USE_GRAPH_REPORT=0
fi
```

Se `USE_GRAPH_REPORT=1`: incluir subseção de arquitetura baseada no `GRAPH_REPORT.md` como fonte auditável.

Se `USE_GRAPH_REPORT=0`: omitir sem quebra de fluxo.

---

## 6. Referências

- `/home/tales/.gemini/config/skills/writing-pipeline/references/archetype-a-academic.md` — Convenções IMRAD, APA,
  Chicago, IEEE, CONSORT, STROBE, PRISMA.
- `/home/tales/.gemini/config/skills/writing-pipeline/references/archetype-b-software.md` — Convenções Google/Microsoft
  Style, OpenAPI, ADR, README.
- `/home/tales/.gemini/config/skills/writing-pipeline/references/archetype-c-cli.md` — Convenções POSIX, manpages,
  mensagens de erro.
- `/home/tales/.gemini/config/skills/writing-pipeline/references/metrics-and-anti-ai.md` — 5 métricas + blacklist + 10
  itens de checklist.
- `/home/tales/.gemini/config/skills/writing-pipeline/references/canonical-sources.md` — Manifesto de fontes autorizadas.
- `/home/tales/.gemini/config/skills/writing-pipeline/references/before-after-examples.md` — 5 pares antes/depois.
- `/home/tales/.gemini/config/skills/writing-pipeline/references/review-protocol.md` — Padrão Original → Sugestão →
  Racional.
