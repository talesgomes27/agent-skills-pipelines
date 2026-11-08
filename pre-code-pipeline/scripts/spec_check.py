#!/usr/bin/env python3
"""Confere a spec viva de um projeto, sem rede e só com a biblioteca padrão.

Saída 0: spec limpa. 1: problemas encontrados. 2: spec não encontrada, ilegível ou argumento inválido.
Formatos: native (docs/spec.md e docs/plan.md), speckit, kiro e openspec; auto detecta.
--stage a3: antes da entrega, requisito aprovado ou implementado sem evidência vira problema (só no formato
nativo; nos formatos de SDD a evidência não é conferida, e a saída diz isso).
"""
import argparse
import re
import sys
from pathlib import Path

ID = re.compile(r'^###\s+([A-Za-z]{1,3})-(\d+)\b')
VALID_ID = re.compile(r'^[RHNDQT]-\d{3}$')
FIELD = re.compile(r'^\s*(?:-\s*)?(?:\*\*)?([A-Za-zÀ-ÿ ]+?)(?::\*\*|\*\*:|:)\s*(.*)$')
STATES = {'proposto', 'aprovado', 'implementado', 'verificado', 'obsoleto'}
APPROVED = {'aprovado', 'implementado', 'verificado'}


def sections(text):
    """Blocos '### X-000 título' com os campos 'Nome: valor' (com ou sem '- ') abaixo.

    Subtítulos '####' continuam o bloco; linhas indentadas continuam o campo anterior.
    """
    blocks, current, last, fence = [], None, None, False
    for line in text.splitlines():
        if line.lstrip().startswith(('```', '~~~')):
            fence = not fence
            continue
        if fence:
            continue
        m = ID.match(line)
        if m:
            current = {'id': m.group(1) + '-' + m.group(2), 'campos': {}}
            blocks.append(current)
            last = None
        elif line.startswith('#') and not line.startswith('####'):
            current = None
        elif current is not None:
            f = FIELD.match(line)
            if f and not line.startswith(('  ', '\t')):
                last = f.group(1).strip().lower()
                current['campos'][last] = f.group(2).strip().strip('`').strip()
            elif last and line.startswith(('  ', '\t')) and line.strip():
                current['campos'][last] = (current['campos'][last] + ' ' + line.strip()).strip()
    return blocks


EXTS = ('py', 'r', 'R', 'qmd', 'rmd', 'Rmd', 'ipynb', 'md', 'sql', 'sh', 'go', 'java', 'kt', 'scala', 'js', 'ts',
        'tsx', 'jsx', 'csv', 'json', 'yaml', 'yml', 'toml', 'html', 'png', 'svg', 'pdf', 'txt', 'log', 'parquet')
# shortcut: caminho é token com '/' ou com uma extensão da lista; amplie EXTS se um projeto usar outra
PATH = re.compile(r'(?<![\w/.:-])((?:[\w.-]+/)+[\w.-]*\w|[\w-]+\.(?:%s))(?=::|#|[\s;,)]|$)' % '|'.join(EXTS))


def evidence_paths(value):
    """Arquivos citados na evidência; URLs são ignoradas, e '::teste' ou '#célula' cortados."""
    value = re.sub(r'https?://\S+', ' ', value)
    for m in PATH.finditer(value):
        yield m.group(1)


def check_native(root, stage):
    spec = root / 'docs/spec.md'
    if not spec.is_file():
        return None
    problems, info = [], []
    blocks = sections(read(spec))
    seen = {}
    for b in blocks:
        if not VALID_ID.match(b['id']):
            problems.append('%s: ID fora do padrão (letra R, H, N, D, Q ou T e três dígitos)' % b['id'])
        seen[b['id']] = seen.get(b['id'], 0) + 1
    problems += ['%s: ID repetido' % i for i, n in seen.items() if n > 1]
    reqs = [b for b in blocks if b['id'][0] in 'RH']
    if not reqs:
        problems.append('docs/spec.md: nenhum requisito (### R-001 ou ### H-001)')
    for b in reqs:
        estado = (b['campos'].get('estado', '').lower().split() or [''])[0].strip('.,;')
        b['estado'] = estado
        if estado not in STATES:
            problems.append('%s: estado ausente ou fora da lista (%s)' % (b['id'], ', '.join(sorted(STATES))))
        criterio = b['campos'].get('critério') or b['campos'].get('criterio') or b['campos'].get('critério de sucesso')
        if estado in APPROVED and not criterio:
            problems.append('%s: requisito %s sem critério' % (b['id'], estado))
        ev = b['campos'].get('evidência') or b['campos'].get('evidencia') or ''
        if stage == 'a3' and estado in ('aprovado', 'implementado'):
            if not list(evidence_paths(ev)):
                problems.append('%s: requisito %s sem evidência antes do A3' % (b['id'], estado))
            for p in evidence_paths(ev):
                if not (root / p).exists():
                    problems.append('%s: evidência cita arquivo que não existe: %s' % (b['id'], p))
        if estado == 'verificado':
            paths = list(evidence_paths(ev))
            if not paths:
                problems.append('%s: verificado sem evidência' % b['id'])
            for p in paths:
                if not (root / p).exists():
                    problems.append('%s: evidência cita arquivo que não existe: %s' % (b['id'], p))
    plan = root / 'docs/plan.md'
    if plan.is_file():
        known = {b['id'] for b in reqs}
        covered = set()
        for t in sections(read(plan)):
            if t['id'][0] != 'T':
                continue
            cited = re.findall(r'\b[RH]-\d{3}\b', t['campos'].get('requisitos', ''))
            if not cited:
                problems.append('%s: tarefa sem requisitos' % t['id'])
            for c in cited:
                if c not in known:
                    problems.append('%s: cita requisito que não existe: %s' % (t['id'], c))
                covered.add(c)
        for b in reqs:
            if b['estado'] == 'aprovado' and b['id'] not in covered:
                problems.append('%s: requisito aprovado sem tarefa no plano' % b['id'])
    info += ['questão aberta: %s' % b['id'] for b in blocks if b['id'][0] == 'Q']
    return problems, info


