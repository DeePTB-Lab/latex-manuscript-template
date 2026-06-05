#!/usr/bin/env python3
"""Check LaTeX sources for temporary author comments."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


COMMENT_MARKERS = [r"\ZH{", r"\LZ{", r"\TODO{", r"\todo{"]
DEFINITION_PREFIXES = (r"\newcommand", r"\renewcommand", r"\def", r"\DeclareRobustCommand")


def is_macro_definition(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith(DEFINITION_PREFIXES)


def find_comments(path: Path) -> list[tuple[int, str, str]]:
    findings = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if is_macro_definition(line):
            continue
        for marker in COMMENT_MARKERS:
            if marker in line:
                findings.append((line_number, marker, line.strip()))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="LaTeX source files to check")
    args = parser.parse_args()

    failed = False
    for path in args.files:
        if not path.exists():
            print(f"error: source file not found: {path}", file=sys.stderr)
            failed = True
            continue
        for line_number, marker, line in find_comments(path):
            if not failed:
                print("Temporary author comment check failed:", file=sys.stderr)
            failed = True
            print(f"- {path}:{line_number}: found {marker} in `{line}`", file=sys.stderr)

    if failed:
        return 1

    print(f"Checked {len(args.files)} LaTeX source file(s): no temporary author comments found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
