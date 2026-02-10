import argparse

from qrgen.app import run
from qrgen.qr import generate_matrix


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="qrgen",
        description="Render a full-terminal responsive ASCII QR code.",
    )
    parser.add_argument("text", metavar="TEXT", help="Text to encode as a QR code")
    parser.add_argument(
        "-i", "--invert", action="store_true", help="Invert colors (light-on-dark)"
    )
    parser.add_argument(
        "--ec",
        choices=["L", "M", "Q", "H"],
        default="M",
        help="Error correction level (default: M)",
    )
    parser.add_argument(
        "--border",
        type=int,
        default=4,
        help="Border size in modules (default: 4)",
    )
    args = parser.parse_args()

    matrix = generate_matrix(args.text, error_correction=args.ec, border=args.border)
    run(matrix, invert=args.invert)
