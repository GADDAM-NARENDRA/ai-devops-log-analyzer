from fastapi import FastAPI
from pydantic import BaseModel
from app.rag_pipeline import analyze_query

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ✅ FIRST create app
app = FastAPI()

# ✅ THEN mount static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Request model
class QueryRequest(BaseModel):
    query: str

# UI route
@app.get("/")
def home():
    return FileResponse("app/static/index.html")

# API route
@app.post("/analyze")
def analyze(request: QueryRequest):
    result = analyze_query(request.query)
    return {"response": result}