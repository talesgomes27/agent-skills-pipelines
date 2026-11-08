"""Cria a tabela de pedidos."""


def upgrade(conn):
    conn.execute(
        "CREATE TABLE pedidos (id SERIAL PRIMARY KEY, cliente_id INTEGER NOT NULL,"
        " valor NUMERIC(12, 2) NOT NULL, criado_em TIMESTAMPTZ DEFAULT now())"
    )


def downgrade(conn):
    conn.execute("DROP TABLE pedidos")
