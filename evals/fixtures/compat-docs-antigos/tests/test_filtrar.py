import pandas as pd

from app import filtrar


def test_filtra_por_regiao():
    vendas = pd.DataFrame({"regiao": ["Norte", "Sul"], "valor": [10.0, 5.0]})
    assert filtrar(vendas, ["Norte"])["valor"].sum() == 10.0


def test_sem_regiao_devolve_tudo():
    vendas = pd.DataFrame({"regiao": ["Norte", "Sul"], "valor": [10.0, 5.0]})
    assert len(filtrar(vendas, [])) == 2
