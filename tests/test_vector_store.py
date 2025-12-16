import pytest
from langchain_chroma.vectorstores import Chroma

from mithryl_rag import config
from mithryl_rag.core.document_loader import DocumentLoader
from mithryl_rag.core.vector_store import VectorStore


@pytest.fixture
def documents():
    document_loader = DocumentLoader()
    return document_loader.load_documents(config.DOCUMENTS_DIRECTORY)[:5]


@pytest.fixture
def vector_store():
    return VectorStore(collection_name="test")


def test_basic_retrieval(vector_store: Chroma, documents):
    vector_store.reset_collection()
    vector_store.add_documents(documents, False)

    assert len(vector_store.get()["documents"]) == len(documents)

    # Sanity check:
    for document in documents:
        query = document.metadata["document_name"]
        results = vector_store.similarity_search(query, k=3)
        assert len(results) == 3


def test_adding_with_splitting(vector_store: Chroma, documents):
    vector_store.reset_collection()
    vector_store.add_documents(documents, True)

    assert len(vector_store.get()["documents"]) > len(documents)
