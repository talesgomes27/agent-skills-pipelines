# Checklist de Saneamento Pré-Push & Segurança de Dados

Este protocolo complementa a skill `codebase-audit-pre-push` e é obrigatório no **Gate 1** da `release-and-ops-pipeline`.

## 1. Bloqueio de Arquivos Volumosos e Pesos de Modelos (`.gitignore`)
Em projetos do **Arquétipo A (Data Science & ML)**, garanta que o `.gitignore` bloqueie explicitamente:
- **Bases de dados brutas/intermediárias:** `*.csv`, `*.parquet`, `*.feather`, `*.arrow`, `*.db`, `*.sqlite`, `*.h5`, `*.hdf5` (exceto amostras minúsculas documentadas em `tests/fixtures/`).
- **Pesos e binários de modelos:** `*.pkl`, `*.joblib`, `*.pt`, `*.pth`, `*.onnx`, `*.cbm`, `*.ubj`, `*.model`.
- **Ambientes e caches:** `.venv/`, `venv/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.ipynb_checkpoints/`, `.DS_Store`.

## 2. Regra de Ouro do Quarto Cache (`_freeze/` vs. `.quarto/`)
- **IGNORAR sempre:** `/.quarto/` (cache interno efêmero de execução do Quarto CLI).
- **VERSIONAR (`NÃO ignorar`):** `/_freeze/` quando `execute: freeze: auto` (ou `true`) estiver ativo no `_quarto.yml`. O diretório `_freeze/` guarda os resultados computados localmente e permite que o GitHub Actions renderize o HTML/site sem precisar das bases `.csv` brutas nem reexecutar treinamentos pesados de ML no runner.
- *Nota condicional:* Esta regra de versionar `_freeze/` só se aplica quando `execute.freeze` está configurado como `auto` ou `true` no `_quarto.yml`. Se `freeze: false`, o diretório `_freeze/` não precisa ser versionado e pode ser incluído no `.gitignore`.

## 3. Auditoria de Segredos e Outputs de Notebooks
Antes de qualquer `git add` ou `git push`:
1. Verifique se não há arquivos `.env`, `*credentials*.json`, `*.pem`, `*.key` ou tokens hardcoded no diff:
   ```bash
   git status --ignored
   grep -rnE "(API_KEY|SECRET|PASSWORD|TOKEN|PRIVATE_KEY|ghp_|sk-)" src/ notebooks/ *.qmd 2>/dev/null || echo "OK: Sem padrões óbvios de segredos"
   ```
2. Em notebooks `.ipynb` versionados, confirme que células de output não imprimiram variáveis de ambiente, caminhos sensíveis de sistema ou dumps gigantescos de DataFrames que inflem o repositório acima de 10 MB.
3. Confirme que arquivos rastreados não excedem 50 MB:
   ```bash
   find . -maxdepth 4 -not -path '*/.*' -type f -size +50M
   ```

## 4. Integridade de Lockfiles
- **Python (`uv`):** `pyproject.toml` e `uv.lock` sincronizados (`uv lock --check`).
- **Node/TS (`pnpm`/`npm`):** `package.json` e `pnpm-lock.yaml` / `package-lock.json` sincronizados.
