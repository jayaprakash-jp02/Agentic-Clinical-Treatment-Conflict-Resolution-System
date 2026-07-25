from pathlib import Path
import fitz


def load_pdf(pdf_path: str) -> str:
    """
    Load a PDF and return all extracted text.
    """

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    try:
        document = fitz.open(pdf_file)

        pages = []

        for page in document:
            pages.append(page.get_text())

        document.close()

        return "\n".join(pages)

    except Exception as e:
        raise RuntimeError(
            f"Unable to load PDF: {e}"
        )