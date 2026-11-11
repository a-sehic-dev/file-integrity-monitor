# File Integrity Monitor

SHA-256 baseline of a directory you own. Later you compare disk to that snapshot: **changed**, **added**, **removed**.

This is the same idea as AIDE / Tripwire, in a small Python tool. No network. No kernel module. Lab and own hosts only.

Portfolio piece for defensive Python + Linux ([Sedin Šehić](https://github.com/a-sehic-dev)). Sister tool: [linux-log-agent](https://github.com/a-sehic-dev/linux-log-agent).

## Why it matters

If `app.conf` changes and nobody ticketed it, that is an integrity event. Hash the tree once. Verify on a schedule. Drift is the alert.

## Requirements

- Python 3.8+
- Standard library only

## Run

Create the baseline:

```bash
python fim.py init
```

Verify (exit code `0` = clean, `1` = drift):

```bash
python fim.py check
```

Custom path:

```bash
python fim.py init --path /etc --baseline ./etc.baseline.json
python fim.py check --path /etc --baseline ./etc.baseline.json
```

Only directories you are allowed to read. Do not point this at other people's machines.

## Tests

```bash
python -m unittest tests.test_fim
```

## How you know it works

1. `python -m unittest tests.test_fim` → `OK`
2. `python fim.py init` then `python fim.py check` → `[OK] Baseline matches disk`
3. Edit `samples/watched/notes.txt`, run `check` again → `[CHANGED] notes.txt` and exit code 1
4. Restore the file, `check` → `[OK]` again

## Stack

Python · SHA-256 · JSON baseline

## License

MIT
