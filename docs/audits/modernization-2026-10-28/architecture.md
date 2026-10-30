# Arquitetura atual e proposta

Finalidade: representar contratos observados e decisões propostas. Consumidores: mantenedor, revisores e executores MOD. Diagramas atuais derivam de catálogo, scripts e SKILL.md na base 869444d; setas entre skills representam encaminhamento instrucional, não execução automática. O grafo ignorado de 2026-10-22 não representa essa base.

## Atual 1 — Componentes

```mermaid
flowchart TD
  C[Catálogo e bundles] --> CLI[scripts/skills.py]
  P[Oito pacotes canônicos] --> CLI
  CLI --> I[Cópias ou links e recibos]
  I --> H[Host do agente]
  H --> S[SKILL.md e referências]
  H --> T[task.md do projeto alvo]
  B[Biblioteca externa] --> L[skill-loader e library_query.py]
  L --> H
  EV[Casos e traces externos] --> G[scripts/evals.py]
  CI[GitHub Actions] --> UT[unittest e doctors]
```

## Atual 2 — Dependências entre skills

```mermaid
flowchart LR
  PRE[pre-code] --> EX[execution]
  AU[audit] --> EX
  EX --> RE[release]
  AU --> RE
  PRE -. consulta .-> W[writing]
  EX -. consulta .-> W
  RE -. consulta .-> W
  W -. estilo solicitado .-> HU[humanizer]
  PRE -. Quarto .-> Q[quarto-expert]
  EX -. Quarto .-> Q
  Q -. texto .-> W
  L[skill-loader] -. lacuna .-> ESP[Especialista externo]
```

## Atual 3 — Descoberta e ativação

```mermaid
flowchart LR
  SEL[Seleção explícita na instalação] --> ROOT[Raiz reconhecida pelo host]
  ROOT --> META[Nome e descrição]
  META --> MATCH[Seleção pelo agente ou usuário]
  MATCH --> BODY[Leitura do SKILL.md]
  BODY --> REF[Referências necessárias]
  GAP[Capacidade ausente] --> LOAD[Loader consulta índice delimitado]
  LOAD --> MAN[Confere caminho e identidade]
  MAN --> BODY
```

## Atual 4 — Fluxo de execução

```mermaid
flowchart TD
  REQ[Pedido] --> MODE{Trabalho}
  MODE -->|novo| PRE[Planejar cinco gates]
  MODE -->|legado| AU[Reconhecer e diagnosticar]
  AU --> STOP[Parecer sem implementação]
  AU --> PLAN[Plano de refatoração]
  PRE --> OK[Plano e implementação autorizados]
  PLAN --> OK
  OK --> EX[Implementar fatias e verificar]
  EX --> REL[Preparar release]
  REL --> AUTH{Publicação autorizada}
  AUTH -->|sim| PUB[Publicar e smoke]
  AUTH -->|não| READY[Resultado preparado]
```

## Atual 5 — Handoffs e gates

```mermaid
flowchart LR
  G1[Descoberta] --> G2[Escopo]
  G2 --> G3[Arquitetura]
  G3 --> G4[Scaffold]
  G4 --> G5[Plano]
  G5 --> AP{Aceite e autorização}
  AP --> E[Execução lógica e integração]
  E --> V[Saída documentação e revisão]
  V --> A2{Aceite real}
  A2 --> R[Release com autorização própria]
  M[Assistido ou contínuo] -. regula avanços .-> AP
```

## Atual 6 — Distribuição multiagente

```mermaid
flowchart TD
  PK[Pacotes na raiz] --> CA[Catálogo release 1.0.1]
  CA --> SE[Skills bundles e exclusões]
  SE --> VA[Validação e preflight]
  VA --> ST[Staging e recibo por pacote]
  ST --> CO[Codex .agents/skills]
  ST --> CL[Claude .claude/skills]
  ST --> AG[Antigravity .agents/skills]
  ST --> CU[Destino customizado]
  SE --> MA[Manifest de caminhos opcional]
```

## Atual 7 — Persistência e retomada

```mermaid
flowchart LR
  RUN[Tarefa em um host] --> TS[Seção da pipeline em task.md]
  RUN --> ART[Artefatos e contratos no projeto]
  TS --> RES[Retomada da aprovação válida]
  ART --> RES
  RES --> CHECK[Conferir base diferenças e pendências]
  CHECK --> NEXT[Próxima tarefa autorizada]
  CLI[Instalador] --> REC[Recibo separado de instalação]
```

## Proposta 1 — Componentes futuros

```mermaid
flowchart TD
  HOST[Descoberta nativa do host] --> SK[Oito skills preservadas]
  SK --> POL[Política proporcional em referências necessárias]
  SK --> HC[Handoff mínimo em task.md]
  SK --> RV[Referência de revisão e review nativo]
  CLI[CLI atual] --> VAL[Validação de fronteiras alinhada]
  EV[Harness atual] --> COV[Cobertura e telemetria explícitas]
  COV --> AB[Comparação de traces A/B]
  SEC[Checklist de segurança por risco] -. consulta .-> SK
```

