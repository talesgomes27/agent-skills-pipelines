# Mudanças condicionais por arquétipo

Um padrão é candidato, não objetivo obrigatório. Preserve a stack e o desenho saudável do projeto; cada mudança precisa de problema, escopo, contrato e verificação.

## A: dados, ciência e publicação

Extraia lógica de notebook quando melhorar teste/reuso comprovado, preservando ordem, efeitos e interfaces. Não force `src/` ou notebook adicional a um relatório funcional.
Vetorização ou troca de biblioteca pode alterar precisão, ordenação, tratamento de nulos, execução e uso de memória. Classifique como otimização/migração e compare resultados e desempenho com dados representativos antes de declarar ganho.
Leakage, split, seed, estimador e métrica são decisões metodológicas que podem mudar resultados. Faça correção aprovada com critérios próprios, sem chamá-la de refatoração equivalente.
Reorganização de relatório, idioma, política de cache, estética, DPI e formato dependem do destino e pedido. Não introduza SHAP/modelos em análise descritiva nem migre R Markdown/ambiente só por preferência. Mudança de engine ou dependências é migração separada, com paridade avaliada.

## B: serviços, APIs e interfaces

Extraia serviços/repositórios apenas quando separar responsabilidade ou reduzir acoplamento real; não crie camadas para todo controlador.
Preserve schema, status, erros, autorização, transações, concorrência e compatibilidade dos consumidores. Otimizações SQL precisam preservar resultados, ordenação contratada e garantias transacionais. Índice/migração pode ter custo e efeitos operacionais, além do diff de código.
Renomeações e codemods devem considerar imports, configuração, serialização, referências dinâmicas e chamados externos; parser/IDE ajuda, mas testes e revisão continuam necessários.

## C: CLI e automação

Separar parser e lógica pode facilitar testes. Transformar um comando existente em subcomandos ou trocar dependências pode quebrar flags, códigos de saída, mensagens e pipelines; precisa de contrato de compatibilidade e autorização.
Confira stdout/stderr, quoting, ambiente, arquivos, interrupções e idempotência pertinentes. Uma nova mensagem de erro não é apenas estilo quando integrações a consomem.

## Aplicação e integração

Não altere golden files, tolerâncias ou testes para esconder uma diferença. Para correção intencional, atualize evidência e expectativa com justificativa.
Use fatias com propriedade de arquivos e pré-requisitos claros. Paralelismo não é obrigatório; só execute mudanças independentes quando capacidade e autorização existirem. Revise integração antes do aceite.
Não rode formatador com reescrita no reconhecimento nem misture migração de ambiente e mudança de lógica em uma fatia sem razão verificável.
