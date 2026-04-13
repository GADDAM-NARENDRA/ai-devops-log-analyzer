import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

    # App settings
    APP_NAME: str = "AI DevOps Log Analyzer"
    VERSION: str = "1.0.0"

    # Vector DB settings
    VECTOR_DB_TYPE: str = "faiss"

    # RAG settings
    TOP_K_RESULTS: int = 2
    TEMPERATURE: float = 0.0

    # File paths
    LOG_FILE_PATH: str = "data/sample_logs.txt"

# Create a global settings object
settings = Settings()