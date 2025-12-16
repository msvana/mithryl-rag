import logging
from pathlib import Path


logging.basicConfig(level=logging.INFO)

BASE_PATH = Path(__file__).parent.parent.parent

DOCUMENTS_DIRECTORY = BASE_PATH / "documents"
EXAMPLES_DIRECTORY = BASE_PATH / "examples"

CHROMA_COLLECTION_NAME = "mithryl-rag"
CHROMA_DIRECTORY = BASE_PATH / "vectors"
CHUNK_SIZE = 4000
CHUNK_OVERLAP = 250

EMBEDDING_LLM = "embeddinggemma:latest"
RAG_LLM = "ministral-3:8b"
VISION_LLM = "ministral-3:3b"
