# Plataformas de apps e sites

Use quando o destino é Vercel, Netlify, Streamlit Community Cloud, shinyapps.io, Posit Connect ou o serviço do Power BI. Os detalhes valem para a documentação oficial de novembro de 2026. Limites e planos mudam sem aviso, então confira a página da plataforma antes de depender de um deles.

## Em qualquer plataforma

- Defina a restrição de acesso na arquitetura: confirme no plano contratado que o app pode ficar privado e como os usuários entram, e confira de novo antes de publicar.
- Restringir quem abre o app na plataforma e autenticar dentro do app, como com `st.login`, são camadas diferentes; o plano diz qual delas atende ao requisito de acesso.
- Segredos ficam no recurso da plataforma ou no cofre da CI, nunca no Git. Se o app só lê o banco, a credencial dele é só de leitura.
- O banco precisa ser alcançável da plataforma: confira rede, SSL e lista de IPs permitidos. Abrir o banco para a internet é decisão do usuário.
- A identidade da release é o commit ou o bundle publicado, com o horário ou ID do deploy que a plataforma mostra.
- Recuperar é publicar de novo o commit ou bundle anterior, com autorização. Dados que o app gravou não voltam com ele.

## Vercel

A Vercel tem um plugin oficial para agentes (`npx plugins add vercel/vercel-plugin`), com skills de deploy, domínios, variáveis de ambiente e autenticação, e a coleção `vercel-labs/agent-skills`, com a `deploy-to-vercel`; use-os como especialistas quando estiverem instalados. Em Netlify ou Cloudflare Pages, confira na documentação o equivalente de cada item abaixo.

- Com a integração Git, push ou merge na branch de produção (em geral `main`) gera deploy de produção; outras branches, pull requests e `vercel` sem `--prod` geram preview. O primeiro deploy de um projeto novo é sempre de produção, mesmo vindo de outra branch: peça a autorização dele como produção. Sem domínio próprio ligado, ele fica só no endereço `vercel.app`; ligue o domínio depois de conferir.
- Cada deploy tem URL própria. Para conferir com a configuração de produção antes de liberar o domínio, desligue a atribuição automática dos domínios de produção e promova manualmente; esse deploy usa variáveis e dados de produção.
- As variáveis de ambiente são separadas por ambiente (Production, Preview e local), e mudar uma pede novo deploy. O primeiro deploy usa as de Production.
- Domínio próprio: o domínio raiz usa registro A, o subdomínio usa o CNAME que o painel mostra para o projeto, ou o domínio inteiro passa para os nameservers da Vercel. Antes de trocar os nameservers, copie os registros existentes, como o MX do e-mail. A propagação do DNS leva tempo, e o smoke espera dentro da janela definida.
- O Instant Rollback aponta os domínios para um deploy de produção anterior, sem restaurar variáveis de ambiente, e desliga a atribuição automática: os pushes seguintes não vão ao ar até desfazer o rollback ou promover outro deploy. No plano Hobby, ele só volta para o deploy imediatamente anterior.

