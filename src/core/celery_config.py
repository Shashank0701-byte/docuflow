from celery import Celery
import os

# 1. Define the Broker URL
# "redis://localhost:6379/0" means:
# Protocol: redis
# Host: localhost (your running Docker container)
# Port: 6379
# DB: 0 (Default)
BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
BACKEND_URL = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# 2. Initialize the App
app = Celery(
    'docuflow',
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=['workers.tasks']  # We will create this file next
)

# 3. Configure Settings
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)