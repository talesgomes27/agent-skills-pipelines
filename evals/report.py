"""Agrega os resultados de evals/results/ em duas tabelas Markdown: cenários e gatilhos.

Uso: python evals/report.py [--versao X.Y.Z]
Cenários: uma linha por versão, nível, modo, host, destino e modelo; resultado sem modo é do assistido,
o padrão antes da 4.0.0. Os checkpoints "deve" e "nao_deve" aparecem como passou/falhou/indeterminado.
Situação: "não recomendada" com falha em nao_deve; "sem evidência" com nao_deve indeterminado ou nenhum
nao_deve julgado; "parcial" com falha em deve; "ok" no resto. Indeterminado em deve não é falha.
Gatilhos: acerto é "ativou" em deve e ambiguo_deve, e qualquer coisa menos "ativou" em nao_deve.
Só biblioteca padrão; o PyYAML é usado quando existe.
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

EVALS = Path(__file__).resolve().parent


def _yaml():
    try:
        import yaml
        return yaml
    except ImportError:
        return None


def nao_deve_ids():
    yaml = _yaml()
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


def gatilhos_esperados(texto_sem_yaml=None):
    """id -> esperado, do triggers.yaml. Com texto_sem_yaml, usa a reserva sem PyYAML."""
    yaml = None if texto_sem_yaml is not None else _yaml()
    text = texto_sem_yaml if texto_sem_yaml is not None else (EVALS / 'triggers.yaml').read_text(encoding='utf-8')
    if yaml:
        return {t['id']: t['esperado'] for t in yaml.safe_load(text)}
    out, current = {}, None
    for line in text.splitlines():
        s = line.split('#', 1)[0].strip()
        if s.startswith('- id:'):
            current = s.split(':', 1)[1].strip().strip('\'"')
        elif s.startswith('esperado:') and current:
            out[current] = s.split(':', 1)[1].strip().strip('\'"')
    return out


def rows(versao=None, root=None, proibidos=None):
    proibidos = nao_deve_ids() if proibidos is None else proibidos
    agg = defaultdict(lambda: {'deve': Counter(), 'nao_deve': Counter(), 'cenarios': 0, 'paradas': {}, 'data': ''})
    for path in sorted((root or EVALS / 'results').rglob('*.json')):
        if path.name.startswith('triggers-'):
            continue
        d = json.loads(path.read_text(encoding='utf-8'))
        if versao and d['versao'] != versao:
            continue
        a = agg[(d['versao'], d['nivel'], d.get('modo', 'assistido'), d['host'], d.get('destino', ''), d['modelo'])]
        a['cenarios'] += 1
        if 'paradas' in d:
            a['paradas'][d['cenario']] = d['paradas']
        a['data'] = max(a['data'], d.get('data', ''))
        for c in d.get('checkpoints', []):
            tipo = 'nao_deve' if c['id'] in proibidos.get(d['cenario'], set()) else 'deve'
            a[tipo][c['resultado']] += 1
    return agg


def situacao(a):
    if a['nao_deve']['falhou']:
        return 'não recomendada'
    if a['nao_deve']['indeterminado'] or not a['nao_deve']['passou']:
        return 'sem evidência'
    if a['deve']['falhou']:
        return 'parcial'
    return 'ok'


def trigger_rows(versao=None, root=None, gatilhos=None):
    gatilhos = gatilhos_esperados() if gatilhos is None else gatilhos
    agg = {}
    for path in sorted((root or EVALS / 'results').rglob('triggers-*.json')):
        d = json.loads(path.read_text(encoding='utf-8'))
        if versao and d['versao'] != versao:
            continue
        a = agg.setdefault((d['versao'], d['nivel'], d['host'], d.get('destino', ''), d['modelo']),
                           {'certos': 0, 'total': 0, 'erros_deve': 0, 'ativou_nao_deve': 0, 'ignorados': 0, 'data': ''})
        a['data'] = max(a['data'], d.get('data', ''))
        for r in d['resultados']:
            esperado = gatilhos.get(r['id'])
            if esperado is None:  # id que saiu do triggers.yaml: sem expectativa, não conta
                a['ignorados'] += 1
                continue
            a['total'] += 1
            if esperado == 'nao_deve':
                certo = r['observado'] != 'ativou'
                a['ativou_nao_deve'] += not certo
            else:
                certo = r['observado'] == 'ativou'
                a['erros_deve'] += not certo
            a['certos'] += certo
    return agg


def _pfi(c):
    return '%d/%d/%d' % (c['passou'], c['falhou'], c['indeterminado'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--versao')
    versao = parser.parse_args().versao
    print('| Versão | Nível | Modo | Host | Destino | Modelo | Cenários | "deve" passou/falhou/indet. | "nao_deve" passou/falhou/indet. | Paradas no Dashboard | Data | Situação |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for (v, nivel, modo, host, destino, modelo), a in sorted(rows(versao).items()):
        print('| %s | %s | %s | %s | %s | %s | %d | %s | %s | %s | %s | %s |' % (
            v, nivel, modo, host, destino or '—', modelo, a['cenarios'], _pfi(a['deve']), _pfi(a['nao_deve']),
            a['paradas'].get('dashboard-streamlit', '—'), a['data'], situacao(a)))
    print()
    print('| Versão | Nível | Host | Destino | Modelo | Gatilhos certos | Erros em "deve" | Ativou em "nao_deve" | Data |')
    print('|---|---|---|---|---|---|---|---|---|')
    ignorados = 0
    for (v, nivel, host, destino, modelo), a in sorted(trigger_rows(versao).items()):
        ignorados += a['ignorados']
        print('| %s | %s | %s | %s | %s | %d de %d | %d | %d | %s |' % (
            v, nivel, host, destino or '—', modelo, a['certos'], a['total'], a['erros_deve'], a['ativou_nao_deve'], a['data']))
    if ignorados:
        print('%d resultados de gatilho com id fora do triggers.yaml atual, ignorados' % ignorados, file=sys.stderr)


if __name__ == '__main__':
    main()
