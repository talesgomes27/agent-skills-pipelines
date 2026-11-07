# Guia de instalação

As skills ficam cada uma numa pasta da raiz do repositório. O catálogo em `distribution/catalog.json` diz quais existem, a release e os bundles, e o instalador `scripts/skills.py` copia ou liga as escolhidas na pasta que o host lê. No Claude Code, o caminho mais simples é o marketplace de plugins, descrito no [README](../../README.md#claude-code).

## Requisitos

Python 3.9 ou mais novo e PyYAML 6.0.3. O instalador não baixa nada da rede e não executa scripts das skills.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r distribution/requirements.txt
.venv/bin/python scripts/skills.py list
```

No Windows, use `py -3 -m venv .venv` e `.venv\Scripts\python.exe`; a CLI não precisa de bash. Nos exemplos abaixo, `python3` é o interpretador com PyYAML.

## Onde cada host procura as skills

| Host | Projeto | Usuário | Opção |
|---|---|---|---|
| Codex | `.agents/skills/` | `~/.agents/skills/` | `--agent codex` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | `--agent claude` |
| Claude Code, pelo marketplace | — | Cache de plugins | `.claude-plugin/marketplace.json`, um plugin por skill |
| Antigravity App/IDE | `.agents/skills/` | `~/.gemini/config/skills/` | `--agent antigravity` |
| Antigravity CLI | `.agents/skills/` | `~/.gemini/antigravity-cli/skills/` | `--agent antigravity-cli` |
| Outro framework | Pasta explícita | Pasta explícita | `--destination PATH` |

O padrão é a pasta do projeto atual; `--scope user` instala no perfil. Os caminhos seguem a documentação de cada host: [Antigravity](https://antigravity.google/docs/skills/), [Claude Code](https://code.claude.com/docs/en/skills) e [OpenAI](https://learn.chatgpt.com/docs/build-skills). Instalações antigas do Codex em `~/.codex/skills` não são migradas nem apagadas. O Antigravity ainda aceita `.agent/skills`, mas o instalador usa `.agents/skills`. O Gemini CLI é outro produto e não tem opção aqui.

`--agent auto` tenta reconhecer a sessão do Codex ou do Claude Code e depois os executáveis `codex`, `claude` e `agy`. É uma estimativa, não prova de qual agente está ativo. Se encontrar mais de um candidato, ou nenhum, ele para antes de gravar e pede `--agent`. O Antigravity App/IDE nunca é detectado: use `--agent antigravity`. `detect` mostra o que ele encontrou. `--destination` ignora `--agent` e `--scope`.

## Escolher o que instalar

| Bundle | Skills |
|---|---|
| `planning` | `pre-code-pipeline` |
| `development` | `pre-code-pipeline`, `execution-pipeline`, `audit-and-refactoring-pipeline`, `scheduled-automation`, `personal-data` |
| `research` | `pre-code-pipeline`, `execution-pipeline`, `writing-pipeline`, `quarto-expert`, `personal-data` |
| `editorial` | `writing-pipeline` |
| `release` | `release-and-ops-pipeline` |
| `library` | `skill-loader` |

Bundles agrupam skills e mais nada; ferramentas e MCPs que uma skill cite você instala à parte. Dá para repetir `--bundle` e `--skill`, combiná-los e tirar nomes com `--exclude`. Instalar tudo exige `--all`.

```bash
# Ver o plano sem gravar nada
python3 scripts/skills.py install --agent codex --bundle development --dry-run

# Todas as skills no perfil do usuário, menos a skill-loader
python3 scripts/skills.py install --agent codex --scope user --all --exclude skill-loader

# Por link, para quem edita as skills e quer ver a mudança na hora
python3 scripts/skills.py install --agent antigravity --skill quarto-expert --mode link

# Pasta de outro framework, conferida pelo doctor
python3 scripts/skills.py install --destination /caminho/skills --bundle research
python3 scripts/skills.py doctor --destination /caminho/skills --bundle research
```

A cópia é o modo padrão e funciona em qualquer sistema. O link depende do suporte do sistema e não volta para cópia em silêncio. Um link expõe a pasta inteira do checkout vivo: mover ou apagar o clone quebra a instalação, e é preciso instalar de novo.

Cada skill instalada aparece com nome e descrição no catálogo do host, e o `SKILL.md` e as referências só são lidos quando a tarefa pede. Quanto isso ocupa de contexto depende do host, e tirar uma skill do catálogo não apaga o que o agente já leu numa conversa. Para manter uma coleção grande fora do catálogo, use a [biblioteca externa](../library-maintenance.md).

## Atualizar

```bash
python3 scripts/skills.py install --agent claude --bundle editorial --update
```

O arquivo `.meta-skills-install.json` no destino registra as skills que o instalador gerencia, com a release e o SHA-256 de cada arquivo. Com isso:

- Repetir a mesma instalação não muda nada.
- Release nova, conteúdo novo ou troca entre cópia e link exigem `--update`.
- Uma cópia que você editou à mão não é sobrescrita, nem com `--update`. Reconcilie a edição e repita.
- Uma pasta com o mesmo nome e sem registro, criada por outro meio, nunca é sobrescrita: a instalação para com erro.
- Escolher um bundle menor não remove o que já estava instalado. Não há comando de remoção.

As cópias levam `SKILL.md`, `references`, `scripts`, `examples`, `assets` e `agents`, sem caches nem arquivos da raiz do repositório.

## Quando uma instalação falha

O instalador confere todo o plano antes de gravar e instala uma skill por vez. Se a gravação falhar no meio do lote, as skills anteriores ficam instaladas e registradas, e a que falhou volta à versão anterior, ou some se era nova. Não rode dois instaladores no mesmo destino ao mesmo tempo.

Para retomar:

1. Guarde a mensagem de erro, o `.meta-skills-install.json` e as pastas como estão. Não apague recibos nem edições para forçar o sucesso.
2. Resolva a causa, como falta de espaço ou de permissão.
3. Confira e repita com a mesma seleção e o mesmo modo:

```bash
python3 scripts/skills.py doctor --destination /caminho/skills --all
python3 scripts/skills.py install --destination /caminho/skills --all --update --dry-run
python3 scripts/skills.py install --destination /caminho/skills --all --update
```

As skills que já tinham terminado aparecem como `unchanged`. Rode o doctor de novo no conjunto todo: o doctor aprovado numa skill confirma a integridade dela, não que o lote inteiro terminou.

## Antigravity e skills.json

Com as skills nas pastas padrão, o `skills.json` não é necessário. Para registrar uma fonte externa, gere as entradas, revise e incorpore ao `.agents/skills.json` do workspace ou ao manifesto global da sua versão:

```bash
python3 scripts/skills.py manifest --bundle research --exclude execution-pipeline
```

O formato de `entries[].path` segue o [exemplo do Chromium](https://chromium.googlesource.com/experimental/chromium/src/+/HEAD/agents/skills/README.md); o [changelog do Antigravity CLI](https://github.com/google-antigravity/antigravity-cli/blob/main/CHANGELOG.md) registra o suporte a exclusões. O `--exclude` é aplicado antes de gerar as entradas. O comando não mescla nem sobrescreve configurações existentes, e os caminhos são absolutos para a máquina atual: gere de novo ao trocar de máquina ou de clone. Não registre a mesma fonte por dois mecanismos.

## Depois de instalar

Rode o doctor no destino, abra uma sessão nova no host e siga a [verificação de descoberta](discovery.md): estar no disco não prova que o host carregou a skill.
