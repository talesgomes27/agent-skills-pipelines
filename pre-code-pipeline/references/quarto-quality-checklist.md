# Checklist de Qualidade: Relatórios Quarto & Data Storytelling (v2.1)

Este documento define os padrões obrigatórios para projetos do **Arquétipo A (Data Science, Analytics & ML)** que utilizam Python/R e Quarto (`.qmd` / `_quarto.yml`). Deve ser consultado obrigatoriamente no **Gate 3**, no **Gate 4** e na revisão final antes da publicação.

## 1. Configuração de Documento e Metadados (`_quarto.yml`)
- **Idioma Nativo:** Sempre defina `lang: pt-BR` no `_quarto.yml` para garantir que rótulos automáticos (`Autor`, `Publicado`, datas e `Figura`) sejam renderizados em português.
- **Prevenção de Numeração Duplicada:** Quando `number-sections: true` estiver ativo no `_quarto.yml`, **NUNCA** escreva números manualmente nos cabeçalhos Markdown do arquivo `.qmd` (escreva `## Contexto de Negócio e Hipóteses` em vez de `## 1. Contexto de Negócio e Hipóteses`).
- **Estética e Navegação:** Utilize temas limpos (`cosmo` ou `zephyr` com folha de estilo `.scss`/`.css` customizada), `toc: true`, `toc-depth: 3`, `smooth-scroll: true`, `code-fold: true` e `title-block-banner: true`.
- **Destaques Visuais:** Utilize *Callout Blocks* (`.callout-note`, `.callout-tip`, `.callout-important`) para destacar hipóteses validadas, métricas campeãs e recomendações executivas da fase *Act*.

## 2. Consistência Metodológica e Rastreabilidade (CRISP-ML(Q) + Storytelling)
- **Estrutura Canônica de 6 Seções para Relatórios `.qmd` (Arquétipo A):**
  1. **Seção 1 — Contexto de Negócio & Hipóteses (*Business Understanding / Ask*):** Problema central, impacto esperado, hipóteses formais e definição matemática da métrica-alvo.
  2. **Seção 2 — Auditoria de Dados & Contratos (*Data Understanding / Prepare*):** Volumetria, tipagem, integridade e blindagem contra *Data Leakage*.
  3. **Seção 3 — Análise Exploratória & Engenharia de Atributos (*Data Prep & EDA / Process*):** Validação visual das hipóteses (300 DPI) e transformações matemáticas.
  4. **Seção 4 — Modelagem Estatística & Machine Learning (*Modeling / Construct*):** Esquema de validação (*Out-of-Time* / K-Fold Estratificado) e tabela multi-métrica (*Baseline* vs. Modelos Candidatos).
  5. **Seção 5 — Avaliação, Diagnóstico & Explicabilidade (*Evaluation / Share*):** Importância por `gain`, SHAP/resíduos, matriz de custo e resposta 1:1 às hipóteses da Seção 1.
  6. **Seção 6 — Recomendações Executivas & Plano de Ação (*Deployment / Act*):** Tradução das métricas em decisões acionáveis e limitações do estudo.
- **Mapeamento 1:1 de Perguntas e Gráficos:** Toda questão central ou hipótese formulada na **Seção 1 (*Business Understanding / Ask*)** deve obrigatoriamente possuir uma visualização direta e uma resposta quantitativa nas seções de **EDA (*Process*)** ou **Avaliação (*Evaluation / Share*)**.
- **Justificativa da Métrica Alvo:** A escolha da métrica primária (ex: RMSLE vs. RMSE vs. MAE vs. F1/PR-AUC) deve ser justificada matematicamente com base na distribuição da variável *target* (ex: assimetria e cauda longa). Sempre apresente uma tabela comparativa multi-métrica entre os modelos avaliados.
- **Alinhamento entre Gráfico e Narrativa (Feature Importance):** Em modelos baseados em árvores (LightGBM, XGBoost, Random Forest), priorize `importance_type='gain'` (ganho real de redução de erro) sobre `split`. Inspecione os valores exatos gerados antes de redigir o texto para nunca contradizer a ordem exibida na figura.

## 3. Padrão de Publicação para Figuras (Matplotlib / Seaborn / Plotly)
- **Nivelamento de Subfiguras Lado a Lado:** Ao exibir dois gráficos lado a lado `(a)` e `(b)`, gere-os preferencialmente em um único painel `fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), constrained_layout=True)` aplicando `ax.set_box_aspect(1)` em ambos os eixos. Jamais misture proporções de caixa diferentes que deixem um gráfico mais achatado que o outro.
- **Limpeza Visual:** Aplique `sns.despine()` (remova bordas superior e direita), utilize grid sutil (`alpha=0.25`, `linestyle='--'`) e exporte sempre com `dpi=300` (ou formato vetorial SVG).
- **Densidade Informacional:** Adicione rótulos de dados diretos nas barras/pontos principais, linhas de referência (ex: erro zero ou meta do PRD) e anotações de variação percentual quando as diferenças absolutas parecerem visualmente pequenas.

## 4. Reprodutibilidade, Execução e Publicação (GitHub Pages)
- **Cache de Execução (`freeze`):** Configure `execute: freeze: auto` no `_quarto.yml` para evitar que treinamentos pesados de Machine Learning sejam reexecutados desnecessariamente durante ajustes estéticos ou builds de CI/CD.
- **Determinismo e Sementes Aleatórias:** Fixe `random_state` / `seed` globalmente em todas as amostragens, divisões de validação e modelos para garantir que os números citados no texto nunca divirjam das tabelas e figuras re-renderizadas.
- **Diretório de Saída e Artefatos:** Padronize a publicação para GitHub Pages (`output-dir: docs` na raiz ou workflow dedicado no GitHub Actions) e garanta que figuras geradas por scripts externos sejam salvas em diretório versionado (ex: `reports/figures/`) antes de executar `quarto render`.

## 5. Diagramas e Grafos de Arquitetura (Mermaid / Graphviz)
- [ ] **Executable Cells:** Todos os diagramas Mermaid usam ` ```{mermaid} ` e Graphviz usam ` ```{dot} ` (NUNCA code blocks sem chaves ` ```mermaid ` ou ` ```dot `).
- [ ] **Extensão do Arquivo:** Arquivos que contêm diagramas executáveis DEVEM ter extensão `.qmd` (o Quarto não executa células de código em `.md`).
- [ ] **Cell Options Canônicas:** Opções declaradas imediatamente após a abertura da célula, usando `%%|` para Mermaid e `//|` para dot (ex: `%%| label: fig-fluxo`, `%%| fig-cap: "..."`).
- [ ] **Cross-References:** Todos os diagramas possuem `label: fig-*` e `fig-cap: "..."` e são referenciados no texto via `@fig-*`.
- [ ] **Formatos de Saída:** HTML usa renderização nativa (JS); PDF/print usa PNG gerado pelo Quarto (via `chrome-headless-shell`). Não forçar `mermaid-format: svg` em PDF sem verificar `rsvg-convert` no PATH.
- [ ] **Arquivos Externos:** Se o diagrama estiver em arquivo `.mmd` ou `.dot` separado, incluir via `file: caminho/arquivo.mmd` nas cell options em vez de copiar inline.
