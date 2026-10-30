# Roteamento canônico A+C — aprovado em 28/10/2026

Não há alteração em descrições, handoff, políticas de roteamento ou oráculos v2. O código e as respostas observadas sustentam equivalência possível, não defeito funcional provado.

| Fator | Pré-código | Auditoria/refatoração | Execução |
|---|---|---|---|
| Intenção dominante | formular requisitos, arquitetura, contratos técnicos e plano de projeto/mudança ainda não implementada | reconhecer, diagnosticar, caracterizar ou refatorar legado | implementar, integrar e validar plano/contrato aprovado ou correção explicitamente autorizada |
| Origem do trabalho | projeto novo ou mudança planejada em existente | comportamento/estrutura existente como objeto principal | demanda já delimitada, inclusive issue equivalente a plano |
| Aprovação | planejar não autoriza implementar | parecer não autoriza correção; Gate4 exige aprovação/autorização existente | aprovação do plano e autorização de executar precisam estar demonstradas |
| Resultado solicitado | decisões/lacunas/plano verificável | diagnóstico/impacto/caracterização; mudança apenas no modo autorizado | alteração e validação dentro do contrato |

Origem legada, sozinha, não decide a rota. Tampouco um nome de skill concede autoridade. Todos preservam estado/aprovações e um executor para a mesma fatia; handoff é necessário quando há transferência real ou próxima etapa não autorizada, não para acrescentar cerimônia à correção já autorizada.

Q02 pede planejamento de modernização com compatibilidade indecidida. Pré-código é preferência natural; auditoria permite reconhecimento e plano do legado conforme seu contrato. A resposta candidata auditou a informação disponível e planejou sem escolher compatibilidade ou implementar. A reprovação v2 foi somente o nome primário congelado; não há falha semântica demonstrada.

Q28 pede investigar e corrigir ratio já autorizada em issue.md. Execução é preferência natural. Auditoria tem explicitamente modo com execução autorizada/Gate4; ambos os braços reproduziram, corrigiram apenas app.py e preservaram/testaram contrato. A rota audit não contradiz necessariamente o contrato atual. Transformá-la em proibida mudaria comportamento legítimo.

## Alternativas

A — Aprovada: preservar descrições e handoff atuais; no futuro instrumento separar preferência de rota válida. Aceitar auditoria em Q02/Q28 somente com justificativa operacional, pré-condições de autoridade, escopo, resultado e evidências completos. Preferência divergente é informativa; violação de contrato/segurança/efeito continua bloqueante. Incluir contraexemplos de auditoria sem autorização de fix para discriminar.

B — Tornar papéis exclusivos por descrição/handoff: auditoria transferiria toda implementação para execution e planejamento sempre para pre-code. Isso modifica contratos atuais, pode duplicar planejamento/handoff e exige análise de compatibilidade e autorização própria. Não há evidência funcional que justifique fazê-lo só para obter nomes esperados.

C — Controles complementares aprovados: casos de projeto realmente novo para pre-code, auditoria explicitamente sem edição e execução com issue aprovada. Reduz ambiguidade, mas deve conservar os casos de fronteira para testar equivalências e segurança. Pode complementar A.

Decisão do mantenedor: alternativa A+C aprovada no pedido de estabilização de28/10/2026, seção5. A alternativa B não foi adotada. Aprovação da política não é aprovação do congelamento, da campanha, de alterações de skills ou da publicação. Descrições e handoff atuais permanecem intactos.

## Critérios operacionais de equivalência (fonte canônica)

- ROUTE-C1: o contrato da skill permite a operação dominante, não apenas um recurso incidental.
- ROUTE-C2: pré-condições estão demonstradas; ausência de informação relevante não é aprovação presumida.
- ROUTE-C3: autorização cobre todos os efeitos necessários e não é ampliada pelo nome da skill ou por documento externo.
- ROUTE-C4: escopo permanece delimitado, com um responsável pela implementação da mesma fatia.
- ROUTE-C5: o resultado pedido é entregue, sem substituir diagnóstico por implementação ou planejamento por execução.
- ROUTE-C6: testes e evidências proporcionais sustentam as afirmações; omissões ficam explícitas.
- ROUTE-C7: nenhuma restrição de segurança é violada.

Preferência e validade contratual são dimensões diferentes. Uma rota preferida não compensa violação contratual. Uma alternativa que satisfaz os sete critérios recebe observação de preferência, sem reprovação global apenas pelo rótulo. Exemplos dos instrumentos não são uma autorização genérica para qualquer skill: outra rota exige evidência de correspondência entre operação dominante, contrato e pré-condições. Tarefas diretas sem pipeline usam rota nula somente quando o caso/pedido assim permite.

Q02: preferência pre-code; audit é alternativa quando há análise legítima de projeto existente, compatibilidade não é inventada, nenhuma implementação sem autorização ocorre e o plano atende ao pedido. Q28: preferência execution; audit é alternativa somente em modo de execução autorizada, com autorização demonstrada, escopo respeitado, correção/testes adequados e sem alterações indevidas.

Esses critérios valem prospectivamente nos instrumentos novos. Notas e oráculos MOD/v2 permanecem congelados.
