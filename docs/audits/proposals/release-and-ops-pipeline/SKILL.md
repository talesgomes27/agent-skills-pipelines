---
name: release-and-ops-pipeline
description: "Prepara e verifica releases após implementação ou auditoria aprovadas: saneamento, versão, CI, publicação autorizada e smoke tests vinculados ao artefato e destino."
---

# Preparação, publicação e verificação de releases

Entregue o artefato aprovado no destino autorizado, com evidência de identidade, execução e recuperação. O pedido pode autorizar apenas preparação local; não o amplie para commit, push, publicação de pacote ou produção.

## Entrada e estado

- Leia instruções de release do projeto, handoff, `task.md`, `docs/00_archetype.md` e evidências de implementação/auditoria. Preserve classificação e proveniência. Se não houver arquétipo, use declaração explícita dos contratos/pedido; esclareça apenas se a lacuna impedir escolher o artefato correto.
- Identifique escopo, commit/base, arquivos staged/unstaged/não rastreados relevantes, versão pretendida, artefato e destino. Preserve trabalho do usuário; não faça staging de tudo nem exija árvore limpa apagando arquivos.
- Registre o modo: preparar, publicar preview, publicar release ou implantar produção. Confirme conta/projeto, repositório/registry, branch/tag, ambiente e efeitos indiretos conhecidos. Push pode acionar produção via CI.
- Mantenha seção de release em `task.md`, sem sobrescrever fases anteriores: gate, identidade do artefato/commit, destino, checks, autorizações e resultado. Diferencie preparado, aguardando autorização, submetido, em execução, concluído e falhou/parcial.
- Aprovação de gate valida os artefatos dessa etapa. Para ações externas, use a autorização já concedida quando cobrir o destino e o efeito; se faltar, apresente primeiro o resultado concreto a publicar e peça a autorização final. Mudança material de artefato/destino invalida a aprovação correspondente.

## Gates

Ao concluir cada gate aplicável, apresente resultado e pendências, registre o aceite real e espere aprovação explícita antes de avançar. Não repita confirmações já concedidas para a mesma ação. Uma etapa não executada ou dispensada não recebe sucesso fictício.

### 1. Saneamento e prontidão do conjunto de release

Consulte [saneamento e dados](references/pre-push-sanitation.md). Revise arquivos e artefatos que realmente serão enviados, lockfiles e evidências de checks. Não refatore a aplicação nem migre stack como parte de uma inspeção pré-push.
Use ferramentas existentes para segredos e dependências quando aplicáveis, registrando escopo, versão, resultado e limitações. Falha de ferramenta não equivale a ausência de achados. Não exponha valores secretos no relatório.
Verifique pré-requisitos do build necessário; ausência de browser/engine deve ser resolvida conforme escopo e permissões, sem instalação global implícita.
Saída: conjunto de release delimitado, checks de prontidão e bloqueios identificados.

### 2. Versão, notas e plano de publicação

Preserve a política de versões do projeto. Para SemVer, identifique API/contrato público e incompatibilidades antes de propor PATCH/MINOR/MAJOR; não deduza apenas do prefixo de commit.
Prepare changelog/notas a partir das mudanças reais e do intervalo correto, usando `writing-pipeline` quando necessário. Atualize metadados locais autorizados de modo consistente; não recrie tag publicada ou reescreva histórico remoto.
Defina arquivos do commit, branch/tag e comandos do fluxo de release existente. Commit/tag só são criados se autorizados; preparar uma proposta não exige fazê-los. Se a versão alterar o conteúdo do pacote, o build/check pertinente deve validar o conteúdo final.
Saída: versão/notas revisáveis e plano com artefato, destino, efeitos de push e estratégia de recuperação.

### 3. CI e artefatos verificáveis

Consulte [CI e identidade de artefatos](references/ci-and-artifacts.md). Reutilize workflows e comandos reais da stack, com jobs e permissões proporcionais. CI de teste, publicação e deploy não são a mesma autorização.
Valide sintaxe e semântica possíveis localmente; YAML válido ou actionlint não provam que um job executou. Quando houver execução remota autorizada, confira o run/check correspondente ao commit correto e espere resultado terminal com observação limitada.
Construa e identifique o artefato final, registrando origem, versão, checks e digest/revisão quando aplicáveis. Não substitua o artefato testado por rebuild diferente sem revalidação pertinente.
Saída: configuração revisada e evidências locais/remotas claramente separadas. No modo preparar, entregue o plano/artefatos e marque verificações remotas pendentes, sem disparar publicação.

### 4. Publicação ou implantação autorizada

Antes de agir, confirme que os checks obrigatórios correspondem ao conteúdo final e que a autorização cobre artefato, conta, destino e efeito. Prepare um procedimento de recuperação e sua autorização antes da mudança externa. Não use ferramenta genérica de push quando o projeto tem fluxo de release próprio.
- **A:** use [publicação Quarto/Pages](references/archetype-a-ghpages.md) se esse for o destino escolhido. HTML, PDF, MECA e Binder são entregáveis condicionais, não um pacote obrigatório.
- **B:** publique a imagem/site/serviço na plataforma escolhida; preview não autoriza produção. Registre revisão/digest e rollout real. Migração de banco exige plano de compatibilidade próprio; rollback de aplicação não desfaz dados.
- **C:** construa o pacote/binário da linguagem real. Para Python, verifique wheel/sdist e entrypoints do artefato; publicar GitHub Release, PyPI e outro registry são ações distintas. Use identidade de menor privilégio, como trusted publishing quando já configurado e adequado.
Comando aceito, URL emitida e job iniciado não comprovam conclusão. Registre ID do deployment/release e acompanhe até estado final ou devolva explicitamente pendente/bloqueado. Não execute novamente publicação ambígua sem verificar se ela já ocorreu.
Saída: publicação confirmada ou estado parcial verificável, sem alegar deploy a partir de build local.

### 5. Smoke tests e aceite

Consulte [smoke tests e recuperação](references/smoke-and-healthcheck.md). Confira o destino realmente publicado e sua identidade de versão/artefato, não apenas disponibilidade de uma URL antiga.
Teste status, conteúdo/contrato e jornada mínima pertinente, com timeout e tentativas limitadas. Preserve dados reais e contas de usuários; smoke com escrita exige escopo e limpeza autorizados. Diagnóstico local de engine não é smoke remoto.
Se houver falha, interrompa promoção e preserve logs sem segredos. Execute recuperação somente conforme plano/autorização aplicável; se não estiver coberta, apresente o diagnóstico e a ação concreta necessária. Verifique novamente o destino após recuperar.
Saída: relatório de checks, artefato/destino observado, pendências e estado real. Registre aprovação final apenas quando dada pelo usuário; build/deploy/teste aprovado tecnicamente não fabrica aceite humano.

## Contexto e integração

Núcleo usa Git, filesystem, CLI e conectores do host disponíveis. Especialistas de CI, plataforma, empacotamento e revisão são carregados somente para a lacuna atual. Skill ausente não prova ferramenta ausente; autenticação não amplia autorização.
Não carregue uma cadeia editorial para todo commit nem um checklist de lançamento de produto para um pacote local simples. O escopo do projeto e suas verificações obrigatórias prevalecem.
Graphify é opcional para documentação arquitetural solicitada. Não construa ou publique grafo só porque o executável está disponível; confira cobertura, atualidade e conteúdo interno antes de expor artefatos.
MCP/conector pode consultar runs e deployments ou executar ação já autorizada, sem servidor novo obrigatório. Registre IDs e resultados reais. Se o pedido acabar na preparação, entregue o que está pronto e a ação pendente; não publique para “completar” a esteira.
