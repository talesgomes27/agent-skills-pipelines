"""Cold-library index maintenance checks."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('library_cli', Path(__file__).resolve().parents[1] / 'scripts/library.py')
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        folder = self.root / 'skills/topic/alpha'
        folder.mkdir(parents=True)
        (folder / 'SKILL.md').write_text('---\nname: alpha\ndescription: Alpha helper.\n---\n', encoding='utf-8')
        self.index = self.root / 'skills_index.json'
        self.index.write_text(json.dumps([{'id': 'alpha', 'path': 'skills/topic/alpha', 'risk': 'safe'}]), encoding='utf-8')

    def run_cli(self, *args):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cli.main(list(args))
        return code, json.loads(out.getvalue())

    def test_doctor_accepts_valid_index(self):
        code, result = self.run_cli('doctor', '--root', str(self.root))
        self.assertEqual(code, 0)
        self.assertEqual(result['valid'], 1)

    def test_doctor_detects_stale_path(self):
        self.index.write_text(json.dumps([{'id': 'alpha', 'path': 'skills/missing'}]), encoding='utf-8')
        self.assertEqual(self.run_cli('doctor', '--root', str(self.root))[0], 1)

    def test_rebuild_is_reviewable_and_preserves_metadata(self):
        output = self.root / 'candidate.json'
        code, result = self.run_cli('rebuild', '--root', str(self.root), '--output', str(output))
        self.assertEqual(code, 0)
        self.assertEqual(result['preserved_metadata'], 1)
        candidate = json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(candidate[0]['risk'], 'safe')
        self.assertEqual(candidate[0]['path'], 'skills/topic/alpha')

    def test_rebuild_requires_explicit_replace_for_source(self):
        self.assertEqual(self.run_cli('rebuild', '--root', str(self.root), '--output', str(self.index))[0], 1)


if __name__ == '__main__':
    unittest.main()
