from celery import shared_task
from core.celery_config import app
from core.ocr import extract_text_from_pdf
from core.parser import parse_invoice_text
from core.database import SessionLocal, InvoiceDB  # <--- NEW IMPORTS
import os

@app.task(name='process_document')
def process_document_task(file_path: str):
    print(f"⚡ [Task Started] Processing: {file_path}")
    
    if not os.path.exists(file_path):
        return {"status": "error", "message": "File not found"}

    try:
        # 1. Run OCR
        raw_text = extract_text_from_pdf(file_path)
        
        # 2. Run Parser
        data = parse_invoice_text(raw_text)
        
        # 3. SAVE TO DATABASE (The New Part)
        print("💾 Saving to Database...")
        db = SessionLocal()
        try:
            new_invoice = InvoiceDB(
                filename=os.path.basename(file_path),
                invoice_number=data.invoice_number,
                vendor_name=data.vendor_name,
                invoice_date=data.invoice_date,
                total_amount=data.total_amount,
                raw_text=raw_text  # We save the raw text too, just in case!
            )
            db.add(new_invoice)
            db.commit()
            print(f"✅ Saved Invoice #{data.invoice_number} to DB with ID: {new_invoice.id}")
        except Exception as e:
            print(f"⚠️ Database Error: {e}")
            db.rollback()
        finally:
            db.close()
        
        # 4. Return Result
        return {"status": "success", "data": data.model_dump()}

    except Exception as e:
        print(f"❌ [Task Failed] {str(e)}")
        return {"status": "failed", "error": str(e)}