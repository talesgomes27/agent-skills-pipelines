# Arquitetura por arquétipo

Em B e C, as restrições do destino que costumam mudar a arquitetura são autenticação, hibernação, limites, custo e armazenamento. Num app novo leve, com um só aceite por PC-2, PC-3 e PC-5, a restrição do destino que muda a arquitetura vai no início da resposta, antes do escopo, para o usuário não aceitar sem vê-la.

Leia só a parte do arquétipo registrado e, em projeto híbrido, a do domínio secundário nas partes que ele usa, além das seções gerais: forma da spec, linguagem por componente, registro do arquétipo e onde a verificação roda. Com dados de pessoas, em qualquer arquétipo, a arquitetura diz onde eles ficam, quem os vê e o que sai do ambiente, seguindo a skill `personal-data`.

## A: análise e modelos

- Separe preparação, análise e publicação, e registre de onde vem cada dado e onde cada resultado é gerado.
- Em estudo acadêmico, siga a organização do formato pedido.
- Previsão de séries define no plano a validação por origem móvel: em cada origem, o modelo treina só com o passado e é avaliado no horizonte pedido, como os 3 meses seguintes. O baseline é o ingênuo sazonal, que repete o valor do mesmo mês do ano anterior, e um modelo que não o supera nessa validação não é recomendado. Para comparar séries de escalas diferentes, como lojas grandes e pequenas, use um erro escalado como o MASE; o MAPE fica infinito com venda zero e extremo perto de zero. Diga ao usuário quantas origens a validação usou, porque com poucos anos de dados a diferença entre modelos pode ser ruído. Quando a diferença não se sustenta nessas origens, recomende o modelo mais simples e declare a limitação. Fontes: [validação de séries](https://otexts.com/fpp3/tscv.html), [métodos simples](https://otexts.com/fpp3/simple-methods.html) e [erros escalados](https://otexts.com/fpp3/accuracy.html), do livro *Forecasting: Principles and Practice*.
- Em Quarto, siga a [checklist](quarto-quality-checklist.md) e defina em PC-4 idioma, formato, política de execução e pré-requisitos de renderização; o `.qmd` pode ter só cabeçalhos e placeholders.

## B: aplicações

- Limites e persistência proporcionais ao domínio, com DDD, C4 ou OpenAPI só quando a complexidade pede.
- Site ou app web define no plano as metas de SEO, acessibilidade e desempenho, o destino do formulário e onde o site é publicado; a referência B da `execution-pipeline` tem o mínimo de cada um.
- App publicado numa plataforma decide na arquitetura as duas camadas de acesso: quem abre o app na plataforma e quem se autentica dentro dele. As restrições de cada plataforma (acesso privado, IPs de saída, hibernação) estão na referência de plataformas da `release-and-ops-pipeline`; leia-a em PC-3, sem esperar a publicação.
- Dashboard no Power BI: o Power BI Desktop roda só no Windows, então fora dele o plano prepara os dados, as medidas DAX com a fórmula e um projeto PBIP, sem dizer que gerou um `.pbix`. Para autoria de modelo e relatório, aponte o plugin oficial `powerbi-authoring` da Microsoft, do marketplace `microsoft/skills-for-fabric`. A arquitetura decide o workspace e quem vê cada dado: quem recebe o relatório lê o modelo inteiro, salvo segurança por linha ou objeto. Publicar, compartilhar e criar o app são efeitos com A2, como diz a referência de plataformas da `release-and-ops-pipeline`.
- App com LLM que envia documentos ou dados ao provedor é esforço rigoroso e decide na arquitetura provedor e modelo, onde fica a chave, quem acessa, o que vai para o provedor e como as respostas serão avaliadas; a `execution-pipeline` tem a referência de apps com LLM.
- App que grava dados, mesmo no esforço leve, diz onde eles ficam e como copiar e restaurar.
- Pedido com login decide em PC-2 quem cria as contas (cadastro aberto, convite ou administrador) e como se recupera a senha, porque isso muda telas, e-mails enviados e o mínimo de segurança da referência B da `execution-pipeline`. Login com senha tira o app do esforço leve.
- Mudança de esquema num banco que já tem dados de produção entra na arquitetura como plano de migração, com backup, etapas compatíveis e volta; a `release-and-ops-pipeline` tem a referência de migrações.

## C: automações

- Entradas, saídas, erros, exit codes e idempotência.
- Num job agendado, também horário e fuso, onde o estado fica entre execuções, nova tentativa e quem recebe o alerta de falha.
- Modelo pontuado ou retreinado de forma recorrente segue a referência de modelo em produção da skill `scheduled-automation`.
- Coleta em sites ou APIs de terceiros declara a fonte, os termos de uso e o robots.txt que valem, o ritmo das requisições e o que fazer diante de login ou CAPTCHA.

## Forma da spec

Os requisitos da [spec viva](spec-template.md) mudam de forma conforme o arquétipo principal; em projeto híbrido, cada componente usa a forma do seu domínio.

- **A, análise e modelos.** Cada pergunta vira um cartão `### H-001`: a pergunta, a hipótese ou estimativa esperada, o dado e o recorte que a respondem, o método, o critério que confirma ou refuta (por exemplo, "diferença maior que o intervalo de 95%" ou "MASE abaixo do ingênuo sazonal em todas as origens") e a decisão que muda com a resposta. A evidência é a célula rotulada, a tabela ou a figura que responde.
- **B, aplicações.** Cada requisito `### R-001` tem critério no formato Dado / Quando / Então, com o valor observável na tela ou na resposta da API, e um critério por papel quando há login. Requisito de interface que outro sistema usa traz o contrato (rota, campos, códigos de erro).
- **C, automações.** Cada job ou comando tem um contrato de execução: entradas e de onde vêm, saídas e para onde vão, horário e fuso, idempotência (rodar duas vezes dá o mesmo resultado), comportamento em falha (código de saída, nova tentativa, alerta e quem recebe) e onde fica o estado entre execuções. O critério diz o que conferir depois de uma execução de teste.

Exemplo de cartão de análise:

```markdown
### H-001 A campanha de março aumentou a recompra?
- Hipótese: a recompra em 60 dias subiu entre quem recebeu a campanha.
- Dados: pedidos de jan a mai, clientes ativos; grupo de controle sem envio.
- Método: diferença de proporções entre os grupos, com intervalo de 95%.
- Critério: confirma se o intervalo da diferença não inclui zero.
- Decisão: repetir a campanha em junho.
- Estado: aprovado
- Evidência: (preenchida na entrega)
```

## Linguagem por componente

Em PC-3, cada componente diz a linguagem e a versão, com o motivo, preferindo a que o projeto e a equipe já usam. Duas linguagens no mesmo projeto, como R na análise e Python na API, pedem uma interface explícita entre elas: arquivo com formato e esquema definidos, tabela ou API, nunca chamada de uma dentro da outra sem decisão registrada. O plano registra a linguagem e a versão de cada componente, e o handoff de PC-5 diz que a `execution-pipeline` vai ler o perfil de cada uma, em `references/languages/` (Python, R, SQL, Bash, Go, JVM).

## Registro do arquétipo

Na spec viva, o arquétipo fica no front matter da `docs/spec.md` (`arquetipo: {principal: aplicacao, secundario: analise}`), como em [spec viva](spec-template.md). Sem spec, ou num projeto que já o tem, `docs/00_archetype.md` registra em YAML `archetype`, `stack`, `project_name`, `gerado_por: pre-code-pipeline` e `data` (ISO 8601). O arquétipo aceita a letra ou o nome: A ou `analise`, B ou `aplicacao`, C ou `automacao`. Stack indefinida fica explícita; não invente versões.

## Onde a verificação roda

O plano diz onde cada verificação roda: dados de teste, cópia ou acesso só de leitura aos dados reais, e banco, pasta, chat ou conta de teste para efeitos externos.
