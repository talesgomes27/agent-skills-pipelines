#!/usr/bin/env bash
# verify_skill.sh — Verificacao pos-execucao da skill quarto-expert.
# Codigos: 0=OK, 1=falha critica, 2=aviso.
set -euo pipefail

SKILL_DIR="/home/tales/.gemini/config/skills/quarto-expert"
REPO_ROOT="/home/tales/.gemini/config"
SKILL_FILE="$SKILL_DIR/SKILL.md"

# Stubs intencionalmente vazios (nao geram WARN no relatorio)
LEGITIMATE_EMPTY=(
    "abnt-thesis-starter/references.bib"
    "manuscript-binder/references.bib"
)

is_legitimately_empty() {
    local path="$1"
    for pattern in "${LEGITIMATE_EMPTY[@]}"; do
        [[ "$path" == *"$pattern" ]] && return 0
    done
    return 1
}

OUTPUT_MODE="human"
for arg in "$@"; do
    case "$arg" in
        --json) OUTPUT_MODE="json" ;;
    esac
done

OK_COUNT=0; WARN_COUNT=0; FAIL_COUNT=0
declare -a REPORT_LINES=()

record_ok()   { OK_COUNT=$((OK_COUNT+1));     REPORT_LINES+=("OK|$1"); }
record_warn() { WARN_COUNT=$((WARN_COUNT+1)); REPORT_LINES+=("WARN|$1"); }
record_fail() { FAIL_COUNT=$((FAIL_COUNT+1)); REPORT_LINES+=("FAIL|$1"); }

check_file() {
    local path="$1" mandatory="${2:-1}" label="${3:-$1}"
    if [ -f "$path" ]; then
        local size; size=$(wc -c < "$path" 2>/dev/null || echo 0)
        if [ "$size" -gt 0 ]; then
            record_ok "$label existe (${size} bytes)"
        elif is_legitimately_empty "$path"; then
            record_ok "$label existe (stub intencional)"
        else
            record_warn "$label existe mas esta vazio"
        fi
    else
        if [ "$mandatory" -eq 1 ]; then record_fail "$label AUSENTE: $path"
        else record_warn "$label ausente (opcional): $path"; fi
    fi
}

check_exec() {
    local path="$1" label="${2:-$1}"
    if [ ! -f "$path" ]; then record_fail "$label inexistente"; return; fi
    if [ -x "$path" ]; then record_ok "$label e executavel"
    else record_fail "$label NAO e executavel"; fi
}

check_dir_nonempty() {
    local path="$1" label="${2:-$1}"
    if [ ! -d "$path" ]; then record_fail "$label AUSENTE: $path"; return; fi
    local count; count=$(find "$path" -type f 2>/dev/null | wc -l)
    if [ "$count" -gt 0 ]; then record_ok "$label existe com $count arquivo(s)"
    else record_warn "$label existe mas esta vazio"; fi
}

echo "[verify] ETAPA 1/6: Estrutura raiz" >&2
check_dir_nonempty "$SKILL_DIR" "Diretorio da skill"
check_file "$SKILL_FILE" 1 "Manifesto principal"

echo "[verify] ETAPA 2/6: Referencias" >&2
check_file "$SKILL_DIR/references/abnt-thesis-guide.md" 1 "Referencia ABNT"
check_file "$SKILL_DIR/references/typst-and-templates.md" 1 "Referencia Typst"
check_file "$SKILL_DIR/references/rmd-to-quarto-migration.md" 1 "Referencia migracao"
check_file "$SKILL_DIR/references/code-cells.md" 1 "Referencia celulas de codigo (Posit)"
check_file "$SKILL_DIR/references/cross-references.md" 1 "Referencia referencias cruzadas (Posit)"
check_file "$SKILL_DIR/references/callouts.md" 1 "Referencia callouts (Posit)"
check_file "$SKILL_DIR/references/figures.md" 1 "Referencia figuras (Posit)"
check_file "$SKILL_DIR/references/tables.md" 1 "Referencia tabelas (Posit)"
check_file "$SKILL_DIR/references/brand-yml.md" 1 "Referencia brand-yml (Posit)"
check_file "$SKILL_DIR/references/alt-text.md" 1 "Referencia alt-text (Posit)"
check_file "$SKILL_DIR/references/conversion-rmarkdown.md" 1 "Referencia conversao rmarkdown (Posit)"
check_file "$SKILL_DIR/references/yaml-front-matter.md" 1 "Referencia yaml front matter (Posit)"

echo "[verify] ETAPA 3/6: Scripts" >&2
check_exec "$SKILL_DIR/scripts/init_quarto_project.sh" "init_quarto_project.sh"
check_exec "$SKILL_DIR/scripts/validate_skill.sh" "validate_skill.sh"
check_exec "$SKILL_DIR/scripts/validate_skill_deep.sh" "validate_skill_deep.sh"
check_exec "$SKILL_DIR/scripts/install_hooks.sh" "install_hooks.sh"
check_exec "$SKILL_DIR/scripts/backup_examples.sh" "backup_examples.sh"
check_exec "$SKILL_DIR/scripts/hooks/pre-commit" "pre-commit hook"

