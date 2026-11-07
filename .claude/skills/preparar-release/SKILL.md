---
name: preparar-release
description: Prepara e publica uma release deste repositório, do número da versão ao smoke num clone limpo da tag. Use quando o usuário pedir para publicar uma versão nova das skills.
disable-model-invocation: true
argument-hint: "<versão, por exemplo 3.2.0>"
---

# Release deste repositório

A `release-and-ops-pipeline` dá os gates e as autorizações; esta skill dá os passos específicos deste repositório. Use `/usr/bin/python3` em todos os comandos e o scratchpad da sessão para arquivos temporários.

## 1. Antes

- `git fetch` e `main` igual à `origin/main`. As notas vêm da seção "Não publicado" do CHANGELOG; sem ela, de `git log <tag anterior>..main`.
- Uma release por vez. Os cenários das skills que mudaram desde a tag anterior precisam de resultados da versão nova em `evals/results/<versão>/<nível>/`, rodados pelo `/cenarios`. Um checkpoint que passava na versão anterior e agora falha bloqueia a release, salvo justificativa escrita no CHANGELOG.
- Proponha a versão pelo SemVer, olhando essas notas: skill removida ou escopo cortado é MAJOR; skill, regra ou referência nova é MINOR; correção é PATCH. Confirme com o usuário.

## 2. Preparar

- Branch `release/X.Y.Z`.
- Suba a versão em três lugares: `distribution/catalog.json` (`release`), `README.md` (badge e "Release atual") e todas as entradas `version` de `.claude-plugin/marketplace.json`.
- Feche o CHANGELOG: `## [X.Y.Z] - AAAA-MM-DD`, a comparação com a tag anterior e o commit dela, as seções existentes e "Como atualizar" (Claude Code, `skills.py --update` e plugins novos que precisam de `install`).

## 3. Validar

- Os testes, o doctor e `claude plugin validate --strict .`.
- `/usr/bin/python3 evals/report.py` e a tabela dele nas notas da versão.
- Instalação de todas as skills por cópia e por link numa pasta temporária, com o doctor no destino.
- Atualização real: `git archive <tag anterior>` numa pasta temporária, instale os bundles `development` e `research` com o `skills.py` antigo e atualize com o atual usando `--update`. Confira os recibos na versão nova, as skills que entraram e as referências renomeadas, e rode o doctor no destino.
- Procure no diff token, chave, senha, caminho pessoal e número com formato de CPF.

## 4. Enviar, com autorização

Commit `chore(release): prepara a X.Y.Z`, push da branch e PR "Release X.Y.Z" com a verificação local na descrição. Não acompanhe a CI em loop: diga ao usuário para continuar quando os checks passarem.

## 5. Publicar, com autorização

- Confira que os checks obrigatórios passaram e que o PR ainda aponta para o commit testado.
- Faça o merge com `gh pr merge <n> --merge --match-head-commit <commit>`, sincronize a `main` por fast-forward e confira que a árvore é a do commit testado.
- Confira que a tag `vX.Y.Z` não existe, nem local nem no GitHub. Crie-a anotada no merge commit e envie.
- Avance a branch `stable` até o commit da tag, só por fast-forward: `git push origin 'vX.Y.Z^{commit}:refs/heads/stable'`. Se o GitHub recusar por não ser fast-forward, pare e investigue; nunca force.
- `gh release create vX.Y.Z --verify-tag` com a seção da versão extraída do CHANGELOG. Confira que ela ficou como latest, fora de rascunho e de pré-release.

## 6. Smoke

Clone a tag `vX.Y.Z` do GitHub numa pasta limpa e confira:

- os testes, o doctor e o `offline_probe.py`;
- a instalação de todas as skills, com o doctor no destino, e a presença das referências novas;
- o validador do plugin;
- a versão no catálogo, no marketplace e no badge;
- que a `stable` aponta para o commit da tag (`git ls-remote origin stable`).

Relate o que foi publicado, o que o smoke conferiu e o que ficou sem conferir, como a CI da `main` depois do merge e as instalações do próprio usuário.
