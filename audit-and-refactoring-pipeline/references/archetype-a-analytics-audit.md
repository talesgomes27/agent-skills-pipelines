# Checklist de Auditoria Analítica, Científica & Quarto (Arquétipo A)

Utilize este checklist no **Gate 2** da `audit-and-refactoring-pipeline` em conjunto com `/home/tales/.gemini/config/skills/pre-code-pipeline/references/quarto-quality-checklist.md`.

## 1. Integridade Estatística e Vazamento de Dados (*Data Leakage*)
- [ ] **Partição Temporal / Grupo:** Eventos cronológicos usam split *Out-of-Time*? Entidades repetidas (ex: `customer_id`) respeitam isolamento de grupo ou janela temporal?
- [ ] **Isolamento de Pré-processamento:** Imputações, normalizações, *target encodings* e janelas móveis são calculados sem usar informações futuras do conjunto de validação/teste?
- [ ] **Isolamento de Múltiplos Targets:** Em bases com mais de uma coluna *target*, as variáveis-alvo irmãs foram estritamente excluídas das features preditoras ($X$)?
- [ ] **Coerência de Métricas:** A métrica primária é adequada ao problema (PR-AUC / Macro-F1 para desbalanceamento severo; RMSLE / MAE para regressão com assimetria forte)?

## 2. Reprodutibilidade e Governança de Notebooks
- [ ] **Determinismo Estrito:** Sementes aleatórias (`random_state` / `seed`) estão fixadas em todos os estimadores, splits e cálculos de SHAP/permutação?
- [ ] **Execução Linear Limpa:** Notebooks `.ipynb` executam do topo ao fim sem células fora de ordem, variáveis órfãs ou warnings/logs poluindo a saída?
- [ ] **Configuração de Freeze:** `_quarto.yml` contém `execute: freeze: auto` para evitar reprocessamento acidental?

## 3. Auditoria Cruzada: Texto × Código × Figuras no Quarto
- [ ] **Aderência às 6 Seções CRISP-ML(Q) + Storytelling (P1):** O relatório está organizado nas 6 etapas canônicas (1. Contexto & Hipóteses; 2. Auditoria & Contratos; 3. EDA & Feature Engineering; 4. Modelagem & Baselines; 5. Avaliação, Diagnóstico & Explicabilidade; 6. Recomendações Executivas & Ação) ou IMRAD (se acadêmico estrito)?
- [ ] **Rastreabilidade 1:1 Hipóteses ➔ Avaliação & Ação (P1):** Todas as perguntas de negócio e hipóteses formuladas na Seção 1 possuem validação visual/quantitativa na Seção 5 e recomendação prática na Seção 6?
- [ ] **Comparação Multi-Métrica com Baseline (P1):** A Seção 4 compara formalmente um modelo Baseline simples contra os modelos candidatos usando métricas justificadas matematicamente?
- [ ] **Fidelidade Numérica:** Cada métrica citada no texto do `.qmd` ou `README.md` coincide exatamente com a saída real das tabelas/modelos?
- [ ] **Importância de Variáveis (`gain` vs. `split`):** Gráficos de modelos de árvore usam `importance_type='gain'` e a hierarquia descrita no texto reflete exatamente a ordem visual das barras?
- [ ] **Padrão Visual e Editorial Quarto:** `lang: pt-BR` ativo, zero numeração manual duplicada nos títulos (`number-sections: true`), subfiguras lado a lado niveladas (`ax.set_box_aspect(1)`), `sns.despine()` e `dpi=300`.
- [ ] **Diagramas como Executable Cells (P1):** Todo diagrama Mermaid usa ` ```{mermaid} ` e Graphviz usa ` ```{dot} `? O documento possui extensão `.qmd`?
- [ ] **Cell Options Canônicas em Diagramas (P2):** As opções `%%|` ou `//|` estão no topo da célula antes do conteúdo?
- [ ] **Cross-References em Diagramas (P2):** Diagramas possuem `label: fig-*` e `fig-cap` e são referenciados no texto via `@fig-*`?