echo "[verify] ETAPA 4/6: Exemplos" >&2
check_file "$SKILL_DIR/examples/minimal-report/_quarto.yml" 1 "minimal-report/_quarto.yml"
check_file "$SKILL_DIR/examples/minimal-report/index.qmd" 1 "minimal-report/index.qmd"
check_file "$SKILL_DIR/examples/abnt-thesis-starter/_quarto.yml" 1 "abnt-thesis-starter/_quarto.yml"
check_file "$SKILL_DIR/examples/abnt-thesis-starter/index.qmd" 1 "abnt-thesis-starter/index.qmd"
check_file "$SKILL_DIR/examples/abnt-thesis-starter/references.bib" 1 "abnt-thesis-starter/references.bib"
check_file "$SKILL_DIR/examples/manuscript-binder/_quarto.yml" 1 "manuscript-binder/_quarto.yml"
check_file "$SKILL_DIR/examples/manuscript-binder/index.qmd" 1 "manuscript-binder/index.qmd"
check_file "$SKILL_DIR/examples/manuscript-binder/requirements.txt" 1 "manuscript-binder/requirements.txt"
check_file "$SKILL_DIR/examples/manuscript-binder/references.bib" 1 "manuscript-binder/references.bib"
check_file "$SKILL_DIR/examples/manuscript-binder/notebooks/01-analise.qmd" 1 "manuscript-binder/notebooks/01-analise.qmd"

echo "[verify] ETAPA 5/6: Conteudo do SKILL.md" >&2
if [ -f "$SKILL_FILE" ]; then
    for section in \
        "## 1. Regras Criticas" \
        "## 1.1 Arvore de Decisao" \
        "## 2. Referencias Modulares" \
        "## 5. Resolucao de Problemas" \
        "## 6. Exemplos de Prompts" \
        "## 9. Validacao Profunda" \
        "## 10. Verificacao Pos-Execucao"; do
        if grep -qF "$section" "$SKILL_FILE" 2>/dev/null; then
            record_ok "Secao presente: $section"
        else
            record_warn "Secao ausente: $section"
        fi
    done

    if python3 -c "
import yaml, sys
with open('$SKILL_FILE') as f:
    c = f.read()
if not c.startswith('---'): sys.exit(1)
d = yaml.safe_load(c.split('---')[1])
assert 'name' in d and 'description' in d
" 2>/dev/null; then
        record_ok "Frontmatter YAML valido"
    else
        record_fail "Frontmatter YAML invalido"
    fi
else
    record_fail "SKILL.md ausente"
fi

echo "[verify] ETAPA 6/6: Integridade do Git" >&2
if [ -d "$REPO_ROOT/.git" ]; then
    UNTRACKED=$(git -C "$REPO_ROOT" status --porcelain skills/quarto-expert/ 2>/dev/null | wc -l)
    if [ "$UNTRACKED" -eq 0 ]; then record_ok "Todos os arquivos versionados"
    else record_warn "$UNTRACKED arquivo(s) nao commitado(s)"; fi

    HOOK_PATH="$REPO_ROOT/.git/hooks/pre-commit"
    if [ -L "$HOOK_PATH" ]; then record_ok "pre-commit hook instalado (symlink)"
    elif [ -x "$HOOK_PATH" ]; then record_warn "pre-commit hook nao e symlink"
    else record_warn "pre-commit hook NAO instalado"; fi
elif [ -d "/home/tales/Documentos/github/antigravity-meta-skills/.git" ]; then
    GIT_DIR="/home/tales/Documentos/github/antigravity-meta-skills"
    UNTRACKED=$(git -C "$GIT_DIR" status --porcelain quarto-expert/ 2>/dev/null | wc -l)
    if [ "$UNTRACKED" -eq 0 ]; then record_ok "Todos os arquivos versionados em antigravity-meta-skills"
    else record_warn "$UNTRACKED arquivo(s) com alteracoes em antigravity-meta-skills"; fi
    record_ok "Repositorio git oficial detectado em $GIT_DIR"
else
    record_warn "Repositorio git nao localizado para validacao automatica"
fi

if [ "$OUTPUT_MODE" = "json" ]; then
    python3 << PYEOF
import json
lines = """$(printf '%s\n' "${REPORT_LINES[@]}")""".strip().split('\n')
entries = []
for line in lines:
    if '|' in line:
        status, msg = line.split('|', 1)
        entries.append({"status": status, "message": msg})
print(json.dumps({
    "skill": "quarto-expert",
    "ok": $OK_COUNT,
    "warn": $WARN_COUNT,
    "fail": $FAIL_COUNT,
    "entries": entries,
    "exit_code": 0 if $FAIL_COUNT == 0 else 1
}, indent=2, ensure_ascii=False))
PYEOF
else
    echo ""
    echo "================================================================"
    echo "  RELATORIO DE VERIFICACAO — SKILL quarto-expert"
    echo "================================================================"
    for line in "${REPORT_LINES[@]}"; do
        status="${line%%|*}"; msg="${line#*|}"
        case "$status" in
            OK)   printf "  \033[32m[OK]\033[0m   %s\n" "$msg" ;;
            WARN) printf "  \033[33m[WARN]\033[0m %s\n" "$msg" ;;
            FAIL) printf "  \033[31m[FAIL]\033[0m %s\n" "$msg" ;;
        esac
    done
    echo "================================================================"
    printf "  Resumo: \033[32m%d OK\033[0m | \033[33m%d WARN\033[0m | \033[31m%d FAIL\033[0m\n" \
        "$OK_COUNT" "$WARN_COUNT" "$FAIL_COUNT"
    echo "================================================================"
fi

if [ "$FAIL_COUNT" -gt 0 ]; then exit 1
elif [ "$WARN_COUNT" -gt 0 ]; then exit 2
else exit 0; fi
