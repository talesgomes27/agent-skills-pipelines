"""Validation-only CI integration; synthetic commits live exclusively in disposable repositories."""
import copy
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


def load(name):
    spec = importlib.util.spec_from_file_location(name, historical.ROOT/'ci'/(name+'.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


adapter = load('payload_ci')


def copy_test_source(source, destination):
    shutil.copytree(source, destination, symlinks=True,
                    ignore=lambda folder, names: {'.git'} if Path(folder) == source else set())
    if any(path.is_symlink() for path in destination.rglob('*')):
        raise ValueError('Symlink in writable test source')


class CIIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='meta-skills-ci-test-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.template = Path(cls.temp.name).resolve()/'template'
        copy_test_source(historical.ROOT, cls.template)
        objects = subprocess.check_output(['git', '--no-optional-locks', '-C', str(historical.ROOT), 'rev-parse',
                                           '--path-format=absolute', '--git-path', 'objects'], text=True).strip()
        meta = cls.template/'.git'
        meta.mkdir()
        shutil.copytree(objects, meta/'objects')
        (meta/'refs').mkdir()
        (meta/'HEAD').write_text(historical.HISTORICAL_REVISION+'\n')
        (meta/'config').write_text('[core]\n\tbare = false\n\tautocrlf = false\n\tlogallrefupdates = false\n')
        cls.paths = [e['path'] for e in json.loads(historical.historical_bytes('ci/payload.json'))['sources']]
        for rel in cls.paths:
            (cls.template/rel).write_bytes(historical.historical_bytes(rel))
        cls.historical_commit = cls.commit(cls.template, 'Synthetic historical validation source')
        for rel in cls.paths:
            (cls.template/rel).write_bytes((historical.ROOT/rel).read_bytes())
        (cls.template/'LICENSE').write_bytes(b'synthetic CI prospective content\n')
        cls.source_commit = cls.commit(cls.template, 'Synthetic prospective validation source')
        selection = json.loads((cls.template/'ci/payload.json').read_bytes())
        selection.update(profile='prospective', source_commit=cls.source_commit)
        for entry in selection['sources']:
            data = (cls.template/entry['path']).read_bytes()
            entry.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        cls.selection_path = 'ci/proposed-test-selection.json'
        cls.selection_bytes = historical.builder.encoded(selection)
        with (cls.template/cls.selection_path).open('xb') as selected:
            selected.write(cls.selection_bytes)
        cls.selection_commit = cls.commit(cls.template, 'Synthetic proposed selection, not release approval')
        cls.selection_sha = hashlib.sha256(cls.selection_bytes).hexdigest()

    @staticmethod
    def git(root, *args):
        return subprocess.check_output(['git', '--no-optional-locks', '--no-replace-objects', '--no-lazy-fetch',
                                        '-C', str(root), *args], env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))

    @classmethod
    def commit(cls, root, message):
        cls.git(root, 'add', '--all')
        cls.git(root, '-c', 'user.name=Synthetic CI test', '-c', 'user.email=ci-test@example.invalid',
                '-c', 'core.hooksPath='+str(root/'.git/no-hooks'),
                '-c', 'commit.gpgsign=false', 'commit', '-q', '-m', message)
        return cls.git(root, 'rev-parse', 'HEAD').decode().strip()

    def setUp(self):
        directory = tempfile.TemporaryDirectory(dir=self.temp.name)
        self.addCleanup(directory.cleanup)
        self.work = Path(directory.name).resolve()
        self.repo = self.work/'repo'
        subprocess.run(['git', 'clone', '--local', '--no-hardlinks', '--quiet', str(self.template), str(self.repo)],
                       check=True, capture_output=True)
        self.git(self.repo, 'checkout', '--quiet', '--detach', self.source_commit)
        self.context = dict(GITHUB_EVENT_NAME='workflow_dispatch', CI_SOURCE_COMMIT=self.source_commit,
                            GITHUB_SHA=self.source_commit,
                            CI_SELECTION_COMMIT=self.selection_commit, CI_SELECTION_PATH=self.selection_path,
                            CI_SELECTION_SHA=self.selection_sha, GITHUB_RUN_ID='123', GITHUB_RUN_ATTEMPT='1')

    def build(self, name='bundle', context=None):
        return adapter.run('build', ['--output', str(self.work/name)], self.repo, context or self.context)

    def verify(self, bundle='bundle', context=None, extract='extracted'):
        folder = self.work/bundle
        delivery = json.loads((folder/'delivery.json').read_bytes())
        return adapter.run('verify', ['--bundle', str(folder), '--run-id', '123', '--attempt', '1',
                                     '--tar-sha', delivery['tar_sha256'], '--manifest-sha', delivery['manifest_sha256'],
                                     '--delivery-sha', hashlib.sha256((folder/'delivery.json').read_bytes()).hexdigest(),
                                     '--extract', str(self.work/extract)], self.repo, context or self.context)

    def test_real_committed_prospective_production_verification_and_determinism(self):
        a, b = self.build(), self.build('second')
        for name in (historical.verifier.ARCHIVE, 'payload-manifest.json', 'delivery.json'):
            self.assertEqual((self.work/'bundle'/name).read_bytes(), (self.work/'second'/name).read_bytes())
        self.assertEqual(a['source_commit'], self.source_commit)
        self.assertEqual(a['selection_sha256'], self.selection_sha)
        self.assertIn('unpublished', a['status'])
        self.assertEqual(self.verify()['files'], 84)
        self.assertEqual((self.work/'extracted/LICENSE').read_bytes(), b'synthetic CI prospective content\n')

    def test_historical_default_with_committed_source(self):
        self.git(self.repo, 'checkout', '--quiet', '--detach', self.historical_commit)
        context = dict(GITHUB_EVENT_NAME='push', CI_SOURCE_COMMIT=self.historical_commit, GITHUB_SHA=self.historical_commit,
                       GITHUB_RUN_ID='123', GITHUB_RUN_ATTEMPT='1')
        self.build(context=context)
        self.assertEqual(self.verify(context=context)['files'], 84)
        self.assertEqual((self.work/'extracted/LICENSE').read_bytes(), historical.historical_bytes('LICENSE'))

    def test_digest_and_revision_fail_before_build(self):
        for key, value in [('CI_SELECTION_SHA', ''), ('CI_SELECTION_SHA', '0'*64),
                           ('CI_SOURCE_COMMIT', self.selection_commit), ('CI_SELECTION_COMMIT', '0'*40),
                           ('CI_SELECTION_PATH', '../outside')]:
            with self.subTest(field=key, value=value):
                context = dict(self.context, **{key:value})
                with self.assertRaises((ValueError, subprocess.CalledProcessError)):
                    self.build(context=context)
                self.assertFalse((self.work/'bundle').exists())

    def test_pr_and_privileged_events_cannot_use_dispatch_values_as_approval(self):
        for event in ('pull_request', 'pull_request_target', 'workflow_run'):
            with self.subTest(event=event):
                context = dict(self.context, GITHUB_EVENT_NAME=event)
                with self.assertRaises(ValueError):
                    self.build(context=context)
                self.assertFalse((self.work/'bundle').exists())
        for operation in ('publish', 'release', 'approved-delivery'):
            with self.assertRaises(ValueError):
                adapter.run(operation, [], self.repo, self.context)

    def test_transport_cannot_supply_its_own_selection_or_commit(self):
        for args in (['--selection', 'artifact/selection.json'], ['--selection-sha='+self.selection_sha],
                     ['--source', 'artifact'], ['--commit='+self.selection_commit], ['--sou=artifact'],
                     ['--comm='+self.selection_commit], ['--selection-s='+self.selection_sha]):
            with self.subTest(args=args), self.assertRaises(ValueError):
                adapter.run('build', args, self.repo, self.context)

    def test_selection_is_read_from_versioned_commit_not_worktree(self):
        (self.repo/self.selection_path).write_text('untrusted transported bytes')
        self.build()
        self.assertEqual(self.verify()['files'], 84)

    def test_cross_selection_and_dirty_source_rejected(self):
        self.build()
        changed = json.loads(self.selection_bytes)
        changed['source_commit'] = self.historical_commit
        (self.repo/self.selection_path).write_bytes(historical.builder.encoded(changed))
        commit = self.commit(self.repo, 'Synthetic incompatible selection')
        digest = hashlib.sha256((self.repo/self.selection_path).read_bytes()).hexdigest()
        self.git(self.repo, 'checkout', '--quiet', '--detach', self.source_commit)
        context = dict(self.context, CI_SELECTION_COMMIT=commit, CI_SELECTION_SHA=digest)
        with self.assertRaises(subprocess.CalledProcessError):
            self.verify(context=context)
        self.assertFalse((self.work/'extracted').exists())
        (self.repo/'LICENSE').write_bytes(b'divergent source')
        with self.assertRaises(subprocess.CalledProcessError):
            self.build('dirty')
        self.assertFalse((self.work/'dirty').exists())

    def test_prospective_copy_link_selective_upgrade_and_recovery(self):
        self.build()
        self.verify()
        installation = load('check_installation')
        for mode in ('copy', 'link'):
            installation.run(self.repo, self.work/'extracted', self.work/('install-'+mode), mode, recovery=True)

    def test_historical_copy_link_upgrade_and_recovery(self):
        self.git(self.repo, 'checkout', '--quiet', '--detach', self.historical_commit)
        context = dict(GITHUB_EVENT_NAME='push', CI_SOURCE_COMMIT=self.historical_commit, GITHUB_SHA=self.historical_commit,
                       GITHUB_RUN_ID='123', GITHUB_RUN_ATTEMPT='1')
        self.build(context=context)
        self.verify(context=context)
        installation = load('check_installation')
        for mode in ('copy', 'link'):
            installation.run(self.repo, self.work/'extracted', self.work/('historical-'+mode), mode, recovery=True)

    def test_workflow_is_validation_only_and_consumers_share_selection_context(self):
        workflow = yaml.safe_load((historical.ROOT/'.github/workflows/ci.yml').read_text())
        self.assertEqual(workflow['permissions'], {'contents':'read'})
        self.assertEqual(set(workflow['on']), {'push','pull_request','workflow_dispatch'})
        for job in workflow['jobs'].values():
            for step in job['steps']:
                if step.get('uses','').startswith('actions/checkout@'):
                    self.assertFalse(step['with']['persist-credentials'])
                    self.assertEqual(step['with']['ref'], '${{ github.sha }}')
        self.assertNotIn('source_commit', workflow['on']['workflow_dispatch']['inputs'])
        text = (historical.ROOT/'.github/workflows/ci.yml').read_text()
        self.assertEqual(text.count('ci/payload_ci.py build'), 2)
        self.assertEqual(text.count('ci/payload_ci.py verify'), 3)
        self.assertNotIn('secrets.', text)
        self.assertNotIn('pull_request_target:', text)
        self.assertNotIn('workflow_run:', text)

    def test_dispatch_cannot_execute_another_revision_in_its_cache_context(self):
        context = dict(self.context, GITHUB_SHA=self.selection_commit)
        with self.assertRaisesRegex(ValueError, 'Workflow source revision mismatch'):
            self.build(context=context)
        self.assertFalse((self.work/'bundle').exists())

    def test_blob_limit_precedes_git_blob_read(self):
        data = b'x' * 2000001
        (self.repo/self.selection_path).write_bytes(data)
        commit = self.commit(self.repo, 'Synthetic oversized selection')
        self.git(self.repo, 'checkout', '--quiet', '--detach', self.source_commit)
        context = dict(self.context, CI_SELECTION_COMMIT=commit, CI_SELECTION_SHA=hashlib.sha256(data).hexdigest())
        query = adapter.subprocess.check_output
        calls = []
        def observed(command, **kwargs):
            calls.append(command)
            return query(command, **kwargs)
        with patch.object(adapter.subprocess, 'check_output', side_effect=observed):
            with self.assertRaisesRegex(ValueError, 'Oversized versioned selection'):
                self.build(context=context)
        self.assertFalse(any(cmd[4:6] == ['cat-file', 'blob'] for cmd in calls))
        self.assertFalse((self.work/'bundle').exists())

    def test_symlink_runner_temp_is_resolved(self):
        real = self.work/'real-temp'
        real.mkdir()
        alias = self.work/'temp-alias'
        alias.symlink_to(real, target_is_directory=True)
        with patch.object(adapter.tempfile, 'tempdir', str(alias)):
            self.build()
            self.assertEqual(self.verify()['files'], 84)

    def test_writable_fixture_rejects_symlinks_without_external_writes(self):
        incoming = self.work/'incoming'
        (incoming/'ci').mkdir(parents=True)
        marker = self.work/'external-marker'
        marker.write_bytes(b'preserve external bytes')
        (incoming/'ci/proposed-test-selection.json').symlink_to(marker)
        with self.assertRaisesRegex(ValueError, 'Symlink in writable test source'):
            copy_test_source(incoming, self.work/'isolated-copy')
        self.assertEqual(marker.read_bytes(), b'preserve external bytes')

    def test_pr_and_branch_proposals_are_deterministic_and_unapproved(self):
        for event, ref in [('pull_request', 'refs/pull/2/merge'),
                           ('push', 'refs/heads/codex/pragmatic-prospective')]:
            with self.subTest(event=event):
                context = dict(GITHUB_EVENT_NAME=event, GITHUB_REF=ref,
                               CI_SOURCE_COMMIT=self.source_commit, GITHUB_SHA=self.source_commit,
                               GITHUB_RUN_ID='123', GITHUB_RUN_ATTEMPT='1')
                with self.assertRaises(subprocess.CalledProcessError):
                    self.build(event+'-default', context=context)
                self.assertFalse((self.work/(event+'-default')).exists())
                context['CI_PROSPECTIVE_VALIDATION'] = 'true'
                a = self.build(event+'-a', context=context)
                b = self.build(event+'-b', context=context)
                self.assertEqual(a['source_commit'], self.source_commit)
                self.assertEqual(a['selection_sha256'], self.selection_sha)
                self.assertIn('unpublished', a['status'])
                for name in (historical.verifier.ARCHIVE, 'payload-manifest.json', 'delivery.json'):
                    self.assertEqual((self.work/(event+'-a')/name).read_bytes(),
                                     (self.work/(event+'-b')/name).read_bytes())
                self.assertEqual(self.verify(event+'-a', context=context, extract=event+'-extracted')['files'], 84)
                self.assertEqual((self.work/(event+'-extracted')/'LICENSE').read_bytes(),
                                 b'synthetic CI prospective content\n')

    def test_proposal_bootstrap_cannot_override_selection_or_use_privileged_context(self):
        for event, ref in [('local', ''), ('workflow_dispatch', 'refs/heads/codex/pragmatic-prospective'),
                           ('push', 'refs/heads/main'), ('push', 'refs/tags/proposed'),
                           ('pull_request_target', 'refs/heads/main'), ('workflow_run', 'refs/heads/main')]:
            context = dict(GITHUB_EVENT_NAME=event, GITHUB_REF=ref, CI_PROSPECTIVE_VALIDATION='true',
                           CI_SOURCE_COMMIT=self.source_commit, GITHUB_SHA=self.source_commit)
            with self.subTest(event=event, ref=ref), self.assertRaises(ValueError):
                self.build(context=context)
            self.assertFalse((self.work/'bundle').exists())
        context = dict(self.context, GITHUB_EVENT_NAME='pull_request', GITHUB_REF='refs/pull/2/merge',
                       CI_PROSPECTIVE_VALIDATION='true')
        with self.assertRaisesRegex(ValueError, 'Cannot combine'):
            self.build(context=context)
        self.assertFalse((self.work/'bundle').exists())

    def test_proposal_bootstrap_rejects_wrong_sha_and_uncommitted_sources(self):
        context = dict(GITHUB_EVENT_NAME='pull_request', GITHUB_REF='refs/pull/2/merge',
                       CI_PROSPECTIVE_VALIDATION='true', CI_SOURCE_COMMIT=self.source_commit,
                       GITHUB_SHA=self.selection_commit, GITHUB_RUN_ID='123', GITHUB_RUN_ATTEMPT='1')
        with self.assertRaisesRegex(ValueError, 'Workflow source revision mismatch'):
            self.build(context=context)
        context['GITHUB_SHA'] = self.source_commit
        (self.repo/'LICENSE').write_bytes(b'dirty proposed source')
        with self.assertRaises(subprocess.CalledProcessError):
            self.build(context=context)
        self.assertFalse((self.work/'bundle').exists())

    def test_proposal_bootstrap_rejects_gitlinks_before_formatting_commits(self):
        self.git(self.repo, 'update-index', '--add', '--cacheinfo',
                 '160000,'+self.historical_commit+',LICENSE')
        self.git(self.repo, '-c', 'user.name=Synthetic CI test',
                 '-c', 'user.email=ci-test@example.invalid',
                 '-c', 'core.hooksPath='+str(self.repo/'.git/no-hooks'),
                 '-c', 'commit.gpgsign=false', 'commit', '-q', '-m', 'Synthetic non-blob source')
        commit = self.git(self.repo, 'rev-parse', 'HEAD').decode().strip()
        context = dict(GITHUB_EVENT_NAME='pull_request', GITHUB_REF='refs/pull/2/merge',
                       CI_PROSPECTIVE_VALIDATION='true', CI_SOURCE_COMMIT=commit,
                       GITHUB_SHA=commit, GITHUB_RUN_ID='123', GITHUB_RUN_ATTEMPT='1')
        with self.assertRaises(subprocess.CalledProcessError) as rejected:
            self.build(context=context)
        self.assertEqual(rejected.exception.cmd[0], 'git')
        self.assertFalse((self.work/'bundle').exists())
