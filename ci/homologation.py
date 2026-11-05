"""Technical validation of an environment-approved tuple; never approves R7 or publication."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

REPOSITORY = 'talesgomes27/agent-skills-pipelines'
ARTIFACT_FILES = ('meta-skills-2.0.0-candidate.tar.gz', 'payload-manifest.json', 'delivery.json')


def need(ok, message):
    if not ok:
        raise ValueError(message)


def tool_env(metadata=None):
    env = {k:v for k,v in os.environ.items() if k in ('PATH', 'SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP', 'LANG')}
    env.update(GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')
    if metadata:
        env.update(GITHUB_SHA=metadata['workflow_commit'], GITHUB_RUN_ID=metadata['run_id'],
                   GITHUB_RUN_ATTEMPT=metadata['run_attempt'])
    return env


def git(root, *args):
    return subprocess.run(['git', '--no-optional-locks', '--no-replace-objects', '--no-lazy-fetch',
                           '-C', str(root), *args], capture_output=True, check=True, env=tool_env()).stdout


def clean(root):
    need(not git(root, 'status', '--porcelain=v1', '--untracked-files=all'), 'Uncommitted source/workflow files')


def verifier(root):
    spec = importlib.util.spec_from_file_location('homologation_verifier', root/'ci/verify_payload.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def committed_tools(root, commit):
    names = {'ci/'+name for name in ('homologation.py', 'verify_payload.py',
                                     'build_payload.py', 'check_installation.py')}
    rows = [row for row in git(root, 'ls-tree', '-rz', commit, '--', *sorted(names)).split(b'\0') if row]
    entries = {}
    for row in rows:
        info, name = row.split(b'\t', 1)
        mode, kind, oid = info.split()
        need(mode in (b'100644', b'100755') and kind == b'blob', 'Non-regular workflow tool')
        entries[name.decode('utf-8')] = oid.decode()
    need(set(entries) == names and not (root/'ci').is_symlink(), 'Missing/unsafe workflow tools')
    for name, oid in entries.items():
        path = root/name
        need(not path.is_symlink() and path.is_file() and path.stat().st_size <= 2000000,
             'Unsafe workflow tool: '+name)
        need(int(git(root, 'cat-file', '-s', oid)) <= 2000000, 'Oversized workflow tool')
        need(path.read_bytes() == git(root, 'cat-file', 'blob', oid), 'Uncommitted workflow tool: '+name)


def metadata(root, context):
    need(context.get('GITHUB_EVENT_NAME') == 'workflow_dispatch'
         and context.get('GITHUB_REF') == 'refs/heads/main'
         and context.get('GITHUB_REPOSITORY') == REPOSITORY, 'Untrusted workflow context')
    commit = context.get('GITHUB_SHA', '')
    need(re.fullmatch('[0-9a-f]{40}', commit) is not None, 'Invalid workflow commit')
    need(git(root, 'rev-parse', 'HEAD').decode().strip() == commit, 'Workflow checkout mismatch')
    clean(root)
    committed_tools(root, commit)
    for key in ('GITHUB_RUN_ID', 'GITHUB_RUN_ATTEMPT'):
        need(re.fullmatch('[1-9][0-9]*', context.get(key, '')) is not None, 'Invalid run identity')
    return dict(workflow_commit=commit, repository=REPOSITORY,
                run_id=context['GITHUB_RUN_ID'], run_attempt=context['GITHUB_RUN_ATTEMPT'])


def selected_tuple(value, checked):
    keys = {'source_commit', 'selection_commit', 'selection_path', 'selection_sha256'}
    need(isinstance(value, dict) and set(value) == keys and all(isinstance(v, str) for v in value.values()),
         'Expected exactly four string tuple fields')
    for key in ('source_commit', 'selection_commit'):
        need(re.fullmatch('[0-9a-f]{40}', value[key]) is not None, 'Invalid tuple commit')
    need(re.fullmatch('[0-9a-f]{64}', value['selection_sha256']) is not None, 'Invalid expected selection digest')
    checked.path_ok(value['selection_path'])
    need(all(ord(c) >= 32 and ord(c) != 127 for c in value['selection_path']), 'Control character in selection path')
    return value


def outside(path, *roots):
    need(all(path != root and root not in path.parents and path not in root.parents for root in roots),
         'Validation directories must be separate from the checkouts')


def prepare(workflow_root, work, context):
    root, work = Path(workflow_root).resolve(), Path(work).resolve()
    meta = metadata(root, context)
    checked = verifier(root)
    value = selected_tuple(checked.decode(context.get('HOMOLOGACAO_TUPLA', '').encode('utf-8')), checked)
    for commit in (value['source_commit'], value['selection_commit']):
        need(git(root, 'cat-file', '-t', commit) == b'commit\n', 'Expected a committed revision')
        git(root, 'merge-base', '--is-ancestor', commit, meta['workflow_commit'])
    rows = [r for r in git(root, 'ls-tree', '-rz', value['selection_commit'], '--',
                           value['selection_path']).split(b'\0') if r]
    need(len(rows) == 1, 'Missing/ambiguous selection blob')
    info, name = rows[0].split(b'\t', 1)
    mode, kind, oid = info.split()
    need(mode in (b'100644', b'100755') and kind == b'blob'
         and name.decode('utf-8') == value['selection_path'], 'Non-regular selection blob')
    need(int(git(root, 'cat-file', '-s', oid.decode())) <= 2000000, 'Oversized selection blob')
    data = git(root, 'cat-file', 'blob', oid.decode())
    need(checked.sha(data) == value['selection_sha256'], 'Selection digest mismatch')
    selection = checked.decode(data)
    need(isinstance(selection, dict) and selection.get('profile') == 'prospective'
         and selection.get('source_commit') == value['source_commit'], 'Selection profile/source mismatch')
    outside(work, root)
    need(not work.exists(), 'Validation directory already exists')
    snapshot = checked.canonical(dict(meta, tuple=value))
    work.mkdir(parents=True, exist_ok=False)
    (work/'selection.json').write_bytes(data)
    (work/'authorization.json').write_bytes(snapshot)
    return dict(source_commit=value['source_commit'], snapshot_sha256=checked.sha(snapshot))


def call(root, script, arguments, meta):
    result = subprocess.run([sys.executable, '-I', '-B', str(root/'ci'/script), *map(str, arguments)],
                            capture_output=True, text=True, check=True, env=tool_env(meta), timeout=300)
    return result.stdout


def validate(workflow_root, source, work, snapshot_sha256, context):
    root, source, work = (Path(p).resolve() for p in (workflow_root, source, work))
    meta = metadata(root, context)
    checked = verifier(root)
    outside(work, root, source)
    snapshot_bytes = checked.regular(work, 'authorization.json', 20000)
    need(re.fullmatch('[0-9a-f]{64}', snapshot_sha256) is not None
         and checked.sha(snapshot_bytes) == snapshot_sha256, 'Authorization snapshot mismatch')
    snapshot = checked.decode(snapshot_bytes)
    need(isinstance(snapshot, dict) and set(snapshot) == set(meta) | {'tuple'}
         and all(snapshot.get(k) == v for k,v in meta.items()), 'Authorization run/workflow mismatch')
    value = selected_tuple(snapshot['tuple'], checked)
    need(git(source, 'rev-parse', 'HEAD').decode().strip() == value['source_commit'], 'Source checkout mismatch')
    clean(source)
    need(checked.regular(root, 'ci/build_payload.py') == checked.regular(source, 'ci/build_payload.py'),
         'Executed recipe differs from source recipe')
    selection = work/'selection.json'
    checked.selected_bytes(source, value['source_commit'], selection, value['selection_sha256'])
    common = ['--source', source, '--selection', selection, '--selection-sha', value['selection_sha256']]
    a = checked.decode(call(root, 'build_payload.py', [*common, '--output', work/'payload-a'], meta).encode('utf-8'))
    call(root, 'build_payload.py', [*common, '--output', work/'payload-b'], meta)
    for directory in (work/'payload-a', work/'payload-b'):
        need({p.name for p in directory.iterdir()} == set(ARTIFACT_FILES), 'Unexpected artifact files')
    for name in ARTIFACT_FILES:
        need(checked.regular(work/'payload-a', name) == checked.regular(work/'payload-b', name),
             'Independent builds differ: '+name)
    need(a['source_commit'] == value['source_commit'] and a['selection_sha256'] == value['selection_sha256'],
         'Producer source/selection mismatch')
    digests = {k:a[k] for k in ('tar_sha256', 'manifest_sha256', 'delivery_sha256')}
    need(all(isinstance(v, str) and re.fullmatch('[0-9a-f]{64}', v) for v in digests.values()), 'Invalid producer digests')
    verified = checked.decode(call(root, 'verify_payload.py', [*common, '--bundle', work/'payload-a',
                    '--commit', value['source_commit'], '--run-id', meta['run_id'], '--attempt', meta['run_attempt'],
                    '--tar-sha', a['tar_sha256'], '--manifest-sha', a['manifest_sha256'],
                    '--delivery-sha', a['delivery_sha256'], '--extract', work/'extracted'], meta).encode('utf-8'))
    need(verified['files'] == 84, 'Expected all eight skills and 84 files')
    for mode in ('copy', 'link'):
        call(root, 'check_installation.py', ['--source', source, '--payload', work/'extracted',
             '--work', work/(mode+'-integration'), '--mode', mode, '--recovery'], meta)
    result = dict(meta, **value, **digests, authorization_snapshot_sha256=snapshot_sha256,
                  files=84, status='unpublished; technical validation only; R7 remains pending')
    with (work/'result.json').open('xb') as output:
        output.write(checked.canonical(result))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='operation', required=True)
    first = commands.add_parser('prepare')
    first.add_argument('--work', type=Path, required=True)
    second = commands.add_parser('validate')
    second.add_argument('--source', type=Path, required=True)
    second.add_argument('--work', type=Path, required=True)
    second.add_argument('--snapshot-sha', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    context = dict(os.environ)
    if args.operation == 'prepare':
        result = prepare(root, args.work, context)
        if 'GITHUB_OUTPUT' in os.environ:
            with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as output:
                for key in ('source_commit', 'snapshot_sha256'):
                    output.write(key+'='+result[key]+'\n')
    else:
        result = validate(root, args.source, args.work, args.snapshot_sha, context)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
