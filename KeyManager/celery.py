import os
from celery import Celery
import logging


logger = logging.getLogger(__name__)


os.environ.setdefault('DJANGO_SETTINGS_MODULE','KeyManager.settings')

try:
    celery_app = Celery('KeyManager')
    celery_app.config_from_object('django.conf:settings',namespace='CELERY')
    celery_app.autodiscover_tasks()
except Exception as e:
    logger.error(f"Error setting up celery app: - {e}")