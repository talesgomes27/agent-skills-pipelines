# Citações, bibliografia e evidências

## Quatro verificações distintas

1. **Sintaxe:** a referência é reconhecida pelo parser do formato?
2. **Resolução:** a chave existe na bibliografia/metadados configurados para este documento?
3. **Identidade:** autor, título, data, DOI/URL e edição correspondem à obra citada?
4. **Sustentação:** o conteúdo consultado sustenta a afirmação específica, com seus qualificadores?

Passar uma etapa não prova as seguintes. Link acessível e DOI resolvido não comprovam conteúdo nem qualidade metodológica. Uma citação estilística não substitui a fonte de uma métrica do projeto.

## Bibliografia do documento

Inspecione a configuração efetiva do documento/projeto: `bibliography`, referências inline ou mecanismo equivalente. Resolva caminhos conforme o motor e a raiz do projeto; não use um manifesto global da skill como allowlist de fontes.
Para Quarto/Pandoc, considere citações narrativas (`@chave`), grupos (`[@a; @b]`), supressão de autor (`[-@a]`) e localizadores (`[@a, p. 12]`). Um parser AST pode distinguir citações reais de exemplos literais em código. Regex simples é triagem, não validador completo.
Não confunda `@fig-*`, `@tbl-*` e outras referências cruzadas com citações bibliográficas. Em documentos Quarto, essas referências dependem do motor e podem exigir validação do build configurado, além de inspeção de AST.
Se a ferramenta adequada não estiver disponível, informe a limitação e confira os casos relevantes manualmente; não instale dependências como requisito de uma revisão curta. Confira a saída do formato pretendido quando o escopo incluir renderização. Typst e backends LaTeX podem usar processadores diferentes de citeproc.
Chave ausente deve gerar achado localizado: verificar grafia, fonte existente ou inclusão fundamentada na bibliografia do projeto quando autorizada. Não substitua citação formal por URL só para contornar validação.

## Origem de afirmações

Para números de projeto, use dados/saídas com versão, recorte, unidade e condições pertinentes. Identifique explicitamente metas, resultados medidos e exemplos hipotéticos. Uma revisão de estilo não cria capacidade de 2.500 transações/s onde o original só dizia “rápido”.
Para comportamento de software, confira implementação, configuração e/ou execução pertinente. Não execute exemplo que possa gravar em banco, publicar ou consumir recursos fora do escopo autorizado.
Para fontes externas, prefira a obra/documentação primária. Catálogos e APIs de metadados podem ajudar a localizar a identidade; confirme o trecho antes de atribuir uma afirmação. Sem acesso integral, não diga que verificou além do material consultado.
Registre pendências no parecer ou rascunho, sem inserir marcadores de aparência final nem omitir incerteza importante. Preserve citações literais e traduções identificadas, respeitando os limites de uso do material.

## Ferramentas opcionais

Parser/citeproc ou motor de publicação: sintaxe, resolução e renderização. Vale: regras de estilo e terminologia com escopos de prosa. markdownlint: estrutura Markdown. Link checker: acessibilidade de URLs/arquivos, com rede e privacidade controladas. Nenhuma dessas ferramentas comprova sustentação factual; a verificação da afirmação permanece necessária.
