# Evidências da Fase 2

Data: 2026-10-22. Ambiente de execução: Linux, Python do sistema com PyYAML 6.0.3.

## Entregas verificadas

- `release-and-ops-pipeline` consolidada após aprovação, com pacote anterior preservado em `docs/audits/legacy/release-and-ops-pipeline/`. Todos os arquivos da proposta foram comparados com os ativos e coincidem.
- CLI `scripts/skills.py`, catálogo de oito pacotes e seis bundles, schema JSON declarativo e dependência Python versionada.
- Matriz de compatibilidade, geração seletiva de manifesto Antigravity e contrato ilustrativo de ferramentas MCP em documentação própria.
- README atualizado: remove caminhos pessoais, métricas históricas apresentadas como atuais, instalação indiscriminada e proibição de referências relativas.

## Resultados

| Verificação | Resultado |
|---|---|
| `python3 -m unittest discover -s tests -v` | 16 testes passaram |
| `python3 scripts/skills.py doctor` | 8 pacotes fonte passaram |
| Instalação dos 8 pacotes por cópia em diretório temporário | Passou |
| Doctor das 8 cópias instaladas | Passou, incluindo integridade registrada |
| Repetição da instalação por cópia | 8 operações `unchanged` |
| Instalação dos 8 pacotes por link em diretório temporário | Passou |
| Doctor dos 8 links | Passou, estrutura e identidade do destino |
| Execução sem site-packages/PyYAML via `python3 -S` | Retornou indisponibilidade e exit 2 |
| Validador quick_validate de release consolidada | Passou |
| Parsing Python e JSON dos novos arquivos | Passou |
| Links locais do README e arquitetura | Passaram |
| `git diff --check` | Passou |

Os testes cobrem seleção explícita, nomes inválidos, exclusão no manifesto, detecção ambígua, dry-run sem gravação no destino, cópia idempotente, conflito antes de iniciar o lote, atualização explícita, preservação de edições locais, integridade de cópia, links e troca para cópia, YAML inválido/duplicado, referência ausente ou externa ao pacote, destino dentro da fonte, registros inválidos, recuperação de falha de gravação e instalação em caminhos de projeto/usuário isolados para os quatro perfis.

## Limites

Não foram alterados perfis globais reais, biblioteca fria ou seu índice. Não houve commit, push, implantação, instalação de MCP ou publicação. Windows/macOS e descoberta real nas aplicações não foram executados; a implementação usa APIs portáveis e oferece cópia sem depender de symlinks.

O doctor não executa instruções das skills, não valida qualidade editorial ou decisões do modelo e não comprova saúde de serviços remotos. O schema de catálogo é publicado, mas a CLI usa validações equivalentes locais e integridade referencial, sem um interpretador genérico de JSON Schema. O exemplo MCP é contrato arquitetural, não servidor entregue.

Instalação é transacional por pacote, não por lote completo nem entre processos concorrentes. Após falha de I/O no meio de um lote, os pacotes anteriores podem permanecer instalados e registrados. Não há testes ou promessa de tolerância a encerramento abrupto do processo ou falha de energia.
