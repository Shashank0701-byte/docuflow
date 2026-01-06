# DocuFlow: Intelligent Document Processing Pipeline

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Celery](https://img.shields.io/badge/Celery-Async_Queue-green)
![Redis](https://img.shields.io/badge/Redis-Broker-red)
![OCR](https://img.shields.io/badge/OCR-Tesseract-orange)

DocuFlow is an automated pipeline designed to ingest, process, and digitize invoices and financial documents. It eliminates manual data entry by extracting structured data (Invoices, Dates, Totals) from unstructured PDF attachments using OCR and Regex parsing.

## 🏗️ Architecture

The system follows a distributed microservices pattern:
1.  **Ingestion:** Listens for incoming documents (Email/Upload).
2.  **Queue:** Dispatches tasks to a Redis Queue to handle high throughput.
3.  **Worker:** A background Celery worker processes the OCR (Tesseract) and Parsing logic.
4.  **Storage:** Validated data is stored in PostgreSQL; invalid data is flagged for review.

## 🚀 Features
- **OCR Engine:** Converts PDF pages to high-resolution images and extracts text.
- **Smart Parsing:** Regex-based heuristic engine to identify financial metrics.
- **Data Validation:** Pydantic models ensure data integrity before storage.
- **Fault Tolerance:** Asynchronous processing prevents system bottlenecks.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (Installed and added to PATH)
- [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) (Required for PDF rendering)

### Local Setup (Windows)

1. **Clone the repository**
   ```bash
   git clone [https://github.com/yourusername/docuflow.git](https://github.com/yourusername/docuflow.git)
   cd docuflow
Create Virtual Environment

Bash

python -m venv venv
.\venv\Scripts\activate
Install Dependencies

Bash

pip install -r requirements.txt
Configure Environment Create a .env file and add your configuration (see .env.example).

Run the Processor

Bash

python src/main.py
🐳 Running with Docker
Build and run the containerized application:

Bash

docker build -t docuflow .
docker run -v $(pwd)/data:/app/data docuflow
