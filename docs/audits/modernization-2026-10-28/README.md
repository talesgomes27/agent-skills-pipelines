# Auditoria e programa de modernização — 2026-10-28

Finalidade: apoiar a decisão do mantenedor sobre mudanças incrementais. Consumidor: usuário e futuros executores das tarefas MOD. Estado: diagnóstico concluído no escopo inspecionado; propostas **planejadas, não autorizadas**. A implementação depende de aprovação explícita de cada tarefa. Este registro não herda permissões operacionais de auditorias anteriores.

Atualização posterior à auditoria: [MOD-001](mod-001.md), [MOD-002](mod-002.md) e [MOD-003](mod-003.md) implementadas e validadas tecnicamente, cada uma sob autorização específica. O diagnóstico e a baseline abaixo preservam o momento original; as demais tarefas não foram iniciadas.

## A. Sumário executivo

A base `main` / `869444d4fd916830b2a8a00ed756134fc031e4ac` tem oito skills ativas, catálogo v1/release 1.0.1 e seis bundles. A árvore Git estava limpa. A arquitetura atual já oferece carregamento progressivo, especialistas opcionais, modos assistido/contínuo, instalação seletiva e preservação de edições locais. Não há evidência que justifique um novo framework ou uma nova skill de orquestração.

Os defeitos prioritários confirmados estão nas fronteiras de validação e na qualidade da evidência: identidade do manifesto no loader, métricas de avaliações e aceitação de resultados incompatíveis com o schema. A governança precisa distinguir estado atual de autorizações históricas e deixar de exigir a mesma coleção documental em tarefas de complexidades diferentes. Não foram identificados P0 ou P1 comprovados; isso não certifica ausência de vulnerabilidades.

A primeira tarefa recomendada é **MOD-001: validar o frontmatter real no loader**, antes de expandir o ecossistema. A sondagem mostrou aceitação de `# Sem frontmatter\nname: alpha\n` como manifesto. O confinamento de caminho continua funcionando na implementação inspecionada; não foi demonstrada execução arbitrária por essa falha.

## Navegação e fontes deste parecer

- [Inventário e governança](governance.md): classificação, propriedade da informação, redundância e política proporcional.
- [Skills e workflows](skills-and-workflows.md): oito contratos, dimensões de auditoria, roteamento e candidatas.
- [Arquiteturas e diagramas](architecture.md): sete representações atuais e sete futuras.
- [Achados](findings.md): evidências, severidade, alternativas e risco; fonte canônica dos diagnósticos desta auditoria.
- [Roadmap e validação](roadmap.md): contratos MOD, cenários A–J, A/B e aceite.
- [Pesquisa oficial](sources.md): fontes consultadas, compatibilidade e limites.
- [Baseline bruto](baseline.json), [sondagens](probes.json), [inventário por arquivo](document-inventory.json) e [duplicações exatas](inventory-stats.json): evidência, sem repetir logs nos pareceres.

As auditorias de 2026-10-22 e `docs/refactoring-plan.md` permanecem históricos preservados. Achados antigos não são automaticamente defeitos atuais. O presente parecer foi produzido após inspeção das versões vigentes.

## B–G. Diagnóstico integrado

A arquitetura é declarativa: skills instruem o host; não existe executor central que faça gates ou handoffs automaticamente. A CLI distribui pacotes, mas não inicia agentes. Os fluxos novo desenvolvimento e auditoria convergem na execução e release; a auditoria também pode refatorar sob autorização própria, uma sobreposição que requer delimitar o executor de cada fatia. Diagramas e tratamento estão em [architecture.md](architecture.md) e [skills-and-workflows.md](skills-and-workflows.md).

A governança proposta usa as fontes existentes: código para comportamento observado, contratos aprovados para comportamento requerido, catálogo para seleção/release, frontmatter para identidade, `SKILL.md` para procedimento e estado por seção em `task.md`. Código não substitui requisito aprovado. Divergências exigem investigação e decisão explícita. Não se recomenda uma `documentation-governance-skill`.

Para as quatro candidatas, recomenda-se começar com referência de revisão e recursos nativos do host; ampliar o harness existente para avaliações; adicionar referência de debugging à execução; e manter segurança como checklist acionado por risco. Nenhuma nova skill é aprovada neste parecer. Os modos leve/padrão/rigoroso são uma política candidata das pipelines existentes e precisam de avaliação antes de adoção.

Não foram medidos tokens de tarefas, latência de agentes, precisão real de roteamento ou retrabalho. Caracteres de arquivos e contagens de documentos são medidas estáticas, não economia de tokens. Não há ganho percentual demonstrado.

