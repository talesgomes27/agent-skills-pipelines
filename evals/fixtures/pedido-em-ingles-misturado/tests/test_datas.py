from datetime import date
from etl.datas import ler_data


def test_iso():
    assert ler_data('2026-11-07') == date(2026, 11, 7)
