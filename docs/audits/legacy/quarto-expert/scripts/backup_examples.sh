#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="/home/tales/.gemini/config/skills/quarto-expert"
EXAMPLES_DIR="$SKILL_DIR/examples"
BACKUP_ROOT="$SKILL_DIR/.backups"

[ ! -d "$EXAMPLES_DIR" ] && { echo "AVISO: $EXAMPLES_DIR nao existe"; exit 0; }

mkdir -p "$BACKUP_ROOT"
TS="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$BACKUP_ROOT/examples-$TS"
cp -r "$EXAMPLES_DIR" "$BACKUP_DIR"
echo "OK: Backup criado em $BACKUP_DIR"

mapfile -t OLD_BACKUPS < <(ls -1dt "$BACKUP_ROOT"/examples-* 2>/dev/null | tail -n +6)
for b in "${OLD_BACKUPS[@]}"; do
    rm -rf "$b"
    echo "Removido backup antigo: $b"
done
