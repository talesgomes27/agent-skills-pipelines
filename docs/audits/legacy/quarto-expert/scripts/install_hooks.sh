#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="/home/tales/.gemini/config/skills/quarto-expert"
REPO_ROOT="/home/tales/.gemini/config"
HOOK_SRC="$SKILL_DIR/scripts/hooks/pre-commit"
HOOK_DST="$REPO_ROOT/.git/hooks/pre-commit"

[ ! -d "$REPO_ROOT/.git" ] && { echo "FALHA: $REPO_ROOT nao e repo git"; exit 1; }
[ ! -f "$HOOK_SRC" ] && { echo "FALHA: $HOOK_SRC nao existe"; exit 1; }

mkdir -p "$(dirname "$HOOK_DST")"

if [ -e "$HOOK_DST" ] && [ ! -L "$HOOK_DST" ]; then
    mv "$HOOK_DST" "${HOOK_DST}.bak.$(date +%s)"
fi

ln -sf "$HOOK_SRC" "$HOOK_DST"
chmod +x "$HOOK_SRC" "$HOOK_DST"
echo "OK: Hook instalado ($HOOK_DST -> $HOOK_SRC)"
