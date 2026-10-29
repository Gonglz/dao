#!/usr/bin/env python3
"""Ensure maintained Chinese translations explicitly match their English Git blobs.

This is a freshness test, NOT a semantic translation review. No external deps.
"""
from __future__ import annotations
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAIRS = (
    ("README.md", "README.zh-CN.md"),
    ("AGENTS.md", "AGENTS.zh-CN.md"),
    ("docs/PROJECT.md", "docs/PROJECT.zh-CN.md"),
    ("templates/CHAT_TASK_PROMPT.md", "templates/CHAT_TASK_PROMPT.zh-CN.md"),
    ("templates/STAKEHOLDER_STATUS_BRIEF.md", "templates/STAKEHOLDER_STATUS_BRIEF.zh-CN.md"),
)
STAMP = re.compile(r"\A<!-- Source blob SHA: ([0-9a-f]{40}) -->\r?\n")


def blob_sha(source: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(source)).encode() + b"\0" + source).hexdigest()


def verify(root: Path = ROOT) -> list[str]:
    errors = []
    for source, translation in PAIRS:
        src, dst = root / source, root / translation
        if not src.is_file() or not dst.is_file():
            errors.append(f"Missing language pair: {source} / {translation}")
            continue
        actual = blob_sha(src.read_bytes())
        stamp = STAMP.match(dst.read_text(encoding="utf-8"))
        if stamp is None:
            errors.append(f"{translation}: missing source SHA metadata")
        elif stamp.group(1) != actual:
            errors.append(f"{translation}: English source {source} changed (expected {actual}); update translation and source SHA")
    return errors


if __name__ == "__main__":
    problems = verify()
    for problem in problems:
        print("ERROR:", problem, file=sys.stderr)
    if problems:
        raise SystemExit(1)
    print(f"PASS: {len(PAIRS)} bilingual documentation pairs match their English source revisions")
