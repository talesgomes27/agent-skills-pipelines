"""Disposable integration checks against the verified artifact and existing installer."""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
from unittest.mock import patch

OLD = '33b773cf099c6be3183526b31b758d783260cbd1'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def fingerprint(root):
    return {p.relative_to(root).as_posix():
            (('link', os.readlink(p)) if p.is_symlink() else
             ('file', hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns))
            for p in root.rglob('*') if p.is_file() or p.is_symlink()}


def run(source, payload, work, mode, recovery=False):
    source, payload, work = Path(source).resolve(), Path(payload).resolve(), Path(work).resolve()
    work.mkdir(parents=True, exist_ok=False)
    journal = []
    def save():
        (work/'results.json').write_text(json.dumps(journal, indent=2)+'\n', encoding='utf-8')
    def call(repo, command, dest=None, update=False, code=0):
        argv = [sys.executable, '-I', '-B', str(repo/'scripts/skills.py'), command, '--agent', 'codex', '--all']
        if dest is not None:
            argv += ['--destination', str(dest), '--mode', mode]
        if update:
            argv += ['--update']
        env = {k:v for k,v in os.environ.items() if k in ('PATH', 'SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP', 'LANG')}
        env.update(HOME=str(work), USERPROFILE=str(work), PYTHONDONTWRITEBYTECODE='1')
        r = subprocess.run(argv, cwd=work, env=env, capture_output=True, text=True, timeout=120)
        journal.append({'argv': argv, 'returncode': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr})
        save()
        need(r.returncode == code, 'Installer returned unexpected exit; see results.json')
        return json.loads(r.stdout)
    names = json.loads((payload/'distribution/catalog.json').read_text(encoding='utf-8'))['skills']
    need(len(names) == 8 and 'humanizer' in names, 'Eight skills required')
    spec = importlib.util.spec_from_file_location('artifact_installer', payload/'scripts/skills.py')
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    def installed(dest, repo, release):
        state = json.loads((dest/cli.STATE).read_text(encoding='utf-8'))
        need(state['version'] == 1 and set(state['skills']) == set(names), 'Receipt membership')
        for n in names:
            rec = state['skills'][n]
            expected = {rel:value for rel,value in cli.fingerprint(repo/n).items()
                        if Path(rel).parts[0] in cli.COMPONENTS}
            need(rec == {'source': str((repo/n).resolve()), 'mode': mode, 'release': release, 'files': expected}, 'Receipt mismatch')
            actual = cli.fingerprint(dest/n)
            if mode == 'link':
                # Links expose the live folder, including non-component root files.
                actual = {rel:value for rel,value in actual.items() if Path(rel).parts[0] in cli.COMPONENTS}
            need(actual == expected, 'Installed bytes mismatch')
            need((dest/n).is_symlink() == (mode == 'link'), 'Installation mode')
            if mode == 'link':
                need((dest/n).resolve() == (repo/n).resolve(), 'Wrong link target')
        checks = call(payload, 'doctor', dest)['checks']
        need(len(checks) == 8 and all(c['status'] == 'pass' for c in checks), 'Doctor failed')
    def unchanged(dest, repo, update=False):
        before = fingerprint(dest)
        need(all(p['action'] == 'unchanged' for p in call(repo, 'install', dest, update)['plan']), 'Not idempotent')
        need(before == fingerprint(dest), 'Idempotence modified files')
    def fault(dest, number):
        replace = cli.os.replace
        count = [0]
        def injected(src, dst):
            if Path(dst) == dest/cli.STATE:
                count[0] += 1
                if count[0] == number:
                    raise OSError('CI controlled receipt failure')
            return replace(src, dst)
        output = io.StringIO()
        args = ['install', '--agent', 'codex', '--all', '--mode', mode, '--destination', str(dest), '--update']
        with patch.object(cli.os, 'replace', side_effect=injected), contextlib.redirect_stdout(output):
            code = cli.main(args)
        journal.append({'fault_receipt_write': number, 'observed_writes': count[0], 'exit': code, 'stdout': output.getvalue()})
        save()
        need(code == 1 and count[0] == number and 'CI controlled receipt failure' in output.getvalue(), 'Fault not exercised')
        need(not list(dest.glob('.meta-skills-stage-*')) and not list(dest.glob('.meta-skills-state-*')), 'Staging debris after failure')

    # Source checks remain separate from the eight-skill artifact installation.
    need(len(call(source, 'doctor')['checks']) == 8, 'Source doctor coverage')
    need(len(call(payload, 'doctor')['checks']) == 8, 'Payload doctor coverage')
    dest = work/'source-install'
    call(source, 'install', dest)
    installed(dest, source, '2.0.0')
    unchanged(dest, source)
    dest = work/'initial'
    call(payload, 'install', dest)
    installed(dest, payload, '2.0.0')
    unchanged(dest, payload)
    listing = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', OLD], cwd=source, text=True).splitlines()
    paths = sorted(set(listing) & {e['path'] for e in json.loads((source/'ci/payload.json').read_text())['sources']})
    need(len(paths) == 80, 'Unexpected historical source selection')
    raw = subprocess.check_output(['git', 'archive', '--format=tar', OLD, '--', *paths], cwd=source)
    old = work/'snapshot-1.0.1'
    old.mkdir()
    extracted = []
    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        for member in tar:
            if member.isdir():
                continue
            need(member.isfile() and member.name in paths and member.name not in extracted, 'Invalid snapshot entry')
            p = old/member.name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(tar.extractfile(member).read())
            extracted.append(member.name)
    need(sorted(extracted) == paths, 'Incomplete historical snapshot')
    need(json.loads((old/'distribution/catalog.json').read_text())['release'] == '1.0.1', 'Wrong old release')
    dest = work/'upgrade'
    call(old, 'install', dest)
    installed(dest, old, '1.0.1')
    before = fingerprint(dest)
    result = call(payload, 'install', dest, code=1)
    need('--update' in result['error'] and fingerprint(dest) == before, 'Upgrade authorization failure')
    call(payload, 'install', dest, update=True)
    installed(dest, payload, '2.0.0')
    unchanged(dest, payload, True)
    dest = work/'conflict'
    (dest/names[-1]).mkdir(parents=True)
    (dest/names[-1]/'user.txt').write_text('synthetic user-owned bytes', encoding='utf-8')
    before = fingerprint(dest)
    need('Unmanaged destination' in call(payload, 'install', dest, code=1)['error'] and fingerprint(dest) == before, 'Conflict was not preserved')
    dest = work/'local-change'
    call(old, 'install', dest)
    if mode == 'copy':
        p = dest/names[0]/'SKILL.md'
        p.write_bytes(p.read_bytes()+b'\n<!-- synthetic local edit -->\n')
    else:
        other = work/'other'
        other.mkdir()
        (dest/names[0]).unlink()
        (dest/names[0]).symlink_to(other, target_is_directory=True)
    before = fingerprint(dest)
    call(payload, 'install', dest, update=True, code=1)
    need(fingerprint(dest) == before, 'Local change not preserved')
    if recovery:
        dest = work/'initial-recovery'
        dest.mkdir()
        (dest/'user.txt').write_bytes(b'preserved root marker')
        before = fingerprint(dest)
        fault(dest, 1)
        need(fingerprint(dest) == before, 'Initial rollback changed destination')
        call(payload, 'install', dest)
        installed(dest, payload, '2.0.0')
        for number in (1, 2):
            dest = work/('recovery-'+str(number))
            call(old, 'install', dest)
            before = fingerprint(dest)
            fault(dest, number)
            if number == 1:
                need(fingerprint(dest) == before, 'Rollback changed old installation')
            else:
                state = json.loads((dest/cli.STATE).read_text())['skills']
                need(state[names[0]]['release'] == '2.0.0' and all(state[n]['release'] == '1.0.1' for n in names[1:]), 'Unexpected partial progress')
                after = fingerprint(dest)
                for name in names[1:]:
                    need({p:v for p,v in after.items() if p == name or p.startswith(name+'/')} ==
                         {p:v for p,v in before.items() if p == name or p.startswith(name+'/')}, 'Later package changed before retry')
            call(payload, 'install', dest, update=True)
            installed(dest, payload, '2.0.0')
            unchanged(dest, payload, True)
    journal.append({'status': 'passed', 'skills': 8, 'mode': mode, 'recovery': recovery,
                    'historical_snapshot': OLD, 'remote_1_0_1_not_asserted': True})
    save()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--payload', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--mode', choices=('copy', 'link'), required=True)
    p.add_argument('--recovery', action='store_true')
    a = p.parse_args()
    run(a.source, a.payload, a.work, a.mode, a.recovery)
