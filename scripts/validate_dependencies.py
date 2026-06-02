#!/usr/bin/env python3
"""Validate knowledge-base/graph/dependencies.yaml file paths exist (stdlib only)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = REPO_ROOT / "knowledge-base" / "graph" / "dependencies.yaml"
FILES_LINE = re.compile(r"^\s+files:\s*\[(.+?)\]\s*$", re.MULTILINE)


def resolve_pattern(repo_root: Path, pattern: str) -> list[Path]:
    path = repo_root / pattern
    if "*" in pattern:
        return sorted(path.parent.glob(path.name))
    return [path]


def collect_file_patterns(text: str) -> list[str]:
    patterns: list[str] = []
    for match in FILES_LINE.finditer(text):
        raw = match.group(1)
        for part in raw.split(","):
            p = part.strip().strip('"').strip("'")
            if p:
                patterns.append(p)
    return patterns


def main() -> int:
    if not GRAPH_PATH.is_file():
        print(f"Missing graph file: {GRAPH_PATH}", file=sys.stderr)
        return 1

    text = GRAPH_PATH.read_text()
    patterns = collect_file_patterns(text)
    if not patterns:
        print("No `files:` entries found in dependencies.yaml", file=sys.stderr)
        return 1

    errors: list[str] = []
    for pattern in patterns:
        resolved = resolve_pattern(REPO_ROOT, pattern)
        if not resolved:
            errors.append(f"no files match `{pattern}`")
            continue
        for path in resolved:
            if not path.is_file():
                errors.append(f"missing file `{path.relative_to(REPO_ROOT)}`")

    if errors:
        print("dependencies.yaml validation failed:\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK: {len(patterns)} file patterns, all paths exist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
