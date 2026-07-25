from pathlib import Path

import numpy as np

from knowledge.embeddings import EmbeddingGenerator
from knowledge.vector_store import VectorStore


class GuidelineRetriever:
    """
    Retrieves the most relevant guideline chunks
    using FAISS similarity search.
    """

    def __init__(self):

        self.embedding_generator = EmbeddingGenerator()

    def retrieve(
        self,
        query: str,
        guideline_directory: str,
        top_k: int = 5,
    ) -> list[dict]:

        guideline_path = Path(guideline_directory)

        index_path = guideline_path / "index.faiss"

        metadata_path = guideline_path / "metadata.pkl"

        store = VectorStore()

        index = store.load_index(str(index_path))

        metadata = store.load_metadata(str(metadata_path))

        query_vector = self.embedding_generator.create_embeddings(
            [query]
        ).astype(np.float32)

        distances, indices = index.search(
            query_vector,
            top_k,
        )

        results = []

        for distance, idx in zip(
            distances[0],
            indices[0],
        ):

            if idx == -1:
                continue

            chunk = metadata[idx]

            results.append(
                {
                    "score": float(distance),
                    "text": chunk["text"],
                    "guideline": chunk["guideline"],
                    "chunk_id": chunk["chunk_id"],
                }
            )

        return results