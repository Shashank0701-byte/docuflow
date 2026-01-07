import time
import os
import logging
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler

# --- FIX: IMPORT FROM 'WORKERS' NOT 'CORE' ---
# Your file tree shows the task is in src/workers/tasks.py
try:
    from workers.tasks import process_document
except ImportError:
    # Fallback in case you named the function 'process_document_task'
    from workers.tasks import process_document_task as process_document

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

WATCH_DIR = "/app/data/raw"

class InvoiceHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if not event.src_path.lower().endswith('.pdf'):
            return

        logger.info(f"👀 New file detected: {event.src_path}")
        
        time.sleep(1)
        
        # Send to Celery
        task = process_document.delay(event.src_path)
        logger.info(f"🚀 Sent to Queue. Task ID: {task.id}")

if __name__ == "__main__":
    if not os.path.exists(WATCH_DIR):
        os.makedirs(WATCH_DIR)

    event_handler = InvoiceHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_DIR, recursive=False)
    
    logger.info(f"🕵️  Watching folder (POLLING MODE): {WATCH_DIR}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()