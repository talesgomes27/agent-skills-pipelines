# A: dados, análise e publicação

Use o tipo de estudo, dados, stack e formatos aprovados. Analytics descritivo não exige estimador, SHAP ou resíduos de regressão; Python, R, `.ipynb` e `.qmd` são escolhas do contrato.

## Gate 1: núcleo testável

Separe transformação reutilizável de apresentação quando isso ajudar os testes. Preserve esquemas, unidades, chaves e tratamento de nulos/outliers aprovado. Não crie wrappers sem propósito; mantenha estruturas nativas que garantam contratos, inclusive `sklearn.pipeline.Pipeline` e transformers quando necessários à validação.

## Gate 2: execução e rigor analítico

- Preserve fontes brutas e a política de acesso. Identifique versão/snapshot dos dados, ambiente, parâmetros e orçamento computacional. Use amostra somente quando apropriada e registre sua cobertura.
- Execute notebook em kernel limpo ou documento no motor configurado; não dependa da ordem interativa de células. Para execução de `.ipynb`, nbclient ou nbconvert são opções se disponíveis. Um `.qmd` executável não exige notebook adicional.
- Para ML, mantenha split temporal/por grupo quando o problema exigir, baseline, métrica e protocolo aprovados. Ajuste imputação, seleção, escala e estimadores apenas no treino de cada fold; teste não participa da seleção. Não troque modelos sem decisão registrada.
- Controle aleatoriedade e registre limites de determinismo, versões e backend; seed isolada não prova reprodução idêntica.
- Preserve verificação de pressupostos e diagnóstico adequados ao método. Use SHAP, resíduos ou outra explicabilidade somente quando responderem a uma questão do estudo.
- Contratos podem ser verificados por código, SQL ou biblioteca apropriada existente. Pandera/Patito não são instalações obrigatórias para toda análise.

## Gate 3: visualizações

Use a biblioteca aprovada e confira valores, unidades, ordenação, legenda e consistência narrativa. Não substitua Seaborn/Plotly exigidos por outra biblioteca devido à ausência de uma skill.
Exportações raster de publicação usam resolução prevista, frequentemente 300 DPI; formatos vetoriais seguem o destino. DPI não é critério universal de gráfico interativo. Aspecto, grid e bordas dependem do tipo de figura, sem impor eixo quadrado a toda curva.
Confira texto alternativo, contraste e legibilidade. Salve em `reports/figures/` se esse for o contrato; não versione dados ou saídas sensíveis automaticamente.

## Gates 4 e 5: relatório e reprodução

Estruture o relatório conforme perguntas, evidências e decisões aprovadas; use CRISP-ML(Q), IMRAD ou outro formato solicitado sem inserir etapas de ML que não se apliquem. Idioma e destino de publicação vêm do projeto.
Para Quarto, use configuração e sintaxe suportadas pelo formato; quando necessário, consulte `quarto-expert` pela descoberta do host, sem depender de paths de outra instalação. Para diagramas executáveis em `.qmd`, use `{mermaid}`/`{dot}` e as opções do motor, labels e legendas quando houver referências cruzadas.
`quarto check` diagnostica ambiente; o aceite exige renderizar os formatos solicitados e inspecionar os outputs. Um projeto HTML não exige PDF adicional.
Use o Python/kernel correto, explicitando `QUARTO_PYTHON` ou configuração equivalente quando necessário. `uv run quarto render` não demonstra sozinho qual kernel executou as células.
`execute: freeze: auto` evita parte das reexecuções globais, mas não detecta toda mudança em dados externos. Confira proveniência dos resultados; faça uma execução controlada quando dados/ambiente/código afetado exigirem, sem apagar caches ou disparar treinamento caro indiscriminadamente. Cache não substitui evidência de atualização.
Relacione números e conclusões às saídas verificadas; registre resultados parciais e limitações. Não remova notebooks ou experimentos válidos sob o rótulo de saneamento sem verificar seu papel.
