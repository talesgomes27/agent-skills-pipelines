# Manutenção da biblioteca fria

A `skill-loader` depende de um índice local que pode ficar divergente do filesystem. O mantenedor `scripts/library.py` trata o índice como cache: valida IDs, caminhos confinados à raiz, presença de `SKILL.md` e identidade do frontmatter.

```bash
python3 scripts/library.py doctor --root /caminho/da/biblioteca
python3 scripts/library.py rebuild --root /caminho/da/biblioteca --output /tmp/skills_index.candidate.json
```

`rebuild` examina por padrão `<raiz>/**/SKILL.md`, preserva metadados antigos dos IDs encontrados e grava uma candidata separada. Use `--skills-dir SUBPASTA` quando a biblioteca adotar um contêiner específico. Compare a candidata com o índice atual antes de substituir. Para escrever no mesmo arquivo é necessário fornecer `--replace` explicitamente; mantenha backup e controle de versão fora deste repositório.

Na verificação de 2026-10-22, a biblioteca configurada em `~/.gemini/config/skills-library` tinha 2.676 entradas e 2.676 manifests válidos. O índice conservava caminhos de um layout anterior com prefixo `skills/`, enquanto os pacotes estavam diretamente na raiz ou em subpastas próprias. A correção foi gerada a partir da identidade do frontmatter, preservando os demais metadados; depois da substituição, o `doctor` confirmou todas as entradas.
