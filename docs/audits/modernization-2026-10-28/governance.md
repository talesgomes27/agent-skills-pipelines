# Inventário e governança documental

Finalidade: definir propriedade da informação e manutenção mínima. Consumidores: pipelines, mantenedor e revisores. Estado: proposta; nenhuma fonte histórica foi removida ou reclassificada em disco.

## Inventário e método

[document-inventory.json](document-inventory.json) lista cada um dos 167 arquivos textuais/contratuais versionados considerados, categoria, tamanho e SHA-256. O conjunto exclui código, binários, `.git`, arquivos ignorados e os novos artefatos desta auditoria. A classificação usa caminho/finalidade observável; não prova leitura integral de cada documento. Proprietários abaixo são papéis propostos, não pessoas formalmente designadas. Cada registro herda finalidade, consumidor e manutenção de sua categoria, salvo exceção explícita.

| Categoria / quantidade | Finalidade e origem | Mantenedor e consumidores | Atualização / carregamento | Relações, atualização e preservação |
|---|---|---|---|---|
| Instruções permanentes / 8 | Procedimentos dos SKILL.md ativos | Autor da skill; host e pipeline chamadora | Mudança de contrato; metadados na descoberta, corpo sob demanda | Catálogo e referências; identidade conferida por inspeção, doctor completo pendente; preservar versões Git |
| Contratos e avaliação / 6 | Catálogo/schema, exemplo MCP, casos/schema de resultados, requirements | Mantenedor da distribuição/evals; CLI, avaliador, CI | Mudança de interface; ferramentas leem sob demanda | JSON Schema e validadores divergem em pontos de F03; preservar proveniência |
| Referências técnicas / 42 | Detalhamento das oito skills | Autor especialista; agente no gate específico | Quando capacidade/versão muda; sob demanda | Não manter cópias nas instruções; validade técnica de todas as opções Quarto não revalidada |
| Documentação operacional / 7 | README e guias de distribuição/evals/biblioteca | Mantenedor; instalador/operador | Mudança no comando/contrato; consulta dirigida | Fonte derivada de código e evidência; divergência F01 confirmada |
| Planejamento e acompanhamento / 2 | task.md e docs/refactoring-plan.md | Responsável pela tarefa; pipelines de retomada | Por aprovação/check; leitura inicial da tarefa pertinente | Snapshot de 2026-10-22, não estado atual; F05; preservar histórico |
| Auditorias / 8 | Diagnósticos anteriores por skill | Autor da auditoria; futuro revisor | Imutável com adendos datados; sob demanda | Referem versões anteriores; não confundir achado resolvido com vigente |
| Histórico arquivado / 77 | legacy e proposals | Custódia do mantenedor; auditor/reprodutor | Sem atualização operacional; consulta explícita | Preservar; não instalar, não corrigir links antigos automaticamente |
| Exemplos reproduzíveis / 17 | QMD/configurações/bibliografia/README | Autor Quarto; usuário que copia exemplo | Mudança de exemplo/engine; sob demanda | Validar antes de executar; não alegar renderização por existir arquivo |

Categorias solicitadas sem artefato próprio identificado: requisitos aprovados atuais do programa são o pedido anexado e este roadmap ainda não aprovado; arquitetura está nos guias existentes; ADRs dedicados não foram identificados; resultados experimentais reais de agentes não foram encontrados entre arquivos versionados inspecionados. Os logs de baseline desta auditoria são resultados determinísticos, não traces comportamentais.

## Matriz de fontes canônicas e propriedade

| Fonte | Informação canônica | Consumidores | Redundâncias/divergências | Ação proposta |
|---|---|---|---|---|
| Pedido e contrato aprovado | Comportamento requerido, escopo e autoridade | Todas as pipelines | Autorizações antigas em task.md parecem atuais | Identificar sessão/data/base/alcance; nunca ampliar autorização por histórico |
| Código e testes | Comportamento observado e regressões reproduzíveis | Implementador/revisor | Código pode contrariar requisito | Investigar discrepância antes de escolher qual fonte mudar |
| distribution/catalog.json | Seleção, bundles e release do conjunto | CLI e instalação | Release repetida no README e snapshots | Conferir derivados na mudança de release, sem tornar README autoridade |
| SKILL.md/frontmatter | Identidade/descrição do pacote | Host e loader | Regex de loader diverge do parser da distribuição | Contrato equivalente nas fronteiras, sem referência fora de pacote |
| SKILL.md/corpo | Procedimento e limites | Host/pipeline | Regras de autorização repetidas para autonomia do pacote | Manter núcleo de segurança em cada pacote; consolidar só explicações extensas |
| Referências da skill | Detalhe especializado | Gate pertinente | Cópias históricas idênticas e conteúdo possivelmente envelhecido | Link sob demanda; não tornar referência irmã externa obrigatória |
| Scripts/configuração | Arquitetura implementada, instalação e CI | Operador/revisor | Diagrama pode resumir demais | Derivar mapa e registrar base; sem gerar grafo obrigatório |
| requirements.txt | Dependência de validação | Ambiente/CI | Não existe lock completo com hashes | Pin existente é útil; avaliar risco antes de exigir lock adicional |
| task.md/seção vigente | Estado e aprovações reais da tarefa | Retomada/handoff | Snapshot anterior contém comandos autorizados fora da missão atual | Acrescentar seção datada, preservar anterior como histórico |
| ADR quando necessário | Decisão relevante aprovada | Mantenedor/futuros autores | Não foi localizada coleção de ADRs | Criar só com decisão aprovada e consequência durável |
| Artefato + logs + base | Resultado de teste/experimento | Avaliador/reprodutor | Ausência de telemetria hoje vira zero | F01; distinguir não observado de zero |
| Auditorias/legacy/proposals | História e alternativas | Auditor futuro | 54 grupos de hashes iguais | Conservar, sinalizar status/precedência em índice |

