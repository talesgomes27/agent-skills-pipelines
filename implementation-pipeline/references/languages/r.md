# R

Leia quando o componente da tarefa é escrito em R (script, pacote, Quarto ou Shiny).

A Posit mantém skills oficiais em https://github.com/posit-dev/skills, como `r-testthat` e `r-package-development`. Quando instaladas, use-as para escrever testes e pacotes; esta referência não repete o conteúdo delas.

## Descubra no projeto

- Versão e dependências: `DESCRIPTION` (`Imports`, `Suggests` e a versão mínima do R em `Depends: R (>= ...)`) e `renv.lock`.
- Ambiente: com `renv`, a biblioteca é do projeto (`renv/library`) e o `.Rprofile` a ativa ao abrir o R na pasta. `renv::restore()` instala as versões do lock já aceito. Instalar pacote novo, mudar versão ou regravar o lock com `renv::snapshot()` é instalar dependência, um efeito do catálogo do contrato comum, e pede A2 com o pacote, a versão e onde instala.
- Comandos: `Makefile`, scripts do projeto e o workflow de CI.

Use os comandos do projeto e a biblioteca do `renv` quando ele existe. Não instale pacote na biblioteca do usuário nem do sistema.

## Testes e checks

Exemplos a confirmar no projeto:

- Testes com testthat ficam em `tests/testthat/`, em arquivos que começam com `test`. `devtools::test()` roda a suíte e `testthat::test_file()` roda um arquivo.
- `R CMD check` ou `devtools::check()` rodam os testes pelo `tests/testthat.R`, além das checagens do pacote.
- `lintr::lint_package()` num pacote e `lintr::lint_dir()` num projeto.

## Armadilhas

- Fatores em versões antigas: antes do R 4.0.0, `data.frame()` e `read.table()` convertiam texto em fator por padrão. Código ou dados de um projeto antigo podem depender disso.
- Fator para número: `as.numeric(f)` devolve os códigos internos, não os valores. Use `as.numeric(as.character(f))`.
- `NA` em comparações: `x == NA` dá `NA` em todas as posições. Use `is.na(x)` e confira os `NA` antes de filtrar ou somar.
- Pacote sem `renv`: a análise roda com as versões que estiverem instaladas e muda de resultado em outra máquina. Num projeto com `renv`, não carregue pacote fora do lock.
- Caminho absoluto ou `setwd()` no script: roda só na máquina do autor. Use caminhos relativos à raiz do projeto.

## Fontes

Conferido em 08/11/2026:

- https://github.com/posit-dev/skills
- https://rstudio.github.io/renv/articles/renv.html
- https://r-pkgs.org/description.html e https://r-pkgs.org/testing-basics.html
- https://testthat.r-lib.org/
- https://lintr.r-lib.org/
- https://cran.r-project.org/doc/manuals/r-release/NEWS.pdf (R 4.0.0, `stringsAsFactors = FALSE`)
- https://cran.r-project.org/doc/FAQ/R-FAQ.html (FAQ 7.10)
- https://cran.r-project.org/doc/manuals/r-release/R-intro.html (valores ausentes)
