# Notas de manutenção

Para quem altera as skills, o instalador ou a CI. As regras de trabalho estão no [AGENTS.md](../AGENTS.md).

## Validar

```bash
python3 scripts/skills.py doctor
python3 -m unittest discover -s tests -v
python3 quarto-expert/scripts/doctor.py
claude plugin validate --strict .
```

A CI repete os testes, o doctor e instalações temporárias em Linux, Windows e macOS. Ela não executa workflows de release, não consulta fontes externas, não inicia MCPs e não certifica a conformidade normativa dos documentos. O doctor da `quarto-expert` tem verificações próprias de ambiente e de render.

Mudança de comportamento numa skill se testa com os cenários de [verificação de descoberta](distribution/discovery.md#cenários-de-comportamento), antes e depois.

## Contratos

- **Skill.** Cada pasta tem um `SKILL.md` com frontmatter YAML `name` e `description`, conforme a [especificação de Agent Skills](https://agentskills.io/specification). Links para recursos são relativos ao arquivo que os contém e ficam dentro da pasta da skill. Um `SKILL.md` tem no máximo 10.000 caracteres, cerca de 4 mil tokens em português. Isso fica abaixo dos 5 mil tokens que a especificação recomenda para o corpo da skill e dos 5 mil que o Claude Code recoloca de cada skill depois de uma compactação ([skills](https://code.claude.com/docs/en/skills)). Não suba o limite sem conferir essas duas referências.
- **Catálogo.** `distribution/catalog.json` usa o schema versão 1, publicado em `distribution/catalog.schema.json`, e a release em SemVer. A CLI confere campos, tipos, versão, unicidade e se os membros dos bundles existem, sem depender de um validador genérico de JSON Schema.
- **Subagentes do Claude Code.** Ficam em `plugin-agents/` e entram pela chave `agents` da entrada do plugin no marketplace, nunca numa pasta `agents/` na raiz, que todos os plugins com `source: "./"` veriam. O `plan-reviewer` só tem ferramentas de leitura. O `diff-reviewer` e o `sanitation-checker` têm Bash, limitado à leitura só pelo texto; a proteção real são as regras `ask` e `deny` da sessão, descritas no guia de instalação. Os três são autocontidos, sem ler arquivos fora do projeto do usuário, e não chegam aos outros hosts pelo instalador. No Claude Code 2.1.319, `claude plugin details` mostra "Agents (0)" para eles, embora carreguem na sessão; confira com uma sessão.
- **`agents/openai.yaml`** é opcional, para interface, política e ferramentas no Codex. Nenhuma skill exige MCP nem bloqueia a invocação implícita.

## O que o doctor confere

- Sintaxe YAML e chaves duplicadas no frontmatter e nos arquivos `.yml` e `.yaml` da skill; nome igual ao da pasta; descrição e metadata como texto.
- Links Markdown inline no `SKILL.md` e em `references/**/*.md`: o destino existe e fica dentro da skill. Ignora código, URLs externas e âncoras; em `arquivo.md#seção`, confere o arquivo, não a seção. Não lê links por definição nem em HTML.
- `examples/` fica fora da varredura de links, mas os arquivos YAML e as regras de symlink continuam valendo.
- O limite de 10.000 caracteres do `SKILL.md`.
- No destino de uma instalação, a integridade de cada cópia gerenciada pelo SHA-256 registrado. Um link é verificado só na estrutura, porque o conteúdo é o do checkout vivo. Uma skill sem registro recebe só a verificação estrutural.

A mesma validação roda antes de `manifest` e `install`, sem rede e sem executar snippets. Não é um validador completo de Markdown nem das extensões de cada host.

As saídas da CLI são JSON, com código 0 para sucesso, 1 para erro e 2 para dependência ausente. Falta de PyYAML nunca conta como sucesso.

## Instalação transacional por skill

O preflight confere o plano inteiro, mas a gravação é transacional só por skill: cada uma é preparada no filesystem do destino, trocada e registrada, com recuperação se a gravação falhar. Um teste cobre a falha tardia em dois estados: atualização por cópia com `alpha` já em 1.1.0 e `beta` restaurado em 1.0.0, e instalação nova por link com só `alpha` registrado. O recibo continua válido e arquivos alheios ao lote ficam intactos. Isso não garante recuperação de qualquer falha do filesystem, e uma falha na própria recuperação deve ser tratada pelo estado observado. Recuperar um link não desfaz mudanças feitas no checkout.

## Integrações

Graphify, MCPs e conectores são opcionais e não ampliam o que o usuário autorizou. Distribuir uma pasta de skill não inicia nenhum servidor. Um framework próprio pode indexar só o frontmatter das skills escolhidas e oferecer busca e leitura pontuais; para um catálogo local pequeno, o filesystem basta, e MCP só se justifica com acesso remoto ou compartilhado.

## Dependências da CI

As actions em `.github/workflows/ci.yml` usam SHA completo, com a versão legível num comentário. Para atualizar:

1. Resolva a tag ou release desejada no repositório oficial, como `actions/checkout` ou `actions/setup-python`.
2. Confira o commit e o `action.yml` nessa revisão e revise a compatibilidade.
3. Atualize todas as ocorrências e registre fonte, versão, SHA e data da conferência.
4. Valide localmente YAML, eventos, permissões, matriz e comandos.

Não copie um SHA sugerido por terceiros sem conferir a origem, nem deixe a dependência seguir a tag sozinha. O SHA não fixa a imagem `*-latest`, os downloads de runtime nem as dependências transitivas.

## Histórico

Auditorias, experimentos e o harness de avaliações até a MOD-010 estão na tag `archive/mod-2026-10`, fora da árvore atual. As avaliações atuais ficam em `evals/`, só com cenários e resultados declarativos.
