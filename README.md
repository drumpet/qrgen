# qrgen

CLI tool that renders full-terminal, responsive QR codes using Unicode half-block characters. The QR code scales to fill your terminal and re-renders on resize.

## Install

```bash
pip install .
```

## Usage

```bash
qrgen "Hello World"
qrgen "https://example.com" --invert --ec H
python -m qrgen "test"
```

Press `q` or `Escape` to exit.

### Options

| Flag | Description |
|---|---|
| `-i`, `--invert` | Invert colors (light-on-dark) |
| `--ec {L,M,Q,H}` | Error correction level (default: M) |
| `--border N` | Border size in modules (default: 4) |

## Requirements

Python 3.10+
