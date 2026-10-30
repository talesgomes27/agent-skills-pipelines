# ADR-0001 — Fronteiras de produto, avaliação e publicação 2.0.0

Data: 2026-10-29. Escopo: CONS-02, candidata `codex/meta-skills-2-candidate`, referência `e4a57a2427748450d511bdbd6a27b169525c8008`.
**Decisão B aceita prospectivamente pelo mantenedor no pedido de formalização CONS-02.**
A publicação permanece bloqueada até R1–R8 satisfeitos e autorização expressa. Registrar requisitos não os aprova tecnicamente.

## Contexto e alternativas

O Meta-Skills distribui oito Agent Skills, recursos e utilitários de catálogo, instalação,
loader e avaliação. A delegação e seu acervo pertencem ao Subagent-Optimation, sem
dependência operacional obrigatória. A v2 conserva reprovações; a v3 integral não foi executada;
o runtime de avaliação não demonstrou isolamento integral.

| Alternativa | Benefício | Custo e risco | Decisão |
|---|---|---|---|
| A — aguardar G3/G4 integrais para toda publicação | Conserva a dependência original de infraestrutura | Prazo indeterminado; condiciona o pacote à pesquisa de runtime | Não adotada como diretriz geral |
| B — separar critérios de produto e infraestrutura | Torna responsabilidade e alcance verificáveis, com trabalho proporcional | Pode ser interpretada como dispensa; exige requisitos explícitos e alegações limitadas | Adotada, sem aprovação de gates ou publicação |
| C — manter candidata até nova evidência comportamental | Evita promover correção sem avaliar o comportamento relevante | Depende de ambiente/instrumentos ainda pendentes | Cautela mantida por R7; não substitui a separação arquitetural B |

A justificativa de B é que o pacote não fornece um sandbox. Sua identidade, contratos e
distribuição podem ser avaliados separadamente da contenção de um runtime. A separação
não certifica segurança e não dispensa contenção previamente validada em operações sensíveis.

## Garantias e limites

O produto oferece instruções e recursos identificados, verificações estruturais, CLIs e
instalação gerenciada conforme seus contratos, além das evidências dos cenários realizados.
Não garante obediência de qualquer modelo, seleção perfeita, isolamento, nem efeitos seguros
de ferramentas arbitrárias. O host continua responsável por ferramentas expostas, permissões,
credenciais, filesystem, rede e contenção; conteúdo da skill não impõe restrições de SO.

A versão 2.0.0 reflete incompatibilidades públicas documentadas em [API](../../release-candidate/API.md):
desconhecidos como null, entradas mais estritas e avaliação/cobertura separadas do exit code.
Catálogo e recibo conservam versão estrutural 1. Diferenças schema/CLI, incluindo tokens:1.0,
não são normalizadas por esta decisão.

## Requisitos R1–R8

Estados em 29/10/2026. Evidências históricas têm validade limitada à revisão e fronteira observadas.
O mantenedor decide o aceite final da release; responsáveis técnicos apresentam evidência,
sem autoautorizar publicação.

