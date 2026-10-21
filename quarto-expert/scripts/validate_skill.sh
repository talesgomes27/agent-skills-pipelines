#!/usr/bin/env bash
set -euo pipefail

SKILL_FILE="/home/tales/.gemini/config/skills/quarto-expert/SKILL.md"
SKILL_DIR="/home/tales/.gemini/config/skills/quarto-expert"

echo "=== [1/4] Validando frontmatter YAML e tamanho do header ==="
python3 << 'PYEOF'
import yaml, sys

SKILL_FILE = "/home/tales/.gemini/config/skills/quarto-expert/SKILL.md"

with open(SKILL_FILE) as f:
    content = f.read()

if not content.startswith("---"):
    print("FALHA: Frontmatter ausente"); sys.exit(1)

data = yaml.safe_load(content.split("---")[1])

for key in ("name", "description"):
    if key not in data:
        print(f"FALHA: Chave obrigatoria ausente: {key}"); sys.exit(1)

entry_line = f"- {data['name']} ({SKILL_FILE}): {data['description']}"
tokens_est = len(entry_line) // 4
print(f"OK: Frontmatter valido. Header: {len(entry_line)} chars (~{tokens_est} tokens)")

if tokens_est >= 80:
    print(f"FALHA: Header excede teto de 80 tokens (~{tokens_est})")
    sys.exit(1)
PYEOF

echo "=== [2/4] Verificando existencia de caminhos internos do pacote ==="
python3 << 'PYEOF'
import re, os, sys

SKILL_FILE = "/home/tales/.gemini/config/skills/quarto-expert/SKILL.md"
PATTERN = r'/home/tales/\.gemini/config/skills/quarto-expert/[a-zA-Z0-9/_.-]+?(?=[\s\)\]\}`\'",;:]|$)'

with open(SKILL_FILE) as f:
    content = f.read()

paths = set(re.findall(PATTERN, content))
missing = [p for p in paths if not os.path.exists(p)]

if missing:
    print("FALHA: Caminhos internos em falta:")
    for m in missing:
        print(f"   - {m}")
    sys.exit(1)

print(f"OK: Todos os {len(paths)} caminhos internos existem.")
PYEOF

echo "=== [3/4] Validando sintaxe YAML dos projetos de exemplo ==="
python3 << 'PYEOF'
import glob, yaml, sys

files = glob.glob('/home/tales/.gemini/config/skills/quarto-expert/examples/**/*.yml', recursive=True)
files += glob.glob('/home/tales/.gemini/config/skills/quarto-expert/examples/**/*.yaml', recursive=True)

if not files:
    print("AVISO: Nenhum exemplo YAML encontrado")
else:
    for f in files:
        try:
            with open(f) as fp:
                yaml.safe_load(fp.read())
            print(f"OK: YAML valido: {f}")
        except yaml.YAMLError as e:
            print(f"FALHA: YAML invalido em {f}: {e}")
            sys.exit(1)
PYEOF

echo "=== [4/4] Validando sintaxe dos scripts bash ==="
for script in "$SKILL_DIR"/scripts/*.sh; do
    [ -f "$script" ] || continue
    bash -n "$script" && echo "OK: Sintaxe bash: $script"
done

echo ""
echo "VALIDACAO RAPIDA COMPLETA: skill quarto-expert em conformidade."
