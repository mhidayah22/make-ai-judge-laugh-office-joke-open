#!/usr/bin/env python3
"""Make the AI Judge Laugh: the Office Joke Open.

Writes the chosen one-line office joke to entry.txt. The program is
fully deterministic: no clock, no randomness, no network, no input.
It honours MAKEFUN_OUTPUT_DIR first, then /output, then a local
fallback, and reads the file back to check what it wrote.
"""

import os
import sys

JOKE = (
    "Our printer has been out of toner since March, but the sign "
    "saying 'out of toner' prints perfectly every time."
)


def choose_dir():
    for candidate in (os.environ.get("MAKEFUN_OUTPUT_DIR"), "/output"):
        if candidate:
            return candidate
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "output")


def main():
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in JOKE):
        print("joke must not contain control characters", file=sys.stderr)
        return 1
    if "\n" in JOKE or "\r" in JOKE:
        print("joke must be a single line", file=sys.stderr)
        return 1
    if JOKE != JOKE.strip():
        print("joke must not start or end with whitespace", file=sys.stderr)
        return 1
    if not 1 <= len(JOKE) <= 200:
        print("joke must be 1-200 characters", file=sys.stderr)
        return 1
    if not JOKE.isascii():
        # The joke is plain ASCII; a non-ASCII character here would be a typo.
        print("joke must be plain ASCII", file=sys.stderr)
        return 1
    directory = choose_dir()
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(JOKE + "\n")
    with open(path, "rb") as handle:
        raw = handle.read()
    try:
        written = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("entry.txt is not valid UTF-8", file=sys.stderr)
        return 1
    if written != JOKE + "\n":
        print("round-trip verification failed", file=sys.stderr)
        return 1
    print("wrote %d characters (%d bytes) to %s"
          % (len(JOKE), len(raw), path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