Fontes: [ambientes](https://vercel.com/docs/deployments/environments), [Instant Rollback](https://vercel.com/docs/instant-rollback), [domínio próprio](https://vercel.com/docs/domains/working-with-domains/add-a-domain).

## Streamlit Community Cloud

- Publica de um repositório GitHub e reflete cada push quase na hora: o push é o deploy, então a autorização de publicação vem antes dele.
- O app herda a visibilidade do repositório: de repositório público, nasce público; de privado, nasce visível só para os desenvolvedores do workspace. Para restringir, em Sharing escolha "Only specific people can view this app" e convide por e-mail; quem entra usa Google ou um link enviado por e-mail. A documentação permite um app privado por vez.
- Dependências: vale o primeiro arquivo reconhecido entre `uv.lock`, `Pipfile`, `environment.yml`, `requirements.txt` e `pyproject.toml` (poetry), procurado na pasta do entrypoint e depois na raiz. Use um só. Pacotes de sistema vão em `packages.txt` na raiz.
- A versão do Python é escolhida nas configurações avançadas do deploy; desenvolva na mesma.
- Segredos: o conteúdo do `secrets.toml` vai no campo Secrets das configurações do app, e o código lê com `st.secrets`. `.streamlit/secrets.toml` fica no `.gitignore`.
- O app dorme depois de 12 horas sem tráfego, e uma visita o acorda. Os limites de CPU e memória são pequenos.
- O acesso privado é por convite a e-mails, sem ligação com o diretório da empresa: grupos e desligamentos não chegam sozinhos à lista. Para dados internos que exigem SSO, use outra plataforma, como o Posit Connect com o login da empresa ou hospedagem própria atrás dele.
- A documentação não publica IPs de saída, e a equipe do Streamlit disse no fórum que a lista de IPs permitidos foi descontinuada. Um banco protegido por lista de IPs pode recusar o app; decida isso na arquitetura, por exemplo com uma API na frente dos dados ou outro destino.

Fontes: [dependências](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies), [segredos](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management), [compartilhamento](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app), [gestão do app](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app), [fórum sobre IPs](https://discuss.streamlit.io/t/security-what-ip-address-range-can-i-whitelist-for-my-db-connection/55865).

## shinyapps.io

- A conta é configurada com o token e o segredo da página Tokens, por `rsconnect::setAccountInfo()` em R ou `rsconnect add` em Python. Eles dão acesso à conta inteira: o usuário os configura na máquina dele ou no cofre da CI, fora do chat, de scripts versionados e de logs.
- Deploy com `rsconnect::deployApp()` em R ou `rsconnect deploy shiny <pasta>` em Python. Em R, o rsconnect varre o código e registra as versões dos pacotes instalados na máquina que publica, junto com a versão do R; a documentação cita as chamadas `library()`, e o app não chama `install.packages()`. São aceitos CRAN, GitHub e Bioconductor.
- App privado existe só nos planos Standard e Professional: em Users, Application Visibility passa a Private, e os usuários são convidados por e-mail. Entram com Google, GitHub ou conta do shinyapps.io. Mudar a visibilidade reinicia o app.
- A documentação não descreve um cofre de variáveis para o app. Se a credencial viaja no bundle, confira o que o deploy envia e mantenha o arquivo fora do Git. O app publicado recebe `R_CONFIG_ACTIVE=shinyapps`, que o pacote `config` usa para escolher a seção do `config.yml`.
- A instância padrão é `large` (1 GB), ajustável com `rsconnect::configureApp()`, e dorme depois de 15 minutos ociosa. Os logs saem com `rsconnect::showLogs()`.

Fontes: [primeiros passos](https://docs.posit.co/shinyapps.io/guide/getting_started/), [autenticação](https://docs.posit.co/shinyapps.io/guide/authentication_and_user_management/), [aplicações](https://docs.posit.co/shinyapps.io/guide/applications/).

## API em contêiner ou PaaS

Para uma API como a de FastAPI em Render, Fly.io, Railway, Cloud Run ou equivalente, confira na documentação da plataforma:

- o endpoint de saúde que a plataforma usa para decidir se a versão nova entra no ar;
- a ordem entre a migração do banco e o deploy, como manda a [referência de migrações](db-migrations.md);
- variáveis de ambiente e segredos por ambiente;
- a conexão com o Postgres: SSL, limite de conexões e pool;
- como a imagem ou o commit publicado é identificado e como voltar ao anterior.

## Posit Connect

Use a skill `deploy-to-connect` da Posit quando ela estiver instalada; sem ela, informe o comando de instalação (`claude plugin install connect@posit-dev-skills` ou `npx skills add posit-dev/skills`) e siga a documentação do rsconnect. A skill diz como publicar; os gates e as autorizações da release continuam valendo.

- O servidor e a conta vêm do usuário. Não publique no único servidor salvo só porque ele é o único.
- `deployApp()` e `posit connect deploy` levam todos os arquivos da pasta: no saneamento, confira o que vai junto e restrinja a seleção quando houver dado, `.env` ou arquivo que o app não usa.
- Conteúdo Python precisa de `requirements.txt`. Gerar um com `--force-generate` roda `pip freeze` e pode fixar versões demais, então criar esse arquivo também pede o aceite do usuário.
- Instalar a CLI, entrar na conta ou criar uma chave de API entram no mesmo pedido de autorização da publicação.

## Power BI

Para autoria de modelo e relatório, a skill oficial é o plugin `powerbi-authoring` da Microsoft, do marketplace `microsoft/skills-for-fabric` ([visão geral](https://learn.microsoft.com/en-us/power-bi/developer/agentic/power-bi-agentic-overview)). Aqui ficam só a publicação e o acesso.

- O Power BI Desktop pede Windows 10 ou Windows Server 2016 ou posterior ([requisitos](https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-get-the-desktop)). Em outro sistema, entregue os dados, as medidas e o projeto PBIP, e diga o que fica para quem tem o Desktop.
- Publicar envia ao workspace escolhido o modelo semântico, com os dados, e os relatórios. Republicar substitui o modelo publicado, pode quebrar visuais que usam um campo renomeado ou apagado e dispara a atualização agendada ([publicar do Desktop](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-upload-desktop-files)). O A2 nomeia o workspace e diz se é a primeira publicação ou uma substituição.
- Link de compartilhamento, papel no workspace, app, compartilhamento externo e publicar na web são efeitos separados, cada um com seu A2. Quem recebe o relatório tem leitura do modelo inteiro, salvo segurança por linha (RLS) ou por objeto (OLS); esconder coluna, medida ou página não restringe o acesso. Publicar na web deixa o relatório e os dados do modelo públicos, sem autenticação ([compartilhar](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-share-dashboards)).
- A identidade da release é o arquivo ou o commit do projeto PBIP, com o horário da publicação. Recuperar é republicar a versão anterior, com autorização.

## Smoke

- Abra o endereço publicado no navegador e confira um valor exibido depois de uma interação. A primeira visita pode só acordar o app.
- Em app privado, o smoke roda numa sessão em que o usuário já entrou, ou o próprio usuário confere e relata. Não guarde senha, cookie ou link de convite, e não torne o app público para testar.
