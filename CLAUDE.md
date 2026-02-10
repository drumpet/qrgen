# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run

```bash
pip install -e .          # install in editable mode
qrgen "Hello World"       # run via console script
python -m qrgen "test"    # run via module
```

No test suite or linter is configured yet.

## Architecture

The tool encodes text as a QR code and renders it fullscreen in the terminal using Unicode half-block characters (`▀▄█ `), re-rendering responsively on terminal resize.

**Data flow:** `cli.py` → `qr.py` → `app.py` → `renderer.py`

- **cli.py** — argparse entry point (`main()`). Parses args, calls `generate_matrix()`, then hands the boolean matrix to `app.run()`.
- **qr.py** — Thin wrapper around the `qrcode` library. `generate_matrix()` returns a `list[list[bool]]` (True = dark module).
- **renderer.py** — Pure-function rendering engine. `compute_scale()` finds the largest integer scale fitting the terminal. `render()` scales the matrix, pairs pixel rows into half-block characters, centers the output, and returns exactly `term_height` lines of exactly `term_width` chars.
- **app.py** — Fullscreen display loop using `blessed`. Handles SIGWINCH for resize, polls input with `inkey(timeout=0.1)`, exits on `q`/Escape/Ctrl-C.

## Key Design Details

- Half-block rendering encodes 2 vertical pixels per terminal row, accounting for the ~2:1 height:width ratio of monospace cells.
- `render()` is a pure function (no terminal I/O) — pass any dimensions for testing.
- The app redraws only when `needs_redraw` is set by the SIGWINCH handler.
