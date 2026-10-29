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


def verify(source, bundle, commit, run_id, attempt, tar_sha, manifest_sha, delivery_sha, extract=None):
    source, bundle = Path(source).resolve(), Path(bundle)
    need(re.fullmatch(r'[0-9a-f]{40}', commit) is not None, 'Invalid expected commit')
    for value in (tar_sha, manifest_sha, delivery_sha):
        need(re.fullmatch(r'[0-9a-f]{64}', value) is not None, 'Invalid expected digest')
    need({p.name for p in bundle.iterdir()} == {ARCHIVE, 'payload-manifest.json', 'delivery.json'}, 'Incomplete/extra artifact files')
    selection_bytes = regular(source, 'ci/payload.json')
    selection = decode(selection_bytes)
    need(selection['format'] == 'meta-skills-ci-selection-v1', 'Selection format')
    entries = selection['sources']
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
    need(manifest == {'format': 'meta-skills-ci-payload-v1', 'source_commit': commit,
         'selection_sha256': sha(selection_bytes), 'generator_sha256': generator_sha,
         'baseline': selection['baseline'], 'sources': entries,
         'readme': {k: readme_entry[k] for k in ('sha256', 'bytes', 'mode')},
         'manifest': {'path': 'payload-manifest.json', 'mode': '0o644', 'digest': 'external'}}, 'Incompatible manifest')
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
    args = p.parse_args()
    need(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.source, text=True).strip() == args.commit, 'Checkout commit mismatch')
    print(json.dumps(verify(args.source, args.bundle, args.commit, args.run_id, args.attempt,
                            args.tar_sha, args.manifest_sha, args.delivery_sha, args.extract), indent=2))


if __name__ == '__main__':
    main()
