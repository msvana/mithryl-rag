# Mithryl RAG

A simple RAG agent for answering questions using a set of DOCX documents.

## Requirements

This tool requires a local [Ollama](https://ollama.com) for running open-source LLMs
locally and [uv](https://docs.astral.sh/uv/) to create a virtual environment and
install dependencies.

## Installation

1. Clone the repository

2. Create a virtual environment and install dependencies

```bash
uv sync
```

3. Pull the LLMs of your choice using Ollama (the LLM has to support tool calling) (see the Configuration section below)

```bash
ollama pull qwen3:8b ministral-3:3b embeddinggemma:latest
```

## Usage

1. Create a vector database for document search. Required documents are not present in the repository for confidentiality reasons.

```bash
uv run load-documents -d {path/to/documents}
```

2. Run the RAG agent and chat with it

```bash
uv run tui
```

3. To exit the chat, send a message `exit`

### Image analysis

ForThis tool can also use images embedded in the documents as sources of information.
Images get processed by a VLM and turned into text documents. To enable image analysis,
run the `load-documents` script with the `-i` flag.

If your documents EMF vector graphics, you need to have `inkscape` installed
so that we can convert them to a format the VLM can understand.

## Configuration

The configuration is stored in `src/mithryl_rag/config.py`. You can change the
following settings:

- `OLLAMA_BASE_URL`: The base URL of the Ollama server
- `EMBEDDING_LLM`: The embedding model to use (has to be supported by Ollama)
- `RAG_LLM`: The LLM to use for the RAG agent (has to be supported by Ollama and has to have tool support)
- `VISION_LLM`: The LLM to use for image analysis (has to be supported by Ollama and has to have vision support)
- `CHROMA_COLLECTION_NAME`: The name of the ChromaDB collection to use
- `CHROMA_DIRECTORY`: The directory where the ChromaDB collection is stored
- `RAG_LLM`: The LLM to use for the RAG agent

## Benchmarking

The repository contains a benchmarking script that can be used to compare different
LLMs and RAG implementations. It calculates the ROUGE1 score on 4 example questions.

To run the benchmark, run the following command:

```bash
uv run benchmark
```

## Testing

To run the tests, run the following command:

```bash
uv run pytest
```

For the tests to work properly, you need to have the relevant documents in the
`documents/` directory.
