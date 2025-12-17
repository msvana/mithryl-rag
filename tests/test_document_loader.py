from pathlib import Path

import pytest

from mithryl_rag import config
from mithryl_rag.core.document_loader import DocumentLoader
from mithryl_rag.core.image_to_text import ImageToText


@pytest.fixture
def document_loader():
    image_to_text = ImageToText()
    return DocumentLoader(image_to_text)


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
    document = document_loader.load_single_document(single_document_path)[0]
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

def test_single_document_with_images(
    document_loader: DocumentLoader, single_document_path: Path
):
    documents = document_loader.load_single_document(single_document_path, True)
    assert len(documents) == 5

    image_0 = documents[0]
    assert image_0.metadata["image_id"] == 0 
    assert "formtech" in image_0.page_content.lower()

    image_qms = documents[-2]
    assert "Quality Manual" in image_qms.page_content
    assert "Quality Management System Procedures" in image_qms.page_content
    assert "Work Instructions, Records, Forms and Documents" in image_qms.page_content
