from langchain_google_genai import ChatGoogleGenerativeAI
from app.rag.memory import get_memory

from app.rag.tools.hybrid_search import hybrid_search


def create_agent(retriever):
    llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", temperature=0.2)

    memory = get_memory()

    def run(query: str):
        """
        docs = retriever.invoke(query)
        context = "\n".join([doc.page_content for doc in docs])
        """

        docs = hybrid_search(query)

        context = "\n".join(docs)

        chat_history = memory.load_memory()

        history_text = "\n".join(
            [f"User: {h['user']}\nAssistant: {h['assistant']}" for h in chat_history]
        )

        with open("./prompt.txt", "r") as file:
            prompt_template = file.read()

        prompt = prompt_template.format(
            history_text=history_text, context=context, query=query
        )

        # print(prompt)

        response = llm.invoke(prompt)

        if isinstance(response.content, list):
            output = " ".join([item.get("text", "") for item in response.content])
        else:
            output = response.content

        memory.save(query, output)

        return output

    return run
