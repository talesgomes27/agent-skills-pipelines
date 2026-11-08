create table clientes (id serial primary key, nome text, cpf text, email text, plano text, criado_em timestamptz);
create table tickets (id serial primary key, cliente_id int references clientes(id), assunto text, mensagem text, status text, aberto_em timestamptz);
create table faturas (id serial primary key, cliente_id int references clientes(id), valor numeric, vencimento date, paga boolean);
