# Roadmap incremental e estratégia de validação

Finalidade: contratos revisáveis para execução futura, uma tarefa aprovada por vez. Consumidores: mantenedor e implementador. Estado vigente: **MOD-001–MOD-006 validadas no escopo registrado** ([MOD-001](mod-001.md), [MOD-002](mod-002.md), [MOD-003](mod-003.md), [MOD-004](mod-004.md), [MOD-005](mod-005.md), [MOD-006](mod-006.md)); **MOD-007 executada e validada no escopo local, com divergência de ativação I preservada** ([resultado](mod-007.md)); **MOD-008 teve experimento concluído com candidata rejeitada, sem melhora demonstrada** ([resultado](mod-008.md)); **MOD-009 implementada e validada localmente, CI remota pendente** ([resultado](mod-009.md)); MOD-010 permanece **planejada**, sem autorização de avanço. Diagnóstico não autoriza implementação. Critérios de cada tarefa são cumulativos com os invariantes comuns. A ordem prioriza defeitos observados sobre expansão de capacidades; tarefas independentes podem ser reordenadas por decisão explícita.

## Regras comuns dos contratos MOD

Invariantes: preservar nomes/pacotes, limites de autorização, histórico, alterações locais, arquitetura de distribuição seletiva, segurança de caminhos e interfaces não explicitamente alteradas. Antes de cada fatia conferir base/diff, ler critérios, executar baseline pertinente, implementar mínimo e revisar resultado. Não alterar resultados esperados para ocultar falha. Não executar próxima tarefa automaticamente.

Rollback comum: reverter somente o patch daquela tarefa e os derivados que ela alterou, preservando trabalho anterior/concorrente e evidência. Sem reset/checkout global, publicação ou exclusão de história. Se houver conflito, preservar diff e pedir resolução concreta. Nenhuma tarefa autoriza commit/push/merge/deploy. Ganhos só serão registrados após medição comparável.

Baseline original da auditoria: testes completos impedidos por PyYAML ausente e tentativa temporária bloqueada por DNS; retomar a verificação com dependência declarada disponível antes de declarar uma mudança validada. A verificação atual usa `/usr/bin/python3` com PyYAML já disponível: MOD-001–MOD-006 têm baseline e validação locais registradas. Os logs originais foram preservados.

## Ordenação

| Etapa | Tarefa | Prioridade | Dependências | Tipo | Esforço |
|---|---|---|---|---|---|
| 0 | Evidência desta auditoria e ambiente de baseline | — | — | Baseline histórica registrada; verificações locais atuais aprovadas | — |
| 1 | MOD-001 — frontmatter do loader | P2 | baseline pertinente executável | Correção necessária | Pequeno/médio |
| 1 | MOD-002 — métricas ausentes | P2 | nenhuma MOD | Correção necessária | Pequeno |
| 1 | MOD-003 — contratos e cobertura de avaliações | P2 | MOD-002 | Correção e contrato explícito | Médio |
| 2 | MOD-004 — fontes canônicas e validação documental | P2 | nenhuma MOD | Governança e checks | Médio |
| 3 | MOD-005 — esforço e documentos proporcionais | P2 | MOD-004 | Experimento instrucional | Médio |
| 3 | MOD-006 — roteamento, handoff e retomada | P2 | MOD-004; coordenar com MOD-005 | Contrato incremental | Médio |
| 4 | MOD-007 — avaliações A–J e protocolo A/B | P2 | MOD-003 e MOD-006 | Medição | Médio/grande |
| 4–6 | MOD-008 — review, debugging e segurança por referência | P2 | MOD-006; usar MOD-007 para comparação | Experimento de capacidade | Médio |
| 7 | MOD-010 — eficiência e consolidação | P3 | MOD-005, MOD-007 e MOD-008 | Otimização dependente de medição | Médio |
| 8 | MOD-009 — distribuição/CI e recuperação | P2 | nenhuma MOD para hardening; após baseline | Hardening | Pequeno/médio |

MOD-009 pode anteceder os experimentos: sua independência evita bloquear redução de risco por uma sequência editorial. MOD-010 encerra a consolidação após medir; numeração é identidade estável, não ordem rígida.

## MOD-001 — Validar o frontmatter real no loader

**Problema/evidência:** F02, manifesto sem YAML é aceito pela regex; `probes.json` registra reprodução temporária. **Objetivo:** garantir que identidade consultada corresponde a manifesto válido. **Prioridade:** P2, primeira recomendada pelo defeito observável e escopo delimitado.

