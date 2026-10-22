# Engines e execução

Confira versão, células, metadados e configuração efetiva com `quarto inspect` quando disponível. Não deduza engine apenas da extensão nem imponha um kernel pessoal.

knitr, Jupyter, Julia e Observable têm capacidades e opções diferentes. Use o engine configurado e suportado pela versão; em caso de documento misto, confira a seleção efetiva em vez de assumir que basta a primeira célula. Extensões de engine adicionam código e exigem revisão de origem/compatibilidade.

## Cache e freeze

A integração Jupyter Cache armazena execução do notebook/documento; não é cache independente de chunks como no knitr. Configure o escopo apropriado e confirme requisitos no ambiente. `freeze` controla reutilização em renderizações de projeto, sem comprovar freshness de dados externos.

## Inline e ambiente

Quarto oferece expressões inline como `{python}` e `{r}` nas versões que as suportam. Limite-as a valores já calculados e confira restrições de YAML/notebooks. Não afirme ausência de inline Python sem verificar a versão.

Confirme interpreter e kernel efetivos. `QUARTO_PYTHON` pode selecionar Python; kernelspec, ambiente e opções Jupyter também importam. `uv run` não prova sozinho qual kernel executou as células.

## Evidência

Versão, diagnóstico de componentes, inspect e render são verificações distintas. Não exija R para HTML estático ou Jupyter para knitr. Renderize só o necessário, em ambiente autorizado, e registre as limitações.

Fontes: [cache](https://quarto.org/docs/computations/caching.html), [inline](https://quarto.org/docs/computations/inline-code.html), [Python](https://quarto.org/docs/computations/python.html), [R](https://quarto.org/docs/computations/r.html).
