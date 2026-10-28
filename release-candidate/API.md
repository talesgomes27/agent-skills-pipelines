# Fronteira pública e decisão de compatibilidade

Estado: análise concluída para esta candidata, sujeita à aprovação do mantenedor. Base 33b773c; nenhum runtime/critério histórico foi alterado.

A documentação publica CLIs e JSON para consumo externo; adotamos fronteira conservadora: scripts/skills.py (list,detect,manifest,install,doctor), scripts/evals.py (validate,matrix,grade), catálogo, recibos gerenciados e consultas da skill-loader são interfaces públicas. Funções Python internas e journals de experimentos não são APIs estáveis; seus snapshots continuam evidência preservada.

## Contratos

| Superfície | Entrada / saída / semântica |
|---|---|
| Catálogo | distribution/catalog.schema.json, version=1, release SemVer numérica; oito skills e seis bundles. A CLI acrescenta unicidade, pertencimento dos bundles e nomes válidos. |
| Instalador | Flags/destinos documentados preservados. list devolve catálogo; detect devolve candidatos/executáveis; manifest devolve entries/path; install devolve dry_run/plan com action,destination,mode,installed_release,source_release. doctor devolve root/checks, integridade/versões conforme fonte ou instalação gerenciada. Campos de versão anterior podem ser null. |
| Recibo | .meta-skills-install.json, version=1, skills indexadas por nome, source/mode/release/files. Estado gerenciado pelo instalador, não editar como mecanismo de atualização. Hash por arquivo, proteção de cópia alterada, recuperação por pacote, não lote transacional. |
| Harness — casos/traces | Casos version=1 e perfil operacional vigente; traces seguem evals/result.schema.json. Métricas omitidas significam desconhecido; metrics:null não é válido. Pares/IDs conhecidos são checagens adicionais do grade. |
| Harness — saída | validate: status/cases/skills/kinds; matrix: cases/id/skill/kind/prompt; grade: status processed, evaluation, coverage expected/observed/complete/missing, results e summary por condição. Totais desconhecidos são null, metric_observations conta observações. |
| Erros / exit | skills: 0 sucesso, 1 erro, 2 dependência indisponível. evals: 0 processamento, inclusive evaluation failed/incomplete, 1 entrada inválida. Erros tratados JSON incluem status/error; erros de argparse ficam fora desse envelope. Consumidor deve conferir evaluation e coverage, não só exit. Não inferir estabilidade do texto humano de error ou de caminhos absolutos entre ambientes. |
| Loader | Configuração de biblioteca, saída JSON e caminhos resolvidos documentados; requer PyYAML no ambiente de execução. Biblioteca fria externa não está embutida na distribuição. |

## Incompatibilidades públicas confirmadas

Desde a base 869444d, summary mudou totais ausentes de 0 para null; consumidores que esperavam apenas inteiros precisam adaptação. Entradas com métricas/campos extras inválidos antes tolerados agora são rejeitadas. Catálogo, identidades e recibo mantêm versão estrutural 1; major da release não implica elevar automaticamente cada schema.

Conclusão: **2.0.0 é a candidata preferencial para entrega unificada**, por compatibilidade do JSON público, não por prefixo de commit. Após autorização de 28/10/2026, o catálogo fonte e README recebem 2.0.0 exclusivamente na branch codex/meta-skills-2-candidate. A preparação anterior mantém seus artefatos identificados separadamente. Não há tag nem versão final publicada. Identificador do artefato contém candidate; 2.0.0-rc.1 não é usado em catalog.release porque o validador atual aceita somente X.Y.Z.

## Schema declarativo e perfil operacional

Draft 2020-12 reconhece integer como número matematicamente inteiro: 1.0 pode passar no schema. A CLI usa type(value) is int e rejeita esse valor após parse JSON. Preservamos essa restrição operacional, sem alterar a validação para produzir aprovação. O relatório schema-matrix.json registra ambos os resultados reais usando jsonschema 4.26.0, offline.

Schema aprovado é necessário, mas insuficiente: pertencimento de bundles, IDs e duplicatas de pares exigem CLI. Para interoperabilidade atual, serializar contagens como inteiros JSON sem ponto decimal. Documentar esse subconjunto e decidir futuramente se haverá normalização; nenhuma normalização foi implementada. O schema de entrada não descreve a saída agregada; contracts/grade-output.schema.json é uma proposta separada, verificada contra as saídas preservadas, sem alterar runtime. A matriz não constitui equivalência universal entre todo JSON Schema e a CLI.

## Limites dos contratos do instalador

Não existe JSON Schema publicado para recibo, install/doctor/detect/manifest; a fronteira é documentada e exercitada pela CLI e seus testes. Não apresentar catalog.schema.json como validação desses objetos. A chave version do recibo é comparada por igualdade Python: 1.0/true podem ser lidos como 1, enquanto o catálogo exige type(int). O instalador deve ser o escritor do recibo e produz 1 inteiro. Isso é permissividade operacional legada, não autorização para consumidores emitirem tipos alternativos; uniformização futura exige decisão e teste de migração. Recibos externos malformados não têm certificação completa por um schema nesta candidata.

Argumentos inválidos de argparse podem encerrar com 2 e texto em stderr; a promessa de erro JSON cobre erros tratados no corpo da CLI, não erros do parser, traceback inesperado ou terminação externa. Caminhos do manifest são absolutos da execução; não são identificadores portáveis persistentes.

## Quatro camadas de API

1. Skills: nomes, condições de ativação, limites de autorização e recursos relativos; texto de resposta não tem formato JSON universal garantido.
2. Distribuição/instalação: catálogo v1, CLIs e recibos descritos acima; caminhos dependem do destino, cópia preserva integridade registrada, link acompanha fonte viva.
3. Entrada das avaliações: cases version=1 e JSONL result.schema.json, com validações operacionais adicionais de tipos/IDs/pares.
4. Saída do harness: status do processamento separado de evaluation/coverage e summary com null para desconhecidos. Schema de saída proposto continua separado dos schemas de entrada.

A divergência tokens:1.0 é **compatibilidade documentada do perfil operacional**, preservada nesta candidata. Serializar contagens como 1, sem ponto decimal. Uma normalização futura ou equivalência declarativa completa exige mudança própria e migração; não é correção implícita desta CI.
