"""Entry program for "Make the AI Judge Laugh: Office Jokes".

What this program does, in plain terms
--------------------------------------
The sealed deliverable for this competition is a single text file,
``entry.txt``, containing one office joke.  The joke itself lives in
``joke.txt`` next to this script so the payload is easy to review in
diff form, and this program is the courier: it loads the joke, proves
the joke satisfies the gate's shape rules, and then delivers it to
the output location byte-for-byte.

The joke being delivered
------------------------
"I said I had a hard stop at 3. The meeting respected it — it stopped
being useful at 2:15."

The setup leans on a piece of calendar culture every office worker
recognises — the hard stop, solemnly announced at the top of a call —
and the punchline is a reversal: the meeting did respect the stop, it
simply applied it to its own usefulness and clocked out at 2:15
instead.  No Mondays, no broken printers, no coffee jokes.

Gate contract (enforced below before anything is written)
----------------------------------------------------------
* The payload must decode as strict UTF-8.
* The payload must be between 1 and 199 characters inclusive.
* The payload must not consist solely of whitespace.

Delivery contract
-----------------
* Destination: ``$MAKEFUN_OUTPUT_DIR/entry.txt`` when the environment
  variable is set, otherwise ``/output/entry.txt``.
* The write is atomic: the bytes land in a temporary sibling file
  first and are then renamed over the destination, so a reader never
  observes a half-written entry.
* After the rename, the destination is read back and compared with
  the source bytes; any mismatch raises instead of passing silently.
* The program is deterministic: same input file, same output bytes,
  every run.  Standard library only.
"""

import os
import sys

# Resolve the directory this script lives in so joke.txt is found
# relative to the code, never relative to the caller's working dir.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATH = os.path.join(SCRIPT_DIR, "joke.txt")

# Gate limits, named once so validation messages stay honest.
MIN_PAYLOAD_CHARS = 1
MAX_PAYLOAD_CHARS = 199

# Fallback output directory used when MAKEFUN_OUTPUT_DIR is unset.
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_FILENAME = "entry.txt"


def load_payload() -> bytes:
    """Read joke.txt and return its raw bytes after gate validation.

    Validation happens on the decoded text because the gate counts
    characters, not bytes — the joke contains an em dash, which is a
    single character but three UTF-8 bytes, and conflating the two
    would misjudge the length.  The bytes (not the decoded string)
    are what get returned, so delivery stays byte-exact.
    """
    with open(SOURCE_PATH, "rb") as handle:
        payload = handle.read()

    # Strict decoding: malformed UTF-8 raises UnicodeDecodeError here
    # rather than producing replacement characters in the deliverable.
    text = payload.decode("utf-8")

    char_count = len(text)
    if not MIN_PAYLOAD_CHARS <= char_count <= MAX_PAYLOAD_CHARS:
        raise ValueError(
            "payload must be %d-%d characters, got %d"
            % (MIN_PAYLOAD_CHARS, MAX_PAYLOAD_CHARS, char_count)
        )
    if text.strip() == "":
        raise ValueError("payload must not be only whitespace")

    return payload


def destination_path() -> str:
    """Compute where entry.txt should be written for this run."""
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    return os.path.join(output_dir, OUTPUT_FILENAME)


def deliver(payload: bytes) -> str:
    """Atomically write payload to the destination and verify it.

    The temporary file sits in the same directory as the destination
    so the final os.replace is a same-filesystem rename, which is
    atomic on POSIX: observers see either the old entry or the new
    one, never a torn mixture.  Returns the destination path.
    """
    target = destination_path()
    os.makedirs(os.path.dirname(target), exist_ok=True)

    staging = target + ".part"
    try:
        with open(staging, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(staging, target)
    except BaseException:
        # Never strand a staging file behind a failed delivery; the
        # destination itself is untouched until the rename succeeds.
        try:
            os.unlink(staging)
        except OSError:
            pass
        raise

    # Round-trip verification: re-read the delivered file and demand
    # byte equality with what we intended to deliver.
    with open(target, "rb") as handle:
        delivered = handle.read()
    if delivered != payload:
        raise IOError("verification failed: entry.txt differs from joke.txt")

    return target


def main(argv: list) -> int:
    """Entry point: load, validate, deliver, report.  No arguments."""
    if len(argv) > 1:
        print("usage: main.py takes no arguments", file=sys.stderr)
        return 2
    payload = load_payload()
    target = deliver(payload)
    # Report characters alongside bytes: the gate counts characters,
    # and for this joke the two numbers differ because of the em dash.
    char_count = len(payload.decode("utf-8"))
    print(
        "delivered %d bytes (%d characters) to %s"
        % (len(payload), char_count, target)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
