# Verificação de descoberta

Ter a skill instalada em disco não prova que o agente a encontra. Depois de instalar ou atualizar:

1. Rode `doctor` no destino para validar estrutura, integridade e versão registrada.
2. Recarregue o host ou abra uma sessão nova.
3. Confira no catálogo do host o nome, a descrição e o caminho das skills instaladas.
4. Envie prompts de `evals/triggers.yaml`, pelo menos um "deve ativar" e um "não deve ativar" por skill, e veja se o host carregou a skill esperada.

## Estado observado

| Host | Destino | Evidência | Estado |
|---|---|---|---|
| Codex Desktop | `~/.agents/skills/` | Em 2026-10-22, o catálogo da sessão exibiu as skills instaladas do repositório | verificado para descoberta |
| Claude Code, pelo marketplace | Cache de plugins | Em 2026-11-07, uma sessão nova listou as oito skills instaladas, todas menos a `skill-loader`, com o prefixo do plugin, como `pre-code-pipeline:pre-code-pipeline` | verificado para descoberta |
| Claude Code, pelo instalador | `~/.claude/skills/` | Nenhuma sessão compatível foi usada | pendente |
| Antigravity App/IDE | `~/.gemini/config/skills/` | Nenhuma sessão compatível foi usada | pendente |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/` | Nenhuma sessão compatível foi usada | pendente |

Atualize a data e a evidência sempre que repetir o teste em um host.

## Prompts de gatilho

Os prompts ficam em [`evals/triggers.yaml`](../../evals/triggers.yaml), com a skill e o resultado esperado: deve ativar, caso ambíguo que deve ativar, ou não deve ativar. Os casos ambíguos testam a fronteira entre skills. Quando um prompt ativar a skill errada, ajuste a `description` da skill, não o arquivo. Grave o que cada host observou em `evals/results/<versão>/<nível>/triggers-<destino>.json`, no formato de [`evals/README.md`](../../evals/README.md).

## Cenários de comportamento

Os prompts de gatilho conferem só a descoberta. Para conferir o comportamento depois de mudar uma skill, use os cenários de [`evals/scenarios/`](../../evals/scenarios/) com a skill `/cenarios`. Rode o mesmo cenário antes e depois da mudança e compare os resultados guardados em `evals/results/`.
