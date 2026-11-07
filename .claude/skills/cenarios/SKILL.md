---
name: cenarios
description: Roda os cenários de comportamento de docs/distribution/discovery.md com agentes novos e compara com a rodada anterior. Use depois de mudar uma skill, antes do commit.
disable-model-invocation: true
argument-hint: "[nomes dos cenários, 'mudados' ou 'todos']"
---

# Cenários de comportamento

Testa se as skills deste repositório levam um agente ao comportamento esperado em pedidos reais. Só lê: nada é editado durante a rodada.

## Escolher os cenários

1. Leia a tabela "Cenários de comportamento" em `docs/distribution/discovery.md`.
2. Com o argumento `mudados` ou sem argumento, rode `git diff --name-only main` e `git ls-files --others --exclude-standard` e proponha só os cenários cujas skills mudaram. Com `todos`, use a tabela inteira. Com nomes, use esses.
3. Mostre ao usuário a lista e quantos agentes vão rodar, e espere o aceite: cada cenário custa um agente.

## Rodar

- Agrupe até dois cenários por agente e rode no máximo quatro agentes em paralelo, com o subagente `skill-prober`.
- Para cada agente, passe: os pedidos literais da tabela, a raiz do repositório como pasta das skills instaladas e a coluna "O que conferir" como foco.
- Quando a mudança envolve skills oficiais de terceiros, diga ao agente que elas não estão disponíveis e que ele avalia só se o apontamento é claro.

## Comparar e relatar

- Para cada cenário: o que a skill agora faz certo, o que falta, o que conflita e o que pesa demais, com o arquivo e o trecho que o agente citou.
- Separe o que é processo, e cabe nas pipelines, do que é conhecimento de ferramenta, que vai para skill oficial ou especialista.
- Compare com a rodada anterior quando ela estiver na conversa ou na memória do projeto. Não grave o relatório no repositório.
- Confira você mesmo, no texto atual, cada lacuna antes de propor uma correção: o agente pode ter lido errado.
- Proponha as correções e espere o aceite do usuário antes de editar.
