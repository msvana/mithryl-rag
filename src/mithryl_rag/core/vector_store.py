from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from mithryl_rag import config


def get_vector_store(
    embedding_model: str = config.EMBEDDING_LLM,
    collection_name: str = config.CHROMA_COLLECTION_NAME,
) -> Chroma:
    embeddings = OllamaEmbeddings(model=embedding_model)

    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=config.CHROMA_DIRECTORY.as_posix(),
    )

    return vector_store
