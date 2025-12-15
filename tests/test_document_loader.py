from pathlib import Path

import pytest

from mithryl_rag.core.document_loader import DocumentLoader
from mithryl_rag import config


@pytest.fixture
def document_loader():
    return DocumentLoader()


@pytest.fixture
def single_document_path():
    return (
        config.DOCUMENTS_DIRECTORY
        / "Copy of F22-855-4.0 - 01 - Organizational Context Procedure.docx"
    )


def test_load_documents(document_loader: DocumentLoader):
    documents = document_loader.load_documents(config.DOCUMENTS_DIRECTORY)
    assert len(documents) == 23


def test_single_document(document_loader: DocumentLoader, single_document_path: Path):
    document = document_loader.load_single_document(single_document_path)
    assert document.metadata["document_name"] == single_document_path.name
    assert len(document.page_content) > 0

    # Here are some pieces of text that should be in the document
    assert "Organizational Context Procedure" in document.page_content
    assert "Quality Controller" in document.page_content
    assert (
        "Formtech Composites maintains and controls documented information"
        in document.page_content
    )
    assert "F22-855-7.5 – Control of Documented Information" in document.page_content
