#!/usr/bin/env python3
"""Fail CI on unresolved LaTeX references, citations, and build warnings."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FAIL_PATTERNS = [
    re.compile(r"^! LaTeX Error:", re.MULTILINE),
    re.compile(r"LaTeX Warning: Reference `[^']+' .* undefined", re.MULTILINE),
    re.compile(r"Package natbib Warning: Citation `[^']+' .* undefined", re.MULTILINE),
    re.compile(r"Package natbib Warning: There were undefined citations", re.MULTILINE),
    re.compile(r"There were undefined references", re.MULTILINE),
    re.compile(r"Rerun to get citations correct", re.MULTILINE),
    re.compile(r"BibTeX .*Warning", re.MULTILINE),
    re.compile(r"Warning--", re.MULTILINE),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log_file", type=Path, help="LaTeX log file to check")
    args = parser.parse_args()

    log = args.log_file.read_text(encoding="utf-8", errors="replace")
    failures = []
    for pattern in FAIL_PATTERNS:
        failures.extend(match.group(0).strip() for match in pattern.finditer(log))

    if not failures:
        print(f"Checked {args.log_file}: no blocking LaTeX warnings found.")
        return 0

    print(f"LaTeX log check failed for {args.log_file}:", file=sys.stderr)
    for failure in sorted(set(failures)):
        print(f"- {failure}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
