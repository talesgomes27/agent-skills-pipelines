# pipeline-guardrails

Plugin opcional do Claude Code que pede confirmação antes das formas comuns de quatro efeitos do catálogo das pipelines (contrato comum, seção "Catálogo de efeitos que pedem A2"): push, tag, PR e merge; deploy e publicação; migração de banco; e instalação de dependência. Os outros efeitos do catálogo, como escrever dados reais, enviar mensagem, enviar dados a terceiros, gastar dinheiro, alterar arquivos fora do escopo e criar credencial, não têm forma de comando reconhecível e ficam só com as regras das skills. Ele só escala para o usuário e nunca libera: uma autorização que o agente grava no `task.md` não desliga nada, porque o agente poderia escrevê-la.

## Duas camadas

1. **Regras de permissão.** Copie `settings-template.json` para o `.claude/settings.json` do projeto, ou junte as listas às suas. As regras são avaliadas na ordem deny, ask e allow, e uma regra `ask` pergunta mesmo quando uma `allow` mais específica também casa. O limite é que uma regra de Bash compara o começo do comando: `Bash(git push *)` não pega `git -C . push`.
2. **Hook `PreToolUse`.** O plugin traz `hooks/hooks.json`, que roda `scripts/effect_guard.py` antes de cada comando das ferramentas Bash e PowerShell. O script procura os padrões de `effects.json` em qualquer ponto do comando, o que pega `git -C . push`, `cd app && git push`, `env X=1 git push` e `bash -c "git push"`, além de escritas no repositório pela API do GitHub com `gh api` ou `curl` (conteúdo, refs, dispatches e mutations como `createRef`), e devolve `permissionDecision: "ask"`. Sem achado, não decide, e as permissões normais seguem.

O hook usa `onFailure: "block"`: se o script falhar, o comando é bloqueado em vez de passar. Isso exige o Claude Code v2.1.295 ou mais novo e um `python3` no PATH. Numa máquina sem `python3`, todo comando Bash fica bloqueado até você desativar o plugin com `claude plugin disable pipeline-guardrails`.

## Instalar

```bash
claude plugin install pipeline-guardrails@agent-skills-pipelines
```

O pacote `completo` já o inclui. O `scripts/skills.py` não o instala, porque ele não é uma skill.

## O que fica de fora

O hook pega as formas comuns, não todas. Ele não vê o que roda dentro de um script intermediário (`./deploy.sh`, um alvo de `make` ou um script de `npm run` com outro nome), comando ofuscado (`eval` de texto decodificado) nem ferramenta fora da lista de `effects.json`. Também não pergunta em `npm ci` e `uv sync`, que instalam o que o lock já fixou. Ele é uma segunda linha: a primeira continua sendo a regra das skills e o aceite do usuário.

- Em `claude -p`, sem ninguém para responder, um `ask` vira recusa, e o agente lê o motivo no resultado da ferramenta. Por isso, um agente sem supervisão que trabalha com PR como gate não consegue fazer push nem abrir o PR com o plugin ativo: nesse ambiente, desative o plugin ou aceite que o agente pare antes desses efeitos. A documentação não diz o que acontece com o modo `bypassPermissions`. Não use esse modo contando com o plugin.
- As regras `deny` do modelo comparam o começo do comando. Elas pegam `git push --force`, `-f` e `--force-with-lease` nessa posição, mas não `git push origin main --force` nem `+main`; essas formas ficam para o hook, que pergunta.
- Falsos positivos: o padrão também casa com `git log --grep=push`, com `git tag -l` e com uma mensagem de commit que cite "push". O custo é uma confirmação a mais.
- Commit não pede confirmação no hook, para não perguntar a cada commit numa branch de trabalho; ele continua no catálogo das skills.
- Conectores MCP que publicam ou enviam não passam pelo Bash. Para cobri-los, acrescente no seu `.claude/settings.json` uma regra `ask` ou um hook com matcher pelo nome da ferramenta, no formato `mcp__<servidor>__.*`.

## Outros hosts

O hook é do Claude Code. Nos outros hosts, use o modo de aprovação que pede confirmação antes de comandos, e `effects.json` documenta o que confirmar:

- Codex: a política de aprovação `on-request`, ou `trust_level = "untrusted"` no projeto para confirmar cada comando. O valor `untrusted` da política de aprovação foi aposentado.
- Antigravity: a política de terminal Require Review, com as listas Allow e Deny.

Fontes, conferidas em 07/11/2026: [hooks](https://code.claude.com/docs/en/hooks), [permissões](https://code.claude.com/docs/en/permissions), [aprovações do Codex](https://learn.chatgpt.com/docs/agent-approvals-security) e [configurações do agente no Antigravity](https://antigravity.google/docs/agent-settings).
