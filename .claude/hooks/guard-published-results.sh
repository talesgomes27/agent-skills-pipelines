#!/usr/bin/env bash
# PreToolUse: editar evals/results/<versão>/ de uma versão já publicada (com tag vX.Y.Z) pede confirmação.
# Resultados publicados não são reescritos; a versão em preparo, sem tag, continua livre.
if ! command -v jq >/dev/null; then
  echo "guard-published-results: jq ausente, resultados publicados sem proteção" >&2
  exit 0
fi
file=$(jq -r '.tool_input.file_path // empty')
case "$file" in
  evals/results/*|*/evals/results/*) ;;
  *) exit 0 ;;
esac
versao=$(printf '%s' "/$file" | sed -n 's#.*/evals/results/\([^/]*\)/.*#\1#p')
[ -z "$versao" ] && exit 0
root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
git -C "$root" rev-parse -q --verify "refs/tags/v$versao" >/dev/null 2>&1 || exit 0
jq -n --arg v "$versao" '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "ask",
  permissionDecisionReason: ("evals/results/" + $v + " é de uma versão publicada (tag v" + $v + "); resultados publicados não são reescritos. Confirme só se for uma correção deliberada.")}}'
