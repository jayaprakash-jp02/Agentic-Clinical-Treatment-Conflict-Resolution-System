from knowledge.vector_store import VectorStore

import numpy as np

vectors = np.random.rand(
    5,
    384,
).astype("float32")

store = VectorStore()

store.build_index(vectors)

store.save_index(
    "processed/test/index.faiss"
)

metadata = [
    {
        "chunk_id": 0,
        "guideline": "ADA",
        "text": "Example"
    }
]

store.save_metadata(
    metadata,
    "processed/test/metadata.pkl",
)

new_store = VectorStore()

new_store.load_index(
    "processed/test/index.faiss"
)

loaded_metadata = new_store.load_metadata(
    "processed/test/metadata.pkl"
)

print(
    "Vectors:",
    new_store.index.ntotal
)

print(
    loaded_metadata
)