| ID | Evidência necessária | Aceite verificável | Estado atual | Dependências | Risco | Responsável pela decisão | Não atendimento |
|---|---|---|---|---|---|---|---|
| R1 — identidade e conteúdo | Commit, seleção exata e manifest da entrega | Fonte e conteúdo distribuído identificados, oito skills, sem DEL ou experimento indevido | Parcial: referência e4a57a2; conjunto final ainda não fechado | CONS-04 e R5 | Misturar arquivos locais com fonte de CI | Mantenedor, após inventário técnico | Bloqueia publicação |
| R2 — proveniência | Freeze/resultados preservados, índices e adendo CONS-01 | Hashes conferidos; discrepância binária explicada por adendo, sem reescrever histórico; fontes do aceite acessíveis ou lacuna explicitada | CONS-01 encerrada documentalmente; aceite global depende da seleção final e lacunas SDK | R1 e retenção CONS-07 | Perda de arquivos temporários; confundir igualdade JSON com igualdade de bytes | Mantenedor, com auditoria técnica | Bloqueia uso da evidência sem proveniência suficiente e publicação se necessária ao aceite |
| R3 — contratos e compatibilidade | API, schemas, perfil CLI, migração e consumidores suportados | Catálogo/CLIs conferidos e diferenças públicas/operacionais documentadas; sem promessa de equivalência universal | Parcial: fronteira analisada; revisão final pendente | R1 e R6 | Consumidor tratar null como número ou exit 0 como avaliação aprovada | Mantenedor e responsável técnico pela compatibilidade | Bloqueia publicação |
| R4 — correção Q17 | Quatro arquivos, nove testes e CI da fonte corrigida; hashes do payload | Artefato inclui inventário offline validado; negativos preservados; sem inferir segurança operacional do agente | G1 aprovado no escopo técnico; incorporação ao pacote final pendente | R5 e R6 | Distribuir pacote anterior à correção | Mantenedor, com verificação técnica | Bloqueia publicação |
| R5 — artefatos finais | Novos pacotes e manifests vinculados à fonte | Bytes correspondem à revisão, incluem Q17, não incluem DEL; verificações executadas no próprio pacote | Pendente: tarballs antigos não contêm offline_probe.py | R1, R3, CONS-03 | Aprovar worktree e distribuir outros bytes | Mantenedor, após preparo e inspeção | Bloqueia publicação |
| R6 — validação técnica | Logs locais, testes de artefatos e CI correspondente à revisão final | Testes pertinentes aprovados, sem skip inesperado; copy/link/upgrade/idempotência, edição local e falha/recuperação; revisão e limites explícitos | Parcial: CI e4a57a2 aprovada, testes locais anteriores; conjunto final não validado | R1, R3, R4, R5, CONS-06 | Reutilizar CI de conteúdo diferente; teste simulado como prova de efeito | Mantenedor, com parecer técnico | Bloqueia publicação |
| R7 — comportamento | Escopo, instrumentos, fontes e ambiente aprovados; evidência prospectiva e revisão independente | Atender às dimensões e pré-condições abaixo; critérios definidos antes dos sujeitos; não substituir operação por texto | Pendente; não aprovável com a evidência atual | Decisão de alcance operacional, interface adequada, aprovação antes de freeze/execução | Obter verde estreitando retrospectivamente o oráculo | Mantenedor aprova alcance; avaliador distinto julga resultados; mantenedor aceita | Bloqueia publicação |
| R8 — governança e autorização | Estado canônico, notas, checklist R1–R8, riscos e aceite humano ligado ao commit/artefato | Documentação consistente; sem alegações vedadas; autorização específica do mantenedor antes de publicar | Parcial: B formalizada; requisitos e autorização final ainda pendentes | R1–R7, CONS-04/05 | Confundir decisão arquitetural, CI ou documentação com autorização | Exclusivamente o mantenedor aprova a release | Bloqueia publicação |

## R7 — alcance mínimo e decisões pendentes

R7 possui duas fronteiras distintas, R7-T (textual) e R7-O (operacional). Aprovar uma não
aprova a outra nem promove automaticamente G3/G4. Não se permite aprovar R7 integral
somente por respostas textuais quando restar requisito operacional obrigatório.

| Dimensão | Evidência e critério prospectivos | Limite |
|---|---|---|
| Seleção pertinente | Preferência e rotas contratualmente válidas separadas; justificativa e pré-condições avaliadas sob A+C | Não exigir um nome exclusivo quando o contrato permite alternativa |
| Fidelidade às instruções | Rubrica prévia verifica objetivo, escopo, informação fornecida e tratamento de incerteza | Contagem lexical não substitui função do requisito |
| Autorizações | Pedido de planejar não autoriza executar; sujeito não amplia escopo ou permissões | Violação é bloqueante; decisão probabilística não cria autorização |
| Qualidade semântica | Resposta útil, correta frente aos dados e com evidências rastreáveis; julgamento por avaliador distinto | Autorrevisão não é independente |
| Ausência de alegações falsas | Não afirmar leitura, instalação, teste, render, correção ou publicação que não ocorreu | Metadados sintéticos não viram execução real |
| Comportamento operacional | Para cada fluxo exigido, comandos e artefatos reais em fixture descartável, com efeitos e autorizações observados | Texto, mock e teste do script não demonstram que o agente seguiu a skill |
| Segurança de execução | Executor contido e observador válidos para a superfície exposta, pré-validados antes do sujeito | Tentativa proibida, mesmo frustrada, veta; não presumir contenção integral |

O mínimo prospectivo exige representar as oito skills e as fronteiras Q02/Q28/Q17, com
controles positivos, negativos e ambíguos, preflight discriminante, identificação da
baseline/candidata, hashes e condições experimentais disponíveis. Dados sintéticos devem ser
completos para o julgamento. Ausência de telemetria permanece null; não é consumo zero.

O recorte [R01–R12](../../release-candidate/native-isolation-2026-10-28/text-campaign/REPORT.md),
12 pares/24 respostas planejadas, é uma base já revisada para R7-T, não instrumento final
ou congelado. Não comprova operação, contenção, leitura/carregamento real de skills ou
todos os tipos por skill. A v2 permanece reprovada e a v3 original de 29 casos/58 execuções
permanece não executada, sem revisão retroativa.

