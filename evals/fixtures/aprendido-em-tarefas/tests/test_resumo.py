from resumo import total


def test_total(tmp_path):
    p = tmp_path / 'v.csv'
    p.write_text('data;valor\n2026-10-01;10.5\n2026-10-02;4.5\n', encoding='utf-8')
    assert total(p) == 15.0
