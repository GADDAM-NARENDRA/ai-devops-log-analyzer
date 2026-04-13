from langchain.embeddings.openai import OpenAIEmbeddings
import faiss

embeddings = OpenAIEmbeddings()

def create_vector_store(texts):
    vectors = embeddings.embed_documents(texts)
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(vectors)
    return index, vectors

def search(index, query_vector, k=2):
    D, I = index.search(query_vector, k)
    return I