import qrcode


def generate_matrix(
    text: str, error_correction: str = "M", border: int = 4
) -> list[list[bool]]:
    """Generate a QR code matrix from text.

    Returns a 2D list of booleans where True = dark module.
    """
    ec_levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }
    qr = qrcode.QRCode(
        version=None,
        error_correction=ec_levels[error_correction],
        box_size=1,
        border=border,
    )
    qr.add_data(text)
    qr.make(fit=True)
    return qr.get_matrix()
