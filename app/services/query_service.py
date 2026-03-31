from app.rag.vector_store import get_vector_store
from app.rag.retriever import get_retriever
from app.rag.agent import create_agent



def process_query(query: str, session_id: str = "default"):
    vector_store = get_vector_store()
    retriever = get_retriever(vector_store)

    agent = create_agent(retriever)

    return agent(query, session_id=session_id)