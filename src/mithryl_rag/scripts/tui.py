from langchain_core.messages import HumanMessage
from langgraph.graph.state import RunnableConfig

from mithryl_rag.core.rag import rag_agent


def main():
    config: RunnableConfig = {"configurable": {"thread_id": "1"}}

    while True:
        user_input = input("Enter a question: ")

        if user_input.lower().strip() == "exit":
            print("Exiting...")
            break

        result = rag_agent.invoke(
            {"messages": [HumanMessage(user_input)]},
            config=config,
        )

        print(result["messages"][-1].content)
