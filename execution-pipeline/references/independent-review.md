# Revisão independente

Uma revisão feita por um agente que não viu o trabalho, antes do A3. Quem escreveu o código revisa com os mesmos pontos cegos e tende a confirmar as próprias decisões, por isso a revisão do autor nunca conta como independente.

## Quando

- Esforço rigoroso: obrigatória antes do A3.
- Esforço padrão: opcional, oferecida ao usuário quando a entrega toca segurança, dados de pessoas ou interface que outro sistema usa.
- A mesma revisão serve à AU-5 da auditoria com execução e, quando o risco pede, a uma segunda olhada no saneamento da release.

## Quem revisa

- No Claude Code, o subagente `diff-reviewer` do plugin da `execution-pipeline`, que só lê por instrução: ele tem Bash, e a proteção mecânica são as regras `ask` e `deny` do guia de instalação.
- No Claude Code sem o plugin, com as skills instaladas pelo `skills.py`, não há `diff-reviewer`: use um subagente novo, com o roteiro abaixo, só ferramentas de leitura e nada da conversa.
- Nos outros hosts, uma sessão nova do agente, com o roteiro abaixo e só ferramentas de leitura.
- Revisor humano, quando o usuário preferir. O formato da resposta é o mesmo.

## O que o revisor recebe e o que não recebe

| Recebe | Não recebe |
|---|---|
| Os requisitos aprovados e os critérios: a spec, ou o plano aprovado com os critérios de aceite | O raciocínio e a conversa de quem implementou |
| O diff da entrega, com a base | Resumos do autor sobre o que "já está certo" |
| As saídas dos checks, com comando e resultado | Permissão de escrita no código |
| O bloco de handoff | Autorização para qualquer efeito externo |

O revisor só lê: ler, buscar e listar arquivos e o histórico do Git, tratando as mensagens de commit como afirmações do autor a conferir. Ele roda testes só se o plano aprovado já autorizou, no mesmo ambiente de teste; no Claude Code, o `diff-reviewer` não roda testes, e os checks vêm do autor.

## Roteiro para o revisor

```text
Você revisa uma entrega que não escreveu. Leia os requisitos aprovados, o
diff, as saídas dos checks e o bloco de handoff que vêm com este pedido.
Não edite nada e não faça efeito externo. Confira, para cada requisito, se o
diff o atende e se há evidência (teste, saída ou check) que prove isso.
Procure defeitos de comportamento, testes fracos ou sem asserção, passos de
segurança ou de recuperação que o plano exigia e faltam, segredos e dados
pessoais, e documentação que não bate com o código.
```

## O que ele devolve

1. A tabela de achados no formato da auditoria: `ID | Linha / Arquivo | Severidade | Diagnóstico Original | Sugestão de Refatoração | Racional Técnico`, com a severidade de P0 a P3 da matriz de triagem da `audit-and-refactoring-pipeline`.
2. Um veredito por requisito aprovado: atendido, não atendido ou sem evidência.
3. O que ele não leu ou não pôde conferir.

## Regras

- Achado P0 ou P1 impede o A3: o autor corrige, ou justifica por escrito, e o usuário decide.
- O autor não edita o relatório do revisor. O relatório vai anexado ao A3 como está.
- Depois de uma correção, a revisão roda de novo, com um revisor que não viu a rodada anterior quando o host permite.
- A revisão não substitui os checks nem o aceite do usuário.
