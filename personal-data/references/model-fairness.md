# Viés de modelo sobre pessoas

Leia quando um modelo pontua, classifica ou ordena pessoas: churn, crédito, risco, triagem de currículos, prioridade de atendimento ou qualquer lista que decide quem recebe uma ação. O que segue é prática de medição; se o resultado tem consequência jurídica, a decisão é de quem responde pelos dados.

## O que a lei diz

- Um dos princípios do tratamento é a não discriminação: o tratamento não pode ter fins discriminatórios ilícitos ou abusivos (LGPD, art. 6, IX).
- O titular pode pedir revisão de decisão tomada só com base em tratamento automatizado que afete seus interesses, e o controlador fornece, quando pedido, informações claras sobre os critérios e os procedimentos da decisão, respeitados os segredos comercial e industrial (art. 20, caput e §1º). Se essas informações não forem dadas por causa do segredo, a autoridade nacional pode fazer auditoria para verificar aspectos discriminatórios (art. 20, §2º).

Fonte: [texto compilado da Lei 13.709/2018 no Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm), conferido em novembro de 2026.

## No plano

- Liste os grupos que importam para a decisão, como faixa etária, região, sexo ou renda, e diga de onde vem o atributo de cada pessoa. Atributo sensível (origem racial ou étnica, saúde, religião e os outros da lista da skill) só entra na avaliação com decisão do responsável pelos dados, e nunca como entrada do modelo sem essa decisão.
- Variável que substitui um atributo protegido, como CEP no lugar de renda ou de origem, também é avaliada: tirar a coluna do modelo não tira o viés.
- Escolha, com o usuário, a métrica que reflete o dano da decisão: taxa de seleção por grupo quando ser escolhido é o benefício ou o dano; erro por grupo (falsos positivos e falsos negativos) quando o problema é errar mais com alguns; calibração por grupo quando o score é lido como probabilidade. O plano diz por que a métrica escolhida reflete o dano daquela decisão.
- Defina antes de medir o limite de diferença entre grupos que bloqueia o uso e o tamanho mínimo de grupo para a comparação valer: no mínimo o de agregação da skill, que protege a privacidade, e o que o método pede para a diferença ser detectável, que costuma ser bem maior.

## Na avaliação e em produção

- Meça as métricas por grupo no mesmo conjunto de validação do modelo, com o número de pessoas de cada grupo. Grupo pequeno demais é relatado como sem conclusão, não como sem viés.
- Diferença acima do limite é achado: o relatório mostra o valor, o grupo e a decisão afetada, e o usuário decide se ajusta o modelo, muda o uso ou aceita a diferença com o motivo registrado.
- Num modelo em produção, como uma lista semanal, as mesmas métricas por grupo entram no monitoramento de cada execução; com retreino, também no critério de troca do modelo, como na referência de modelo em produção da `scheduled-automation`.
- A saída para quem decide diz que o score é estimativa e a quem pedir a revisão do art. 20. Esta skill exige que a revisão possa ser feita por uma pessoa, como diz o SKILL.md; a lei não o exige desde o veto do §3º, que o previa.
- Saídas desta avaliação mostram agregados por grupo, nunca pessoas.
