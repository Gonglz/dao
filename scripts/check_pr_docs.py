#!/usr/bin/env python3
"""Small, deterministic PR documentation-impact gate.

This checks the author's declaration, not semantic correctness. Contract behavior
must still be validated by executable tests and reviewed when policy changes.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

OPTIONS = (
    "No maintained documentation change",
    "Maintained documentation updated",
    "Contract change requires review",
)


def _checked_option(body: str) -> list[str]:
    return [
        option for option in OPTIONS
        if re.search(r"(?im)^\s*-\s*\[x\]\s*" + re.escape(option) + r"\s*$", body)
    ]


def _field(body: str, label: str) -> str:
    match = re.search(r"(?im)^\s*" + re.escape(label) + r":\s*(.+)$", body)
    if not match:
        return ""
    value = match.group(1).strip()
    return "" if value in ("-", "...", "n/a", "N/A") else value


def check(body: str, paths: list[str]) -> list[str]:
    errors: list[str] = []
    selections = _checked_option(body)
    if len(selections) != 1:
        return ["Select exactly one Documentation Impact checkbox in the PR body."]
    choice = selections[0]
    maintained_docs = [
        p for p in paths
        if p in ("AGENTS.md", "README.md", "ENGINEERING.md")
        or (p.startswith("docs/") and p.endswith(".md")
            and not p.startswith(("docs/audits/", "docs/history/", "docs/_tmp/", "docs/_handoff/")))
    ]
    implementation = [
        p for p in paths
        if p.startswith(("src/", "scripts/", "config/", "deploy/", ".github/workflows/"))
    ]
    if choice == OPTIONS[0]:
        if maintained_docs:
            errors.append("Maintained documentation changed: select the updated-docs option.")
        if implementation and len(_field(body, "Reason")) < 12:
            errors.append("Explain why implementation/config changes do not affect maintained docs (Reason: ...).")
    elif choice == OPTIONS[1]:
        if not maintained_docs:
            errors.append("Docs-updated selected but no maintained documentation file is in the diff.")
        if len(_field(body, "Affected docs")) < 5:
            errors.append("List affected documentation (Affected docs: ...).")
    else:
        if len(_field(body, "Contract evidence")) < 8:
            errors.append("Describe the proposed contract change and approval reference (Contract evidence: ...).")
        if len(_field(body, "Tests")) < 5:
            errors.append("Identify executable contract checks (Tests: ...).")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_pr_docs.py EVENT_JSON", file=sys.stderr)
        return 2
    event = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    pr = event.get("pull_request")
    if not pr:
        print("Documentation Impact: not a pull_request event; skipped.")
        return 0
    base_sha = pr["base"]["sha"]
    paths = subprocess.check_output(
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", base_sha, "HEAD"], text=True
    ).splitlines()
    errors = check(pr.get("body") or "", paths)
    print("Documentation Impact: " + ("PASS" if not errors else "FAIL"))
    print("Changed files: " + ", ".join(paths[:30]))
    for error in errors:
        print("ERROR: " + error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
