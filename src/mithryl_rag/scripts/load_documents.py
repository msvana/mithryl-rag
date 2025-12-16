import logging
from argparse import ArgumentParser
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from mithryl_rag.core.document_loader import DocumentLoader
from mithryl_rag.core.image_to_text import ImageToText
from mithryl_rag.core.vector_store import get_vector_store


def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    logging.info(f"Loading documents from {args.dir}")
    image_to_text = ImageToText() if args.extract_images else None
    document_loader = DocumentLoader(image_to_text)
    documents = document_loader.load_documents(args.dir, args.extract_images)
    logging.info(f"Loaded {len(documents)} documents")

    logging.info("Splitting documents into chunks")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,  
        chunk_overlap=250,  
        add_start_index=True, 
    )
    splits = text_splitter.split_documents(documents)

    logging.info("Creating vector store")
    vector_store = get_vector_store()

    logging.info("Adding documents to vector store")
    vector_store.reset_collection()
    vector_store.add_documents(splits)
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
