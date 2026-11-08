"""Agrega os resultados de evals/results/ numa tabela Markdown.

Uso: python evals/report.py [--versao X.Y.Z]
Uma linha por versão, nível, modo, host e modelo; resultado sem modo é do assistido,
o padrão antes da 4.0.0. Uma combinação com falha em
checkpoint nao_deve aparece como "não recomendada". Só biblioteca padrão.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

EVALS = Path(__file__).resolve().parent


def nao_deve_ids():
    try:
        import yaml
    except ImportError:
        yaml = None
    ids = {}
    for path in (EVALS / 'scenarios').glob('*.yaml'):
        text = path.read_text(encoding='utf-8')
        if yaml:
            checkpoints = yaml.safe_load(text).get('checkpoints', [])
            found = {c['id'] for c in checkpoints if c.get('tipo') == 'nao_deve'}
        else:  # reserva sem PyYAML, para o formato gerado por yaml.safe_dump
            found, current = set(), None
            for line in text.splitlines():
                s = line.split('#', 1)[0].strip().strip('- ')
                if s.startswith('id:'):
                    current = s.split(':', 1)[1].strip().strip('\'"')
                elif s.startswith('tipo:') and current and s.split(':', 1)[1].strip().strip('\'"') == 'nao_deve':
                    found.add(current)
        if found:
            ids[path.stem] = found
    return ids


def rows(versao=None):
    proibidos = nao_deve_ids()
    agg = defaultdict(lambda: {'deve': [0, 0], 'nao_deve_falhas': 0, 'cenarios': 0, 'paradas': {}, 'data': ''})
    for path in sorted((EVALS / 'results').rglob('*.json')):
        if path.name.startswith('triggers-'):
            continue
        d = json.loads(path.read_text(encoding='utf-8'))
        if versao and d['versao'] != versao:
            continue
        a = agg[(d['versao'], d['nivel'], d.get('modo', 'assistido'), d['host'], d['modelo'])]
        a['cenarios'] += 1
        if 'paradas' in d:
            a['paradas'][d['cenario']] = d['paradas']
        a['data'] = max(a['data'], d.get('data', ''))
        for c in d.get('checkpoints', []):
            if c['id'] in proibidos.get(d['cenario'], set()):
                a['nao_deve_falhas'] += c['resultado'] == 'falhou'
            else:
                a['deve'][1] += 1
                a['deve'][0] += c['resultado'] == 'passou'
    return agg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--versao')
    agg = rows(parser.parse_args().versao)
    print('| Versão | Nível | Modo | Host | Modelo | Cenários | "deve" aprovados | Falhas "nao_deve" | Paradas no Dashboard | Data | Situação |')
    print('|---|---|---|---|---|---|---|---|---|---|---|')
    for (versao, nivel, modo, host, modelo), a in sorted(agg.items()):
        situacao = 'não recomendada' if a['nao_deve_falhas'] else 'ok'
        print('| %s | %s | %s | %s | %s | %d | %d de %d | %d | %s | %s | %s |' % (
            versao, nivel, modo, host, modelo, a['cenarios'], a['deve'][0], a['deve'][1],
            a['nao_deve_falhas'], a['paradas'].get('dashboard-streamlit', '—'), a['data'], situacao))


if __name__ == '__main__':
    main()
