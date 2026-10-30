# Skills, workflows e capacidades candidatas

Finalidade: identificar responsabilidades e oportunidades sem alterar contratos. Consumidor: mantenedor e executor das tarefas futuras. Todas as avaliações de maturidade abaixo são qualitativas: contrato estruturado não equivale a eficácia comprovada em agente.

## Inventário vigente

Catálogo v1/release 1.0.1 confirma exatamente as oito skills solicitadas. Todas têm um caso positivo, um ambíguo e um negativo no corpus de 24 casos; nenhum desses casos foi executado com modelo nesta auditoria. Metadados são leves na descoberta e o corpo cresce sob demanda. Tamanhos abaixo são caracteres Unicode medidos, não tokens.

| Skill / caracteres | Responsabilidade, trigger e entrada | Saída, gates e estado | Dependências, handoff e documentação | Testes, limite, maturidade e melhoria |
|---|---|---|---|---|
| pre-code-pipeline / 8.913 | Novo projeto/mudança relevante que precisa de plano; pedido, contratos e instruções | Cinco gates: descoberta, requisitos, arquitetura, scaffold, plano; task.md e arquétipo | Host; checklist Quarto quando A; especialistas opcionais; execução após plano e autorização; docs/00–05 e ADR condicional | Estrutura validável pelo doctor; sem teste real de carga documental. Estruturada; MOD-005 permite fontes equivalentes e esforço proporcional |
| execution-pipeline / 8.834 | Plano aprovado e execução autorizada; task, contratos e manifests | Lógica, integração, apresentação, documentação, revisão/build; seção própria no task | Referência A/B/C sob demanda; writing/Quarto/Graphify opcionais; release após aprovação real | Casos do harness e limites explícitos; bug simples sem plano pode retornar ao planejamento. Estruturada; referência debugging/review e handoff mínimo |
| audit-and-refactoring-pipeline / 9.417 | Legado, reconhecimento ou auditoria; modo e base Git | Reconhecimento, diagnóstico, caracterização/plano, execução autorizada, verificação; pode encerrar no Gate 2 | Quatro referências; escrita opcional; plano para execução ou implementação própria sob aceite | Preservação/falhas claras; sobreposição de execução precisa de dono da fatia. Estruturada; separar diagnóstico e executor na retomada |
| release-and-ops-pipeline / 8.584 | Preparar/publicar release após implementação/auditoria; alvo, artefato e autorização | Saneamento, versão, CI, publicação, smoke; task com identidade e estado real | Quatro referências operacionais; Git/CLI/conector conforme alvo; sem dependência obrigatória | Bons limites externos; comportamento remoto não exercitado. Estruturada; handoff com checks e destino sem duplicar logs |
| writing-pipeline / 6.147 | Redação/edição/revisão técnica; alvo, público e modo | Texto ou tabela não destrutiva; sem cinco gates; usa arquétipo existente | Três referências, Quarto/humanizer quando útil; devolve ao chamador; sem criar estado paralelo | Preserva fatos e schema do chamador; revisão automática de toda saída seria excesso, não exigência atual. Estruturada; revisão documental por risco |
| quarto-expert / 6.857 | Autoria/configuração/depuração/migração Quarto; formato, engine e alvo | Arquivos/diagnóstico e evidência de render quando executado; caller conserva gates | Referências especializadas e três exemplos; doctor Python; runtime opcional; writing quando útil | Doctor distingue skipped/fail/pass; render e engines não testados agora. Estruturada; melhorar links de referências e smoke proporcional |
| humanizer / 3.366 | Revisão de estilo solicitada; trecho, voz e modalidade | Texto fiel ou diagnóstico; comparação original/revisão; sem estado próprio | Host; sem dependência externa obrigatória; retorna ao chamador | Caso de preservação textual no corpus, sem medição real de fidelidade. Enxuta; manter opcional, sem detector de autoria |
| skill-loader / 3.570 | Especialista ausente do catálogo nativo e biblioteca configurada | Candidatos e manifesto canônico; sem instalação ou execução implícita | library_query.py, config e índice externo; deduplicação de caminhos/ciclos instrucional | 3 testes específicos e testes da biblioteca; regex de identidade aceita manifesto inválido. Funcional com defeito F02; MOD-001 |

## Auditoria nas 14 dimensões

Legenda: **C** = contrato explícito inspecionado; **L** = lacuna/limite de validação; **O** = oportunidade, não defeito; **D** = defeito reproduzido. Testabilidade e compatibilidade marcadas L não negam os contratos existentes.

| Skill | Clareza | Responsabilidade | Trigger | Entrada/saída | Gates | Handoff | Estado | Segurança | Falhas | Testabilidade | Contexto | Documentação | Multiagente | Manutenção |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pre-code | C | C | O | C | O | O | C | C | C | L | O | O | L | C |
| execution | C | O | O | C | C | O | C | C | C | L | C | C | L | C |
| audit | C | O | C | C | C | O | C | C | C | L | C | O | L | C |
| release | C | C | C | C | C | O | C | C | C | L | C | C | L | C |
| writing | C | C | O | C | C | C | C | C | C | L | C | C | L | C |
| quarto | C | C | O | C | C | C | C | C | C | L | C | O | L | C |
| humanizer | C | C | O | C | C | C | C | C | C | L | C | C | L | C |
| loader | C | C | C | D | C | C | C | L | C | L | C | C | L | O |

