import pytesseract
from pdf2image import convert_from_path
import os
import sys

# --- CONFIGURATION START ---

# 1. Capture Environment Variables
# We grab these immediately to decide if we are in Docker or Windows
env_tess = os.getenv('TESSERACT_CMD')
env_poppler = os.getenv('POPPLER_PATH')

# 2. DEBUG PRINT (Crucial for troubleshooting)
print(f"🔍 DEBUG: TESSERACT_CMD found: '{env_tess}'")
print(f"🔍 DEBUG: POPPLER_PATH found: '{env_poppler}'")

# 3. Apply Logic
if env_tess:
    # === DOCKER / LINUX MODE ===
    # If the environment variable exists, we TRUST it.
    pytesseract.pytesseract.tesseract_cmd = env_tess
    
    # If Poppler env is set, use it. If not, default to standard Linux path '/usr/bin'
    POPPLER_PATH = env_poppler if env_poppler else '/usr/bin'
    
    print(f"🔧 Config: Active Mode -> DOCKER/LINUX")
    print(f"   -> Tesseract: {pytesseract.pytesseract.tesseract_cmd}")
    print(f"   -> Poppler: {POPPLER_PATH}")

else:
    # === WINDOWS LOCAL MODE ===
    # Fallback for when you run 'python src/watcher.py' on your laptop
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    POPPLER_PATH = r'C:\Program Files\poppler-24.02.0\Library\bin'
    
    print(f"🔧 Config: Active Mode -> WINDOWS LOCAL")
    print(f"   -> Tesseract: {pytesseract.pytesseract.tesseract_cmd}")
    print(f"   -> Poppler: {POPPLER_PATH}")

# --- CONFIGURATION END ---


def extract_text_from_pdf(pdf_path):
    """
    Converts a PDF to images and then runs OCR on them.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")
    
    # Convert PDF to images
    try:
        images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    except Exception as e:
        print(f"❌ Poppler Error: {e}")
        # Hint for the user if it fails
        print("   -> Tip: Check if the POPPLER_PATH is correct for your OS.")
        raise e

    extracted_text = ""
    print(f"📄 Processing: {pdf_path}...")

    for i, image in enumerate(images):
        print(f"   Scanning page {i + 1}...")
        text = pytesseract.image_to_string(image)
        extracted_text += f"\n--- Page {i + 1} ---\n"
        extracted_text += text

    return extracted_text

if __name__ == "__main__":
    # Simple test to run this file directly
    if len(sys.argv) > 1:
        print(extract_text_from_pdf(sys.argv[1]))
    else:
        print("Usage: python ocr.py <path_to_pdf>")