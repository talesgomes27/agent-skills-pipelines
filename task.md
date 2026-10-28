# Estado de melhoria do ecossistema

## Estado vigente — MOD-008 / 2026-10-28

- Objetivo/estado/base: experimento C/D/H concluído; candidata de referências rejeitada, pois melhora discriminável não foi demonstrada; base `bc41c7e`. Nenhum aceite humano presumido.
- Escopo/autorização: pedido atual para commitar MOD-007 e prosseguir somente à MOD-008; dois agentes C/D/H isolados autorizados expressamente. MOD-007 commitada em `bc41c7e`, sem push; resultado failed em I preservado.
- Executor: agente principal via execution-pipeline, único integrador; workers escreveram somente fixtures temporárias, sem Git de escrita, rede ou publicação.
- Artefatos/decisões: [resultado e critérios](docs/audits/modernization-2026-10-28/mod-008.md), [protocolo, candidata e lote](evals/experiments/mod-008/README.md). Doze execuções completas, 23/23 rubricas por condição; grader failed por literal ausente em C-uncertain/candidata, preservado. As oito skills ativas voltaram exatamente à base.
- Checks: 50 testes locais, doctors, corpus geral/coortes, copy/link temporários e diff-check; oito replays finais das fixtures (seis verdes e duas falhas esperadas no review sem correção). Telemetria nativa desconhecida; sem alegação de ganho de eficiência.
- Restrições/próxima ação: apresentar decisão e parar; MOD-008 sem commit, sem push e sem avanço à MOD-009. Plano de delegação separado preservado fora desta fatia.
- Os registros abaixo são históricos datados; suas permissões e próximos passos não substituem esta seção.

## Histórico — melhoria de 2026-10-22

- modo: auditoria com execução autorizada
- arquétipo: C (CLI e automação), com conteúdo declarativo de Agent Skills
- base: `main` em `f89b9c9`; worktree já continha a refatoração aprovada das oito skills e a Fase 2 sem commit
- autorização: usuário aprovou seguir as recomendações, na ordem, em 2026-10-22
- release: usuário autorizou commit e push em 2026-10-22; renomeação aguarda escolha do nome exato

| Fase | Estado | Evidência / pendência |
|---|---|---|
| 1. Avaliações comportamentais | concluído | 24 casos, schema, classificador A/B e testes; execução com modelos permanece uma etapa explícita do host |
| 2. Modos de aprovação | concluído | Modos assistido e contínuo adicionados às quatro pipelines, com limites para ações externas |
| 3. CI multiplataforma | concluído | Workflow para Linux, Windows e macOS em Python 3.9 e 3.14; cópia e link cobertos |
| 4. Descoberta nos agentes | parcial | Codex verificado no catálogo da sessão; Claude Code e Antigravity aguardam sessões compatíveis |
| 5. Versionamento/atualização | concluído | Catálogo `1.0.0`, recibos por release e sete skills do Codex atualizadas; `humanizer` do repositório excluída |
| 6. Índice da biblioteca fria | concluído | 2.676 entradas reparadas e validadas; configuração persistente criada; busca exata e temática da `skill-loader` verificadas no pacote instalado |

Commit e push da entrega estão autorizados. Renomeação do repositório será executada após a escolha do nome; publicação adicional, alteração de credenciais ou instalação em outros perfis permanecem fora do escopo.

## Auditoria de modernização — 2026-10-28

- Modo: auditoria sem alteração de implementação, autorizada pelo pedido anexado nesta sessão.
- Base: `main` / `869444d4fd916830b2a8a00ed756134fc031e4ac`; árvore inicialmente limpa.
- Gates de auditoria 1–2: reconhecimento e diagnóstico realizados; nenhum aceite humano foi presumido.
- Artefatos e evidências: [índice da auditoria](docs/audits/modernization-2026-10-28/README.md).
- Baseline: 24 casos estruturalmente válidos; testes/doctors limitados por PyYAML ausente; instalação temporária falhou por DNS. Detalhes no baseline da auditoria.
- Achados: F01–F10; roadmap MOD-001–MOD-010, todas planejadas.
- Próxima ação proposta: MOD-001 (frontmatter do loader), aguardando aprovação explícita antes de implementar.
- As autorizações de commit/push e informações de release na seção anterior pertencem ao registro de 2026-10-22; não autorizam ações nesta missão. Histórico preservado.

## Execução MOD-001 — 2026-10-28

