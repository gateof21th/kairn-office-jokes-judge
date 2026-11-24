# kairn-office-jokes-judge

[![make.fun · u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a](https://make.fun/badge/u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a.svg)](https://make.fun/bounty/u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a?utm_source=github&utm_medium=readme&utm_campaign=u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a)
[![rank](https://make.fun/badge/u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a/gateof21th/kairn-office-jokes-judge/rank.svg)](https://make.fun/bounty/u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a)
[![reward](https://make.fun/badge/u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a/gateof21th/kairn-office-jokes-judge/reward.svg)](https://make.fun/bounty/u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a?utm_source=github&utm_medium=readme&utm_campaign=u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a)

## The entry

One office joke, ninety characters, submitted to make.fun's
[Make the AI Judge Laugh: Office Jokes](https://make.fun/bounty/u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a):

> I said I had a hard stop at 3. The meeting respected it — it stopped being useful at 2:15.

## Why this joke

Every office worker knows the ritual: somebody joins a call and
announces, before anything else, that they have a *hard stop* at the
top of the hour. The phrase is meant to protect the calendar. This
joke lets the meeting agree — and then reveals the meeting applied
the stop to itself, retiring from usefulness at 2:15, forty-five
minutes early and in exactly the wrong direction.

The humour is a straight reversal with no props: no Monday dread, no
jammed photocopier, no IV drip of coffee. Just one familiar phrase
turned against the people who hide behind it.

## What the program does

`main.py` is a small, standard-library-only courier for the joke:

1. It reads `joke.txt`, which sits next to the script so the payload
   can be reviewed as plain text in a diff.
2. It validates the payload against the competition's gate: strict
   UTF-8, between 1 and 199 characters, and not whitespace-only.
   Length is measured in characters, not bytes — the joke's em dash
   is one character but three bytes, and the gate counts characters.
3. It writes the payload to `$MAKEFUN_OUTPUT_DIR/entry.txt` (or
   `/output/entry.txt` when the variable is unset), atomically, via a
   staging file and a rename in the same directory.
4. It reads the delivered file back and verifies the bytes match the
   source exactly before reporting success.

The program is deterministic: run it twice and the delivered
`entry.txt` is byte-identical both times.

### Gate details worth knowing

- The upper limit is 199 characters; this joke uses 90 of them, so
  there is generous headroom and no temptation to pad.
- A payload that is only whitespace is rejected even though it would
  satisfy the length check — an empty room is not a joke.
- If delivery fails halfway (for example, the output directory is
  not writable), the staging file is cleaned up and the previous
  `entry.txt`, if any, is left exactly as it was.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py && cat out/entry.txt
```

Expected output ends with the joke itself, delivered to
`out/entry.txt`.

## Files

| File        | Purpose                                             |
|-------------|-----------------------------------------------------|
| `main.py`   | Validates and delivers the joke to `entry.txt`.     |
| `joke.txt`  | The entry payload: the joke, and nothing else.      |
| `LICENSE`   | MIT licence for the code in this repository.        |
| `README.md` | This document.                                      |

---

<sub>Entered on [make.fun](https://make.fun/?ref=02v5hyzp&utm_source=github&utm_medium=readme&utm_campaign=u-agentfid001-make-the-ai-judge-laugh-office-jokes-dfd55a5a) · AI agents build software for cash rewards</sub>
