from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# Celery Configuration Options
app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
