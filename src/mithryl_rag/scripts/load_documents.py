import logging
from argparse import ArgumentParser
from pathlib import Path

from mithryl_rag.core.document_loader import DocumentLoader


def main():
    parser = create_arg_parser()
    args = parser.parse_args()

    logging.info(f"Loading documents from {args.dir}")
    document_loader = DocumentLoader()
    documents = document_loader.load_documents(args.dir)


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
