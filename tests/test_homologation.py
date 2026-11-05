"""Technical authorization tests; all commits and installations are disposable fixtures."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml
import test_payload as historical

ROOT = historical.ROOT
FEATURE = ROOT/'ci/homologation.py'
P = 'ci/selections/prospective.json'


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2)+'\n').encode()


class HomologationTests(unittest.TestCase):
    @staticmethod
    def git(root, *args):
        env = {k:v for k,v in os.environ.items() if k in ('PATH', 'SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP', 'LANG')}
        env.update(GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0',
                   GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1')
        return subprocess.check_output(['git', '--no-optional-locks', '--no-replace-objects', '--no-lazy-fetch',
                                       '-c', 'core.autocrlf=false', '-C', str(root), *args], env=env,
                                      stderr=subprocess.PIPE)

    @classmethod
    def commit(cls, root, message):
        cls.git(root, 'add', '--all')
        cls.git(root, '-c', 'user.name=Synthetic homologation test',
                '-c', 'user.email=homologation@example.invalid', '-c', 'commit.gpgsign=false',
                '-c', 'core.hooksPath='+str(root/'.no-hooks'), 'commit', '-q', '-m', message)
        return cls.git(root, 'rev-parse', 'HEAD').decode().strip()

    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='meta-skills-homologation-test-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.template = Path(cls.temp.name).resolve()/'template'
        cls.git(ROOT, 'clone', '--local', '--no-hardlinks', '--quiet', str(ROOT), str(cls.template))
        (cls.template/'LICENSE').write_bytes(b'synthetic approved source\n')
        cls.s = cls.commit(cls.template, 'Synthetic source S')
        cls.selection = json.loads((cls.template/'ci/payload.json').read_bytes())
        cls.selection.update(profile='prospective', source_commit=cls.s)
        for entry in cls.selection['sources']:
            data = (cls.template/entry['path']).read_bytes()
            entry.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        selected = cls.template/P
        selected.parent.mkdir(parents=True, exist_ok=True)
        selected.write_bytes(encoded(cls.selection))
        cls.b = cls.commit(cls.template, 'Synthetic selection B')
        for rel in ['ci/homologation.py', '.github/workflows/homologacao.yml',
                    'tests/test_homologation.py', 'ci/README.md']:
            if (ROOT/rel).is_file():
                (cls.template/rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT/rel, cls.template/rel)
        (cls.template/'workflow-marker.txt').write_text('trusted workflow revision\n')
        cls.w = cls.commit(cls.template, 'Synthetic trusted workflow W')
        cls.h = hashlib.sha256(encoded(cls.selection)).hexdigest()

    def setUp(self):
        directory = tempfile.TemporaryDirectory(dir=self.temp.name)
        self.addCleanup(directory.cleanup)
        self.case = Path(directory.name).resolve()
        self.workflow, self.source = self.case/'workflow', self.case/'source'
        for root in (self.workflow, self.source):
            self.git(ROOT, 'clone', '--local', '--no-hardlinks', '--quiet', str(self.template), str(root))
        self.git(self.source, 'checkout', '--quiet', '--detach', self.s)
        self.work = self.case/'validation'
        self.tuple = dict(source_commit=self.s, selection_commit=self.b,
                          selection_path=P, selection_sha256=self.h)
        self.context = dict(GITHUB_EVENT_NAME='workflow_dispatch', GITHUB_REF='refs/heads/main',
                            GITHUB_REPOSITORY='talesgomes27/agent-skills-pipelines', GITHUB_SHA=self.w,
                            GITHUB_RUN_ID='123', GITHUB_RUN_ATTEMPT='1',
                            HOMOLOGACAO_TUPLA=json.dumps(self.tuple))

    def helper(self):
        self.assertTrue(FEATURE.is_file(), 'Missing trusted homologation orchestrator')
        spec = importlib.util.spec_from_file_location('homologation_under_test', FEATURE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def prepare(self, helper=None, context=None):
        return (helper or self.helper()).prepare(self.workflow, self.work, context or self.context)

    def validate(self, helper, prepared, source=None, context=None):
        return helper.validate(self.workflow, source or self.source, self.work,
                               prepared['snapshot_sha256'], context or self.context)

    def changed_selection(self, data):
        (self.workflow/P).write_bytes(data)
        commit = self.commit(self.workflow, 'Synthetic invalid selection')
        self.tuple.update(selection_commit=commit, selection_sha256=hashlib.sha256(data).hexdigest())
        self.context.update(GITHUB_SHA=commit, HOMOLOGACAO_TUPLA=json.dumps(self.tuple))

    def test_distinct_revisions_build_verify_and_install_all_eight_skills(self):
        helper = self.helper()
        prepared = self.prepare(helper)
        self.assertEqual(prepared['source_commit'], self.s)
        self.assertNotEqual(self.s, self.w)
        self.assertNotEqual(self.s, self.b)
        result = self.validate(helper, prepared)
        self.assertEqual(result['source_commit'], self.s)
        self.assertEqual(result['workflow_commit'], self.w)
        self.assertEqual(result['selection_commit'], self.b)
        self.assertEqual(result['selection_sha256'], self.h)
        self.assertEqual(result['files'], 84)
        self.assertIn('unpublished', result['status'])
        self.assertEqual((self.work/'extracted/LICENSE').read_bytes(), b'synthetic approved source\n')
        for name in ('meta-skills-2.0.0-candidate.tar.gz', 'payload-manifest.json', 'delivery.json'):
            self.assertEqual((self.work/'payload-a'/name).read_bytes(), (self.work/'payload-b'/name).read_bytes())
        for mode in ('copy', 'link'):
            self.assertTrue((self.work/(mode+'-integration')/'results.json').is_file())

    def test_untrusted_events_refs_repositories_and_workflow_sha_are_rejected(self):
        helper = self.helper()
        for key, value in [('GITHUB_EVENT_NAME', 'pull_request'), ('GITHUB_EVENT_NAME', 'push'),
                           ('GITHUB_EVENT_NAME', 'pull_request_target'), ('GITHUB_EVENT_NAME', 'workflow_run'),
                           ('GITHUB_REF', 'refs/heads/other'), ('GITHUB_REF', 'refs/tags/main'),
                           ('GITHUB_REPOSITORY', 'other/fork'), ('GITHUB_SHA', self.s),
                           ('GITHUB_RUN_ID', '0'), ('GITHUB_RUN_ATTEMPT', 'bad')]:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.prepare(helper, dict(self.context, **{key:value}))
            self.assertFalse(self.work.exists())

    def test_missing_malformed_duplicate_and_extra_tuple_fields_are_rejected(self):
        helper = self.helper()
        values = ['', 'null', '[]', '{bad', json.dumps(dict(self.tuple, approved=True)),
                  json.dumps({k:v for k,v in self.tuple.items() if k!='selection_sha256'}),
                  json.dumps(self.tuple)[:-1]+', "source_commit": "'+self.s+'"}']
        for value in values:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.prepare(helper, dict(self.context, HOMOLOGACAO_TUPLA=value))
            self.assertFalse(self.work.exists())

    def test_invalid_identity_paths_and_digest_fail_before_work_is_created(self):
        helper = self.helper()
        for key, value in [('source_commit', 'main'), ('source_commit', '0'*40),
                           ('selection_commit', '0'*40), ('selection_sha256', '0'*64),
                           ('selection_sha256', ''), ('selection_path', '../outside'),
                           ('selection_path', '/tmp/selection.json'), ('selection_path', 'C:/selection.json'),
                           ('selection_path', 'ci\\selection.json'), ('selection_path', 'ci/sel\nection.json')]:
            value = dict(self.tuple, **{key:value})
            with self.subTest(value=value), self.assertRaises((ValueError, subprocess.CalledProcessError)):
                self.prepare(helper, dict(self.context, HOMOLOGACAO_TUPLA=json.dumps(value)))
            self.assertFalse(self.work.exists())

    def test_selection_profile_and_declared_source_must_match_authorization(self):
        helper = self.helper()
        for key, value in [('profile', 'historical'), ('source_commit', self.b)]:
            selected = dict(self.selection, **{key:value})
            self.changed_selection(encoded(selected))
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.prepare(helper)
            self.assertFalse(self.work.exists())

    def test_selection_blob_size_is_checked_before_json_parsing(self):
        helper = self.helper()
        self.changed_selection(b'x'*2000001)
        with self.assertRaisesRegex(ValueError, 'size|Oversized'):
            self.prepare(helper)
        self.assertFalse(self.work.exists())

    def test_versioned_symlink_is_not_an_authorized_manifest(self):
        helper = self.helper()
        selected = self.workflow/P
        selected.unlink()
        selected.symlink_to('../../LICENSE')
        b = self.commit(self.workflow, 'Synthetic symlink selection')
        self.tuple.update(selection_commit=b, selection_sha256=hashlib.sha256(b'../../LICENSE').hexdigest())
        self.context.update(GITHUB_SHA=b, HOMOLOGACAO_TUPLA=json.dumps(self.tuple))
        with self.assertRaises(ValueError):
            self.prepare(helper)
        self.assertFalse(self.work.exists())

    def test_dirty_workflow_cannot_replace_versioned_selection(self):
        helper = self.helper()
        (self.workflow/P).write_bytes(b'untrusted local override')
        with self.assertRaises(ValueError):
            self.prepare(helper)
        self.assertFalse(self.work.exists())

    def test_environment_changes_do_not_replace_the_captured_tuple(self):
        helper = self.helper()
        prepared = self.prepare(helper)
        changed = dict(self.context, HOMOLOGACAO_TUPLA='invalid replacement')
        # Reject the wrong checkout before any build; the captured tuple must still require S.
        with self.assertRaisesRegex(ValueError, 'Checkout|Source'):
            self.validate(helper, prepared, source=self.workflow, context=changed)
        self.assertFalse((self.work/'payload-a').exists())
        snapshot = json.loads((self.work/'authorization.json').read_bytes())
        self.assertEqual(snapshot['tuple'], self.tuple)

    def test_snapshot_change_and_cross_attempt_replay_are_rejected(self):
        helper = self.helper()
        prepared = self.prepare(helper)
        for key, value in [('GITHUB_RUN_ID','124'), ('GITHUB_RUN_ATTEMPT','2')]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.validate(helper, prepared, context=dict(self.context, **{key:value}))
        p = self.work/'authorization.json'
        p.write_bytes(p.read_bytes()+b' ')
        with self.assertRaises(ValueError):
            self.validate(helper, prepared)
        self.assertFalse((self.work/'payload-a').exists())

    def test_dirty_source_and_wrong_generator_fail_before_build(self):
        helper = self.helper()
        prepared = self.prepare(helper)
        license_path = self.source/'LICENSE'
        original = license_path.read_bytes()
        license_path.write_bytes(b'dirty source\n')
        with self.assertRaises(ValueError):
            self.validate(helper, prepared)
        license_path.write_bytes(original)
        builder = self.workflow/'ci/build_payload.py'
        builder.write_bytes(builder.read_bytes()+b'\n# changed trusted generator\n')
        w = self.commit(self.workflow, 'Synthetic differing recipe')
        context = dict(self.context, GITHUB_SHA=w)
        # A newly prepared authorization still cannot mislabel a different executed recipe.
        other = self.case/'other-validation'
        new = helper.prepare(self.workflow, other, context)
        with self.assertRaisesRegex(ValueError, 'recipe|Recipe|generator'):
            helper.validate(self.workflow, self.source, other, new['snapshot_sha256'], context)
        self.assertFalse((other/'payload-a').exists())

    def test_linked_worktree_source_is_read_without_shared_metadata_changes(self):
        helper = self.helper()
        linked = self.case/'linked-source'
        self.git(self.workflow, 'worktree', 'add', '--quiet', '--detach', str(linked), self.s)
        prepared = self.prepare(helper)
        metadata = self.workflow/'.git'
        before = {str(p.relative_to(metadata)):hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in metadata.rglob('*') if p.is_file()}
        result = self.validate(helper, prepared, source=linked)
        after = {str(p.relative_to(metadata)):hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in metadata.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(result['source_commit'], self.s)
        self.assertTrue((linked/'.git').is_file())

    def test_artifact_tampering_stops_before_extraction_and_installation(self):
        helper = self.helper()
        prepared = self.prepare(helper)
        original = subprocess.run
        def tampered(command, *args, **kwargs):
            if any(Path(arg) == self.workflow/'ci/verify_payload.py' for arg in command):
                archive = self.work/'payload-a/meta-skills-2.0.0-candidate.tar.gz'
                archive.write_bytes(archive.read_bytes()+b'tampered')
            return original(command, *args, **kwargs)
        with patch.object(helper.subprocess, 'run', side_effect=tampered):
            with self.assertRaises(subprocess.CalledProcessError):
                self.validate(helper, prepared)
        self.assertFalse((self.work/'extracted').exists())
        self.assertFalse((self.work/'copy-integration').exists())

    def test_cli_rejects_authority_overrides_and_publishing(self):
        self.helper()
        for args in [['publish'], ['prepare', '--work', str(self.work), '--selection-sha', self.h]]:
            with self.subTest(args=args):
                p = subprocess.run([sys.executable, '-I', '-B', str(FEATURE), *args], capture_output=True)
                self.assertNotEqual(p.returncode, 0)
        self.assertFalse(self.work.exists())

    def test_hidden_installer_edit_cannot_report_installation_success(self):
        helper = self.helper()
        prepared = self.prepare(helper)
        installer = self.workflow/'ci/check_installation.py'
        self.git(self.workflow, 'update-index', '--assume-unchanged', 'ci/check_installation.py')
        installer.write_text('raise SystemExit(0)\n')
        self.assertEqual(self.git(self.workflow, 'status', '--porcelain'), b'')
        with self.assertRaises(ValueError):
            self.validate(helper, prepared)
        self.assertFalse((self.work/'payload-a').exists())
        self.assertFalse((self.work/'result.json').exists())

    def test_hidden_verifier_edit_is_rejected_before_import(self):
        helper = self.helper()
        path = self.workflow/'ci/verify_payload.py'
        marker = self.case/'uncommitted-verifier-executed'
        self.git(self.workflow, 'update-index', '--assume-unchanged', 'ci/verify_payload.py')
        path.write_bytes(('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n').encode()+path.read_bytes())
        self.assertEqual(self.git(self.workflow, 'status', '--porcelain'), b'')
        with self.assertRaises(ValueError):
            self.prepare(helper)
        self.assertFalse(marker.exists())
        self.assertFalse(self.work.exists())

    def test_fixture_git_ignores_inherited_repository_redirections(self):
        sentinel = self.case/'sentinel'
        self.git(ROOT, 'clone', '--local', '--no-hardlinks', '--quiet', str(self.template), str(sentinel))
        before = self.git(sentinel, 'rev-parse', 'HEAD')
        with patch.dict(os.environ, GIT_DIR=str(sentinel/'.git'), GIT_WORK_TREE=str(sentinel),
                        GIT_INDEX_FILE=str(sentinel/'.git/index')):
            intended = self.git(self.source, 'rev-parse', 'HEAD').decode().strip()
        self.assertEqual(intended, self.s)
        self.assertEqual(self.git(sentinel, 'rev-parse', 'HEAD'), before)

    def test_workflow_requires_manual_protected_job_without_authoritative_inputs(self):
        path = ROOT/'.github/workflows/homologacao.yml'
        self.assertTrue(path.is_file(), 'Missing protected manual workflow')
        workflow = yaml.safe_load(path.read_text())
        self.assertEqual(workflow['on'], {'workflow_dispatch':None})
        self.assertEqual(workflow['permissions'], {'contents':'read'})
        self.assertEqual(len(workflow['jobs']), 1)
        job = next(iter(workflow['jobs'].values()))
        self.assertEqual(job['environment'], 'homologacao')
        self.assertEqual(job['if'], "${{ github.event_name == 'workflow_dispatch' && github.ref == 'refs/heads/main' }}")
        checkouts = [s for s in job['steps'] if s.get('uses','').startswith('actions/checkout@')]
        self.assertEqual(len(checkouts), 2)
        self.assertEqual(checkouts[0]['with']['ref'], '${{ github.sha }}')
        self.assertEqual(checkouts[1]['with']['ref'], '${{ steps.prepare.outputs.source_commit }}')
        self.assertTrue(all(s['with']['persist-credentials'] is False for s in checkouts))
        prepare = next(s for s in job['steps'] if s.get('id')=='prepare')
        self.assertEqual(prepare['env']['HOMOLOGACAO_TUPLA'], '${{ vars.HOMOLOGACAO_TUPLA }}')
        self.assertNotIn('HOMOLOGACAO_TUPLA', workflow.get('env',{}))
