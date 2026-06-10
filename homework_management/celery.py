import os
from celery import Celery

# Set default Django settings module for 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homework_management.settings')

app = Celery('homework_management')

# Load settings from django settings file, with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
