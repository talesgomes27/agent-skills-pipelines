# Convenções por tipo de documento

Leia apenas a seção do artefato solicitado. Arquétipo do projeto ajuda no contexto, mas não determina sozinho pessoa gramatical, estrutura, idioma ou norma. Preserve requisitos editoriais declarados.

## PRD, especificação e plano

Distinga problema observado, objetivo futuro, requisito, critério de aceite e decisão. Métricas desejadas ficam identificadas como metas, nunca como resultados alcançados. Preserve non-goals, restrições e questões abertas. Use os nomes e contratos de arquivos da pipeline chamadora, sem criar um segundo plano.
Na spec viva (`docs/spec.md`), redija cada requisito com ID, enunciado, critério verificável e estado, sem promover critério a resultado alcançado; na revisão, preserve os IDs e o caráter futuro dos critérios. Num formato de SDD do projeto, siga as convenções dele.

## ADR

Registre contexto, decisão, alternativas consideradas e consequências. Descreva razões e trade-offs verificáveis; evite preencher o documento com princípios genéricos. Preserve o status real da decisão: proposta, aprovada ou substituída conforme a convenção do projeto.

## README, API e docstring

Priorize o que o software faz, pré-requisitos, setup, exemplo e contratos de erro relevantes. Não prometa setup em cinco minutos sem medição. Documente variáveis e flags reais, sem segredos; não acrescente exemplos incompatíveis com a versão do projeto.
Use o formato de docstring existente; Google Style não é universal. Documente unidades, efeitos, restrições e exceções que não sejam óbvios na assinatura. Não reescreva toda a API para corrigir uma função.

## CLI, manpage e mensagem de erro

Mostre ação, sintaxe e consequência. Erros devem ajudar a identificar e corrigir a falha; não invente uma mensagem como se fosse exigência universal de POSIX. Preserve stdout/stderr, nomes de flags e códigos de saída documentados. Prosa explicativa e links para padrões são válidos quando necessários ao leitor.

## Relatório analítico, acadêmico ou executivo

Estruture por pergunta, método, evidência, limitações e decisão. IMRAD, CRISP-ML(Q) e guias de reporte são escolhas do tipo de estudo e do destinatário; não acrescente modelagem a analytics descritivo. Não transforme associação em causalidade durante a edição.
Norma de citação e formatação vem do requisito institucional/editorial, não apenas do idioma. Preserve a voz e pessoa gramatical apropriadas. Não invente conteúdo de norma não consultada.
Em Quarto, preserve bibliografia e estilo configurados. Diagramas renderizáveis em `.qmd` usam células do motor correspondente; exemplos literais de sintaxe e Markdown comum podem usar code fences. Verifique somente os formatos solicitados. Não presuma um formato de imagem ou interatividade igual em HTML, PDF e Typst.

### Relatório executivo

Para diretoria ou gestão, a partir de uma análise ou de um modelo:

- Pergunte no início o formato (docx, PDF, Quarto, slides) e o tamanho. Para docx, PDF ou pptx, use as skills de documentos da Anthropic (`document-skills`) quando estiverem instaladas; sem elas, entregue o rascunho em Markdown e diga como gerar o formato pedido.
- Comece pela conclusão e pela recomendação; a evidência vem depois.
- Traduza cada métrica no efeito para o negócio. Em vez de AUC, diga quantos dos clientes em risco a lista acerta entre os primeiros nomes e o que errar significa para o negócio. Sem custo informado, não invente valor: peça ao usuário ou descreva o efeito sem número. A métrica técnica vai para uma nota ou para o anexo à parte.
- Diga a incerteza e o que o relatório não afirma: o período e os dados que valem, que uma estimativa pode errar e que associação não prova causa.
- Um gráfico por mensagem, com um título que diz a conclusão.
- Monte uma tabela que liga cada número do texto à célula ou saída de onde ele veio, e confira os números nessas saídas. Essa tabela e o anexo técnico acompanham o relatório à parte, ou ficam na resposta, sem contar no limite de páginas. Se as saídas podem estar desatualizadas, diga isso ou rode de novo com autorização.
- Dados de pessoas aparecem só agregados, como pede a skill `personal-data`.

## Postmortem de incidente

Linha do tempo com horários e fonte de cada evento, impacto medido (quem, quantos, por quanto tempo), causa, o que ajudou e o que atrapalhou a resposta, e ações com responsável e prazo. Descreva falhas de processo e de sistema, sem culpar pessoas. Separe o confirmado do que ainda é hipótese. Não inclua segredos, nem o valor de um segredo vazado, e dados de pessoas só agregados, como pede a skill `personal-data`. Publicar ou enviar o postmortem é decisão do usuário.

## Release notes, changelog, PR e commit

Descreva mudanças efetivamente implementadas e seus efeitos. Separe novidades, correções e incompatibilidades conforme a convenção do projeto. Preserve rastreabilidade e divulgações exigidas; não proíba menções a ferramentas ou assistência quando forem relevantes ou requeridas.
Gerar o texto não autoriza criar commit, abrir PR, publicar release ou enviar mensagem a terceiros.
