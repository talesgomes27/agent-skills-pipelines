import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

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


if __name__ == '__main__':
    unittest.main()
