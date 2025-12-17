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

I just think I somehow need to deal with images later they might

Anyways, I have a basic document loader, so I can now move
to the Vector Store part.

I've already started implementing a `load-documents` script. For now, it just 
creates langchain documents from the DOCX files. The next step is to store
the documents in the vector store.

# 4

I implemented a vector store using ChromaDB. Chose it mainly for its ease of use.
I ended up using HuggingFace embeddings wrapper provided by LangChain
to interact with the embedding model. I originally planned to use Llama.cpp
but I had some issues loading the model. I didn't want to spend time on that
so I went with HuggingFace. Might get back to it later.

# 5

I've implemented a basic RAG agent as a CLI tool. I changed a few things though.
First, I I am using gwen3:8b instead of Gemma. As it turns out, the 12B variant
of Gemma 3 doesn't support tool calling. I want to make the RAG a bit agentic.
Document search is provided as a tool, and the agent can decide when and how to
use it.

I chose the 8B version because, I can run it locally.

Also, Instead of Llama.cpp I decided to use Ollama. The reason is speed. I
already have Ollama up and running on my machine. I would have to compile Llama.cpp
with CUDA support, which would take unnnecessary time. Given that this is a relatively
small demo and I have limited time, I decided to go with Ollama.

However, if I were to turn this into a real product, I'd revisit this decision.
AFAIK, Ollama is not great at handling multiple requests in parallel.

Given that the RAG tool seems to provide reasonable answers,
I'll now spend some time writing a README. Then, just make things a bit more
interesting, I'll also look into extracting images.

# 6

I've implemented turning images into text and adding them to the vector store.
I used the recently released `ministral-3:3b model`. I originally started
with QWEN, but it regularly got stuck. Ministral seems to work fine.

The RAG tool was able to answer a test question about an image and I am
quite happy about that.

I still need to write some tests for this part.

I am replacing the images in the extracted markdown with placeholders
containing the image ID. I could introduce a tool that would get the
contents of a specific image.

I've also started using Ollama for embeddings. This solution uses less
memory and reduces the number of dependecies - I don't need to install
`sentence-transformers` and `PyTorch` anymore.and

As the next step I'll do some refactoring and think about introducing
a basic benchmarking script. I am thinking about taking the
example questions, answering them manually and then using a metric
like BLEU to compare the answers.

Using this benchmark, I could try different models like Ministral, some
smaller Llama, or somethinng like that.

# 7

After some basic refactoring, I implemented a benchmarking script.
As a toy example, I've decded using the ROUGE1 score to evaluate the agent. 

I've used 3 questions from the assignment for which I could extract answers 
from the documents on my own. I also added a question whose answer is contained in an image.

I've compared two models - Ministral and Qwen3 in their 8B variants.
As it turns out, Ministral is better on average.

Tomorrow, I'll just make sure that everything works and merge the branch.

# 8

I did some cleanup and small enhancements.

- I've modified the prompt so that the agent doesn't answer if the answer to the question is not in the documents.
- The agent should now also better handle multiple questions in one chat session.
- I've extended the tests to better cover image analysis.
- I've updated the README to reflect the changes, especially the presence of the `benchmark` script.

# 9 

Let me end with some thoughts on possible improvements. In no particular order:

- I could have created a web UI for the RAG agent.
- I could have implemented a tool for loading the text representation of a specific image.
  The documents contain image IDs. The agent could request them to better connect the information
  in the documents and in images.
- In a real-world setting, I would probably use a different LLM runner instead of Ollama.
  Ollama is quick to set up and easy to use, but it's not great at handling multiple requests
  in parallel. It's also limited to a specific quatntization type. Something like Llama.cpp or vLLM
  would be better suited for real-world use.
- I could also experiment with larger LLMs. As I was working on this project, I added a hidden
  requirement that everything has to run on my local machine with limited VRAM.
- I could have added a list of sources used to anser the questions to the output.
