# Guia Técnico: Teses, Dissertações e TCCs segundo a ABNT NBR 14724:2024 no Quarto

Este documento estabelece as regras estruturais e tipográficas da **ABNT NBR 14724:2024** (4ª edição, dez/2024) e normas correlatas (NBR 6023, 6024, 6027, 6028, 10520) para implementação em projetos Quarto (`type: book` ou template `danielvartan/abnt`).

## 1. Ordem Estrita dos Elementos Normativos (NBR 14724:2024)

| Divisão Normativa | Elementos Constituintes (em Ordem Estrita) | Obrigatoriedade | Regras Críticas de Posicionamento e Formatação |
| :--- | :--- | :--- | :--- |
| **Parte Externa** | 1. Capa<br>2. Lombada (NBR 12225) | Capa: Obrigatório<br>Lombada: Opcional | Ordem na capa: Instituição (opcional), Autor, Título, Subtítulo (precedido de `:`), Volume (se houver), Local (cidade + UF se homónima) e Ano. Fonte 12pt. |
| **Elementos Pré-Textuais** | 1. Folha de rosto (anverso/verso)<br>2. Errata<br>3. Folha de aprovação<br>4. Dedicatória<br>5. Agradecimentos<br>6. Epígrafe<br>7. Resumo na língua vernácula (NBR 6028)<br>8. Resumo em língua estrangeira<br>9. Lista de ilustrações<br>10. Lista de tabelas<br>11. Lista de abreviaturas e siglas<br>12. Lista de símbolos<br>13. Sumário (NBR 6027) | **Obrigatórios:** Folha de rosto, Folha de aprovação, Resumo vernáculo, Resumo estrangeiro e Sumário.<br>**Demais:** Opcionais. | - **Regra de Ouro:** Agradecimentos precedem obrigatoriamente o Sumário (entre Dedicatória e Epígrafe).<br>- O **Sumário é sempre o último elemento pré-textual** e nunca lista elementos pré-textuais que o antecedem.<br>- Títulos sem indicativo numérico (Agradecimentos, Resumos, Listas, Sumário) são centralizados.<br>- Natureza do trabalho na folha de rosto usa espaço simples. |
| **Elementos Textuais** | 1. Introdução<br>2. Desenvolvimento (seções NBR 6024)<br>3. Conclusão | Todos Obrigatórios | - Papel A4 branco; margens: `top: 3cm`, `left: 3cm`, `bottom: 2cm`, `right: 2cm`.<br>- Corpo em 12pt, entrelinha 1,5, recuo de parágrafo de 1,25 cm sem linha em branco entre parágrafos.<br>- **Exceções em 10pt e espaço simples:** citações diretas > 3 linhas (recuo de 4 cm), notas de rodapé, paginação, legendas e fontes de ilustrações/tabelas. |
| **Elementos Pós-Textuais** | 1. Referências (NBR 6023)<br>2. Glossário<br>3. Apêndice (autor)<br>4. Anexo (terceiros)<br>5. Índice (NBR 6034) | **Obrigatório:** Referências.<br>**Demais:** Opcionais. | - Referências alinhadas à esquerda, em espaço simples internamente e separadas entre si por uma linha em branco (espaço simples).<br>- Apêndices e anexos identificados por letras maiúsculas, travessão e título (`APÊNDICE A – ...`). |

## 2. Implementação Prática no Quarto

### Opção 1: Conformidade Integral `abntex2` / `lualatex` (`danielvartan/abnt`)
Como o Quarto padrão ainda não expõe divisões nativas completas para `frontmatter`, `annexes` e `backmatter` (Quarto Issue #2908), utilize o template `danielvartan/abnt` (baseado em `abntex2`/`memoir`, `biblatex` e `lualatex`):
```bash
/usr/bin/git clone https://github.com/danielvartan/abnt.git meu-tcc-abnt
cd meu-tcc-abnt
/usr/bin/Rscript -e "if (!requireNamespace('renv')) install.packages('renv'); renv::restore()"
/opt/quarto/bin/quarto render
```
- **Requisitos:** TinyTeX (`quarto install tinytex`), `lualatex` e fontes *Noto Sans* e *Noto Sans Mono* instaladas no sistema.

### Opção 2: Projeto `type: book` com Typst Rápido
Para dissertações/relatórios que exigem geometria ABNT (A4, margens 3cm/2cm e CSL ABNT) sem a sobrecarga do LaTeX, configure `format: typst` no `_quarto.yml` com `papersize: a4`, `margin: {top: 3cm, left: 3cm, bottom: 2cm, right: 2cm}` e `csl: abnt.csl` (ou o template `m-aucejo/bookly-typst`).
