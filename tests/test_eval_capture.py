import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('capture', Path(__file__).resolve().parents[1] / 'evals/experiments/mod-007/capture.py')
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)
prepare_spec = importlib.util.spec_from_file_location('prepare', Path(__file__).resolve().parents[1] / 'evals/experiments/mod-007/prepare.py')
prepare = importlib.util.module_from_spec(prepare_spec)
prepare_spec.loader.exec_module(prepare)
collect_spec = importlib.util.spec_from_file_location('collect', Path(__file__).resolve().parents[1] / 'evals/experiments/mod-007/collect.py')
collect = importlib.util.module_from_spec(collect_spec)
collect_spec.loader.exec_module(collect)


class CaptureTests(unittest.TestCase):
    def test_collection_preserves_raw_evidence_and_rejects_provenance_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            run = Path(temp)
            cohort = run / 'cases.json'
            cohort.write_text(json.dumps({'cases': [{'id': 'G', 'rubric': ['route']}]}))
            inputs = {'input_sha256': {}, 'revisions': {}, 'cohort_sha256': collect.sha(cohort.read_bytes())}
            judgments = {}
            for condition in ('baseline', 'skill'):
                root = run / (condition + '-main')
                work = root / 'work/G'
                work.mkdir(parents=True)
                (root / 'catalog.md').write_text('metadata')
                inputs['input_sha256'][root.name + '/catalog.md'] = collect.sha(b'metadata')
                inputs['revisions'][root.name] = 'pinned'
                capture.capture(root, 'G', 'main', 'start')
                capture.capture(root, 'G', 'main', 'read', ['catalog.md'])
                (work / 'trace.json').write_text(json.dumps({'selected_skills': [], 'operations': []}))
                (work / 'response.md').write_text('original')
                capture.capture(root, 'G', 'main', 'end')
                judgments['G/' + condition] = {'rubric': {'route': True}, 'evidence': ['response.md']}
            (run / 'inputs.json').write_text(json.dumps(inputs))
            with patch.object(collect, 'HERE', run):
                rows, evidence = collect.collect(run, judgments)
                self.assertEqual(len(rows), 2)
                self.assertEqual(rows[0]['response'], 'original\n')
                self.assertEqual(set(rows[0]['metrics']), {'elapsed_ms'})
                self.assertEqual(evidence['runs'][0]['observed_reads']['bytes'], 8)
                self.assertIsNone(evidence['runs'][0]['parent_test_replay'])
                outside = run / 'outside.txt'
                outside.write_text('outside')
                link = run / 'baseline-main/work/G/link'
                try:
                    link.symlink_to(outside)
                except OSError:
                    self.skipTest('Host cannot create symlinks')
                with self.assertRaises(ValueError):
                    collect.collect(run, judgments)
                link.unlink()
                journal = run / 'baseline-main/.capture/G-main.jsonl'
                original = journal.read_text(encoding='utf-8')
                journal.write_text('\n'.join(original.splitlines()[:-1]) + '\n')
                with self.assertRaises(ValueError):
                    collect.collect(run, judgments)
                journal.write_text(original)
                (run / 'baseline-main/catalog.md').write_text('changed')
                with self.assertRaises(ValueError):
                    collect.collect(run, judgments)
                (run / 'baseline-main/catalog.md').write_text('metadata')
                cohort.write_text('{}')
                with self.assertRaises(ValueError):
                    collect.collect(run, judgments)

    def test_prepare_pins_equal_inputs_and_refuses_existing_destination(self):
        try:
            for revision in (prepare.BASELINE, prepare.CANDIDATE):
                if subprocess.run(['git', 'rev-parse', '--verify', revision], cwd=prepare.REPO,
                                  capture_output=True).returncode:
                    self.skipTest('Campaign replay needs pinned Git history (unavailable in shallow/source archives)')
        except FileNotFoundError:
            self.skipTest('Campaign replay needs Git')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'campaign'
            manifest = prepare.prepare(root)
            self.assertEqual(manifest['revisions']['baseline-fresh'], manifest['revisions']['skill-fresh'])
            self.assertNotEqual(manifest['revisions']['baseline-main'], manifest['revisions']['skill-main'])
            for path in (root / 'baseline-main/work').rglob('*'):
                if path.is_file():
                    self.assertEqual(path.read_bytes(), (root / 'skill-main/work' / path.relative_to(root / 'baseline-main/work')).read_bytes())
            self.assertTrue(manifest['input_sha256'])
            with self.assertRaises(FileExistsError):
                prepare.prepare(root)

    def test_reads_and_elapsed_are_observed_without_native_metrics(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'input.md').write_text('ação', encoding='utf-8')
            capture.capture(root, 'A', 'main', 'start')
            self.assertIn('ação', capture.capture(root, 'A', 'main', 'read', ['input.md']))
            capture.capture(root, 'A', 'main', 'end')
            events = [json.loads(line) for line in (root / '.capture/A-main.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual([e['action'] for e in events], ['start', 'read', 'end'])
            self.assertEqual(events[1]['files'][0]['bytes'], len('ação'.encode()))
            self.assertEqual(events[1]['files'][0]['chars'], 4)
            self.assertGreaterEqual(events[-1]['elapsed_ms'], 0)
            self.assertNotIn('tokens', events[-1])
            self.assertNotIn('tool_calls', events[-1])

    def test_paths_and_phase_boundaries(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            root = Path(temp)
            secret = Path(outside) / 'outside.txt'
            secret.write_text('outside', encoding='utf-8')
            second = root / 'second'
            second.mkdir()
            try:
                (root / 'link').symlink_to(secret)
                (second / '.capture').symlink_to(Path(outside), target_is_directory=True)
            except OSError:
                self.skipTest('Host cannot create symlinks')
            with self.assertRaises(ValueError):
                capture.capture(second, 'A', 'main', 'start')
            for action in ('read', 'end'):
                with self.assertRaises(ValueError):
                    capture.capture(root, 'A', 'main', action, ['link'] if action == 'read' else [])
            with self.assertRaises(ValueError):
                capture.capture(root, '../A', 'main', 'start')
            capture.capture(root, 'A', 'main', 'start')
            for name in ('link', str(secret), '../' + Path(outside).name + '/outside.txt', '.capture/A-main.jsonl'):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    capture.capture(root, 'A', 'main', 'read', [name])
            with self.assertRaises(ValueError):
                capture.capture(root, 'A', 'main', 'start')
            capture.capture(root, 'A', 'main', 'end')
            with self.assertRaises(ValueError):
                capture.capture(root, 'A', 'main', 'end')
