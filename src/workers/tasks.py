from celery import shared_task
from core.celery_config import app
from core.ocr import extract_text_from_pdf
from core.parser import parse_invoice_text
import os
import time

@app.task(name='process_document')
def process_document_task(file_path: str):
    """
    This function runs in the background.
    It receives a file path, processes it, and returns the result.
    """
    print(f"⚡ [Task Started] Processing: {file_path}")
    
    # 1. Check file existence
    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found"}

    try:
        # 2. Run OCR (The Eyes)
        raw_text = extract_text_from_pdf(file_path)
        
        # 3. Run Parser (The Brain)
        data = parse_invoice_text(raw_text)
        
        # 4. Return Result (for now, just print/return it)
        result = data.model_dump() # Convert Pydantic to JSON dict
        print(f"✅ [Task Finished] Invoice #{result.get('invoice_number')} processed.")
        
        return {"status": "success", "data": result}

    except Exception as e:
        print(f"❌ [Task Failed] {str(e)}")
        return {"status": "failed", "error": str(e)}