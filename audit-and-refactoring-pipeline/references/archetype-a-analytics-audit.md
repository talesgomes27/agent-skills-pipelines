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
- [ ] **Fidelidade Numérica:** Cada métrica citada no texto do `.qmd` ou `README.md` coincide exatamente com a saída real das tabelas/modelos?
- [ ] **Importância de Variáveis (`gain` vs. `split`):** Gráficos de modelos de árvore usam `importance_type='gain'` e a hierarquia descrita no texto reflete exatamente a ordem visual das barras?
- [ ] **Rastreabilidade 1:1 (*Ask ➔ Share*):** Todas as perguntas de negócio ou hipóteses listadas na abertura possuem visualização e resposta direta na seção de resultados?
- [ ] **Padrão Visual e Editorial Quarto:** `lang: pt-BR` ativo, zero numeração manual duplicada nos títulos (`number-sections: true`), subfiguras lado a lado niveladas (`ax.set_box_aspect(1)`), `sns.despine()` e `dpi=300`.
