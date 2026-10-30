#!/usr/bin/env python3
"""Reconcile existing MOD evidence and replay saved fixtures; does not invoke agents."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / 'docs/audits/modernization-2026-10-28'


def measure(run, metrics):
    if not run['capture']:
        raise ValueError('No captured interval')
    elapsed, reads = 0, []
    for events in run['capture'].values():
        if not events or events[0]['action'] != 'start' or events[-1]['action'] != 'end':
            raise ValueError('Incomplete captured interval')
        duration = (events[-1]['monotonic_ns'] - events[0]['monotonic_ns']) // 1_000_000
        if duration < 0 or duration != events[-1]['elapsed_ms']:
            raise ValueError('Inconsistent captured duration')
        elapsed += duration
        reads.extend(item for event in events if event['action'] == 'read' for item in event['files'])
    if 'elapsed_ms' in metrics and metrics['elapsed_ms'] != elapsed:
        raise ValueError('Trace and captured duration differ')
    paths = {item['path'] for item in reads}
    return {'elapsed_ms': elapsed, 'file_emissions': len(reads), 'distinct_paths': len(paths),
            'repeat_emissions': len(reads) - len(paths), 'bytes_emitted': sum(item['bytes'] for item in reads),
            'distinct_entrypoints': len({path for path in paths if path.endswith('/SKILL.md')}),
            'tokens': metrics.get('tokens'), 'tool_calls': metrics.get('tool_calls')}


def verify():
    sources = {}

    def read(path):
        data = path.read_bytes()
        sources[path.relative_to(ROOT).as_posix()] = hashlib.sha256(data).hexdigest()
        return json.loads(data)

    old = read(AUDIT / 'mod-005-ab.json')
    proportional = {}
    for condition in ('baseline', 'candidate-v2'):
        proportional[condition] = {}
        for case, effects in old['runs'][condition]['verified_file_effects'].items():
            documents = sorted(name for name in effects['created'] if name.endswith('.md'))
            assert len(documents) == effects['new_document_count']
            proportional[condition][case] = {'new_documents': documents, 'count': len(documents)}
    handoff = read(AUDIT / 'mod-006-behavior.json')
    campaigns, replays = {}, []
    for name in ('mod-007', 'mod-008'):
        experiment = ROOT / 'evals/experiments' / name
        folder = experiment / 'runs/2026-10-28'
        evidence, grade = read(folder / 'evidence.json'), read(folder / 'grade.json')
        read(experiment / 'cases.json')
        result_path = folder / 'results.jsonl'
        data = result_path.read_bytes()
        sources[result_path.relative_to(ROOT).as_posix()] = hashlib.sha256(data).hexdigest()
        results = {(r['case_id'] + '/' + r['condition']): r for r in map(json.loads, data.splitlines())}
        command = [sys.executable, '-B', str(ROOT / 'scripts/evals.py'), 'grade',
                   '--cases', str(experiment / 'cases.json'), '--results', str(result_path)]
        processed = subprocess.run(command, check=True, capture_output=True, text=True)
        assert json.loads(processed.stdout) == grade, 'Historical grade changed'
        assert grade['coverage']['complete'] and len(results) == len(evidence['runs'])
        measurements = {}
        for run in evidence['runs']:
            result = results[run['key']]
            observed = measure(run, result.get('metrics', {}))
            assert observed['file_emissions'] == run['observed_reads']['files']
            assert observed['distinct_paths'] == run['observed_reads']['distinct_paths']
            assert observed['bytes_emitted'] == run['observed_reads']['bytes']
            observed['rubric_met'] = sum(result['rubric'].values())
            observed['rubric_total'] = len(result['rubric'])
            # Fixture response/logs are instrumentation; supplied Markdown is not a new document.
            prefix = ('skill' if result['condition'] == 'skill' else 'baseline') + (
                '-fresh' if result['case_id'] == 'J' else '-main') + '/work/' + result['case_id'] + '/'
            initial = {path[len(prefix):] for path in evidence['inputs']['input_sha256'] if path.startswith(prefix)}
            observed['additional_md'] = [path for path in run['changed']
                if path.endswith('.md') and path not in initial and path != 'response.md']
            measurements[run['key']] = observed
            if 'test_app.py' not in run['artifacts']:
                continue
            test = run['artifacts']['test_app.py']['content'].encode('utf-8')
            assert hashlib.sha256(test).hexdigest() == evidence['inputs']['input_sha256'][prefix + 'test_app.py']
            with tempfile.TemporaryDirectory(prefix='mod010-replay-') as temp:
                work = Path(temp)
                for filename, artifact in run['artifacts'].items():
                    if filename.endswith('.py'):
                        path = work / filename
                        path.resolve().relative_to(work.resolve())
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_text(artifact['content'], encoding='utf-8')
                command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', '.', '-v']
                replay = subprocess.run(command, cwd=work, capture_output=True, text=True, timeout=30)
                expected = 1 if name == 'mod-008' and result['case_id'] == 'D-review' else 0
                assert replay.returncode == expected, run['key'] + replay.stderr
                if expected:
                    assert 'AssertionError' in replay.stderr and 'test_preview' in replay.stderr
                replays.append({'campaign': name, 'key': run['key'], 'command': command,
                    'exit_code': replay.returncode, 'expected_exit': expected,
                    'stdout': replay.stdout, 'stderr': replay.stderr})
        campaigns[name] = {'coverage': grade['coverage'], 'strict_grade': grade['evaluation'],
                           'strict_failures': [r for r in grade['results'] if not r['pass']],
                           'measurements': measurements}
        if name == 'mod-007':
            prefix = 'skill-main/policy/'
            policy = {name[len(prefix):]: digest for name, digest in evidence['inputs']['input_sha256'].items()
                      if name.startswith(prefix)}
            for filename, digest in policy.items():
                assert hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() == digest, filename
    return {'sources_sha256': sources, 'proportional_MOD005': proportional,
            'handoff_MOD006': {'transfer': handoff['transfer'], 'coverage': handoff['grader_output']['coverage'],
                               'strict_grade': handoff['grader_output']['evaluation']},
            'campaigns': campaigns, 'active_policy_files_matching_MOD007': len(policy), 'replays': replays,
            'interpretation': 'Existing evidence reprocessed; no new agent run. Studies and cases are not pooled. '
                'Emitted bytes/documents are not tokens. Native metrics absent remain null; n=1 per case/condition.'}


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
