from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from mithryl_rag import config


class VectorStore:
    CHUNK_SIZE = config.CHUNK_SIZE
    CHUNK_OVERLAP = config.CHUNK_OVERLAP

    def __init__(
        self,
        embedding_model: str = config.EMBEDDING_LLM,
        collection_name: str = config.CHROMA_COLLECTION_NAME,
    ):
        self._embeddings = OllamaEmbeddings(model=embedding_model)
        self._vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self._embeddings,
            persist_directory=config.CHROMA_DIRECTORY.as_posix(),
        )

    def reset_collection(self):
        self._vector_store.reset_collection()

    def add_documents(self, documents: list[Document], split: bool = True):
        if split:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.CHUNK_SIZE,
                chunk_overlap=self.CHUNK_OVERLAP,
                add_start_index=True,
            )
            documents = text_splitter.split_documents(documents)
        self._vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 5) -> list:
        return self._vector_store.similarity_search(query, k=k)

    def get(self) -> dict:
        return self._vector_store.get()
