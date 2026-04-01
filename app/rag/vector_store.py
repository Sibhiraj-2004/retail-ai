from langchain_community.vectorstores import PGVector
from app.core.config import settings
from app.rag.embeddings import get_embeddings


def get_vector_store():
    return PGVector(
        connection_string=settings.DATABASE_URL,
        embedding_function=get_embeddings(),
        collection_name="financial_docs",
    )
