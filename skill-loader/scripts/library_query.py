#!/usr/bin/env python3
"""Resolve and query a local cold skills library without loading its full index into context."""
import argparse
import json
import os
from pathlib import Path
import re
import sys

USER_CONFIG = Path.home() / '.config/agent-skills/library.json'


def configured_root(explicit=None, project=None):
    if explicit:
        return Path(explicit).expanduser().resolve()
    project_root = Path(project or Path.cwd()).expanduser().resolve()
    project_config = project_root / '.agents/skills-library.json'
    for config in (project_config, USER_CONFIG):
        if config.is_file():
            data = json.loads(config.read_text(encoding='utf-8'))
            if not isinstance(data, dict) or not isinstance(data.get('root'), str):
                raise ValueError('invalid library configuration: ' + str(config))
            return Path(data['root']).expanduser().resolve()
    env_root = os.environ.get('SKILLS_LIBRARY_ROOT')
    if env_root:
        return Path(env_root).expanduser().resolve()
    raise ValueError('library root unavailable; use --root, project/user configuration, or SKILLS_LIBRARY_ROOT')


def load_index(root):
    path = root / 'skills_index.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, list) or any(not isinstance(v, dict) for v in data):
        raise ValueError('skills_index.json must be an array of objects')
    return data


def manifest_for(root, entry):
    relative = entry.get('path')
    if not isinstance(relative, str) or not relative:
        raise ValueError('entry has invalid path: ' + str(entry.get('id')))
    manifest = (root / relative / 'SKILL.md').resolve()
    try:
        manifest.relative_to(root)
    except ValueError as exc:
        raise ValueError('entry escapes library root: ' + str(entry.get('id'))) from exc
    if not manifest.is_file():
        raise ValueError('manifest not found: ' + str(entry.get('id')))
    text = manifest.read_text(encoding='utf-8', errors='replace')
    match = re.search(r'^name:\s*["\']?([^"\'\n]+)', text, re.M)
    if not match or match.group(1).strip() != entry.get('id'):
        raise ValueError('manifest identity mismatch: ' + str(entry.get('id')))
    return manifest


def compact(entry, manifest):
    return {
        'id': entry.get('id'),
        'name': entry.get('name'),
        'description': entry.get('description'),
        'category': entry.get('category'),
        'risk': entry.get('risk'),
        'manifest': str(manifest),
    }


def exact(root, entries, skill_id):
    matches = [entry for entry in entries if entry.get('id') == skill_id]
    if len(matches) != 1:
        raise ValueError('skill id not found or duplicated: ' + skill_id)
    manifest = manifest_for(root, matches[0])
    return {'status': 'pass', 'root': str(root), 'result': compact(matches[0], manifest)}


def search(root, entries, query, limit):
    terms = [term for term in re.findall(r'[a-z0-9]+', query.casefold()) if len(term) > 1]
    if not terms:
        raise ValueError('query must contain searchable terms')
    ranked = []
    for entry in entries:
        skill_id = str(entry.get('id', '')).casefold()
        name = str(entry.get('name', '')).casefold()
        description = str(entry.get('description', '')).casefold()
        haystack = skill_id + ' ' + name + ' ' + description
        if not all(term in haystack for term in terms):
            continue
        score = sum(20 if skill_id == term else 10 if skill_id.startswith(term) else 3 if term in skill_id else 1 for term in terms)
        ranked.append((-score, skill_id, entry))
    results = []
    skipped = []
    for _, _, entry in sorted(ranked)[:limit * 3]:
        try:
            results.append(compact(entry, manifest_for(root, entry)))
        except ValueError as exc:
            skipped.append(str(exc))
        if len(results) == limit:
            break
    return {'status': 'pass', 'root': str(root), 'query': query, 'matches': len(ranked), 'results': results, 'skipped_invalid': skipped[:10]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('root', 'exact', 'search'))
    parser.add_argument('value', nargs='?')
    parser.add_argument('--root')
    parser.add_argument('--project')
    parser.add_argument('--limit', type=int, default=8)
    args = parser.parse_args(argv)
    try:
        if not 1 <= args.limit <= 25:
            raise ValueError('--limit must be between 1 and 25')
        root = configured_root(args.root, args.project)
        if not root.is_dir():
            raise ValueError('library root not found: ' + str(root))
        if args.command == 'root':
            result = {'status': 'pass', 'root': str(root)}
        else:
            if not args.value:
                raise ValueError(args.command + ' requires a value')
            entries = load_index(root)
            result = exact(root, entries, args.value) if args.command == 'exact' else search(root, entries, args.value, args.limit)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({'status': 'fail', 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
