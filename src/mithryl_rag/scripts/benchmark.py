from langchain.messages import HumanMessage
from langgraph.graph.state import RunnableConfig
from rouge_score import rouge_scorer

from mithryl_rag.config import EXAMPLES_DIRECTORY
from mithryl_rag.core.rag import rag_agent


def main():
    with open(EXAMPLES_DIRECTORY / "questions.txt", "r") as f:
        questions = f.readlines()
        questions = [q.strip() for q in questions]

    answers = []

    for i in range(len(questions)):
        with open(EXAMPLES_DIRECTORY / f"answer_{i + 1}.txt", "r") as f:
            answers.append(f.read().strip())

    scorer = rouge_scorer.RougeScorer(["rouge1"], use_stemmer=True)

    for i in range(len(questions)):
        config: RunnableConfig = {"configurable": {"thread_id": str(i)}}
        expected = answers[i]
        response = rag_agent.invoke(
            {"messages": [HumanMessage(content=questions[i])]}, config=config
        )
        actual = response["messages"][-1].content
        score = scorer.score(expected, actual)
        print(f"Question {i + 1} score: {score}")


if __name__ == "__main__":
    main()
