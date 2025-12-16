# Mithryl RAG

A simple RAG agent for answering questions using a set of DOCX documents.

## Requirements

This tool requires a local [Ollama](https://ollama.com) for running open-source LLMs
locally and [uv](https://docs.astral.sh/uv/) to create a virtual environment and
install dependencies.

## Installation and usage

1. Clone the repository

2. Create a virtual environment and install dependencies

```bash
uv sync
```

3. Pull the LLMs of your choice using Ollama (the LLM has to support tool calling) (see the Configuration section below)

```bash
ollama pull qwen3:8b ministral-3:3b embeddinggemma:latest
```

4. Create a vector database for document search

```bash
uv run load-documents -d {path/to/documents}
```

5. Run the RAG agent and chat with it

```bash
uv run tui
```

### Image analysis

This tool can also use images embedded in the documents as sources of information.
Images get processed by a VLM and turned into text documents. To enable image analysis,
run the `load-documents` script with the `-i` flag.

If your documents EMF vector graphics, you need to have `inkscape` installed
so that we can convert them to a format the VLM can understand.

## Configuration

The configuration is stored in `src/mithryl_rag/config.py`. You can change the
following settings:

- `EMBEDDING_LLM`: The embedding model to use (has to be supported by Ollama)
- `RAG_LLM`: The LLM to use for the RAG agent (has to be supported by Ollama)
- `VISION_LLM`: The LLM to use for image analysis (has to be supported by Ollama)
- `CHROMA_COLLECTION_NAME`: The name of the ChromaDB collection to use
- `CHROMA_DIRECTORY`: The directory where the ChromaDB collection is stored
- `RAG_LLM`: The LLM to use for the RAG agent
