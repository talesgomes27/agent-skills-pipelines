#!/usr/bin/env python3
"""Check the skill package, optionally rendering a static isolated HTML fixture."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import unquote, urlsplit


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--runtime", action="store_true")
    parser.add_argument("--render-smoke", action="store_true")
    parser.add_argument("--quarto", help="Executable path or name; defaults to PATH discovery")
    args = parser.parse_args()
    root = args.root.resolve()
    checks = []

    def record(name: str, status: str, detail: str) -> None:
        checks.append({"check": name, "status": status, "detail": detail})

    try:
        content = (root / "SKILL.md").read_text(encoding="utf-8")
        if not content.strip():
            raise ValueError("Empty manifest")
        record("manifest", "pass", str(root / "SKILL.md"))
    except (OSError, ValueError) as exc:
        content = ""
        record("manifest", "fail", str(exc))

    for target in re.findall(r"\]\(([^)]+)\)", content):
        parts = urlsplit(target)
        if parts.scheme in {"https", "http"} or target.startswith("#"):
            continue
        candidate = (root / unquote(parts.path)).resolve()
        valid = not parts.scheme and candidate.is_relative_to(root) and candidate.exists()
        record("resource:" + target, "pass" if valid else "fail", str(candidate))

    try:
        import yaml
    except ImportError:
        yaml = None
        record("yaml", "skipped", "PyYAML unavailable; YAML/frontmatter not validated")

    if yaml is not None and content:
        try:
            if not content.startswith("---\n"):
                raise ValueError("Missing YAML frontmatter")
            metadata = yaml.safe_load(content.split("---", 2)[1])
            if not isinstance(metadata, dict) or metadata.get("name") != "quarto-expert":
                raise ValueError("Expected name: quarto-expert")
            if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
                raise ValueError("Missing description")
            record("frontmatter", "pass", "Required fields parsed")
        except (ValueError, IndexError, yaml.YAMLError) as exc:
            record("frontmatter", "fail", str(exc))
        for path in sorted((root / "examples").rglob("*")):
            if path.suffix not in {".yml", ".yaml"}:
                continue
            try:
                yaml.safe_load(path.read_text(encoding="utf-8"))
                record("yaml:" + str(path.relative_to(root)), "pass", "Syntax only")
            except (OSError, yaml.YAMLError) as exc:
                record("yaml:" + str(path.relative_to(root)), "fail", str(exc))

    executable = None
    if args.runtime or args.render_smoke:
        executable = shutil.which(args.quarto or "quarto")
        if executable is None:
            record("quarto", "fail", "Executable unavailable; no install attempted")
        else:
            try:
                result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=15)
                record("quarto", "pass" if result.returncode == 0 else "fail",
                       result.stdout.strip() or result.stderr.strip()[-1500:])
                if result.returncode != 0:
                    executable = None
            except (OSError, subprocess.TimeoutExpired) as exc:
                record("quarto", "fail", str(exc))
                executable = None

    if args.render_smoke and executable is not None:
        with tempfile.TemporaryDirectory(prefix="quarto-skill-smoke-") as directory:
            work = Path(directory)
            marker = "quarto-skill-static-fixture"
            target = work / "fixture.qmd"
            target.write_text('---\ntitle: "Skill smoke"\nformat: html\n---\n\n' + marker + "\n", encoding="utf-8")
            try:
                result = subprocess.run(
                    [executable, "render", str(target), "--to", "html", "--no-execute"],
                    cwd=work, capture_output=True, text=True, timeout=60,
                )
                output = work / "fixture.html"
                valid = result.returncode == 0 and output.is_file() and marker in output.read_text(encoding="utf-8")
                detail = "Static isolated HTML only; no compute engine or user document validated"
                if not valid:
                    detail = (result.stderr or result.stdout)[-2000:] or "Expected output missing"
                record("render_static_html", "pass" if valid else "fail", detail)
            except (OSError, subprocess.TimeoutExpired) as exc:
                record("render_static_html", "fail", str(exc))

    statuses = {item["status"] for item in checks}
    code = 1 if "fail" in statuses else 2 if "skipped" in statuses else 0
    print(json.dumps({"skill": "quarto-expert", "root": str(root), "checks": checks,
                      "exit_code": code}, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
