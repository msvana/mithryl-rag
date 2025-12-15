from pathlib import Path
from markitdown import MarkItDown

from langchain_core.documents import Document


class DocumentLoader:
    def __init__(self):
        self._md = MarkItDown(enable_plugins=False)

    def load_documents(self, path: Path) -> list[Document]:
        documents = []

        for file in path.iterdir():
            if file.suffix != ".docx":
                continue
            document = self.load_single_document(file)
            documents.append(document)

        return documents

    def load_single_document(self, path: Path) -> Document:
        result = self._md.convert_local(path)
        return Document(page_content=result.markdown, metadata={"document_name": path.name})