Justificativas: gates C em especialistas significam que respeitam o gate chamador ou não impõem gates, não que executem cinco etapas. Segurança C é limite instrucional explícito, sem certificação de resistência a injection. Multiagente L: formato e caminhos são inspecionados, mas sessões/versões reais de hosts não foram exercitadas. Clareza e manutenção C são avaliação qualitativa do contrato, não aprovação humana. Linhas O estão detalhadas a seguir e em F05–F10.

## Fluxos reais e riscos de orquestração

Desenvolvimento novo: pré-código produz contratos; execução consome plano aprovado; release recebe artefatos/checks. Auditoria: pode parar no parecer, preparar plano e executar sob autorização ou transferir para execução. Não há chamada automática entre scripts de pipelines; o host interpreta instruções e registra estado. Um handoff textual não prova que outra skill rodou.

Sobreposições: auditoria Gate 4 e execução cobrem alterações; writing revisa fatos/forma e humanizer estilo; Quarto é especialista de formato e não dona do projeto. Escolher um executor por fatia evita baseline/revisão duplicadas. Não foi identificada dependência obrigatória circular no contrato; chamadas opcionais entre especialistas devem conservar o chamador e evitar recursão. O loader já instrui deduplicação e interrupção de ciclos, sem implementação de um scheduler.

Ambiguidades a avaliar: “corrigir erro de render e revisar texto” pode selecionar Quarto+writing; “melhorar documentação” pode ativar writing ou humanizer; “corrigir bug pequeno” pode cair em execução sem plano ou auditoria completa. Nenhum desses cenários foi medido como erro real de roteamento. Testes negativos devem discriminar operação e autorização, não apenas palavras no prompt. Aprovação assistida/contínua já existe; não confundir com os novos modos de esforço.

Proposta de esforço: leve para mudança localizada com contrato existente, padrão para funcional convencional, rigoroso para interface pública/segurança/dados ou risco elevado. Ajustar número de artefatos e profundidade, preservando inspeção, autorização, teste relevante e recuperação. Não tornar leve sinônimo de pular segurança; não criar nova flag de CLI para uma política instrucional.

Contrato mínimo de handoff proposto: objetivo; base e estado; escopo aprovado com origem/data; dono da próxima fatia; referências de artefatos/decisões; pendências; checks com resultados; restrições; próxima ação autorizada. No task.md, usar seção datada e links em vez de copiar o PRD. Handoff sem autorização explícita retorna preparado, não executa automaticamente. Retomada lê a seção da tarefa vigente e revalida base/diffs antes de reutilizar aprovação.

## Quatro candidatas, cinco alternativas cada

| Candidata | Nova skill | Expandir existente | Referência especializada | AGENTS.md | Nativo do host | Recomendação, custo e risco |
|---|---|---|---|---|---|---|
| code-review-pipeline | Útil só se ritual recorrente multi-host mostrar lacuna; custo de trigger e manutenção | Revisão já existe no Gate 5 da execução; adicionar modos sem misturar autorização de editar | Contrato de revisão local/PR e findings é alternativa pequena | Apenas regras do repo, não procedimento universal | Codex oferece revisão de PR; verificar disponibilidade e autorização para comentar | Começar por referência+recursos nativos; benefício esperado: revisão consistente; custo pequeno/médio; risco de findings cosméticos e duplicação |
| agent-evaluation-pipeline | Duplicaria harness antes de provar necessidade | Expandir scripts/evals.py, schemas, casos e protocolo | Guia de captura/adaptador por host | Só comandos e limites do repo | Usar traces/telemetria disponíveis, sem presumir API comum | Ampliar infraestrutura existente; custo médio; risco de rubricagem autorreferida e comparação enviesada |
| debugging-pipeline | Trigger disputa execução/auditoria | Execução já orienta testes; acrescentar referência ao núcleo | Reproduzir, hipóteses, experimento, causa e regressão | Só instruções locais de reprodução | Debugger/logs/test runner do host | Referência na execução; custo pequeno; risco de impor investigação longa a erro trivial |
| security-review | Exige domínio e manutenção adicionais; justificar por demanda observada | Inserir seleção por risco na auditoria/review/release | Checklist de entrada, supply chain, injection, paths, segredos e ações externas | Só fronteiras específicas do projeto | Sandbox/scanners existentes como evidência | Checklist sob demanda; custo pequeno/médio; risco de transmitir falsa certificação |

Para revisão: distinguir local-review (unstaged/staged/commit/branch), pr-review (PR e head verificados) e pr-optimization (coesão/divisão/descrição, proposta sem mutação). Cada finding deve indicar arquivo/linha, severidade, evidência, impacto, cenário, correção e confiança. Diagnóstico não edita nem publica comentário. Após correção autorizada, revisar o diff final; não assumir que review anterior cobre novos commits. Nativo do Codex não garante cobertura universal ou disponibilidade em Claude/Antigravity.

Rejeitadas nesta fase: nova orquestradora, nova skill de governança, servidor MCP obrigatório, banco de estado, toda revisão delegada, geração fixa de documentação e instalação de novas dependências de produção. Reavaliar uma candidata somente com casos recorrentes e comparação entre a alternativa pequena e a skill completa.
