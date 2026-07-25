"""
vector_store.py

Purpose
-------
Build a FAISS vector index from embeddings.

Responsibilities
----------------
- Create FAISS index
- Store embedding vectors
- Return the FAISS index

This module intentionally DOES NOT:
- Generate embeddings
- Retrieve documents
"""

import pickle
from pathlib import Path

import faiss
import numpy as np


class VectorStore:
    """
    Builds and manages a FAISS index.
    """

    def __init__(self):
        
        self.index = None
        self.dimension = None

    def build_index(self, vectors: np.ndarray) -> faiss.Index:
        """
        Build a FAISS index from embedding vectors.

        Parameters
        ----------
        vectors : np.ndarray

        Returns
        -------
        faiss.Index
        """

        if vectors.size == 0:
            raise ValueError("Embedding array is empty.")

        # FAISS requires float32
        vectors = vectors.astype("float32")

        self.dimension = vectors.shape[1]

        self.index = faiss.IndexFlatL2(self.dimension)

        self.index.add(vectors)

        return self.index

    def save_index(
        self,
        save_path: str,
    ) -> None:
        """
        Save the FAISS index to disk.
        """

        if self.index is None:
            raise ValueError(
                "No FAISS index available to save."
            )

        save_file = Path(save_path)

        save_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        faiss.write_index(
            self.index,
            str(save_file),
        )


    def load_index(
        self,
        save_path: str,
    ):
        """
        Load an existing FAISS index.
        """

        save_file = Path(save_path)

        if not save_file.exists():
            raise FileNotFoundError(
                f"Index not found: {save_path}"
            )

        self.index = faiss.read_index(
            str(save_file)
        )

        return self.index


    def save_metadata(
        self,
        metadata: list[str],
        save_path: str,
    ) -> None:
        """
        Save chunk metadata.
        """

        save_file = Path(save_path)

        save_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            save_file,
            "wb",
        ) as file:

            pickle.dump(
                metadata,
                file,
            )


    def load_metadata(
    self,
    save_path: str,
    ) -> list[str]:
        """
        Load chunk metadata.
        """

        save_file = Path(save_path)

        if not save_file.exists():
            raise FileNotFoundError(
                f"Metadata not found: {save_path}"
            )

        with open(
            save_file,
            "rb",
        ) as file:

            return pickle.load(file)