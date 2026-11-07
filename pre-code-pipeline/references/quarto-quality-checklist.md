# Checklist de Qualidade: Relatórios Quarto & Data Storytelling (v2.1)

Consulte esta checklist nos Gates 3 e 4 e na revisão final quando houver Quarto no projeto do **Arquétipo A (Data Science, Analytics & ML)**. Aplique os itens pertinentes ao idioma, gênero, análise e formatos aprovados. Requisitos institucionais, contratos, acessibilidade e verificações técnicas necessárias continuam obrigatórios; não acrescente seções, modelos, figuras ou configurações apenas para cumprir um exemplo.

## 1. Configuração de Documento e Metadados (`_quarto.yml`)
- **Idioma:** Defina `lang` conforme o idioma do projeto; use `lang: pt-BR` quando português brasileiro for requerido, preservando traduções e rótulos aplicáveis.
- **Prevenção de Numeração Duplicada:** Quando `number-sections: true` estiver ativo no `_quarto.yml`, **NUNCA** escreva números manualmente nos cabeçalhos Markdown do arquivo `.qmd` (escreva `## Contexto de Negócio e Hipóteses` em vez de `## 1. Contexto de Negócio e Hipóteses`).
- **Estética e Navegação:** Preserve o tema e escolha navegação conforme o formato e os requisitos. Temas `cosmo`/`zephyr`, CSS, sumário, rolagem, code folding e banner são opções quando necessários e compatíveis, não uma configuração obrigatória.
- **Destaques Visuais:** Use *Callout Blocks* (`.callout-note`, `.callout-tip`, `.callout-important`) quando ajudarem a destacar resultados e recomendações sustentados pela análise.

## 2. Consistência Metodológica e Rastreabilidade (CRISP-ML(Q) + Storytelling)
- **Exemplo de 6 Seções, somente quando essa estrutura for requerida pelo projeto:**
  1. **Seção 1 — Contexto de Negócio & Hipóteses (*Business Understanding / Ask*):** Problema central, impacto esperado, hipóteses formais e definição matemática da métrica-alvo.
  2. **Seção 2 — Auditoria de Dados & Contratos (*Data Understanding / Prepare*):** Volumetria, tipagem, integridade e blindagem contra *Data Leakage*.
  3. **Seção 3 — Análise Exploratória & Engenharia de Atributos (*Data Prep & EDA / Process*):** Evidências e transformações pertinentes, com resolução de figuras adequada ao destino.
  4. **Seção 4 — Modelagem Estatística & Machine Learning (*Modeling / Construct*):** Esquema de validação (*Out-of-Time* / K-Fold Estratificado) e tabela multi-métrica (*Baseline* vs. Modelos Candidatos).
  5. **Seção 5 — Avaliação, Diagnóstico & Explicabilidade (*Evaluation / Share*):** Importância por `gain`, SHAP/resíduos, matriz de custo e resposta 1:1 às hipóteses da Seção 1.
  6. **Seção 6 — Recomendações Executivas & Plano de Ação (*Deployment / Act*):** Tradução das métricas em decisões acionáveis e limitações do estudo.
- **Perguntas e Evidências:** Relacione cada questão central às evidências que a respondem. Inclua visualização ou resposta quantitativa quando a pergunta e o contrato as exigirem; não crie um gráfico por obrigação de correspondência 1:1.
- **Modelagem e Métricas:** Inclua modelagem somente quando prevista no projeto. Nesse caso, justifique a métrica primária pelo objetivo, pelos dados e pelo contrato; apresente comparação multi-métrica quando exigida pela avaliação.
- **Alinhamento entre Gráfico e Narrativa (Feature Importance):** Quando apresentar importância de atributos, use a medida pertinente à análise e suportada pelo modelo. Inspecione significado, valores e ordenação antes de redigir o texto.

## 3. Padrão de Publicação para Figuras (Matplotlib / Seaborn / Plotly)
- **Subfiguras Lado a Lado:** Quando houver gráficos comparáveis lado a lado, um painel com `constrained_layout=True` pode facilitar o alinhamento. Escolha proporções conforme dados e legibilidade; `ax.set_box_aspect(1)` só se a caixa quadrada for apropriada.
- **Limpeza Visual:** Escolha bordas, grid e resolução conforme legibilidade e destino. Use `dpi=300` quando requerido para exportação raster; formatos vetoriais e gráficos interativos seguem seus próprios requisitos. Preserve contraste e texto alternativo.
- **Densidade Informacional:** Use rótulos, linhas de referência e anotações quando ajudarem a interpretar os resultados, sem sobrecarregar a figura ou sugerir precisão não sustentada.

## 4. Reprodutibilidade, Execução e Publicação
- **Cache de Execução (`freeze`):** Quando houver execução custosa, escolha cache/freeze conforme a política do projeto e confira atualização dos resultados. Configuração de cache não substitui evidência de atualidade ou de execução.
- **Determinismo e Sementes Aleatórias:** Quando houver aleatoriedade, fixe `random_state` / `seed` conforme o protocolo e registre ambiente e limites de determinismo. Confira os números citados contra tabelas e figuras efetivamente geradas.
- **Diretório de Saída e Artefatos:** Use o destino e a política de retenção/versionamento aprovados. Para GitHub Pages, `output-dir: docs` ou workflow dedicado são opções; outros destinos não exigem essa configuração. Salve figuras em `reports/figures/` se esse for o contrato, sem versionar dados ou saídas sensíveis automaticamente.

## 5. Diagramas e Grafos de Arquitetura (Mermaid / Graphviz)
- [ ] **Executable Cells:** Para diagramas executáveis no Quarto, Mermaid usa ` ```{mermaid} ` e Graphviz usa ` ```{dot} `. Exemplos literais podem usar code blocks sem chaves.
- [ ] **Extensão do Arquivo:** Use `.qmd` quando o diagrama precisar ser executado pelo Quarto; exemplos literais não exigem conversão de `.md`.
- [ ] **Cell Options Canônicas:** Opções declaradas imediatamente após a abertura da célula, usando `%%|` para Mermaid e `//|` para dot (ex: `%%| label: fig-fluxo`, `%%| fig-cap: "..."`).
- [ ] **Cross-References:** Quando houver referências cruzadas, use `label: fig-*`, `fig-cap: "..."` e `@fig-*`. Preserve legendas e descrições necessárias à acessibilidade.
- [ ] **Formatos de Saída:** Verifique a renderização nos formatos solicitados e os recursos necessários de cada motor. Não exija PDF para projeto HTML nem force SVG em PDF sem conferir o suporte de conversão.
- [ ] **Arquivos Externos:** Se o diagrama estiver em arquivo `.mmd` ou `.dot` separado, incluir via `file: caminho/arquivo.mmd` nas cell options em vez de copiar inline.
