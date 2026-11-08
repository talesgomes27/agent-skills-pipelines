# Bash

Leia quando o componente da tarefa é um script de shell.

## Descubra no projeto

- Shell: o shebang (`#!/usr/bin/env bash`, `#!/bin/sh`) diz qual interpretador roda o script. Não troque um pelo outro.
- Comandos e ambiente: `Makefile`, o workflow de CI, `.shellcheckrc` e a pasta de testes (`test/*.bats`).
- Dependências: os programas externos que o script chama e as versões disponíveis no CI.

Use os comandos do projeto. Não instale nada global; rode em diretório temporário, com dados de teste, como pede a [referência C](../archetype-c.md).

## Testes e checks

Exemplos a confirmar no projeto:

- `bash -n script.sh` para sintaxe e `shellcheck script.sh` para análise estática.
- Bats: cada teste é um bloco `@test` em arquivo `.bats`, e o `run` guarda o código de saída em `$status` e a saída em `$output`.
- Execução real num diretório temporário, conferindo códigos de saída e arquivos gerados.

## Armadilhas

- `set -euo pipefail` ajuda, mas não cobre tudo. O `-e` não sai quando o comando que falha está no teste de `if`, `while` ou `until`, numa lista `&&` ou `||` antes do último comando, invertido com `!`, ou dentro de função chamada nesses contextos. Sem `pipefail`, só o último comando do pipeline conta.
- Variável sem aspas: `$arquivo` sem aspas passa por divisão de palavras e expansão de glob, e quebra com espaço ou `*` no nome. Escreva `"$arquivo"` e use arrays para listas.
- Ler de pipe em `while`: em `cmd | while read ...`, o laço roda num subshell e as variáveis alteradas nele se perdem. Use `while read ...; done < <(cmd)` ou `shopt -s lastpipe`.
- `-u` com variável opcional: referência a variável não definida encerra o script não interativo. Dê um valor padrão explícito à variável opcional antes de usá-la.
- Erro em stdout: mensagens de erro e progresso vão para stderr, para não sujar a saída que outra ferramenta lê.

## Fontes

Conferido em 08/11/2026:

- https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html
- https://www.gnu.org/software/bash/manual/html_node/Pipelines.html
- https://www.shellcheck.net/wiki/SC2086
- https://www.shellcheck.net/wiki/SC2031
- https://bats-core.readthedocs.io/en/stable/writing-tests.html
