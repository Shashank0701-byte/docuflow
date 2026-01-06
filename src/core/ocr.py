import pytesseract
from pdf2image import convert_from_path
import os
import sys

# --- CONFIGURATION ---
# This logic handles both "Docker" (Linux) and "Local" (Windows) automatically.

# 1. Setup Tesseract Path
# If we are in Docker, this environment variable will exist.
tess_env = os.getenv('TESSERACT_CMD')
if tess_env:
    pytesseract.pytesseract.tesseract_cmd = tess_env
    print(f"🔧 Config: Using Docker Tesseract at {tess_env}")
else:
    # FALLBACK: Your specific Windows path
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print(f"🔧 Config: Using Windows Tesseract at {pytesseract.pytesseract.tesseract_cmd}")

# 2. Setup Poppler Path
poppler_env = os.getenv('POPPLER_PATH')
if poppler_env:
    # Linux/Docker usually puts poppler in the system path
    POPPLER_PATH = None
    print("🔧 Config: Using Docker Poppler (System Path)")
else:
    # FALLBACK: Your specific Windows path
    POPPLER_PATH = r'C:\Program Files\poppler-24.02.0\Library\bin'
    print(f"🔧 Config: Using Windows Poppler at {POPPLER_PATH}")


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Converts a PDF file to text using OCR.
    """
    # 1. Sanity Check: Does the file exist?
    if not os.path.exists(pdf_path):
        return f"❌ Error: File not found at {pdf_path}"

    print(f"📄 Processing: {pdf_path}...")
    
    try:
        # 2. Convert PDF pages to Images
        # We use the POPPLER_PATH variable we set up above
        images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
        
        full_text = ""
        
        # 3. Process each page
        for i, image in enumerate(images):
            print(f"   Scanning page {i + 1}...")
            text = pytesseract.image_to_string(image)
            full_text += f"\n--- Page {i + 1} ---\n{text}"
            
        return full_text

    except Exception as e:
        # If something breaks, return the error message so we see it
        return f"❌ Critical Error in OCR: {str(e)}"

if __name__ == "__main__":
    print("Don't run this file directly! Run 'python src/main.py' instead.")