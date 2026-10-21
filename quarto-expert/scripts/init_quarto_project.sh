#!/usr/bin/env bash
set -euo pipefail

# Utilitário de diagnóstico e inicialização de projetos Quarto alinhado ao AGENTS.md
PROJECT_TYPE="${1:-default}"
TARGET_DIR="${2:-.}"

QUARTO_BIN="/opt/quarto/bin/quarto"
if [ ! -x "$QUARTO_BIN" ]; then
  QUARTO_BIN="$(command -v quarto || echo "/usr/local/bin/quarto")"
fi

echo "=== [1/4] Verificando binário do Quarto CLI: $QUARTO_BIN ==="
"$QUARTO_BIN" --version

echo "=== [2/4] Criando estrutura para projeto Quarto ($PROJECT_TYPE) em: $TARGET_DIR ==="
mkdir -p "$TARGET_DIR"/{docs,notebooks,reports/figures,src,tests}

GITIGNORE_FILE="$TARGET_DIR/.gitignore"
touch "$GITIGNORE_FILE"
for pattern in "/.quarto/" "/_*.local" "/_site/" "/_book/" "/_manuscript/" ".venv/" "__pycache__/" ".pytest_cache/" ".ruff_cache/" "*.csv" "*.parquet" "*.pkl"; do
  grep -qxF "$pattern" "$GITIGNORE_FILE" || echo "$pattern" >> "$GITIGNORE_FILE"
done

echo "=== [3/4] Nota sobre _freeze/ ==="
echo "Diretório _freeze/ mantido FORA do .gitignore para suportar CI/CD com execute: freeze: auto."

echo "=== [4/4] Diagnóstico rápido de motores ==="
"$QUARTO_BIN" check install
