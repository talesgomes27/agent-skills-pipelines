# Exemplo: Manuscrito Cientifico com MECA + Binder

Regra critica: `quarto use binder` NAO inspeciona arquivos `.qmd` em busca
de imports. Exige manifesto na raiz:

- Python: `requirements.txt` ou `environment.yml`
- R: `renv.lock` ou `install.R`

Rode `quarto use binder` APOS criar `requirements.txt`.
