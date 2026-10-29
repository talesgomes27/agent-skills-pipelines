"""Candidate package controls, separate from the historical 62-test baseline.

All fixtures are disposable; the 40-character commit below is synthetic test data.
These tests do not run during the implementation-only stage.
"""
import copy
import gzip
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT/'ci'/(name+'.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load('build_payload')
verifier = load('verify_payload')


class PayloadTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name).resolve()
        self.source = self.work/'source'
        selected = json.loads((ROOT/'ci/payload.json').read_text(encoding='utf-8'))
        self.paths = [e['path'] for e in selected['sources']]
        for rel in self.paths + ['ci/payload.json', 'ci/PAYLOAD-README.md', 'ci/build_payload.py']:
            dst = self.source/rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/rel, dst)
        self.bundle = self.work/'bundle'
        self.commit = '1'*40
        self.delivery = builder.build(self.source, self.bundle, self.commit, '123', '1')

    def verify(self, **kw):
        args = dict(source=self.source, bundle=self.bundle, commit=self.commit,
                    run_id='123', attempt='1', tar_sha=self.delivery['tar_sha256'],
                    manifest_sha=self.delivery['manifest_sha256'], extract=self.work/'extract')
        args['delivery_sha'] = hashlib.sha256((self.bundle/'delivery.json').read_bytes()).hexdigest() if (self.bundle/'delivery.json').exists() else '0'*64
        args.update(kw)
        return verifier.verify(**args)

    def reject(self, reason=None):
        expected = (self.assertRaisesRegex(ValueError, reason) if reason is not None
                    else self.assertRaises((ValueError, OSError, KeyError, tarfile.TarError)))
        with expected:
            self.verify()
        self.assertFalse((self.work/'extract').exists(), 'Rejected package was extracted')

    def rewrite(self, change, preserve_extent=False):
        archive = self.bundle/verifier.ARCHIVE
        original = gzip.decompress(archive.read_bytes()) if preserve_extent else None
        with tarfile.open(archive, 'r:gz') as tar:
            items = [(copy.copy(m), tar.extractfile(m).read()) for m in tar]
        if preserve_extent:
            peers = {m.name: (original[m.offset:m.offset+512], data) for m, data in items}
        items = change(items)
        with archive.open('wb') as raw:
            with gzip.GzipFile(fileobj=raw, filename='', mode='wb', mtime=0) as gz:
                with tarfile.open(fileobj=gz, mode='w', format=tarfile.USTAR_FORMAT) as tar:
                    for member, data in items:
                        tar.addfile(member, io.BytesIO(data))
        if preserve_extent:
            changed = gzip.decompress(archive.read_bytes())
            self.assertLessEqual(len(changed), len(original))
            padded = changed + bytes(len(original) - len(changed))
            archive.write_bytes(gzip.compress(padded, mtime=0))
            self.assertEqual(len(gzip.decompress(archive.read_bytes())), len(original))
            with tarfile.open(archive, 'r:gz') as tar:
                for member in tar:
                    header = padded[member.offset:member.offset+512]
                    self.assertEqual(header[257:265], b'ustar\x0000')
                    if member.isfile():
                        self.assertEqual(header, peers[member.name][0])
                        self.assertEqual(tar.extractfile(member).read(), peers[member.name][1])
        self.delivery['tar_sha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
        self.delivery['tar_bytes'] = archive.stat().st_size
        (self.bundle/'delivery.json').write_bytes(builder.encoded(self.delivery))

    def test_positive_and_two_equivalent_builds(self):
        other = self.work/'second'
        builder.build(self.source, other, self.commit, '123', '1')
        for name in (verifier.ARCHIVE, 'payload-manifest.json', 'delivery.json'):
            self.assertEqual((self.bundle/name).read_bytes(), (other/name).read_bytes())
        self.assertEqual(self.verify()['files'], 84)
        self.assertEqual((self.work/'extract'/verifier.Q17).read_bytes(), (ROOT/verifier.Q17).read_bytes())

    def test_package_digest_mismatch(self):
        with (self.bundle/verifier.ARCHIVE).open('ab') as out:
            out.write(b'tamper')
        self.reject()

    def test_missing_source(self):
        (self.source/self.paths[0]).unlink()
        with self.assertRaises(FileNotFoundError):
            builder.build(self.source, self.work/'missing', self.commit, '123', '1')
        self.reject()

    def test_source_hash_mismatch(self):
        (self.source/self.paths[0]).write_bytes(b'tampered source')
        with self.assertRaises(ValueError):
            builder.build(self.source, self.work/'changed', self.commit, '123', '1')
        self.reject()

    def test_extra_entry(self):
        def extra(items):
            m = tarfile.TarInfo('unexpected.txt')
            m.mode = 0o664
            return items+[(m, b'')]
        self.rewrite(extra)
        self.reject()

    def test_duplicate_entry(self):
        self.rewrite(lambda items: items + [items[0]])
        self.reject()

    def test_case_collision(self):
        def collision(items):
            m, data = items[0]
            duplicate = copy.copy(m)
            duplicate.name = m.name.lower()
            return items + [(duplicate, data)]
        self.rewrite(collision)
        self.reject()

    def test_traversal_absolute_and_windows_paths(self):
        for name in ('../escape', '/absolute', 'C:/escape', 'x\\escape', 'x//escape', './escape'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                verifier.path_ok(name)
        def traversal(items):
            items[0][0].name = '../escape'
            return items
        self.rewrite(traversal)
        self.reject()
        self.assertFalse((self.work/'escape').exists())

    def test_symlink_and_special_entries(self):
        def link(items):
            items[0][0].type = tarfile.SYMTYPE
            items[0][0].linkname = '/outside'
            items[0][0].size = 0
            return items
        self.rewrite(link, preserve_extent=True)
        with tarfile.open(self.bundle/verifier.ARCHIVE, 'r:gz') as tar:
            members = tar.getmembers()
            self.assertEqual([m.name for m in members], sorted(self.paths + ['README.md', 'payload-manifest.json']))
            self.assertEqual([m.name for m in members if not m.isfile()], ['LICENSE'])
            self.assertTrue(tar.getmember('LICENSE').issym())
            self.assertEqual(tar.getmember('LICENSE').linkname, '/outside')
            self.assertEqual(tar.getmember('LICENSE').size, 0)
        self.reject(r'^Non-USTAR/extended header$')

    def test_special_file(self):
        def special(items):
            items[0][0].type = tarfile.FIFOTYPE
            items[0][0].size = 0
            return items
        self.rewrite(special, preserve_extent=True)
        with tarfile.open(self.bundle/verifier.ARCHIVE, 'r:gz') as tar:
            members = tar.getmembers()
            self.assertEqual([m.name for m in members], sorted(self.paths + ['README.md', 'payload-manifest.json']))
            self.assertEqual([m.name for m in members if not m.isfile()], ['LICENSE'])
            self.assertTrue(tar.getmember('LICENSE').isfifo())
            self.assertEqual(tar.getmember('LICENSE').linkname, '')
            self.assertEqual(tar.getmember('LICENSE').size, 0)
        self.reject(r'^Non-USTAR/extended header$')

    def test_mode_mismatch(self):
        def mode(items):
            items[0][0].mode = 0o644
            return items
        self.rewrite(mode)
        self.reject()

    def test_incompatible_manifest(self):
        path = self.bundle/'payload-manifest.json'
        value = json.loads(path.read_text())
        value['format'] = 'unknown'
        data = builder.encoded(value)
        path.write_bytes(data)
        self.delivery['manifest_sha256'] = hashlib.sha256(data).hexdigest()
        self.delivery['manifest_bytes'] = len(data)
        (self.bundle/'delivery.json').write_bytes(builder.encoded(self.delivery))
        self.reject()

    def test_manifest_digest_mismatch(self):
        (self.bundle/'payload-manifest.json').write_bytes(b'{}')
        self.reject()

    def test_delivery_digest_mismatch(self):
        expected = hashlib.sha256((self.bundle/'delivery.json').read_bytes()).hexdigest()
        with (self.bundle/'delivery.json').open('ab') as out:
            out.write(b' ')
        with self.assertRaises(ValueError):
            self.verify(delivery_sha=expected)
        self.assertFalse((self.work/'extract').exists())

    def test_hidden_data_after_tar_end(self):
        archive = self.bundle/verifier.ARCHIVE
        data = gzip.decompress(archive.read_bytes())
        archive.write_bytes(gzip.compress(data[:-1]+b'x', mtime=0))
        self.delivery['tar_sha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
        self.delivery['tar_bytes'] = archive.stat().st_size
        (self.bundle/'delivery.json').write_bytes(builder.encoded(self.delivery))
        self.reject()

    def test_decompression_budget(self):
        archive = self.bundle/verifier.ARCHIVE
        data = gzip.decompress(archive.read_bytes())
        archive.write_bytes(gzip.compress(data + bytes(10240), mtime=0))
        self.delivery['tar_sha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
        self.delivery['tar_bytes'] = archive.stat().st_size
        (self.bundle/'delivery.json').write_bytes(builder.encoded(self.delivery))
        self.reject()

    def test_derived_readme_changed(self):
        def altered(items):
            for index, (member, data) in enumerate(items):
                if member.name == 'README.md':
                    items[index] = (member, b'x'*len(data))
            return items
        self.rewrite(altered)
        self.reject()

    def test_incomplete_artifact(self):
        (self.bundle/'delivery.json').unlink()
        self.reject()

    def test_wrong_commit(self):
        with self.assertRaises(ValueError):
            self.verify(commit='2'*40)
        self.assertFalse((self.work/'extract').exists())

    def test_wrong_run_or_attempt(self):
        for params in ({'run_id': '124'}, {'attempt': '2'}):
            with self.subTest(params=params), self.assertRaises(ValueError):
                self.verify(**params)
        self.assertFalse((self.work/'extract').exists())

    def test_extraction_error_preserves_existing_destination(self):
        dest = self.work/'extract'
        dest.mkdir()
        (dest/'user').write_bytes(b'preserve')
        with self.assertRaises(FileExistsError):
            self.verify()
        self.assertEqual(list(dest.iterdir()), [dest/'user'])
        self.assertEqual((dest/'user').read_bytes(), b'preserve')
        alias = self.work/'untrusted-parent'
        alias.symlink_to(self.work, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, r'^Extraction parent symlink$'):
            self.verify(extract=alias/'not-created')
        self.assertFalse((self.work/'not-created').exists())
        self.assertEqual((dest/'user').read_bytes(), b'preserve')

    def test_missing_q17(self):
        self.rewrite(lambda items: [(m,d) for m,d in items if m.name != verifier.Q17], preserve_extent=True)
        with tarfile.open(self.bundle/verifier.ARCHIVE, 'r:gz') as tar:
            members = tar.getmembers()
            names = [m.name for m in members]
            self.assertNotIn(verifier.Q17, names)
            self.assertEqual(names, sorted(set(self.paths + ['README.md', 'payload-manifest.json']) - {verifier.Q17}))
            self.assertTrue(all(m.isfile() for m in members))
        self.reject(r'^Missing/unsorted entries$')

    def test_del_entry(self):
        def del_file(items):
            m = tarfile.TarInfo('subagent-optimation/DEL-010.txt')
            m.mode = 0o664
            return items+[(m, b'')]
        self.rewrite(del_file)
        self.reject()

    def test_silent_mode_policy_change(self):
        p = self.source/'ci/payload.json'
        selection = json.loads(p.read_text())
        selection['sources'][0]['mode'] = '0o644'
        p.write_bytes(builder.encoded(selection))
        with self.assertRaises(ValueError):
            builder.build(self.source, self.work/'newmode', self.commit, '123', '1')
        self.reject()

    def test_wrong_size(self):
        def size(items):
            items[0][0].size += 1
            m,d = items[0]
            items[0] = (m, d+b'x')
            return items
        self.rewrite(size)
        self.reject()


if __name__ == '__main__':
    unittest.main()
