# CI e vínculo com o artefato

## Contrato do workflow

Identifique eventos de entrada, commits, branch/tag, scripts, lockfiles e required checks reais. Não imponha pytest a TypeScript, uv a shell ou GitHub Actions a um projeto hospedado em outra plataforma.
Separe validação de código não confiável e jobs privilegiados de publicação. Evite disponibilizar secrets/credenciais de escrita a builds de origem não confiável. Revise checkout, caches e artefatos entre contextos de confiança; não execute conteúdo de PR externo com privilégio por conveniência.
Use permissões mínimas por job e timeout explícito. Um `environment` nomeado não cria reviewers/proteções sozinho; confira a configuração efetiva. OIDC/trusted publishing depende de vínculo real com repositório, workflow, ambiente e registry, não apenas `id-token: write` no YAML.
Fixe dependências de workflow por mecanismo imutável suportado e verificável pelo projeto, como lockfile de dependências de workflow quando disponível ou SHA completo revisado. Não invente SHA nem copie uma tag antiga como se fosse a versão adequada ao ambiente atual.
Condições e jobs skipped não podem ser apresentados como testes aprovados. Verifique que falhas impedem publicação e que build/deploy têm a dependência correta. Prefira concorrência que evite duas promoções conflitantes do mesmo destino.

## Artefato e evidência

Registre commit, versão, run produtor e identificador/digest do artefato quando disponíveis. A aprovação deve referir-se a esse conteúdo, não a “latest” sem resolução.
Mudança de versão/arquivo depois do teste exige checks pertinentes do artefato final. Para pacotes, inspecione conteúdo e instale o wheel/binário construído em ambiente temporário fora da árvore de desenvolvimento, sem importação editable do checkout. `uv run` no projeto não comprova essa instalação isolada.
Para containers, identifique imagem por digest/revisão e confira entrypoint/configuração no destino de teste. Build local e registry push são estados distintos.
Validador YAML/actionlint verifica propriedades locais; confirmação de CI exige consultar run e conclusão para o commit certo. URL de deployment emitida pode representar fila, erro ou preview: confira status e destino final antes de concluir.

## Observação e recuperação

Use consultas limitadas e intervalos razoáveis para runs/deployments; se não houver estado terminal dentro da janela disponível, relate pendência, sem loop infinito ou repetição de upload/deploy.
Defina revisão estável anterior e critérios de contenção antes da implantação. Inclua compatibilidade de schema e migrações no plano; restaurar binário não reverte gravações de dados. Publicação de pacote pode exigir nova versão corretiva ou procedimento do registry, não sobrescrita da versão existente.
