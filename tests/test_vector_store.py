from pathlib import Path

from knowledge.pdf_loader import load_pdf
from knowledge.text_cleaner import clean
from knowledge.chunker import split
from knowledge.embeddings import EmbeddingGenerator
from knowledge.vector_store import VectorStore


pdf = Path(
    "data/guidelines/ADA_2025.pdf"
)

text = load_pdf(str(pdf))

text = clean(text)

chunks = split(text)

generator = EmbeddingGenerator()

vectors = generator.create_embeddings(chunks)

store = VectorStore()

store.build_index(vectors)

store.save_index(
    "processed/ADA_2025/index.faiss"
)

store.save_metadata(
    chunks,
    "processed/ADA_2025/metadata.pkl"
)

print()

print("Dimension :", store.dimension)

print("Vectors :", store.index.ntotal)

print("Metadata :", len(chunks))

print()

print("Vector Store Test Passed")