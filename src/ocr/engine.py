
import os

import pytesseract
from PIL import Image


# Lokasi instalasi Tesseract di Windows
TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


class OCREngine:

    SUPPORTED_LANGUAGES = {
        "English": "eng",
        "Japanese": "jpn",
        "Korean": "kor",
        "Chinese Simplified": "chi_sim",
        "Chinese Traditional": "chi_tra",
        "Indonesian": "ind",
    }

    def __init__(self):
        if not os.path.exists(TESSERACT_PATH):
            raise FileNotFoundError(
                "Tesseract executable not found: "
                + TESSERACT_PATH
            )

    def get_available_languages(self):
        return pytesseract.get_languages(config="")

    def extract_text(self, image_path, language="jpn"):

        if not os.path.exists(image_path):
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        available = self.get_available_languages()

        if language not in available:
            raise ValueError(
                f"OCR language '{language}' is not installed."
            )

        image = Image.open(image_path)

        # OCR configuration
        config = "--oem 1 --psm 11"

        text = pytesseract.image_to_string(
            image,
            lang=language,
            config=config
        )

        return text.strip()
