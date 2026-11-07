#!/usr/bin/env bash
# PostToolUse: depois de editar um SKILL.md ou uma referência, roda o doctor e devolve a falha ao Claude.
file=$(jq -r '.tool_input.file_path // empty')
case "$file" in
  */.claude/*) exit 0 ;;  # skills do próprio projeto: o doctor não as confere
  */SKILL.md|*/references/*.md) ;;
  *) exit 0 ;;
esac
root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
if ! out=$(/usr/bin/python3 "$root/scripts/skills.py" doctor 2>&1); then
  echo "O doctor falhou depois de editar $file:" >&2
  printf '%s\n' "$out" | jq -r '(.error // empty | "- \(.)"), (.checks[]? | select(.status != "pass") | "- \(.skill): \(.error // .status)")' 2>/dev/null | head -8 >&2
  echo "Detalhes: /usr/bin/python3 scripts/skills.py doctor" >&2
  exit 2
fi
exit 0
