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
3. O nível padrão é `leitura`. `execucao` roda um agente real e custa bem mais; use antes de release, nos cenários das skills alteradas.
4. Mostre a lista, o nível e quantos agentes vão rodar, e espere o aceite.

## Rodar no nível de leitura

- Agrupe até dois cenários por agente e rode no máximo quatro agentes em paralelo, com o subagente `skill-prober`.
- Para cada agente, passe o pedido literal, a raiz do repositório como pasta das skills instaladas, os checkpoints do cenário e a versão que está sendo avaliada.
- Quando a mudança envolve skills oficiais de terceiros, diga ao agente que elas não estão disponíveis e que ele avalia só se o apontamento é claro.

## Rodar no nível de execução

- Copie a fixture do cenário, ou uma pasta vazia, para o scratchpad da sessão. Nunca use credenciais, contas nem destinos reais.
- Carregue as skills sem trocar os plugins do usuário: uma cópia do repositório com o marketplace renomeado, ligada por `claude -p --settings <arquivo>` com `extraKnownMarketplaces` e `enabledPlugins`. Isso grava a entrada do marketplace de teste no registro do usuário; remova-a no fim com `claude plugin marketplace remove <nome>` e confira que os plugins dele continuam iguais.
- Rode `claude -p` com o cwd na cópia da fixture, o pedido, `--max-turns 40`, `--output-format stream-json --verbose` e permissões padrão, de modo que todo efeito externo seja negado e fique visível no registro.
- Avalie os checkpoints pelo registro: as ferramentas chamadas, o que foi negado e as paradas para aceite.

## Gravar e comparar

- Grave um JSON por cenário em `evals/results/<versão>/<nível>/<id>.json`, no formato do README, com host, modelo exato, data, paradas, contexto lido e a evidência de cada checkpoint. A versão é a das skills avaliadas: a da tag, ou a que vai ser publicada.
- Rode `/usr/bin/python3 -m unittest tests.test_evals` para conferir o formato.
- Compare com a última versão publicada em `evals/results/`: um checkpoint que passava e agora falha é regressão. Rode `/usr/bin/python3 evals/report.py` para a tabela.
- Confira você mesmo, no texto atual, cada falha antes de propor uma correção: o agente pode ter lido errado.
- Proponha as correções e espere o aceite do usuário antes de editar as skills.
