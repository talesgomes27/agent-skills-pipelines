import requests


def cotacao(moeda, sessao=None):
    s = sessao or requests.Session()
    r = s.get(f'https://api.exemplo.invalid/cotacao/{moeda}', timeout=10)
    r.raise_for_status()
    return r.json()['valor']