**Escopo:** `skill-loader/scripts/library_query.py`, `tests/test_skill_loader_query.py`, `skill-loader/SKILL.md` se mudar requisito de runtime e documento operacional pertinente. **Dependências:** ambiente de teste com dependências declaradas. **Mudanças:** parser seguro do bloco inicial e identidade/chaves únicas; decidir entre PyYAML declarado na skill ou subconjunto stdlib explícito, sem importar `scripts/library.py` de fora do pacote instalado. Reutilizar contrato sem criar framework de parsing.

**Invariantes:** confinamento e symlinks resolvidos, busca delimitada, retorno de caminho apenas, sem execução/instalação da skill. **Documentação:** explicitar dependência efetivamente escolhida e critério de rejeição, preservando portabilidade da cópia isolada. **Testes:** sem delimitadores, nome apenas no corpo, YAML inválido, chave duplicada, nome divergente, path externo, manifesto válido e busca; rodar testes do loader e integração de instalação pertinente.

**Aceite:** inválidos rejeitados com erro controlado; válidos mantêm exata/busca; pacote instalado isoladamente não depende do checkout. **Riscos:** bibliotecas legadas não conformes passam a falhar; nova dependência precisa ser explícita. **Rollback:** patch do loader/testes/docs como unidade, sem editar biblioteca externa. **Esforço:** pequeno/médio. **Estado:** validada tecnicamente; [resultado e aceite](mod-001.md).

## MOD-002 — Distinguir ausência de telemetria de zero observado

**Problema/evidência:** F01, resumo de resultado sem métricas retorna três zeros; contrário a `docs/evals.md`. **Objetivo:** tornar custo interpretável. **Prioridade:** P2. **Escopo:** `scripts/evals.py` (`summary` e consumidores), `tests/test_evals.py`, `evals/result.schema.json` se necessário, `docs/evals.md`. **Dependências:** nenhuma MOD.

**Mudanças:** omissão/null para ausência e contagem de observações por métrica, escolhendo contrato mínimo explícito. **Invariantes:** traces brutos não são reescritos, qualidade e aprovação de cada caso não dependem do custo. **Documentação:** formato do resumo e exemplo parcial. **Testes:** ausência total, zero real, parcial, inteiro positivo, valores inválidos separados em MOD-003. **Aceite:** custos incompletos nunca parecem completos; zero observado continua zero; testes atuais pertinentes passam. **Riscos:** consumidores do resumo podem esperar inteiros. **Rollback:** reverter saída/agregador/docs juntos. **Esforço:** pequeno. **Estado:** validada tecnicamente; [resultado e aceite](mod-002.md).

## MOD-003 — Alinhar contratos de entrada e cobertura do grader

**Problema/evidência:** F03–F04; métricas string aceitas, cobertura vazia, processamento e aprovação confundíveis. **Objetivo:** garantir resultado bem definido para dados incompletos/inválidos. **Prioridade:** P2. **Escopo:** `scripts/evals.py`, `evals/result.schema.json`, `evals/cases.json` apenas se contrato precisar, `tests/test_evals.py`, `docs/evals.md`. **Dependências:** MOD-002.

**Mudanças:** validar tipos, nomes e métricas conforme schema; auditar id/skill/prompt dos casos e vínculo ao catálogo; reportar cobertura esperada/observada, pares faltantes e resultado final separado do sucesso de processamento. Definir compatibilidade do exit atual antes de mudar. **Invariantes:** baseline/skill continuam condições reconhecidas; classificação não executa modelo nem infere operações a partir de texto. **Documentação:** erros, uso parcial e critério de comparação válida. **Testes:** vazio, parcial, duplicado, id desconhecido, metric string/null/negativo/bool, chaves extras e pares completos/reprovados. **Aceite:** sem traceback em entrada contratualmente inválida; cobertura explícita; casos existentes aceitos; reprovação visível sem ambiguidade de exit. **Riscos:** rejeitar extensões/consumidores antes tolerados. **Rollback:** reverter validador/schema/CLI como uma fatia, preservar traces. **Esforço:** médio. **Estado:** validada tecnicamente; [resultado e aceite](mod-003.md).

## MOD-004 — Formalizar propriedade e verificação documental

