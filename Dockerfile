# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# --- System Dependencies ---
# Install Tesseract and Poppler (Linux versions)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# --- Python Dependencies ---
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Application Code ---
COPY . .

# Create the data directories inside the container
RUN mkdir -p data/raw data/archive

# Default command
CMD ["python", "src/main.py"]