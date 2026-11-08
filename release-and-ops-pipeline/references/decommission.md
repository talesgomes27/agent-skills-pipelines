# Desligar um serviço

Leia quando o pedido é desligar, desativar ou apagar um serviço, app, job ou banco que já está em produção.

Desligar é efeito externo em cada passo, e apagar dados não tem volta. "Ninguém usa mais" e "pode apagar tudo" no pedido são a premissa a conferir, não a autorização: cada efeito pede A2 com o alvo e como desfazer.

## Antes de propor

1. **Confira o uso real.** Leia os logs de acesso, as métricas e as chamadas de outros sistemas do período recente. Aponte cada cliente que ainda acessa, inclusive outros serviços da própria empresa. Uso encontrado volta ao usuário antes de qualquer plano de desligamento.
2. **Liste o que é do serviço e o que depende dele.** Registro de DNS e domínio, job agendado, banco e volumes, segredos e variáveis de ambiente, certificados, monitores e alertas, integrações, licenças e a infraestrutura como código que o recria.
3. **Separe os dados que precisam ser guardados.** Dados com retenção legal ou contratual, ou com pessoas, seguem a `personal-data` e o dono dos dados: arquive antes de apagar, com o local e o prazo registrados.

## Plano em etapas

1. Avise os donos e os clientes encontrados, com a data; a mensagem é um envio e tem o seu A2.
2. Guarde a configuração e faça o backup dos dados, conferindo que ele restaura.
3. Com A2, bloqueie o acesso ou pare o serviço sem apagar nada, por um período de observação combinado, com o caminho de volta testado.
4. Observe erros e reclamações no período. Qualquer uso que aparecer interrompe o plano.
5. Só então remova DNS, agendamentos, monitores, segredos e recursos, e por último os dados, cada um com o seu A2 e, no mesmo pedido, a autorização de como desfazê-lo.

Registre o que foi removido, o backup e onde ficou, para quem precisar consultar depois.

## Fontes

Conferidas em 08/11/2026:

- AWS Well-Architected, COST04-BP02 Implement a decommissioning process: https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/cost_decomissioning_resources_implement_process.html (confirmar o uso, backup, bloquear o acesso por um período com reversão, depois remover DNS e monitores)
- Microsoft Cloud Adoption Framework, Decommission source workloads: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/migrate/decommission-source-workload (aprovação dos donos com critério e prazo de carência para reverter, arquivar dados com retenção, retirar monitores)