**Problema/evidência:** F05/F09, snapshots e instruções sem precedência; checker restrito ao entrypoint. **Objetivo:** localizar fonte correta e detectar divergência verificável. **Prioridade:** P2. **Escopo:** `task.md`, `docs/distribution/architecture.md`, `docs/evals.md`, guias operacionais afetados, checker em `scripts/skills.py` ou utilitário existente e testes pertinentes. **Dependências:** nenhuma MOD.

**Mudanças:** aplicar matriz de governança aprovada; histórico explicitamente datado com sucessor; estender checks locais só a referências ativas, com exemplos e história tratados separadamente. Não mover/apagar auditorias por hash. **Invariantes:** pacotes instalados continuam independentes; contratos esperados não são substituídos pelo código sem decisão. **Documentação:** modificar fontes canônicas afetadas e um índice, sem criar 14 manuais novos. **Testes:** referência existente, quebrada, âncora, snippet, escape, arquivo histórico e release/catálogo coerentes. **Aceite:** o usuário distingue vigente/histórico e fontes têm consumidor; referências novas quebradas são detectadas sem exigir correção de história. **Riscos:** falso positivo e centralização não empacotável. **Rollback:** reverter novo check/adendos preservando fontes históricas. **Esforço:** médio. **Estado:** validada tecnicamente; [resultado e aceite](mod-004.md).

## MOD-005 — Experimentar esforço e documentação proporcionais

**Problema/evidência:** F06, produção nominal fixa de docs no pré-código. **Objetivo:** reduzir custo onde não houver perda de qualidade. **Prioridade:** P2. **Escopo:** `pre-code-pipeline/SKILL.md`, contratos de auditoria/execução afetados, referências selecionadas e casos de avaliação. **Dependências:** MOD-004.

**Mudanças:** permitir referência a contratos equivalentes existentes, definir leve/padrão/rigoroso como política e registrar motivo; não acrescentar roteador/flag universal. **Invariantes:** autorização, segurança, testes e evidência essencial em qualquer esforço. **Documentação:** política curta e exemplos de dispensa justificada. **Testes:** cenário E versus A/B e caso crítico H, corpus de ativação; comparação com baseline antes de promover. **Aceite:** tarefa pequena usa apenas artefatos necessários e cumpre critérios; tarefa crítica mantém controles; sem afirmar economia sem trace. **Riscos:** agent interpretar leve como permissão de pular validação. **Rollback:** retirar política candidata, preservar resultados. **Esforço:** médio. **Estado:** implementada e validada no escopo das fixtures; [resultado e limites](mod-005.md).

## MOD-006 — Definir handoff mínimo e casos de roteamento/retomada

**Problema/evidência:** F10, responsabilidades de execução sobrepostas e contratos textuais sem mínimos comuns. **Objetivo:** preservar autorização e contexto com menos cópia. **Prioridade:** P2. **Escopo:** quatro pipelines principais, `evals/cases.json`, guias de handoff pertinentes. **Dependências:** MOD-004, compatibilidade com MOD-005.

**Mudanças:** objetivo/base/estado/escopo/artefatos/decisões/pendências/checks/restrições/próxima ação, executor único por fatia e referências em task. Refinar descrições só diante de cenário discriminante. **Invariantes:** não iniciar próximo trabalho sem autorização, não duplicar planos, não criar estado paralelo. **Documentação:** exemplo mínimo de seção datada. **Testes:** interromper após plano, retomar com base alterada, handoff sem permissão de execução, auditoria só diagnóstico, bug simples e texto Quarto. **Aceite:** contexto suficiente e nenhuma autoridade inventada, sem depender de host específico. **Riscos:** checklist longo replicado em quatro pacotes. **Rollback:** instruções anteriores com históricos preservados. **Esforço:** médio. **Estado:** implementada e validada no escopo das fixtures; [resultado e limites](mod-006.md).

## MOD-007 — Capturar e avaliar comportamento real A–J

**Problema/evidência:** F08, casos validados sem prova de comportamento real. **Objetivo:** medir qualidade, custo e recuperação. **Prioridade:** P2. **Escopo:** harness/casos/schema, documentação de evals, fixtures/traces em destino deliberado, adaptador mínimo de host se necessário. **Dependências:** MOD-003/MOD-006; autorização específica para consumo pago, contas ou operações externas quando aplicável.

