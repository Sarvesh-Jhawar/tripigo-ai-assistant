"""
Vector Service.
Handles the generation of dense vector embeddings from raw text.
It uses the SentenceTransformer library with a pre-trained HuggingFace model.
"""
import os
import torch

# Restrict thread count and parallelism to prevent RAM spikes on 512MB containers
os.environ["TOKENIZERS_PARALLELISM"] = "false"
torch.set_num_threads(1)

from sentence_transformers import SentenceTransformer

# Initialize the lightweight embedding model.
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
