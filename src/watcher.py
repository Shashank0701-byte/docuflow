import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from workers.tasks import process_document_task

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        # 1. Ignore folders, only look at files
        if event.is_directory:
            return

        # 2. Only process PDFs
        if not event.src_path.lower().endswith('.pdf'):
            return

        print(f"👀 New file detected: {event.src_path}")
        
        # 3. Wait a second to ensure file copy is finished (Windows quirk)
        time.sleep(1)
        
        # 4. Send to Celery!
        task = process_document_task.delay(event.src_path)
        print(f"🚀 Sent to Queue. Task ID: {task.id}")

def start_watching():
    # Define the folder to watch
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    watch_folder = os.path.join(base_dir, "data", "raw")

    # Create the observer
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_folder, recursive=False)
    
    print(f"🕵️  Watching folder: {watch_folder}")
    print("Press Ctrl+C to stop.")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_watching()