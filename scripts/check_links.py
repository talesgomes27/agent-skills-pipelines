"""Confere os links externos das skills e da documentação.

Uso: python scripts/check_links.py [--timeout 15]
Sai com 1 quando algum link responde 404 ou 410 ou o domínio não resolve.
Respostas 401, 403 e 429, conexão recusada e tempo esgotado são comuns em
sites que recusam robôs e só geram aviso.
"""
import argparse
import re
import socket
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
URL = re.compile(r'https?://[^\s\]>"\'`]+')
SKIP_HOSTS = re.compile(r'^https?://(localhost|127\.0\.0\.1|([^/]*\.)?example\.(com|org|net))(?=[:/]|$)')
SOFT = {401, 403, 405, 429}


def sources():
    yield from REPO.glob('*/SKILL.md')
    yield from REPO.glob('*/references/**/*.md')
    yield from (REPO / 'docs').rglob('*.md')
    yield REPO / 'README.md'


def extract(text):
    out = []
    for url in URL.findall(text):
        url = url.rstrip('.,;:')
        while url.endswith(')') and url.count(')') > url.count('('):
            url = url[:-1].rstrip('.,;:')
        if not SKIP_HOSTS.match(url):
            out.append(url)
    return out


def urls():
    found = {}
    for path in sources():
        for url in extract(path.read_text(encoding='utf-8')):
            found.setdefault(url, path.relative_to(REPO))
    return found


def status(url, timeout):
    headers = {'User-Agent': 'agent-skills-pipelines-link-check'}
    for method in ('HEAD', 'GET'):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers, method=method), timeout=timeout) as r:
                return r.status
        except urllib.error.HTTPError as exc:
            if method == 'HEAD' and exc.code in (403, 404, 405):
                continue
            return exc.code
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if method == 'HEAD':
                continue
            reason = getattr(exc, 'reason', exc)
            return 'dns' if isinstance(reason, socket.gaierror) else 'rede: ' + str(reason)
    return 'sem resposta'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout', type=float, default=15)
    args = parser.parse_args()
    broken = 0
    for url, where in sorted(urls().items()):
        code = status(url, args.timeout)
        if isinstance(code, int) and code < 400:
            continue
        soft = code in SOFT or (isinstance(code, str) and code.startswith('rede'))
        broken += not soft
        print(('AVISO' if soft else 'QUEBRADO'), code, url, '(' + str(where) + ')')
    print(str(broken) + ' link(s) quebrado(s)')
    return 1 if broken else 0


if __name__ == '__main__':
    sys.exit(main())