def read(path):
    return path.read_text(encoding='utf-8-sig')


def check_speckit(root, stage):
    specs = sorted(p for p in (root / 'specs').glob('*/spec.md')) if (root / 'specs').is_dir() else []
    if not specs or not (root / '.specify').is_dir():
        return None
    problems = []
    for spec in specs:
        text = read(spec)
        known = set(re.findall(r'\b(?:FR|SC)-\d{3}\b', text))
        stories = set(re.findall(r'User Story (\d+)', text))
        tasks = spec.parent / 'tasks.md'
        if tasks.is_file():
            ttext = read(tasks)
            for c in sorted(set(re.findall(r'\b(?:FR|SC)-\d{3}\b', ttext)) - known):
                problems.append('%s: tasks.md cita %s, que não existe na spec' % (spec.parent.name, c))
            for us in sorted(set(re.findall(r'\[US(\d+)\]', ttext)) - stories):
                problems.append('%s: tasks.md cita US%s, que não existe na spec' % (spec.parent.name, us))
    return problems, []


def check_kiro(root, stage):
    base = root / '.kiro'
    dirs = sorted({p.parent for p in base.rglob('requirements.md')}) if base.is_dir() else []
    if not dirs:
        return None
    # shortcut: só o trio de arquivos foi confirmado na documentação; a numeração dos requisitos não
    missing = ['%s: falta %s' % (d.relative_to(root), n) for d in dirs for n in ('design.md', 'tasks.md') if not (d / n).is_file()]
    # o Kiro cria design e tarefas por fase: o trio incompleto só é problema na entrega
    return (missing, []) if stage == 'a3' else ([], ['ainda em andamento: ' + m for m in missing])


def check_openspec(root, stage):
    base = root / 'openspec'
    if not any((base / d).is_dir() and any((base / d).rglob('*.md')) for d in ('specs', 'changes')):
        return None
    problems = []
    archive = base / 'changes' / 'archive'
    for spec in sorted(base.rglob('spec.md')):
        if archive in spec.parents:
            continue
        current, removed = None, False
        for line in read(spec).splitlines() + ['### ']:
            if line.startswith('## '):
                removed = 'REMOVED' in line
            if line.startswith('### '):
                if current and not current[1]:
                    problems.append('%s: requisito sem cenário: %s' % (spec.relative_to(root), current[0]))
                current = [line[4:].strip(), False] if line.startswith('### Requirement:') and not removed else None
            elif line.startswith('#### Scenario:') and current:
                current[1] = True
    changes = base / 'changes'
    info = []
    for change in sorted(p for p in changes.iterdir() if p.is_dir() and p.name != 'archive') if changes.is_dir() else []:
        for name in ('proposal.md', 'tasks.md'):
            if not (change / name).is_file():
                msg = 'openspec/changes/%s: falta %s' % (change.name, name)
                # como no Kiro, os arquivos da mudança nascem por fase: incompleto só é problema na entrega
                (problems if stage == 'a3' else info).append(msg if stage == 'a3' else 'ainda em andamento: ' + msg)
    return problems, info


CHECKS = {'speckit': check_speckit, 'kiro': check_kiro, 'openspec': check_openspec, 'native': check_native}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--format', choices=['auto'] + list(CHECKS), default='auto')
    parser.add_argument('--stage', choices=['plano', 'a3'], default='plano')
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 2
    if not args.root.is_dir():
        print('raiz não encontrada: %s' % args.root, file=sys.stderr)
        return 2
    order = list(CHECKS) if args.format == 'auto' else [args.format]
    try:
        found = [(n, r) for n, r in ((n, CHECKS[n](args.root, args.stage)) for n in order) if r is not None]
    except (OSError, UnicodeDecodeError) as e:
        print('não consegui ler a spec: %s' % e, file=sys.stderr)
        return 2
    if not found:
        print('nenhuma spec encontrada (%s)' % ', '.join(order), file=sys.stderr)
        return 2
    name, (problems, info) = found[0]
    print('formato: %s' % name)
    others = [n for n, _ in found[1:]]
    native = dict(found).get('native')
    if native and name != 'native':
        # a spec nativa nunca fica sem conferência só porque outro formato veio antes na detecção
        problems = problems + ['native: ' + p for p in native[0]]
        info = info + native[1]
        others.remove('native')
    if others:
        print('aviso: também há spec em %s; só %s foi conferido' % (', '.join(others), name))
    if args.stage == 'a3' and name != 'native':
        print('evidência não conferida no formato %s: liste a evidência de cada requisito no A3' % name)
    for p in problems:
        print('problema: %s' % p)
    for i in info:
        print(i)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
