#!/usr/bin/env python3
"""Check BibTeX files for duplicate entries."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ENTRY_RE = re.compile(r"@(?P<type>[A-Za-z]+)\s*\{\s*(?P<key>[^,\s]+)\s*,", re.MULTILINE)
FIELD_RE = re.compile(
    r"(?P<name>[A-Za-z][A-Za-z0-9_-]*)\s*=\s*(?P<value>\{(?:[^{}]|\{[^{}]*\})*\}|\"[^\"]*\"|[^,\n]+)",
    re.MULTILINE,
)


def find_entry_end(text: str, start: int) -> int:
    depth = 0
    in_quote = False
    escaped = False

    for index in range(start, len(text)):
        char = text[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            in_quote = not in_quote
            continue
        if in_quote:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index + 1

    return len(text)


def normalize_value(value: str) -> str:
    value = value.strip().strip("{}\"")
    value = re.sub(r"[{}\\]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.casefold().strip()


def parse_entries(path: Path) -> list[dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    entries = []

    for match in ENTRY_RE.finditer(text):
        entry_end = find_entry_end(text, match.start())
        body = text[match.end() : entry_end]
        fields = {
            field.group("name").casefold(): normalize_value(field.group("value"))
            for field in FIELD_RE.finditer(body)
        }
        entries.append(
            {
                "file": str(path),
                "key": match.group("key"),
                "type": match.group("type").casefold(),
                **fields,
            }
        )

    return entries


def add_duplicate(groups: dict[str, list[dict[str, str]]], label: str, entry: dict[str, str]) -> None:
    groups.setdefault(label, []).append(entry)


def entry_location(entry: dict[str, str]) -> str:
    return f"{entry['file']}:{entry['key']}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path, help="BibTeX files to check")
    args = parser.parse_args()

    entries = [entry for path in args.files for entry in parse_entries(path)]
    duplicate_groups: dict[str, list[dict[str, str]]] = {}
    seen_keys: dict[str, dict[str, str]] = {}
    seen_doi: dict[str, dict[str, str]] = {}
    seen_title_year: dict[str, dict[str, str]] = {}

    for entry in entries:
        key = entry["key"].casefold()
        if key in seen_keys:
            add_duplicate(duplicate_groups, f"duplicate key `{entry['key']}`", seen_keys[key])
            add_duplicate(duplicate_groups, f"duplicate key `{entry['key']}`", entry)
        else:
            seen_keys[key] = entry

        doi = entry.get("doi", "")
        if doi:
            doi_key = doi.removeprefix("https://doi.org/").removeprefix("http://dx.doi.org/")
            if doi_key in seen_doi:
                add_duplicate(duplicate_groups, f"duplicate DOI `{doi}`", seen_doi[doi_key])
                add_duplicate(duplicate_groups, f"duplicate DOI `{doi}`", entry)
            else:
                seen_doi[doi_key] = entry

        title = entry.get("title", "")
        year = entry.get("year", "")
        if title and year:
            title_year_key = f"{title}|{year}"
            if title_year_key in seen_title_year:
                add_duplicate(duplicate_groups, f"duplicate title/year `{title}` ({year})", seen_title_year[title_year_key])
                add_duplicate(duplicate_groups, f"duplicate title/year `{title}` ({year})", entry)
            else:
                seen_title_year[title_year_key] = entry

    if not duplicate_groups:
        print(f"Checked {len(entries)} BibTeX entries: no duplicates found.")
        return 0

    print("BibTeX duplicate check failed:", file=sys.stderr)
    for label, group in duplicate_groups.items():
        unique_locations = sorted({entry_location(entry) for entry in group})
        print(f"- {label}: {', '.join(unique_locations)}", file=sys.stderr)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
