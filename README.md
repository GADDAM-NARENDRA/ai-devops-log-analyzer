# 🚀 AI DevOps Log Analyzer (RAG-Based System)

An AI-powered DevOps assistant that analyzes logs and provides **root cause analysis** and **actionable fixes** using **Retrieval-Augmented Generation (RAG)**.

---

## 🔥 Features

* 🔍 Intelligent log analysis using AI
* 🧠 Root cause detection from historical logs
* 💡 Suggested fixes for incidents
* ⚡ FastAPI-based REST API
* 📦 Dockerized for easy deployment
* 🔎 Vector search using FAISS

---

## 🧠 Architecture Overview

```text
User Query
   ↓
FastAPI API
   ↓
RAG Pipeline
   ↓
FAISS (Vector Search)
   ↓
LLM (OpenAI)
   ↓
Response (Root Cause + Fix)
```

---

## 🛠️ Tech Stack

* Python (FastAPI)
* FAISS (Vector Database)
* LangChain
* OpenAI API
* Docker

---

## 📁 Project Structure

```
ai-devops-log-analyzer/
│
├── app/
│   ├── main.py
│   ├── rag_pipeline.py
│   ├── embeddings.py
│   ├── data_loader.py
│   └── config.py
│
├── data/
│   └── sample_logs.txt
│
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## ⚙️ Setup & Run

### 🔹 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-devops-log-analyzer.git
cd ai-devops-log-analyzer
```

---

### 🔹 2. Setup Environment

Create `.env` file:

```bash
OPENAI_API_KEY=your_api_key_here
```

---

### 🔹 3. Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Access:

```
http://localhost:8000/docs
```

---

### 🔹 4. Run with Docker

```bash
docker build -t ai-log-analyzer .
docker run -p 8001:8000 --env-file .env ai-log-analyzer
```

Access:

```
http://localhost:8001/docs
```

---

## 🧪 API Usage

### POST `/analyze`

#### Request:

```json
{
  "query": "Why is my pod restarting?"
}
```

#### Response:

```json
{
  "response": "Root cause: CrashLoopBackOff...\nSuggested fix: Check logs, memory limits..."
}
```

---

## 🚀 Future Improvements

* 🔗 Integration with Kubernetes logs
* 📊 Grafana / Prometheus integration
* 💬 Slack / ChatOps bot
* ☸️ Kubernetes deployment
* 📈 Advanced RAG optimization

---

## 💰 Use Case

* DevOps incident analysis
* SRE alert investigation
* Log intelligence systems
* Internal AI assistants

---

## 🧠 Key Concept

This project uses **RAG (Retrieval-Augmented Generation)**:

* Retrieves relevant logs
* Uses AI to generate accurate answers

---

## 🔐 Security Note

* API keys are managed via environment variables
* `.env` is excluded using `.gitignore`

---

## 👨‍💻 Author

**Narendra Gaddam**
DevOps | Cloud | SRE/PE | AI Enthusiast

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
