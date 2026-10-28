# Matriz consolidada de achados

Finalidade: única fonte dos diagnósticos desta auditoria. Consumidores: mantenedor, roadmap e revisores. P0 crítico, P1 alto, P2 médio, P3 baixo. Confiança refere-se à evidência, não ao tamanho do efeito. Não foram demonstrados P0/P1. `baseline.json` e `probes.json` guardam observações executadas; demais achados são inspeção ou oportunidades explicitamente indicadas.

| ID | Componente/localização | Achado e natureza | Evidência | Severidade | Impacto | Confiança | Proposta | Verificação |
|---|---|---|---|---|---|---|---|---|
| F01 | scripts/evals.py:84, summary | Defeito: métricas ausentes viram zero | baseline.json/probes; doc/evals contradiz implementação | P2 | Falsa impressão de custo zero e comparação enviesada | Alta | MOD-002, ausência explícita e cobertura por métrica | Ausente, zero real, parcial e valor inválido |
| F02 | skill-loader/scripts/library_query.py:36, manifest_for | Defeito: regex procura name no texto, aceita manifesto sem YAML | probes.json: invalid_manifest_accepted=true | P2 | Seleção por identidade aparente; pacote não conforme pode ser carregado | Alta | MOD-001, parser/validação real de frontmatter | Texto sem delimitador/nome no corpo/duplicado rejeitados |
| F03 | scripts/evals.py:35, load_results | Defeito de fronteira: metrics pode ser string apesar do schema | probes.json: invalid_metrics_loaded; summary usa .get | P2 | Entrada aceita causa falha não controlada, contratos divergem | Alta | MOD-003, alinhar validação com schema | Inválidos retornam diagnóstico JSON, sem traceback |
| F04 | scripts/evals.py:55 e main | Lacuna: resultados vazios/parciais não indicam cobertura esperada; grade usa exit 0 mesmo com caso reprovado | baseline/probes; teste atual exige exit 0 no grading | P2 | Consumidor pode confundir processamento com avaliação aprovada | Alta | MOD-003, cobertura explícita e decidir status compatível | Vazio, par ausente, reprovação e lote completo |
| F05 | task.md e docs/refactoring-plan.md | Divergência temporal: release/renomeação e autorização passada parecem vigentes | task: release 1.0.0/renomeação pendente; catálogo 1.0.1; README atual | P2 | Retomada errada ou reaproveitamento indevido de autoridade | Alta | MOD-004, seção datada com precedência | Retomar nova tarefa sem herdar permissão externa |
| F06 | pre-code-pipeline/SKILL.md, Entrada e Gates 1–5 | Oportunidade: nomes e criação de artefatos fixos podem onerar mudança pequena | Exige task/arquétipo e docs/01–05; dispensa parcial já existe | P2 | Custo documental potencial, ainda não medido | Média | MOD-005, política proporcional | Cenário simples vs padrão/crítico, sem perda de controle |
| F07 | .github/workflows/ci.yml | Hardening: actions por tags mutáveis | checkout@v7/setup-python@v7; contents: read já reduz privilégio | P2 | Dependência de resolução futura da tag | Alta | MOD-009, SHAs de origem verificada | Matriz e link-install no commit da mudança |
| F08 | evals/cases.json e docs/evals.md | Lacuna: corpus estrutural não prova comportamento e não há traces reais versionados inspecionados | 24 casos válidos; harness não executa modelos | P2 | Eficácia/custo e recuperação sem medição | Alta | MOD-007, cenários A–J e captura controlada | Traces reais, pares, proveniência e rubricagem |
| F09 | scripts/skills.py, validate_skill; referências ativas | Oportunidade: links só do entrypoint; sem verificação transversal de docs | Código remove blocos e verifica links do corpo do SKILL.md | P3 | Links internos secundários podem envelhecer | Alta quanto à cobertura, não quanto à existência de links quebrados | MOD-004, escopo documental ativo | Fixtures de links/snippets/histórico sem falsos bloqueios |
| F10 | audit/execution/release SKILL.md, Handoff | Oportunidade: sem schema mínimo comum; auditoria e execução podem implementar mesma fatia | Contratos textuais e estado por pipeline | P2 | Repetição/perda de contexto potencial, não observada em benchmark | Média | MOD-006, dono e referências no handoff | Interrupção/retomada e mudança de base |

