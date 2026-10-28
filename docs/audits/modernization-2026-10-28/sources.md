# Pesquisa oficial e compatibilidade

Finalidade: fundamentar propostas sem copiar manuais. Consumidor: mantenedor que aprovar MOD e executor que precisar conferir capacidade do host. Consulta: 2026-10-28, documentação online mutável; páginas sem versão normativa fixa não foram tratadas como versões de binários instalados. URLs antigas OpenAI redirecionaram ao ChatGPT Learn. Nenhum recurso dependente de conta foi considerado habilitado pela simples leitura.

| Fonte primária consultada | Evidência utilizada e decisão | Compatibilidade e limite |
|---|---|---|
| [Agent Skills specification](https://agentskills.io/specification) | `SKILL.md`, identidade e descrição, recursos opcionais e progressive disclosure | Formato comum; não padroniza gates, task.md ou permissões do host |
| [Build skills](https://learn.chatgpt.com/docs/build-skills) | Descoberta por metadados e leitura posterior; `agents/openai.yaml` opcional | Usar descoberta nativa Codex; configuração específica não deve ser imposta aos outros hosts |
| [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | Instruções de projeto com escopo | Reservar para convenções do repo; não duplicar todo procedimento de skill |
| [Codex GitHub review](https://learn.chatgpt.com/docs/third-party/github) | Revisão por `@codex review` e regras de revisão em AGENTS.md | Disponibilidade depende da integração/conta; comentar em PR é ação externa e exige autorização |
| [OpenAI skills catalog](https://github.com/openai/skills) | Exemplos reutilizáveis do formato | Branch main mutável; não copiar ou instalar pacote sem revisão de origem/licença |
| [Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Casos representativos, avaliação orientada por critérios e repetição | Adotar método no harness local; não exigir API hospedada ou orçamento pago |
| [Claude Code skills](https://code.claude.com/docs/en/skills) | Skills locais e recursos específicos de invocação | Extensões Claude não são contrato comum Agent Skills; descoberta real não foi testada aqui |
| [Antigravity skills](https://antigravity.google/docs/skills?tab=ide) | `.agents/skills` e raiz de usuário documentadas | App/IDE e CLI têm documentação própria; conferir versão do host antes de migrar |
| [Antigravity CLI migration](https://antigravity.google/docs/cli/gcli-migration/) | Perfis e migração específicos da CLI | Não unificar caminhos de usuário por analogia entre hosts |
| [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use) | Menor privilégio e fixação de actions por SHA completo | Recomendar SHAs de origem verificada e política de atualização; não alterar nesta auditoria |
| [Diátaxis](https://diataxis.fr/) | Separar necessidades de tutorial, procedimento, referência e explicação | Taxonomia útil para consumidores; não exige quatro arquivos por mudança |

Inferências desta auditoria: referências e recursos nativos devem preceder novas skills; um ADR só se justifica para decisão relevante, com contexto, alternativas, consequência e estado. Essas são escolhas propostas para este repositório, não obrigações dos hosts. Não se recomenda subagente obrigatório: capacidade varia por host e revisão independente precisa de autor diferente, autorização e evidência. O relatório foi elaborado por um agente, sem alegar revisão independente.

Não foram prescritas funcionalidades novas ou mudanças de modelo. A compatibilidade operacional permanece condicionada aos testes descritos em `docs/distribution/discovery.md`. Recursos de segurança/permissão são responsabilidade do host; Markdown de uma skill não substitui sandbox nem validação de ferramentas.
