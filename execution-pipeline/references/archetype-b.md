# B: aplicações, APIs e dashboards

Use a linguagem, framework e gerenciador aprovados. Não introduza FastAPI, React ou Tailwind apenas por constarem de uma biblioteca de skills.

## EX-1 e EX-2

Implemente contratos e testes na estrutura real do projeto, com tipos suportados pela linguagem. Para Python, use comandos configurados no projeto; para TS/JS, consulte scripts de `package.json`, lockfile e runner antes de escolher teste, lint, formato, typecheck e build. Não crie um ambiente Python para validar aplicação TS.
Valide fronteiras relevantes: autenticação/autorização, payloads inválidos, erros de serviços, persistência e transações conforme o escopo. Clientes falsos e mocks devem representar fronteiras identificadas, sem substituir a integração exigida no plano.
Crie migrações como arquivos revisáveis. Aplicação fica limitada à base de desenvolvimento/teste autorizada, com destino e efeitos conhecidos. Aplicar em produção é release e segue a referência de migrações da `release-and-ops-pipeline`. Credenciais, MCP e uma ferramenta disponível não concedem autorização de produção.

## Sites e APIs

Sem a skill citada em cada item, os itens desta seção são o mínimo, junto com a documentação oficial do framework.

- Segurança: revise com a ferramenta do host, como o `/security-review` do Claude Code, e com as [Cheat Sheets da OWASP](https://cheatsheetseries.owasp.org/). O mínimo: senha com hash de uma biblioteca mantida (Argon2 ou bcrypt), limite de tentativas no login, mensagem que não revela se o e-mail existe no login e na recuperação de senha (no cadastro, resposta neutra e confirmação por e-mail), sessão ou token com expiração, proteção contra CSRF em sessão por cookie, CORS só para as origens do app, HTTPS, validação no servidor e segredos fora do front-end.
- Acessibilidade e UX: use a `web-design-guidelines` (vercel-labs/agent-skills) quando instalada; sem ela, confira rótulos de formulário, contraste, foco visível, ordem do teclado e texto alternativo.
- Desempenho em React e Next.js: use a `vercel-react-best-practices` (vercel-labs/agent-skills), ou a `react-best-practices` do plugin da Vercel, e as skills oficiais do Next.js quando instaladas. Meça com Lighthouse ou com os Core Web Vitals da plataforma antes e depois de otimizar.
- Autenticação em Next.js na Vercel: a skill `auth` do plugin da Vercel cobre os provedores.
- SEO: title e description por página, Open Graph, sitemap, robots.txt e URL canônica, com o conteúdo que precisa ser indexado renderizado no servidor ou estático. Preview e staging ficam fora do índice.
- Formulário: diga para onde vão as mensagens (e-mail, serviço ou banco), proteja contra spam com honeypot, limite de envio ou CAPTCHA, valide no servidor e trate os dados como pede a skill `personal-data`. Site estático precisa de uma função serverless ou de um serviço externo para receber o formulário; esse serviço, e o de CAPTCHA, também recebem os dados. Em ambiente serverless, o limite de envio fica guardado fora da memória da função.
- App com LLM: siga [apps com LLM](llm-apps.md).

## Dashboards e apps de dados

Streamlit, Shiny, Dash e similares são B com dados de A. Use a skill oficial do framework quando instalada: `developing-with-streamlit` para Streamlit, `shiny-for-python` para Shiny em Python e, para Shiny em R, as da Posit (`shiny-bslib` para layout, `shiny-r-optimize` para desempenho). Elas cobrem estrutura, cache, reatividade e testes do framework; esta referência só acrescenta o que a pipeline exige. Sem a skill, informe o comando de instalação (`streamlit skills`, `uvx library-skills` ou o marketplace `posit-dev/skills`); instalar fica a critério do usuário. Atualizar o framework ou adotar a ferramenta nova que uma skill oficial recomenda é mudança de dependência e pede o aceite do usuário. Shiny em R não tem skill oficial de testes: `testServer()` testa a lógica dos módulos e `shinytest2` a interação. Separe consulta e transformação da interface para testá-las sem a UI, e confira os números exibidos com as regras de A: filtros, unidades, totais e nulos. Teste a interação pelo runner do framework se o projeto já usa um, ou por navegador, com asserção sobre um valor exibido depois de mudar um filtro. Cache e estado de sessão mudam o que cada usuário vê: confira a invalidação quando os dados mudam. Exportação de tabela é saída de dados e segue a política de acesso aprovada. Antes de otimizar, meça o tempo da interação lenta e repita a mesma medida depois.

## EX-3

- Com UI: preserve design system e framework, confira navegação, teclado, estados de erro/carregamento e responsividade do escopo alterado.
- Sem UI: valide status codes, serialização, erros e contratos de API; OpenAPI/Swagger somente quando aplicáveis ao protocolo.
- Para navegador, aproveite o runner existente; use locators e asserções que aguardam o estado esperado. Não use pausa fixa ou `networkidle` como comprovação genérica de prontidão.

## EX-4 e EX-5

Documente setup realista, configuração, uso e limites operacionais. Exemplos de API devem corresponder ao contrato implementado, sem tokens reais.
Execute os checks obrigatórios da stack, integrações e build. Cobertura ajuda a identificar lacunas quando prevista, mas percentual ou mocks não provam requisitos atendidos. E2E cobre jornadas críticas afetadas; não gere uma suíte web para serviço sem tela.
Use Playwright Test/CLI ou equivalente para regressão repetível; MCP de navegador é opcional para exploração e inspeção interativa, sem substituir testes versionados quando exigidos.
