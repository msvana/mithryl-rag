# 1

So, the task is to implement a simple RAG that can answer a predefined set of questions.
I have to use an open-source LLM and I have access to a set of DOCX documents that
should be used as a knowledge base.

My thinking is that I should start with a simle MVP and then extend the functionality
if I have time.

To implement the MVP I need to:
1. Load the DOCX documents into a vector database
2. Set up an open-source LLM
3. Create a simple RAG that can answer questions
4. Create a UI for interating with the RAG

I decided to use LangChain with ChromaDB to implement the RAG + vector database.
These two part should be pretty straightforward.

One thing to explore is reading DOCX files in Python. I haven't done that before
but I am sure that there will be some library for that.

As for the LLM, I need an embedding model as well some generative model to actually
asnwer the questions. I'll find out which tools for running open-source LLMs are 
supported by LangChain and use one of them. Ideally, I'd prefer something 
like Llama.cpp. It's easy to set up and use, and it support quantized LLMs. For the
embeddings I can also use SentenceTransformers.

As for specific models, I think I'll start with the Gemma 3 family. I should be able
to run the 12B model on my GPU and the Gemma embedding model seems seems to also
be sized quite reasonably.

For starters, I'll implment the tool as a an CLI app.

Here are some things I can implement after the MVP is running:

- Some documents contain images. I am thinking about using an LLM to extract their contents
  and add the textual description as addition documents to tht DB.
- I can create a web UI. I think LangChain offers some web UI out of the box, but I am not sure.
  If not, I'll use Streamlit or Gradio
- I can use more "agentic" RAG instead of a base RAG. 
- I can write a benchmarking script to compare different LLMs and RAG implementations.

But now I'll start by researching local LLM tools supported by LangChain and libraries
for working with DOCX files.

# 2

So, LangChain supports Llama.cpp, both for embeddings and chat models. 
I'll go with that and if needed, I'll change it later.

As for reading DOCX files, I found that `python-docx` is pretty popular.

I could also use something like  `UnstructuredLoader` but as I understand it, 
this is a 3rd party service. I'll assume that we want to keep as much processing
as possible on the local machine.

As the next step, I'll write a simple script that loads DOCX files and

# 3

I disovered a library that might be more suitable for this project:
`markitdown`. It's a Markdown parser that can convert DOCX files to Markdown.

It's much simpler to use, because I don't have to iterate over the elements
of the document manually. It also offers a natural way to represent tables.

I just think I somehow need to deal with images later.

Anyways, I have a basic document loader, so I can now move
to the Vector Store part.

I've already started implementing a `load-documents` script. For now, it just 
creates langchain documents from the DOCX files. The next step is to store
the documents in the vector store.

