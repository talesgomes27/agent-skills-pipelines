#!/usr/bin/env python3
"""Validate behavioral cases and grade captured agent traces without invoking a model."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / 'evals/cases.json'


def load_cases(path=None):
    data = json.loads((path or CASES).read_text(encoding='utf-8'))
    if (not isinstance(data, dict) or type(data.get('version')) is not int or data['version'] != 1
            or not isinstance(data.get('cases'), list) or not data['cases']):
        raise ValueError('Unsupported eval case format')
    skills = json.loads((ROOT / 'distribution/catalog.json').read_text(encoding='utf-8'))['skills']
    required = {'id', 'skill', 'kind', 'prompt', 'expected_activation', 'required_signals', 'forbidden_operations', 'rubric'}
    ids = set()
    for case in data['cases']:
        if not isinstance(case, dict) or set(case) != required:
            raise ValueError('Invalid case fields')
        for field in ('id', 'skill', 'prompt'):
            if not isinstance(case[field], str) or not case[field].strip():
                raise ValueError('Invalid case ' + field)
        if case['skill'] not in skills:
            raise ValueError('Unknown case skill: ' + case['skill'])
        if case['id'] in ids:
            raise ValueError('Duplicate case id: ' + case['id'])
        ids.add(case['id'])
        if case['kind'] not in ('positive', 'ambiguous', 'negative'):
            raise ValueError('Invalid kind: ' + case['id'])
        if not isinstance(case['expected_activation'], bool):
            raise ValueError('expected_activation must be boolean: ' + case['id'])
        for field in ('required_signals', 'forbidden_operations', 'rubric'):
            if not isinstance(case[field], list) or not case[field] or any(not isinstance(v, str) or not v for v in case[field]):
                raise ValueError('Invalid ' + field + ': ' + case['id'])
    return data['cases']


def load_results(path):
    results = []
    for line_no, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f'Invalid JSONL at line {line_no}') from exc
        required = {'case_id', 'condition', 'selected_skills', 'operations', 'files_changed', 'response', 'rubric'}
        if (not isinstance(item, dict) or not required <= set(item)
                or set(item) - required - {'metrics', 'notes'}
                or not isinstance(item['case_id'], str)
                or item['condition'] not in ('baseline', 'skill')):
            raise ValueError(f'Invalid result at line {line_no}')
        for field in ('selected_skills', 'operations', 'files_changed'):
            if not isinstance(item[field], list) or any(not isinstance(v, str) for v in item[field]):
                raise ValueError(f'Invalid {field} at line {line_no}')
        if len(set(item['selected_skills'])) != len(item['selected_skills']):
            raise ValueError(f'Duplicate selected_skills at line {line_no}')
        if not isinstance(item['response'], str) or not isinstance(item['rubric'], dict) or any(type(v) is not bool for v in item['rubric'].values()):
            raise ValueError(f'Invalid response/rubric at line {line_no}')
        if 'notes' in item and not isinstance(item['notes'], str):
            raise ValueError(f'Invalid notes at line {line_no}')
        metrics = item.get('metrics', {})
        if (not isinstance(metrics, dict) or set(metrics) - {'tool_calls', 'tokens', 'elapsed_ms'}
                or any(type(v) is not int or v < 0 for v in metrics.values())):
            raise ValueError(f'Invalid metrics at line {line_no}')
        results.append(item)
    return results


def grade(cases, results):
    by_id = {c['id']: c for c in cases}
    seen = set()
    graded = []
    for result in results:
        key = (result['case_id'], result['condition'])
        if key in seen:
            raise ValueError('Duplicate result: ' + '/'.join(key))
        seen.add(key)
        if result['case_id'] not in by_id:
            raise ValueError('Unknown case: ' + result['case_id'])
        case = by_id[result['case_id']]
        active = case['skill'] in result['selected_skills']
        activation_ok = active == case['expected_activation'] if result['condition'] == 'skill' else True
        operations = {v.casefold() for v in result['operations']}
        forbidden = [v for v in case['forbidden_operations'] if v.casefold() in operations]
        response = result['response'].casefold()
        missing = [v for v in case['required_signals'] if v.casefold() not in response]
        rubric_missing = [v for v in case['rubric'] if result['rubric'].get(v) is not True]
        passed = activation_ok and not forbidden and not missing and not rubric_missing
        graded.append({
            'case_id': case['id'], 'condition': result['condition'], 'pass': passed,
            'activation_ok': activation_ok, 'forbidden_operations': forbidden,
            'missing_signals': missing, 'rubric_missing': rubric_missing,
            'metrics': result.get('metrics', {})
        })
    return graded


def summary(graded):
    conditions = {}
    for item in graded:
        bucket = conditions.setdefault(item['condition'], {
            'total': 0, 'passed': 0, 'tool_calls': None, 'tokens': None, 'elapsed_ms': None,
            'metric_observations': {'tool_calls': 0, 'tokens': 0, 'elapsed_ms': 0},
        })
        bucket['total'] += 1
        bucket['passed'] += int(item['pass'])
        for metric in ('tool_calls', 'tokens', 'elapsed_ms'):
            value = item['metrics'].get(metric)
            if type(value) is int and value >= 0:
                bucket[metric] = (bucket[metric] or 0) + value
                bucket['metric_observations'][metric] += 1
    return conditions


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('validate', 'matrix', 'grade'))
    parser.add_argument('--results', type=Path)
    parser.add_argument('--cases', type=Path, help='Explicit cohort; defaults to evals/cases.json')
    args = parser.parse_args(argv)
    try:
        cases = load_cases(args.cases)
        if args.command == 'validate':
            counts = {}
            for case in cases:
                counts[case['kind']] = counts.get(case['kind'], 0) + 1
            output = {'status': 'pass', 'cases': len(cases), 'skills': len({c['skill'] for c in cases}), 'kinds': counts}
        elif args.command == 'matrix':
            output = {'cases': [{'id': c['id'], 'skill': c['skill'], 'kind': c['kind'], 'prompt': c['prompt']} for c in cases]}
        else:
            if args.results is None:
                raise ValueError('--results is required for grade')
            graded = grade(cases, load_results(args.results))
            observed = {(item['case_id'], item['condition']) for item in graded}
            missing = [{'case_id': case['id'], 'condition': condition}
                       for case in cases for condition in ('baseline', 'skill')
                       if (case['id'], condition) not in observed]
            evaluation = 'failed' if any(not item['pass'] for item in graded) else (
                'incomplete' if missing else 'passed')
            output = {
                'status': 'processed', 'evaluation': evaluation,
                'coverage': {'expected': len(cases) * 2, 'observed': len(observed),
                             'complete': not missing, 'missing': missing},
                'results': graded, 'summary': summary(graded),
            }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({'status': 'fail', 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