## H. Linha de base e testes

Ambiente: Ubuntu 26.04.1 LTS, kernel/versão Python registrados em [baseline.json](baseline.json). Dependência declarada: `PyYAML==6.0.3`; não está disponível no Python padrão. Testes inspecionados usam diretórios temporários, fixtures e mocks; não houve execução contra produção.

| Comando executado | Exit | Resultado observado |
|---|---:|---|
| `python3 -B -m unittest discover -s tests -v` | 1 | 27 testes, 18 falhas; ausência de PyYAML afeta expectativas dos testes dependentes |
| `python3 -B scripts/skills.py doctor` | 2 | indisponível: PyYAML ausente |
| `python3 -B scripts/evals.py validate` | 0 | 24 casos, 8 skills, 8 positivos/8 ambíguos/8 negativos |
| `python3 -B quarto-expert/scripts/doctor.py` | 2 | validações disponíveis executadas; YAML pulado |
| `graphify query 'skills distribution installer evals handoff task.md' --budget 1200` | 4 | nenhum nó correspondente; grafo de `f89b9c92`, anterior à base atual |
| `python3 -m venv /tmp/meta-skills-audit-20261028-venv` | 0 | ambiente temporário criado |
| `/tmp/meta-skills-audit-20261028-venv/bin/python -m pip install --disable-pip-version-check -r distribution/requirements.txt` | 1 | DNS de pypi.org indisponível; nenhuma dependência instalada |

O histórico registra checks positivos em 2026-10-22, mas eles não substituem uma execução atual. Não se alteraram testes para obter sucesso. A baseline verde atual permanece pendente até disponibilizar a dependência declarada. As sondagens stdlib confirmam defeitos independentemente de PyYAML. O harness valida/classifica traces; não executa modelos. CI configurada não significa CI remota confirmada nesta auditoria.

## I. Segurança e distribuição

A CLI valida seleção antes de escrever, rejeita pacotes não gerenciados, preserva cópias divergentes, restringe referências do entrypoint e usa recibo com SHA-256 e troca/rollback por pacote. Links são fontes vivas, sem promessa de imutabilidade. O instalador não executa os scripts distribuídos e não acessa rede. A revisão não incluiu análise de CVEs ou certificação de segurança.

A instalação em lote tem preflight de conflitos e recuperação por pacote, não transação global diante de falha de I/O em pacote posterior. Isso é uma limitação operacional; não há recomendação de um coordenador transacional. CI usa `contents: read`, sem deploy, mas actions são referenciadas por tags. Fixar SHAs verificados é hardening recomendado, não prova de comprometimento atual.

## J–L. Arquitetura futura, roadmap e primeira tarefa

Preservar as oito skills, distribuição e harness. Melhorar primeiro as fronteiras determinísticas, depois fontes canônicas/handoff/revisão e só então medir eficiência. O [roadmap](roadmap.md) contém tarefas MOD-001 a MOD-010, todas planejadas, dependências e critérios. Os [14 diagramas](architecture.md) distinguem fluxo existente de proposta.

MOD-001 alcança `skill-loader/scripts/library_query.py`, `tests/test_skill_loader_query.py` e o contrato de dependência/documentação do loader. Benefício esperado: rejeitar identidade aparente fora de YAML e frontmatter inválido. Aceite: rejeitar manifesto sem delimitadores, nome no corpo, chaves duplicadas, identidade divergente e escapes; aceitar pacote válido, preservar busca e execução stdlib conforme decisão de parser. Rollback: reverter apenas a fatia, preservando evidência e fixtures. Possível regressão: bibliotecas antigas com manifests incompletos podem passar a ser rejeitadas. Não modificar bibliotecas externas automaticamente.

## M. Limitações e cobertura

Inspecionados: oito entrypoints ativos, referências de contratos pertinentes, CLI, schemas, loader, biblioteca, harness, quatro arquivos de testes, workflow, README, documentos operacionais, plano/estado histórico e inventário de arquivos versionados. O inventário documental é exaustivo no conjunto textual classificado; a leitura semântica das 77 cópias históricas e de cada referência especializada não foi exaustiva. Duplicação foi medida por hash, sem inferir equivalência semântica.

Não executados: modelos A/B, sessões novas Claude/Antigravity, instalação em perfis reais, renderização Quarto, benchmarks, scans de segredos/CVEs, CI remota ou ações de escrita no GitHub. Quarto existe no PATH; isso não comprova engines ou outputs. Não foram criados testes de produção, novas skills, mudanças em catálogo/CLI/workflow, commits, push ou releases. O grafo não foi reconstruído. Verificação documental final consta em `delivery-check.json`.
