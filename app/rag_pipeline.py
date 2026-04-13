from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from app.embeddings import create_vector_store, search
from app.data_loader import load_logs

logs = load_logs("data/sample_logs.txt")

embedding_model = OpenAIEmbeddings()
index, vectors = create_vector_store(logs)

llm = ChatOpenAI(temperature=0)

def analyze_query(query):
    query_vector = embedding_model.embed_query(query)
    query_vector = [query_vector]

    indices = search(index, query_vector)

    context = "\n".join([logs[i] for i in indices[0]])

    prompt = f"""
    You are a DevOps expert.

    Logs:
    {context}

    Question:
    {query}

    Provide:
    - Root cause
    - Suggested fix
    """

    response = llm.predict(prompt)
    return response