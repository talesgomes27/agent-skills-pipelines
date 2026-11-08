# Incidentes e segredo vazado

É incidente o defeito com efeito fora do desenvolvimento (usuários, dados reais, envios), o serviço ou job de produção usado por outros que parou e o segredo exposto; falha local, sem publicação nem envio, é bug. Na dúvida, pergunte se algo saiu do ambiente local. Num incidente, as paradas são o A2 de cada contenção fora do plano de recuperação já autorizado, envio, reprocessamento ou limpeza de histórico, e o A3 depois da verificação no destino; os gates RL-1 a RL-5 voltam na nova publicação. O conserto do código segue a correção de bug da `execution-pipeline`.

## Ordem

1. **Classificar.** Registre o que aconteceu, desde quando, quem e quantos foram afetados e se ainda está acontecendo. Separe fato observado de hipótese, com a origem de cada evidência. Dano em andamento a pessoas ou dados vem antes de qualquer outra tarefa. Num envio errado, confira se a mensagem expôs dado de uma pessoa a outra, como destinatário trocado ou cobrança com dados de terceiros: isso já é incidente com dados pessoais.
2. **Conter dentro do autorizado.** Pausar o agendamento, desligar a funcionalidade ou voltar ao deploy anterior pelo plano de recuperação já autorizado. Uma contenção fora desse plano é efeito externo. Mostre a ação, o alvo e como desfazer, e peça a autorização para o mínimo que interrompe o dano. Não apague dados, logs nem registros de envio: eles são a evidência.
3. **Preservar a evidência.** Guarde logs, IDs de execução, versão do artefato e horários, sem segredos e sem dados pessoais além do necessário.
4. **Comunicar.** Quem precisa saber, como a equipe, os afetados ou o cliente, é decisão do usuário. O agente redige a mensagem e não a envia: enviar é efeito com autorização própria. Incidente com dados pessoais segue a skill `personal-data`: comunicar a ANPD e os titulares cabe ao controlador, que tem essa obrigação quando há risco ou dano relevante ([LGPD, art. 48](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm), conferido em 07/11/2026).
5. **Corrigir pela causa.** Reproduza, escreva o teste que falha e corrija, como na `execution-pipeline`. Reprocessar ou reenviar só com escopo autorizado e com a idempotência conferida, para não repetir o envio errado.
6. **Verificar no destino.** O sintoma parou onde aconteceu, não só no ambiente local. Confira de novo depois de qualquer recuperação.
7. **Postmortem.** Escreva com a `writing-pipeline`, no tipo postmortem: linha do tempo, impacto, causa, o que ajudou, o que atrapalhou e ações com responsável e prazo, sem culpar pessoas.

## Segredo vazado

Apagar a linha não invalida um segredo que já saiu num commit, num push, num log de CI, numa imagem, num notebook renderizado ou no chat.

1. **Revogar ou desativar primeiro**, no painel do provedor. Quem revoga é o usuário, dono da conta; o agente diz onde e como, pela documentação oficial do provedor. Muitas vezes isso basta, e o histórico nem precisa ser reescrito.
2. **Trocar.** O usuário cria a credencial nova, com o menor escopo, e a guarda no cofre da plataforma ou da CI, nunca no chat. O agente ajusta o código para ler do cofre ou de variável de ambiente.
3. **Verificar uso indevido.** O usuário consulta os logs de uso e de cobrança do provedor no período em que o segredo ficou exposto; o agente lista o que olhar.
4. **Limpar o histórico, só depois de revogar e só se ainda valer a pena.** Reescrever o histórico remoto, com `git-filter-repo` e force push, troca os hashes, afeta clones, forks e PRs abertos, e exige autorização própria. Cópias em forks, clones e caches continuam com o segredo. Em repositório público, trate o segredo como comprometido mesmo depois da limpeza.
5. **Impedir a repetição.** `.gitignore`, o scanner de segredos que o projeto já usa ou um proposto com aceite, e checagem antes do commit.

Nunca mostre, repita nem teste o segredo vazado, nem para conferir se ele ainda funciona. Ao mostrar o diff da correção, mascare o valor removido.

Fonte: [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository), GitHub Docs, conferido em 07/11/2026.