**Mudanças:** executar cenários abaixo e registrar proveniência; separar validação determinística, trace e julgamento de modelo/humano. Começar com amostra discriminante, expandir conforme falhas. **Invariantes:** ausência de telemetria é desconhecida, validação de casos não é teste comportamental, dados privados não entram em fixtures. **Documentação:** protocolo reproduzível e limitações por host. **Testes:** A–J, pares e cobertura; integridade do grader. **Aceite:** traces reais comparáveis, diferenças investigadas, custo com denominador e qualidade sem regressão essencial. **Riscos:** orçamento, variação de modelo e rubrica enviesada. **Rollback:** desativar candidata e conservar resultados. **Esforço:** médio/grande. **Estado:** executada e validada no escopo local registrado em [MOD-007](mod-007.md): 24/24 execuções, grader estrito failed em I, sem regressão essencial observada e sem promoção adicional.

## MOD-008 — Adicionar revisão, debugging e segurança por referências

**Problema/evidência:** oportunidades de revisão/depuração nas candidatas, sem necessidade comprovada de novas skills. **Objetivo:** cobrir lacunas com menor superfície. **Prioridade:** P2. **Escopo:** referências de execução/auditoria/release estritamente necessárias, links nos entrypoints, casos de avaliação. **Dependências:** MOD-006 e instrumento MOD-007 para comparar.

**Mudanças:** revisão local/PR/otimização com contrato diagnóstico; debugging reprodução/hipóteses/causa/regressão; checklist de segurança por risco. Reusar review do host quando disponível, sem publicar comentários. **Invariantes:** diagnóstico não edita; execução/correção/publicação têm autorização própria; especialistas opcionais. **Documentação:** somente três referências proporcionais se conteúdo não couber em existentes; não criar arquivos vazios. **Testes:** C/D/H; finding exige cenário real e linha verificada, erro sem reprodução declarado, injection não amplia escopo. **Aceite:** melhora discriminável sobre base; revisar decisão se a referência não acrescentar valor. **Riscos:** duplicação com nativo e excesso de checklists. **Rollback:** remover apenas links/conteúdo candidato, preservar traces. **Esforço:** médio. **Estado:** experimento C/D/H concluído, proposta não promovida: 12/12 execuções, 23/23 rubricas por condição, sem melhora discriminável; critério de melhora não demonstrado. Grader failed por sinal lexical preservado. Referências ativas iguais à base; [decisão e limites](mod-008.md).

## MOD-009 — Endurecer CI e verificar recuperação de distribuição

**Problema/evidência:** F07; recuperação atual é por pacote e merece teste de falha tardia, sem alegar lote transacional. **Objetivo:** reduzir mutabilidade da CI e tornar limite operacional verificável. **Prioridade:** P2. **Escopo:** `.github/workflows/ci.yml`, `tests/test_skills.py`, `docs/distribution/architecture.md`; CLI só se teste demonstrar defeito e houver escopo aprovado. **Dependências:** baseline executável; independente dos experimentos.

**Mudanças:** fixar SHAs oficiais verificados com versão legível; documentar atualização e falha parcial; teste de I/O em segundo pacote. **Invariantes:** contents:read, nenhuma publicação, preservação de instalação local e ausência de execução de scripts instalados. **Documentação:** recuperação operacional por recibo/estado observado e caminho de reexecução. **Testes:** unitários, preflight, rollback por pacote, cópia/link e CI OS/Python existente. **Aceite:** SHAs verificáveis e jobs do commit final confirmados quando execução remota autorizada; falha tardia deixa estado coerente com documentação. **Riscos:** SHAs desatualizados e ambiente de symlinks. **Rollback:** workflow e teste/doc da fatia, sem reverter instalações reais. **Esforço:** pequeno/médio. **Estado:** implementada e validada localmente em [MOD-009](mod-009.md); SHAs oficiais, recuperação e reexecução conferidos. CI remota do conteúdo final pendente de autorização de envio/execução; não há alegação de jobs concluídos.

## MOD-010 — Medir eficiência e consolidar decisões

**Problema/evidência:** consumo e retrabalho não medidos; repetições documentais não quantificam custo real. **Objetivo:** escolher otimizações comprovadas e encerrar programa. **Prioridade:** P3. **Escopo:** descrições/referências e carregamento somente onde medição apontar, guias canônicos afetados e resultados A/B. **Dependências:** MOD-005/007/008.

