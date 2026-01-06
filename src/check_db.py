from core.database import SessionLocal, InvoiceDB

db = SessionLocal()
invoices = db.query(InvoiceDB).all()

print(f"\n📊 Total Invoices in DB: {len(invoices)}")
for inv in invoices:
    print("-" * 30)
    print(f"ID: {inv.id}")
    print(f"Vendor: {inv.vendor_name}")
    print(f"Total: ${inv.total_amount}")
    print(f"Filename: {inv.filename}")

db.close()