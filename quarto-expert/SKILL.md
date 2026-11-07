---
name: quarto-expert
description: "Use quando um projeto Quarto precisa de diagnóstico de ambiente ou de render (qual Quarto, Python ou R executa, LaTeX ou Typst, máquina sem rede, erro que só acontece numa máquina), de tese ou trabalho acadêmico em ABNT, ou de manuscrito reprodutível com Binder."
---

# Ambiente, render e trabalhos acadêmicos em Quarto

Esta skill cuida do que faz um projeto Quarto renderizar no ambiente certo e dos trabalhos acadêmicos. Para autoria e sintaxe (callouts, tabelas, figuras, referências cruzadas, citações, YAML, extensões) e para migrar de R Markdown, bookdown, blogdown, xaringan, distill ou Jupyter, use a `quarto-authoring` da Posit quando ela estiver instalada. Sem ela, informe o comando de instalação (`claude plugin install quarto@posit-dev-skills` ou `npx skills add posit-dev/skills --skill quarto-authoring`), que fica a critério do usuário, e siga a documentação oficial do Quarto. A pipeline chamadora mantém escopo, gates e autorizações. Não imponha modelagem, CRISP-ML ou norma acadêmica a todo documento.

## Diagnóstico

- Identifique alvo, formatos, idioma e o sintoma: erro de render, saída diferente entre máquinas, dependência ausente. Leia instruções locais e o conteúdo existente antes de editar, e não sobrescreva um projeto existente.
- Descubra o Quarto no PATH ou no caminho configurado. Com execução autorizada, registre `quarto --version`; a presença do arquivo não comprova funcionamento. Preserve perfis e runtimes globais.
- Sem autorização de rede, comece com o [inventário offline](references/offline-diagnostics.md): `python3 <raiz-da-skill>/scripts/offline_probe.py`. Ele só consulta arquivos locais. `quarto tools` consulta versões remotas, mesmo sem instalar, e exige autorização de rede. Para executar diagnóstico ou render sob proibição de rede, use contenção técnica já validada e registre as tentativas; DNS indisponível não é contenção.
- Leia configuração, perfis, `_metadata.yml`, o YAML do documento, extensões e manifests pertinentes. Use `quarto inspect <alvo>` quando disponível para conferir a configuração e o engine efetivos; inspeção não comprova renderização.
- Confira qual interpretador e kernel executam as células: veja [engines e execução](references/engines.md). Procure nesta ordem: `QUARTO_PYTHON` no ambiente, `jupyter:` ou kernelspec no YAML, um ambiente virtual do projeto e o `python3` do PATH; com execução autorizada, `quarto check jupyter` mostra o que o Quarto encontra; sob proibição de rede, rode-o só com a contenção do inventário offline. `uv run quarto render` não prova sozinho qual Python rodou.
- Antes de executar, examine células, filtros e scripts de pré e pós-render. Render e preview podem executar código, escrever caches e acessar a rede. Preserve as fontes brutas e as alterações do usuário, e use ambiente e destino controlados no escopo autorizado.
- Pergunte só se faltar formato, requisito ou autorização indispensável. HTML não exige PDF adicional, e corrigir sintaxe não autoriza migrar ambiente, instalar hooks ou publicar.

## Depuração

1. Reproduza no menor alvo seguro e identifique a etapa que falha: configuração, código e engine, Pandoc e filtros, compilador ou assets. Corrija a causa e revalide o escopo afetado; não esconda erro nem apague caches só para obter sucesso.
2. Confira a configuração efetiva. `format` no documento seleciona a lista de formatos; não presuma que ele apaga as opções herdadas do formato selecionado. Cache e freeze têm escopos diferentes e não comprovam que dados externos estão atualizados.
3. Escolha o motor pelo requisito. Typst, LaTeX, HTML e RevealJS têm capacidades e dependências próprias, e um binário embutido não elimina fontes, pacotes ou downloads; veja [Typst e templates](references/typst-and-templates.md).
4. Templates e extensões acrescentam código: confira origem e revisão antes de instalar ou executar.

## Trabalhos acadêmicos

- Siga [teses e requisitos institucionais](references/abnt-thesis-guide.md): o manual da instituição e a edição da norma vêm antes do template.
- Para renderizar um PDF de tese sem rede, tudo precisa estar na máquina: a distribuição LaTeX com os pacotes do template (ou o Typst embutido no Quarto), o formato ou a extensão ABNT em `_extensions/`, as fontes, o arquivo CSL e a bibliografia. Liste o que falta a partir do YAML e do inventário offline antes de tentar o render.
- Os exemplos são pontos de partida: [tese inicial](examples/abnt-thesis-starter/README.md), [manuscrito com Binder](examples/manuscript-binder/README.md) e [HTML mínimo](examples/minimal-report/index.qmd). Copie para o destino autorizado e revise dados e manifests antes de executar. Gráficos sintéticos devem ser identificados e suas métricas calculadas.
- Margens, template e compilação não certificam ABNT, PDF/A ou prontidão para depósito. Verifique os requisitos institucionais e os próprios outputs; sem acesso ao requisito, diga o limite.
- Ao migrar um trabalho acadêmico, preserve o original e compare código, resultados, bibliografia, labels, navegação e assets no formato novo. Renomear arquivo ou converter notebook não prova equivalência.

## Verificação e manutenção

- Confira YAML, bibliografia e referências; execute só os formatos e engines necessários e inspecione os outputs pertinentes. Registre comando, versão, engine e ambiente, resultado e limitações. Separe configuração inspecionada, render executado, output inspecionado e conformidade avaliada.
- Para manter o pacote, use [scripts/doctor.py](scripts/doctor.py): `python3 <raiz-da-skill>/scripts/doctor.py --root <raiz-da-skill>`. O padrão lê o pacote; `--runtime` verifica o Quarto; `--render-smoke` renderiza HTML sem código num diretório temporário; `--quarto <executavel>` seleciona um caminho explícito. Nenhum modo valida R, Python, ABNT, PDF ou o documento do usuário.
- Sem PyYAML, o doctor relata YAML não verificado e não instala dependências. Saídas: 0 = os checks pedidos passaram; 1 = falha; 2 = check não executado sem outra falha. Render pulado nunca vira sucesso de render.
- Não instale hooks, não substitua `.git/hooks`, não altere perfil global e não apague backups automaticamente. Integração de ambiente é um procedimento separado, com alvo e efeitos explícitos.

## Integração

Use a `writing-pipeline` para revisão textual. Graphify e MCP não são requisitos: a CLI do Quarto e os verificadores locais bastam para configurar e renderizar. Devolva artefatos, evidências e pendências, sem marcar aprovação humana nem publicar como efeito da compilação.
