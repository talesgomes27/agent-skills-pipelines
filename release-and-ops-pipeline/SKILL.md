---
name: release-and-ops-pipeline
description: "Use quando o usuário pedir para preparar, versionar, publicar ou implantar uma release, ou para verificar um deploy, depois de uma implementação ou auditoria aprovada."
---

# Releases e operações

Entregue o artefato aprovado no destino autorizado, com evidência de identidade, execução e recuperação. Se o pedido autoriza só preparar localmente, não o amplie para commit, push, publicação de pacote ou produção.

## Antes de começar

1. Leia as instruções de release do projeto, o handoff, o estado, `docs/00_archetype.md` e as evidências da implementação ou auditoria. Sem arquétipo registrado, use o que os contratos ou o pedido dizem; pergunte só se isso impedir escolher o artefato certo.
2. Identifique escopo, commit base, arquivos staged, unstaged e não rastreados relevantes, versão pretendida, artefato e destino. Preserve o trabalho do usuário: não faça staging de tudo nem apague arquivos para limpar a árvore.
3. Defina o modo: **preparar**, **publicar preview**, **publicar release** ou **implantar em produção**. Confirme conta ou projeto, repositório ou registry, branch ou tag, ambiente e efeitos indiretos; um push pode acionar produção pela CI.
4. Registre a release onde o projeto já registra estado, ou na própria resposta, sem apagar o que outras pipelines registraram: gate, artefato e commit, destino, checks, autorizações e resultado, com os estados `preparado`, `aguardando autorização`, `submetido`, `em execução`, `concluído` ou `falhou/parcial`.

## Autorização e modo

Aprovar um gate valida os artefatos daquele gate. Uma ação externa usa a autorização já dada só quando ela cobre o destino e o efeito; senão, mostre o que será publicado e peça a autorização final. Mudança material no artefato ou no destino invalida a aprovação correspondente. Preparar localmente não autoriza commit, push, publicação ou deploy, e estar autenticado não amplia a autorização.

- **Assistido** (padrão): ao fim de cada gate, marque `aguardando_aprovacao` e espere o aceite.
- **Contínuo**: se o usuário autorizou uma sequência concreta de preparação e operações, avance pelas ações cobertas e registre qual autorização sustentou cada uma. Pare diante de mudança material no artefato ou destino, decisão bloqueante, risco de perda, falha que mude a estratégia ou ação externa fora do autorizado.

## Gates

Em cada gate, apresente resultado e pendências e registre o aceite real, sem repetir confirmação já dada para a mesma ação. Etapa não executada ou dispensada não recebe sucesso fictício.

