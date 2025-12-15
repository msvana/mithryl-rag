import logging
from argparse import ArgumentParser
from pathlib import Path

from mithryl_rag.core.document_loader import DocumentLoader
from mithryl_rag.core.vector_store import get_vector_store


def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    logging.info(f"Loading documents from {args.dir}")
    document_loader = DocumentLoader()
    documents = document_loader.load_documents(args.dir)
    logging.info(f"Loaded {len(documents)} documents")

    logging.info("Creating vector store")
    vector_store = get_vector_store()
    
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

    return parser
