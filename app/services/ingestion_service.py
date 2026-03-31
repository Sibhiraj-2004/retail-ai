from app.utils.loaders import load_document
from app.utils.chunking import split_documents
from app.rag.vector_store import get_vector_store


def ingest(file_path: str):
    docs = load_document(file_path)
    print("Number of pages loaded:", len(docs))
    chunks = split_documents(docs)

    vector_store = get_vector_store()
    vector_store.add_documents(chunks)

    return {"status": "success", "chunks": len(chunks)}
