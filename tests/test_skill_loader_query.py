"""Tests for bounded cold-library lookup."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
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

    def test_invalid_frontmatter_is_rejected_by_exact_and_search(self):
        manifests = [
            '# No frontmatter\nname: alpha\n',
            '---\ndescription: Helper.\n---\nname: alpha\n',
            '---\nname: alpha\ndescription: [\n---\n',
            '---\nname: alpha\nname: beta\ndescription: Helper.\n---\n',
            '---\nname: alpha\ndescription: First\ndescription: Second\n---\n',
            '---\nname: alpha\n---\n',
            '---\nname: alpha\ndescription: 123\n---\n',
            '---\nname: alpha\ndescription: " "\n---\n',
            '---\nname: alpha\ndescription: !!python/object:builtins.object {}\n---\n',
            '---\nname: alpha\ndescription: Helper.\n? [a, b]\n: value\n---\n',
            '---\n- alpha\n---\n',
            '---\nname: alpha\ndescription: Helper.\n',
        ]
        for text in manifests:
            with self.subTest(text=text):
                (self.root / 'nested/alpha/SKILL.md').write_text(text)
                code, result = self.run_cli('exact', 'alpha', '--root', str(self.root))
                self.assertEqual(code, 1)
                self.assertEqual(result['status'], 'fail')
                code, result = self.run_cli('search', 'database', '--root', str(self.root))
                self.assertEqual(code, 0)
                self.assertEqual(result['results'], [])
                self.assertEqual(len(result['skipped_invalid']), 1)

    def test_yaml_quoted_and_multiline_values_are_accepted(self):
        (self.root / 'nested/alpha/SKILL.md').write_text(
            '---\nname: "alpha" # identity\ndescription: >-\n  Database architecture\n  helper.\n---\nname: ignored-in-body\n')
        self.assertEqual(self.run_cli('exact', 'alpha', '--root', str(self.root))[0], 0)
        self.assertEqual(len(self.run_cli('search', 'database', '--root', str(self.root))[1]['results']), 1)

    def test_missing_yaml_dependency_is_reported(self):
        original_import = __import__

        def without_yaml(name, *args, **kwargs):
            if name == 'yaml':
                raise ImportError('Unavailable in this environment')
            return original_import(name, *args, **kwargs)

        with patch('builtins.__import__', side_effect=without_yaml):
            code, result = self.run_cli('exact', 'alpha', '--root', str(self.root))
        self.assertEqual(code, 2)
        self.assertEqual(result['status'], 'unavailable')

    def test_path_and_symlink_escapes_are_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            folder = Path(outside)
            (folder / 'SKILL.md').write_text('---\nname: alpha\ndescription: Helper.\n---\n')
            with self.assertRaisesRegex(ValueError, 'escapes library root'):
                cli.manifest_for(self.root, {'id': 'alpha', 'path': str(folder)})
            try:
                (self.root / 'escape').symlink_to(folder, target_is_directory=True)
            except OSError:
                self.skipTest('Host cannot create symlinks')
            with self.assertRaisesRegex(ValueError, 'escapes library root'):
                cli.manifest_for(self.root, {'id': 'alpha', 'path': 'escape'})

    def test_installed_copy_works_outside_checkout(self):
        repo = Path(__file__).resolve().parents[1]
        dest = self.root / 'installed'
        installed = subprocess.run(
            [sys.executable, '-B', str(repo / 'scripts/skills.py'), 'install',
             '--skill', 'skill-loader', '--destination', str(dest)],
            cwd=self.root, capture_output=True, text=True)
        self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
        script = dest / 'skill-loader/scripts/library_query.py'
        for command, value in [('exact', 'alpha'), ('search', 'database')]:
            result = subprocess.run(
                [sys.executable, '-B', str(script), command, value, '--root', str(self.root)],
                cwd=dest, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'pass')
        (self.root / 'nested/alpha/SKILL.md').write_text('# No frontmatter\nname: alpha\n')
        result = subprocess.run(
            [sys.executable, '-B', str(script), 'exact', 'alpha', '--root', str(self.root)],
            cwd=dest, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'fail')


if __name__ == '__main__':
    unittest.main()
