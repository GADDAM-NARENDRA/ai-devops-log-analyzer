from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from app.embeddings import create_vector_store, search
from app.data_loader import load_logs
from app.config import settings
from pathlib import Path
import os

# Load all logs from data folder (will be reloaded dynamically)
def get_logs():
    """Dynamically load logs to always get the latest"""
    return load_logs()

# Load logs grouped by source file
def load_logs_by_file():
    """Load logs grouped by source file"""
    data_dir = "data"
    logs_by_file = {}
    
    if not os.path.exists(data_dir):
        return logs_by_file
    
    for file_path in Path(data_dir).glob("*"):
        if file_path.is_file() and file_path.suffix in ['.log', '.txt']:
            try:
                with open(file_path, "r") as f:
                    file_logs = f.readlines()
                logs_by_file[file_path.name] = [log.strip() for log in file_logs if log.strip()]
            except Exception as e:
                logs_by_file[file_path.name] = [f"Error reading file: {str(e)}"]
    
    return logs_by_file

logs_by_file = load_logs_by_file()

# ✅ DEFINE embedding_model HERE (GLOBAL)
embedding_model = OpenAIEmbeddings(
    openai_api_key=settings.OPENAI_API_KEY
)

# Vector DB
try:
    index, vectors = create_vector_store(get_logs())
except Exception as e:
    index, vectors = None, None
    print(f"Warning: Could not create vector store: {e}")

# LLM
llm = ChatOpenAI(
    temperature=settings.TEMPERATURE,
    openai_api_key=settings.OPENAI_API_KEY
)

def analyze_query(query):
    if not index or not vectors:
        return "Error: No logs loaded. Please run: python -m app.fetch_logs"
    
    try:
        # Get fresh logs each time
        current_logs = get_logs()
        query_vector = embedding_model.embed_query(query)
        query_vector = [query_vector]

        indices = search(index, query_vector)
        context = "\n".join([current_logs[i] for i in indices[0] if i < len(current_logs)])

        prompt = f"""You are a DevOps expert. Analyze the following logs and provide:
1. Root cause analysis
2. Severity level (Critical/High/Medium/Low)
3. Suggested fixes
4. Prevention tips

Logs:
{context}

Question:
{query}

Format your response clearly with sections."""

        response = llm.invoke(prompt)
        return response.content
    
    except Exception as e:
        return f"Error during analysis: {str(e)}"

def analyze_logs_by_file(query=None):
    """
    Analyze logs file by file and return separate reports
    If query is None, generates a general analysis for each file
    Fresh read from disk each time to get latest logs
    """
    reports = {}
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        return {"error": "Data folder not found"}
    
    # Read files fresh to get latest logs
    for file_path in Path(data_dir).glob("*"):
        if file_path.is_file() and file_path.suffix in ['.log', '.txt']:
            try:
                with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    file_logs = [log.strip() for log in content.split('\n') if log.strip()]
                
                if not file_logs:
                    reports[file_path.name] = "No logs found in this file"
                    continue
                
                context = "\n".join(file_logs[:100])  # First 100 lines per file
                
                if query:
                    prompt = f"""You are a DevOps expert. Given this {file_path.name} file content and the query, provide:
1. Relevant findings
2. Severity level (Critical/High/Medium/Low)
3. Suggested actions

{file_path.name} content:
{context}

Query:
{query}

Keep response concise and actionable."""
                else:
                    # General analysis if no specific query
                    prompt = f"""You are a DevOps expert. Analyze this {file_path.name} file and provide:
1. Overall health status
2. Issues detected (if any)
3. Error/Warning counts
4. Recommended actions
5. Key alerts

{file_path.name} content (first 100 lines):
{context}

Provide a concise but comprehensive analysis."""
                
                response = llm.invoke(prompt)
                reports[file_path.name] = response.content
            
            except Exception as e:
                reports[file_path.name] = f"Error analyzing {file_path.name}: {str(e)}"
    
    return reports

def get_logs_summary():
    """Get summary statistics for each log file - fresh read each time"""
    summary = {}
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        return summary
    
    # Read files fresh to get latest stats
    for file_path in Path(data_dir).glob("*"):
        if file_path.is_file() and file_path.suffix in ['.log', '.txt']:
            try:
                with open(file_path, "r", encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    file_logs = [log.strip() for log in content.split('\n') if log.strip()]
                
                total_lines = len(file_logs)
                error_count = sum(1 for log in file_logs if 'error' in log.lower() or 'failed' in log.lower() or 'exception' in log.lower())
                warning_count = sum(1 for log in file_logs if 'warning' in log.lower() or 'warn' in log.lower())
                info_count = sum(1 for log in file_logs if 'info' in log.lower())
                
                summary[file_path.name] = {
                    "total_lines": total_lines,
                    "error_count": error_count,
                    "warning_count": warning_count,
                    "info_count": info_count,
                    "critical_ratio": round((error_count / total_lines * 100) if total_lines > 0 else 0, 2),
                    "file_size": f"{file_path.stat().st_size / 1024:.2f} KB"
                }
            except Exception as e:
                summary[file_path.name] = {
                    "total_lines": 0,
                    "error_count": 0,
                    "warning_count": 0,
                    "info_count": 0,
                    "critical_ratio": 0,
                    "file_size": "0 KB",
                    "error": str(e)
                }
    
    return summary
