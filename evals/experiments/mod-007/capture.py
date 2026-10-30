#!/usr/bin/env python3
"""Experiment-only read journal and active-phase wall time; no native token/tool telemetry."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import time


def capture(root, case, phase, action, paths=()):
    if any(not re.fullmatch(r'[A-Za-z0-9_-]+', value) for value in (case, phase)):
        raise ValueError('Invalid case/phase')
    root = root.resolve(strict=True)
    journal = root / '.capture' / f'{case}-{phase}.jsonl'
    journal.resolve().relative_to(root)
    journal.parent.mkdir(exist_ok=True)
    events = [json.loads(line) for line in journal.read_text(encoding='utf-8').splitlines()] if journal.exists() else []
    if action == 'start':
        if events:
            raise ValueError('Phase already started; use a fresh fixture')
    elif not events or events[-1]['action'] == 'end':
        raise ValueError('No active phase')
    if (action == 'read') != bool(paths):
        raise ValueError('Only read accepts and requires paths')
    output = []
    pending = []
    if action == 'read':
        for name in paths:
            path = (root / name).resolve(strict=True)
            path.relative_to(root)
            if '.capture' in path.relative_to(root).parts:
                raise ValueError('Journal is not fixture input')
            data = path.read_bytes()
            content = data.decode('utf-8')
            pending.append({'path': path.relative_to(root).as_posix(), 'bytes': len(data),
                            'chars': len(content), 'sha256': hashlib.sha256(data).hexdigest()})
            output.append(f'--- {name} ---\n{content}')
    event = {'action': action, 'utc': datetime.now(timezone.utc).isoformat(),
             'monotonic_ns': time.monotonic_ns()}
    if pending:
        event['files'] = pending
    if action == 'end':
        event['elapsed_ms'] = (event['monotonic_ns'] - events[0]['monotonic_ns']) // 1_000_000
    with journal.open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + '\n')
    return '\n'.join(output) if output else json.dumps(event)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('start', 'read', 'end'))
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--case', required=True)
    parser.add_argument('--phase', default='main')
    parser.add_argument('paths', nargs='*')
    args = parser.parse_args(argv)
    try:
        print(capture(args.root, args.case, args.phase, args.action, args.paths))
        return 0
    except (OSError, ValueError, UnicodeError) as exc:
        print(json.dumps({'error': str(exc)}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
