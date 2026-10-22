# Auditoria analítica orientada ao estudo

Leia somente as partes aplicáveis ao escopo: analytics, ML, pesquisa ou publicação. Ausência de um modelo ou SHAP não é defeito em análise descritiva.

## Dados e método

- Identifique pergunta, fontes, recortes, unidades, chaves, nulos e regras de transformação. Confira proveniência e acesso sem copiar dados privados ao parecer.
- Para ML, verifique instante de previsão, split temporal/por entidade e informação disponível em cada etapa. Examine imputação, seleção e transformação ajustadas dentro do treino/fold. Não exclua automaticamente uma coluna só por ser target de outra tarefa: avalie disponibilidade e contrato de previsão.
- Confira baseline, métrica e avaliação quando necessários à pergunta. Não selecione PR-AUC, F1 ou RMSLE apenas pelo rótulo do dataset; registre o objetivo e suas restrições.
- Diferencie associação, capacidade preditiva e efeito causal. Estilo de relatório não substitui desenho do estudo e validade do método.

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
