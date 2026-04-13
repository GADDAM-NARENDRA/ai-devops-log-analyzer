from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from app.embeddings import create_vector_store, search
from app.data_loader import load_logs
from app.config import settings

# Load logs
logs = load_logs(settings.LOG_FILE_PATH)

# Embeddings
embedding_model = OpenAIEmbeddings(
    openai_api_key=settings.OPENAI_API_KEY
)

# Vector DB
index, vectors = create_vector_store(logs)

# LLM
llm = ChatOpenAI(
    temperature=settings.TEMPERATURE,
    openai_api_key=settings.OPENAI_API_KEY
)

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