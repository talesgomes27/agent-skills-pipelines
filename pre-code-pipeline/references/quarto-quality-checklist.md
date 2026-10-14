# Checklist de Qualidade: Relatórios Quarto & Data Storytelling (v2.1)

Este documento define os padrões obrigatórios para projetos do **Arquétipo A (Data Science, Analytics & ML)** que utilizam Python/R e Quarto (`.qmd` / `_quarto.yml`). Deve ser consultado obrigatoriamente no **Gate 3**, no **Gate 4** e na revisão final antes da publicação.

## 1. Configuração de Documento e Metadados (`_quarto.yml`)
- **Idioma Nativo:** Sempre defina `lang: pt-BR` no `_quarto.yml` para garantir que rótulos automáticos (`Autor`, `Publicado`, datas e `Figura`) sejam renderizados em português.
- **Prevenção de Numeração Duplicada:** Quando `number-sections: true` estiver ativo no `_quarto.yml`, **NUNCA** escreva números manualmente nos cabeçalhos Markdown do arquivo `.qmd` (escreva `## Ask (Pergunta de Negócio)` em vez de `## 1. Ask (Pergunta de Negócio)`).
- **Estética e Navegação:** Utilize temas limpos (`cosmo` ou `zephyr` com folha de estilo `.scss`/`.css` customizada), `toc: true`, `toc-depth: 3`, `smooth-scroll: true`, `code-fold: true` e `title-block-banner: true`.
- **Destaques Visuais:** Utilize *Callout Blocks* (`.callout-note`, `.callout-tip`, `.callout-important`) para destacar hipóteses validadas, métricas campeãs e recomendações executivas da fase *Act*.

## 2. Consistência Metodológica e Rastreabilidade (Ask ➔ Analyze ➔ Share)
- **Mapeamento 1:1 de Perguntas e Gráficos:** Toda questão central ou hipótese formulada na fase **Ask (Seção 1)** deve obrigatoriamente possuir uma visualização direta e uma resposta quantitativa na fase **Share**.
- **Justificativa da Métrica Alvo:** A escolha da métrica primária (ex: RMSLE vs. RMSE vs. MAE vs. F1/AUC) deve ser justificada matematicamente com base na distribuição da variável *target* (ex: assimetria e cauda longa). Sempre apresente uma tabela comparativa multi-métrica entre os modelos avaliados.
- **Alinhamento entre Gráfico e Narrativa (Feature Importance):** Em modelos baseados em árvores (LightGBM, XGBoost, Random Forest), priorize `importance_type='gain'` (ganho real de redução de erro) sobre `split`. Inspecione os valores exatos gerados antes de redigir o texto para nunca contradizer a ordem exibida na figura.

## 3. Padrão de Publicação para Figuras (Matplotlib / Seaborn / Plotly)
- **Nivelamento de Subfiguras Lado a Lado:** Ao exibir dois gráficos lado a lado `(a)` e `(b)`, gere-os preferencialmente em um único painel `fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), constrained_layout=True)` aplicando `ax.set_box_aspect(1)` em ambos os eixos. Jamais misture proporções de caixa diferentes que deixem um gráfico mais achatado que o outro.
- **Limpeza Visual:** Aplique `sns.despine()` (remova bordas superior e direita), utilize grid sutil (`alpha=0.25`, `linestyle='--'`) e exporte sempre com `dpi=300` (ou formato vetorial SVG).
- **Densidade Informacional:** Adicione rótulos de dados diretos nas barras/pontos principais, linhas de referência (ex: erro zero ou meta do PRD) e anotações de variação percentual quando as diferenças absolutas parecerem visualmente pequenas.

## 4. Reprodutibilidade, Execução e Publicação (GitHub Pages)
- **Cache de Execução (`freeze`):** Configure `execute: freeze: auto` no `_quarto.yml` para evitar que treinamentos pesados de Machine Learning sejam reexecutados desnecessariamente durante ajustes estéticos ou builds de CI/CD.
- **Determinismo e Sementes Aleatórias:** Fixe `random_state` / `seed` globalmente em todas as amostragens, divisões de validação e modelos para garantir que os números citados no texto nunca divirjam das tabelas e figuras re-renderizadas.
- **Diretório de Saída e Artefatos:** Padronize a publicação para GitHub Pages (`output-dir: docs` na raiz ou workflow dedicado no GitHub Actions) e garanta que figuras geradas por scripts externos sejam salvas em diretório versionado (ex: `reports/figures/`) antes de executar `quarto render`.
