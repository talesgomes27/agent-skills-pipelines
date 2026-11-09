---
name: cenarios
description: Roda os cenários de comportamento de evals/scenarios/ com agentes novos, grava os resultados em evals/results/ e compara com a última versão publicada. Use depois de mudar uma skill, antes do commit, e antes de cada release.
disable-model-invocation: true
argument-hint: "[nomes dos cenários, 'mudados' ou 'todos'] [leitura|execucao]"
---

# Cenários de comportamento

Testa se as skills deste repositório levam um agente ao comportamento esperado em pedidos reais. O formato dos cenários e dos resultados está em `evals/README.md`. Nada nas skills é editado durante a rodada.

## Escolher

1. Leia `evals/scenarios/*.yaml`.
2. Com `mudados` ou sem argumento, rode `git diff --name-only main` e `git ls-files --others --exclude-standard` e proponha só os cenários cujas `skills_esperadas` mudaram. Com `todos`, use todos. Com nomes, use esses.
3. Rode cada cenário no modo padrão, por efeito, e também no assistido quando a mudança mexe em modos, aceites ou no contrato comum. No assistido, diga ao agente que o `AGENTS.md` do projeto tem `Modo: assistido`. O nível padrão é `leitura`. `execucao` roda um agente real e custa bem mais; use antes de release, nos cenários das skills alteradas.
4. Mostre a lista, o nível e quantos agentes vão rodar, e espere o aceite.

## Rodar no nível de leitura

- Agrupe até dois cenários por agente e rode no máximo quatro agentes em paralelo, com o subagente `skill-prober`.
- Para cada agente, passe o pedido literal, a raiz do repositório como pasta das skills instaladas, os checkpoints do cenário e a versão que está sendo avaliada.
- Quando a mudança envolve skills oficiais de terceiros, diga ao agente que elas não estão disponíveis e que ele avalia só se o apontamento é claro.

## Rodar no nível de execução

O harness é `scripts/execucao.py`, só com a biblioteca padrão. Rode `/usr/bin/python3 .claude/skills/cenarios/scripts/execucao.py` sem argumentos para ver os comandos. Nunca use credenciais, contas nem destinos reais.

- Para uma rodada inteira, use `lote <pasta> --cenarios a,b --gatilhos c,d|todos --amostras N`. Ele monta o plugin de teste em `<pasta>/plugin`, prepara e roda cada execução nos dois destinos, quatro de cada vez, e retoma numa nova chamada as que ficaram sem `done`. Depois, `contar <pasta> --contra <versão anterior>` dá os gatilhos certos por destino, com o resultado da versão anterior ao lado, e as skills carregadas em cada cenário. Os comandos abaixo são as peças do `lote`, para uma execução avulsa.
- Monte o plugin de teste uma vez por rodada com `plugin <pasta no scratchpad>`. Ele copia todas as skills, os subagentes de `plugin-agents/` e o hook do `pipeline-guardrails` para um plugin `asp`, carregado por `--plugin-dir` sem tocar os plugins do usuário.
- Para cada execução, rode `preparar <exec> "<pedido>" [<fixture do cenário>]` e depois `rodar <exec> <destino>`:
  - destino `claude-code`, com `--plugin <pasta>/asp`;
  - destino `claude-code-instalador`: o harness instala as skills na cópia com `skills.py install --scope project --all --mode copy` e roda sem o plugin. O escopo `project` não toca o `~/.claude/skills/` do usuário. Esse destino não tem os subagentes nem o hook do `pipeline-guardrails`: o que falhar por falta deles é limite do destino, não da skill.
- Os dois destinos rodam o mesmo `claude -p`:
  - Sonnet, `--setting-sources project` e `--strict-mcp-config`;
  - `--permission-mode acceptEdits`, com uma allowlist só de leitura e do pytest;
  - 40 turnos e teto de US$ 1,50.

  Todo efeito externo é negado e fica visível no registro. Em gatilhos, use `--turnos 8`.
- Na primeira execução de cada destino, confira na linha INIT do `resumo` que só aparecem as skills do repositório e as do próprio Claude Code. Se aparecerem as do usuário, pare e diga ao usuário.
- Se o cenário tem `aceite_simulado`, passe `--aceite "<texto>"`. Depois de um primeiro turno terminado com sucesso, o harness retoma a mesma sessão com `--resume` e grava `log2.jsonl`; se o primeiro turno estourou turnos ou orçamento, grava `aceite_pulado` no lugar.
- Rode até quatro execuções em paralelo, em segundo plano. Uma execução que termina em erro da API, como o limite de uso da conta, grava `erro_api` em vez de `done`; prepare a execução de novo, porque a cópia do projeto pode ter sido editada, e não a conte como `nao_ativou`. Mudança de skill usa três amostras por destino, e diferença pequena entre destinos usa dez.
- Alternativa oficial para gatilhos no marketplace: o `claude plugin eval`, com um caso por gatilho e o grader `tool_used: Skill` (`min: 0` e `max: 0` para um "não deve"), rodado com `--ablation none`, `-j 4` e `--no-publish`, que mantém o relatório local. Num piloto em 2026-11-08, ele deu os mesmos 24 de 24 do `lote` em 8 gatilhos, mais rápido e com o custo por caso. Ele não cobre o destino `claude-code-instalador` e só copia fixture com `--scaffold`, que roda bash; por isso o `lote` continua sendo o padrão.
- Gatilho: prepare com a `fixture` do gatilho, quando houver, rode com `--turnos 8` e classifique com `gatilho <log> <skill>`, que devolve `ativou`, `nao_ativou` ou `outra`.
- Julgue com o subagente `juiz-cenarios`, até quatro cenários por juiz, passando as execuções, a versão, o destino e a pasta de saída; ele segue o [roteiro do juiz](roteiro-juiz.md). Ele roda em Sonnet: em 74 checkpoints julgados pelos dois modelos em 2026-11-09, concordou com o Opus em 71, e as três diferenças foram entre passou e indeterminado. Um segundo `juiz-cenarios`, no modo cego, revê as falhas no modelo da sessão; para isso, passe o modelo ao chamá-lo, porque o do frontmatter é o Sonnet.

## Gravar e comparar

- Grave um JSON por cenário e modo em `evals/results/<versão>/<nível>/<id>.json` no modo padrão, ou `<id>--<modo>.json` com o campo `modo` nos outros, numa subpasta `<destino>/` com o campo `destino` quando não é o destino padrão do host, no formato do README, com host, modelo exato, data, paradas, contexto lido e a evidência de cada checkpoint. A versão é a das skills avaliadas: a da tag, ou a que vai ser publicada.
- Rode `/usr/bin/python3 -m unittest tests.test_evals` para conferir o formato.
- Compare com a última versão publicada em `evals/results/`: um checkpoint que passava e agora falha é regressão. Rode `/usr/bin/python3 evals/report.py` para a tabela.
- Confira você mesmo, no texto atual, cada falha antes de propor uma correção: o agente pode ter lido errado.
- Proponha as correções e espere o aceite do usuário antes de editar as skills.
