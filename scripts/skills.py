#!/usr/bin/env python3
"""Selective local Agent Skills installer. Python 3.9+, PyYAML; no network calls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import unquote, urlsplit

REPO = Path(__file__).resolve().parents[1]
STATE = '.meta-skills-install.json'
AGENTS = ('codex', 'claude', 'antigravity', 'antigravity-cli')
COMPONENTS = ('SKILL.md', 'references', 'scripts', 'examples', 'assets', 'agents')
IGNORE = shutil.ignore_patterns('__pycache__', '*.pyc', '.quarto', '_site', '.git', '.venv')


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def catalog():
    c = read_json(REPO / 'distribution/catalog.json')
    if not isinstance(c, dict) or set(c) != {'version', 'release', 'skills', 'bundles'} or type(c['version']) is not int or c['version'] != 1:
        raise ValueError('Unsupported catalog shape/version')
    if not isinstance(c['release'], str) or not re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', c['release']):
        raise ValueError('Invalid catalog release')
    names = c['skills']
    if not isinstance(names, list) or not names or any(not isinstance(n, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', n) or len(n) > 64 for n in names) or len(set(names)) != len(names):
        raise ValueError('Invalid/duplicate skill names')
    if not isinstance(c['bundles'], dict):
        raise ValueError('bundles must be an object')
    for name, members in c['bundles'].items():
        if not isinstance(name, str) or not isinstance(members, list) or not members or any(n not in names for n in members) or len(set(members)) != len(members):
            raise ValueError('Invalid bundle: ' + str(name))
    return c


def selected(args, c):
    wanted = set(args.skill or [])
    for bundle in args.bundle or []:
        if bundle not in c['bundles']:
            raise ValueError('Unknown bundle: ' + bundle)
        wanted.update(c['bundles'][bundle])
    if args.all:
        wanted.update(c['skills'])
    if wanted - set(c['skills']):
        raise ValueError('Unknown skills: ' + ', '.join(sorted(wanted - set(c['skills']))))
    if not wanted and args.command == 'doctor':
        wanted.update(c['skills'])
    excluded = set(args.exclude or [])
    if excluded - set(c['skills']):
        raise ValueError('Unknown exclusions: ' + ', '.join(sorted(excluded - set(c['skills']))))
    wanted.difference_update(excluded)
    if not wanted:
        raise ValueError('Select --skill NAME, --bundle NAME or --all explicitly')
    return [n for n in c['skills'] if n in wanted]


def detect():
    # Session evidence takes precedence over executables installed on PATH.
    if os.environ.get('CODEX_THREAD_ID') or os.environ.get('CODEX_CI'):
        return ['codex']
    if os.environ.get('CLAUDECODE') == '1':
        return ['claude']
    found = [a for a, exe in [('codex', 'codex'), ('claude', 'claude'), ('antigravity-cli', 'agy')] if shutil.which(exe)]
    return found


def target(args):
    if args.destination:
        return Path(args.destination).expanduser().absolute()
    agent = args.agent
    if agent == 'auto':
        candidates = detect()
        if len(candidates) != 1:
            raise ValueError('Agent detection ambiguous/unavailable: ' + ', '.join(candidates) + '; use --agent')
        agent = candidates[0]
    if args.scope == 'project':
        root = Path(args.project).expanduser().resolve()
        return root / ('.claude/skills' if agent == 'claude' else '.agents/skills')
    return Path.home() / {
        'codex': '.agents/skills', 'claude': '.claude/skills',
        'antigravity': '.gemini/config/skills',
        'antigravity-cli': '.gemini/antigravity-cli/skills',
    }[agent]


def validate_skill(folder, expected):
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError('PyYAML missing; install distribution/requirements.txt in a virtualenv') from exc
    text = (folder / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not match:
        raise ValueError(str(folder) + ': missing YAML frontmatter')
    class UniqueLoader(yaml.SafeLoader):
        pass

    def mapping(loader, node):
        pairs = loader.construct_pairs(node)
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate YAML key: ' + str(key))
            result[key] = value
        return result

    UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)
    try:
        data = yaml.load(match.group(1), Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise ValueError(str(folder) + ': invalid YAML frontmatter') from exc
    if not isinstance(data, dict) or data.get('name') != expected or not isinstance(data.get('description'), str) or not 0 < len(data['description'].strip()) <= 1024:
        raise ValueError(str(folder) + ': invalid name/description')
    if 'metadata' in data and (not isinstance(data['metadata'], dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in data['metadata'].items())):
        raise ValueError(str(folder) + ': metadata must map strings to strings')
    # Entrypoint links are executable routing, unlike illustrative snippets in guides.
    body = re.sub(r'```.*?```', '', text[match.end():], flags=re.S)
    for link in re.findall(r'\]\(([^)]+)\)', body):
        url = urlsplit(link.strip('<>'))
        if url.scheme or not url.path:
            continue
        resource = (folder / unquote(url.path)).resolve()
        try:
            resource.relative_to(folder.resolve())
        except ValueError as exc:
            raise ValueError('Entrypoint reference escapes package: ' + link) from exc
        if not resource.exists():
            raise ValueError('Missing entrypoint reference: ' + link)
    for f in folder.rglob('*'):
        if f.is_symlink():
            raise ValueError('Nested symlink unsupported in distributed package: ' + str(f))
        if f.is_file() and f.suffix in ('.yaml', '.yml'):
            try:
                yaml.load(f.read_text(encoding='utf-8'), Loader=UniqueLoader)
            except yaml.YAMLError as exc:
                raise ValueError('Invalid resource YAML: ' + str(f)) from exc
    return {'skill': expected, 'status': 'pass', 'characters': len(text)}


def fingerprint(folder):
    entries = {}
    for f in sorted(folder.rglob('*')):
        if f.is_symlink():
            raise ValueError('Unexpected nested symlink: ' + str(f))
        if f.is_file() and '__pycache__' not in f.parts and f.suffix != '.pyc':
            entries[f.relative_to(folder).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
    return entries


def state_at(dest):
    p = dest / STATE
    if not p.exists():
        return {'version': 1, 'skills': {}}
    if p.is_symlink():
        raise ValueError('State file cannot be a symlink')
    state = read_json(p)
    if not isinstance(state, dict) or state.get('version') != 1 or not isinstance(state.get('skills'), dict) or any(not isinstance(v, dict) for v in state['skills'].values()):
        raise ValueError('Invalid installation state')
    return state


def write_state(dest, state):
    fd, name = tempfile.mkstemp(prefix='.meta-skills-state-', dir=dest)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
            f.write('\n')
        os.replace(name, dest / STATE)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def stage_copy(src, dst):
    for name in COMPONENTS:
        p = src / name
        if p.is_dir():
            shutil.copytree(p, dst / name, ignore=IGNORE)
        elif p.is_file():
            shutil.copy2(p, dst / name)


def install(args, names, release):
    dest = target(args)
    for n in names:
        validate_skill(REPO / n, n)
        if dest.resolve() == (REPO / n).resolve() or (REPO / n).resolve() in dest.resolve().parents:
            raise ValueError('Destination cannot be inside a source skill')
    state = state_at(dest)
    plans = []
    with tempfile.TemporaryDirectory(prefix='meta-skills-') as tmp:
        staging = Path(tmp)
        # Validate the entire plan, including conflicts, before changing the destination.
        for n in names:
            src, dst = REPO / n, dest / n
            staged = staging / n
            staged.mkdir()
            stage_copy(src, staged)
            digest = fingerprint(staged)
            exists = dst.exists() or dst.is_symlink()
            old = state['skills'].get(n)
            if exists:
                if not old:
                    raise ValueError('Unmanaged destination; preserved: ' + str(dst))
                if dst.is_symlink():
                    if old.get('mode') != 'link' or str(dst.resolve()) != old.get('source'):
                        raise ValueError('Managed link changed; preserved: ' + str(dst))
                    same = args.mode == 'link' and dst.resolve() == src.resolve() and old.get('release') == release
                else:
                    if old.get('mode') != 'copy' or not dst.is_dir() or fingerprint(dst) != old.get('files'):
                        raise ValueError('Local changes detected; preserved: ' + str(dst))
                    same = args.mode == 'copy' and fingerprint(dst) == digest and old.get('release') == release
                if not same and not args.update:
                    raise ValueError('Managed update requires --update: ' + str(dst))
            else:
                same = False
            plans.append((n, src, dst, staged, digest, exists, same))
        output = []
        for n, src, dst, staged, digest, exists, same in plans:
            action = 'unchanged' if same else ('update' if exists else 'install')
            old = state['skills'].get(n, {})
            output.append({'skill': n, 'action': action, 'destination': str(dst), 'mode': args.mode, 'installed_release': old.get('release'), 'source_release': release})
        if args.dry_run:
            return {'dry_run': True, 'plan': output}
        dest.mkdir(parents=True, exist_ok=True)
        for n, src, dst, staged, digest, exists, same in plans:
            if same:
                continue
            # Prepare on destination filesystem, then swap this package with rollback.
            with tempfile.TemporaryDirectory(prefix='.meta-skills-stage-', dir=dest) as work:
                work = Path(work)
                new, backup = work / 'new', work / 'old'
                if args.mode == 'link':
                    new.symlink_to(src.resolve(), target_is_directory=True)
                else:
                    shutil.copytree(staged, new)
                if exists:
                    dst.rename(backup)
                try:
                    new.rename(dst)
                    state['skills'][n] = {'source': str(src.resolve()), 'mode': args.mode, 'release': release, 'files': digest}
                    write_state(dest, state)
                except Exception:
                    if dst.is_symlink():
                        dst.unlink()
                    elif dst.exists():
                        shutil.rmtree(dst)
                    if exists:
                        backup.rename(dst)
                    raise
        return {'dry_run': False, 'plan': output}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('list', 'detect', 'manifest', 'install', 'doctor'))
    parser.add_argument('--skill', action='append')
    parser.add_argument('--bundle', action='append')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--exclude', action='append', help='Exclude an exact catalog skill name')
    parser.add_argument('--agent', choices=('auto',) + AGENTS, default='auto')
    parser.add_argument('--scope', choices=('project', 'user'), default='project')
    parser.add_argument('--project', default=str(Path.cwd()))
    parser.add_argument('--destination', help='Explicit skills root; overrides agent/scope')
    parser.add_argument('--mode', choices=('copy', 'link'), default='copy')
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    try:
        c = catalog()
        if args.command == 'list':
            result = c
        elif args.command == 'detect':
            result = {'candidates': detect(), 'executables': {a: shutil.which(exe) for a, exe in [('codex', 'codex'), ('claude', 'claude'), ('antigravity-cli', 'agy')]}}
        else:
            names = selected(args, c)
            if args.command == 'manifest':
                for n in names:
                    validate_skill(REPO / n, n)
                result = {'entries': [{'path': str((REPO / n).resolve())} for n in names]}
            elif args.command == 'install':
                result = install(args, names, c['release'])
            else:
                root = Path(args.destination).expanduser().absolute() if args.destination else REPO
                checks = []
                state = state_at(root) if args.destination else {'skills': {}}
                for n in names:
                    try:
                        check = validate_skill(root / n, n)
                        receipt = state['skills'].get(n)
                        if receipt:
                            folder = root / n
                            if receipt.get('mode') == 'copy':
                                if folder.is_symlink() or fingerprint(folder) != receipt.get('files'):
                                    raise ValueError('Installed copy differs from recorded files: ' + n)
                            elif receipt.get('mode') == 'link':
                                if not folder.is_symlink() or str(folder.resolve()) != receipt.get('source'):
                                    raise ValueError('Installed link target changed: ' + n)
                            else:
                                raise ValueError('Unknown recorded mode: ' + n)
                            check['integrity'] = 'managed-copy' if receipt['mode'] == 'copy' else 'live-link'
                            check['installed_release'] = receipt.get('release')
                            check['source_release'] = c['release']
                            check['update_available'] = receipt.get('release') != c['release']
                        else:
                            check['integrity'] = 'structure-only'
                            check['source_release'] = c['release']
                        checks.append(check)
                    except (ValueError, OSError) as exc:
                        checks.append({'skill': n, 'status': 'fail', 'error': str(exc)})
                result = {'root': str(root), 'checks': checks}
                if any(c['status'] == 'fail' for c in checks):
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                    return 1
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except RuntimeError as exc:
        print(json.dumps({'status': 'unavailable', 'error': str(exc)}, ensure_ascii=False))
        return 2
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({'status': 'fail', 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
