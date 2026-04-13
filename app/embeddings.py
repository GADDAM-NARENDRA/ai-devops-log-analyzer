from langchain_openai import OpenAIEmbeddings
import faiss
from app.config import settings

embeddings = OpenAIEmbeddings(
    openai_api_key=settings.OPENAI_API_KEY
)

def create_vector_store(texts):
    vectors = embeddings.embed_documents(texts)
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(vectors)
    return index, vectors

def search(index, query_vector, k=2):
    D, I = index.search(query_vector, k)
    return I