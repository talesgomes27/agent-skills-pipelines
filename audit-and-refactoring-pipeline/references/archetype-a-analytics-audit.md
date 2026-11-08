# Auditoria analítica orientada ao estudo

Leia somente as partes aplicáveis ao escopo: analytics, ML, pesquisa ou publicação. Ausência de um modelo ou SHAP não é defeito em análise descritiva.

## Dados e método

- Identifique pergunta, fontes, recortes, unidades, chaves, nulos e regras de transformação. Confira proveniência e acesso sem copiar dados privados ao parecer; dados pessoais já gravados em saídas de notebook, logs ou exportações são achado, e a skill `personal-data` traz as regras.
- Para ML, verifique instante de previsão, split temporal/por entidade e informação disponível em cada etapa. Examine imputação, seleção e transformação ajustadas dentro do treino/fold. Não exclua automaticamente uma coluna só por ser target de outra tarefa: avalie disponibilidade e contrato de previsão.
- Confira baseline, métrica e avaliação quando necessários à pergunta. Não selecione PR-AUC, F1 ou RMSLE apenas pelo rótulo do dataset; registre o objetivo e suas restrições.
- Modelo que pontua, classifica ou ordena pessoas sem métricas por grupo, ou com diferença entre grupos acima do limite combinado, é achado; a referência de viés de modelo da skill `personal-data` diz o que medir.
- Diferencie associação, capacidade preditiva e efeito causal. Estilo de relatório não substitui desenho do estudo e validade do método.

## Experimentos e testes A/B

- Antes de comparar as variantes, confira a divisão observada contra a planejada, pela unidade do sorteio (usuário, sessão). A Microsoft ExP usa o qui-quadrado com p < 0,0005 como alarme de sample ratio mismatch (SRM); com SRM, o resultado não vale até a causa ser achada.
- Confira se o teste cumpriu a duração e o tamanho de amostra do plano. Parar quando uma variante "está ganhando" aumenta o falso positivo; resultado de teste parado antes é achado.
- Relate a diferença da métrica principal do plano com intervalo de confiança e o teste usado, não só o p-valor, e diga se a conclusão se sustenta com as ressalvas acima. Métrica trocada depois do resultado é achado.

Fonte, conferida em 08/11/2026: Microsoft ExP, "Diagnosing Sample Ratio Mismatch in A/B Testing", https://www.microsoft.com/en-us/research/group/experimentation-platform-exp/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/

## Reprodução e execução

- Registre ambiente, dados, parâmetros, sementes e limites de determinismo. Seed sozinha não prova reprodução bit a bit.
- Confira execução limpa de notebook/documento em ambiente seguro quando autorizada, sem tornar todo warning um defeito ou limpar saída para esconder erro.
- Examine cache/freeze e origem dos resultados. Alteração de dados externos pode exigir nova execução mesmo sem mudança no `.qmd`; não imponha `freeze: auto` como requisito universal.

## Texto, figuras e publicação

- Confronte métricas e conclusões com tabelas/saídas do mesmo recorte e versão. Use arredondamento/unidade documentados, sem exigir igualdade textual entre número formatado e valor completo.
- Confira método de importância/explicabilidade que o estimador suporta e sua interpretação; `gain` não é uma API universal de todos os modelos de árvore.
- Avalie legibilidade, escalas, acessibilidade e resolução de exportação conforme o destino. Não force eixos quadrados, idioma pt-BR ou 300 DPI em todo gráfico interativo.
- Valide bibliografia, referências cruzadas, opções e formatos Quarto contratados. Preserve exemplos literais de sintaxe e diferencie Markdown comum de células executáveis `.qmd`.
- Estrutura CRISP-ML(Q), IMRAD ou outra é a exigida pelo documento, não uma severidade automática. Consulte especialistas apenas para a questão técnica efetivamente encontrada.

Uma auditoria pode registrar limite metodológico sem refazer o estudo. Refazer split, estimador ou métrica exige decisão explícita e comparação dos resultados sob o novo contrato.
