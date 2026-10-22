# Quarto e publicação estática

Escolha a estratégia configurada/autorizada no projeto. Idioma, formatos, cache, MECA e Binder pertencem ao contrato do documento, não ao simples rótulo A.

## Estratégias distintas

1. **Branch/pasta:** renderizar localmente, revisar e versionar os arquivos estáticos no diretório configurado, como `/docs`, e publicar pela branch/pasta escolhida. `.nojekyll` é pertinente quando esse fluxo precisa evitar processamento Jekyll. Não force push para main ou altere a configuração remota de Pages sem autorização.
2. **Publicação Quarto para gh-pages:** usar o fluxo Quarto existente que escreve na branch de publicação. O job precisa da permissão de conteúdo necessária a essa estratégia; não lhe conceda permissões extras de outro fluxo sem uso.
3. **Artifact Pages via Actions:** build produz artefato e job de deploy o consome. O deploy precisa de `pages: write`, `id-token: write`, dependência do build e ambiente apropriado; conferir configuração e proteção reais. Não confundir esse modelo com push à branch gh-pages.

Não misture as três estratégias como requisitos simultâneos. Não instale setup/workflow novo quando o projeto já possui entrega funcional, salvo mudança solicitada.

## Computação e conteúdo

Quando o runner não terá dados/ambiente para reexecutar, use outputs computacionais já gerados e revisados conforme o mecanismo Quarto. `_freeze/` é uma opção dessa estratégia, não obrigação universal: CI com dados/ambiente pode executar o estudo deliberadamente.
Valide que os outputs correspondem a código, dados e versão pretendidos, incluindo a política para dados externos alterados. Não reexecute treinamento caro só para atualizar tema sem necessidade; não declare freshness a partir de cache existente.
Revise conteúdo publicado: dados em tabelas, outputs de notebooks, gráficos e bundles podem conter informação privada. HTML final e grafo não são seguros só porque arquivos brutos ficaram fora do Git.
Compile apenas os formatos contratados. Browser headless e conversores só são pré-requisitos quando o motor/formato efetivo precisar deles; sua presença local não comprova deploy ou conteúdo remoto.

## Verificação do site

Confira output real, páginas afetadas e links/assets com parser/checker adequado. Resolva caminhos conforme URL base, subdiretório do site, percent-encoding e query/fragment, considerando `src`, `srcset` e recursos CSS/JS necessários à jornada. Regex de `<img>` no index é uma checagem parcial, não integridade completa do site.
Após publicar, confirme domínio/caminho, conteúdo da versão e assets críticos no destino. Preview e site público definitivo são estados diferentes. Se houver recuperação, restaure/republique o artefato/revisão anterior pelo mecanismo remoto aprovado e verifique o site de novo; checkout de tag local não faz isso.
