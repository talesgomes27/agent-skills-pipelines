# Exemplo: TCC / Dissertacao ABNT NBR 14724:2024

Configuracao minima de um projeto `type: book` usando **Typst** para
compilacao rapida em PDF com geometria ABNT.

Para conformidade integral com `abntex2` (folha de aprovacao, errata,
lombada, PDF/A), prefira o template `danielvartan/abnt`:

    git clone https://github.com/danielvartan/abnt.git meu-tcc
    cd meu-tcc && quarto render

Os arquivos `01-introducao.qmd` a `references.qmd` sao stubs para garantir
que `quarto render` funcione sem erros.
