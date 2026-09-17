#!/usr/bin/env python3
"""Consistency checks for the personal directives (AI.md + people/).

Dependency-free and fast, so an agent can run it before every commit that
touches these files. Exits non-zero on any failure and says what to fix.

    python3 scripts/check-personal-directives.py

Checks:
  1. AI.md's `Revision:` date matches the receipt token assistants echo back.
     They sit in two places in one file and drift silently.
  2. paste-block.md's never-use list is a subset of AI.md's. The paste block
     is deliberately shorter; it must never ban a word AI.md allows.
  3. No em dashes anywhere in the personal directives. SJ's hardest rule,
     and the one an assistant is most likely to reintroduce while editing.
  4. No model, vendor, or tool names in the instruction files, so the same
     files serve every assistant.
  5. paste-block.md is not older than AI.md in git history. The paste block
     duplicates AI.md's rules by hand; if AI.md moved on alone, say so.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AI = ROOT / "AI.md"
PROFILE = ROOT / "people" / "sunil-james"
PASTE = PROFILE / "paste-block.md"

# Files an assistant reads as directives. Their own README is operator
# documentation and may name platforms, so it is not in this list.
INSTRUCTION_FILES = [AI, PASTE, PROFILE / "working-agreement.md", PROFILE / "writing-style.md"]

VENDORS = r"\b(claude|anthropic|chatgpt|openai|gpt-[0-9]|gemini|bard|copilot|llama|mistral|grok|perplexity)\b"

failures: list[str] = []
notes: list[str] = []


def fail(check: str, detail: str) -> None:
    failures.append(f"{check}: {detail}")


def never_use_words(text: str) -> set[str]:
    m = re.search(r"\*\*Never use:\*\*(.+?)(?:\n|$)", text, re.S)
    if not m:
        m = re.search(r"Never use:(.+?)(?:\n|$)", text, re.S)
    if not m:
        return set()
    body = re.split(r"\.\s+(?:No |Fuller |$)", m.group(1))[0]
    body = body.replace("*", "")
    return {w.strip().lower().split("(")[0].strip() for w in body.split(",") if w.strip()}


def main() -> int:
    ai = AI.read_text()

    # 1. revision date vs receipt token
    rev = re.search(r"\*\*Revision:\s*(\d{4}-\d{2}-\d{2})\*\*", ai)
    receipt = re.search(r"\[directives (\d{4}-\d{2}-\d{2})\]", ai)
    if not rev:
        fail("revision", "AI.md has no `**Revision: YYYY-MM-DD**` line")
    elif not receipt:
        fail("revision", "AI.md has no `[directives YYYY-MM-DD]` receipt token")
    elif rev.group(1) != receipt.group(1):
        fail("revision", f"AI.md revision {rev.group(1)} != receipt {receipt.group(1)}; bump both")

    # 2. never-use list is a subset
    extra = never_use_words(PASTE.read_text()) - never_use_words(ai)
    if extra:
        fail("never-use", f"paste-block.md bans words AI.md allows: {sorted(extra)}")

    # 3. no em dashes
    for f in INSTRUCTION_FILES + [PROFILE / "README.md", ROOT / "people" / "README.md"]:
        for i, line in enumerate(f.read_text().splitlines(), 1):
            if "—" in line:
                fail("em-dash", f"{f.relative_to(ROOT)}:{i} contains an em dash")

    # 4. vendor-neutral instruction files
    for f in INSTRUCTION_FILES:
        for i, line in enumerate(f.read_text().splitlines(), 1):
            hit = re.search(VENDORS, line, re.I)
            if hit:
                fail("vendor", f"{f.relative_to(ROOT)}:{i} names '{hit.group(0)}'")

    # 5. paste block not left behind
    try:
        def last_commit(p: Path) -> str:
            out = subprocess.run(
                ["git", "-C", str(ROOT), "log", "-1", "--format=%ct", "--", str(p)],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
            return out
        ai_t, paste_t = last_commit(AI), last_commit(PASTE)
        if ai_t and paste_t and int(ai_t) > int(paste_t):
            notes.append(
                "paste-block.md was last committed before AI.md. If you changed a rule, "
                "change it in both; if the AI.md edit was cosmetic, ignore this."
            )
    except (subprocess.CalledProcessError, ValueError):
        pass

    for n in notes:
        print(f"note:  {n}")
    for f in failures:
        print(f"FAIL:  {f}")
    if failures:
        print(f"\n{len(failures)} check(s) failed.")
        return 1
    print(f"ok:    personal directives consistent ({len(INSTRUCTION_FILES)} instruction files checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
