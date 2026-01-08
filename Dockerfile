# 1. Base Image
FROM python:3.11-slim

# 2. Environment Config
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. System Dependencies (Linux)
# We need gcc and libpq-dev for the Postgres driver
# We need tesseract-ocr and poppler-utils for the OCR
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 4. Work Directory
WORKDIR /app

# 5. Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy Application Code
COPY . .

# 7. Create Data Directories
RUN mkdir -p data/raw data/archive

# 8. Default Command (Will be overridden by docker-compose)
CMD ["python", "src/dashboard.py"]