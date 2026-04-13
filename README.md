# AI DevOps Log Analyzer (RAG)

This project uses Retrieval-Augmented Generation (RAG) to analyze logs and provide root cause analysis and solutions.

## Features
- Log ingestion
- Vector search using FAISS
- AI-based insights using OpenAI
- FastAPI backend

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload