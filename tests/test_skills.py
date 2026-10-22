"""Integration checks isolated from user profiles and real agent sessions."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('skills_cli', Path(__file__).resolve().parents[1] / 'scripts/skills.py')
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'source'
        self.dest = self.root / 'target'
        (self.repo / 'distribution').mkdir(parents=True)
        self.names = ['alpha', 'beta']
        (self.repo / 'distribution/catalog.json').write_text(json.dumps({'version': 1, 'release': '1.0.0', 'skills': self.names, 'bundles': {'pair': self.names}}))
        for name in self.names:
            d = self.repo / name
            (d / 'references').mkdir(parents=True)
            (d / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: Edit a selected document.\n---\n[Guide](references/guide.md)\n')
            (d / 'references/guide.md').write_text('Useful detail\n')
            (d / 'SKILL.proposed.md').write_text('Exclude proposals\n')
        self.patcher = patch.object(cli, 'REPO', self.repo)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def run_cli(self, *args):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = cli.main(list(args))
        return code, json.loads(out.getvalue())

    def install(self, *args):
        return self.run_cli('install', '--destination', str(self.dest), *args)

    def test_explicit_selection_and_unknown_name(self):
        self.assertEqual(self.install()[0], 1)
        self.assertEqual(self.install('--skill', '../alpha')[0], 1)
        self.assertFalse(self.dest.exists())

    def test_dry_run_no_destination_writes(self):
        code, data = self.install('--bundle', 'pair', '--dry-run')
        self.assertEqual(code, 0)
        self.assertEqual(len(data['plan']), 2)
        self.assertFalse(self.dest.exists())

    def test_copy_idempotence_and_isolation(self):
        self.assertEqual(self.install('--skill', 'alpha')[0], 0)
        self.assertFalse((self.dest / 'beta').exists())
        self.assertFalse((self.dest / 'alpha/SKILL.proposed.md').exists())
        self.assertEqual(self.install('--skill', 'alpha')[1]['plan'][0]['action'], 'unchanged')
        self.assertEqual(self.run_cli('doctor', '--destination', str(self.dest), '--skill', 'alpha')[0], 0)
        self.assertEqual(self.run_cli('doctor', '--destination', str(self.dest), '--all')[0], 1)

    def test_conflict_preflight_preserves_unmanaged_and_no_partial_batch(self):
        (self.dest / 'beta').mkdir(parents=True)
        marker = self.dest / 'beta/user.txt'
        marker.write_text('user data')
        self.assertEqual(self.install('--all')[0], 1)
        self.assertFalse((self.dest / 'alpha').exists())
        self.assertEqual(marker.read_text(), 'user data')

    def test_update_requires_flag_and_preserves_local_changes(self):
        self.assertEqual(self.install('--skill', 'alpha')[0], 0)
        source = self.repo / 'alpha/references/guide.md'
        source.write_text('New source\n')
        self.assertEqual(self.install('--skill', 'alpha')[0], 1)
        self.assertEqual(self.install('--skill', 'alpha', '--update')[0], 0)
        dest = self.dest / 'alpha/references/guide.md'
        dest.write_text('Local edit\n')
        self.assertEqual(self.install('--skill', 'alpha', '--update')[0], 1)
        self.assertEqual(dest.read_text(), 'Local edit\n')

    def test_release_change_requires_managed_update(self):
        self.assertEqual(self.install('--skill', 'alpha')[0], 0)
        catalog = self.repo / 'distribution/catalog.json'
        data = json.loads(catalog.read_text())
        data['release'] = '1.1.0'
        catalog.write_text(json.dumps(data))
        self.assertEqual(self.install('--skill', 'alpha')[0], 1)
        code, result = self.install('--skill', 'alpha', '--update')
        self.assertEqual(code, 0)
        self.assertEqual(result['plan'][0]['installed_release'], '1.0.0')
        state = json.loads((self.dest / cli.STATE).read_text())
        self.assertEqual(state['skills']['alpha']['release'], '1.1.0')

    def test_link_and_switch_to_copy(self):
        try:
            (self.root / 'probe').symlink_to(self.repo, target_is_directory=True)
        except OSError:
            self.skipTest('Host cannot create symlinks')
        self.assertEqual(self.install('--skill', 'alpha', '--mode', 'link')[0], 0)
        self.assertTrue((self.dest / 'alpha').is_symlink())
        self.assertEqual(self.install('--skill', 'alpha', '--mode', 'link')[1]['plan'][0]['action'], 'unchanged')
        self.assertEqual(self.install('--skill', 'alpha', '--update')[0], 0)
        self.assertFalse((self.dest / 'alpha').is_symlink())

    def test_invalid_manifest_and_missing_or_escaping_reference(self):
        f = self.repo / 'alpha/SKILL.md'
        for text in ['---\nname: [\n---\n', '---\nname: alpha\nname: beta\ndescription: edit\n---\n', '---\nname: alpha\ndescription: edit\n---\n[Missing](references/missing.md)', '---\nname: alpha\ndescription: edit\n---\n[Outside](../beta/SKILL.md)']:
            f.write_text(text)
            self.assertEqual(self.install('--skill', 'alpha')[0], 1)
        self.assertFalse(self.dest.exists())

    def test_destination_inside_source_rejected(self):
        self.assertEqual(self.run_cli('install', '--skill', 'alpha', '--destination', str(self.repo / 'alpha/nested'))[0], 1)

    def test_ambiguous_auto_detection(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(cli.shutil, 'which', return_value='/bin/tool'):
            self.assertEqual(self.run_cli('install', '--skill', 'alpha', '--project', str(self.dest))[0], 1)
        self.assertFalse(self.dest.exists())

    def test_agent_project_destinations(self):
        for agent in cli.AGENTS:
            project = self.root / agent
            code, data = self.run_cli('install', '--skill', 'alpha', '--agent', agent, '--project', str(project))
            self.assertEqual(code, 0)
            suffix = '.claude/skills' if agent == 'claude' else '.agents/skills'
            self.assertTrue((project / suffix / 'alpha/SKILL.md').is_file())

    def test_receipt_write_failure_restores_previous_package(self):
        self.assertEqual(self.install('--skill', 'alpha')[0], 0)
        before = (self.dest / 'alpha/references/guide.md').read_text()
        (self.repo / 'alpha/references/guide.md').write_text('Changed\n')
        with patch.object(cli, 'write_state', side_effect=OSError('disk failure')):
            self.assertEqual(self.install('--skill', 'alpha', '--update')[0], 1)
        self.assertEqual((self.dest / 'alpha/references/guide.md').read_text(), before)

    def test_doctor_detects_installed_copy_drift(self):
        self.assertEqual(self.install('--skill', 'alpha')[0], 0)
        (self.dest / 'alpha/references/guide.md').write_text('Modified after install')
        self.assertEqual(self.run_cli('doctor', '--destination', str(self.dest), '--skill', 'alpha')[0], 1)

    def test_filtered_manifest_has_only_selected_paths(self):
        code, data = self.run_cli('manifest', '--bundle', 'pair', '--exclude', 'beta')
        self.assertEqual(code, 0)
        self.assertEqual(data, {'entries': [{'path': str((self.repo / 'alpha').resolve())}]})
        self.assertFalse(self.dest.exists())

    def test_invalid_yaml_resource_blocks_install(self):
        (self.repo / 'alpha/examples').mkdir()
        (self.repo / 'alpha/examples/config.yml').write_text('format: [')
        self.assertEqual(self.install('--skill', 'alpha')[0], 1)
        self.assertFalse(self.dest.exists())

    def test_user_scope_in_isolated_home(self):
        expected = {'codex': '.agents/skills', 'claude': '.claude/skills', 'antigravity': '.gemini/config/skills', 'antigravity-cli': '.gemini/antigravity-cli/skills'}
        home = self.root / 'home'
        with patch.object(cli.Path, 'home', return_value=home):
            for agent, suffix in expected.items():
                self.assertEqual(self.run_cli('install', '--agent', agent, '--scope', 'user', '--skill', 'alpha')[0], 0)
                self.assertTrue((home / suffix / 'alpha/SKILL.md').is_file())

    def test_malformed_receipt_preserved(self):
        self.dest.mkdir()
        (self.dest / cli.STATE).write_text('[]')
        self.assertEqual(self.install('--skill', 'alpha')[0], 1)
        self.assertEqual((self.dest / cli.STATE).read_text(), '[]')


if __name__ == '__main__':
    unittest.main()
