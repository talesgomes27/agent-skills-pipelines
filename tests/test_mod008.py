import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prepare_mod008', ROOT / 'evals/experiments/mod-008/prepare.py')
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)
eval_spec = importlib.util.spec_from_file_location('eval_mod008', ROOT / 'scripts/evals.py')
evals = importlib.util.module_from_spec(eval_spec)
eval_spec.loader.exec_module(evals)


class Mod008Tests(unittest.TestCase):
    def test_cohort_rejects_authority_escalation_and_keeps_catalog_identity(self):
        cases = evals.load_cases(ROOT / 'evals/experiments/mod-008/cases.json')
        self.assertEqual(len(cases), 6)
        for case in cases:
            result = {'case_id': case['id'], 'condition': 'skill', 'selected_skills': [case['skill']],
                      'operations': [], 'files_changed': [], 'response': ' '.join(case['required_signals']),
                      'rubric': {item: True for item in case['rubric']}}
            self.assertTrue(evals.grade(cases, [result])[0]['pass'])
            for operation in case['forbidden_operations']:
                with self.subTest(case=case['id'], operation=operation):
                    result['operations'] = [operation]
                    self.assertFalse(evals.grade(cases, [result])[0]['pass'])

    def test_preparation_has_matched_inputs_and_declared_external_symlink(self):
        try:
            if subprocess.run(['git', 'rev-parse', '--verify', prepare.BASELINE], cwd=ROOT,
                              capture_output=True).returncode:
                self.skipTest('Campaign replay needs pinned Git history')
        except FileNotFoundError:
            self.skipTest('Campaign replay needs Git')
        with tempfile.TemporaryDirectory() as temp:
            probe = Path(temp) / 'probe'
            try:
                probe.symlink_to(Path(temp) / 'target')
                probe.unlink()
            except OSError:
                self.skipTest('Host cannot create symlinks')
            destination = Path(temp) / 'campaign'
            manifest = prepare.prepare(destination)
            proposal = json.loads((prepare.HERE / 'candidate.json').read_text(encoding='utf-8'))
            for name, content in proposal['files'].items():
                self.assertEqual((destination / 'skill-main/policy' / name).read_text(encoding='utf-8'), content)
            for path in (destination / 'baseline-main/work').rglob('*'):
                peer = destination / 'skill-main/work' / path.relative_to(destination / 'baseline-main/work')
                if path.is_symlink():
                    self.assertTrue(peer.is_symlink())
                    with self.assertRaises(ValueError):
                        path.resolve().relative_to(destination / 'baseline-main')
                    self.assertIn(path.relative_to(destination).as_posix(), manifest['symlinks'])
                    self.assertNotIn(path.relative_to(destination).as_posix(), manifest['input_sha256'])
                elif path.is_file():
                    self.assertEqual(path.read_bytes(), peer.read_bytes())
            self.assertEqual(json.loads((destination / 'inputs.json').read_text(encoding='utf-8')), manifest)
            with self.assertRaises(FileExistsError):
                prepare.prepare(destination)
