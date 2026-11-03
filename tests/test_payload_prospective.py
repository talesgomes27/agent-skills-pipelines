"""Synthetic selections/digests exercise the opt-in API; they are not release approval."""
import copy
from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import unittest
from unittest.mock import patch

import test_payload as historical


class ProspectiveTests(unittest.TestCase):
    def setUp(self):
        self.old = historical.PayloadTests()
        self.old.setUp()
        self.addCleanup(self.old.doCleanups)
        self.work, self.source = self.old.work, self.old.source
        self.frozen = (self.source/'ci/payload.json').read_bytes()
        self.selected = json.loads(self.frozen)
        self.selected.update(profile='prospective', source_commit=self.old.commit)
        (self.source/'LICENSE').write_bytes(b'artificial prospective fixture\n')
        entry = next(e for e in self.selected['sources'] if e['path'] == 'LICENSE')
        entry.update(bytes=len(b'artificial prospective fixture\n'), sha256=hashlib.sha256(b'artificial prospective fixture\n').hexdigest())
        (self.source/'ci/build_payload.py').write_bytes((historical.ROOT/'ci/build_payload.py').read_bytes())
        self.selection = self.work/'selection.json'
        self.write_selection()
        self.valid_bundle = self.work/'valid-prospective'
        self.build(output=self.valid_bundle)

    def write_selection(self):
        data = historical.builder.encoded(self.selected)
        self.selection.write_bytes(data)
        self.digest = hashlib.sha256(data).hexdigest()

    def build(self, output=None, **kwargs):
        args = dict(selection_path=self.selection, selection_sha=self.digest)
        args.update(kwargs)
        return historical.builder.build(self.source, output or self.work/'prospective',
                                        self.old.commit, '123', '1', **args)

    def verify(self, bundle=None, **kwargs):
        bundle = bundle or self.valid_bundle
        args = dict(source=self.source, bundle=bundle, commit=self.old.commit, run_id='123', attempt='1',
                    tar_sha=hashlib.sha256((bundle/historical.verifier.ARCHIVE).read_bytes()).hexdigest(),
                    manifest_sha=hashlib.sha256((bundle/'payload-manifest.json').read_bytes()).hexdigest(),
                    delivery_sha=hashlib.sha256((bundle/'delivery.json').read_bytes()).hexdigest(),
                    extract=self.work/'extract', selection_path=self.selection, selection_sha=self.digest)
        args.update(kwargs)
        return historical.verifier.verify(**args)

    def reject_both(self, reason, **kwargs):
        with self.assertRaisesRegex(ValueError, reason):
            self.build(**kwargs)
        with self.assertRaisesRegex(ValueError, reason):
            self.verify(**kwargs)
        self.assertFalse((self.work/'prospective').exists())
        self.assertFalse((self.work/'extract').exists())

    def test_valid_selection_and_deterministic_builds(self):
        delivery = self.build()
        self.build(output=self.work/'second')
        for name in (historical.verifier.ARCHIVE, 'payload-manifest.json', 'delivery.json'):
            self.assertEqual((self.work/'prospective'/name).read_bytes(), (self.work/'second'/name).read_bytes())
        result = self.verify(self.work/'prospective')
        self.assertEqual(result['files'], 84)
        self.assertEqual((self.work/'extract/LICENSE').read_bytes(), b'artificial prospective fixture\n')
        self.assertEqual(delivery['selection_sha256'], self.digest)
        self.assertEqual(delivery['generator_sha256'], hashlib.sha256((historical.ROOT/'ci/build_payload.py').read_bytes()).hexdigest())
        self.assertEqual(json.loads((self.work/'prospective/payload-manifest.json').read_bytes())['format'], 'meta-skills-ci-payload-v1')
        self.assertEqual(delivery['format'], 'meta-skills-ci-delivery-v1')
        self.assertEqual((self.source/'ci/payload.json').read_bytes(), self.frozen)

    def test_missing_or_orphan_expected_digest(self):
        self.reject_both('digest', selection_sha=None)
        self.reject_both('digest', selection_path=None)

    def test_wrong_digest_cannot_be_authorized_by_selection(self):
        self.reject_both('Selection digest mismatch', selection_sha='0'*64)
        self.selected['expected_sha256'] = self.digest
        self.write_selection()
        self.reject_both('Selection fields')

    def test_source_divergence(self):
        (self.source/'LICENSE').write_bytes(b'tampered source')
        self.reject_both('Changed source|Checkout differs')

    def test_invalid_paths_collisions_and_composition(self):
        original = copy.deepcopy(self.selected)
        for name in ('../outside', '/outside', 'C:\\outside', 'unexpected.txt', 'LICENSE', 'license'):
            with self.subTest(path=name):
                self.selected = copy.deepcopy(original)
                self.selected['sources'][1]['path'] = name
                self.write_selection()
                self.reject_both('Unsafe|composition|collision')
        self.selected = copy.deepcopy(original)
        self.selected['sources'].pop()
        self.write_selection()
        self.reject_both('Source composition')

    def test_bad_modes_hashes_sizes_and_profile_identity(self):
        original = copy.deepcopy(self.selected)
        for key, value in (('mode', '0o644'), ('sha256', 'bad'), ('bytes', -1), ('bytes', True)):
            with self.subTest(field=key, value=value):
                self.selected = copy.deepcopy(original)
                self.selected['sources'][0][key] = value
                self.write_selection()
                self.reject_both('Source size/digest/mode')
        for key, value in (('profile', 'historical'), ('source_commit', '2'*40), ('format', 'unknown'), ('mode_policy', 'different')):
            with self.subTest(field=key):
                self.selected = copy.deepcopy(original)
                self.selected[key] = value
                self.write_selection()
                self.reject_both('Selection profile/source identity' if key in ('profile', 'source_commit') else 'Incompatible selection')
        self.selected = copy.deepcopy(original)
        self.selected['baseline']['commit'] = '2'*40
        self.write_selection()
        self.reject_both('Incompatible selection baseline')

    def test_symlink_source_and_selection(self):
        source = self.source/'LICENSE'
        real = self.work/'real-license'
        source.rename(real)
        source.symlink_to(real)
        self.reject_both('symlink')
        source.unlink()
        real.rename(source)
        selected = self.work/'real-selection.json'
        self.selection.rename(selected)
        self.selection.symlink_to(selected)
        self.reject_both('symlink')

    def test_duplicate_json_keys_and_derived_contract(self):
        data = self.selection.read_bytes().replace(b'"profile": "prospective"', b'"profile": "prospective", "profile": "prospective"')
        self.selection.write_bytes(data)
        self.digest = hashlib.sha256(data).hexdigest()
        self.reject_both('Duplicate')
        self.selected['derived']['README.md']['template'] = '../outside'
        self.write_selection()
        self.reject_both('Incompatible selection derived')

    def test_unexpected_archive_content_rejected_before_extraction(self):
        for label, change in [('content', lambda items: [(m, b'x'*len(d) if m.name == 'LICENSE' else d) for m, d in items]),
                              ('extra', lambda items: items + [(tarfile.TarInfo('unexpected.txt'), b'')])]:
            with self.subTest(label=label):
                bundle = self.work/label
                self.old.bundle = bundle
                self.old.delivery = self.build(output=bundle)
                self.old.rewrite(change)
                with self.assertRaisesRegex(ValueError, 'Entry digest mismatch' if label == 'content' else 'Oversized/truncated decompressed tar'):
                    self.verify(bundle)
                self.assertFalse((self.work/'extract').exists())

    def test_selection_does_not_authorize_another_selection(self):
        a = self.work/'a'
        self.build(output=a)
        (self.source/'LICENSE').write_bytes(b'another authorized test selection\n')
        entry = next(e for e in self.selected['sources'] if e['path'] == 'LICENSE')
        data = (self.source/'LICENSE').read_bytes()
        entry.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        self.write_selection()
        self.build(output=self.work/'b')
        with self.assertRaisesRegex(ValueError, 'Delivery identity mismatch'):
            self.verify(a)
        self.assertFalse((self.work/'extract').exists())

    def test_no_opt_in_keeps_frozen_selection(self):
        with self.assertRaises(ValueError):
            historical.builder.build(self.source, self.work/'historical', self.old.commit, '123', '1')
        with self.assertRaises(ValueError):
            self.verify(selection_path=None, selection_sha=None)
        self.selection.write_bytes(self.frozen)
        self.digest = hashlib.sha256(self.frozen).hexdigest()
        self.reject_both('Selection fields')
        self.assertEqual((self.source/'ci/payload.json').read_bytes(), self.frozen)

    def test_generator_identity_cannot_name_another_recipe(self):
        p = self.source/'ci/build_payload.py'
        p.write_bytes(p.read_bytes() + b'\n# different recipe\n')
        self.reject_both('recipe identity')

    def test_cli_requires_both_selection_arguments(self):
        for name, extra in [('build_payload.py', ['--output', str(self.work/'cli-output')]),
                            ('verify_payload.py', ['--bundle', str(self.old.bundle), '--commit', self.old.commit,
                             '--run-id', '123', '--attempt', '1', '--tar-sha', '0'*64,
                             '--manifest-sha', '0'*64, '--delivery-sha', '0'*64])]:
            command = [sys.executable, '-B', str(historical.ROOT/'ci'/name), '--source', str(self.source),
                       '--selection', str(self.selection), *extra]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('selection', result.stderr.lower())
            self.assertIn('digest', result.stderr.lower())
            self.assertFalse((self.work/'cli-output').exists())

    def test_exact_historical_reproduction_uses_historical_recipe(self):
        source = self.work/'historical-source'
        frozen = json.loads(self.frozen)
        for rel in [e['path'] for e in frozen['sources']] + ['ci/payload.json', 'ci/PAYLOAD-README.md', 'ci/build_payload.py', 'ci/verify_payload.py']:
            p = source/rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(historical.historical_bytes(rel))
        def load_old(name):
            spec = importlib.util.spec_from_file_location('historical_'+name, source/'ci'/(name+'.py'))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        old_builder, old_verifier = load_old('build_payload'), load_old('verify_payload')
        a, b = self.work/'old-a', self.work/'old-b'
        delivery = old_builder.build(source, a, historical.HISTORICAL_REVISION, '123', '1')
        old_builder.build(source, b, historical.HISTORICAL_REVISION, '123', '1')
        for name in (old_verifier.ARCHIVE, 'payload-manifest.json', 'delivery.json'):
            self.assertEqual((a/name).read_bytes(), (b/name).read_bytes())
        self.assertEqual(delivery['generator_sha256'], hashlib.sha256(historical.historical_bytes('ci/build_payload.py')).hexdigest())
        result = old_verifier.verify(source, a, historical.HISTORICAL_REVISION, '123', '1', delivery['tar_sha256'],
                                     delivery['manifest_sha256'], hashlib.sha256((a/'delivery.json').read_bytes()).hexdigest())
        self.assertEqual(result['files'], 84)

    def test_cli_rejects_claimed_revision_with_uncommitted_recipe(self):
        source = self.work/'git-source'
        for rel in self.old.paths + ['ci/payload.json', 'ci/PAYLOAD-README.md']:
            p = source/rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(historical.historical_bytes(rel))
        (source/'ci/build_payload.py').write_bytes((historical.ROOT/'ci/build_payload.py').read_bytes())
        meta = source/'.git'
        (meta/'objects/info').mkdir(parents=True)
        objects = subprocess.check_output(
            ['git', '--no-optional-locks', '--no-replace-objects', '--no-lazy-fetch',
             'rev-parse', '--path-format=absolute', '--git-path', 'objects'],
            cwd=historical.ROOT, text=True).strip()
        (meta/'objects/info/alternates').write_bytes((objects+'\n').encode('utf-8'))
        (meta/'refs').mkdir()
        (meta/'HEAD').write_text(historical.HISTORICAL_REVISION+'\n')
        (meta/'config').write_text('[core]\n\tbare = false\n')
        self.selected = json.loads(self.frozen)
        self.selected.update(profile='prospective', source_commit=historical.HISTORICAL_REVISION)
        self.write_selection()
        for name, extra in [('build_payload.py', ['--output', str(self.work/'cli-output')]),
                            ('verify_payload.py', ['--bundle', str(self.old.bundle), '--commit', historical.HISTORICAL_REVISION,
                             '--run-id', '123', '--attempt', '1', '--tar-sha', '0'*64,
                             '--manifest-sha', '0'*64, '--delivery-sha', '0'*64, '--extract', str(self.work/'extract')])]:
            command = [sys.executable, '-B', str(historical.ROOT/'ci'/name), '--source', str(source),
                       '--selection', str(self.selection), '--selection-sha', self.digest, *extra]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Uncommitted input: ci/build_payload.py', result.stderr)
            self.assertFalse((self.work/'cli-output').exists())
            self.assertFalse((self.work/'extract').exists())

    def test_selection_encoding_and_size_are_consistent(self):
        original = historical.builder.encoded(self.selected)
        for encoding in ('utf-16', 'utf-32', 'utf-8-sig'):
            with self.subTest(encoding=encoding):
                data = original.decode().encode(encoding)
                self.selection.write_bytes(data)
                self.digest = hashlib.sha256(data).hexdigest()
                self.reject_both('(?i)utf')
        data = original + b' ' * 2000000
        self.selection.write_bytes(data)
        self.digest = hashlib.sha256(data).hexdigest()
        self.reject_both('oversized')

    def test_frozen_json_types_and_manifest_bytes_are_exact(self):
        self.selected['derived']['README.md']['bytes'] = 543.0
        self.write_selection()
        self.reject_both('Incompatible selection derived')
        manifest = self.valid_bundle/'payload-manifest.json'
        value = json.loads(manifest.read_bytes())
        value['readme']['bytes'] = 543.0
        data = historical.builder.encoded(value)
        manifest.write_bytes(data)
        delivery_path = self.valid_bundle/'delivery.json'
        delivery = json.loads(delivery_path.read_bytes())
        delivery.update(manifest_sha256=hashlib.sha256(data).hexdigest(), manifest_bytes=len(data))
        delivery_path.write_bytes(historical.builder.encoded(delivery))
        self.selected['derived']['README.md']['bytes'] = 543
        self.write_selection()
        with self.assertRaisesRegex(ValueError, 'Incompatible manifest'):
            self.verify()
        self.assertFalse((self.work/'extract').exists())

    def test_oversized_archive_rejected_without_partial_output(self):
        data = hashlib.shake_256(b'deterministic incompressible payload').digest(2000000)
        (self.source/'LICENSE').write_bytes(data)
        entry = next(e for e in self.selected['sources'] if e['path'] == 'LICENSE')
        entry.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        self.write_selection()
        with self.assertRaisesRegex(ValueError, 'Oversized archive'):
            self.build()
        self.assertFalse((self.work/'prospective').exists())

    def test_prospective_fields_cannot_activate_the_default(self):
        for entry in json.loads(self.frozen)['sources']:
            (self.source/entry['path']).write_bytes(historical.historical_bytes(entry['path']))
        recipe = self.source/'ci/build_payload.py'
        recipe.write_bytes(historical.historical_bytes('ci/build_payload.py'))
        frozen = json.loads(self.frozen)
        frozen.update(profile='prospective', source_commit=self.old.commit)
        (self.source/'ci/payload.json').write_bytes(historical.builder.encoded(frozen))
        spec = importlib.util.spec_from_file_location('old_recipe_for_negative', recipe)
        old_builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old_builder)
        old_builder.build(self.source, self.work/'old-profile', self.old.commit, '123', '1')
        with self.assertRaisesRegex(ValueError, 'Prospective selection requires explicit opt-in'):
            historical.builder.build(self.source, self.work/'historical', self.old.commit, '123', '1')
        with self.assertRaisesRegex(ValueError, 'Prospective selection requires explicit opt-in'):
            self.verify(self.work/'old-profile', selection_path=None, selection_sha=None)
        self.assertFalse((self.work/'historical').exists())
        self.assertFalse((self.work/'extract').exists())

    def cli(self, module, args, bad_mode=False):
        # Synthetic Git boundary: no commits are created; paths, modes and blob bytes are explicit.
        names = ['ci/payload.json', 'ci/PAYLOAD-README.md', 'ci/build_payload.py'] + self.old.paths
        blobs = {name: (self.source/name).read_bytes() for name in names}
        ids = {name: hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() for name, data in blobs.items()}
        def checked_git(command, **kwargs):
            self.assertEqual(command[:4], ['git', '--no-optional-locks', '--no-replace-objects', '--no-lazy-fetch'])
            op = command[4:]
            if op == ['rev-parse', 'HEAD']:
                result = self.old.commit.encode() + b'\n'
            elif op == ['cat-file', '-t', self.old.commit]:
                result = b'commit\n'
            elif op[:2] == ['ls-tree', '-rz']:
                result = b''.join(((('120000' if bad_mode and name == 'LICENSE' else '100644') + ' blob ' + ids[name] + '\t' + name).encode() + b'\0') for name in names)
            elif op[:2] == ['cat-file', 'blob']:
                result = next(data for name, data in blobs.items() if ids[name] == op[2])
            elif op[:1] == ['show']:
                result = blobs[op[1].split(':', 1)[1]]
            else:
                raise AssertionError('unexpected Git request: ' + repr(op))
            return result.decode() if kwargs.get('text') else result
        output = io.StringIO()
        with patch.object(sys, 'argv', ['payload', '--source', str(self.source), '--selection', str(self.selection), '--selection-sha', self.digest, *args]), \
             patch.object(module.subprocess, 'check_output', side_effect=checked_git), \
             patch.dict(os.environ, {'GITHUB_RUN_ID': '123', 'GITHUB_RUN_ATTEMPT': '1'}, clear=True), redirect_stdout(output):
            module.main()
        return json.loads(output.getvalue())

    def test_cli_positive_and_versioned_symlink_rejection(self):
        out = self.work/'cli-valid'
        built = self.cli(historical.builder, ['--output', str(out)])
        args = ['--bundle', str(out), '--commit', self.old.commit, '--run-id', '123', '--attempt', '1',
                '--tar-sha', built['tar_sha256'], '--manifest-sha', built['manifest_sha256'],
                '--delivery-sha', built['delivery_sha256'], '--extract', str(self.work/'cli-extract')]
        self.assertEqual(self.cli(historical.verifier, args)['files'], 84)
        self.assertEqual((self.work/'cli-extract/LICENSE').read_bytes(), b'artificial prospective fixture\n')
        with self.assertRaisesRegex(ValueError, 'Non-regular committed input'):
            self.cli(historical.builder, ['--output', str(self.work/'cli-invalid')], bad_mode=True)
        args[-1] = str(self.work/'invalid-extract')
        with self.assertRaisesRegex(ValueError, 'Non-regular committed input'):
            self.cli(historical.verifier, args, bad_mode=True)
        self.assertFalse((self.work/'cli-invalid').exists())
        self.assertFalse((self.work/'invalid-extract').exists())
