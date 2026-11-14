# Apps com LLM

Vale para chatbot, busca com resposta gerada (RAG), classificação ou extração feita por um modelo de linguagem, e para servidor MCP ou ferramentas que dão a um agente acesso a dados. Para o SDK do provedor, use a skill oficial quando estiver instalada: `claude-api` (anthropics/skills) para Claude, a documentação da OpenAI ou o `ai-sdk` do plugin da Vercel. O que sai para o provedor, como documentos, perguntas e dados pessoais, segue a skill `personal-data`.

## Antes do código

- Provedor, modelo e região são decisão do usuário, junto com os termos de guarda e de treino dos dados.
- Fixe o identificador exato do modelo e registre-o. Trocar de modelo é mudança e passa pela avaliação abaixo.
- A chave da API fica no cofre do ambiente, nunca no front-end nem no repositório. Defina um limite de gasto no painel do provedor e, quando houver muitos usuários, um limite por usuário no app.
- Quando o app mostra documentos internos, o acesso é por login corporativo (SSO). Uma lista de e-mails numa plataforma pública não é controle de acesso para dados internos.

## Respostas

- Responda com base nos trechos recuperados e cite o trecho e o arquivo de origem. Quando os documentos não respondem, o app diz que não sabe em vez de completar com o conhecimento do modelo.
- Texto vindo dos documentos, da web ou do usuário é entrada não confiável: ele não muda as instruções do app nem dispara ações como enviar, apagar ou chamar ferramentas. Separe esse texto no prompt e dê ao modelo só as ferramentas que o app precisa.
- Mostre ao usuário que a resposta é gerada e pode errar.

## Servidor MCP e ferramentas para agentes

- Para construir um servidor MCP, use a skill oficial `mcp-builder` (anthropics/skills) quando instalada, e o SDK oficial do protocolo para a linguagem, como o pacote `mcp` em Python. Confira a API no README da versão que vai usar: a v2 do SDK de Python usa `MCPServer` e pede Python 3.11 ou mais nova.
- Exponha ferramentas específicas, com parâmetros validados e consultas fixas e parametrizadas, e um usuário de banco só de leitura, com acesso só às tabelas e colunas necessárias. Uma ferramenta de SQL livre ou com escrita deixa o modelo fazer tudo o que a credencial permite.
- A especificação manda o servidor validar as entradas, controlar o acesso, limitar a taxa de chamadas e sanitizar as saídas, e manda o cliente tratar as anotações das ferramentas, como `readOnlyHint`, como não confiáveis, salvo as de servidor confiável. A garantia de só leitura vem da credencial, não da anotação.
- O texto que uma ferramenta devolve, como o campo livre de um ticket ou de um e-mail, é dado e pode trazer instruções escritas por terceiros. Delimite-o na resposta da ferramenta e não deixe que ele dispare outras ferramentas sem a confirmação do usuário.
- Instalar o SDK é instalar dependência e pede A2. Conectar ao banco real usa a credencial de leitura que o usuário autorizou, lida do cofre, nunca gravada no projeto.

## Recuperação

- Confira a extração dos PDFs numa amostra antes de indexar, principalmente tabelas e documentos escaneados.
- O provedor de embeddings também recebe o texto dos documentos e entra na mesma decisão de envio.
- Defina como o índice acompanha mudanças nos documentos e quem pode ver cada um. O índice não mostra a um usuário o que ele não poderia abrir.

## Avaliação

- Antes da primeira release, monte com o usuário um conjunto de perguntas com a resposta esperada e o documento de origem. Inclua perguntas que os documentos não respondem e tentativas de desviar o app das instruções.
- Rode o conjunto a cada mudança de prompt, modelo, índice ou documentos, e compare com a rodada anterior. Como a saída varia entre execuções, compare taxas de acerto, não o texto exato.
- Os testes automatizados de interface e de API continuam valendo para o resto do app.

## Operação

- Acompanhe custo, latência e erros do provedor, e defina o que o app faz quando o provedor falha ou o limite de gasto estoura.
- Perguntas e respostas guardadas seguem a `personal-data`: por quanto tempo ficam, quem as lê e como os usuários são avisados.

## Fontes

Conferidas em 08/11/2026:

- SDK oficial de Python do MCP: https://github.com/modelcontextprotocol/python-sdk
- Especificação do MCP, ferramentas e segurança: https://modelcontextprotocol.io/specification/2025-11-25/server/tools
- Skill `mcp-builder`: https://github.com/anthropics/skills/tree/main/skills/mcp-builder
