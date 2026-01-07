# 🚀 DocuFlow — Intelligent Invoice Ingestion Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/Postgres-Database-336791?logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Build-Passing-brightgreen)

DocuFlow is a containerized, event-driven data pipeline that automates ingestion, OCR, parsing, and analytics for invoices and other financial documents. It uses a small microservice stack so heavy OCR work runs asynchronously without blocking the UI.

Quick highlights:
- Hot-folder watcher for real-time ingestion
- Celery + Redis for asynchronous OCR and parsing tasks
- Tesseract + Poppler for PDF/image text extraction
- PostgreSQL for structured invoice storage
- Streamlit dashboard for visualization and quick analysis

---

## 🏗️ Architecture

The system follows a microservices pattern orchestrated with Docker Compose.

```mermaid
graph LR
  A[data/raw (Hot Folder)] -->|New PDF detected| B[Watcher Service]
  B -->|Push Task| C[Redis (Broker)]
  C -->|Distribute Task| D[Celery Worker(s)]
  D -->|Extract Text| E[Tesseract OCR + Poppler]
  D -->|Parse & Save| F[(PostgreSQL)]
  F -->|Query| G[Streamlit Dashboard]
```

Key flow: drop a PDF into `data/raw` → watcher detects it → pushes a Celery task into Redis → worker runs OCR & parsing → stores normalized invoice rows in Postgres → dashboard reads and visualizes results.

---

## ✨ Features

- Event-driven ingestion from a monitored "Hot Folder"
- Asynchronous processing using Celery and Redis for scalability
- OCR (Tesseract) with PDF → image conversion (Poppler)
- Regex-based parsing to extract Invoice #, Date, Vendor, Total Amount
- Duplicate detection to avoid re-processing the same invoice
- Streamlit dashboard with charts and logs for real-time visibility
- Docker Compose-based cross-platform deployment

---

## 🛠️ Tech Stack

- Language: Python 3.11
- Orchestration: Docker Compose
- Broker: Redis
- Database: PostgreSQL 15
- Task Queue: Celery
- OCR: Tesseract + Poppler
- Frontend: Streamlit
- ORM: SQLAlchemy

---

## 📂 Project Structure

Use the tree below (plain ASCII) to avoid rendering issues:

```
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
│   └── watcher.py         # Watchdog-based producer
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## 🚀 Getting Started

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

How to ingest:
- Copy or save a PDF invoice into `data/raw`. The watcher will detect the new file and queue processing.
- Watch the service logs:
  - Watcher: "New file detected"
  - Worker: "Celery Task started" → "Saved to Database"

Notes:
- When testing, include human-readable text (e.g., "Invoice #", "Date", "Total") to help the parser.
- The watcher uses polling (compatible with WSL2/Docker on Windows); renaming/moving in some OSes may not trigger events—see troubleshooting below.

---

## 🔧 Configuration & Environment

Example environment variables used by the services in docker-compose:

- REDIS_URL (e.g., redis://redis:6379/0)
- DATABASE_URL (e.g., postgresql://user:password@postgres:5432/docuflow)
- CELERY_BROKER_URL (same as REDIS_URL)
- CELERY_RESULT_BACKEND (same as REDIS_URL)

If you'd like, I can add a `.env.example` with recommended values.

---

## 🧪 Troubleshooting

1. "New File Detected" doesn't trigger on Windows/WSL2:
   - The watcher is configured to use PollingObserver for compatibility. Ensure you place a brand-new file in `data/raw` (copy/paste or create new file). Renaming existing files sometimes does not trigger events on some volumes.

2. Dashboard shows empty charts:
   - Confirm files have text that Tesseract can read. Low-quality scans or images may produce poor OCR.
   - Check worker logs for parsing failures. If OCR fails completely, amounts may default to 0.0.

3. Tesseract errors in Docker:
   - Ensure the Docker image includes Tesseract and language packs. The provided Dockerfile should install Tesseract/Poppler. If not, add installation lines or use an image that bundles them.

4. Duplicate invoice detection:
   - The system uses an ID (hash or invoice number + vendor + date) to avoid duplicates. If duplicates are still appearing, check the parsing normalization logic in `parser.py`.

---

## 📈 Dashboard Overview

The Streamlit UI displays:
- Total spend over time
- Vendor breakdown and top vendors
- Recent parsed invoices with status and raw OCR logs
- Real-time task logs (watcher & worker)

---

## 🛣️ Roadmap

- [ ] Integrate LLMs (OpenAI/Gemini) for non-standard invoice parsing
- [ ] Email ingestion (auto-ingest invoices from mailbox)
- [ ] User authentication for the dashboard
- [ ] Add sample PDFs for testing and automated integration tests
- [ ] CI pipeline and image scanning

---

## Contributing

Contributions welcome! Open an issue or a PR:
- Preface PRs with a clear title and describe the changes.
- Add tests for parsing changes when possible.
- For large features (email ingestion, LLM parsing), open an issue first to discuss design.

---

## License

This project is available under the MIT License — see the included LICENSE file for details.
