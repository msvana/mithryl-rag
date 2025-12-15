from langchain.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver

from mithryl_rag.core.vector_store import get_vector_store
from mithryl_rag.config import RAG_LLM

vector_store = get_vector_store()
llm = ChatOllama(model=RAG_LLM, temperature=0.0)


@tool(response_format="content_and_artifact")
def retrieve_documents(query: str):
    """Retrieve documents containing information relevatn to the query."""
    retrieved_docs = vector_store.similarity_search(query, k=3)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata['document_name']}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


system_prompt = """
You are a helpful assistant that can answer user questions using
documents you have access to.

You can retreive documents using the `retrieve_documents` tool. The query
used with this tool doesn't have to be the same as the question
from the user. You can modify it. 

If you don't know the answer to a question, just say that you don't know.
Do not guess.
"""

rag_agent = create_agent(
    llm,
    tools=[retrieve_documents],
    system_prompt=system_prompt,
    checkpointer=InMemorySaver(),
)