- Autorização: implementar somente MOD-001 e validar o aceite; proibidos avanço de tarefa, commit e push, conforme pedido atual do usuário.
- Base e alterações preservadas: `869444d`; adendo de auditoria e diretório de auditoria já estavam presentes antes desta execução.
- Estado: MOD-001 validada tecnicamente; aceite humano final não presumido. Demais MOD permanecem planejadas e não iniciadas.
- Mudança: frontmatter inicial com PyYAML seguro, chaves únicas, identidade e descrição válidas; erro controlado para dependência ausente. Nenhuma biblioteca externa ou perfil instalado foi alterado.
- Ambiente: `/usr/bin/python3` 3.14.4 com PyYAML 6.0.3, já disponíveis; sem instalação. A limitação anterior permanece registrada como histórico do Python padrão 3.15.
- Validação: baseline 27 testes OK; regressões reproduzidas antes da correção; final 32 testes OK, doctor das oito skills, 24 casos estruturais, doctor Quarto e diff-check OK.
- Evidência e limites: [resultado MOD-001](docs/audits/modernization-2026-10-28/mod-001.md).
- Próxima ação autorizada: apresentar resultado ao usuário e parar. Sem MOD-002, commit, push ou atualização de instalações reais.

## Execução MOD-002 — 2026-10-28

- Autorização: implementar somente MOD-002, validar e apresentar resultados; sem próxima tarefa, commit ou push.
- Base: `869444d`; alterações locais da auditoria e da MOD-001 preservadas.
- Estado: MOD-002 validada tecnicamente; aceite humano final não presumido. MOD-003–MOD-010 não iniciadas.
- Mudança: totais sem observações agora são null; zero real preservado; metric_observations informa cobertura por métrica/condição. Schema dos traces e julgamento de qualidade inalterados.
- Validação: baseline 32 testes OK; 4 falhas reproduzidas antes da correção; final 35 testes OK, doctor de oito skills, 24 casos estruturais, doctor Quarto e diff-check OK.
- Evidência: [resultado MOD-002](docs/audits/modernization-2026-10-28/mod-002.md).
- Próxima ação autorizada: apresentar o resultado e parar, sem iniciar MOD-003.

## Execução MOD-003 — 2026-10-28

- Autorização: implementar somente MOD-003, validar e apresentar resultados; sem próxima tarefa, commit ou push.
- Base: `869444d`; auditoria e MOD-001/MOD-002 preservadas no working tree.
- Estado: MOD-003 validada tecnicamente; aceite humano final não presumido. MOD-004–MOD-010 não iniciadas.
- Mudança: validação dos traces/casos, vínculo ao catálogo e cobertura por pares; exit 0 de processamento preservado, evaluation separado em passed/failed/incomplete.
- Validação: baseline 35 testes OK; regressões reproduzidas antes da correção; final 38 testes OK, oito skills/24 casos/doctor Quarto/diff-check OK; smoke da CLI em cinco cenários sem traceback e sem alterar traces.
- Evidência: [resultado MOD-003](docs/audits/modernization-2026-10-28/mod-003.md).
- Próxima ação autorizada: apresentar resultado e parar. Sem MOD-004 ou operações Git de escrita.

## Execução MOD-004 — 2026-10-28

- Autorização: commit das mudanças acumuladas até MOD-003 e implementação da MOD-004, conforme pedido atual; sem push ou avanço à MOD-005.
- Commit acumulado: `fce31fe`; árvore limpa antes de iniciar esta fatia.
- Resultado: MOD-004 validada tecnicamente, em mudanças locais para revisão. Matriz operacional de fontes, precedência do estado vigente e validação dos links de referências ativas adotadas sem remover história.
- Verificações: baseline 38 testes OK, quatro falhas reproduzidas antes da correção, final 42 testes OK; doctors/24 casos/instalação temporária copy e link/diff-check OK.
- Evidência: [resultado MOD-004](docs/audits/modernization-2026-10-28/mod-004.md); nenhuma atualização de instalação real.

## Execução MOD-005 — 2026-10-28

