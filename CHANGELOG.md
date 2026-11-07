# Changelog

As versões seguem [SemVer](https://semver.org/lang/pt-BR/).

## Não publicado

### Novo

- Formulário de issue "A skill errou" (`.github/ISSUE_TEMPLATE/skill-errou.yml`). O `AGENTS.md` pede que cada issue aceita vire primeiro um cenário que falha, no mesmo PR da correção.
- Linha de base da 3.3.0 em `evals/results/3.3.0/`, com o claude-sonnet-5-5 no Claude Code:
  - no nível de leitura, os 17 cenários e os 37 gatilhos: 46 de 52 checkpoints `deve` aprovados, nenhuma falha `nao_deve` e todos os gatilhos como esperado;
  - no nível de execução, quatro cenários em sessões reais (`claude -p`): 6 de 15 `deve` e nenhuma falha `nao_deve`. Em duas rodadas, API com migração e Script de fotos, nenhuma skill do repositório foi carregada.
  - Os resultados ficam em pastas por nível, `evals/results/<versão>/<nível>/`.
- `/cenarios` lê `evals/scenarios/`, roda nos níveis de leitura ou de execução e grava os resultados em `evals/results/<versão>/`, e o `skill-prober` devolve o resultado em JSON.
- O `/preparar-release` exige resultados da versão nova para as skills alteradas, e uma regressão bloqueia a release salvo justificativa no CHANGELOG. `evals/matrix.yaml` declara as combinações de host e modelo, `evals/report.py` gera a tabela dos resultados, e `tests/test_evals.py` confere os dois.
- Os 17 cenários de comportamento e os 37 prompts de gatilho saem das tabelas de `docs/distribution/discovery.md` para `evals/scenarios/` e `evals/triggers.yaml`, cada cenário com checkpoints `deve` e `nao_deve`.
- Pasta `evals/` com o formato de cenários, gatilhos e resultados por versão, e `tests/test_evals.py` conferindo esse formato sem chamar modelo. O `AGENTS.md` passa a permitir avaliações nessa pasta, sem framework nem dependência nova.
- Três subagentes de revisão do Claude Code, que só leem e relatam, declarados nas entradas do marketplace e chamados pela descrição: `pre-code-pipeline:plan-reviewer` no Gate 5 do planejamento, `execution-pipeline:diff-reviewer` no Gate 5 da execução e `release-and-ops-pipeline:sanitation-checker` no saneamento da release. Eles relatam sem editar e não substituem o aceite do usuário.

### Mudanças

- CI: `timeout-minutes` nos jobs e `concurrency` que cancela a rodada antiga de um PR. O push só dispara na `main`, e os testes conferem o "Use quando" e o limite de 1.024 caracteres das `description`. Um workflow semanal, `links.yml`, roda `scripts/check_links.py` sobre os links externos das skills e da documentação.
- Exemplos Quarto:
  - Acentos corrigidos e introdução sem duplicata na tese.
  - Bloco `{#refs}` na tese e uma entrada de exemplo em cada `.bib`.
  - Estilo ABNT (`associacao-brasileira-de-normas-tecnicas.csl`, CC BY-SA 3.0, registrado no `NOTICE.md`) para a tese renderizar sem rede.
  - Versões fixadas no `requirements.txt` do manuscrito.
- O limite do `SKILL.md` no doctor sobe de 8.000 para 10.000 caracteres, cerca de 4 mil tokens. Fica abaixo dos 5 mil que a especificação recomenda e que o Claude Code recoloca de cada skill depois de uma compactação. Os cortes para caber em 8.000 estavam criando ambiguidade.
- Um app novo que a `pre-code-pipeline` aprovou como leve continua leve na `execution-pipeline`. O pedido de construí-lo já autoriza implementar depois do aceite do plano. O único aceite que falta é o do fim do Gate 5, e as paradas do modo contínuo continuam valendo.
- O teste que outra skill pede, como a ponytail, entra no plano sem substituir nem reduzir os testes dele, e vem antes do código como eles.
- Num app novo leve, com um só aceite pelos Gates 2, 3 e 5, a restrição do destino que muda a arquitetura vai no início da resposta, antes do escopo.
- A `scheduled-automation` diz que um job novo com credencial ou efeito externo não é leve. Regras de brevidade não tiram itens do contrato: alerta, estado, idempotência e a decisão de falha parcial ficam, e o sinal de vida também, num job importante.
- `refactoring-patterns-abc.md` ganha um roteiro para app Shiny em R num único `app.R`. Primeiro, caracterizar com `testServer()` e `shinytest2`. Depois, medir pela `shiny-r-optimize` ou com `profvis`, deixando o `reactlog` para o usuário. Por fim, modularizar e só então otimizar, repetindo a medida a cada fatia. Instalar `shinytest2`, o Chrome ou `profvis` pede aceite.
- Pedido com login decide no Gate 2 quem cria as contas e como se recupera a senha, e login com senha tira o app do esforço leve. App que grava dados diz, mesmo no leve, como copiar e restaurar.
- A referência de migrações diz o que fazer sem ambiente de ensaio: ensaiar no backup restaurado num banco temporário protegido. Se nem isso der, dizer ao usuário que a migração vai sem ensaio e com backup não testado, e pedir a autorização sabendo disso.
- Ajustes de redação na `pre-code-pipeline` para caber no limite de 8.000 caracteres, sem mudar regras.
- O guia de instalação ganha a seção "Claude Code: confirmação antes de publicar", com regras `ask` de permissão para push, merge, release, disparo de workflow e deploy. Ela explica a precedência entre deny, ask e allow e os limites de uma regra que compara texto de comando. As skills não mudam.

## [3.3.0] - 2026-11-07

Comparada com a 3.2.0 (`e133b8e`). Acrescenta a regra de precedência sobre skills de brevidade e o esforço leve para app novo pequeno, e reescreve a documentação, sem quebra de compatibilidade.

### Mudanças

- As quatro pipelines dizem como convivem com regras de brevidade de outra skill sempre ativa, como a ponytail: elas valem dentro do escopo aprovado e não dispensam gate, aceite, testes, rede de segurança, saneamento nem smoke. Um pedido vago vira uma versão mínima no plano, não código.
- O esforço leve da `pre-code-pipeline` passa a cobrir app novo pequeno, de uso interno, sem dados sensíveis nem acesso público: os gates cabem numa resposta, com um aceite que vale pelos Gates 2, 3 e 5. O formato de `docs/00_archetype.md`, as restrições do destino em B e C e onde cada verificação roda passam para `architecture-by-archetype.md`.
- Documentação reescrita para quem chega ao projeto: o README diz o que é uma skill, mostra um pedido do começo à publicação, separa pipelines de especialistas e indica o que instalar primeiro. `docs/distribution/architecture.md` vira o guia de instalação, e os contratos do doctor, a transação por skill e a manutenção da CI vão para `docs/maintainers.md`. A biblioteca fria passa a se chamar biblioteca externa.

### Como atualizar

- No Claude Code, rode `claude plugin marketplace update agent-skills-pipelines` e `claude plugin update <plugin>` para cada plugin instalado. Não há plugin novo.
- Instalações feitas com `scripts/skills.py` recebem a 3.3.0 com `--update`. Nenhuma skill entra ou sai e nenhuma referência muda de nome. Cópias editadas à mão continuam protegidas.

## [3.2.0] - 2026-11-07

Comparada com a 3.1.0 (`9755dd5`). Acrescenta regras de agendamento e de previsão de séries, sem quebra de compatibilidade.

### Mudanças

- `scheduled-automation`: o agente propõe ao usuário um minuto fora da hora cheia em vez de escolher sozinho, e a referência do GitHub Actions ganha a receita do SQLite num bucket: baixar dentro do `concurrency`, gerar a cópia com `VACUUM INTO`, conferir com `integrity_check`, subir com nome datado e manter as versões anteriores. O aviso de falha do próprio GitHub conta como alerta independente quando chega ao usuário.
- A arquitetura de A na `pre-code-pipeline` passa a definir, para previsão de séries, validação por origem móvel, baseline ingênuo sazonal e erro escalado como o MASE. Quando a diferença entre modelos não se sustenta, o agente recomenda o mais simples. O retreino em `model-in-production.md` usa o mesmo protocolo.
- O repositório ganha `AGENTS.md` e automações do Claude Code para quem mantém as skills: hooks com o doctor e os testes, as skills `/cenarios` e `/preparar-release` e os subagentes `skill-prober` e `rule-keeper`. Nada disso é carregado pelos plugins nem instalado pelo `skills.py`.

### Como atualizar

- No Claude Code, rode `claude plugin marketplace update agent-skills-pipelines` e `claude plugin update <plugin>` para cada plugin instalado. Não há plugin novo.
- Instalações feitas com `scripts/skills.py` recebem a 3.2.0 com `--update`. Nenhuma skill entra ou sai e nenhuma referência muda de nome. Cópias editadas à mão continuam protegidas.

## [3.1.0] - 2026-11-07

Comparada com a 3.0.0 (`1c26256`). Acrescenta a skill `personal-data`, ajustes de processo e conteúdo técnico para web, apps com LLM, modelo em produção e notebooks herdados, sem quebra de compatibilidade.

### Novo

- Skill `personal-data`, para trabalho com dados de pessoas: inventário dos campos pessoais e sensíveis, minimização e pseudonimização com chave (hash simples de CPF é reversível), saídas só com agregados e grupos pequenos omitidos, onde os dados ficam, envio a provedores externos como decisão do usuário, coleta e vazamento. A referência `lgpd-basics.md` traz os pontos da Lei 13.709/2018 que a skill usa. Entra nos bundles `development` e `research`.
- `execution-pipeline/references/llm-apps.md`: apps com LLM, com provedor e modelo fixados, chave no cofre e limite de gasto, login corporativo, respostas que citam a origem e dizem quando não sabem, texto dos documentos como entrada não confiável, conjunto de avaliação rodado a cada mudança e operação.
- `audit-and-refactoring-pipeline/references/inherited-notebooks.md`: reconhecimento de uma pasta de notebooks herdada, com mapa de entradas e saídas sem executar, execução só numa cópia isolada e entrega em três listas.
- Seção "Sites e APIs" em `execution-pipeline/references/archetype-b.md`: segurança mínima, acessibilidade, desempenho, SEO e formulário, com apontamentos para as skills oficiais da Vercel e para o `/security-review` do host.
- Receita de relatório executivo em `writing-pipeline/references/document-types.md`.
- `release-and-ops-pipeline/references/db-migrations.md`: migração de banco em produção com backup testado, ensaio, etapas compatíveis (expandir, publicar, migrar, contrair), travas e como voltar. A release e a referência B da execution apontam para ela.
- Seção da Vercel em `release-and-ops-pipeline/references/app-platforms.md` (antes `data-app-platforms.md`): preview e produção, primeiro deploy, variáveis por ambiente, domínio e DNS, Instant Rollback.
- Regras de coleta externa em `execution-pipeline/references/archetype-c.md`: API oficial antes de raspar, termos de uso e robots.txt, ritmo, parar diante de login ou CAPTCHA, fixtures para os seletores.
- `pre-code-pipeline/references/architecture-by-archetype.md`, com o detalhe do Gate 3 por arquétipo.
- Cenários de comportamento em `docs/distribution/discovery.md`, para repetir com agentes depois de cada mudança.

### Mudanças

- `scheduled-automation/references/model-retraining.md` vira `model-in-production.md` e passa a cobrir a passagem do notebook para o pipeline, o mesmo código de features no treino e na pontuação, artefato e versões, lote ou API, e limiar e entrega da lista, além do retreino. A descrição da skill passa a citar a pontuação periódica.
- O README lista as skills oficiais da Vercel e da Anthropic, com os comandos de instalação.
- `pre-code-pipeline` ganha a entrega pontual: análise, script ou documento entregue uma vez é planejado numa só resposta, com um aceite, e entregue pela `execution-pipeline`.
- O caminho rápido da `execution-pipeline` passa a aceitar leitura de páginas ou APIs públicas, com as regras de coleta externa.
- Na `release-and-ops-pipeline`, site estático só vai para a referência de GitHub Pages quando o destino é o GitHub Pages; Vercel e Netlify entram em app ou serviço.
- `writing-pipeline` e `skill-loader` ganham descrições que dizem só quando usá-las, como as outras skills.
- A `execution-pipeline`, a `scheduled-automation` e as referências de arquitetura, de A, de auditoria analítica e de saneamento apontam para a `personal-data`.
- Para abrir espaço, detalhes de saneamento e de recuperação de fatias saíram da release e da audit para as referências que já os tinham.

### Como atualizar

- No Claude Code, rode `claude plugin marketplace update agent-skills-pipelines` e `claude plugin update <plugin>` para cada plugin instalado. A `personal-data` é um plugin novo: `claude plugin install personal-data@agent-skills-pipelines`.
- Instalações feitas com `scripts/skills.py` recebem a 3.1.0 com `--update`. Repetir a instalação dos bundles `development` ou `research` com `--update` também instala a `personal-data`. As cópias perdem `data-app-platforms.md` e `model-retraining.md`, que mudaram de nome, e ganham as referências novas. Cópias editadas à mão continuam protegidas.
- As skills oficiais da Vercel e da Anthropic são opcionais; a seção "Skills oficiais de frameworks" do README mostra como instalá-las.

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
