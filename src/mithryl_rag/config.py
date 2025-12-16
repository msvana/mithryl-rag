import logging
from pathlib import Path


logging.basicConfig(level=logging.INFO)

BASE_PATH = Path(__file__).parent.parent.parent

DOCUMENTS_DIRECTORY = BASE_PATH / "documents"

CHROMA_COLLECTION_NAME = "mithryl-rag"
CHROMA_DIRECTORY = BASE_PATH / "vectors"

EMBEDDING_LLM = "embeddinggemma:latest"
RAG_LLM = "qwen3:8b"
VISION_LLM = "ministral-3:3b"
