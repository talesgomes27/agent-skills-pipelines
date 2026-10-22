---
name: quarto-expert
description: "Cria, configura, depura e migra projetos Quarto. Use para células, metadados, referências, HTML/PDF/Typst, books, sites e manuscritos com formatos e execução definidos."
---

# Engenharia de documentos Quarto

Produza o formato solicitado preservando conteúdo, resultados, estrutura e ambiente. A pipeline chamadora mantém seu escopo e gates. Não imponha modelagem, CRISP-ML ou uma norma acadêmica a todo documento.

## Entrada e diagnóstico

- Identifique alvo, idioma, tipo de projeto, formatos e operação: autoria, configuração, erro ou migração. Leia instruções locais e conteúdo existente antes de editar.
- Descubra Quarto no PATH ou caminho explicitamente configurado e registre `quarto --version`. Não adote um perfil pessoal nem instale runtimes globais para iniciar a inspeção.
- Leia configuração, perfis, `_metadata.yml`, YAML do documento, extensões e manifests pertinentes. Use `quarto inspect <alvo>` quando disponível para conferir configuração/engine efetivos; inspeção não comprova renderização.
- Antes de executar, examine células, filtros e scripts pré/pós-render. Render/preview pode executar código, escrever caches e acessar rede. Preserve fontes brutas e alterações do usuário; use ambiente/destino controlados no escopo autorizado.
- Pergunte apenas se faltar formato, requisito ou autorização indispensável. HTML não exige PDF adicional; corrigir sintaxe não autoriza migrar ambiente, instalar hooks ou publicar.

## Referências sob demanda

Resolva os links a partir da raiz instalada desta skill, não do diretório corrente do shell. Leia apenas os guias pertinentes à tarefa.

| Necessidade | Referências |
|---|---|
| Configuração/engine | [yaml-front-matter](references/yaml-front-matter.md), [engines](references/engines.md), [code-cells](references/code-cells.md) |
| Objetos e fontes | [cross-references](references/cross-references.md), [citations](references/citations.md), [figures](references/figures.md), [tables](references/tables.md) |
| Layout | [layout](references/layout.md), [callouts](references/callouts.md), [diagrams](references/diagrams.md), [divs-and-spans](references/divs-and-spans.md) |
| Identidade/acessibilidade | [brand-yml](references/brand-yml.md), [alt-text](references/alt-text.md) |
| Typst/tese | [typst-and-templates](references/typst-and-templates.md), [abnt-thesis-guide](references/abnt-thesis-guide.md) |
| Migração | Uma referência: [Rmd](references/conversion-rmarkdown.md), [Jupyter](references/conversion-jupyter.md), [Bookdown](references/conversion-bookdown.md), [Blogdown](references/conversion-blogdown.md), [Distill](references/conversion-distill.md) ou [Xaringan](references/conversion-xaringan.md) |
| Outros recursos | [extensions](references/extensions.md), [shortcodes](references/shortcodes.md), [conditional-content](references/conditional-content.md), [markdown-linting](references/markdown-linting.md) |

Guias não garantem compatibilidade com toda versão. Confira opções sensíveis à versão na documentação oficial e no alvo; resolva contradições pela evidência, sem carregar o catálogo inteiro.

## Operação

1. **Autoria/configuração:** preserve convenções e use o menor conjunto de opções adequado. Criação nativa Quarto ou template revisado são candidatos; não sobrescreva projeto existente. Diretórios vazios não constituem scaffold Quarto completo.
2. **Células/referências:** distinga execução e exemplo literal. Use opções suportadas pelo engine, com hashpipe apropriado (`#|`, `%%|`, `//|`). Preserve labels; referências cruzadas e chaves bibliográficas têm mecanismos distintos.
3. **Metadados/execução:** confira configuração efetiva. `format` no documento seleciona a lista de formatos; não presuma que apaga todas as opções herdadas do formato selecionado. Cache e freeze têm escopos diferentes e não comprovam freshness de dados externos.
4. **Formato/identidade:** `_brand.yml` depende de versão, formato e tema. Typst, LaTeX, HTML e RevealJS têm capacidades/dependências próprias; binário embutido não elimina fontes, pacotes ou downloads. Escolha motor por requisito.
5. **Migração:** preserve o original e compare código, resultados, bibliografia, labels, navegação e assets no formato-alvo. Renomear arquivo ou converter notebook não prova equivalência. Templates/extensões acrescentam código: confira origem e revisão antes de instalar/executar.
6. **Depuração:** reproduza no menor alvo seguro e identifique a etapa: configuração, código/engine, Pandoc/filtro, compilador ou assets. Corrija a causa e revalide o escopo afetado; não esconda erro nem apague caches apenas para obter sucesso.

## Exemplos

Os três exemplos são pontos de partida: [HTML mínimo](examples/minimal-report/index.qmd), [tese inicial](examples/abnt-thesis-starter/README.md) e [manuscrito](examples/manuscript-binder/README.md). Copie para destino autorizado e revise dados/manifests antes de executar. Gráficos sintéticos devem ser identificados e suas métricas calculadas.
Margens, template e compilação não certificam ABNT, PDF/A ou prontidão de produção. Verifique requisitos institucionais e outputs próprios; sem acesso ao requisito, explicite o limite.

## Verificação e manutenção

Confira YAML, bibliografia, referências e sintaxe; execute somente formatos/engines necessários e inspecione outputs pertinentes. Registre comando, versão, engine/ambiente, resultado e limitações. Separe configuração inspecionada, render executado, output inspecionado e conformidade avaliada.
Para manter o pacote, use [scripts/doctor.py](scripts/doctor.py): `python3 <raiz-da-skill>/scripts/doctor.py --root <raiz-da-skill>`. O padrão lê o pacote. `--runtime` verifica Quarto; `--render-smoke` renderiza HTML sem código em diretório temporário. `--quarto <executavel>` seleciona caminho explícito. Nenhum modo valida automaticamente R, Python, ABNT, PDF ou documento do usuário.
Sem PyYAML, o doctor relata YAML não verificado; não instala dependências. Exits/JSON: 0 = checks solicitados passaram; 1 = falha; 2 = check não executado sem outra falha. Nunca converta render pulado em sucesso de render.
Não instale hooks, substitua `.git/hooks`, altere perfil global ou apague backups automaticamente. Integração de ambiente fica em procedimento separado com alvo e efeitos explícitos.

## Integração

Use `writing-pipeline` quando necessária à revisão textual. Graphify é independente da autoria/renderização e não deve ser requisito para editar `.qmd`. Seu guia compartilhado é passivo e precisa ser conferido para a versão em uso em tarefas explícitas de grafo.
MCP não é obrigatório: CLI Quarto e verificadores locais atendem à configuração/renderização; conectores existentes podem recuperar fontes autorizadas quando necessário. Devolva artefatos, evidências e pendências, sem marcar aprovação humana ou publicar como efeito da compilação.
