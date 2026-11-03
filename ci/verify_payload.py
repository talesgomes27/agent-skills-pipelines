"""Independent Python 3.9 verifier. Validate every byte before optional extraction."""
import argparse
import gzip
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tarfile

BASELINE_RECORDS_SHA = '8182c53b97c5c31dd3cd4f4364b5f1d4f6657aaaa17634aac456760d3c197062'
SKILLS = {'pre-code-pipeline', 'execution-pipeline', 'writing-pipeline',
          'audit-and-refactoring-pipeline', 'release-and-ops-pipeline',
          'quarto-expert', 'humanizer', 'skill-loader'}
Q17 = 'quarto-expert/scripts/offline_probe.py'
ARCHIVE = 'meta-skills-2.0.0-candidate.tar.gz'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def pairs(items):
    result = {}
    for key, value in items:
        need(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def decode(data):
    return json.loads(data.decode('utf-8'), object_pairs_hook=pairs)


def path_ok(name):
    need(isinstance(name, str), 'Non-string path')
    p = PurePosixPath(name)
    need(p.parts and not p.is_absolute() and p.as_posix() == name
         and not any(c in name for c in '\\:\x00')
         and not any(x in ('.', '..') or x.endswith((' ', '.')) for x in name.split('/')),
         'Unsafe archive path: ' + repr(name))


def regular(root, name, limit=2000000):
    path_ok(name)
    p = Path(root)
    for part in PurePosixPath(name).parts:
        p = p / part
        need(not p.is_symlink(), 'Unexpected symlink: ' + name)
    need(stat.S_ISREG(p.stat().st_mode) and p.stat().st_size <= limit, 'Invalid/oversized file: ' + name)
    return p.read_bytes()


def selected_bytes(source, commit, selection_path, selection_sha):
    # The digest's provenance and approval must be established outside this verifier.
    if selection_path is None:
        need(selection_sha is None, 'Selection and expected digest are required together')
        data = regular(source, 'ci/payload.json')
        value = decode(data)
        need('profile' not in value and 'source_commit' not in value, 'Prospective selection requires explicit opt-in')
        return data
    need(isinstance(selection_sha, str) and re.fullmatch(r'[0-9a-f]{64}', selection_sha),
         'Expected selection digest is required')
    path = Path(selection_path).absolute()
    data = regular(Path(path.anchor), path.relative_to(path.anchor).as_posix())
    need(sha(data) == selection_sha, 'Selection digest mismatch')
    value = decode(data)
    frozen_bytes = regular(source, 'ci/payload.json')
    need(sha(frozen_bytes) == HISTORICAL_SELECTION_SHA, 'Historical selection changed')
    frozen = decode(frozen_bytes)
    need(isinstance(value, dict) and set(value) == set(frozen) | {'profile', 'source_commit'}, 'Selection fields')
    need(value['profile'] == 'prospective' and value['source_commit'] == commit, 'Selection profile/source identity')
    for key in ('format', 'baseline', 'derived', 'mode_policy'):
        need(canonical(value[key]) == canonical(frozen[key]), 'Incompatible selection ' + key)
    entries = value['sources']
    need(isinstance(entries, list) and len(entries) == 82, 'Source composition')
    for entry in entries:
        need(isinstance(entry, dict) and set(entry) == {'path', 'bytes', 'sha256', 'mode'}, 'Source record')
        path_ok(entry['path'])
        need(type(entry['bytes']) is int and 0 <= entry['bytes'] <= 2000000
             and isinstance(entry['sha256'], str) and re.fullmatch(r'[0-9a-f]{64}', entry['sha256'])
             and entry['mode'] == '0o664', 'Source size/digest/mode')
    need(len({e['path'].casefold() for e in entries}) == 82
         and {e['path'] for e in entries} == {e['path'] for e in frozen['sources']}, 'Source composition/collision')
    return data


def committed_inputs(source, commit, names):
    git = ['git', '--no-optional-locks', '--no-replace-objects', '--no-lazy-fetch']
    need(subprocess.check_output(git + ['cat-file', '-t', commit], cwd=source) == b'commit\n', 'Expected a source commit')
    tree = subprocess.check_output(git + ['ls-tree', '-rz', commit, '--', *names], cwd=source)
    entries = {}
    for row in tree.split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            mode, kind, oid = meta.split()
            need(mode in (b'100644', b'100755') and kind == b'blob', 'Non-regular committed input')
            entries[name.decode('utf-8')] = oid.decode('ascii')
    need(set(entries) == set(names), 'Missing committed input')
    for name, oid in entries.items():
        need(regular(source, name) == subprocess.check_output(git + ['cat-file', 'blob', oid], cwd=source),
             'Uncommitted input: ' + name)


def verify(source, bundle, commit, run_id, attempt, tar_sha, manifest_sha, delivery_sha, extract=None,
           *, selection_path=None, selection_sha=None):
    source, bundle = Path(source).resolve(), Path(bundle)
    need(re.fullmatch(r'[0-9a-f]{40}', commit) is not None, 'Invalid expected commit')
    for value in (tar_sha, manifest_sha, delivery_sha):
        need(re.fullmatch(r'[0-9a-f]{64}', value) is not None, 'Invalid expected digest')
    need({p.name for p in bundle.iterdir()} == {ARCHIVE, 'payload-manifest.json', 'delivery.json'}, 'Incomplete/extra artifact files')
    selection_bytes = selected_bytes(source, commit, selection_path, selection_sha)
    selection = decode(selection_bytes)
    need(selection['format'] == 'meta-skills-ci-selection-v1', 'Selection format')
    entries = selection['sources']
    if selection_path is None:
        need(sha(canonical(entries)) == BASELINE_RECORDS_SHA, 'Baseline/mode/allowlist changed')
    expected = {e['path']: e for e in entries}
    need(len(entries) == len(expected) == 82 and Q17 in expected, 'Missing Q17/source')
    need({n.split('/')[0] for n in expected if n.endswith('/SKILL.md')} == SKILLS, 'Eight skills required')
    for name, entry in expected.items():
        path_ok(name)
        need(entry['mode'] == '0o664', 'Unapproved source mode')
        data = regular(source, name)
        need(len(data) == entry['bytes'] and sha(data) == entry['sha256'], 'Checkout differs: ' + name)
    readme = regular(source, 'ci/PAYLOAD-README.md')
    readme_entry = selection['derived']['README.md']
    need(readme_entry == {'template': 'ci/PAYLOAD-README.md', 'sha256': '7d7a38f0e789ba4278a674520e523f56dabb9ff9c80a4ba7816b3ca710184c4a', 'bytes': 543, 'mode': '0o644'}, 'Unexpected README contract')
    need(sha(readme) == readme_entry['sha256'], 'README template mismatch')
    need(selection['derived']['payload-manifest.json']['mode'] == '0o644', 'Unapproved manifest mode')
    need(selection['baseline'] == {
        'commit': 'e4a57a2427748450d511bdbd6a27b169525c8008',
        'selection_sha256': '087d2a1d525678e4522af349d24c9aefd014da83bf4d35e003c26a9a1d75ce0c',
        'tar_sha256': '3452ee7c91c8b742f04503bad46def4cb7d14b9ef30c20b3fc15ef696df81feb',
        'manifest_sha256': '7053347b4debf81d5f81fa81d8b587f84a31c835f9f1906e364c54b48df90790'}, 'Wrong historical identity')
    tar_data = regular(bundle, ARCHIVE)
    manifest_data = regular(bundle, 'payload-manifest.json', 200000)
    delivery_data = regular(bundle, 'delivery.json', 20000)
    need(sha(delivery_data) == delivery_sha, 'Delivery digest mismatch')
    delivery = decode(delivery_data)
    need(sha(tar_data) == tar_sha and sha(manifest_data) == manifest_sha, 'Producer digest mismatch')
    need(delivery['format'] == 'meta-skills-ci-delivery-v1'
         and delivery['source_commit'] == commit
         and delivery['run_id'] == str(run_id) and delivery['run_attempt'] == str(attempt)
         and delivery['tar_sha256'] == tar_sha and delivery['tar_bytes'] == len(tar_data)
         and delivery['manifest_sha256'] == manifest_sha and delivery['manifest_bytes'] == len(manifest_data)
         and delivery['files'] == 84 and delivery['selection_sha256'] == sha(selection_bytes), 'Delivery identity mismatch')
    generator_sha = sha(regular(source, 'ci/build_payload.py'))
    need(delivery['generator_sha256'] == generator_sha, 'Wrong recipe identity')
    manifest = decode(manifest_data)
    need(manifest_data == canonical({'format': 'meta-skills-ci-payload-v1', 'source_commit': commit,
         'selection_sha256': sha(selection_bytes), 'generator_sha256': generator_sha,
         'baseline': selection['baseline'], 'sources': entries,
         'readme': {k: readme_entry[k] for k in ('sha256', 'bytes', 'mode')},
         'manifest': {'path': 'payload-manifest.json', 'mode': '0o644', 'digest': 'external'}}), 'Incompatible manifest')
    need(canonical(manifest) == manifest_data, 'Noncanonical manifest')
    expected['README.md'] = {'bytes': len(readme), 'sha256': sha(readme), 'mode': '0o644'}
    expected['payload-manifest.json'] = {'bytes': len(manifest_data), 'sha256': manifest_sha, 'mode': '0o644'}
    blobs = {}
    seen = set()
    blocks = sum(512 + ((e['bytes'] + 511)//512)*512 for e in expected.values())
    limit = ((blocks + 1024 + 10239)//10240)*10240
    # Bound decompression before tarfile processes any extended header or payload.
    with gzip.GzipFile(fileobj=io.BytesIO(tar_data), mode='rb') as gz:
        raw_tar = gz.read(limit + 1)
    need(len(raw_tar) == limit, 'Oversized/truncated decompressed tar')
    with tarfile.open(fileobj=io.BytesIO(raw_tar), mode='r:') as tar:
        for member in tar:
            path_ok(member.name)
            key = member.name.casefold()
            need(key not in seen, 'Duplicate/case-colliding path')
            seen.add(key)
            need(member.name in expected, 'Extra file (including DEL): ' + member.name)
            record = expected[member.name]
            header = raw_tar[member.offset:member.offset+512]
            need(header[156:157] in (b'0', b'\x00') and header[257:265] == b'ustar\x0000', 'Non-USTAR/extended header')
            need(member.isfile() and not member.pax_headers and member.linkname == '', 'Forbidden link/special entry')
            need(member.size == record['bytes'] and member.mode == int(record['mode'], 8), 'Size/mode mismatch')
            need(member.uid == member.gid == member.mtime == 0 and not member.uname and not member.gname, 'Nondeterministic metadata')
            data = tar.extractfile(member).read(record['bytes'] + 1)
            need(len(data) == record['bytes'] and sha(data) == record['sha256'], 'Entry digest mismatch: ' + member.name)
            blobs[member.name] = data
        need(not raw_tar[tar.offset:].strip(b'\x00'), 'Hidden data after tar end')
    need(list(blobs) == sorted(expected), 'Missing/unsorted entries')
    if extract is not None:
        dest = Path(extract)
        # Exclusive destination: no extraction into a reused tree or through its links.
        for parent in [dest] + list(dest.parents):
            need(not parent.is_symlink(), 'Extraction parent symlink')
        dest.mkdir(parents=True, exist_ok=False)
        for name, data in blobs.items():
            p = dest / name
            p.parent.mkdir(parents=True, exist_ok=True)
            with p.open('xb') as out:
                out.write(data)
            os.chmod(p, int(expected[name]['mode'], 8))
            need(sha(p.read_bytes()) == expected[name]['sha256'], 'Extraction readback mismatch')
    return {'status': 'verified', 'files': len(blobs), 'commit': commit,
            'run_id': str(run_id), 'run_attempt': str(attempt), 'tar_sha256': tar_sha,
            'manifest_sha256': manifest_sha, 'selection_sha256': sha(selection_bytes)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--bundle', type=Path, required=True)
    p.add_argument('--commit', required=True)
    p.add_argument('--run-id', required=True)
    p.add_argument('--attempt', required=True)
    p.add_argument('--tar-sha', required=True)
    p.add_argument('--manifest-sha', required=True)
    p.add_argument('--delivery-sha', required=True)
    p.add_argument('--extract', type=Path)
    p.add_argument('--selection', type=Path, help='Explicit prospective selection; requires --selection-sha')
    p.add_argument('--selection-sha', help='Expected selection digest from independently trusted context; not approval by itself')
    args = p.parse_args()
    need((args.selection is None) == (args.selection_sha is None), 'Selection and expected digest are required together')
    git = ['git', '--no-optional-locks', '--no-replace-objects', '--no-lazy-fetch'] if args.selection is not None else ['git']
    need(subprocess.check_output(git + ['rev-parse', 'HEAD'], cwd=args.source, text=True).strip() == args.commit, 'Checkout commit mismatch')
    if args.selection is not None:
        selected_bytes(args.source.resolve(), args.commit, args.selection, args.selection_sha)
        frozen = decode(regular(args.source, 'ci/payload.json'))
        inputs = ['ci/payload.json', 'ci/PAYLOAD-README.md', 'ci/build_payload.py'] + [e['path'] for e in frozen['sources']]
        committed_inputs(args.source, args.commit, inputs)
    print(json.dumps(verify(args.source, args.bundle, args.commit, args.run_id, args.attempt,
                            args.tar_sha, args.manifest_sha, args.delivery_sha, args.extract,
                            selection_path=args.selection, selection_sha=args.selection_sha), indent=2))


HISTORICAL_SELECTION_SHA = '35e6d9bfba253cfde3ee91e96810933dbc9d9c994fcfbf30b30ced3773331a2d'

if __name__ == '__main__':
    main()