## Proposta 2 — Desenvolvimento

```mermaid
flowchart LR
  PED[Pedido e risco] --> CT[Contrato existente ou planejamento necessário]
  CT --> AP[Escopo e autorização registrados]
  AP --> SL[Fatia mínima]
  SL --> TEST[Testes de resultado]
  TEST --> REV[Revisão do diff e docs afetados]
  REV --> ACE[Aceite verificável]
  ACE --> REL[Release quando solicitada]
```

## Proposta 3 — Auditoria e refatoração

```mermaid
flowchart LR
  A[Inspeção e baseline] --> F[Achados com evidência]
  F --> ROAD[Fatias MOD priorizadas]
  ROAD --> AP{Tarefa explicitamente aprovada}
  AP --> OWN[Escolher auditoria ou execução como dona]
  OWN --> CHAR[Caracterização pertinente]
  CHAR --> PATCH[Mudança mínima]
  PATCH --> VAL[Validação e docs afetados]
  VAL --> WAIT[Aguardar autorização da próxima tarefa]
```

## Proposta 4 — Revisão de PR

```mermaid
flowchart LR
  ID[PR e revisão head] --> SCOPE[Diff e contratos afetados]
  SCOPE --> READ[Revisão diagnóstica sem escrita]
  READ --> FIND[Achados acionáveis com localização]
  FIND --> AP{Correção ou comentário autorizado}
  AP --> FIX[Aplicar ação delimitada]
  FIX --> TEST[Checks e novo diff]
  TEST --> REREV[Revisar head final]
```

## Proposta 5 — Avaliação A/B

```mermaid
flowchart LR
  PIN[Fixar base host modelo e cenários] --> A[Executar baseline isolada]
  PIN --> B[Executar candidata isolada]
  A --> TRACE[Traces e proveniência]
  B --> TRACE
  TRACE --> SCH[Validar contrato e cobertura]
  SCH --> RUB[Critérios observáveis e revisão]
  RUB --> COMP[Qualidade custo e estabilidade]
  COMP --> DEC[Aceitar rejeitar ou repetir]
```

## Proposta 6 — Carregamento seletivo

```mermaid
flowchart TD
  META[Metadados nativos] --> SEL{Capacidade suficiente}
  SEL -->|sim| MIN[Usar host e contrato existente]
  SEL -->|não| SK[Selecionar skill pertinente]
  SK --> GAP{Lacuna restante}
  GAP -->|sim| IDX[Busca limitada na biblioteca]
  IDX --> VALID[Frontmatter e confinamento válidos]
  VALID --> READ[Uma referência necessária]
  READ --> DEDUP[Registrar caminho já lido]
  GAP -->|não| RUN[Executar escopo autorizado]
  DEDUP --> RUN
```

## Proposta 7 — Código, contratos, docs e testes

```mermaid
flowchart LR
  REQ[Requisito aprovado] --> CONTR[Contrato público]
  CONTR --> CODE[Código implementado]
  CONTR --> TEST[Testes de comportamento]
  CODE --> OBS[Resultado observado]
  TEST --> OBS
  OBS --> DOC[Documentação de uso afetada]
  CONTR --> DOC
  DIS[Divergência] --> DEC[Investigar e decidir com autorização]
  OBS --> DIS
  DEC --> CONTR
```

## Comparação e trade-offs

| Aspecto | Atual | Proposto | Custo e alternativa descartada |
|---|---|---|---|
| Roteamento | Metadados e critérios de cada skill | Casos negativos/discriminantes e limites refinados por evidência | Mais avaliações; descartar roteador central sem lacuna medida |
| Gates | Cinco gates em pipelines; contratos documentais nomeados | Mesmos controles com evidência proporcional por referência | Exige mudar contrato sob aprovação; não apagar rastreabilidade |
| Handoff | Instrucional e task.md | Campos mínimos, base/autoridade e dono da fatia | Pequena disciplina; descartar banco/framework de estado |
| Documentação | Fontes + propostas/histórico | Propriedade e precedência explícitas | Preservar cópias históricas, não deduplicar por exclusão |
| Revisão | Gate 5 e capacidades do host | Referência e modo diagnóstico por escopo | Pode faltar interface uniforme entre hosts; testar antes de nova skill |
| Avaliações | Classificador de traces fornecidos | Contratos robustos, cobertura e métricas observadas | Captura externa continua necessária; não prometer execução automática |
| Segurança | Limites instrucionais, filesystem e CI | Validar entradas e checklist por risco | Sandbox real continua do host; checklist não certifica segurança |
| Distribuição | Cópia/link com recibo | Preservar; hardening de CI e falhas por pacote | SHAs exigem manutenção; transação global adiada sem necessidade comprovada |
