from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_pipeline import analyze_query

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/analyze")
def analyze(request: QueryRequest):
    result = analyze_query(request.query)
    return {"response": result}