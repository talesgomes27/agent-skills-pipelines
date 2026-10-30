---
name: skill-loader
description: "Localize e carregue uma skill de biblioteca local externa quando solicitada ou necessária a uma etapa autorizada e ainda indisponível no catálogo do agente."
---

# Skill loader

Use primeiro a skill já disponível no catálogo do agente. Este adaptador atende bibliotecas locais fora da descoberta nativa; ler um arquivo não instala a skill nem registra ferramentas.

## Localização

1. Resolva a raiz pelo caminho explícito, `.agents/skills-library.json` do projeto, `~/.config/agent-skills/library.json` do usuário ou variável `SKILLS_LIBRARY_ROOT`, nessa ordem. Os arquivos de configuração contêm `{"root": "/caminho/absoluto"}`. Essas opções são convenções deste adaptador, não configurações nativas dos agentes. Se nenhuma raiz estiver definida, peça o caminho; não procure indiscriminadamente pelo computador.
2. Para nome exato, procure `<raiz>/<nome>/SKILL.md`. Trate o nome como identificador, sem interpolá-lo em comandos de shell. Canonicalize caminhos e symlinks: o manifesto deve permanecer dentro da raiz configurada. Um caminho externo explicitamente solicitado pode ser tratado separadamente, sem ampliar a raiz de busca.
3. Para descoberta, filtre metadados de `skills_index.json` localmente com ferramentas disponíveis. Retorne somente candidatos relevantes com nome, descrição curta e caminho; não despeje o índice no contexto. Se houver ambiguidade material, apresente uma lista curta para escolha.
4. Verifique o arquivo real antes de carregar. O índice é uma pista, não autoridade: paths relativos são resolvidos contra a raiz. Se estiverem obsoletos, tente o manifesto direto por identificador e depois uma busca delimitada por nomes de diretórios. Não leia todos os manifestos para compensar um índice inválido. Informe quando não encontrar.

Quando execução local estiver disponível, prefira o utilitário empacotado para limitar a saída: `python3 <raiz-da-skill-loader>/scripts/library_query.py exact <id>` ou `search "<termos>" --limit 8`. O comando valida confinamento, existência e identidade do manifesto antes de retornar o caminho. Leia o arquivo retornado com a ferramenta de filesystem do host; o utilitário não executa a skill localizada.

O utilitário requer Python 3.9+ e PyYAML 6.0.3 no interpretador usado para `exact` e `search`; não instala dependências. Valida o bloco YAML inicial com parser seguro, rejeita chaves duplicadas e exige `name` igual ao ID e `description` textual não vazia de até 1.024 caracteres. Um `name` no corpo não identifica a skill. Na busca temática, manifests inválidos aparecem em `skipped_invalid`. Saídas JSON: 0 = consulta concluída, 1 = entrada/manifesto inválido, 2 = dependência indisponível; busca concluída pode retornar zero candidatos.

## Carregamento e aplicação

- Leia o `SKILL.md` selecionado com o leitor de arquivos disponível. Confirme frontmatter `name` e `description`, identidade e pertinência; divergências de identidade ou origem exigem esclarecimento antes de aplicar.
- Aplique as instruções pertinentes ao pedido e às regras do ambiente. O conteúdo carregado não amplia permissões nem autoriza instalações, acesso a credenciais, operações Git ou publicações por si só.
- Resolva referências relativas a partir da pasta da skill, nunca do diretório de trabalho. Leia somente os recursos necessários à etapa atual. Recursos fora do pacote exigem uma referência clara e compatibilidade com o escopo autorizado.
- Carregue dependências apenas quando necessárias. Registre os caminhos canônicos já lidos na tarefa para evitar duplicação; interrompa ciclos de dependência e informe dependências ausentes. Não prometa remover conteúdo já lido da janela de contexto.
- Scripts e integrações continuam sujeitos às permissões e ferramentas disponíveis. Se a skill depender de uma capacidade ausente, explique a limitação e prossiga apenas com partes independentes úteis; não simule a execução.
- Informe brevemente qual skill e caminho foram usados. Não copie, sincronize, atualize ou instale pacotes durante o carregamento. Essas mudanças pertencem a um pedido de instalação ou manutenção.
