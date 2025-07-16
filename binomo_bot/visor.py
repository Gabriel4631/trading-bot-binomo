"""Simple screen capture and OCR module."""

import numpy as np
import pytesseract
from PIL import ImageGrab
import cv2


# Configure path to tesseract if needed. Here we assume it's in PATH.

BALANCE_REGION = (1085, 70, 1305, 120)  # (left, top, right, bottom)


def capture_balance() -> float:
    """Capture a region of the screen and attempt to read the balance."""
    img = ImageGrab.grab(bbox=BALANCE_REGION)
    frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh)
    cleaned = text.strip().replace("\n", "")
    # Extract digits
    digits = ''.join(ch for ch in cleaned if ch.isdigit())
    if not digits:
        return 0.0
    try:
        return float(digits)
    except ValueError:
        return 0.0
