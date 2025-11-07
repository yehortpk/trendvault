import os
from celery import Celery

# Celery Configuration Options

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trendvault.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
