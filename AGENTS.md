# Instruções para agentes neste repositório

Este repositório é uma biblioteca de Agent Skills em português, distribuída como marketplace de plugins do Claude Code e pelo instalador `scripts/skills.py`.

## Ambiente

- Use `/usr/bin/python3`: o `python3` do PATH pode não ter o PyYAML 6.0.3.
- Validação: `/usr/bin/python3 -m unittest discover -s tests`, `/usr/bin/python3 scripts/skills.py doctor` e `claude plugin validate --strict .`.
- No zsh, escreva `${var}` antes de dois-pontos, como em `git show "${c}:caminho"`; `$c:q` vira um modificador e corta o caminho.

## Regras das skills

- Um `SKILL.md` tem no máximo 10.000 caracteres, e o doctor recusa acima disso. Detalhe vai para `references/` sem perder regra; confira com o subagente `rule-keeper` antes de commitar.
- A `description` diz só quando usar a skill e começa por "Use quando".
- O fluxo padrão das pipelines é por efeito, com os aceites A1, A2 e A3 do contrato comum. Regra de aceite, catálogo de efeitos ou spec viva muda em `shared/common-contract.md`, seguida de `/usr/bin/python3 scripts/skills.py sync-shared`.
- Antes de escrever conhecimento de uma ferramenta, procure a skill oficial do fabricante e aponte para ela. Escreva só o que nenhuma cobre.
- Fato de terceiros (plataforma, biblioteca, lei) é conferido na documentação oficial, com o link na referência.
- Não reintroduza registros de estado nem auditorias no repositório. Avaliações ficam em `evals/`, como cenários declarativos e resultados por versão; nada de framework próprio nem dependência nova.
- Mudança de comportamento é testada com os cenários de `evals/scenarios/`, antes e depois, pela skill `/cenarios`.

## Fluxo de trabalho

- Uma branch por mudança. Commit, push, PR e merge só com o aceite do usuário.
- O merge usa `gh pr merge --merge --match-head-commit <commit testado>`, depois que os checks obrigatórios do ruleset passam. Não acompanhe a CI em loop.
- Uma issue "A skill errou" aceita vira primeiro um cenário em `evals/scenarios/`, rodado pelo `/cenarios` para mostrar a falha na versão atual. O cenário e a correção entram no mesmo PR.
- Release segue a skill `/preparar-release`. Pelo SemVer, remover skill ou cortar o escopo de uma é MAJOR; skill, regra ou referência nova é MINOR; correção é PATCH.

## Ferramentas do Claude Code neste repositório

- Hooks em `.claude/settings.json`: o doctor roda depois de editar um `SKILL.md` ou uma referência, e testes e doctor rodam ao fim de cada turno enquanto houver mudança não commitada em skills, catálogo, scripts ou testes.
- Skills: `/cenarios` e `/preparar-release`. Subagentes: `skill-prober` e `rule-keeper`.
