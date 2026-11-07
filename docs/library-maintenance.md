# Biblioteca externa

Uma coleção grande de skills, com centenas ou milhares de pastas, não cabe no catálogo do host: cada skill instalada ocupa contexto com nome e descrição. A `skill-loader` mantém essa coleção fora das pastas de descoberta e busca uma skill só quando uma tarefa precisa dela. Encontrar uma skill não a executa nem concede permissões.

## Configurar a raiz

A `skill-loader` procura a raiz da biblioteca, nesta ordem: o argumento explícito, `.agents/skills-library.json` no projeto, `~/.config/agent-skills/library.json` no usuário e a variável `SKILLS_LIBRARY_ROOT`. O índice fica fora do contexto até uma busca delimitada.

```bash
python3 skill-loader/scripts/library_query.py exact database-architect
python3 skill-loader/scripts/library_query.py search "database architecture" --limit 5
```

O carregador confere se o caminho fica dentro da raiz, se o `SKILL.md` existe e se o frontmatter bate com o índice.

## Manter o índice

A `skill-loader` depende de um índice local que pode ficar divergente do filesystem. O mantenedor `scripts/library.py` trata o índice como cache: valida IDs, caminhos confinados à raiz, presença de `SKILL.md` e identidade do frontmatter.

As consultas com `skill-loader/scripts/library_query.py` requerem Python 3.9+ com PyYAML 6.0.3, já declarado em `distribution/requirements.txt`. O pacote instalado funciona sem o checkout. O [contrato do loader](../skill-loader/SKILL.md#localização) define a validação de frontmatter, os candidatos rejeitados e os códigos de saída. Bibliotecas legadas incompletas podem precisar de correção pelo mantenedor; o loader não as altera.

```bash
python3 scripts/library.py doctor --root /caminho/da/biblioteca
python3 scripts/library.py rebuild --root /caminho/da/biblioteca --output /tmp/skills_index.candidate.json
```

`rebuild` examina por padrão `<raiz>/**/SKILL.md`, preserva metadados antigos dos IDs encontrados e grava uma candidata separada. Use `--skills-dir SUBPASTA` quando a biblioteca adotar um contêiner específico. Um caso comum é o índice guardar caminhos de um layout antigo depois que as pastas mudaram de lugar: o `rebuild` gera a candidata a partir do frontmatter de cada `SKILL.md`. Compare a candidata com o índice atual antes de substituir. Para escrever no mesmo arquivo é necessário fornecer `--replace` explicitamente; mantenha backup e controle de versão fora deste repositório.
