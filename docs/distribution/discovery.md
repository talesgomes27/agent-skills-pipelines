# Verificação de descoberta

Ter a skill instalada em disco não prova que o agente a encontra. Depois de instalar ou atualizar:

1. Rode `doctor` no destino para validar estrutura, integridade e versão registrada.
2. Recarregue o host ou abra uma sessão nova.
3. Confira no catálogo do host o nome, a descrição e o caminho das skills instaladas.
4. Envie prompts de `evals/triggers.yaml`, pelo menos um "deve ativar" e um "não deve ativar" por skill, e veja se o host carregou a skill esperada.

## Estado observado

| Host | Destino | Evidência | Estado |
|---|---|---|---|
| Codex Desktop | `~/.agents/skills/` | Em 2026-10-22, o catálogo da sessão exibiu as skills instaladas do repositório, na 3.x. Não reverificado desde a 4.0.0 | verificado para descoberta na 3.x |
| Claude Code, pelo marketplace | Cache de plugins | Em 2026-11-14, na 5.0.0 (Claude Code 2.1.325), o catálogo de uma sessão do usuário listou as dez skills com o prefixo do plugin, como `planning-pipeline:planning-pipeline`. Com muitos plugins instalados, o catálogo mostrou seis delas sem a `description`. O comportamento foi medido no destino `claude-code` do `/cenarios`, que usava uma cópia de teste num plugin único (`asp`, por `--plugin-dir`) e não a instalação do marketplace; desde 2026-11-16 a cópia tem um plugin por entrada do marketplace, com os nomes da instalação real: 51 dos 57 gatilhos certos, sem disparo nos casos "não deve" (`evals/results/5.0.0/execucao/triggers-claude-code.json`). Em 2026-11-17, na 5.1.1, com pastas de execução neutras, um plugin por entrada do marketplace e 5 amostras: 46 dos 53 gatilhos contados certos em todas as amostras, 245 de 261 amostras certas, nenhum disparo em "não deve" (`evals/results/5.1.1/execucao/triggers-claude-code.json`) | verificado para descoberta; comportamento medido com a cópia de teste |
| Claude Code, pelo instalador | `.claude/skills/` do projeto (escopo `project`); o escopo `user` usa `~/.claude/skills/` e não foi testado | Em 2026-11-14, na 5.0.0, `claude -p --setting-sources project` com as dez skills instaladas pelo `skills.py`, sem prefixo: 53 dos 57 gatilhos certos, sem disparo nos casos "não deve" (`evals/results/5.0.0/execucao/triggers-claude-code-instalador.json`). Em 2026-11-17, na 5.1.1, com pastas neutras e 5 amostras: 50 dos 53 certos em todas as amostras, 254 de 261 amostras certas, nenhum disparo em "não deve" (`evals/results/5.1.1/execucao/triggers-claude-code-instalador.json`). Esse destino não traz os subagentes de `plugin-agents/` nem o hook do `pipeline-guardrails` | verificado para descoberta e comportamento |
| Antigravity App/IDE | `~/.gemini/config/skills/` | Nenhuma sessão compatível foi usada | pendente |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/` | Nenhuma sessão compatível foi usada | pendente |

Atualize a data e a evidência sempre que repetir o teste em um host. Um destino sem resultado gravado está "não testado", o que não quer dizer suportado.

Na 5.0.0, a descoberta está verificada em 2 dos 5 destinos, os dois do Claude Code. Todos os resultados de gatilho desde a 4.0.0 usam o mesmo modelo (`claude-sonnet-5-5`). Até a 5.1.0, as pastas de execução levavam o id do gatilho, muitas vezes com o nome da skill, e o `claude` vê esse caminho: esses acertos estão inflados. A partir da 5.1.1, as pastas são neutras. Por decisão do mantenedor em 2026-11-08, os testes rodam por enquanto só no Claude Code.

As rodadas isolam o ambiente (`--setting-sources project`, `--strict-mcp-config`). Assim, elas não medem o efeito de um catálogo cheio de outros plugins. No Claude Code, a lista de skills tem um orçamento de 1% da janela de contexto, e, quando ele estoura, o host tira primeiro as descrições das skills menos invocadas, mantendo só o nome ([documentação](https://code.claude.com/docs/en/skills#skill-descriptions-are-cut-short), conferida em 2026-11-15). Uma instalação nova, que ainda não usou estas skills, é a primeira a perder as descrições. O `/doctor` estima o custo da lista, e `skillListingBudgetFraction` ou `skillOverrides` com `"name-only"` abrem espaço; o README traz o mesmo aviso.

## Prompts de gatilho

Os prompts ficam em [`evals/triggers.yaml`](../../evals/triggers.yaml), com a skill e o resultado esperado: deve ativar, caso ambíguo que deve ativar, não deve ativar, ou opcional, quando ativar ou não são ambos aceitáveis. Os casos ambíguos testam a fronteira entre skills. Quando um prompt ativar a skill errada, ajuste a `description` da skill, não o arquivo. Grave o que cada host observou em `evals/results/<versão>/<nível>/triggers-<destino>.json`, no formato de [`evals/README.md`](../../evals/README.md).

## Cenários de comportamento

Os prompts de gatilho conferem só a descoberta. Uma pipeline que ativou segue, por padrão, o fluxo por efeito do [contrato comum](../../shared/common-contract.md): para no A1 (escopo, requisitos e efeitos previstos), num A2 antes de cada efeito do catálogo, como push, deploy ou instalação, e no A3 (entrega com evidência), além das paradas condicionais; `Modo: assistido` no pedido ou no `AGENTS.md` do projeto volta às paradas por gate. Para conferir o comportamento depois de mudar uma skill, use os cenários de [`evals/scenarios/`](../../evals/scenarios/) com a skill `/cenarios`. Rode o mesmo cenário antes e depois da mudança e compare os resultados guardados em `evals/results/`.
