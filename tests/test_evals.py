import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('evals_cli', Path(__file__).resolve().parents[1] / 'scripts/evals.py')
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class EvalTests(unittest.TestCase):
    def run_cli(self, *args):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cli.main(list(args))
        return code, json.loads(out.getvalue())

    def test_catalog_has_three_kinds_per_skill(self):
        cases = cli.load_cases()
        skills = {case['skill'] for case in cases}
        self.assertEqual(len(skills), 8)
        for skill in skills:
            self.assertEqual({c['kind'] for c in cases if c['skill'] == skill}, {'positive', 'ambiguous', 'negative'})
        self.assertEqual(self.run_cli('validate')[0], 0)

    def test_workflow_cases_reject_forbidden_operations(self):
        cases = cli.load_cases()
        prohibited = {'proportional-simple': 'create_document',
                      'proportional-new': 'edit_application',
                      'proportional-legacy': 'edit_application',
                      'proportional-injection': 'delete_test',
                      'handoff-interrupted': 'edit_application',
                      'resume-changed-base': 'reuse_stale_checks',
                      'handoff-no-authority': 'claim_execution',
                      'routing-audit-only': 'start_execution',
                      'routing-small-bug': 'create_plan',
                      'routing-quarto-text': 'change_yaml'}
        by_id = {c['id']: c for c in cases}
        for case_id, operation in prohibited.items():
            with self.subTest(case_id=case_id):
                case = by_id[case_id]
                result = {'case_id': case_id, 'condition': 'skill',
                          'selected_skills': [case['skill']], 'operations': [], 'files_changed': [],
                          'response': ' '.join(case['required_signals']),
                          'rubric': {item: True for item in case['rubric']}}
                self.assertTrue(cli.grade(cases, [result])[0]['pass'])
                result['operations'] = [operation]
                self.assertFalse(cli.grade(cases, [result])[0]['pass'])

    def test_grade_pass_and_failure(self):
        case = cli.load_cases()[0]
        base = {
            'case_id': case['id'], 'condition': 'skill', 'selected_skills': [case['skill']],
            'operations': [], 'files_changed': [],
            'response': 'Requisitos, arquitetura e plano.',
            'rubric': {item: True for item in case['rubric']},
            'metrics': {'tool_calls': 2, 'tokens': 100, 'elapsed_ms': 10}
        }
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'results.jsonl'
            path.write_text(json.dumps(base) + '\n', encoding='utf-8')
            code, data = self.run_cli('grade', '--results', str(path))
            self.assertEqual(code, 0)
            self.assertTrue(data['results'][0]['pass'])
            self.assertEqual(data['summary']['skill'], {
                'total': 1, 'passed': 1, 'tool_calls': 2, 'tokens': 100, 'elapsed_ms': 10,
                'metric_observations': {'tool_calls': 1, 'tokens': 1, 'elapsed_ms': 1}})
            base['operations'] = [case['forbidden_operations'][0]]
            path.write_text(json.dumps(base) + '\n', encoding='utf-8')
            _, data = self.run_cli('grade', '--results', str(path))
            self.assertFalse(data['results'][0]['pass'])

    def test_duplicate_result_is_rejected(self):
        case = cli.load_cases()[0]
        result = {'case_id': case['id'], 'condition': 'baseline', 'selected_skills': [], 'operations': [], 'files_changed': [], 'response': '', 'rubric': {}}
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'results.jsonl'
            path.write_text(json.dumps(result) + '\n' + json.dumps(result) + '\n', encoding='utf-8')
            self.assertEqual(self.run_cli('grade', '--results', str(path))[0], 1)

    def test_grade_without_metrics_preserves_input_and_quality(self):
        case = cli.load_cases()[0]
        result = {'case_id': case['id'], 'condition': 'skill',
                  'selected_skills': [case['skill']], 'operations': [], 'files_changed': [],
                  'response': ' '.join(case['required_signals']),
                  'rubric': {item: True for item in case['rubric']}}
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'results.jsonl'
            path.write_text(json.dumps(result) + '\n', encoding='utf-8')
            before = path.read_bytes()
            code, data = self.run_cli('grade', '--results', str(path))
            self.assertEqual(code, 0)
            self.assertTrue(data['results'][0]['pass'])
            self.assertEqual(data['results'][0]['metrics'], {})
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(data['summary']['skill'], {
                'total': 1, 'passed': 1, 'tool_calls': None, 'tokens': None, 'elapsed_ms': None,
                'metric_observations': {'tool_calls': 0, 'tokens': 0, 'elapsed_ms': 0}})

    def test_summary_preserves_observed_zero(self):
        graded = [{'condition': 'skill', 'pass': True,
                   'metrics': {'tool_calls': 0, 'tokens': 0, 'elapsed_ms': 0}}]
        self.assertEqual(cli.summary(graded)['skill'], {
            'total': 1, 'passed': 1, 'tool_calls': 0, 'tokens': 0, 'elapsed_ms': 0,
            'metric_observations': {'tool_calls': 1, 'tokens': 1, 'elapsed_ms': 1}})

    def test_summary_reports_partial_coverage_per_metric_and_condition(self):
        graded = [
            {'condition': 'skill', 'pass': True, 'metrics': {'tool_calls': 2, 'tokens': 10}},
            {'condition': 'skill', 'pass': False, 'metrics': {}},
            {'condition': 'skill', 'pass': True, 'metrics': {'tool_calls': 0, 'tokens': 20}},
            {'condition': 'baseline', 'pass': False, 'metrics': {'elapsed_ms': 7}},
        ]
        self.assertEqual(cli.summary(graded), {
            'skill': {'total': 3, 'passed': 2, 'tool_calls': 2, 'tokens': 30, 'elapsed_ms': None,
                      'metric_observations': {'tool_calls': 2, 'tokens': 2, 'elapsed_ms': 0}},
            'baseline': {'total': 1, 'passed': 0, 'tool_calls': None, 'tokens': None, 'elapsed_ms': 7,
                         'metric_observations': {'tool_calls': 0, 'tokens': 0, 'elapsed_ms': 1}},
        })

    def test_invalid_results_return_controlled_errors(self):
        case = cli.load_cases()[0]
        valid = {'case_id': case['id'], 'condition': 'skill', 'selected_skills': [],
                 'operations': [], 'files_changed': [], 'response': '', 'rubric': {}}
        invalid = [
            {'case_id': []}, {'case_id': 'unknown-case'}, {'condition': 'candidate'},
            {'selected_skills': [1]}, {'selected_skills': ['x', 'x']},
            {'operations': 'shell'}, {'files_changed': [False]}, {'response': None},
            {'rubric': {'criterion': 1}}, {'notes': []}, {'unexpected': True},
        ]
        invalid += [{'metrics': value} for value in ('bad', None, [], {'other': 1})]
        invalid += [{'metrics': {'tokens': value}} for value in ('1', None, -1, True, 1.5)]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'results.jsonl'
            for changes in invalid:
                with self.subTest(changes=changes):
                    path.write_text(json.dumps(dict(valid, **changes)) + '\n', encoding='utf-8')
                    code, data = self.run_cli('grade', '--results', str(path))
                    self.assertEqual(code, 1)
                    self.assertEqual(data['status'], 'fail')
                    self.assertIsInstance(data['error'], str)
            for content in ('{', '[]', json.dumps({'case_id': case['id']})):
                with self.subTest(content=content):
                    path.write_text(content, encoding='utf-8')
                    self.assertEqual(self.run_cli('grade', '--results', str(path))[0], 1)

    def test_case_identity_types_and_catalog_membership(self):
        case = cli.load_cases()[0]
        invalid = [{'id': []}, {'id': ''}, {'skill': 1}, {'skill': 'unknown-skill'},
                   {'prompt': None}, {'prompt': ' '}, {'expected_activation': 1}]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'cases.json'
            for changes in invalid:
                with self.subTest(changes=changes), patch.object(cli, 'CASES', path):
                    path.write_text(json.dumps({'version': 1, 'cases': [dict(case, **changes)]}), encoding='utf-8')
                    code, data = self.run_cli('validate')
                    self.assertEqual(code, 1)
                    self.assertEqual(data['status'], 'fail')
            for content in ({'version': True, 'cases': [case]}, {'version': 1, 'cases': []},
                            {'version': 1, 'cases': [case, case]}):
                with self.subTest(content=content), patch.object(cli, 'CASES', path):
                    path.write_text(json.dumps(content), encoding='utf-8')
                    self.assertEqual(self.run_cli('validate')[0], 1)

    def test_coverage_and_evaluation_status_are_separate_from_processing(self):
        cases = cli.load_cases()
        results = [
            {'case_id': case['id'], 'condition': condition,
             'selected_skills': [case['skill']] if case['expected_activation'] else [],
             'operations': [], 'files_changed': [], 'response': ' '.join(case['required_signals']),
             'rubric': {item: True for item in case['rubric']}, 'notes': 'Synthetic fixture'}
            for case in cases for condition in ('baseline', 'skill')
        ]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'results.jsonl'
            for rows, expected_status in (([], 'incomplete'), (results[:1], 'incomplete'),
                                          (results, 'passed')):
                with self.subTest(count=len(rows)):
                    path.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
                    code, data = self.run_cli('grade', '--results', str(path))
                    self.assertEqual(code, 0)
                    self.assertEqual(data.get('status'), 'processed')
                    self.assertEqual(data['evaluation'], expected_status)
                    self.assertEqual(data['coverage']['expected'], len(results))
                    self.assertEqual(data['coverage']['observed'], len(rows))
                    self.assertEqual(data['coverage']['complete'], len(rows) == len(results))
                    self.assertEqual(len(data['coverage']['missing']), len(results) - len(rows))
                    if not rows:
                        self.assertEqual(data['coverage']['missing'][0],
                                         {'case_id': cases[0]['id'], 'condition': 'baseline'})
                    else:
                        self.assertNotIn({'case_id': cases[0]['id'], 'condition': 'baseline'},
                                         data['coverage']['missing'])
            results[0]['operations'] = [cases[0]['forbidden_operations'][0]]
            for rows in (results[:1], results):
                path.write_text(''.join(json.dumps(row) + '\n' for row in rows), encoding='utf-8')
                code, data = self.run_cli('grade', '--results', str(path))
                self.assertEqual(code, 0)
                self.assertEqual(data.get('status'), 'processed')
                self.assertEqual(data['evaluation'], 'failed')
                self.assertFalse(data['results'][0]['pass'])


if __name__ == '__main__':
    unittest.main()
