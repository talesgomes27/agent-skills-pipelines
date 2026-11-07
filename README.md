# Agent Skills Pipelines

[![CI](https://github.com/talesgomes27/agent-skills-pipelines/actions/workflows/ci.yml/badge.svg)](https://github.com/talesgomes27/agent-skills-pipelines/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/badge/release-3.4.0-blue.svg)](distribution/catalog.json)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Codex%20%7C%20Claude%20Code%20%7C%20Antigravity-6f42c1.svg)](docs/distribution/architecture.md)

Uma skill é uma pasta de instruções que um agente de IA, como o Claude Code, o Codex ou o Antigravity, lê quando a tarefa pede. Estas skills, em português, dão ao agente um processo de trabalho: planejar antes de programar, implementar em etapas verificadas, auditar código herdado e publicar só com a sua autorização. Foram pensadas para ciência de dados, sites e dashboards em Streamlit ou Shiny, e automações.

Release atual: **3.4.0**.

## Como é na prática

Você pede: *"Quero um dashboard em Streamlit com as vendas mensais por loja, publicado para a equipe."*

1. A `pre-code-pipeline` entra antes de qualquer código. Ela lê os dados, pergunta só o que muda a decisão e escreve escopo, arquitetura e plano. Por padrão, para e espera o seu aceite no escopo, na arquitetura e no plano.
2. A `execution-pipeline` implementa o plano aprovado em fatias: lógica com testes, integração com os dados, telas, documentação e revisão. Para o Streamlit, ela usa a skill oficial do próprio Streamlit, se estiver instalada.
3. A `release-and-ops-pipeline` confere o que vai ser enviado, publica e testa o app publicado. Push, deploy, conta nova ou envio de dados a terceiros só acontecem com o seu aceite.

Um pedido pequeno, como uma análise pontual ou a correção de um bug, passa por menos etapas: as pipelines ajustam o esforço ao risco e dizem qual escolheram. Se você aprovar a sequência toda de uma vez, o agente segue sem parar em cada etapa, mas ainda para quando o escopo muda, surge uma decisão sua ou há risco de perder trabalho.

Você não precisa chamar as skills: o agente as escolhe pelo pedido. Para forçar uma, peça pelo nome; no Claude Code, as skills dos plugins têm o prefixo do plugin, como `pre-code-pipeline:pre-code-pipeline`.

As pipelines separam o trabalho em três tipos, cada um com as suas regras de teste e de publicação:

- **A, análise e modelos:** notebooks, machine learning, relatórios e Quarto.
- **B, aplicações:** sites, APIs e dashboards em Streamlit ou Shiny.
- **C, automações:** scripts, CLI, jobs agendados e ETL.

## Skills

Pipelines, que conduzem uma etapa inteira do trabalho, com paradas para o seu aceite:

| Skill | Quando entra |
|---|---|
| [`pre-code-pipeline`](pre-code-pipeline/SKILL.md) | Antes de programar: descoberta, escopo, arquitetura e plano. |
| [`execution-pipeline`](execution-pipeline/SKILL.md) | Para implementar um plano aprovado, com testes proporcionais à stack. |
| [`audit-and-refactoring-pipeline`](audit-and-refactoring-pipeline/SKILL.md) | Para entender e refatorar código ou notebooks herdados sem quebrar o que funciona. |
| [`release-and-ops-pipeline`](release-and-ops-pipeline/SKILL.md) | Para publicar: saneamento, versão, CI, deploy autorizado e teste do que foi publicado. |
| [`writing-pipeline`](writing-pipeline/SKILL.md) | Para redigir ou revisar documentos técnicos e de negócio sem perder fatos e fontes. |

Especialistas, que as pipelines chamam quando o assunto aparece:

| Skill | Quando entra |
|---|---|
| [`scheduled-automation`](scheduled-automation/SKILL.md) | Jobs agendados, ETL recorrente e retreino de modelo: estado, falhas, alertas e primeira execução. |
| [`personal-data`](personal-data/SKILL.md) | Dados de pessoas em análises, apps e listas, com base na LGPD. |
| [`quarto-expert`](quarto-expert/SKILL.md) | Ambiente e render de projetos Quarto, teses em ABNT e manuscritos com Binder. |
| [`skill-loader`](skill-loader/SKILL.md) | Buscar uma skill numa biblioteca externa grande, sem carregar tudo. Veja [biblioteca externa](docs/library-maintenance.md). |

## Instalação

### Claude Code

O repositório é um marketplace de plugins, com um plugin por skill e dois pacotes. Para o fluxo do exemplo acima, instale o pacote `essencial`, que traz as três pipelines e a `personal-data`:

```bash
claude plugin marketplace add talesgomes27/agent-skills-pipelines@stable
claude plugin install essencial@agent-skills-pipelines
```

O pacote `completo` instala as nove skills. Os pacotes não têm conteúdo próprio: eles instalam os plugins das skills como dependências. Ao desinstalar um pacote, o Claude Code mantém essas dependências e sugere `claude plugin prune`, que remove só as que ele instalou automaticamente, não as que você instalou à mão.

Cada uma dessas três pipelines traz um subagente de revisão que o Claude Code pode chamar sozinho nesse ponto, ou que você chama pelo nome, como `@agent-pre-code-pipeline:plan-reviewer`: `plan-reviewer` revisa o plano antes do seu aceite, `diff-reviewer` revisa o diff no fim da implementação e `sanitation-checker` confere segredos, dados pessoais e arquivos grandes antes de publicar. Eles relatam e não editam.

Acrescente as outras skills da tabela uma a uma, com `claude plugin install <skill>@agent-skills-pipelines`. A branch `stable` só avança quando sai uma release, então você recebe só versões publicadas; para fixar uma versão exata, use uma tag, como `@v3.4.0`, no lugar de `@stable`. Sem o `@`, o marketplace acompanha a `main`, que muda a cada PR. Abra uma sessão nova para o Claude Code encontrá-las. No Claude Code, prefira o marketplace ao instalador abaixo: ele atualiza com `claude plugin update`.

### Codex, Antigravity e outros hosts

O instalador instala grupos de skills, os bundles. O `development` traz planejamento, execução, auditoria, automações e dados pessoais; o `research` troca a auditoria e as automações por escrita e Quarto. Com Python 3.9 ou mais novo:

```bash
git clone --branch stable https://github.com/talesgomes27/agent-skills-pipelines.git
cd agent-skills-pipelines
python3 -m venv .venv
.venv/bin/python -m pip install -r distribution/requirements.txt
# Mostra o que seria instalado, sem gravar nada
.venv/bin/python scripts/skills.py install --agent codex --bundle development --dry-run
.venv/bin/python scripts/skills.py install --agent codex --bundle development
```

Troque `codex` por `antigravity` ou `antigravity-cli`. No Windows, use `.venv\Scripts\python.exe`. Para atualizar, repita o comando com `--update`: cópias que você editou à mão não são sobrescritas.

O [guia de instalação](docs/distribution/architecture.md) tem os destinos de cada host, todos os bundles, a instalação por link e o que fazer quando uma instalação falha.

### Skills oficiais de frameworks

Para o conhecimento de cada framework, as pipelines usam as skills que os próprios fabricantes mantêm. Instale as que o seu trabalho usa:

| Framework | Skills | Instalação |
|---|---|---|
| Streamlit 1.58 ou mais novo | `developing-with-streamlit` | `streamlit skills` na pasta do projeto, ou `streamlit skills --global` |
| Shiny para Python | `shiny-for-python` | Na pasta do app, com o `shiny` no ambiente do projeto: `uvx library-skills --claude` no Claude Code, `uvx library-skills` nos outros hosts |
| Shiny em R e Posit Connect | `shiny-bslib`, `shiny-r-optimize`, `deploy-to-connect` e outras | `claude plugin marketplace add posit-dev/skills`, depois `claude plugin install shiny@posit-dev-skills` e `connect@posit-dev-skills`; nos outros hosts, `npx skills add posit-dev/skills` |
| Sites e apps na Vercel | `vercel-react-best-practices`, `web-design-guidelines`, `deploy-to-vercel` | `npx skills add vercel-labs/agent-skills` |
| Plataforma da Vercel | `auth`, `domains`, `env-vars`, `deployments-cicd`, `ai-sdk` e outras | `npx plugins add vercel/vercel-plugin` |
| Claude API e documentos | `claude-api`, `docx`, `pdf`, `pptx`, `xlsx` | `claude plugin marketplace add anthropics/skills`, depois `claude plugin install claude-api@anthropic-agent-skills` e `document-skills@anthropic-agent-skills` |
| Quarto (autoria e migração) | `quarto-authoring`, `brand-yml`, `alt-text` | Com o marketplace da Posit, `claude plugin install quarto@posit-dev-skills`; nos outros hosts, `npx skills add posit-dev/skills --skill quarto-authoring` |

As do Streamlit e do Shiny para Python vêm dentro da biblioteca e acompanham a versão instalada no projeto. O `library-skills` descobre o projeto pelo ambiente Python: numa pasta sem ambiente próprio, ele pode adotar a pasta pessoal e copiar a skill para `~/.claude/skills` e `~/.agents/skills`.

## Documentação

- [Guia de instalação](docs/distribution/architecture.md): destinos, bundles, atualização, recuperação e confirmação antes de publicar no Claude Code.
- [Verificação de descoberta](docs/distribution/discovery.md): como confirmar que o host encontra as skills.
- [Biblioteca externa](docs/library-maintenance.md): a `skill-loader` e a manutenção do índice.
- [Notas de manutenção](docs/maintainers.md): validação, contratos do doctor e CI.
- [Changelog](CHANGELOG.md) e [avisos de terceiros](NOTICE.md).

## Contribuir

As regras do repositório estão no [AGENTS.md](AGENTS.md), escrito para pessoas e agentes: limite de tamanho das skills, fontes oficiais, uma branch por mudança e como validar. Antes de abrir um PR, rode os testes, o doctor e o validador do plugin, com um Python que tenha o PyYAML:

```bash
python3 -m unittest discover -s tests
python3 scripts/skills.py doctor
claude plugin validate --strict .
```

## Licença

Distribuído sob a [licença MIT](LICENSE).
