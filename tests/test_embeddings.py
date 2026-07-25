from pathlib import Path

from knowledge.pdf_loader import load_pdf
from knowledge.text_cleaner import clean
from knowledge.chunker import split
from knowledge.embeddings import EmbeddingGenerator


GUIDELINE_FOLDER = Path("data/guidelines")

embedding_generator = EmbeddingGenerator()


for pdf in sorted(GUIDELINE_FOLDER.glob("*.pdf")):

    print("=" * 100)
    print(pdf.name)
    print("=" * 100)

    raw_text = load_pdf(str(pdf))

    cleaned_text = clean(raw_text)

    chunks = split(cleaned_text)

    print("Generating embeddings...")

    vectors = embedding_generator.create_embeddings(
        chunks[:5]
    )

    print()

    print("Embedding Shape :", vectors.shape)

    print("Embedding Type  :", vectors.dtype)

    print()

    print("First Vector (first 10 values)")

    print(vectors[0][:10])

    print()

    print("SUCCESS")

    print("\n")