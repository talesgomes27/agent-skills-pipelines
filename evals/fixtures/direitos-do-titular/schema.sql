create table clientes (id serial primary key, nome text, cpf text, email text, telefone text, criado_em timestamptz);
create table enderecos (id serial primary key, cliente_id int references clientes(id), logradouro text, cidade text, cep text);
create table pedidos (id serial primary key, cliente_id int references clientes(id), total numeric, criado_em timestamptz);
create table notas_fiscais (id serial primary key, pedido_id int references pedidos(id), chave_acesso text, cpf_destinatario text, emitida_em timestamptz);
create table logs_acesso (id bigserial primary key, cliente_id int, ip inet, user_agent text, em timestamptz);
create table marketing_optin (cliente_id int references clientes(id), canal text, aceito_em timestamptz);