Tabela de compatibilidade com o protocolo da skill de auditoria:

| ID | Linha / Arquivo | Severidade | Diagnóstico Original | Sugestão de Refatoração | Racional Técnico |
|---|---|---|---|---|---|
| F01–F04 | locais acima | P2 | Contratos de evidência/validação divergem | Correções funcionais MOD-001–003, não refatoração equivalente | Alteram aceitação/saída, exigem aceite e teste |
| F05–F06/F09 | task e documentação acima | P2/P3 | Precedência/custo/cobertura documental | MOD-004–005 | Consolidar autoridade e reduzir redundância sem apagar história |
| F07 | workflow acima | P2 | Tags mutáveis | MOD-009 | Reduzir dependência de resolução mutável |
| F08/F10 | evals e contratos acima | P2 | Medição e handoff incompletos | MOD-006–007 | Melhorar prova de resultado e recuperação |

Estado posterior: **F02 corrigido pela MOD-001** ([evidência](mod-001.md)) e **F01 corrigido pela MOD-002** ([evidência](mod-002.md)), ambos validados no working tree. **F03/F04 corrigidos pela MOD-003** ([evidência](mod-003.md)), validados no working tree. **F05/F09 tratados pela MOD-004** ([evidência e limites](mod-004.md)), com estado vigente e verificação de links de referências ativas. **F06 tratado pela MOD-005** ([comparação e limites](mod-005.md)), com contratos equivalentes e esforço proporcional; economia de tokens não demonstrada. Os demais achados permanecem sem implementação.

## Contratos das recomendações

Cada item abaixo complementa a matriz com alternativas, benefício esperado, custo, risco, aceite e rollback; escopo/testes/dependências estão no contrato MOD correspondente. Benefícios são esperados, não medidos.

**F01:** problema confirmado na agregação. Solução: distinguir ausência/zero e informar número de observações por métrica. Alternativas: omitir totais ausentes ou null com contagem; rejeitada inferência de zero. Benefício: comparação interpretável. Custo pequeno; risco de quebrar consumidor que assume int. Aceite: mistura observada/ausente não se apresenta como custo completo. Rollback: reverter mudança do resumo e manter dados brutos, sem reescrever traces.

**F02:** problema confirmado no parser do loader. Solução: frontmatter delimitado, parser seguro, identidade e chaves únicas. Alternativas: reutilizar contrato existente com PyYAML e dependência explícita, ou validação stdlib limitada claramente declarada; não importar script do repositório numa skill distribuída isolada. Benefício: identidade compatível com distribuição. Custo pequeno/médio; risco de novas dependências ou rejeição de biblioteca legada. Aceite: casos do README executivo. Rollback: reverter fatia; não corrigir manifests externos automaticamente.

**F03:** validar estrutura/tipos de métricas, nomes, unicidade e campos conforme decisão de contrato. O loader de casos também não valida tipos completos de id/skill/prompt nem pertencimento ao catálogo; incluir na mesma revisão de fronteira com fixtures. Alternativas: validação manual existente ou motor de schema, preferindo não adicionar dependência sem necessidade. Benefício: falhas previsíveis. Custo médio; risco de rejeitar extensões antes aceitas. Aceite: entradas inválidas com exit controlado e contrato explícito; rollback da fatia de validação, preservando arquivos de entrada.

