from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.schemas.response import QueryResponse
from app.rag.memory import get_session_history
from app.rag.vector_store import get_vector_store
from sqlalchemy import text
from app.core.database import engine
import os
import time


def create_agent(retriever):

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite-preview",
        temperature=0.2,
    )

    def vector_search(query, k=5):
        vector_store = get_vector_store()
        retriever = vector_store.as_retriever(search_kwargs={"k": k})
        def safe_invoke(retriever,query):
            for i in range(3):
                try:
                    docs = retriever.invoke(query)
                    return docs
                except Exception as e:
                    if "429" in str(e):
                        time.sleep(2**i)
                    else:
                        raise e
        docs = safe_invoke(query=query,retriever=retriever)
        return [doc.page_content for doc in docs]

    def fts_search(query, k=5):
        sql = text("""
            SELECT document
            FROM langchain_pg_embedding
            WHERE document ILIKE :query
            LIMIT :k
        """)

        with engine.connect() as conn:
            result = conn.execute(sql, {"query": f"%{query}%", "k": k})
            rows = result.fetchall()

        return [row[0] for row in rows]

    def hybrid_search(query, k=5):
        vector_docs = vector_search(query, k)
        fts_docs = fts_search(query, k)

        combined = list(set(vector_docs + fts_docs))
        return combined[:k]

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an intelligent Financial Advisory Assistant designed to help users make informed financial decisions.

Your responsibilities:
- Understand user queries related to finance, investments, banking, and risk.
- Analyze provided document context carefully.
- Use previous conversation history to maintain continuity.
- Provide accurate, concise, and well-structured responses.

Guidelines:
1. Always prioritize information from the provided CONTEXT.
2. If context is insufficient or missing, clearly state that the information is not available instead of guessing.
3. Use CHAT HISTORY to understand follow-up questions and user intent.
4. Maintain a professional, neutral, and advisory tone at all times.
5. Avoid hallucination — do not invent financial facts, figures, or guarantees.
6. Explain concepts in simple, beginner-friendly language.
7. When relevant, explicitly mention:
   - Risk level (Low / Medium / High)
   - Suitability (e.g., short-term, long-term investors)
8. Keep responses concise but informative.
9. Avoid repeating unnecessary or previously stated information.
10. When multiple financial concepts are involved, structure the answer clearly using bullet points or numbered sections.

Search & Retrieval Awareness:
11. Understand the purpose of different search tools used to retrieve financial document context:
   - FTS (Full-Text Search):
     - Used when users ask keyword-based or exact-term questions.
     - Suitable for regulatory text, policy documents, disclosures, and contracts.
     - Best when users reference specific phrases or terminology.
   - Vector Search:
     - Used for semantic or meaning-based queries.
     - Helpful when users ask conceptual questions or vague queries (e.g., “safe investment options”).
     - Captures intent even if exact keywords do not match.
   - Hybrid Search:
     - Used when both accuracy and semantic understanding are important.
     - Ideal for complex financial advisory questions combining facts and intent.
     - Ensures higher relevance and completeness of retrieved context.

12. Always rely on retrieved context from these search tools to ground responses.
13. If search results conflict or are incomplete, acknowledge uncertainty and explain limitations clearly.
14. Do not assume user intent beyond what is stated or implied in the query and context.

""",
            ),
            ("human", "{input}"),
        ]
    )

    def build_input(input_dict):
        query = input_dict["input"]

        docs = hybrid_search(query)
        context = "\n".join(docs)

        return {
            "input": f"""
Context:
{context}

Question:
{query}
"""
        }

    structured_llm = llm.with_structured_output(QueryResponse)
    chain = build_input | prompt | structured_llm

    chain_with_memory = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    def run(query: str, session_id: str = "default"):

        def safe_invoke(llm, messages, config):
            for i in range(3):
                try:
                    response = chain_with_memory.invoke(messages, config=config)
                    return response
                except Exception as e:
                    if "429" in str(e):
                        time.sleep(2**i)
                    else:
                        raise e

        response = safe_invoke(
            messages={"input": query},
            config={"configurable": {"session_id": session_id}},
        )

        if isinstance(response.content, list):
            return " ".join([item.get("text", "") for item in response.content])

        return response.content

    return run
