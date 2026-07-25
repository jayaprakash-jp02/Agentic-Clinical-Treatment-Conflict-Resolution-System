"""
text_cleaner.py

Purpose:
--------
Cleans raw text extracted from PDF documents.

Responsibilities:
- Remove page numbers
- Remove repeated headers
- Remove extra spaces
- Normalize whitespace

This module intentionally DOES NOT:
- Chunk text
- Generate embeddings
- Store vectors
"""

import re


def clean(raw_text: str) -> str:
    """
    Clean raw PDF text.

    Parameters
    ----------
    raw_text : str
        Text extracted from the PDF.

    Returns
    -------
    str
        Cleaned text.
    """

    if not raw_text:
        return ""

    text = raw_text

    # -------------------------------------------------
    # Remove standalone page numbers
    # Example:
    # 1
    # 2
    # 15
    # -------------------------------------------------
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

    # -------------------------------------------------
    # Remove multiple blank lines
    # -------------------------------------------------
    text = re.sub(r'\n\s*\n+', '\n', text)

    # -------------------------------------------------
    # Replace multiple spaces/tabs with a single space
    # -------------------------------------------------
    text = re.sub(r'[ \t]+', ' ', text)

    # -------------------------------------------------
    # Normalize line endings
    # -------------------------------------------------
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # -------------------------------------------------
    # Remove leading/trailing whitespace
    # -------------------------------------------------
    text = text.strip()

    return text