**F04:** separar avaliação bem processada de casos aprovados. Não chamar exit 0 atual de bug isolado: teste/documentação devem decidir compatibilidade. Solução: cobertura esperada/observada e status de avaliação explícitos, mantendo modo parcial para uso diagnóstico se necessário. Alternativa: consumidor exige pares externamente; descartado novo executor. Benefício: evitar conclusão com dados insuficientes. Custo médio, risco de romper automações; aceite com lote vazio/parcial/completo e falhas; rollback de CLI/schema/documentação como uma unidade.

**F05:** solução por seção datada e precedência, sem apagar autorização histórica. Alternativas: renomear snapshot para arquivo histórico com índice (mais alteração) ou simples nota no task (menor). Benefício: retomada segura; custo pequeno; risco de parecer revogar aprovações passadas válidas para outros escopos. Aceite: nova seção aponta base e autorização desta missão. Rollback somente do adendo.

**F06:** permitir contratos equivalentes por referência e esforço proporcional. Alternativas: manter fluxo atual e dispensas explícitas; não criar três pipelines novas. Benefício hipotético de menor custo, a medir. Custo médio; risco de interpretação permissiva de gates. Aceite: A/B conserva qualidade e nenhum controle essencial é suprimido. Rollback da política candidata, mantendo resultados.

**F07:** fixar SHA completo conferido nos repositórios oficiais e registrar versão legível, com atualização periódica. Alternativa: tags com política de revisão; trade-off é manutenção versus reprodutibilidade. Benefício: reduzir mutabilidade. Custo pequeno; risco de SHA incorreto ou ficar desatualizado. Aceite: todas as jobs do novo commit verificadas, sem ampliar permissões. Rollback só workflow ao estado previamente validado; execução remota exige autorização correspondente.

**F08:** ampliar harness existente e realizar captura em sandbox autorizada; primeiro poucos cenários discriminantes, depois A–J. Alternativas: avaliação manual rastreável ou adaptadores nativos; não criar plataforma de evals. Benefício: medir comportamento/custo real. Custo médio/grande, orçamento e conta dependem de autorização; risco de viés de avaliador e injection nas fixtures. Aceite: proveniência, efeitos reais e pares comparáveis, sem ganhos estimados apresentados como medidos. Rollback: desativar candidata e preservar evidências.

**F09:** reaproveitar checker de links e definir escopo ativo, ignorando exemplos ilustrativos/história de maneira explícita. Alternativa: ferramenta externa existente se instalada; não executar comandos arbitrários extraídos de docs. Benefício: detectar inconsistência cedo. Custo pequeno/médio; risco de falso positivo. Aceite: fixtures positivas/negativas e sem obrigação de corrigir história. Rollback de check novo sem apagar documentos.

**F10:** handoff mínimo e executor único por fatia. Alternativa: campos livres com checklist versus schema rígido; preferir checklist antes de formato novo. Benefício esperado: menor releitura/perda de autoridade. Custo pequeno/médio; risco de centralizar documentação fora do pacote instalado. Aceite: task interrompida retoma a aprovação correta sem duplicar planos. Rollback de instruções, preservando histórico.

## Limitações e propostas não promovidas a defeito

- Grafo local ignorado está desatualizado e cobre scripts históricos; não reconstruí-lo só para esta auditoria. Nenhum ciclo/centralidade foi usado como severidade.
- 54 grupos de duplicatas por hash incluem cópias preservadas; não se recomenda removê-las sem valor/consumidor conhecido.
- Falha de I/O no segundo pacote pode deixar primeiro atualizado: instalador recupera por pacote; não promete lote transacional. Documentar e testar a recuperação antes de propor transação global.
- `operations` usa comparação exata casefold e `required_signals` substrings; trace normalizado e rubricagem humana são necessários. Não se demonstrou resistência a aliases de comando/injection por esse grader.
- Ausência local de PyYAML é condição de ambiente, não regressão de produto. Nenhuma execução remota atual foi confirmada.
- Rejeitados: nova orquestradora, governança como skill independente, MCP/banco obrigatórios, novos agentes permanentes e otimização percentual sem benchmark.
