---
name: execution-pipeline
description: "Use quando o usuário pedir para implementar ou continuar um plano já aprovado, vindo do planejamento ou de uma auditoria, com autorização para alterar o código."
---

# Execução de um plano aprovado

Implemente o plano em fatias pequenas e verificáveis, com evidência de que funcionam. Os cinco gates organizam o aceite; nenhum deles exige um documento próprio.

## Antes de começar

1. Leia as instruções locais (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`), o estado do projeto e o plano aprovado: `docs/05-implementation-plan.md` ou o plano aprovado na conversa, vindos do pré-código, ou o plano e as restrições encaminhados por uma auditoria. Leia requisitos e arquitetura só nas partes que a tarefa usa.
2. Confirme que o plano foi aprovado e que implementar está autorizado. Vale a aprovação registrada no estado do projeto ou dada pelo usuário na conversa. Sem plano aprovado, pare e encaminhe para `pre-code-pipeline`, exceto numa tarefa pequena: local (arquivos do projeto ou os que o usuário apontou), reversível, sem efeito externo (escrita ou envio pela rede, contas, mensagens, produção) e sem mudar interface que outro sistema usa. Ler páginas ou APIs públicas pode, com as regras de coleta da [referência C](references/archetype-c.md). Nela o pedido é o plano: diga em poucas linhas o que vai fazer e como vai verificar, implemente e verifique sem abrir os gates. Se ela mexe em arquivos do usuário, mostre antes o que vai mudar, não sobrescreva nada e deixe como desfazer. Quando a tarefa precisa de escopo antes (fontes, cuidados com os dados, formato), use a entrega pontual da `pre-code-pipeline`: o aceite dela vale como plano, e a entrega segue sem abrir os gates, só com as paradas do modo contínuo.
3. Use o arquétipo registrado em `docs/00_archetype.md` ou no contrato: A = análise e modelos, B = aplicações (site, API, dashboard), C = automações (script, CLI, job agendado, ETL). Sem registro, infira pelo contexto quando for óbvio (um script de linha de comando é C) e diga que inferiu; pergunte só quando a escolha muda uma decisão.
4. Descubra os comandos reais em manifests, lockfiles, scripts e CI. Rode os checks afetados antes de mudar qualquer coisa e anote o que já falhava. Falha preexistente fora do escopo não bloqueia a entrega, mas aparece no relatório separada das falhas novas.
5. Preserve as alterações do usuário que já estão na árvore.

## Esforço

Diga qual escolheu e por quê: **leve** para correção local sem mudar interface ou dados, **padrão** para capacidade ou integração comum, **rigoroso** para segurança, dados sensíveis, migração, interface pública ou impacto incerto. O esforço define quanto verificar e documentar. Diff curto numa interface pública continua rigoroso.

## Regras de trabalho

- Fique no escopo e nas interfaces do plano. Mudança de requisito volta ao planejamento; falha de implementação se corrige na própria tarefa.
- Para comportamento novo ou corrigido, escreva o teste antes quando o plano prevê, veja-o falhar pelo motivo esperado, implemente e rode de novo. Em código legado sem teste, caracterize o comportamento antes de mudá-lo.
- Não enfraqueça testes nem troque dados reais por sintéticos para mostrar sucesso.
- Valide com as ferramentas do projeto, por exemplo `uv run pytest` e `uv run ruff check .`. Comece pelos checks afetados e amplie conforme o risco.
- Mantenha a stack exigida: não troque biblioteca, framework, estimador ou formato por conveniência. Se faltar algo indispensável, bloqueie só a tarefa afetada e explique o que falta.
- Testes, migrações, notebooks e builds executam código. Rode em ambiente de desenvolvimento ou teste, nunca contra produção salvo a leitura do item seguinte, e não instale nada globalmente.
- Ler dados reais com uma credencial só de leitura que o usuário autorizou vale quando o plano prevê; o que for para testes, logs ou relatórios segue a política de dados. Escrever, enviar mensagem, cobrar ou publicar usa o recurso de teste do plano (banco, pasta, chat ou conta) ou uma autorização específica para aquela execução.

## Modo

- **Assistido** (padrão): mostre o resultado e espere o aceite ao fim dos Gates 3 e 5. Nos outros, apresente e siga, com as paradas do modo contínuo; eles entram no aceite seguinte.
- **Contínuo**: se o usuário autorizou o plano de ponta a ponta, avance pelos gates sem pedir de novo. Pare quando o escopo mudar, surgir uma decisão bloqueante, houver conflito com trabalho existente ou risco de perda.

Implementar não inclui commit, push, publicação ou deploy. Faça essas ações só quando o usuário pedir.

## Gates

Leia só a referência do arquétipo confirmado: [A](references/archetype-a.md), [B](references/archetype-b.md) ou [C](references/archetype-c.md). Em projeto híbrido, leia também a do domínio secundário, só nas partes que ele usa.

1. **Núcleo e contratos.** A menor fatia de lógica do plano, na estrutura e na linguagem existentes, com testes de contratos, limites e falhas relevantes.
2. **Integração.** Ligue a lógica à fonte de dados, API, notebook, serviço ou CLI prevista e rode o fluxo principal em ambiente controlado, incluindo as falhas de fronteira importantes.
3. **Saídas.** Apenas as figuras, telas, serializações ou mensagens previstas. Confira unidades, semântica e acessibilidade conforme a referência do arquétipo.
4. **Documentação.** Atualize README, relatório ou referência de API a partir do que foi implementado. Confira exemplos, flags e números, e separe resultado real de esperado.
5. **Revisão e build.** Revise o diff quanto a comportamento, qualidade dos testes e fidelidade da documentação. Rode lint, tipos, testes e build do projeto e corrija o que for concreto. Com um check obrigatório falhando ou não executado, a entrega não está validada. Não chame de revisão independente a revisão que você mesmo fez.

Gate que não se aplica fica marcado como não aplicável, com o motivo.

## Estado e retomada

Registre o progresso onde o projeto já registra: `task.md`, issue, PR ou a própria resposta. Não crie arquivo de estado só para isso. Ao parar, deixe o que foi feito, os checks com comando e resultado, o que falta e qual é o próximo passo autorizado.

Ao retomar, confira a base e o diff antes de reaproveitar checks anteriores e refaça os que a mudança afetou.

## Especialistas e ferramentas

Carregue outra skill só para uma lacuna concreta da tarefa: `quarto-authoring` (Posit) para autoria Quarto e `quarto-expert` para ambiente, render e ABNT, `writing-pipeline` para revisão editorial, `scheduled-automation` para job agendado, `personal-data` para dados de pessoas, a skill oficial do framework quando instalada, como `developing-with-streamlit` ou `shiny-for-python`. A especialista diz como fazer; escopo, gates e autorizações continuam os desta skill. Skill ausente não significa ferramenta ausente; consulte a documentação oficial da versão em uso. Graphify, MCPs e conectores são opcionais, e o que eles sugerirem precisa ser confirmado no código.

## Entrega

Ao fim do Gate 5, informe alterações, checks executados, limitações e próximo passo. Para publicar, encaminhe a `release-and-ops-pipeline`; sem autorização, pare no estado preparado.
