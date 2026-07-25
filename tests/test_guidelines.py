print("TEST STARTED")
from pathlib import Path

from knowledge.pdf_loader import load_pdf


GUIDELINE_FOLDER = Path("data/guidelines")


for pdf in sorted(GUIDELINE_FOLDER.glob("*.pdf")):

    print("=" * 80)

    print(f"Testing : {pdf.name}")

    print("=" * 80)

    try:

        text = load_pdf(str(pdf))

        print(f"Characters : {len(text)}")

        print()

        print("Preview")

        print("-" * 80)

        print(text[:500])

        print()

        if len(text.strip()) == 0:

            print("FAILED : No text extracted")

        else:

            print("SUCCESS")

    except Exception as e:

        print("FAILED")

        print(e)

    print("\n")