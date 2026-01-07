# 🚀 DocuFlow — Intelligent Invoice Ingestion Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/Postgres-Database-336791?logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Build-Passing-brightgreen)

**DocuFlow** is a robust, containerized, event-driven data pipeline designed to automate the ingestion, processing, and analysis of financial documents. It leverages **Optical Character Recognition (OCR)** to extract unstructured data from PDF invoices and transforms it into structured insights via a real-time dashboard.

---

## 🏗️ Architecture

The system follows a microservices pattern orchestrated with Docker Compose.

```mermaid
graph LR
    A[📂 Data/Raw Folder] -->|New PDF Detected| B(🕵️ Watcher Service)
    B -->|Push Task| C{Redis Message Broker}
    C -->|Distribute Task| D[⚙️ Celery Worker]
    D -->|Extract Text| E[Tesseract OCR]
    D -->|Save Structured Data| F[(PostgreSQL DB)]
    F -->|Query Data| G[📊 Streamlit Dashboard]


✨ Key Features
Event-Driven Ingestion: Monitors a "Hot Folder" for new PDF files in real-time using watchdog (configured with Polling for WSL2/Docker compatibility).

Asynchronous Processing: Utilizes Celery and Redis to handle heavy OCR tasks in the background without blocking the main application.

OCR & Parsing: Integrates Tesseract OCR and Regex-based parsing logic to extract Invoice #, Date, Vendor, and Total Amount.

Data Integrity: Implements duplication checks to prevent processing the same invoice twice.

Analytics Dashboard: Interactive Streamlit UI with Plotly charts for spend analysis, vendor tracking, and real-time logs.

Cross-Platform Dockerization: Runs seamlessly on Windows, Linux, and Mac via Docker Compose, handling system-level dependencies (Poppler, Tesseract) automatically.

🛠️ Tech Stack

Component,Technology,Description
Language,Python 3.11,Core logic
Orchestration,Docker Compose,Multi-container management
Broker,Redis,Message queue for task distribution
Database,PostgreSQL 15,Persistent storage for invoice data
Task Queue,Celery,Async worker management
OCR Engine,Tesseract + Poppler,Text extraction from images/PDFs
Frontend,Streamlit,Data visualization dashboard
ORM,SQLAlchemy,Database interaction

📂 Project Structure

docuflow/
├── data/
│   └── raw/               # Drop PDFs here (Hot Folder)
├── src/
│   ├── core/
│   │   ├── ocr.py         # Tesseract / PDF2Image logic
│   │   ├── parser.py      # Regex / parsing logic
│   │   └── database.py    # DB models & connection
│   ├── workers/
│   │   └── tasks.py       # Celery task definitions
│   ├── dashboard.py       # Streamlit UI
│   └── watcher.py         # Watchdog script (Producer)
├── docker-compose.yml     # Infrastructure as Code
├── Dockerfile             # Container definition
└── requirements.txt       # Python dependencies



🚀 Getting Started
Prerequisites
- Docker Desktop (Windows / Mac) or Docker + docker-compose (Linux).
- (Optional, for local non-Docker runs) Install system dependencies:
  - Tesseract (with language data)
  - Poppler (for pdf2image)
  - PostgreSQL or a running Postgres instance

Clone the repository:
```bash
git clone https://github.com/Shashank0701-byte/docuflow.git
cd docuflow
```

Build and start the system:
```bash
docker compose up --build
```

Wait until logs show Celery worker(s) ready and the watcher reports polling mode. Then open:
- Streamlit dashboard: http://localhost:8501

🎮 Usage Guide
Ingest Data: Drag and drop any PDF invoice into the data/raw folder on your local machine. (Note: If testing with dummy files, ensure they contain text like "Invoice #", "Date", and "Total").

Watch the Magic:

Watcher Logs: Will trigger 👀 New file detected.

Worker Logs: Will trigger ⚡ Celery Task Started -> ✅ Saved to Database.

Analyze: Refresh the Dashboard to see the Total Spend, Vendor breakdown, and recent transactions update instantly.

🔧 Troubleshooting
1. "New File Detected" doesn't trigger on Windows/WSL2:
   - The watcher is configured to use PollingObserver for compatibility. Ensure you place a brand-new file in `data/raw` (copy/paste or create new file). Renaming existing files sometimes does not trigger events on some volumes.

2. Dashboard shows Empty Charts:

Solution: Ensure your PDFs are readable. The system handles NaN values gracefully, but if OCR fails completely, the amount defaults to 0.0.

🔮 Future Roadmap
[ ] Integration with LLMs (OpenAI/Gemini) for smarter parsing of non-standard invoices.

[ ] Email integration (auto-ingest from inbox).

[ ] User Authentication for the Dashboard.