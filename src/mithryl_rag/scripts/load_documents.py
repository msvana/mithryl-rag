import logging
from argparse import ArgumentParser
from pathlib import Path

from mithryl_rag.core.document_loader import DocumentLoader
from mithryl_rag.core.image_to_text import ImageToText
from mithryl_rag.core.vector_store import VectorStore


def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    logging.info(f"Loading documents from {args.dir}")
    image_to_text = ImageToText() if args.extract_images else None
    document_loader = DocumentLoader(image_to_text)
    documents = document_loader.load_documents(args.dir, args.extract_images)
    logging.info(f"Loaded {len(documents)} documents")


    logging.info("Creating vector store")
    vector_store = VectorStore()

    logging.info("Adding documents to vector store")
    vector_store.reset_collection()
    vector_store.add_documents(documents)
    logging.info("Documents added to vector store")


def create_arg_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-d",
        "--dir",
        type=Path,
        required=True,
        help="Path to the directory containing the DOCX files",
    )

    parser.add_argument(
        "-i",
        "--extract-images",
        action="store_true",
        help="Extract images from the DOCX files and add them to the vector store",
    )

    return parser
