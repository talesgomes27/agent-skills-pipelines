# Changelog

As versões seguem [SemVer](https://semver.org/lang/pt-BR/).

## [Não publicado]

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
