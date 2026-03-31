import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model=os.getenv("GOOGLE_EMBEDDINGS_MODEL"),
        api_key=os.getenv("GOOGLE_API_KEY"),
        output_dimensionality=1536,
    )
