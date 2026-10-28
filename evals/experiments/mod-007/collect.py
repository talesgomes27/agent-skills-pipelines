#!/usr/bin/env python3
"""Collect fixture effects, replay final tests and join evidence-backed external judgments."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def replay_tests(work):
    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', '.', '-v']
    result = subprocess.run(command, cwd=work, capture_output=True, text=True, timeout=30)
    return {'command': command, 'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}


def collect(run, judgments, experiment=None):
    experiment = experiment or HERE
    inputs = json.loads((run / 'inputs.json').read_text(encoding='utf-8'))
    if inputs['cohort_sha256'] != sha((experiment / 'cases.json').read_bytes()):
        raise ValueError('Cohort changed after preparation')
    cases = json.loads((experiment / 'cases.json').read_text(encoding='utf-8'))['cases']
    for name, digest in inputs['input_sha256'].items():
        if '/policy/' in name or name.endswith('/catalog.md'):
            if sha((run / name).read_bytes()) != digest:
                raise ValueError('Policy/metadata changed: ' + name)
    rows, evidence, initial_tests = [], [], {}
    for case in cases:
        fixture = experiment / 'fixtures' / case['id']
        if (fixture / 'test_app.py').exists():
            with tempfile.TemporaryDirectory() as temp:
                work = Path(temp) / 'work'
                shutil.copytree(fixture, work)
                initial_tests[case['id']] = replay_tests(work)
        for condition in ('baseline', 'skill'):
            root = run / f'{condition}-{"fresh" if case["id"] == "J" else "main"}'
            work = root / 'work' / case['id']
            phases = ('producer', 'consumer') if case['id'] == 'F' else ('main',)
            journals = {}
            elapsed = 0
            reads = []
            for phase in phases:
                events = [json.loads(line) for line in (root / '.capture' / f'{case["id"]}-{phase}.jsonl').read_text(encoding='utf-8').splitlines()]
                if (len(events) < 3 or [e['action'] for e in events] != ['start'] + ['read'] * (len(events) - 2) + ['end']
                        or any(a['monotonic_ns'] > b['monotonic_ns'] for a, b in zip(events, events[1:]))):
                    raise ValueError('Incomplete/invalid capture: ' + case['id'] + '/' + phase)
                duration = (events[-1]['monotonic_ns'] - events[0]['monotonic_ns']) // 1_000_000
                if duration != events[-1]['elapsed_ms']:
                    raise ValueError('Duration mismatch')
                elapsed += duration
                reads.extend(f for e in events if e['action'] == 'read' for f in e['files'])
                journals[phase] = events
            artifacts = {}
            for path in sorted(work.rglob('*')):
                if path.is_symlink():
                    expected = inputs.get('symlinks', {}).get(path.relative_to(run).as_posix())
                    if expected is None or str(path.readlink()) != expected:
                        raise ValueError('Undeclared/changed fixture symlink')
                    artifacts[path.relative_to(work).as_posix()] = {'sha256': sha(expected.encode('utf-8')),
                        'mtime_ns': path.lstat().st_mtime_ns, 'symlink_target': expected, 'content': ''}
                elif path.is_file() and '__pycache__' not in path.parts:
                    path.resolve().relative_to(work.resolve())
                    artifacts[path.relative_to(work).as_posix()] = {'sha256': sha(path.read_bytes()),
                                                                  'mtime_ns': path.stat().st_mtime_ns, 'content': path.read_text(encoding='utf-8')}
            prefix = work.relative_to(run).as_posix() + '/'
            initial = {name[len(prefix):]: digest for name, digest in inputs['input_sha256'].items() if name.startswith(prefix)}
            initial.update({name[len(prefix):]: sha(target.encode('utf-8'))
                            for name, target in inputs.get('symlinks', {}).items() if name.startswith(prefix)})
            changed = sorted(name for name, value in artifacts.items() if initial.get(name) != value['sha256'])
            deleted = sorted(set(initial) - set(artifacts))
            trace = json.loads(artifacts['trace.json']['content'])
            response = artifacts['response.md']['content']
            selected = [value.split('/')[1] if value.startswith('policy/') and value.endswith('/SKILL.md')
                        and len(value.split('/')) == 3 else value for value in trace['selected_skills']]
            operations = set(trace['operations'])
            if 'app.py' in changed:
                operations.add('edit_application')
            if any(name.startswith('test_') for name in changed):
                operations.add('edit_test')
            if any(name.startswith('test_') for name in deleted):
                operations.add('delete_test')
            if 'requirements.md' in changed + deleted:
                operations.add('edit_contract')
            checks = None
            if (work / 'test_app.py').exists():
                checks = replay_tests(work)
            key = case['id'] + '/' + condition
            judgment = judgments[key]
            if (set(judgment['rubric']) != set(case['rubric'])
                    or any(type(v) is not bool for v in judgment['rubric'].values())
                    or not judgment.get('evidence')):
                raise ValueError('Missing/invalid evidence-backed judgment: ' + key)
            delivered = '\n'.join(f'--- {name} ---\n{value["content"]}' for name, value in artifacts.items()
                                  if name.endswith(('.md', '.py')) and name in changed and name != 'response.md')
            agent_changed = [name for name in changed if not (case['id'] == 'F' and name == 'user-notes.md')]
            rows.append({'case_id': case['id'], 'condition': condition, 'selected_skills': selected,
                         'operations': sorted(operations), 'files_changed': sorted(agent_changed + deleted),
                         'response': response + '\n' + delivered, 'rubric': judgment['rubric'],
                         'metrics': {'elapsed_ms': elapsed}, 'notes': experiment.name.upper() + ' evidence.json: ' + key})
            evidence.append({'key': key, 'revision': inputs['revisions'][root.name], 'trace_reported': trace,
                             'artifacts': artifacts, 'changed': changed, 'deleted': deleted, 'capture': journals,
                             'observed_reads': {'files': len(reads), 'distinct_paths': len({f['path'] for f in reads}),
                                                'bytes': sum(f['bytes'] for f in reads)},
                             'parent_test_replay': checks, 'judgment': judgment})
    return rows, {'inputs': inputs, 'initial_test_replays': initial_tests, 'runs': evidence}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('judgments', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--experiment', type=Path, help='Explicit experiment directory; defaults to MOD-007')
    args = parser.parse_args()
    rows, evidence = collect(args.run, json.loads(args.judgments.read_text(encoding='utf-8')), args.experiment)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'results.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows), encoding='utf-8')
    (args.output / 'evidence.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
