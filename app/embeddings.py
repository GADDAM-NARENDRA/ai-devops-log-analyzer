import numpy as np
from langchain_openai import OpenAIEmbeddings
import faiss
from app.config import settings

embeddings = OpenAIEmbeddings(
    openai_api_key=settings.OPENAI_API_KEY
)

def create_vector_store(texts):
    vectors = embeddings.embed_documents(texts)

    # 🔥 FIX: convert list → numpy array
    vectors = np.array(vectors).astype("float32")

    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    return index, vectors


def search(index, query_vector, k=2):
    query_vector = np.array(query_vector).astype("float32")
    D, I = index.search(query_vector, k)
    return I
