"""Make the AI Judge Laugh: Office Jokes — entry writer.

The joke: "I said I had a hard stop at 3. The meeting respected it — it
stopped being useful at 2:15." Calendar culture gives the setup (the
hard stop everyone announces), and the reversal gives the punchline:
the meeting honoured the stop, just forty-five minutes early and in
the wrong way. No Monday, no photocopier, no coffee drip.

Writes joke.txt verbatim to $MAKEFUN_OUTPUT_DIR/entry.txt (default
/output/entry.txt), exactly as the sealed gate wants it: UTF-8 text of
1 to 199 characters, not only white space, byte-identical across runs.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
JOKE_FILE = os.path.join(HERE, "joke.txt")
MAX_CHARS = 199


def read_joke() -> bytes:
    with open(JOKE_FILE, "rb") as fh:
        data = fh.read()
    text = data.decode("utf-8")  # strict: raises on invalid UTF-8
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"joke must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("joke must not be only white space")
    return data


def write_output(data: bytes) -> str:
    """Write entry.txt atomically (temp file + rename in the same
    directory) so the artifact is never a partial write, then read it
    back and verify the bytes round-tripped exactly."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    tmp_path = out_path + ".tmp"
    with open(tmp_path, "wb") as fh:
        fh.write(data)
    os.replace(tmp_path, out_path)
    with open(out_path, "rb") as fh:
        written = fh.read()
    if written != data:
        raise ValueError("entry.txt round-trip mismatch")
    return out_path


def main() -> int:
    data = read_joke()
    out_path = write_output(data)
    print(f"wrote {out_path} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
