from celery import Celery
import os
import sys

# --- CRITICAL FIX: CONFIGURATION ---
# 1. Get the URLs from the Environment Variables (set in docker-compose)
# 2. If variables are missing (running on Windows), default to localhost
BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
BACKEND_URL = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

print(f"🔧 Worker Config: Connecting to Redis at {BROKER_URL}")

# 3. Initialize Celery with these specific URLs
app = Celery('docuflow', broker=BROKER_URL, backend=BACKEND_URL)

# --- OCR LOGIC (Keep your existing logic) ---
# We need to ensure OCR imports work inside the task
try:
    from core.ocr import extract_text_from_pdf
    from core.parser import parse_invoice
    from core.database import SessionLocal, InvoiceDB
except ImportError:
    # Fallback for different folder structures
    import sys
    sys.path.append('/app/src')
    from core.ocr import extract_text_from_pdf
    from core.parser import parse_invoice
    from core.database import SessionLocal, InvoiceDB

@app.task(name='workers.tasks.process_document')
def process_document(file_path):
    print(f"⚡ Celery Task Started: Processing {file_path}")
    
    try:
        # 1. Run OCR
        text = extract_text_from_pdf(file_path)
        print(f"   -> OCR Complete ({len(text)} chars)")

        # 2. Parse Data
        data = parse_invoice(text)
        print(f"   -> Extracted: {data}")

        # 3. Save to DB
        if data:
            db = SessionLocal()
            try:
                # Deduplication Check
                exists = db.query(InvoiceDB).filter_by(filename=os.path.basename(file_path)).first()
                if exists:
                    print(f"   -> ⚠️ Skipped: File already exists in DB.")
                    return "Skipped (Duplicate)"

                new_invoice = InvoiceDB(
                    filename=os.path.basename(file_path),
                    invoice_number=data.get('invoice_number'),
                    invoice_date=data.get('date'),
                    vendor_name=data.get('vendor'),
                    total_amount=data.get('total_amount')
                )
                db.add(new_invoice)
                db.commit()
                print("   -> ✅ Saved to Database!")
                return "Success"
            except Exception as e:
                print(f"   -> ❌ Database Error: {e}")
                db.rollback()
            finally:
                db.close()
        
    except Exception as e:
        print(f"   -> ❌ Task Failed: {e}")
        return f"Failed: {e}"