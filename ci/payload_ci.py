"""Validation-only CI adapter. Proposal inputs never establish delivery/publication approval."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile


def need(ok, message):
    if not ok:
        raise ValueError(message)


def run(operation, arguments, source, context):
    need(operation in ('build', 'verify'), 'Validation operations only; trusted delivery is not configured')
    reserved = ('--source', '--commit', '--selection', '--selection-sha')
    need(not any(arg.startswith('--') and any(flag.startswith(arg.split('=', 1)[0]) for flag in reserved)
                 for arg in arguments), 'Source/selection identity must come from the validation context')
    source = Path(source).resolve()
    git = ['git', '--no-optional-locks', '--no-replace-objects', '--no-lazy-fetch']
    def query(*args):
        return subprocess.check_output(git + list(args), cwd=source)
    event = context.get('GITHUB_EVENT_NAME', 'local')
    need(event in ('local', 'push', 'pull_request', 'workflow_dispatch'), 'Unsupported privileged event')
    head = query('rev-parse', 'HEAD').decode().strip()
    commit = context.get('CI_SOURCE_COMMIT') or head
    need(re.fullmatch('[0-9a-f]{40}', commit) and head == commit, 'Source revision mismatch')
    if event != 'local':
        need(commit == context.get('GITHUB_SHA'), 'Workflow source revision mismatch')
    need(query('cat-file', '-t', commit) == b'commit\n', 'Expected a source commit')
    selection_commit = context.get('CI_SELECTION_COMMIT', '')
    selection_path = context.get('CI_SELECTION_PATH', '')
    selection_sha = context.get('CI_SELECTION_SHA', '')
    proposed = any((selection_commit, selection_path, selection_sha))
    data = None
    proposal_validation = context.get('CI_PROSPECTIVE_VALIDATION') == 'true'
    if proposal_validation:
        need(not proposed, 'Cannot combine generated proposal validation with a versioned selection')
        ref = context.get('GITHUB_REF', '')
        need(event == 'pull_request' or (event == 'push' and ref.startswith('refs/heads/')),
             'Proposal bootstrap requires an unprivileged PR/branch event')
        # This digest identifies test inputs; it never authorizes delivery.
        frozen = commit + ':ci/payload.json'
        need(int(query('cat-file', '-s', frozen)) <= 2000000, 'Oversized historical selection')
        data = query('cat-file', 'blob', frozen)
        need(hashlib.sha256(data).hexdigest() == '35e6d9bfba253cfde3ee91e96810933dbc9d9c994fcfbf30b30ced3773331a2d',
             'Historical selection changed')
        selection = json.loads(data)
        selection.update(profile='prospective', source_commit=commit)
        for entry in selection['sources']:
            obj = commit + ':' + entry['path']
            need(int(query('cat-file', '-s', obj)) <= 2000000, 'Oversized proposed source')
            content = query('cat-file', 'blob', obj)
            entry.update(bytes=len(content), sha256=hashlib.sha256(content).hexdigest())
        data = (json.dumps(selection, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')
        selection_sha = hashlib.sha256(data).hexdigest()
    if proposed:
        need(all((selection_commit, selection_path, selection_sha)), 'Selection commit, path and expected digest required together')
        need(event in ('local', 'workflow_dispatch'), 'Proposed selection requires explicit dispatch; PR inputs are not approval')
        need(re.fullmatch('[0-9a-f]{40}', selection_commit) and re.fullmatch('[0-9a-f]{64}', selection_sha), 'Invalid selection revision/digest')
        path = PurePosixPath(selection_path)
        need(not path.is_absolute() and path.parts and path.as_posix() == selection_path
             and not any(c in selection_path for c in '\\:\x00')
             and not any(p in ('.', '..') or p.endswith((' ', '.')) for p in selection_path.split('/')), 'Unsafe selection path')
        need(query('cat-file', '-t', selection_commit) == b'commit\n', 'Expected a selection commit')
        rows = query('ls-tree', '-rz', selection_commit, '--', selection_path).split(b'\0')
        rows = [row for row in rows if row]
        need(len(rows) == 1, 'Missing/ambiguous versioned selection')
        metadata, name = rows[0].split(b'\t', 1)
        mode, kind, oid = metadata.split()
        need(mode in (b'100644', b'100755') and kind == b'blob' and name.decode() == selection_path,
             'Non-regular versioned selection')
        need(int(query('cat-file', '-s', oid.decode())) <= 2000000, 'Oversized versioned selection')
        data = query('cat-file', 'blob', oid.decode())
        need(len(data) <= 2000000 and hashlib.sha256(data).hexdigest() == selection_sha, 'Selection digest mismatch')
    command = [sys.executable, '-I', '-B', str(source/'ci'/(operation+'_payload.py')), '--source', str(source)]
    if operation == 'verify':
        command += ['--commit', commit]
    with tempfile.TemporaryDirectory(prefix='meta-skills-ci-selection-') as temporary:
        if data is not None:
            selected = Path(temporary).resolve()/'selection.json'
            selected.write_bytes(data)
            command += ['--selection', str(selected), '--selection-sha', selection_sha]
        command += list(arguments)
        result = subprocess.run(command, cwd=source, env=dict(os.environ, **context),
                                capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('build', 'verify'))
    args, forwarded = parser.parse_known_args()
    result = run(args.operation, forwarded, Path(__file__).resolve().parents[1], dict(os.environ))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
