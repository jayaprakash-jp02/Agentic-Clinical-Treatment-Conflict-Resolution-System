from typing import List


def split(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(text), step):

        end = min(start + chunk_size, len(text))

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

    return chunks