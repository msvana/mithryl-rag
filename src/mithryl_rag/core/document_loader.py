from pathlib import Path
from markitdown import MarkItDown
import re

from langchain_core.documents import Document

from mithryl_rag.core.image_to_text import ImageToText


class DocumentLoader:
    IMAGE_REGEX = re.compile(r"data:image/([^;]+);base64,([^)]+)")

    def __init__(self, image_to_text: ImageToText | None = None):
        self._md = MarkItDown(enable_plugins=False)
        self._image_to_text = image_to_text

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
        documents = []
        result = self._md.convert_local(path, keep_data_uris=True)
        result_text = result.markdown

        if extract_images:
            if not self._image_to_text:
                raise ValueError("Image extraction requires an image to text agent")

            for i, match in enumerate(self.IMAGE_REGEX.finditer(result_text)):
                image_match = match.group(0)
                result_text = result_text.replace(image_match, f"%IMAGE_{i}%")
                image_text = self._image_to_text.analyze_image(image_match)
                document = Document(
                    page_content=image_text,
                    metadata={"document_name": path.name, "image_id": i},
                )
                documents.append(document)

        document = Document(
            page_content=result_text, metadata={"document_name": path.name}
        )
        documents.append(document)

        return documents
