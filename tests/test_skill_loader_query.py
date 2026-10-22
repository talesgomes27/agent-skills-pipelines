"""Tests for bounded cold-library lookup."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('library_query', Path(__file__).resolve().parents[1] / 'skill-loader/scripts/library_query.py')
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class QueryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        folder = self.root / 'nested/alpha'
        folder.mkdir(parents=True)
        (folder / 'SKILL.md').write_text('---\nname: alpha\ndescription: Database architecture helper.\n---\n')
        (self.root / 'skills_index.json').write_text(json.dumps([{'id': 'alpha', 'name': 'alpha', 'path': 'nested/alpha', 'description': 'Database architecture helper.', 'risk': 'safe'}]))

    def run_cli(self, *args):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cli.main(list(args))
        return code, json.loads(out.getvalue())

    def test_exact_and_search_validate_manifest(self):
        code, result = self.run_cli('exact', 'alpha', '--root', str(self.root))
        self.assertEqual(code, 0)
        manifest = Path(result['result']['manifest'])
        self.assertEqual(manifest.name, 'SKILL.md')
        self.assertEqual(manifest.parent.name, 'alpha')
        self.assertEqual(manifest.parent.parent.name, 'nested')
        code, result = self.run_cli('search', 'database architecture', '--root', str(self.root))
        self.assertEqual(code, 0)
        self.assertEqual(result['results'][0]['id'], 'alpha')

    def test_user_configuration_resolves_root(self):
        config = self.root / 'library.json'
        config.write_text(json.dumps({'root': str(self.root)}))
        with patch.object(cli, 'USER_CONFIG', config):
            resolved = Path(self.run_cli('root')[1]['root'])
            self.assertTrue(resolved.samefile(self.root))

    def test_identity_mismatch_is_rejected(self):
        (self.root / 'nested/alpha/SKILL.md').write_text('---\nname: beta\ndescription: Wrong.\n---\n')
        self.assertEqual(self.run_cli('exact', 'alpha', '--root', str(self.root))[0], 1)


if __name__ == '__main__':
    unittest.main()