- Autorização: commit da MOD-004 e somente MOD-005; A/B com agentes isolados autorizado explicitamente. Sem push ou avanço à MOD-006.
- Commit anterior: `b9b9469`; MOD-005 fica sem commit para revisão.
- Resultado: política de esforço e contratos equivalentes adotada nos três pacotes após comparação; quatro casos adicionados, sem novo roteador/flag/serviço.
- Evidência: [MOD-005](docs/audits/modernization-2026-10-28/mod-005.md). Candidata final atendeu 4/4 casos da amostra; baseline 3/4 por documentação adicional no caso simples. Captura/resumo corrigida de forma simétrica, com resultado original preservado.
- Limites: cobertura do experimento 8/56 pares; relatório combinado failed inclui falha da baseline. Não há medição de economia de tokens nem validação de ativação automática.
- Checks: baseline 42 testes, final 43 testes OK; doctors/oito pacotes/28 casos/diff-check OK. Históricos e instalações reais preservados.

## Execução MOD-006 — 2026-10-28

- Autorização: commit da MOD-005 e somente MOD-006; cenários com agentes isolados autorizados explicitamente. Sem push ou avanço à MOD-007.
- Commit anterior: `10c6951`; nova fatia sem commit para revisão.
- Resultado: contrato compacto nos quatro pacotes, executor único, referências e revalidação de contexto/checks. Descrições/triggers preservados; nenhum roteador/estado paralelo criado.
- Evidência: [MOD-006](docs/audits/modernization-2026-10-28/mod-006.md). Seis cenários passaram na amostra, incluindo consumidor em contexto novo e edição textual Quarto sem render/configuração.
- Limites: cobertura comportamental 6/68, incomplete; base de retomada simulada, sem comparação Git histórica. Sem métrica estimada ou alegação de validação de todos os hosts.
- Checks: baseline/final 43 testes OK; doctors/oito pacotes/34 casos/copy e link temporários/diff-check OK.

## Execução MOD-007 — 2026-10-28

- Autorização: commit da MOD-006 e somente MOD-007; campanha A–J isolada autorizada expressamente, sem ações externas/Git de escrita pelos agentes. Commit anterior `10b14ad`; sem push.
- Mudança: coorte explícita via --cases; instrumentos locais de preparação/captura/coleta, fixtures A–J e lote completo com proveniência. Corpus geral e oito skills inalterados.
- Validação: baseline 43 testes, final 48 testes locais; doctors/casos/copy/link/diff-check aprovados. 24/24 execuções (12 pares A/B), 16/16 replays finais e 66/66 rubricas atendidas no escopo inspecionado.
- Diferenças: I escolheu writing-pipeline nas duas versões, contra oráculo fixado em auditoria; grader estrito failed, preservado. Baseline ignora ativação no contrato do grader; totais 12/12 versus 11/12 não provam regressão. Sem regressão essencial observada, sem promoção adicional.
- Limites: uma observação por caso/condição, contexto compartilhado A–I, revisão pelo integrador e telemetria nativa indisponível. Não demonstrada economia de tokens/velocidade ou validação multi-host.
- Evidência: [resultado MOD-007](docs/audits/modernization-2026-10-28/mod-007.md). Próxima ação autorizada: apresentar e parar; MOD-007 sem commit, MOD-008 não iniciada.

## Execução MOD-008 — 2026-10-28

- Autorização: commit da MOD-007 e somente MOD-008; comparação C/D/H em dois agentes isolados autorizada explicitamente. Commit anterior `bc41c7e`, sem push; plano de delegação paralelo preservado fora do commit.
- Candidata: uma referência nova de debugging, duas referências existentes ampliadas e três pointers condicionais, sem novos nomes/metadados. Fontes fixadas antes do teste e preservadas em candidate.json.
- Resultado: 12/12 execuções; mesmas 23/23 rubricas atendidas nas duas condições. Melhora discriminável não demonstrada: proposta rejeitada conforme contrato; removidas somente próprias edições nas skills ativas, idênticas à base.
- Grader: failed em C-uncertain/candidata por ausência do literal normalize_age, com diagnóstico semanticamente correto; sinal e resposta preservados. Não se fabrica aprovação da coorte.
- Entrega: coorte/fixtures, preparação reproduzível da proposta preservada, coletor com experimento explícito e metadados de symlink sem seguir alvo. Corpus geral/schema inalterados.
- Checks: baseline 48 e final 50 testes locais; doctors/casos/copy/link/diff-check aprovados; oito replays finais com seis verdes e duas falhas esperadas D-review. Sem CI remota, tokens/chamadas nativas ou validação de host externo.
- Evidência: [MOD-008](docs/audits/modernization-2026-10-28/mod-008.md). Próxima ação autorizada: apresentar e parar; sem commit desta fatia, push ou MOD-009.
