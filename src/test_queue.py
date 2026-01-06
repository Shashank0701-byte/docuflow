from workers.tasks import process_document_task
import os

# Point to your sample invoice
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdf_path = os.path.join(base_dir, "data", "raw", "sample_invoice.pdf")

print("📨 Sending task to Redis queue...")

# .delay() is the magic command that sends it to the background
result = process_document_task.delay(pdf_path)

print(f"🎫 Task ID: {result.id}")
print("Check your Worker terminal to see it run!")