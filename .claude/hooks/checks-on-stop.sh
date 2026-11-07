#!/usr/bin/env bash
# Stop: enquanto houver mudança não commitada em skills, catálogo, scripts ou testes, roda os testes e o doctor antes de encerrar.
input=$(cat)
# Sem jq não há como ler o stop_hook_active, e bloquear poderia virar laço.
command -v jq >/dev/null || exit 0
# Já bloqueado uma vez neste encerramento: não insiste, para não entrar em laço.
[ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false')" = "true" ] && exit 0
root="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$root" 2>/dev/null || exit 0
changes=$(git status --porcelain -- '*/SKILL.md' '*/references/*' distribution .claude-plugin README.md scripts tests ':(exclude).claude' 2>/dev/null)
[ -z "$changes" ] && exit 0
failed=""
tests_out=$(/usr/bin/python3 -m unittest discover -s tests 2>&1) || failed="testes"
doctor_out=$(/usr/bin/python3 scripts/skills.py doctor 2>&1) || failed="${failed:+$failed e }doctor"
[ -z "$failed" ] && exit 0
echo "Há mudanças pendentes e falharam: $failed." >&2
printf '%s\n' "$tests_out" | grep -E '^(FAIL|ERROR):' | head -5 >&2
printf '%s\n' "$doctor_out" | jq -r '(.error // empty | "- \(.)"), (.checks[]? | select(.status != "pass") | "- \(.skill): \(.error // .status)")' 2>/dev/null | head -5 >&2
echo "Corrija antes de encerrar, ou diga ao usuário por que fica assim." >&2
exit 2
