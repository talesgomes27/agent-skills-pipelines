---
name: scheduled-automation
description: "Use quando o trabalho envolve um job que roda sem ninguém olhando: script ou workflow agendado (cron, schedule do GitHub Actions, agendador de nuvem ou do servidor), ETL recorrente, bot que envia mensagens ou retreino periódico de modelo."
---

# Automações agendadas

Um job agendado roda sem ninguém olhando, então o erro dele aparece depois e às vezes se repete a cada execução. Esta skill dá o contrato que o job precisa ter antes de ser agendado. Ela informa as pipelines: gates, escopo e autorizações continuam os delas. Sem pipeline ativa, valem as mesmas regras: nenhum efeito externo, conta ou agendamento sem autorização do usuário. Num job pequeno e pessoal, cada item do contrato pode ter uma linha, na própria resposta.

## Contrato do job

Responda por escrito antes de implementar, no plano da `pre-code-pipeline` ou na tarefa da `execution-pipeline`:

1. **Gatilho.** Agendador, horário e fuso; o que acontece com atraso, execução perdida e duas execuções ao mesmo tempo. Inclua o disparo manual do mesmo job, para testar e reprocessar. Escolha o agendador pelo que o job precisa: GitHub Actions serve a job curto, sem disco persistente e com dados que podem passar pelo GitHub; servidor próprio ou agendador de nuvem servem quando o job precisa de disco, rede privada ou dados que não devem sair do seu ambiente.
2. **Janela.** De onde vêm os dados, que janela cada execução processa (o dia anterior, os arquivos novos desde a última marca) e como reprocessar uma janela passada.
3. **Estado.** Confira antes se ele precisa existir, porque às vezes a fonte ou o destino já guardam o histórico. Depois defina o que sobrevive entre execuções (banco, marca da última execução, arquivos já processados) e onde fica. Runner de CI começa vazio a cada execução; veja [GitHub Actions](references/github-actions-schedule.md).
4. **Idempotência.** A chave que impede processar duas vezes, como id do arquivo com data de modificação, ou data de referência com fonte, e como a escrita a usa: upsert, merge ou troca da partição. Vale também para efeito externo: a reexecução não reenvia a mensagem nem cobra de novo, porque o job registra o que já enviou. Se o envio dá certo e a gravação do estado falha, a reexecução reenvia: registre o envio no mesmo passo que confirma a execução, ou documente que um reenvio raro é aceitável.
5. **Falhas.** Quantas novas tentativas, com espera crescente, para quais erros (rede, 429, 5xx), e quais falham na hora (credencial, esquema). Na falha parcial, decida se uma planilha ruim entre dez para tudo, é pulada com aviso ou vai para quarentena. Mudança de esquema na fonte falha de forma explícita, com o arquivo e a coluna no aviso.
6. **Segredos.** Conta de serviço ou token com o menor escopo que serve, no cofre do agendador, fora do código, do log e do estado versionado. O plano diz quem cria a credencial e onde: o agente não cria contas nem recebe segredo pelo chat. No Google Drive, uma conta de serviço com escopo só de leitura, e a pasta compartilhada com ela, evita depender de um token pessoal que pode expirar ou ser revogado.
7. **Saídas e resumo.** O que o job grava e envia, em que formato, e o resumo de cada execução: o que leu, gravou, pulou e enviou. Dados de pessoas no resumo, nos logs ou numa lista enviada seguem a skill `personal-data`.
8. **Alerta.** Quem é avisado de uma falha, por um canal que não dependa do componente que falhou. Um job que manda resumo pelo Telegram não avisa pelo Telegram que o Telegram falhou.
9. **Execução que não rodou.** Agendador que atrasa, desativa ou descarta uma execução não gera erro. Para job importante, use um sinal de vida externo: cada execução bem-sucedida avisa um monitor de heartbeat, com conta criada pelo usuário, ou grava uma marca que outro processo confere, e a ausência dispara o alerta.
10. **Custos e cotas.** Minutos de CI, cotas das APIs, limite de tamanho de mensagem e volume de dados por execução.

## Dry-run e testes

- O dry-run lê as entradas reais, com credencial só de leitura quando o plano prevê, e mostra o que gravaria e enviaria. Ele não grava estado, não envia mensagem e não avança a marca de execução; a mensagem que seria enviada aparece na saída do job. O plano diz o que ele suprime.
- Teste a lógica com fixtures pequenas: o arquivo repetido, a planilha com esquema mudado e a falha no meio do lote. Para a idempotência, rode duas vezes sobre a mesma entrada; o resultado e os envios ficam iguais.
- Teste a integração com os recursos de teste do plano, como pasta, banco e chat de teste. No recurso de teste, gravar e enviar seguem a regra da `execution-pipeline` para o recurso que o plano nomeia. No destino real, a primeira execução vem com a autorização de ativar.

## Ativar, acompanhar e desligar

- Ativar o agendamento é uma publicação e segue a `release-and-ops-pipeline`. Antes, rode uma vez pelo disparo manual, de preferência em dry-run, e confira saída, estado e alerta. No GitHub Actions, o disparo manual também exige o workflow na branch padrão, e o merge de um workflow com `schedule` já ativa o agendamento. Para rodar antes de ativar, faça o merge só com `workflow_dispatch`, rode e confira, e acrescente o `schedule` depois, como a publicação.
- A autorização de ativar cobre os efeitos recorrentes que o plano descreve, como gravar no banco, enviar o resumo e republicar o relatório. Efeito ou destino novo pede outra autorização.
- Depois, confira a primeira execução no horário previsto, no fuso do agendador. Se ela está distante, o usuário pode aceitar pela execução manual, e a agendada fica como pendência com o horário esperado e como conferir.
- Deixe escrito como pausar o agendamento sem apagar o estado e como voltar à versão anterior do job.

## Retreino de modelo

Retreino é um job sobre um modelo de análise. Siga também [retreino agendado](references/model-retraining.md).

## Servidor próprio

Em cron ou systemd timer:

- Declare o fuso, porque o cron usa o do sistema.
- Declare o ambiente completo (PATH, diretório de trabalho, variáveis), porque o cron não carrega o perfil do usuário.
- Evite sobreposição com uma trava de arquivo, como `flock`.
- Prefira systemd timer com `Persistent=true` quando a execução perdida precisa rodar assim que a máquina volta.
- Mantenha os logs com rotação.

## Especialistas

Carregue só para uma lacuna concreta, sem mudar gates nem autorizações:

- `dagster-expert` (dagster-io/skills) quando o projeto usa Dagster;
- as skills do dltHub (dlt-hub/dlthub-ai-workbench) quando a ingestão usa dlt, por exemplo para carga incremental;
- `github-actions-hardening` para revisar a segurança do workflow e `github-actions-efficiency` para custo de minutos, ambas de github/awesome-copilot.

Sem a especialista, siga a documentação oficial da versão em uso.
