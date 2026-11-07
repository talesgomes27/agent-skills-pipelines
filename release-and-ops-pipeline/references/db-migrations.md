# Migrações de banco em produção

Mudança de esquema ou de dados num banco com dados reais é uma publicação com risco de perda. Ela entra no plano da release com autorização própria, separada da autorização do deploy da aplicação.

## Antes

- Use a ferramenta de migração do projeto (Alembic, Django, Prisma, Flyway ou equivalente) e revise o SQL que ela gera.
- Faça backup e teste a restauração antes da mudança: backup que nunca foi restaurado não é recuperação.
- Ensaie a migração numa cópia com volume parecido e meça duração e travas.
- Defina a janela, quem é avisado e o critério para abortar.
- O plano diz quem roda o comando contra produção, de onde e com qual credencial; a credencial fica com o usuário ou no cofre da CI, fora do chat.
- Cópia de produção para ensaio carrega os mesmos dados pessoais: guarde-a com a mesma proteção e apague-a depois, ou use uma cópia com esses campos mascarados.

## Mudança em etapas compatíveis

Divida a mudança para que a versão atual e a nova da aplicação funcionem durante a transição:

1. **Expandir.** Crie a tabela ou coluna nova sem quebrar a antiga: a coluna nova aceita nulo ou tem default, e nada é renomeado nem apagado.
2. **Publicar o código** que grava no novo, e no antigo quando preciso, e lê dos dois.
3. **Migrar os dados existentes** em lotes, com contagem antes e depois.
4. **Contrair** só numa release seguinte, quando nada mais lê o antigo. Só então remova coluna ou tabela.

Uma tabela nova que nada usa ainda é o caso simples: a etapa 1 basta.

## Travas e tempo

- Mudança que reescreve a tabela ou cria índice pode travar leituras e escritas. No Postgres, `CREATE INDEX CONCURRENTLY` evita bloquear escritas, mas não roda dentro de uma transação, e `lock_timeout` faz a migração desistir em vez de esperar sem limite.
- Confira na documentação da versão do banco quais operações reescrevem a tabela.

Na release, a migração de expandir roda antes do deploy do código que depende dela, e a de contrair só depois que nenhuma versão no ar usa o antigo.

## Depois

- Confira esquema, constraints, contagens e uma jornada da aplicação que use a mudança. Uma jornada que grava, como um pedido de teste, segue a regra de smoke da release: escopo, dados de teste e limpeza autorizados.
- Mantenha o backup pelo prazo que o plano definiu.

## Voltar

- Aplicação e esquema voltam separados: reverter o deploy não desfaz a migração.
- A migração reversa só vale se não perder dados gravados desde a mudança. Se perder, restaurar o backup descarta essas escritas, e só o usuário decide fazer isso.
- Com a mudança em etapas, voltar costuma ser só voltar o código, porque o esquema antigo ainda existe.
