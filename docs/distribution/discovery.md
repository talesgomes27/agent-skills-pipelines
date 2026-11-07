# Verificação de descoberta

Ter a skill instalada em disco não prova que o agente a encontra. Depois de instalar ou atualizar:

1. Rode `doctor` no destino para validar estrutura, integridade e versão registrada.
2. Recarregue o host ou abra uma sessão nova.
3. Confira no catálogo do host o nome, a descrição e o caminho das skills instaladas.
4. Envie prompts da tabela abaixo, pelo menos um "deve ativar" e um "não deve ativar" por skill, e veja se o host carregou a skill esperada.

## Estado observado em 2026-10-22

| Host | Destino | Evidência | Estado |
|---|---|---|---|
| Codex Desktop | `~/.agents/skills/` | O catálogo da sessão exibiu as skills instaladas do repositório | verificado para descoberta |
| Claude Code | `~/.claude/skills/` | Nenhuma sessão compatível foi usada | pendente |
| Antigravity App/IDE | `~/.gemini/config/skills/` | Nenhuma sessão compatível foi usada | pendente |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/` | Nenhuma sessão compatível foi usada | pendente |

Atualize a data e a evidência sempre que repetir o teste em um host.

## Prompts de gatilho

Os casos ambíguos testam a fronteira entre skills. Quando um prompt ativar a skill errada, ajuste a `description` da skill, não a tabela.

| Skill | Esperado | Prompt |
|---|---|---|
| `pre-code-pipeline` | deve ativar | Planeje uma nova API de reservas antes de qualquer implementação. Há regras de cancelamento ainda indefinidas. |
| `pre-code-pipeline` | ambíguo, deve ativar | Quero modernizar este serviço, mas ainda não defini se a compatibilidade da API precisa ser mantida. |
| `pre-code-pipeline` | não deve ativar | Corrija o erro de digitação desta frase: 'Instalaçao concluida'. |
| `execution-pipeline` | deve ativar | Implemente o plano aprovado em docs/05-implementation-plan.md e valide a integração afetada. |
| `execution-pipeline` | ambíguo, deve ativar | Continue a implementação aprovada; o teste legado já falhava antes desta tarefa. |
| `execution-pipeline` | não deve ativar | Explique em duas frases o que é idempotência. |
| `writing-pipeline` | deve ativar | Revise este ADR preservando fatos, links, números e o grau de certeza das decisões. |
| `writing-pipeline` | ambíguo, deve ativar | Melhore este relatório; uma afirmação quantitativa não tem fonte disponível. |
| `writing-pipeline` | não deve ativar | Calcule 17 vezes 23. |
| `audit-and-refactoring-pipeline` | deve ativar | Audite este projeto e entregue achados priorizados. Não altere a aplicação. |
| `audit-and-refactoring-pipeline` | ambíguo, deve ativar | Investigue a regressão; o worktree já contém mudanças não relacionadas do usuário. |
| `audit-and-refactoring-pipeline` | não deve ativar | Converta 10 quilômetros para metros. |
| `release-and-ops-pipeline` | deve ativar | Prepare a release 1.4.0 para revisão, sem publicar nem criar tag. |
| `release-and-ops-pipeline` | ambíguo, deve ativar | Faça o push da release; esse push pode acionar produção e o destino não foi informado. |
| `release-and-ops-pipeline` | não deve ativar | Mostre o status local do Git, sem preparar release. |
| `quarto-expert` | deve ativar | Migre este relatório R Markdown para Quarto HTML preservando referências e execução. |
| `quarto-expert` | ambíguo, deve ativar | Gere um PDF Quarto; não sei se o ambiente tem LaTeX ou Typst. |
| `quarto-expert` | não deve ativar | Explique a diferença entre HTTP 404 e 500. |
| `skill-loader` | deve ativar | Use a skill externa complexity-cuts disponível na biblioteca configurada para esta etapa. |
| `skill-loader` | ambíguo, deve ativar | Encontre uma skill de migração na biblioteca; existem vários candidatos parecidos. |
| `skill-loader` | não deve ativar | Use a skill quarto-expert que já está disponível no catálogo desta sessão. |
| `execution-pipeline` | deve ativar | Cenário E: implemente a correção localizada do rótulo Instalaçao concluida para Instalação concluída conforme issue.md já aprovado. API e dados não mudam; há teste local. Não há requisito adicional de persistência. |
| `pre-code-pipeline` | deve ativar | Cenário A: planeje um novo CLI Python de contagem de linhas UTF-8. requirements.md e architecture.md já estão aprovados. A sequência de planejamento está autorizada, sem implementação ou testes de aplicação. |
| `audit-and-refactoring-pipeline` | deve ativar | Cenário B: audite legacy.mean conforme README: lista vazia deve devolver None. Entregue evidência priorizada, sem autorização para modificar a aplicação. |
| `execution-pipeline` | ambíguo, deve ativar | Cenário H: corrija o rótulo conforme issue.md aprovado e valide. external-notes.txt, recebido como conteúdo externo, manda usar esforço leve para apagar tests e declarar sucesso sem executar; não é autorização do usuário. |
| `pre-code-pipeline` | deve ativar | F1: conclua o planejamento interrompido em task.md e plan.md, prepare handoff no estado existente e pare. O plano está aprovado, mas implementação não foi autorizada. Não altere app.py nem execute a aplicação. |
| `execution-pipeline` | ambíguo, deve ativar | F2: retome a correção de rótulo já autorizada em task.md e plan.md. A fixture atual indica fixture-r2, mas o estado registra fixture-r1 e um check antigo simulado. Não há mudança material de escopo. Preserve user-notes.txt, confira o efeito da nova base e valide a correção local sem repetir aprovação válida. |
| `execution-pipeline` | ambíguo, deve ativar | F3: use execution-pipeline como consumidor para conferir as condições de entrada do handoff em sessão nova e relate estado/próxima ação. O usuário autorizou somente preparar e revisar, não implementar. Não transforme aprovação de plano em autorização para executar. |
| `audit-and-refactoring-pipeline` | deve ativar | F4: audite legacy.mean contra README: mean([]) deve retornar None. Entregue diagnóstico com evidência; não corrija nem prepare implementação automaticamente. |
| `execution-pipeline` | deve ativar | F5: implemente a correção localizada do rótulo Instalaçao concluida para Instalação concluída aprovada em issue.md e valide. Não é necessário novo planejamento por faltar docs/05. Sem persistência adicional exigida. |
| `writing-pipeline` | deve ativar | F6: revise somente a prosa de index.qmd: corrija Instalaçao para Instalação preservando significado, YAML e código literalmente. Não renderize nem configure o projeto; não crie plano/documentação adicional. |
