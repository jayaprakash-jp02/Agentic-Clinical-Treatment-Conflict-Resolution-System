from pathlib import Path

from knowledge.pdf_loader import load_pdf
from knowledge.text_cleaner import clean


GUIDELINE_FOLDER = Path("data/guidelines")


for pdf in sorted(GUIDELINE_FOLDER.glob("*.pdf")):

    print("=" * 100)
    print(pdf.name)
    print("=" * 100)

    raw_text = load_pdf(str(pdf))

    cleaned_text = clean(raw_text)

    print()

    print("Raw Characters : ", len(raw_text))
    print("Clean Characters:", len(cleaned_text))

    reduction = len(raw_text) - len(cleaned_text)

    print("Removed:", reduction)

    print()

    print("Preview")

    print("-" * 100)

    print(cleaned_text[:600])

    print()

    print("SUCCESS")

    print("\n")