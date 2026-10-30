import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('verify_mod010', Path(__file__).resolve().parents[1] / 'evals/experiments/mod-010/verify.py')
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


class Mod010Tests(unittest.TestCase):
    def test_reconciliation_counts_emissions_and_preserves_unknown_and_real_zero(self):
        entry = {'path': 'policy/execution-pipeline/SKILL.md', 'bytes': 10}
        run = {'capture': {
            'first': [{'action': 'start', 'monotonic_ns': 0},
                      {'action': 'read', 'files': [entry, entry]},
                      {'action': 'end', 'monotonic_ns': 3_000_000, 'elapsed_ms': 3}],
            'second': [{'action': 'start', 'monotonic_ns': 10_000_000},
                       {'action': 'read', 'files': [{'path': 'work/test.py', 'bytes': 20}]},
                       {'action': 'end', 'monotonic_ns': 12_000_000, 'elapsed_ms': 2}]}}
        result = verify.measure(run, {})
        self.assertEqual(result, {'elapsed_ms': 5, 'file_emissions': 3, 'distinct_paths': 2,
            'repeat_emissions': 1, 'bytes_emitted': 40, 'distinct_entrypoints': 1,
            'tokens': None, 'tool_calls': None})
        measured = verify.measure(run, {'tokens': 0, 'tool_calls': 0, 'elapsed_ms': 5})
        self.assertEqual(measured['tokens'], 0)
        self.assertEqual(measured['tool_calls'], 0)
        with self.assertRaises(ValueError):
            verify.measure({'capture': {}}, {})
        with self.assertRaises(ValueError):
            verify.measure(run, {'elapsed_ms': 0})
        run['capture']['first'].pop()
        with self.assertRaises(ValueError):
            verify.measure(run, {})
