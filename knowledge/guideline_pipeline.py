from pathlib import Path

from knowledge.pdf_loader import load_pdf
from knowledge.text_cleaner import clean
from knowledge.chunker import split
from knowledge.embeddings import EmbeddingGenerator
from knowledge.vector_store import VectorStore


class GuidelinePipeline:

    def __init__(self):

        self.embedding_generator = EmbeddingGenerator()

        self.vector_store = VectorStore()

    def process_guideline(
        self,
        pdf_path: str,
        output_directory: str,
    ):
    
        pdf_file = Path(pdf_path)

        if not pdf_file.exists():
            raise FileNotFoundError(
                f"Guideline not found: {pdf_path}"
            )

        guideline_name = pdf_file.stem

        save_folder = Path(output_directory) / guideline_name

        index_path = save_folder / "index.faiss"

        metadata_path = save_folder / "metadata.pkl"

        if index_path.exists() and metadata_path.exists():

            print(f"{guideline_name} already processed.")

            return {
                "guideline": guideline_name,
                "chunks": None,
                "index_path": str(index_path),
                "metadata_path": str(metadata_path),
            }

        print(f"\nProcessing {guideline_name}")

        # -----------------------------
        # Load PDF
        # -----------------------------
        raw_text = load_pdf(pdf_path)

        # -----------------------------
        # Clean Text
        # -----------------------------
        cleaned_text = clean(raw_text)

        # -----------------------------
        # Chunk Text
        # -----------------------------
        chunks = split(cleaned_text)

        # -----------------------------
        # Create Metadata
        # -----------------------------
        metadata = []

        for index, chunk in enumerate(chunks):

            metadata.append(
            {
                "chunk_id": index,
                "guideline": guideline_name,
                "text": chunk,
            }
           )
        if not chunks:
          raise ValueError(
            f"No chunks generated from {guideline_name}"
        )

        # -----------------------------
        # Generate Embeddings
        # -----------------------------
        embeddings = self.embedding_generator.create_embeddings(
            chunks
        )

        # -----------------------------
        # Build FAISS
        # -----------------------------
        self.vector_store.build_index(
            embeddings
        )

        

        # -----------------------------
        # Save
        # -----------------------------
        self.vector_store.save_index(
            str(index_path)
        )

        self.vector_store.save_metadata(
            metadata,
            str(metadata_path),
        )

        print("Completed.")

        return {
            "guideline": guideline_name,
            "chunks": len(chunks),
            "index_path": str(index_path),
            "metadata_path": str(metadata_path),
        }