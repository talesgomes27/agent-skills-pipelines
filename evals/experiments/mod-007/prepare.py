#!/usr/bin/env python3
"""Prepare matched, private-data-free fixtures from pinned local Git revisions."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
BASELINE = 'b9b9469'
CANDIDATE = '10b14ad'


def prepare(destination):
    destination.mkdir(parents=True, exist_ok=False)
    skills = json.loads((REPO / 'distribution/catalog.json').read_text(encoding='utf-8'))['skills']
    cases = json.loads((HERE / 'cases.json').read_text(encoding='utf-8'))['cases']
    revisions = {}
    for condition in ('baseline', 'skill'):
        for group in ('main', 'fresh'):
            root = destination / f'{condition}-{group}'
            root.mkdir()
            revision = BASELINE if condition == 'baseline' and group == 'main' else CANDIDATE
            revisions[root.name] = subprocess.check_output(['git', 'rev-parse', revision], cwd=REPO, text=True).strip()
            archive = subprocess.check_output(['git', 'archive', revision, '--', *skills], cwd=REPO)
            with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
                for member in tar:
                    if member.isfile():
                        path = root / 'policy' / member.name
                        path.resolve().relative_to(root.resolve())
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(tar.extractfile(member).read())
            metadata = []
            for skill in skills:
                text = (root / 'policy' / skill / 'SKILL.md').read_text(encoding='utf-8')
                description = next(line for line in text.splitlines() if line.startswith('description:'))
                metadata.append(f'{skill}: {description.removeprefix("description:").strip()}')
            (root / 'catalog.md').write_text('\n'.join(metadata) + '\n', encoding='utf-8')
            for case in cases:
                if (case['id'] == 'J') != (group == 'fresh'):
                    continue
                work = root / 'work' / case['id']
                if case['id'].startswith('G-'):
                    work.mkdir(parents=True)
                else:
                    shutil.copytree(HERE / 'fixtures' / case['id'], work)
                (work / 'REQUEST.md').write_text(case['prompt'] + '\n', encoding='utf-8')
    inputs = {path.relative_to(destination).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(destination.rglob('*')) if path.is_file()}
    manifest = {'revisions': revisions, 'input_sha256': inputs,
                'cohort_sha256': hashlib.sha256((HERE / 'cases.json').read_bytes()).hexdigest()}
    (destination / 'inputs.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    print(json.dumps(prepare(parser.parse_args().destination)['revisions'], indent=2))
