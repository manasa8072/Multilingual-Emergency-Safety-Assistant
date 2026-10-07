"""
Text Preprocessing Module for Multilingual Emergency & Safety Assistant.
Preserves Tamil Unicode characters, normalizes whitespace, and converts English characters to lowercase.
"""

import re
import unicodedata


def clean_text(text: str) -> str:
    """
    Common cleaning function for English, Tamil, and Tanglish text.
    
    Requirements:
    - Convert English characters to lowercase
    - Remove unnecessary whitespace / extra spaces
    - Preserve Tamil Unicode characters (U+0B80 - U+0BFF)
    - Do NOT remove Tamil text
    - Do NOT aggressively remove punctuation that may contain useful structural information
    """
    if not isinstance(text, str):
        return ""
    
    # Normalize unicode representations (NFC keeps combined Tamil glyphs intact)
    normalized = unicodedata.normalize("NFC", text)
    
    # Strip leading/trailing whitespaces and lowercase English characters
    lowercased = normalized.strip().lower()
    
    # Replace multiple whitespaces, tabs, and newlines with a single space
    cleaned = re.sub(r"\s+", " ", lowercased)
    
    return cleaned.strip()


if __name__ == "__main__":
    test_inputs = [
        "Emergency: Someone has collapsed.",
        "   எங்கள்   வீட்டில்   தீப்பிடித்துவிட்டது!  ",
        "Road  la   accident aayiduchu, help venum  ",
        "Yaaro enna follow panranga..."
    ]
    for inp in test_inputs:
        print(f"Original: '{inp}' -> Cleaned: '{clean_text(inp)}'")
