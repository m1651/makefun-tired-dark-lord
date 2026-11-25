"""The Tired Dark Lord: a 100-word villain monologue.

Writes the monologue to ``entry.txt`` in MAKEFUN_OUTPUT_DIR (default /output)
and enforces the competition gate in code: UTF-8 text, 1-600 characters,
not only whitespace, and exactly 100 words.
"""

import os
import sys

ENTRY = (
    "Heroes, sit. Not the throne \u2014 the stool by the hearth. "
    "The throne's back has been digging into me since the third siege, "
    "and I have stopped pretending otherwise. You came to end me, yes? "
    "Lovely. Give me a moment. The kettle, the good cups, the ones "
    "without chips. I have poisoned kingdoms with less ceremony than "
    "this tea. Three centuries I have kept the northern passes shut, "
    "the tolls collected, the ravens fed, and still every spring some "
    "bright-eyed child climbs my stairs with a borrowed sword. "
    "Drink up, please. The door locks behind you, darling. "
    "It always did."
)

EXPECTED_WORDS = 100
MIN_CHARS = 1
MAX_CHARS = 600
# The judge rewards tiredness felt in rhythm and deflection, never announced:
# the entry must not simply say the villain is tired/weary/exhausted.
BANNED_WORDS = ("tired", "weary", "exhausted", "fatigued", "sleepy")


def main() -> int:
    words = ENTRY.split()
    if len(words) != EXPECTED_WORDS:
        print(f"gate failed: {len(words)} words, expected {EXPECTED_WORDS}",
              file=sys.stderr)
        return 1
    if not (MIN_CHARS <= len(ENTRY) <= MAX_CHARS):
        print(f"gate failed: {len(ENTRY)} chars, allowed {MIN_CHARS}-{MAX_CHARS}",
              file=sys.stderr)
        return 1
    if not ENTRY.strip():
        print("gate failed: entry is only whitespace", file=sys.stderr)
        return 1
    if "\n" in ENTRY or "\r" in ENTRY:
        print("gate failed: entry must be a single line", file=sys.stderr)
        return 1
    lowered = ENTRY.lower()
    for banned in BANNED_WORDS:
        if banned in lowered:
            print(f"gate failed: entry announces tiredness ({banned!r})",
                  file=sys.stderr)
            return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(ENTRY)

    # Round-trip verify the written bytes: exact text, exact byte length,
    # and re-check the gate against what is actually on disk.
    with open(path, "rb") as f:
        raw = f.read()
    on_disk = raw.decode("utf-8")
    if on_disk != ENTRY:
        print("gate failed: round-trip mismatch", file=sys.stderr)
        return 1
    if len(raw) != len(ENTRY.encode("utf-8")):
        print("gate failed: byte length mismatch", file=sys.stderr)
        return 1
    if not (MIN_CHARS <= len(on_disk) <= MAX_CHARS) or len(on_disk.split()) != EXPECTED_WORDS:
        print("gate failed: on-disk text fails the gate", file=sys.stderr)
        return 1

    print(f"wrote {path}: {len(words)} words, {len(ENTRY)} chars, "
          f"{len(raw)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
