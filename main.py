"""Weirdest Job Title entry generator.

Writes a single job title -- the weirdest one we could think of -- to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` (default ``/output``).

The title is a real-sounding bureaucratic role with one hilariously
specific twist: a council officer whose entire job is apologising to
geese on the council's behalf. It reads like a genuine job advert,
which is exactly what makes it funny on first read.

Self-check gates (the entry is refused, not written, if any fail):
  * UTF-8 encodable
  * 1-60 characters long
  * a single line (no newline characters inside the title)
  * not only whitespace
  * no control characters
The file is written with no trailing newline, so its bytes are exactly
the title and nothing else. After writing, the file is read back and
the bytes are compared with the title: a mismatch fails the run, so a
silent write error can never ship a wrong entry.
"""

import os
import sys

TITLE = "Head of Apologizing to Geese on Behalf of the Council"

MAX_LENGTH = 60


def validate(title):
    """Return a list of gate failures; empty means the title passes."""
    failures = []
    try:
        title.encode("utf-8")
    except UnicodeEncodeError:
        failures.append("title is not UTF-8 encodable")
    if not 1 <= len(title) <= MAX_LENGTH:
        failures.append(
            "title must be 1-%d characters, got %d" % (MAX_LENGTH, len(title))
        )
    if title != title.strip() or not title.strip():
        failures.append("title must not be only whitespace or padded")
    if "\n" in title or "\r" in title:
        failures.append("title must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in title):
        failures.append("title contains control characters")
    return failures


def main():
    failures = validate(TITLE)
    if failures:
        for failure in failures:
            print("gate failed: %s" % failure, file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry_path = os.path.join(output_dir, "entry.txt")
    with open(entry_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(TITLE)
    with open(entry_path, "rb") as handle:
        on_disk = handle.read()
    if on_disk != TITLE.encode("utf-8"):
        print("gate failed: file on disk does not match the title", file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(TITLE), entry_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
