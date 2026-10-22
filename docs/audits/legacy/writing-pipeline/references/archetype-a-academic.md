# Arquétipo A: Convenções de Escrita

## Registro e Voz

- Acadêmico-executivo, analítico, demonstrativo.
- 3ª pessoa impessoal ("Os dados indicam...") ou 1ª plural metódico
  ("Nós calculamos...").
- Tom sóbrio, cético quanto a métricas.

## Estrutura

- **Modelo Híbrido CRISP-ML(Q) + Storytelling (Padrão para Projetos de Data Science & ML em Quarto):** Estruturar em 6 seções canônicas (*1. Contexto de Negócio & Hipóteses ➔ 2. Auditoria de Dados & Contratos ➔ 3. EDA & Engenharia de Atributos ➔ 4. Modelagem Estatística/ML ➔ 5. Avaliação, Diagnóstico & Explicabilidade ➔ 6. Recomendações Executivas & Ação*).
- **IMRAD (Padrão para Artigos Científicos e Teses/TCC):** *Introduction, Methods, Results, and Discussion*.
- Cada seção abre com o dado central, depois contextualiza.

## Citação

- **APA 7th** para autor-data.
- **ABNT NBR 10520** para PT-BR.
- **IEEE** para relatórios técnicos de engenharia.
- **Chicago** para humanidades quantitativas.
- **Vancouver/AMA** para relatórios médicos.

### Guias de Reporte

- **CONSORT** para ensaios clínicos randomizados.
- **STROBE** para estudos observacionais.
- **PRISMA** para revisões sistemáticas.

## Convenções Quarto

- `lang: pt-BR` quando o documento for em português.
- `code-fold: true`, `freeze: auto`, `toc: true`.
- Callouts: `.callout-note`, `.callout-tip`, `.callout-important`.
- Proibido numerar títulos manualmente quando `number-sections: true`.

## Comprimento de Frase

Variabilidade alta: alternar frases de 4–8 palavras com períodos de
20–30 palavras.

## Exemplos

### Introdução de Resultados
Antes: "Ao analisar os dados, é fascinante notar não apenas uma
tendência clara, mas também um salto extraordinário..."

Depois: "As vendas cresceram 18,4% no Q3, totalizando R$ 4,2 milhões
(Figura 2). O aumento decorreu da entrada de 120 novos clientes
corporativos."
