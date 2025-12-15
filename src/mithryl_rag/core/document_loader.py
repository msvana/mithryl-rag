from pathlib import Path
from markitdown import MarkItDown
import re

from langchain_core.documents import Document


class DocumentLoader:
    IMAGE_REGEX = re.compile(r"data:image/([^;]+);base64,([^)]+)")

    def __init__(self):
        self._md = MarkItDown(enable_plugins=False)

    def load_documents(
        self, path: Path, extract_images: bool = False
    ) -> list[Document]:
        documents = []

        for file in path.iterdir():
            if file.suffix != ".docx":
                continue
            document = self.load_single_document(file, extract_images)
            documents.extend(document)

        return documents

    def load_single_document(
        self, path: Path, extract_images: bool = False
    ) -> list[Document]:
        result = self._md.convert_local(path, keep_data_uris=True)
        result_text = result.markdown

        if extract_images:
            for match in self.IMAGE_REGEX.finditer(result_text):
                image_match = match.group(0)
                result_text = result_text.replace(image_match, "%IMAGE%")

        document = Document(
            page_content=result_text, metadata={"document_name": path.name}
        )

        return [document]
