# Formatos de SDD existentes

Antes de criar `docs/spec.md`, confira se o projeto já usa Spec Kit, Kiro ou OpenSpec. Se usar, a pipeline lê e escreve no formato dele e não cria uma segunda fonte de verdade.

## Detecção e mapeamento

| Ferramenta | Sinal no repositório | Requisitos | Design ou plano | Tarefas | Observação |
|---|---|---|---|---|---|
| Spec Kit | `.specify/` e `specs/<funcionalidade>/spec.md` | `spec.md`: histórias "User Story N", requisitos `FR-001` e critérios de sucesso `SC-001` | `plan.md` | `tasks.md`: `T001`, `[P]` para paralelizável e `[US1]` para a história | A constitution do projeto entra como restrição |
| Kiro | `.kiro/`, com `requirements.md`, `design.md` e `tasks.md` de cada spec | `requirements.md`, com critérios no formato EARS: "WHEN [condição] THE SYSTEM SHALL [comportamento]" | `design.md` | `tasks.md` | Os arquivos de `.kiro/steering/` são convenções do projeto, como o `AGENTS.md` |
| OpenSpec | `openspec/specs/` e `openspec/changes/<mudança>/` | `specs/<domínio>/spec.md`: "### Requirement:" com cenários "#### Scenario:" (WHEN/THEN); a mudança traz deltas em "## ADDED Requirements", "## MODIFIED Requirements" e "## REMOVED Requirements" | `design.md`, com o porquê em `proposal.md` | `tasks.md` | Ao concluir, a mudança vai para `openspec/changes/archive/` |
| Nenhum | — | `docs/spec.md` | `docs/architecture.md` | `docs/plan.md` | O formato nativo da [spec viva](spec-template.md) |

## Regras

- O formato detectado vence: a pipeline não cria `docs/spec.md` em paralelo nem migra sem pedido.
- Arquivo da ferramenta não prova aprovação, como diz a seção "Spec viva" do contrato comum: uma spec ou um `tasks.md` só vale como plano aprovado com aceite do usuário que se possa conferir. Sem ele, a pipeline mostra o A1 (requisitos, tarefas e efeitos previstos) e espera o aceite antes de implementar.
- Se o formato não usa IDs, a pipeline não renomeia nada. Ela cita os requisitos pelo título, e o A3 lista os atendidos com os nomes da própria ferramenta.
- Os comandos da ferramenta, como implementar as tarefas ou arquivar uma mudança do OpenSpec, não substituem os aceites. Rodá-los é execução e segue as regras das pipelines, inclusive o catálogo de efeitos.
- Divergência entre código e spec continua sendo achado, em qualquer formato.
- Na entrega, a pipeline atualiza a spec no formato da ferramenta: no Spec Kit e no Kiro, os arquivos da funcionalidade; no OpenSpec, só os deltas da mudança em `openspec/changes/<mudança>/`, porque arquivar a mudança é o que leva os deltas para `openspec/specs/`.

## O que o `spec_check.py` confere

Com `--format auto`, ele detecta o formato nesta ordem: Spec Kit, Kiro, OpenSpec (só com arquivos em `openspec/specs/` ou `openspec/changes/`) e o nativo, que é conferido também quando outro formato vem antes. Com um formato de SDD pedido em `--format`, a spec nativa que existir também é conferida; se o formato pedido não existir, ele sai com 2. Nestes formatos ele não confere evidência, nem com `--stage a3`: a saída avisa, e o A3 lista a evidência de cada requisito.

- Spec Kit (detectado só com `.specify/`): as tarefas citam histórias (`[USn]`) e requisitos (`FR-` ou `SC-`) que existem na spec.
- Kiro: cada pasta com `requirements.md` tem também `design.md` e `tasks.md`. Como o Kiro cria esses arquivos por fase, o trio incompleto só vira problema com `--stage a3`; antes disso aparece como em andamento.
- OpenSpec: todo "### Requirement:" fora de uma seção REMOVED tem ao menos um "#### Scenario:", e cada mudança em andamento tem `proposal.md` e `tasks.md`; como no Kiro, a mudança incompleta só vira problema com `--stage a3`.

## Limites da conferência

Os caminhos e convenções mudam entre versões das ferramentas; confira na documentação da versão em uso.

- Spec Kit: os IDs de requisito, critério, tarefa e história estão nos modelos oficiais. A pasta exata de `constitution.md` não foi confirmada na documentação lida.
- Kiro: o formato EARS e o trio de arquivos foram confirmados. Não foram confirmados a pasta `.kiro/specs/`, a numeração dos critérios nem a forma como as tarefas citam requisitos. Por isso o verificador procura o trio em qualquer pasta de `.kiro/`.
- OpenSpec: a documentação diz que cada requisito tem cenários, sem dizer se isso é obrigatório. O exemplo de REMOVED não traz cenário.

Fontes, conferidas em 07/11/2026: [modelo de spec do Spec Kit](https://raw.githubusercontent.com/github/spec-kit/main/templates/spec-template.md), [modelo de tarefas do Spec Kit](https://raw.githubusercontent.com/github/spec-kit/main/templates/tasks-template.md), [specs no Kiro](https://kiro.dev/docs/specs/feature-specs/), [steering no Kiro](https://kiro.dev/docs/steering/), [conceitos do OpenSpec](https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/docs/concepts.md) e [README do OpenSpec](https://raw.githubusercontent.com/Fission-AI/OpenSpec/main/README.md).
