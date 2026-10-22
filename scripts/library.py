#!/usr/bin/env python3
"""Validate or rebuild a cold Agent Skills library index. Python 3.9+, PyYAML."""
import argparse
import json
import os
from pathlib import Path
import re
import sys


def load_yaml_frontmatter(path):
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError('PyYAML missing; install distribution/requirements.txt in a virtualenv') from exc
    text = path.read_text(encoding='utf-8')
    match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not match:
        raise ValueError('missing YAML frontmatter')
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict) or not isinstance(data.get('name'), str) or not isinstance(data.get('description'), str):
        raise ValueError('frontmatter requires string name and description')
    return data


def read_index(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise ValueError('skills_index.json must be an array of objects')
    return data


def safe_manifest(root, relative):
    if not isinstance(relative, str) or not relative:
        raise ValueError('invalid relative path')
    candidate = (root / relative / 'SKILL.md').resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError('path escapes library root') from exc
    return candidate


def doctor(root, index):
    entries = read_index(index)
    issues = []
    seen = set()
    for position, entry in enumerate(entries):
        skill_id = entry.get('id')
        if not isinstance(skill_id, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', skill_id):
            issues.append({'position': position, 'id': skill_id, 'error': 'invalid id'})
            continue
        if skill_id in seen:
            issues.append({'position': position, 'id': skill_id, 'error': 'duplicate id'})
            continue
        seen.add(skill_id)
        try:
            manifest = safe_manifest(root, entry.get('path'))
            if not manifest.is_file():
                raise ValueError('manifest not found')
            metadata = load_yaml_frontmatter(manifest)
            if metadata['name'] != skill_id:
                raise ValueError('frontmatter name differs from id')
        except (OSError, ValueError) as exc:
            issues.append({'position': position, 'id': skill_id, 'path': entry.get('path'), 'error': str(exc)})
    return {
        'status': 'pass' if not issues else 'fail',
        'root': str(root),
        'index': str(index),
        'entries': len(entries),
        'valid': len(entries) - len(issues),
        'issues': issues[:100],
        'issues_truncated': max(0, len(issues) - 100),
    }


def rebuild(root, index, skills_dir, output, replace):
    old = read_index(index) if index.is_file() else []
    old_by_id = {item.get('id'): item for item in old if isinstance(item.get('id'), str)}
    scan_root = (root / skills_dir).resolve()
    try:
        scan_root.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError('skills directory escapes library root') from exc
    if not scan_root.is_dir():
        raise ValueError('skills directory not found: ' + str(scan_root))
    found = {}
    for manifest in sorted(scan_root.rglob('SKILL.md')):
        metadata = load_yaml_frontmatter(manifest)
        skill_id = metadata['name']
        if skill_id in found:
            raise ValueError('duplicate manifest name: ' + skill_id)
        item = dict(old_by_id.get(skill_id, {}))
        item.update({
            'id': skill_id,
            'path': manifest.parent.relative_to(root.resolve()).as_posix(),
            'name': skill_id,
            'description': metadata['description'].strip(),
        })
        found[skill_id] = item
    if output.resolve() == index.resolve() and not replace:
        raise ValueError('refusing to replace the source index without --replace')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps([found[name] for name in sorted(found)], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'status': 'pass', 'output': str(output), 'entries': len(found), 'preserved_metadata': sum(1 for name in found if name in old_by_id)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('doctor', 'rebuild'))
    parser.add_argument('--root', default=os.environ.get('SKILLS_LIBRARY_ROOT'))
    parser.add_argument('--index')
    parser.add_argument('--skills-dir', default='.', help='Relative subtree to scan; defaults to the library root')
    parser.add_argument('--output')
    parser.add_argument('--replace', action='store_true')
    args = parser.parse_args(argv)
    try:
        if not args.root:
            raise ValueError('set --root or SKILLS_LIBRARY_ROOT')
        root = Path(args.root).expanduser().resolve()
        index = Path(args.index).expanduser().resolve() if args.index else root / 'skills_index.json'
        if args.command == 'doctor':
            result = doctor(root, index)
            code = 0 if result['status'] == 'pass' else 1
        else:
            if not args.output:
                raise ValueError('rebuild requires --output')
            result = rebuild(root, index, args.skills_dir, Path(args.output).expanduser().resolve(), args.replace)
            code = 0
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return code
    except RuntimeError as exc:
        print(json.dumps({'status': 'unavailable', 'error': str(exc)}, ensure_ascii=False))
        return 2
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({'status': 'fail', 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
