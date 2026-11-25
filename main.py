#!/usr/bin/env python3
"""Fix Human Sleep: Funniest Patch Note.

Writes a single patch-note line announcing that human sleep has been
fixed to /output/entry.txt, enforcing the competition's sealed gate:
UTF-8 text of 1 to 160 characters, a single non-blank line.
"""

import sys
from pathlib import Path

ENTRY = (
    "v2.4.1 — Fixed: humans now fall asleep in under 8 hours "
    "instead of lying awake replaying a conversation from 2019."
)

MAX_CHARS = 160
OUTPUT_PATH = Path("/output/entry.txt")


def validate_entry(text: str) -> None:
    """Fail loudly unless the entry passes the sealed gate."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(text)}"
        )
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")  # raises if the text is not valid UTF-8


def write_entry(text: str, path: Path = OUTPUT_PATH) -> int:
    validate_entry(text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    # Round-trip read-back: what landed on disk must be exactly the entry.
    if path.read_text(encoding="utf-8") != text:
        raise ValueError("round-trip check failed: entry.txt differs")
    return len(text)


def main() -> int:
    count = write_entry(ENTRY)
    print(f"Wrote {count} characters to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