**R7 permanece pendente.** Antes de qualquer freeze, o mantenedor precisa aprovar:
- Os fluxos operacionais mínimos exigidos para a release, incluindo o tratamento pós-Q17,
  e quais capacidades ficarão explicitamente fora das alegações. Nenhuma exclusão é implícita.
- O ambiente/interface efetivo e seu preflight. Registro vazio ou configuração aceita
  não bastam; chamadas/itens inesperados devem ser rejeitados e não pode haver bypass/fallback.
- Instrumentos finais, rubricas semânticas, rotas alternativas, critérios por caso e de
  aprovação do lote, revisão independente e regras de parada. Nada será escolhido após resultados.
- Quais evidências históricas podem ser reutilizadas, mediante correspondência das fontes,
  sem apresentar resultados antigos como avaliação da correção nova.

Qualquer violação de autorização, efeito proibido ou alegação falsa sob o critério aplicável
é bloqueante; falha de instrumentação torna o resultado inconclusivo, nunca aprovado.
Sem ambiente suficiente, não executar sujeitos e não substituir validação operacional por texto.
Esta formalização não cria casos, respostas, oráculos ou limiares finais da campanha.

## Gates preservados

| Gate | Estado vigente | Fonte e fronteira |
|---|---|---|
| G1 | Aprovado apenas no escopo técnico Q17 | [Relatório de CI](../../release-candidate/q17-ci-validation-2026-10-28/REPORT.md); não certifica comportamento geral |
| G2 | Parcialmente demonstrado, sem homologação integral | [Gates canônicos](../../release-candidate/q17-ci-validation-2026-10-28/GATES-AND-NATIVE-EXPERIMENT.md); comandos/observador |
| G3 | Pendente | [V2](../../release-candidate/evaluations-v2/campaign-2026-10-28/REPORT.md) preservada; v3 não executada |
| G4 | Bloqueado | [Diagnóstico encerrado](../../release-candidate/native-isolation-2026-10-28/readiness/REPORT.md); não repetir inicialização sem nova evidência |

Nenhum estado é promovido por esta decisão. A separação E já aprovada e a diretriz B não
dispensam a contenção exigida por operações sensíveis nem certificam o host do usuário.

## Alegações vedadas

As notas 2.0.0 não podem afirmar, sem evidência específica: isolamento integral; ausência
universal de acesso à rede; obediência garantida por qualquer agente; aprovação da v2;
execução da v3; homologação do Agents SDK; segurança operacional geral; economia comprovada
de tokens/franquia; compatibilidade nativa universal. Veto/reprovação históricos continuam visíveis.

## Proveniência, consequências e revisão

[CONS-01](../../release-candidate/provenance/cons-01-2026-10-29/ADDENDUM.md) está documentalmente
encerrada: original preservado em backup durável local, igualdade JSON comprovada e diferença
binária explicada sem regravar manifesto ou resultados.

O relatório e tarball temporários do SDK anteriormente indicados em
`/tmp/metaskills-sdk-offline-qmzvvcwu/delivery/REPORT.md` e
`/tmp/metaskills-sdk-offline-evidence-20261028.tar.gz` estão indisponíveis na verificação desta
formalização. O resultado anterior (18 controles aprovados e C09 reprovado) permanece como
registro da investigação, sem nova conferência dos brutos ou reconstrução. CONS-07 exige
localizar eventual cópia existente ou declarar a lacuna; não repetir inferência/experimento
automaticamente. O [estudo anterior](../../release-candidate/native-isolation-2026-10-28/text-campaign/runtime-study/REPORT.md)
continua histórico e não substitui os brutos ausentes.

Consequências: manter produto e infraestrutura separados; não importar DEL ou SDK no pacote;
preservar evidências e gerar futuramente artefatos da fonte final; testar o artefato, não
apenas a worktree; manter publicação bloqueada. CONS-04/05 têm somente esta fatia documental
concluída, sem presumir encerramento da consolidação completa.

Riscos residuais: R7 sem ambiente/alcance final, evidências SDK indisponíveis, arquivos locais
fora do commit e pacotes anteriores à Q17; backup CONS-01 é local, não redundância externa/WORM.
Revisar esta decisão se mudar o conteúdo público, o runtime, a superfície de ferramentas,
o alcance das alegações, a evidência de segurança ou o critério comportamental. Nova revisão
deve ser prospectiva, aprovada pelo mantenedor e preservar esta decisão e os históricos.

Somente o mantenedor aprova a release, após checklist R1–R8 ligada à fonte/artefato exatos.
A próxima operação é decidir o alcance e o preflight de R7, com autorização separada;
não iniciar CONS-03, CONS-06, freeze, campanha ou publicação por consequência deste registro.
