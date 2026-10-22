#!/usr/bin/env bash
# Validacao DEEP: inclui render real + verificacao de binarios.
set -euo pipefail

SKILL_DIR="/home/tales/.gemini/config/skills/quarto-expert"
QUARTO_BIN="/opt/quarto/bin/quarto"
[ -x "$QUARTO_BIN" ] || QUARTO_BIN="$(command -v quarto || echo "/usr/local/bin/quarto")"

OFFLINE=0
SKIP_RENDER=0
for arg in "$@"; do
    case "$arg" in
        --offline) OFFLINE=1 ;;
        --skip-render) SKIP_RENDER=1 ;;
    esac
done

if [ -x "$SKILL_DIR/scripts/validate_skill.sh" ]; then
    "$SKILL_DIR/scripts/validate_skill.sh"
else
    echo "FALHA: validate_skill.sh nao encontrado"; exit 1
fi

echo "=== [5/8] Verificando binarios essenciais ==="
check_binary() {
    local name="$1" path="$2" args="${3:---version}"
    if [ ! -x "$path" ]; then
        echo "FALHA: $name nao encontrado em $path"; return 1
    fi
    if ! timeout 5 "$path" $args > /dev/null 2>&1; then
        echo "FALHA: $name existe mas nao responde a '$args'"; return 1
    fi
    echo "OK: $name operacional ($path)"
}

check_binary "Quarto CLI" "$QUARTO_BIN" "--version"
check_binary "Python 3" "$(command -v python3)" "--version"

if [ "$OFFLINE" -eq 0 ]; then
    if curl -sSf --max-time 3 https://quarto.org > /dev/null 2>&1; then
        echo "OK: Conectividade de rede detectada"
    else
        echo "AVISO: Sem rede. Ativando --offline automaticamente."
        OFFLINE=1
    fi
fi

echo "=== [6/8] Verificando motores computacionais (opcional) ==="
"$QUARTO_BIN" check jupyter 2>/dev/null && echo "OK: Jupyter operacional" \
    || echo "AVISO: Jupyter nao disponivel (nao bloqueante)"
"$QUARTO_BIN" check knitr 2>/dev/null && echo "OK: Knitr operacional" \
    || echo "AVISO: Knitr nao disponivel (nao bloqueante)"

echo "=== [6.5/8] Auto-deteccao de Python com Jupyter ==="
detect_quarto_python() {
    for candidate in \
        "/home/tales/miniforge3/envs/science/bin/python" \
        "/home/tales/miniforge3/bin/python3" \
        "$(command -v python3 2>/dev/null)"; do
        [ -z "$candidate" ] && continue
        [ ! -x "$candidate" ] && continue
        if "$candidate" -c "import jupyter, nbformat" 2>/dev/null; then
            echo "$candidate"
            return 0
        fi
    done
    return 1
}

if QUARTO_PYTHON_DETECTED=$(detect_quarto_python); then
    export QUARTO_PYTHON="$QUARTO_PYTHON_DETECTED"
    echo "OK: QUARTO_PYTHON auto-detectado: $QUARTO_PYTHON"
else
    echo "AVISO: Nenhum Python com Jupyter encontrado. Render com celulas Python pode falhar."
fi

echo "=== [7/8] Teste de renderizacao real ==="
EXAMPLE_DIR="$SKILL_DIR/examples/minimal-report"
if [ "$SKIP_RENDER" -eq 1 ]; then
    echo "AVISO: Renderizacao pulada por --skip-render"
elif [ "$OFFLINE" -eq 1 ]; then
    echo "AVISO: Renderizacao pulada (modo offline)"
elif [ ! -d "$EXAMPLE_DIR" ] || [ ! -f "$EXAMPLE_DIR/index.qmd" ]; then
    echo "AVISO: Exemplo minimal-report incompleto, pulando render"
else
    TMP_OUT="$(mktemp -d -t quarto-render-XXXXXX)"
    LOG_FILE="$TMP_OUT/render.log"
    cleanup() { [ -d "$TMP_OUT" ] && rm -rf "$TMP_OUT"; }
    trap cleanup EXIT

    if ( cd "$EXAMPLE_DIR" && \
         timeout 120 "$QUARTO_BIN" render index.qmd \
             --to html \
             --output-dir "$TMP_OUT" \
             --quiet > "$LOG_FILE" 2>&1 ); then
        if [ -f "$TMP_OUT/index.html" ]; then
            SIZE=$(wc -c < "$TMP_OUT/index.html")
            echo "OK: minimal-report renderizado (${SIZE} bytes)"
        else
            echo "FALHA: render completou mas index.html nao foi gerado"
            cat "$LOG_FILE"; exit 1
        fi
    else
        echo "FALHA: renderizacao falhou. Ultimas 30 linhas:"
        tail -30 "$LOG_FILE"; exit 1
    fi
fi

echo ""
echo "VALIDACAO DEEP COMPLETA: quarto-expert apta para producao."