## Redundância, envelhecimento e órfãos

[Estatística por hash](inventory-stats.json): 54 grupos de conteúdo exatamente igual. São grupos, não 54 documentos excedentes. Propostas preservadas coincidem com arquivos ativos em diversos pontos; isso é evidência histórica útil, não desperdício automaticamente removível. Cópias históricas não são fontes operacionais concorrentes se o índice as delimitar.

Divergências comprovadas: `docs/evals.md` afirma que ausência de telemetria não vira zero, em oposição a `summary`; `task.md` declara release 1.0.0 e renomeação pendente, enquanto catálogo/README/remoto registrado em Git refletem release 1.0.1 e nome público atual. Autorizações antigas não valem para esta missão. O grafo ignorado referencia base e scripts antigos; não deve guiar a arquitetura atual.

O validador cobre links do entrypoint, não links de todas as referências. Não foi executada varredura semântica exaustiva de links, exemplos ou todos os documentos. Portanto não se afirma que todos estejam íntegros, órfãos ou desatualizados. Ausência de link entrante não basta para chamar documento de órfão: um procedimento pode ser consumido diretamente. Registrar consumidor desconhecido como hipótese e perguntar ao mantenedor antes de arquivar.

## Política proporcional proposta

| Tipo de mudança | Trabalho documental necessário | Evidência de fechamento |
|---|---|---|
| Pequena/localizada | Atualizar apenas uso ou regra afetados; pode bastar diff e resultado | Referência do contrato e check pertinente |
| Funcional | Conferir requisitos, uso e teste observável | Exemplo/comando coerente com implementação |
| Arquitetural | Registrar decisão relevante e diagrama que mudou | Alternativas, consequência e interfaces verificadas |
| Interface pública | Contrato, compatibilidade, exemplos e migração | Casos válidos/inválidos e consumidores afetados |
| Auditoria | Achados numa única matriz; logs referenciados | ID estável, base e distinção fato/hipótese |
| Release | Catálogo, notas e instruções de distribuição afetadas | Artefato final e destino verificados conforme autorização |
| Experimento | Método, configuração, entradas e proveniência suficientes | Reexecução comparável ou limitação explícita |

Não obrigar todos os projetos a gerar cinco novos documentos antes de uma alteração pequena. Documentos existentes aprovados podem satisfazer gates por referência; a decisão de mudar esse contrato precisa ser avaliada em MOD-005, não aplicada agora. Invariantes de segurança, testes pertinentes e autorização permanecem em todos os modos.

Arquivamento: considerar somente artefato substituído, com consumidor conhecido e destino canônico referenciado. Marcar motivo/data/base/sucessor; preservar Git e evidências, não apagar por baixa leitura. Resultados científicos, conformidade e histórico nunca são descartados por contagem de linhas. Aprovação do mantenedor antecede remoção de qualquer artefato com valor incerto.

## Documentação como código e custo

Expandir o checker existente antes de acrescentar ferramenta: links locais em referências ativas fora de exemplos, confinamento, existência, paridade schema/validador e consistência catálogo/frontmatter. Tratar snippets, placeholders e história com escopos explícitos para reduzir falsos positivos. Comandos documentados somente em fixtures temporárias e após verificar efeitos; nunca executar todos os blocos shell extraídos de Markdown.

Métricas propostas por tarefa: documentos lidos distintos e repetidos, bytes/caracteres lidos como proxy, tokens reais quando disponíveis, arquivos documentais modificados por mudança funcional, inconsistências detectadas e tempo para localizar fonte. Não foram medidos esses indicadores em tarefas reais; o inventário é baseline estática. Não fixar teto universal de Markdown.

Aplicação transversal: pré-código escolhe artefatos proporcionais; execução sincroniza afetados; auditoria detecta divergência; writing preserva fatos e adapta leitor; release verifica distribuição; loader evita leitura duplicada; referência de review confere docs relacionadas ao diff. Política compartilhada não deve virar dependência fora do pacote instalado: uma referência mínima pode ser empacotada onde necessária ou validada na fonte por CI. Escolher distribuição antes de centralizar fisicamente.
