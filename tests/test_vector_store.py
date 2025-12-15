import pytest
from langchain_chroma.vectorstores import Chroma

from mithryl_rag import config
from mithryl_rag.core.document_loader import DocumentLoader
from mithryl_rag.core.vector_store import get_vector_store


@pytest.fixture
def documents():
    document_loader = DocumentLoader()
    return document_loader.load_documents(config.DOCUMENTS_DIRECTORY)[:5]


@pytest.fixture
def vector_store():
    return get_vector_store(collection_name="test")


def test_basic_retrieval(vector_store: Chroma, documents):
    vector_store.reset_collection()
    vector_store.add_documents(documents)

    assert len(vector_store.get()["documents"]) == len(documents)

    # Sanity check:
    # querying document name should return the document with the same name
    for document in documents:
        query = document.metadata["document_name"]
        results = vector_store.similarity_search(query, k=3)
        assert len(results) == 3
        assert query in results[0].metadata["document_name"]
