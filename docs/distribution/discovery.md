# Verificação de descoberta

Instalação em disco e descoberta pelo agente são evidências diferentes. Use esta sequência após instalar ou atualizar:

1. Execute `doctor` no destino para validar estrutura, integridade e versão registrada.
2. Recarregue ou inicie uma sessão nova do host.
3. Inspecione o catálogo exposto pelo host e confirme nome, descrição e caminho das skills selecionadas.
4. Execute pelo menos um caso positivo e um negativo de `evals/cases.json`; registre o trace no formato descrito em `docs/evals.md`.

## Estado observado em 2026-10-22

| Host | Destino | Evidência | Estado |
|---|---|---|---|
| Codex Desktop | `~/.agents/skills/` | Catálogo desta sessão exibiu as sete skills instaladas do repositório; `humanizer` permaneceu na implementação já disponível no ambiente | verificado para descoberta |
| Claude Code | `~/.claude/skills/` | Nenhuma sessão compatível foi usada nesta execução | pendente |
| Antigravity App/IDE | `~/.gemini/config/skills/` | Nenhuma sessão compatível foi usada nesta execução | pendente |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/` | Nenhuma sessão compatível foi usada nesta execução | pendente |

Esta tabela registra a evidência disponível, sem inferir autenticação ou funcionamento comportamental a partir da presença de arquivos. Atualize a data e a evidência quando o teste for repetido em cada host.
