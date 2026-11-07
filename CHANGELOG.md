# Changelog

As versões seguem [SemVer](https://semver.org/lang/pt-BR/).

## [3.0.0] - 2026-11-07

Comparada com a 2.1.0 (`88f9b04`). É uma MAJOR porque a `quarto-expert` deixou de cobrir autoria, sintaxe e migração de Quarto.

### Quebra de compatibilidade

- A `quarto-expert` passa a cobrir só ambiente e render de projetos Quarto, teses em ABNT e manuscritos com Binder. Saíram 23 referências: 20 eram cópias idênticas das da `quarto-authoring` da Posit, `alt-text.md` e `brand-yml.md` eram versões das skills de mesmo nome da Posit, e `rmd-to-quarto-migration.md` repetia a `conversion-rmarkdown` dela, com regras conflitantes. Quem usava a `quarto-expert` para autoria, sintaxe ou migração deve instalar o plugin `quarto@posit-dev-skills`.

### Novo

- Skill `scheduled-automation`, para jobs que rodam sem ninguém olhando: script ou workflow agendado, ETL recorrente, bot que envia mensagens e retreino de modelo. Ela define o contrato do job (gatilho e fuso, janela, estado, idempotência, falhas, segredos, alertas e execução que não rodou), dry-run, testes e primeira execução, com referências para o GitHub Actions como agendador e para retreino agendado. Entra no bundle `development`.
- `NOTICE.md` com o aviso da licença MIT da Posit para os arquivos de `posit-dev/skills` que a `quarto-expert` distribuiu na 2.0.0 e na 2.1.0 sem esse aviso.

### Mudanças

- No modo assistido, as pipelines esperam o aceite só nos marcos com decisão: `pre-code-pipeline` e `audit-and-refactoring-pipeline` nos Gates 2, 3 e 5, `execution-pipeline` nos Gates 3 e 5 e `release-and-ops-pipeline` nos Gates 2, 4 e 5. Os outros gates são apresentados e entram no aceite seguinte; as paradas por mudança de escopo, decisão bloqueante, conflito e risco de perda continuam.
- `pre-code-pipeline`, `execution-pipeline` e a referência C da execution apontam para a `scheduled-automation`.
- `execution-pipeline`, a referência A dela, a `writing-pipeline` e o README separam a `quarto-authoring`, para autoria, da `quarto-expert`, para ambiente, render e ABNT.

### Como atualizar

- No Claude Code, rode `claude plugin marketplace update agent-skills-pipelines` e `claude plugin update <plugin>` para cada plugin instalado. A `scheduled-automation` é um plugin novo: `claude plugin install scheduled-automation@agent-skills-pipelines`.
- Instalações feitas com `scripts/skills.py` recebem a 3.0.0 com `--update`, e a `quarto-expert` copiada perde as referências removidas. Repetir a instalação do bundle `development` com `--update` também instala a `scheduled-automation`. Cópias editadas à mão continuam protegidas.
- Para autoria, sintaxe e migração de Quarto, instale o plugin `quarto@posit-dev-skills` ou, fora do Claude Code, `npx skills add posit-dev/skills --skill quarto-authoring`.

## [2.1.0] - 2026-11-07

Comparada com a 2.0.0 (`014ec10`). Adapta as pipelines a ciência de dados, dashboards em Streamlit e Shiny e automações, sem quebra de compatibilidade.

### Mudanças

- Os arquétipos mantêm as letras e mudam de definição: A = análise e modelos, B = aplicações (incluindo dashboards em Streamlit e Shiny), C = automações (incluindo jobs agendados e ETL). Classificações já gravadas em `docs/00_archetype.md` continuam valendo.
- `execution-pipeline` aceita uma tarefa pequena sem plano formal: local, reversível, sem efeito externo e sem mudar interface que outro sistema usa.
- `pre-code-pipeline` permite exploração descartável dos dados nos Gates 1 e 2, pede na arquitetura as restrições do destino e, no plano, onde cada verificação roda.
- `execution-pipeline` e `release-and-ops-pipeline` separam ler dados reais com credencial só de leitura de escrever ou enviar.
- `release-and-ops-pipeline` escolhe o destino pelo que será entregue e ganha app em plataforma e job agendado, com smoke próprio.
- As referências por arquétipo cobrem dashboards e jobs agendados.
- As pipelines usam as skills oficiais do Streamlit, do Shiny para Python e da Posit como especialistas. Elas dizem como fazer; gates, escopo e autorizações continuam os da pipeline. O README lista como instalá-las.

### Novo

- `release-and-ops-pipeline/references/data-app-platforms.md`, para publicar no Streamlit Community Cloud e no shinyapps.io: dependências, segredos, acesso privado, hibernação e smoke de app privado. O Posit Connect fica com a skill `deploy-to-connect` da Posit.

### Como atualizar

- No Claude Code, rode `claude plugin marketplace update agent-skills-pipelines` e depois `claude plugin update <plugin>` para cada plugin instalado.
- Instalações feitas com `scripts/skills.py` recebem a 2.1.0 com `--update`. Cópias editadas à mão continuam protegidas.
- As skills oficiais do Streamlit, do Shiny e da Posit não vêm com este repositório; a seção "Skills oficiais de frameworks" do README mostra como instalá-las.

## [2.0.0] - 2026-11-07

Comparada com a 1.0.1 (`869444d`), a última versão anunciada no README. A candidata 2.0.0 que esteve na `main` entre 30/10 e 07/11 nunca foi publicada; esta versão a substitui.

### Quebra de compatibilidade

- A skill `humanizer` saiu do catálogo e do bundle `editorial`. Use a do host, como o plugin `humanizer` do Claude Code.
- Saiu o harness de avaliações: `scripts/evals.py`, a pasta `evals/` e o formato JSON da saída do `grade`.
- `doctor` e `install` recusam `SKILL.md` com mais de 8.000 caracteres e validam o frontmatter com mais rigor: chaves únicas, `name` igual ao da pasta e `description` obrigatória.
- As quatro pipelines (`pre-code`, `execution`, `audit-and-refactoring` e `release-and-ops`) foram reescritas e ficaram de 26% a 51% menores. Gates, modos e limites de autorização continuam, mas o texto mudou: releia a skill antes de depender de uma regra específica.

### Novo

- Marketplace de plugins do Claude Code em `.claude-plugin/marketplace.json`, com um plugin por skill.
- `quarto-expert/scripts/offline_probe.py`, que inventaria o Quarto e as engines sem acessar a rede.
- Prompts de gatilho por skill em `docs/distribution/discovery.md`, para conferir a descoberta à mão em cada host.

### Mudanças

- A checklist do Quarto usada pela `pre-code-pipeline` trocou regras obrigatórias por condicionais.
- A `description` de cada pipeline diz só quando usar a skill.
- Saíram do repositório as auditorias, os experimentos, o `task.md`, `release-candidate/`, `ci/` e o workflow de homologação. Tudo continua no histórico do Git; a tag `archive/mod-2026-10` marca o estado anterior à limpeza.

### Como atualizar

- Instalações feitas com `scripts/skills.py` só recebem a 2.0.0 com `--update`. Cópias editadas à mão continuam protegidas.
- O instalador não remove pacotes que saíram do catálogo. Se você instalou a `humanizer` por este repositório, ela fica onde está até você removê-la.
