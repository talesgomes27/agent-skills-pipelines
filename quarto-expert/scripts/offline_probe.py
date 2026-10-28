#!/usr/bin/env python3
"""Inventory local Quarto/tool files without executing binaries or querying versions online."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import stat


def inventory(quarto=None):
    executable = shutil.which(quarto or 'quarto')
    prefix = Path(executable).resolve().parent.parent if executable else None
    version = None
    metadata_path = None
    if prefix:
        descriptor = None
        try:
            version_file = (prefix / 'share/version').resolve()
            version_file.relative_to(prefix)
            flags = os.O_RDONLY | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_BINARY', 0)
            descriptor = os.open(version_file, flags)
            if stat.S_ISREG(os.fstat(descriptor).st_mode):
                raw = os.read(descriptor, 129)
                metadata_path = str(version_file)
                value = raw.decode('utf-8').strip()
                if len(raw) <= 128 and re.fullmatch(r'\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?', value):
                    version = value
        except (OSError, ValueError, RuntimeError):
            pass
        finally:
            if descriptor is not None:
                os.close(descriptor)
    tools = {name: {'path': shutil.which(name), 'source': 'PATH'}
             for name in ('typst', 'pdflatex', 'xelatex', 'lualatex', 'Rscript', 'python3')}
    if prefix and tools['typst']['path'] is None:
        machine = (os.uname().machine if hasattr(os, 'uname') else os.environ.get('PROCESSOR_ARCHITECTURE', '')).lower()
        arch = {'amd64': 'x86_64', 'arm64': 'aarch64'}.get(machine, machine)
        for suffix in ('', '.exe'):
            candidate = prefix / 'bin/tools' / arch / ('typst' + suffix)
            try:
                candidate = candidate.resolve(strict=True)
                candidate.relative_to(prefix)
            except (OSError, ValueError, RuntimeError):
                continue
            if candidate.is_file() and os.access(candidate, os.X_OK):
                tools['typst'] = {'path': str(candidate), 'source': 'bundled-file'}
                break
    return {'mode': 'filesystem-only', 'quarto': {'path': executable, 'version_metadata': metadata_path, 'version': version},
            'tools': tools, 'execution_verified': False, 'render_verified': False,
            'limitations': 'File presence/version metadata only; engines, render and document validity not executed'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--quarto', help='Explicit binary path or name; never executed')
    data = inventory(parser.parse_args().quarto)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0 if data['quarto']['path'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