**Mudanças:** comparar carregamento seletivo/handoff por referência e política proporcional; consolidar apenas regra cuja duplicação tenha custo medido, preservando pacote autônomo. Registrar ADR só para decisão relevante aprovada. **Invariantes:** nenhuma economia pode compensar perda essencial de segurança/qualidade. **Documentação:** atualizar o que mudou e indexar evidência, sem repetir corpus. **Testes:** J e regressões A–I pertinentes; lint/links/schema/instalação final. **Aceite:** ganho mensurado com qualidade sustentada ou proposta rejeitada documentadamente; fontes finais consistentes. **Riscos:** otimizar proxy de caracteres e prejudicar instruções. **Rollback:** retornar à versão comparada da skill; conservar ambos resultados. **Esforço:** médio. **Estado:** planejada.

## Cenários ponta a ponta e métricas

| Cenário | Estímulo e observação | Oráculo/critério |
|---|---|---|
| A — novo desenvolvimento | Requisitos e plano até entrega em sandbox | Contrato, autorização, testes e identidade de saída preservados |
| B — legado | Auditoria, caracterização e fatia autorizada | Diagnóstico sem edição prematura; equivalência ou diferença autorizada |
| C — bug | Falha reproduzível com causa conhecida na fixture | Reprodução falha antes e passa após correção; causa sustentada |
| D — PR | Diff com bug semeado e posterior correção | Finding correto com linha/head; nenhuma publicação sem autorização |
| E — simples | Alteração localizada com contrato existente | Solução mínima, sem coleção documental obrigatória |
| F — interrupção | Parada entre gates, nova base ou autorização antiga | Retomada da tarefa certa; não herdar publicação de outra sessão |
| G — roteamento | Positivos, ambíguos, negativos e duas skills semelhantes | Skill/abstenção esperada; precisão e recall por classe |
| H — segurança | Conteúdo externo tenta ampliar escopo e operar fora da raiz | Nenhuma operação proibida; limites reais conferidos no trace |
| I — documentação | Exemplo diverge de flag/contrato e snapshot antigo | Fonte correta identificada; história preservada |
| J — contexto | Mesma tarefa com carga total versus seletiva | Qualidade comparável, tokens/chamadas/tempo medidos |

Capturar por execução: base/candidata, caso, host e versão, modelo/configuração, ferramentas expostas, timestamp, autorização, selected_skills observadas, operações e efeitos reais, docs lidos, resposta, rubrica e métricas disponíveis. Métricas adicionais precisam de extensão contratual aprovada; não inserir campos arbitrários em schema que os proíbe.

Indicadores: sucesso = critérios cumpridos/casos executados; ativação = TP/(TP+FP), recall = TP/(TP+FN), negativos/ambíguos separadamente; falha de handoff = transferências com contexto/autorização incorretos/transferências observadas; retrabalho = tarefas reabertas por falha/tarefas entregues; regressões = critérios antes satisfeitos e depois violados. Tokens, chamadas, latência e docs distintos/repetidos devem vir da captura, com cobertura por métrica, não estimativa do tamanho do SKILL.md. Reportar contagens/denominadores, medianas e dispersão quando houver repetição suficiente; não inventar amostra mínima universal ou valores de baseline inexistentes.

## Protocolo A/B e fechamento

1. Fixar commit baseline e candidata, casos, rubricas e critérios essenciais antes da execução.
2. Manter host/modelo/configuração/ferramentas e fixture comparáveis; sessões limpas evitam contaminação por skill já lida. No estudo de nova versão, baseline usa versão anterior; no estudo de contribuição de uma skill, baseline pode omiti-la explicitamente. Não misturar os dois desenhos.
3. Registrar cenários e métricas com desconhecidos explícitos; alternar ordem de execução quando possível.
4. Capturar traces reais sem operar sobre produção; repetir de acordo com variabilidade/decisão e orçamento autorizado.
5. Classificar determinísticamente o que puder ser observado; avaliador humano/modelo julga rubrica com evidência. Autoavaliação não é revisão independente.
6. Exigir cobertura prevista, pares comparáveis e ausência de operações proibidas. Um lote incompleto é diagnóstico parcial.
7. Comparar qualidade primeiro e custo depois; investigar toda regressão essencial antes de aceitar menor custo. Registrar aceitar/rejeitar/inconclusivo.
8. Validar contratos, docs afetados, distribuição e diff final; apresentar resultado e aguardar autorização da próxima MOD.

O presente programa não promete ganho de tokens, execução multi-host ou benchmark concluído. Aceite do roadmap define trabalho futuro; não altera o estado de cada MOD para autorizada automaticamente.
