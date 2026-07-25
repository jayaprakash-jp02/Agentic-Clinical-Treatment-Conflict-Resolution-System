from pathlib import Path

from knowledge.pdf_loader import load_pdf
from knowledge.text_cleaner import clean
from knowledge.chunker import split


GUIDELINE_FOLDER = Path("data/guidelines")


for pdf in sorted(GUIDELINE_FOLDER.glob("*.pdf")):

    print("=" * 100)
    print(pdf.name)
    print("=" * 100)

    raw_text = load_pdf(str(pdf))

    cleaned_text = clean(raw_text)

    chunks = split(cleaned_text)

    print()

    print("Total Chunks :", len(chunks))

    print()

    print("First Chunk")

    print("-" * 100)

    print(chunks[0])

    print()

    print("First Chunk Length :", len(chunks[0]))

    print()

    print("Last Chunk Length :", len(chunks[-1]))

    print()

    print("SUCCESS")

    print("\n")