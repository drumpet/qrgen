import signal

from blessed import Terminal

from qrgen.renderer import render


def run(matrix: list[list[bool]], invert: bool = False) -> None:
    """Run the fullscreen QR display loop with responsive resizing."""
    term = Terminal()
    needs_redraw = True

    def on_resize(signum: int, frame: object) -> None:
        nonlocal needs_redraw
        needs_redraw = True

    signal.signal(signal.SIGWINCH, on_resize)

    with term.fullscreen(), term.hidden_cursor(), term.cbreak():
        try:
            while True:
                if needs_redraw:
                    needs_redraw = False
                    lines = render(matrix, term.height, term.width, invert=invert)
                    buf = []
                    for y, line in enumerate(lines):
                        buf.append(term.move_xy(0, y) + line)
                    print("".join(buf), end="", flush=True)

                key = term.inkey(timeout=0.1)
                if key:
                    if key == "q" or key.code == term.KEY_ESCAPE:
                        break
        except KeyboardInterrupt:
            pass
