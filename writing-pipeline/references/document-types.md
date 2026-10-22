# Convenções por tipo de documento

Leia apenas a seção do artefato solicitado. Arquétipo do projeto ajuda no contexto, mas não determina sozinho pessoa gramatical, estrutura, idioma ou norma. Preserve requisitos editoriais declarados.

## PRD, especificação e plano

Distinga problema observado, objetivo futuro, requisito, critério de aceite e decisão. Métricas desejadas ficam identificadas como metas, nunca como resultados alcançados. Preserve non-goals, restrições e questões abertas. Use os nomes e contratos de arquivos da pipeline chamadora, sem criar um segundo plano.

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

## Release notes, changelog, PR e commit

Descreva mudanças efetivamente implementadas e seus efeitos. Separe novidades, correções e incompatibilidades conforme a convenção do projeto. Preserve rastreabilidade e divulgações exigidas; não proíba menções a ferramentas ou assistência quando forem relevantes ou requeridas.
Gerar o texto não autoriza criar commit, abrir PR, publicar release ou enviar mensagem a terceiros.
