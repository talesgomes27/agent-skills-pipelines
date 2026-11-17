#!/usr/bin/env bash
# Monta, num diretório temporário, um plugin implementation-pipeline com os casos deste piloto.
# O claude plugin eval só lê casos dentro do plugin, e aqui o plugin real é a raiz do repositório.
# Uso: evals/plugin-eval/montar.sh <destino>; depois: claude plugin eval <destino> ...
set -euo pipefail
repo=$(cd "$(dirname "$0")/../.." && pwd)
dest=${1:?uso: montar.sh <destino>}
rm -rf "$dest"
mkdir -p "$dest/.claude-plugin" "$dest/skills" "$dest/agents" "$dest/evals"
printf '{"name": "implementation-pipeline"}\n' > "$dest/.claude-plugin/plugin.json"
cp -r "$repo/implementation-pipeline" "$dest/skills/"
cp "$repo/plugin-agents/diff-reviewer.md" "$dest/agents/"
for caso in "$repo"/evals/plugin-eval/*/; do
  nome=$(basename "$caso")
  cp -r "$caso" "$dest/evals/$nome"
  fixture=$(cat "$caso/fixture.txt")
  rm "$dest/evals/$nome/fixture.txt"
  # a fixture vai embutida no scaffold, que roda no workspace vazio sem acesso garantido ao diretório do caso
  printf '#!/usr/bin/env bash\nset -e\necho %s | base64 -d | tar xz\n' \
    "$(tar -C "$repo/evals/$fixture" -cz . | base64 -w0)" > "$dest/evals/$nome/scaffold.sh"
done
