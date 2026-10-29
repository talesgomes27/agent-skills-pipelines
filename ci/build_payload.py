"""Deterministic candidate packaging; stdlib only, never publishes."""
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
import sys
import tarfile
import zlib


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def safe_path(name):
    p = PurePosixPath(name)
    require(isinstance(name, str) and not p.is_absolute() and p.parts
            and p.as_posix() == name and not any(c in name for c in '\\:\x00')
            and not any(x in ('.', '..') or x.endswith((' ', '.')) for x in name.split('/')),
            'Unsafe path: ' + repr(name))
    return p


def read_source(root, name):
    safe_path(name)
    p = root
    for part in PurePosixPath(name).parts:
        p = p / part
        require(not p.is_symlink(), 'Source symlink: ' + name)
    require(stat.S_ISREG(p.stat().st_mode), 'Not a regular source: ' + name)
    return p.read_bytes()


def build(source, output, commit, run_id, attempt):
    source, output = Path(source).resolve(), Path(output)
    require(re.fullmatch(r'[0-9a-f]{40}', commit), 'Invalid commit')
    require(str(run_id).isdigit() and str(attempt).isdigit(), 'Invalid run identity')
    selection_bytes = read_source(source, 'ci/payload.json')
    selection = json.loads(selection_bytes)
    require(selection['format'] == 'meta-skills-ci-selection-v1', 'Selection format')
    entries = selection['sources']
    require(len(entries) == 82 and len({e['path'].casefold() for e in entries}) == 82, 'Source count/collision')
    # Pin the historical records independently of the new selection's descriptive fields.
    require(digest(encoded(entries)) == BASELINE_RECORDS_SHA, 'Changed CONS-03 baseline')
    blobs = {}
    for entry in entries:
        data = read_source(source, entry['path'])
        require(len(data) == entry['bytes'] and digest(data) == entry['sha256'], 'Changed source: ' + entry['path'])
        require(entry['mode'] == '0o664', 'Changed source mode policy')
        blobs[entry['path']] = data
    template = read_source(source, selection['derived']['README.md']['template'])
    expected = selection['derived']['README.md']
    require(digest(template) == expected['sha256'] and len(template) == expected['bytes']
            and expected['mode'] == '0o644', 'Changed README template')
    require(selection['derived']['payload-manifest.json']['mode'] == '0o644', 'Changed manifest mode')
    blobs['README.md'] = template
    manifest = {'format': 'meta-skills-ci-payload-v1', 'source_commit': commit,
                'selection_sha256': digest(selection_bytes),
                'generator_sha256': digest(read_source(source, 'ci/build_payload.py')),
                'baseline': selection['baseline'], 'sources': entries,
                'readme': {k: expected[k] for k in ('sha256', 'bytes', 'mode')},
                'manifest': {'path': 'payload-manifest.json', 'mode': '0o644', 'digest': 'external'}}
    blobs['payload-manifest.json'] = encoded(manifest)
    output.mkdir(parents=True, exist_ok=False)
    archive = output / 'meta-skills-2.0.0-candidate.tar.gz'
    with archive.open('xb') as raw:
        with gzip.GzipFile(fileobj=raw, filename='', mode='wb', mtime=0, compresslevel=9) as gz:
            with tarfile.open(fileobj=gz, mode='w', format=tarfile.USTAR_FORMAT) as tar:
                for name, data in sorted(blobs.items()):
                    info = tarfile.TarInfo(name)
                    info.size = len(data)
                    info.mode = 0o644 if name in ('README.md', 'payload-manifest.json') else 0o664
                    info.uid = info.gid = info.mtime = 0
                    info.uname = info.gname = ''
                    tar.addfile(info, io.BytesIO(data))
    (output / 'payload-manifest.json').write_bytes(blobs['payload-manifest.json'])
    delivery = {'format': 'meta-skills-ci-delivery-v1', 'source_commit': commit,
                'run_id': str(run_id), 'run_attempt': str(attempt),
                'selection_sha256': digest(selection_bytes),
                'generator_sha256': manifest['generator_sha256'],
                'tar_sha256': digest(archive.read_bytes()), 'tar_bytes': archive.stat().st_size,
                'manifest_sha256': digest(blobs['payload-manifest.json']),
                'manifest_bytes': len(blobs['payload-manifest.json']), 'files': 84,
                'toolchain': {'python': sys.version, 'zlib': zlib.ZLIB_VERSION},
                'status': 'unpublished; technical checks do not approve R7 or release'}
    (output / 'delivery.json').write_bytes(encoded(delivery))
    return delivery


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    # Inputs must be committed bytes, not a dirty checkout or a future invented SHA.
    inputs = ['ci/payload.json', 'ci/PAYLOAD-README.md', 'ci/build_payload.py']
    selection = json.loads(read_source(source, inputs[0]))
    inputs += [e['path'] for e in selection['sources']]
    for name in inputs:
        require(read_source(source, name) == subprocess.check_output(['git', 'show', commit + ':' + name], cwd=source), 'Uncommitted input: ' + name)
    result = build(source, args.output, commit, os.environ.get('GITHUB_RUN_ID', '0'), os.environ.get('GITHUB_RUN_ATTEMPT', '0'))
    result['delivery_sha256'] = digest((args.output / 'delivery.json').read_bytes())
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as out:
            for key in ('tar_sha256', 'manifest_sha256', 'delivery_sha256'):
                out.write(key + '=' + result[key] + '\n')
    print(json.dumps(result, indent=2))


BASELINE_RECORDS_SHA = '8182c53b97c5c31dd3cd4f4364b5f1d4f6657aaaa17634aac456760d3c197062'

if __name__ == '__main__':
    main()
