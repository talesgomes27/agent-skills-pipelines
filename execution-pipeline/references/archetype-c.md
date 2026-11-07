# C: automações, scripts e CLI

Preserve linguagem e interfaces aprovadas. Um script shell não exige `src/`, Python, uv ou pytest por padrão.

## Gates 1 e 2

Implemente funções e parser proporcionais à tarefa. Trate argumentos inválidos, stdin, stdout, stderr e códigos de saída de acordo com o contrato. Mensagens de falha devem ser acionáveis; não esconda erros nem exponha segredos.
Use diretórios temporários e dados de teste para validar efeitos no filesystem. Confira idempotência, quoting, interrupções e pipelines quando parte dos requisitos. Testes não devem alterar a configuração real do usuário.

## Gate 3

Mantenha stdout adequado a consumo por outras ferramentas. Direcione logs/progresso para stderr quando necessário; desative controles de terminal em saída redirecionada. JSON ou outro modo estruturado só é obrigatório se estiver no contrato.
Não adicione barra de progresso a toda execução; use-a quando duração e interação justificarem. Preserve modos verbose/debug se definidos, sem traceback ruidoso na experiência normal.

## Job agendado

Um job agendado (cron, `schedule` do GitHub Actions, agendador da plataforma) segue o mesmo contrato de entradas, saídas e erros, sem terminal para acompanhar. A skill `scheduled-automation` traz o contrato completo, as opções de estado e os alertas. Sem ela instalada, o mínimo que o plano responde antes de agendar é:

- horário e fuso do agendador, e o que acontece com atraso ou execução perdida;
- onde o estado sobrevive entre execuções (banco, arquivos, marca da última execução), já que runners de CI são descartados;
- qual chave torna a reexecução idempotente, inclusive para reprocessar um dia passado;
- o que acontece com falha parcial e quantas novas tentativas, com espera crescente;
- quem é avisado quando falha, e por qual canal.

Ofereça dry-run e disparo manual do mesmo job, e teste com o recurso de teste do plano (pasta, banco, chat). Logs não mostram segredos nem dados pessoais.

Retreino de modelo é um job sobre um modelo de A. O plano define se o modelo novo substitui o anterior sozinho, por qual critério comparado com o atual, e onde fica a versão anterior para voltar.

## Gates 4 e 5

Documente sintaxe, flags, envs, exit codes e exemplos verificados. Confira `--help`, entradas inválidas e comportamento de erro quando suportados pela interface.
Para Python, use o runner e verificadores do projeto; para shell, `bash -n` e ShellCheck são checks estáticos candidatos, complementados por execução em ambiente isolado. Bats ou outro runner existente pode verificar comportamento. Sintaxe válida não comprova quoting correto ou efeitos seguros.
Valide empacotamento/entrypoint somente quando parte da entrega. A construção local não autoriza publicar o pacote.
