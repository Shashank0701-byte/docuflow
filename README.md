# 🚀 DocuFlow — Intelligent Invoice Ingestion Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Postgres](https://img.shields.io/badge/Postgres-Database-336791?logo=postgresql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Build-Passing-brightgreen)

DocuFlow is a containerized, event-driven pipeline that automates ingestion, OCR, parsing, and analytics for invoices and financial documents. It uses a lightweight microservice pattern so heavy OCR work runs asynchronously and does not block the UI.

Quick highlights:
- Hot-folder watcher for real-time ingestion
- Celery + Redis for asynchronous OCR and parsing
- Tesseract + Poppler for PDF/image text extraction
- PostgreSQL for persistent storage
- Streamlit dashboard for visualization and quick analysis

---

## 🏗️ Architecture

The system follows a microservices pattern and is orchestrated with Docker Compose.

If GitHub renders the diagram you will see the flow below. If it doesn't, a plain ASCII fallback is provided right after.

```mermaid
graph LR
  A[data_raw_hot_folder] -->|New PDF detected| B[watcher_service]
  B -->|Push task| C[redis_broker]
  C -->|Distribute task| D[celery_worker]
  D -->|Extract text| E[tesseract_poppler]
  D -->|Parse & save| F[postgres_db]
  F -->|Query| G[streamlit_dashboard]
```

Plain fallback (always visible):

```
Flow:
data/raw (Hot Folder) -> Watcher Service -> Redis (Broker) -> Celery Worker(s)
Celery Worker -> OCR (Tesseract + Poppler) -> Parse -> PostgreSQL -> Streamlit Dashboard
```

---

## ✨ Features

- Event-driven ingestion from a monitored "Hot Folder"
- Asynchronous processing using Celery + Redis for scalability and resiliency
- OCR pipeline: PDF -> images -> Tesseract (via pdf2image / Poppler)
- Regex-based parsing to extract Invoice Number, Date, Vendor, Total Amount
- Duplicate detection to avoid re-processing the same invoice
- Streamlit dashboard with charts, vendor breakdown, and recent transactions
- Cross-platform Docker Compose deployment

---

## 🛠️ Tech Stack

- Language: Python 3.11  
- Orchestration: Docker Compose  
- Broker: Redis  
- Database: PostgreSQL 15  
- Task Queue: Celery  
- OCR: Tesseract + Poppler (pdf2image)  
- Frontend: Streamlit  
- ORM: SQLAlchemy

---

## 📂 Project Structure

Use the ASCII tree below — it's intentionally plain so it displays consistently across renderers.

```
docuflow/
├── data/
│   └── raw/               # Drop PDFs here (Hot Folder)
├── src/
│   ├── core/
│   │   ├── ocr.py         # Tesseract / pdf2image logic
│   │   ├── parser.py      # Regex / parsing logic
│   │   └── database.py    # DB models & connection
│   ├── workers/
│   │   └── tasks.py       # Celery task definitions
│   ├── dashboard.py       # Streamlit UI
│   └── watcher.py         # Watchdog-based producer
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

Prerequisites
- Docker Desktop (Windows / Mac) or Docker + docker-compose (Linux).
- (Optional, for local non-Docker runs) Install system dependencies:
  - Tesseract (with language data)
  - Poppler (for pdf2image)
  - A running PostgreSQL instance (or let Docker Compose create one)

Clone the repository:
```bash
git clone https://github.com/Shashank0701-byte/docuflow.git
cd docuflow
```

Build and start the stack:
```bash
docker compose up --build
```

Wait until the logs show Celery worker(s) ready and the watcher reporting polling mode. Then open:
- Streamlit dashboard: http://localhost:8501

How to ingest:
- Copy or save a PDF invoice into `data/raw`. The watcher will detect the new file and queue processing.
- Watch logs:
  - Watcher: "New file detected"
  - Worker: "Celery task started" → "Saved to database"

Notes:
- For reliable parsing include human-readable tokens like "Invoice", "Date", and "Total".
- The watcher uses polling (compatible with many Docker/WSL setups); some file operations (rename/move) may not trigger events on certain host/volume configurations.

---

## 🔧 Configuration & Environment

Services are configured via environment variables in docker-compose. Typical variables:

- REDIS_URL (e.g., redis://redis:6379/0)  
- DATABASE_URL (e.g., postgresql://user:password@postgres:5432/docuflow)  
- CELERY_BROKER_URL (same as REDIS_URL)  
- CELERY_RESULT_BACKEND (same as REDIS_URL)

If you'd like, I can add a `.env.example` file with recommended values.

---

## 🧪 Troubleshooting

1. "New File Detected" doesn't trigger on Windows/WSL2:
   - The watcher uses a PollingObserver for compatibility. Ensure you place a brand-new file (copy/paste or create new). Renaming or moving files may not trigger events depending on host/volume behavior.

2. Diagram won't render on GitHub (Mermaid parse error):
   - GitHub's Mermaid renderer is strict. Avoid emojis, nested bracket/parenthesis node notation (e.g., don't use F[(PostgreSQL)]), and avoid certain special characters (&, +) inside node labels.
   - Use simple labels in nodes and put human-readable text on edge labels (as we do above).
   - If rendering still fails, use the plain ASCII fallback or include a pre-generated SVG/PNG diagram in the repo and reference it from the README.

3. Dashboard shows empty charts:
   - Ensure OCR succeeded. Inspect worker logs for parsing errors. Low-quality scans may yield poor OCR results.

4. Tesseract errors in Docker:
   - Confirm the Dockerfile installs Tesseract and Poppler. If errors persist, run Tesseract locally to check available language packs.

5. Duplicate invoice entries:
   - The system attempts deduplication using a composite identifier (hash or invoice number + vendor + date). If duplicates appear, review normalization logic in `src/core/parser.py`.

---

## 📈 Dashboard Overview

The Streamlit UI includes:
- Total spend over time
- Vendor breakdown and top vendors
- Recent parsed invoices with status and OCR logs
- Task logs (watcher & workers)

---

## 🛣️ Roadmap

- [ ] Integrate LLMs (OpenAI/Gemini) for complex invoice parsing  
- [ ] Email ingestion (auto-ingest invoices from mailbox)  
- [ ] User authentication for the dashboard  
- [ ] Add sample PDFs for testing and CI integration tests  
- [ ] CI pipeline and image scanning

---

## Contributing

Contributions welcome! Please open an issue or a PR.

Guidelines:
- Open an issue before large features (email ingestion, LLM parsing) to discuss design.
- Include tests where possible for parser changes.
- Use clear commit messages and reference related issues.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for full details.
