TOP_HALF = "\u2580"  # ▀ — top dark, bottom light
BOTTOM_HALF = "\u2584"  # ▄ — top light, bottom dark
FULL_BLOCK = "\u2588"  # █ — both dark
EMPTY = " "  # both light


def compute_scale(matrix_size: int, term_width: int, term_height: int) -> int:
    """Compute the largest integer scale that fits the terminal.

    Each terminal cell is roughly 2:1 (height:width), so we use half-block
    characters to get 2 vertical pixels per row.
    """
    scale_x = term_width // matrix_size
    scale_y = (term_height * 2) // matrix_size
    return max(1, min(scale_x, scale_y))


def render(
    matrix: list[list[bool]],
    term_height: int,
    term_width: int,
    invert: bool = False,
) -> list[str]:
    """Render a QR matrix as lines of half-block Unicode characters.

    Returns exactly `term_height` lines, each exactly `term_width` characters,
    centered in the terminal.
    """
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    scale = compute_scale(cols, term_width, term_height)

    # Build scaled pixel grid
    scaled_rows = rows * scale
    scaled_cols = cols * scale

    def pixel(r: int, c: int) -> bool:
        """Get the pixel value at scaled coordinates."""
        val = matrix[r // scale][c // scale]
        return (not val) if invert else val

    # Pair rows and encode to half-block characters
    qr_lines: list[str] = []
    for y in range(0, scaled_rows, 2):
        line_chars: list[str] = []
        for x in range(scaled_cols):
            top = pixel(y, x)
            bot = pixel(y + 1, x) if y + 1 < scaled_rows else False
            if top and bot:
                line_chars.append(FULL_BLOCK)
            elif top:
                line_chars.append(TOP_HALF)
            elif bot:
                line_chars.append(BOTTOM_HALF)
            else:
                line_chars.append(EMPTY)
        qr_lines.append("".join(line_chars))

    # Center vertically
    qr_height = len(qr_lines)
    pad_top = max(0, (term_height - qr_height) // 2)
    pad_bottom = max(0, term_height - qr_height - pad_top)

    # Center horizontally and pad each line to exact terminal width
    def center_line(line: str) -> str:
        pad_left = max(0, (term_width - len(line)) // 2)
        padded = " " * pad_left + line
        return padded.ljust(term_width)[:term_width]

    output: list[str] = []
    output.extend(" " * term_width for _ in range(pad_top))
    output.extend(center_line(line) for line in qr_lines)
    output.extend(" " * term_width for _ in range(pad_bottom))

    return output[:term_height]
