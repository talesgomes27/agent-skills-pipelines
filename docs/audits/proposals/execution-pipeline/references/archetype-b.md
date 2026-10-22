# B: software, APIs e interfaces

Use a linguagem, framework e gerenciador aprovados. Não introduza FastAPI, React ou Tailwind apenas por constarem de uma biblioteca de skills.

## Gates 1 e 2

Implemente contratos e testes na estrutura real do projeto, com tipos suportados pela linguagem. Para Python, use comandos configurados no projeto; para TS/JS, consulte scripts de `package.json`, lockfile e runner antes de escolher teste, lint, formato, typecheck e build. Não crie um ambiente Python para validar aplicação TS.
Valide fronteiras relevantes: autenticação/autorização, payloads inválidos, erros de serviços, persistência e transações conforme o escopo. Clientes falsos e mocks devem representar fronteiras identificadas, sem substituir a integração exigida no plano.
Crie migrações como arquivos revisáveis. Aplicação fica limitada à base de desenvolvimento/teste autorizada, com destino e efeitos conhecidos. Credenciais, MCP e uma ferramenta disponível não concedem autorização de produção.

## Gate 3

- Com UI: preserve design system e framework, confira navegação, teclado, estados de erro/carregamento e responsividade do escopo alterado.
- Sem UI: valide status codes, serialização, erros e contratos de API; OpenAPI/Swagger somente quando aplicáveis ao protocolo.
- Para navegador, aproveite o runner existente; use locators e asserções que aguardam o estado esperado. Não use pausa fixa ou `networkidle` como comprovação genérica de prontidão.

## Gates 4 e 5

Documente setup realista, configuração, uso e limites operacionais. Exemplos de API devem corresponder ao contrato implementado, sem tokens reais.
Execute os checks obrigatórios da stack, integrações e build. Cobertura ajuda a identificar lacunas quando prevista, mas percentual ou mocks não provam requisitos atendidos. E2E cobre jornadas críticas afetadas; não gere uma suíte web para serviço sem tela.
Use Playwright Test/CLI ou equivalente para regressão repetível; MCP de navegador é opcional para exploração e inspeção interativa, sem substituir testes versionados quando exigidos.
