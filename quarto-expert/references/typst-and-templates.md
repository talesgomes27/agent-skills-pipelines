# Guia Avançado: Motor Typst, Geometria Marginalia e Templates Académicos

## 1. Parametrização Declarativa do Motor Typst (`format: typst`)
O Typst vem embutido nativamente no Quarto CLI e compila PDFs instantaneamente sem depender do LaTeX:
```yaml
format:
  typst:
    papersize: a4 # ou us-letter, a5, jis-b5
    margin:
      top: 3cm
      bottom: 2.5cm # aumente se page-numbering estiver ativo, pois o número fica na margem inferior
      left: 3cm
      right: 2cm
    toc: true
    number-sections: true
    page-numbering: "1 / 1"
    columns: 1
```

## 2. Layout Tufte / Notas de Margem (Pacote `marginalia`)
Quando o documento utiliza classes fora da coluna principal (`.column-margin` ou `.column-page`), o Quarto ativa automaticamente o pacote Typst `marginalia`, dividindo as margens esquerda (`inner`) e direita (`outer`) em três zonas controladas por `margin-geometry`:
- `far`: margem extrema até à borda do papel.
- `width`: largura reservada para a coluna de notas de margem.
- `separation`: distância entre o corpo do texto e a coluna de margem.

A largura útil do corpo de texto (`.column-body`) é dada por:
$$W_{\text{body}} = W_{\text{paper}} - (\text{inner.far} + \text{inner.width} + \text{inner.separation} + \text{outer.far} + \text{outer.width} + \text{outer.separation})$$

> **Restrição Crítica:** Nunca combine `columns: 2` com classes `.column-margin` ou `.column-page` no Typst — o pacote `marginalia` conflita com fluxos de corpo multicoluna.

## 3. Cabeçalhos Correntes (*Running Headers*) em Typst
O Quarto não expõe chave YAML nativa para cabeçalhos de página no Typst. Injete um bloco bruto `=typst` no início do `.qmd`:
````markdown
```{=typst}
#set page(header: align(right)[Título Corrente do Relatório])
```
````

## 4. Catálogo de Templates e Extensões Académicas
- **Multi-Alvo Integrado (`academic-pandoc-template`):** Subprojetos `article/`, `presentation/` e `thesis/` com `_brand.yml` e separação entre `_quarto.yml` e `_metadata.yml` (`[https://github.com/maehr/academic-pandoc-template](https://github.com/maehr/academic-pandoc-template)`).
- **Livros e Teses em Typst (`bookly-typst`):** Suporta Português (`lang: "pt"`), 6 temas (`classic`, `modern`, `fancy`, `obook`, `orly`, `pretty`), `minitoc` (`suboutline`), subfiguras (`subpar`) e caixas `showybox`:
  `quarto use template m-aucejo/bookly-typst`
- **Tese Doutoral PDF/A-1b (`cnam-thesis`):** Extensão LaTeX + Lua + HTML validada para depósito arquivístico PDF/A-1b (`[https://github.com/zinc75/quarto-cnam-thesis](https://github.com/zinc75/quarto-cnam-thesis)`).
- **Apresentações Typst (`touying-typst` / `diaquarto`):** Alternativas rápidas ao Beamer sem LaTeX.
- **Execução Interativa WebAssembly (`quarto-live`):** Executa R (`webr`) e Python (`pyodide`) ao vivo em HTML e RevealJS.