1. **Saneamento.** Siga [saneamento e dados](references/pre-push-sanitation.md). Revise o que realmente será enviado, os lockfiles e as evidências dos checks; não refatore a aplicação nem migre a stack aqui. Use as ferramentas de segredos e dependências que o projeto já tem e registre escopo, versão, resultado e limites. Falha da ferramenta não significa ausência de achado, e o relatório nunca mostra o valor de um segredo. Confira os pré-requisitos do build, sem instalação global implícita.
2. **Versão, notas e plano.** Preserve a política de versões do projeto; sem política declarada, use SemVer. App ou job publicado do Git, sem versão que alguém consuma, dispensa o número: o commit identifica a release. Identifique a API pública e as incompatibilidades antes de propor PATCH, MINOR ou MAJOR, sem deduzir só pelo prefixo dos commits; em 0.x, quebra de compatibilidade sobe o MINOR. Atualize de forma consistente os metadados de versão autorizados, como manifest, changelog e badges. Escreva as notas a partir das mudanças reais do intervalo certo, com a `writing-pipeline` se preciso. Não recrie tag publicada nem reescreva histórico remoto. O plano define os arquivos do commit, a branch ou tag, os comandos do fluxo de release do projeto, os efeitos do push e a recuperação; commit e tag só com autorização. Se a versão muda o conteúdo do pacote, o build valida o conteúdo final.
3. **CI e artefato.** Siga [CI e identidade de artefatos](references/ci-and-artifacts.md). Reuse os workflows e comandos do projeto; CI de teste, de publicação e de deploy são autorizações diferentes. YAML válido ou actionlint não provam que um job rodou: com execução remota autorizada, acompanhe o run do commit certo até o resultado final. Construa o artefato final e registre origem, versão, checks e digest, ou o commit quando a plataforma publica do Git; não troque o artefato testado por outro build sem revalidar. Mantenha separado o que foi verificado localmente e o que foi verificado na CI. No modo preparar, entregue plano e artefatos e marque as verificações remotas como pendentes.
4. **Publicação.** Confirme que os checks obrigatórios correspondem ao conteúdo final e que a autorização cobre artefato, conta, destino e efeito. Peça a autorização da recuperação junto com a da publicação, antes da mudança externa, e use o fluxo de release do projeto em vez de um push genérico. Siga o destino de cada entrega:
   - Relatório ou site estático: [Quarto e páginas estáticas](references/archetype-a-ghpages.md); HTML, PDF, MECA e Binder só se o contrato pedir.
   - App ou serviço: imagem, site ou serviço na plataforma escolhida, com digest e rollout real; em plataforma que publica do Git ou de um bundle, como Streamlit Community Cloud, shinyapps.io ou Posit Connect, registre o commit ou bundle e o ID do deploy. Preview não autoriza produção. Migração de banco tem plano próprio, e rollback da aplicação não desfaz dados.
   - Job agendado: o artefato é o commit do job com sua configuração, e publicar é ativar o agendamento, com segredos no cofre do destino e escopo mínimo.
   - Pacote: o pacote real da linguagem; em Python, confira wheel, sdist e entrypoints. GitHub Release, PyPI e outro registry são ações distintas; use identidade de menor privilégio, como trusted publishing já configurado.

   Comando aceito, URL emitida ou job iniciado não provam conclusão: registre o ID e acompanhe até o estado final, ou declare pendente. Não repita uma publicação ambígua sem verificar se ela já aconteceu.
5. **Smoke e aceite.** Siga [smoke tests e recuperação](references/smoke-and-healthcheck.md). Confira o destino publicado e a versão do artefato, não só se uma URL responde. Teste status, conteúdo e a jornada mínima, com timeout e tentativas limitadas, sem escrever em dados reais nem agir em contas de usuários; ler com credencial só de leitura autorizada pode, e smoke que escreve ou envia mensagem precisa de escopo, destino e limpeza autorizados. Num job agendado, o smoke inclui a primeira execução no horário previsto. Build ou diagnóstico local não é smoke nem deploy remoto. Com falha, interrompa a promoção, guarde logs sem segredos e recupere só conforme o plano autorizado; fora dele, apresente o diagnóstico e a ação necessária. Depois de recuperar, verifique o destino de novo. O aceite final é do usuário: build, deploy ou teste aprovados não o substituem.

## Estado e retomada

Ao parar ou transferir, deixe objetivo, modo, gate, artefato e destino, o que foi autorizado e quando, os checks e IDs reais, as pendências e o próximo passo autorizado. Ao retomar, confira base, artefato e destino antes de reaproveitar checks ou aprovações. Se o pedido termina na preparação, entregue o que está pronto e a ação pendente; não publique para completar a esteira. Sem resposta do usuário a um pedido de autorização, pare no estado atual com a ação pendente registrada.

## Especialistas e ferramentas

Carregue especialistas de CI, plataforma, empacotamento ou revisão só para a lacuna atual; skill ausente não significa ferramenta ausente. Não use cadeia editorial em todo commit nem checklist de lançamento de produto num pacote local simples. Conectores podem consultar runs e deployments ou executar uma ação já autorizada. Graphify é opcional: não construa nem publique grafo sem pedido, e confira o conteúdo interno antes de expô-lo.
