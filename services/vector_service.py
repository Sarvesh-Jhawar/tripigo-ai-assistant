"""
Vector Service.
Handles the generation of dense vector embeddings from raw text.
It uses the SentenceTransformer library with a pre-trained HuggingFace model.
"""
from sentence_transformers import SentenceTransformer

# Initialize the embedding model.
# BAAI/bge-small-en-v1.5 is chosen because it is highly efficient, fast, 
# and provides excellent semantic representation for Retrieval tasks.
model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def embed_text(text: str) -> list[float]:
    """
    Converts a single string of text into a list of floating-point numbers (vector).
    Used primarily for converting the user's chat question into a searchable vector.
    """
    return model.encode(text).tolist()

def embed_documents(documents: list[str]) -> list[list[float]]:
    """
    Converts a list of text strings into a list of vectors.
    Used primarily during the /ingest process to embed all our travel data at once.
    """
    return model.encode(documents).tolist()
