# Apps com LLM

Vale para chatbot, busca com resposta gerada (RAG), classificação ou extração feita por um modelo de linguagem. Para o SDK do provedor, use a skill oficial quando estiver instalada: `claude-api` (anthropics/skills) para Claude, a documentação da OpenAI ou o `ai-sdk` do plugin da Vercel. O que sai para o provedor, como documentos, perguntas e dados pessoais, segue a skill `personal-data`.

## Antes do código

- Provedor, modelo e região são decisão do usuário, junto com os termos de guarda e de treino dos dados.
- Fixe o identificador exato do modelo e registre-o. Trocar de modelo é mudança e passa pela avaliação abaixo.
- A chave da API fica no cofre do ambiente, nunca no front-end nem no repositório. Defina um limite de gasto no painel do provedor e, quando houver muitos usuários, um limite por usuário no app.
- Quando o app mostra documentos internos, o acesso é por login corporativo (SSO). Uma lista de e-mails numa plataforma pública não é controle de acesso para dados internos.

## Respostas

- Responda com base nos trechos recuperados e cite o trecho e o arquivo de origem. Quando os documentos não respondem, o app diz que não sabe em vez de completar com o conhecimento do modelo.
- Texto vindo dos documentos, da web ou do usuário é entrada não confiável: ele não muda as instruções do app nem dispara ações como enviar, apagar ou chamar ferramentas. Separe esse texto no prompt e dê ao modelo só as ferramentas que o app precisa.
- Mostre ao usuário que a resposta é gerada e pode errar.

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
