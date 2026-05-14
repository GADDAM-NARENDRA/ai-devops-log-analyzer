# 🚀 AI DevOps Log Analyzer (RAG-Based System)

An AI-powered DevOps assistant that analyzes logs and provides **root cause analysis** and **actionable fixes** using **Retrieval-Augmented Generation (RAG)**.

---

## 🔥 Features

* 🔍 **Intelligent Log Analysis** - AI-powered insights from multi-source logs
* 🧠 **Per-File Analysis** - Separate analysis for each log source with detailed reports
* 📊 **Real-time Statistics** - Error/Warning counts, critical ratio, file sizes
* 🔗 **Multi-Source Integration** - Loki, Prometheus, Grafana, custom logs
* 💡 **Root Cause Detection** - AI finds root causes from historical logs
* 🚀 **Suggested Fixes** - Actionable recommendations from AI analysis
* ⚡ **FastAPI REST API** - Production-ready endpoints
* 📱 **Beautiful Dashboard** - Responsive web UI for log analysis
* 🔄 **Continuous Monitoring** - Auto-fetch logs every 15 minutes
* 🐳 **Docker Ready** - Easy deployment with Docker
* 🔎 **Vector Search** - FAISS-based semantic search

---

## 🧠 Architecture Overview

```text
Multiple Log Sources (Loki, Prometheus, Grafana, Files)
   ↓
Fetch Logs API / Continuous Monitor
   ↓
Data Aggregation (data/ folder)
   ↓
FastAPI Application
   ├─ Per-File Analysis
   ├─ Summary & Statistics
   └─ RAG Pipeline
       ├─ Vector Embeddings (OpenAI)
       ├─ FAISS Vector Search
       └─ LLM Analysis (OpenAI)
   ↓
Beautiful Web Dashboard + REST API
   ↓
Root Cause Analysis + Actionable Fixes
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
│   ├── main.py                    # FastAPI application & REST endpoints
│   ├── rag_pipeline.py            # RAG pipeline with per-file analysis
│   ├── embeddings.py              # Vector embeddings with FAISS
│   ├── data_loader.py             # Multi-source log loader
│   ├── config.py                  # Configuration management
│   ├── loki_connector.py          # Loki API integration
│   ├── prometheus_connector.py    # Prometheus API integration
│   ├── grafana_connector.py       # Grafana API integration
│   ├── fetch_logs.py              # Log aggregation script
│   ├── continuous_monitor.py      # Background scheduler for monitoring
│   └── static/
│       └── index.html             # Web dashboard UI
│
├── data/
│   ├── sample_logs.txt            # Sample DevOps logs
│   ├── loki.log                   # Loki logs (auto-generated)
│   ├── prometheus.log             # Prometheus metrics (auto-generated)
│   └── grafana.log                # Grafana data (auto-generated)
│
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose (optional)
├── .env.example                   # Environment variables template
└── README.md                       # This file
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
# Build image
docker build -t ai-devops-analyzer .

# Run container
docker run -d \
  --name ai-analyzer \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key_here \
  -e LOKI_URL=http://localhost:3100 \
  -e PROMETHEUS_URL=http://localhost:9090 \
  -e GRAFANA_URL=http://localhost:3000 \
  ai-devops-analyzer
```

Access:

```
http://localhost:8000
```

---

## 🎯 Features

### ✨ **New Features Added**

1. **Multi-Source Log Integration**
   - Loki logs ingestion
   - Prometheus metrics & alerts
   - Grafana data sources & annotations
   - Traditional log files

2. **Beautiful Dashboard**
   - 🎨 Modern, responsive UI
   - 📊 Per-file analysis reports
   - 📈 Summary statistics and health metrics
   - 🔍 Query-based analysis across all logs

3. **Per-File Report Analysis**
   - Individual analysis for each log source
   - Separate health status per file
   - Error/Warning/Info counts
   - AI-powered recommendations per file

4. **Continuous Monitoring**
   - Auto-fetch logs every 15 minutes
   - Background scheduler (APScheduler)
   - Start/Stop monitoring via API
   - Status checking

5. **RESTful API Endpoints**
   - `/analyze` - Query-based analysis
   - `/analyze-files` - Per-file analysis
   - `/logs-summary` - Statistics and health
   - `/fetch-logs` - Manual log fetch
   - `/monitoring/*` - Monitoring control

---

## 🚀 Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Fetch logs from Loki, Prometheus, Grafana
python -m app.fetch_logs

# Or set environment variables
export LOKI_URL=http://localhost:3100
export PROMETHEUS_URL=http://localhost:9090
export GRAFANA_URL=http://localhost:3000
```

### 2. Run Server

```bash
# Start with monitoring
uvicorn app.main:app --reload

# Or run monitoring separately
python -m app.continuous_monitor
```

### 3. Access Dashboard

Open: **http://localhost:8000**

---

## 📋 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Web dashboard |
| `/analyze` | POST | Query-based analysis across all logs |
| `/analyze-files` | POST | Separate analysis for each log file |
| `/logs-summary` | GET | Statistics (errors, warnings, health) |
| `/fetch-logs` | POST | Manually fetch logs from external sources |
| `/monitoring/start` | POST | Start continuous monitoring |
| `/monitoring/stop` | POST | Stop continuous monitoring |
| `/monitoring/status` | GET | Check monitoring status |
| `/health` | GET | Health check |

---

## 📂 Log Files Analyzed

The analyzer automatically processes all logs in `data/` folder:

- **loki.log** - Application logs from Loki
- **prometheus.log** - Metrics and alerts from Prometheus
- **grafana.log** - Dashboards and events from Grafana
- **sample_logs.txt** - Sample DevOps logs

Each file is analyzed separately with specific insights and recommendations.

---

## 🔧 Configuration

Set these environment variables in `.env`:

```env
OPENAI_API_KEY=your_api_key_here
LOKI_URL=http://localhost:3100
PROMETHEUS_URL=http://localhost:9090
GRAFANA_URL=http://localhost:3000
GRAFANA_API_KEY=optional_api_key
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
