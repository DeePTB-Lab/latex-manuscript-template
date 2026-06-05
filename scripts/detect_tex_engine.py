#!/usr/bin/env python3
"""Detect the LaTeX engine needed for a manuscript source file."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CJK_RE = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]")
XELATEX_PACKAGE_RE = re.compile(r"\\usepackage(?:\[[^\]]*\])?\{[^}]*\b(?:ctex|xeCJK|fontspec)\b[^}]*\}")
LUALATEX_PACKAGE_RE = re.compile(r"\\usepackage(?:\[[^\]]*\])?\{[^}]*\b(?:luatexja|luacode)\b[^}]*\}")


def detect_engine(source: str) -> str:
    if LUALATEX_PACKAGE_RE.search(source):
        return "lualatex"
    if XELATEX_PACKAGE_RE.search(source) or CJK_RE.search(source):
        return "xelatex"
    return "pdflatex"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="LaTeX source file to inspect")
    args = parser.parse_args()

    if not args.source.exists():
        print(f"error: source file not found: {args.source}", file=sys.stderr)
        return 1

    source = args.source.read_text(encoding="utf-8", errors="replace")
    print(detect_engine(source))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
