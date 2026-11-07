# Mudanças condicionais por arquétipo

Um padrão é candidato, não objetivo obrigatório. Preserve a stack e o desenho saudável do projeto; cada mudança precisa de problema, escopo, contrato e verificação.

## A: dados, ciência e publicação

Extraia lógica de notebook quando melhorar teste/reuso comprovado, preservando ordem, efeitos e interfaces. Não force `src/` ou notebook adicional a um relatório funcional.
Vetorização ou troca de biblioteca pode alterar precisão, ordenação, tratamento de nulos, execução e uso de memória. Classifique como otimização/migração e compare resultados e desempenho com dados representativos antes de declarar ganho.
Leakage, split, seed, estimador e métrica são decisões metodológicas que podem mudar resultados. Faça correção aprovada com critérios próprios, sem chamá-la de refatoração equivalente.
Reorganização de relatório, idioma, política de cache, estética, DPI e formato dependem do destino e pedido. Não introduza SHAP/modelos em análise descritiva nem migre R Markdown/ambiente só por preferência. Mudança de engine ou dependências é migração separada, com paridade avaliada.

## B: aplicações, APIs e dashboards

Extraia serviços/repositórios apenas quando separar responsabilidade ou reduzir acoplamento real; não crie camadas para todo controlador.
Preserve schema, status, erros, autorização, transações, concorrência e compatibilidade dos consumidores. Otimizações SQL precisam preservar resultados, ordenação contratada e garantias transacionais. Índice/migração pode ter custo e efeitos operacionais, além do diff de código.
Em dashboard, separar consulta, transformação e interface costuma ser a primeira fatia. Para diagnosticar lentidão, use a skill oficial quando instalada (`shiny-r-optimize`, `shiny-py-optimize` ou a referência de desempenho do Streamlit), sem aplicar correções fora do modo autorizado. Ganho de desempenho só vale medido: registre o tempo da interação lenta antes e depois, com os mesmos dados, e trate cache novo como mudança de comportamento quando ele pode mostrar dado antigo.

Num app Shiny em R num único `app.R`, siga esta ordem. Instalar `shinytest2`, o Chrome ou `profvis` é dependência nova e pede o aceite do usuário, e tudo roda no ambiente isolado que a auditoria autorizou.

1. Caracterize antes de mudar. `testServer()` aceita o próprio app, não só módulos, e confere valores reativos e saídas sem navegador. O `shinytest2` grava a interação com `record_test()` e a repete num Chrome headless pelo `chromote`; use-o para os valores exibidos depois de mudar um filtro. Snapshots não guardam segredos nem dados pessoais.
2. Meça antes de otimizar, pelo roteiro da `shiny-r-optimize` quando instalada. Sem ela, rode o app dentro de `profvis({ shiny::runApp() })`, com a interação lenta feita pelo usuário ou por um `AppDriver` do `shinytest2`, e veja onde vai o tempo. O `reactlog` mostra o grafo reativo e fica para o usuário explorar. Meça com dados sem linhas pessoais, porque os registros guardam valores.
3. Modularize em fatias, com os testes passando, e otimize depois, repetindo a mesma medida ao fim de cada fatia. Assim o ganho medido não se mistura com a mudança de estrutura.

Fontes: [testServer](https://shiny.posit.co/r/reference/shiny/latest/testserver.html), [shinytest2](https://rstudio.github.io/shinytest2/), [profvis](https://profvis.r-lib.org/articles/examples.html) e [reactlog](https://rstudio.github.io/reactlog/).

Renomeações e codemods devem considerar imports, configuração, serialização, referências dinâmicas e chamados externos; parser/IDE ajuda, mas testes e revisão continuam necessários.

## C: automações e CLI

Separar parser e lógica pode facilitar testes. Transformar um comando existente em subcomandos ou trocar dependências pode quebrar flags, códigos de saída, mensagens e pipelines; precisa de contrato de compatibilidade e autorização.
Confira stdout/stderr, quoting, ambiente, arquivos, interrupções e idempotência pertinentes. Uma nova mensagem de erro não é apenas estilo quando integrações a consomem. Em job agendado, preserve horário, fuso, chave de idempotência e o estado entre execuções.

## Aplicação e integração

Não altere golden files, tolerâncias ou testes para esconder uma diferença. Para correção intencional, atualize evidência e expectativa com justificativa.
Use fatias com propriedade de arquivos e pré-requisitos claros. Paralelismo não é obrigatório; só execute mudanças independentes quando capacidade e autorização existirem. Revise integração antes do aceite.
Não rode formatador com reescrita no reconhecimento nem misture migração de ambiente e mudança de lógica em uma fatia sem razão verificável.
