"""
embeddings.py

Purpose
-------
Generate sentence embeddings for text chunks.

Responsibilities
----------------
- Load SentenceTransformer model
- Convert chunks into embeddings
- Return embedding vectors

This module intentionally DOES NOT:
- Build FAISS index
- Retrieve documents
"""

from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """
    Loads the embedding model only once.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):

        self.model = SentenceTransformer(model_name)

    def create_embeddings(
        self,
        chunks: List[str]
    ) -> np.ndarray:
        """
        Convert text chunks into embeddings.

        Parameters
        ----------
        chunks : List[str]

        Returns
        -------
        np.ndarray
        """

        if not chunks:
            return np.array([])

        embeddings = self.model.encode(
            chunks,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        return embeddings