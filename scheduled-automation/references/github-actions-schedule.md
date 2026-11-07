# GitHub Actions como agendador

Os detalhes valem para a documentação do GitHub de novembro de 2026. Confira a página antes de depender de um limite.

## Agendamento

- O `schedule` usa cron em UTC por padrão, e a chave `timezone` aceita um fuso IANA. Em fuso com horário de verão, o horário que não existe avança para o próximo válido.

  ```yaml
  on:
    schedule:
      - cron: '17 7 * * *'
        timezone: 'America/Sao_Paulo'
    workflow_dispatch:
  ```

- O intervalo mínimo é de 5 minutos. A execução pode atrasar com carga alta, principalmente no início de cada hora, e com carga suficiente pode ser descartada. Agende fora da hora cheia e não dependa do minuto exato.
- O agendamento só vale na branch padrão: roda no último commit dela e só se o arquivo do workflow existir lá. Workflow numa branch de feature não agenda nada até o merge.
- Em repositório público, o agendamento é desativado depois de 60 dias sem atividade no repositório, e num fork público ele já começa desativado. A documentação não diz o mesmo de repositório privado. Reative pela aba Actions ou com `gh workflow enable`. Só o sinal de vida externo da skill avisa desse caso.
- O aviso de falha do próprio GitHub vai para quem alterou por último a linha do cron.
- `workflow_dispatch` dá o disparo manual e aceita inputs, como `dry_run` e a data a reprocessar. Ele também só funciona com o arquivo do workflow na branch padrão; depois da primeira execução, a API e a CLI podem dispará-lo em outra branch ou tag. Como o merge de um workflow com `schedule` já ativa o agendamento, para rodar antes de ativar faça o merge só com `workflow_dispatch` e acrescente o `schedule` depois.

## Concorrência

`concurrency` com um grupo fixo e `cancel-in-progress: false` impede que duas execuções mexam no mesmo estado ao mesmo tempo. A nova execução espera como `pending`, mas só uma pode esperar: se chega outra, a que esperava é cancelada. Num job diário isso quase nunca pesa; num job frequente, a reexecução precisa cobrir a janela perdida.

## Estado entre execuções

O runner começa vazio a cada execução.

| Onde | Serve para | Cuidado |
|---|---|---|
| Commit no próprio repositório | Estado pequeno, como a marca da última execução | Exige `permissions: contents: write`; dado sensível entra no histórico para sempre; dois jobs podem conflitar no push; a proteção da branch pode recusar o push do job |
| Cache (`actions/cache`) | Acelerar dependências | Entrada sem acesso há mais de 7 dias é removida, o limite padrão é 10 GB por repositório e o conteúdo de uma chave não muda; não serve como estado |
| Artifact | Histórico e auditoria de cada execução | Expira pela retenção do repositório, e baixar o de outra execução exige o ID dela |
| Banco ou bucket externo | Estado de verdade, como um SQLite consolidado ou um banco gerenciado | Credencial no cofre, backup e custo |

Um SQLite que cresce a cada execução fica melhor fora do runner, num bucket ou trocado por banco gerenciado. Commitar o banco binário no Git aumenta o histórico a cada execução e expõe os dados a quem lê o repositório.

## Segredos e permissões

- Guarde os segredos em Settings → Secrets and variables → Actions, ou num environment com regras de proteção. O log mascara o valor exato, mas não um valor derivado dele, como o segredo decodificado ou recortado.
- Declare `permissions` mínimas no workflow em vez de depender do padrão do `GITHUB_TOKEN`.
- Eventos causados pelo `GITHUB_TOKEN` não criam nova execução de workflow, exceto `workflow_dispatch` e `repository_dispatch`. Por isso o commit de estado feito pelo job não dispara um laço.

Fontes: [eventos e schedule](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows), [desativar e reativar workflows](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows), [cache de dependências](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching), [GITHUB_TOKEN](https://docs.github.com/en/actions/tutorials/authenticate-with-github_token).
