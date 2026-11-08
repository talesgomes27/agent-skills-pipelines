import duckdb
from pathlib import Path


def test_consulta_roda():
    con = duckdb.connect()
    con.execute(Path("tests/esquema.sql").read_text())
    sql = Path("sql/receita_por_regiao.sql").read_text().replace(":inicio", "$inicio").replace(":fim", "$fim")
    con.execute(sql, {"inicio": "2026-10-01", "fim": "2026-11-01"}).fetchall()
